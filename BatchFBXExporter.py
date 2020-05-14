import bpy
import os

#----------------------------------
# Properties for our exporter panel
#----------------------------------

class PathProperties(PropertyGroup):
    path : StringProperty(
        name="Export Directory Path",
        description="Path to export directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')

# Swap coordinates on all selected objects
def swap_axis():
    selection = bpy.context.selected_objects

    for obj in selection:
        
        bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', constraint_axis=(True, False, False))    # Rotate -90d in radians
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)                                              # Apply rotation
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', constraint_axis=(True, False, False))     # Rotate 90d in radians

# export to blend file location
def export_fbx(self, context):
    basedir = os.path.dirname(bpy.data.filepath)    # Change this to be a user defined path
    view_layer = bpy.context.view_layer

    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    for obj in selection:

        obj.select_set(True)

        name = bpy.path.clean_name(obj.name) # Remove any funky characters
        fn = os.path.join(basedir, name) # Decide file name, path
        
        # Export in .FBX, only Meshes, apply scale using FBX Scale Units
        bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, object_types={'MESH'}, apply_scale_options='FBX_SCALE_UNITS')

        obj.select_set(False)

        print("written:", fn) # Print what we created


    view_layer.objects.active = obj_active

    for obj in selection:
        obj.select_set(True)
        
classes = (
    PathProperties
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.fbx_exporter = PointerProperty(type=PathProperties)
    
    def unregister():
        from bpy.utils import unregister_class
        for cls in reversed(classes):
            unregister_class(cls)
        del bpy.types.Scene.fbx_exporter
        
if __name_ == "__main__":
    register()





    
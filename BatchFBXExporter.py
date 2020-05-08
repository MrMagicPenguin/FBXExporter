bl_info = {
    "name": "FBX Batch Exporter",
    "blender": (2, 80, 75),
    "category": "Object",

}

# exports each selected object into its own file

import bpy
import os

class FBXBatchExporter(bpy.types.Operator):
    """FBX Batch Exporter"""
    bl_idname = "object.fbx_batch_exporter"
    bl_label = "FBX Batch Exporter"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        # export to blend file location
        # Change this to be a user defined path
        basedir = os.path.dirname(bpy.data.filepath)

        view_layer = bpy.context.view_layer

        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects

        # Primary operator
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:

            obj.select_set(True)

            name = bpy.path.clean_name(obj.name) # Remove any funky characters
            fn = os.path.join(basedir, name)
            
            # Export in .FBX, only Meshes, apply scale using FBX Scale Units
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, object_types={'MESH'}, apply_scale_options='FBX_SCALE_UNITS')

            obj.select_set(False)

            print("written:", fn) # Print what we wrote


        view_layer.objects.active = obj_active

        for obj in selection:
            obj.select_set(True)
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(FBXBatchExporter)

def unregister():
    bpy.utils.unregister_class(FBXBatchExporter)
    
if __name__ == "__main__":
    register()


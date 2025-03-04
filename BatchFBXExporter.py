bl_info = {
    "name": "FBX Batcher",
    "description": "Description of this addon",
    "author": "Rug.",
    "version": (0, 0, 1),
    "blender": (2, 9, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Import-Export" }
    

import os
import bpy
from bpy.props import (
                StringProperty,
                PointerProperty,
                )
                
from bpy.types import (Panel, 
                Operator,
                AddonPreferences,
                PropertyGroup,
                )

#----------------------------------
# Properties for our exporter panel
#----------------------------------
class PathProperties(PropertyGroup):
    path : StringProperty(
        name="",
        description="Path to export directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
        
#----------------------------------
# Unity Conversion Operator
#----------------------------------
class BatchExporter_OT_swap_axis(bpy.types.Operator):
    """Swap coordinates on all selected objects"""
    bl_idname = "batchexporter.swapaxis" # Robot name
    bl_label = "Swap Axis" # Human name

    def execute(self, context):
        selection = bpy.context.selected_objects

        for obj in selection:
            
            bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', constraint_axis=(True, False, False))    # Rotate -90d in radians
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)                                              # Apply rotation
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', constraint_axis=(True, False, False))     # Rotate 90d in radians

        return {'FINISHED'}
#----------------------------------
# Export to FBX Operator
#----------------------------------
class BatchExporter_OT_export_fbx(bpy.types.Operator):
    """Export selection to FBX"""
    bl_idname = "batchexporter.export" # Robot name
    bl_label = "Export Selected"       # Human name
    
    def execute(self, context):
        
        # Get user defined path from PathProperties
        scn = context.scene
        abspath = bpy.path.abspath(scn.batch_exporter.path)
           
        view_layer = bpy.context.view_layer
        
        # Define selection
        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects

        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:

            obj.select_set(True)

            name = bpy.path.clean_name(obj.name) # Remove any funky characters
            fn = os.path.join(abspath, name) # Decide file name, path
            
            # Export in .FBX, only Meshes, apply scale using FBX Scale Units
            bpy.ops.export_scene.fbx(filepath= fn + ".fbx", use_selection=True, object_types={'MESH'}, apply_scale_options='FBX_SCALE_UNITS')
            # Deselect
            obj.select_set(False)

    #DEBUG PRINTING
            print("written:", fn) # Print what we created
            print(exportdir + " exportdir") # Plain exportdir variable printed
            print(stripexportdir + " Stripped exportdir") # exportdir after running rstrip


        view_layer.objects.active = obj_active

        for obj in selection:
            obj.select_set(True)
            
        return {'FINISHED'}


class OBJECT_PT_BatchExporterPanel(Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "FBX Batch Exporter"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Exporter"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        # Box to contain settings
        box = layout.box()
        box.label(text="Export Tools")
        box.operator("batchexporter.swapaxis")
        row = layout.row()
        box.label(text= "Export to...")
        row = layout.row()
        box.operator("batchexporter.export")
        
        scn = context.scene
        col = layout.column(align=True)
        col.prop(scn.batch_exporter, "path", text="")
        col.prop
        
        
        # print the path to the console
        print (scn.batch_exporter.path)
        
classes = (
    PathProperties,
    OBJECT_PT_BatchExporterPanel,
    BatchExporter_OT_swap_axis,
    BatchExporter_OT_export_fbx
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.batch_exporter = PointerProperty(type=PathProperties)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.fbx_exporter
        
if __name__ == "__main__":
    register()


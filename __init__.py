import bpy

#inverted mask from curve object
class CurvePolyinvert(bpy.types.Operator):
    """Canvas Flip Horizontal Macro"""
    bl_idname = "artist_panel.inverted_mask" # must match a operator
    bl_label = "Inverted Mask"
    bl_options = { 'REGISTER', 'UNDO' }
    
    @classmethod
    def poll(self, context):
        if context.active_object:
            return context.active_object.type == 'CURVE'
        else:
            return False
    
    def execute(self, context):
        
        scene = context.scene
        
        #with previous curve selected        
        #deselect and select points
        bpy.ops.curve.select_all(action='TOGGLE')
        bpy.ops.curve.select_all(action='TOGGLE')


        #close curve
        bpy.ops.curve.cyclic_toggle()
        bpy.ops.object.editmode_toggle()

        bpy.context.object.data.dimensions ='2D'
        #bpy.ops.object.select_all(action='TOGGLE')
        
        #gotta get the mesh plane and dup/convert to curve/obj mode
        #context is wrong
        context.active_object
        bpy.ops.object.select_by_type(type = 'MESH')
        
        #duplicate        
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
        
        #convert to curve
        bpy.ops.object.convert(target='CURVE')
        bpy.context.object.data.dimensions = '2D'
	
	    #deselect and select all curve
	    
        bpy.ops.object.select_all(action = 'TOGGLE')
        #select both curves
        bpy.ops.object.select_by_type(type = 'CURVE')
        #join
        bpy.ops.object.join()
        #convert to mesh
        bpy.ops.object.convert(target='MESH')
        #toggle to edit mode
        bpy.ops.object.editmode_toggle()
        #select all faces/mesh
        bpy.ops.mesh.select_all(action='TOGGLE')
        #project form camera view
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False, scale_to_bounds=False)
        #toggle obj mode
        bpy.ops.object.editmode_toggle()
        #toggle tex paint
        bpy.ops.paint.texture_paint_toggle()   
        
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.
                            
                            
                            
class TestPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Test Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Test Macros"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        row.label(text="Test Macros")
        
        row = layout.row()
        row.operator("artist_panel.inverted_mask", text = "Invert Mask", icon = 'CURVE_NCURVE')                            
                            
                            
                            
                            

                            
def register():
    bpy.utils.register_class(CurvePolyinvert)
    bpy.utils.register_class(TestPanel)
    
def unregister():
    bpy.utils.unregister_class(CurvePolyinvert)
    bpy.utils.unregister_class(TestPanel)
    
if __name__ == "__main__":
    register()

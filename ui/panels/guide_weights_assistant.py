import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide_weights

####### Weights assistant Guide

class BLENRIG_PT_lattices_guide(bpy.types.Panel):
    bl_label = "Weights Assistant Guide"
    bl_idname = "BLENRIG_PT_weights_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER",}


    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False

        obj = context.object
        valid_types = {'POSE','ARAMTURE', 'MESH', 'LATTICE', 'CURVE', 'SURFACE', 'EDIT_ARMATURE'}

        return obj or obj.type in valid_types

    def draw(self, context):
        layout = self.layout

        # if VIEW3D_OT_blenrig_guide_lattices.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'MDEF_Select_Body_Objects':
        #     steps = layout.column(align=True)
        #     box_set = steps.box()
        #     box_set.label(text='Define Object tha use Mesh Deform')
        #     box_set.operator("blenrig.add_body_modifiers", text = 'Set Body Objects')




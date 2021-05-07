import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide_datatransfer

####### Data Transfer assistant Guide

class BLENRIG_PT_datatransfer_guide(bpy.types.Panel):
    bl_label = "Data Transfer Assistant Guide"
    bl_idname = "BLENRIG_PT_datatransfer_guide"
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

        if VIEW3D_OT_blenrig_guide_datatransfer.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'DT_Edit_Face':
            steps = layout.column(align=True)
            box = steps.box()
            box.operator("blenrig.transfer_vgroups")
        if VIEW3D_OT_blenrig_guide_datatransfer.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'DT_Edit_Fingers':
            steps = layout.column(align=True)
            box = steps.box()
            box.operator("blenrig.transfer_vgroups")
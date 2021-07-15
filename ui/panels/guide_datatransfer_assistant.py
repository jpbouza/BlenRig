import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_datatransfer

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

        if VIEW3D_OT_blenrig_guide_datatransfer.instance and context.scene.blenrig_guide.guide_current_step == 'DT_Edit_Head':
            steps = layout.column(align=True)
            box_transfer = steps.box()
            box_transfer.label(text='Weights Transfer')
            box_transfer.operator("blenrig.guide_transfer_vgroups", text = 'Transfer Head Weights').body_area = 'head'
            row_options = box_transfer.row()
            col_ray = row_options.column()
            col_ray.label(text = 'Ray Distance:')
            col_ray.prop(context.scene.blenrig_guide, "transfer_ray_distance", text = '')
            col_mapping = row_options.column()
            col_mapping.label(text = 'Mapping:')
            col_mapping.prop(context.scene.blenrig_guide, "transfer_mapping", text =  '')
        if VIEW3D_OT_blenrig_guide_datatransfer.instance and context.scene.blenrig_guide.guide_current_step == 'DT_Edit_Hands':
            steps = layout.column(align=True)
            box_transfer = steps.box()
            box_transfer.label(text='Weights Transfer')
            box_transfer.operator("blenrig.guide_transfer_vgroups", text = 'Transfer Hand Weights').body_area = 'hands'
            row_options = box_transfer.row()
            col_ray = row_options.column()
            col_ray.label(text = 'Ray Distance:')
            col_ray.prop(context.scene.blenrig_guide, "transfer_ray_distance", text = '')
            col_mapping = row_options.column()
            col_mapping.label(text = 'Mapping:')
            col_mapping.prop(context.scene.blenrig_guide, "transfer_mapping", text =  '')

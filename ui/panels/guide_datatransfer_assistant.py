import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_datatransfer
from . assistant_base import BLENRIG_PT_guide_assistant

####### Data Transfer assistant Guide

class BLENRIG_PT_datatransfer_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Data Transfer Assistant Guide"
    bl_idname = "BLENRIG_PT_datatransfer_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"

    def draw(self, context):
        layout = self.layout
        if VIEW3D_OT_blenrig_guide_datatransfer.instance and context.scene.blenrig_guide.guide_current_step == 'DT_Select_Head':
            steps = layout.column(align=True)
            set_head = steps.box()
            set_head.label(text='Set Head Object')
            set_head.operator("blenrig.define_body_area", text = 'Define selected as Head Object').area = 'Head'
        if VIEW3D_OT_blenrig_guide_datatransfer.instance and context.scene.blenrig_guide.guide_current_step == 'DT_Select_Hands':
            steps = layout.column(align=True)
            set_head = steps.box()
            set_head.label(text='Set Hands Object')
            set_head.operator("blenrig.define_body_area", text = 'Define selected as Hands Object').area = 'Hands'
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


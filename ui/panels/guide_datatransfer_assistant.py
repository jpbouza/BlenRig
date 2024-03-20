import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_datatransfer
from . assistant_base import BLENRIG_PT_guide_assistant

####### Data Transfer assistant Guide

class BLENRIG_PT_datatransfer_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Data Transfer Assistant Guide"
    bl_idname = "BLENRIG_PT_datatransfer_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_datatransfer.is_instantiated(context):
            return

        guide_props = bpy.context.scene.blenrig_guide
        head_weights_model = guide_props.mdef_head_weights_transfer_obj
        hands_weights_model = guide_props.mdef_hands_weights_transfer_obj
        head_model = guide_props.character_head_obj
        hands_model = guide_props.character_hands_obj
        layout = self.layout
        if context.scene.blenrig_guide.guide_current_step == 'DT_Weight_Mesh_Shapekey_Head':
            steps = layout.column(align=True)
            box = steps.box()
            box.label(text="Head Weights Mesh Editing Options")
            mirror_row = box.row()
            if head_weights_model.mode == 'EDIT':
                mirror_row.prop(head_weights_model.data, "use_mirror_x", text='X-Mirror')
                mirror_row.prop(head_weights_model.data, "use_mirror_topology")
                mirror_row.prop(head_weights_model, "show_in_front")
                box.prop(head_weights_model, "display_type")
        if context.scene.blenrig_guide.guide_current_step == 'DT_Weight_Mesh_Shapekey_Hands':
            steps = layout.column(align=True)
            box = steps.box()
            box.label(text="Hands Weights Mesh Editing Options")
            mirror_row = box.row()
            if hands_weights_model.mode == 'EDIT':
                mirror_row.prop(hands_weights_model.data, "use_mirror_x", text='X-Mirror')
                mirror_row.prop(hands_weights_model.data, "use_mirror_topology")
                mirror_row.prop(hands_weights_model, "show_in_front")
                box.prop(hands_weights_model, "display_type")
        if context.scene.blenrig_guide.guide_current_step == 'DT_Select_Head':
            steps = layout.column(align=True)
            set_head = steps.box()
            set_head.label(text='Set Head Object')
            set_head.operator("blenrig.define_body_area", text = 'Define selected as Head Object').area = 'Head'
        if context.scene.blenrig_guide.guide_current_step == 'DT_Select_Hands':
            steps = layout.column(align=True)
            set_head = steps.box()
            set_head.label(text='Set Hands Object')
            set_head.operator("blenrig.define_body_area", text = 'Define selected as Hands Object').area = 'Hands'
        if context.scene.blenrig_guide.guide_current_step == 'DT_Edit_Head':
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
            steps = layout.column(align=True)
            box = steps.box()
            box.label(text="Head Weights Mesh Editing Options")
            mirror_row = box.row()
            if head_weights_model.mode == 'EDIT':
                mirror_row.prop(head_weights_model.data, "use_mirror_x", text='X-Mirror')
                mirror_row.prop(head_weights_model.data, "use_mirror_topology")
                mirror_row.prop(head_weights_model, "show_in_front")
            box.prop(head_weights_model, "display_type")
            box.separator()
            
            try:
                if head_model.mode == 'EDIT':
                    box = steps.box()
                    box.label(text="Character Head Editing Options")
                    mirror_row = box.row()
                    mirror_row.prop(head_model.data, "use_mirror_x", text='X-Mirror')
                    mirror_row.prop(head_model.data, "use_mirror_topology")
            except:
                pass

        if context.scene.blenrig_guide.guide_current_step == 'DT_Test_Face':
            steps = layout.column(align=True)
            box_modifiers = steps.box()
            box_modifiers.label(text='Face Deformation')
            box_modifiers.operator("blenrig.add_head_modifiers", text = 'Add Head Modifiers')
            box_modifiers.operator("blenrig.guide_transfer_test_rig", text = 'Test Defomation').bone = 'mouth_ctrl'
        if context.scene.blenrig_guide.guide_current_step == 'DT_Edit_Hands':
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
            steps = layout.column(align=True)
            box = steps.box()
            box.label(text="Hands Weights Mesh Editing Options")
            mirror_row = box.row()
            if hands_weights_model.mode == 'EDIT':
                mirror_row.prop(hands_weights_model.data, "use_mirror_x", text='X-Mirror')
                mirror_row.prop(hands_weights_model.data, "use_mirror_topology")
                mirror_row.prop(hands_weights_model, "show_in_front")
            box.prop(hands_weights_model, "display_type")
            box.separator()
            if hands_model.mode == 'EDIT':
                box = steps.box()
                box.label(text="Character Hands Editing Options")
                mirror_row = box.row()
                mirror_row.prop(hands_model.data, "use_mirror_x", text='X-Mirror')
                mirror_row.prop(hands_model.data, "use_mirror_topology")
        if context.scene.blenrig_guide.guide_current_step == 'DT_Test_Hands':
            steps = layout.column(align=True)
            box_modifiers = steps.box()
            box_modifiers.label(text='Hands Deformation')
            box_modifiers.operator("blenrig.add_hands_modifiers", text = 'Add Hands Modifiers')
            box_modifiers.separator()
            box_modifiers.operator("blenrig.guide_transfer_test_rig", text = 'Test Defomation').bone = 'hand_close_L'
        if context.scene.blenrig_guide.guide_current_step == 'DT_Eyes':
            steps = layout.column(align=True)
            box_modifiers = steps.box()
            box_modifiers.label(text='Eyes Deformation')
            box_modifiers.operator("blenrig.add_eyes_modifiers", text = 'Add Left Eye Modifiers').side = 'Left'
            box_modifiers.separator()
            box_modifiers.operator("blenrig.add_eyes_modifiers", text = 'Add Right Eye Modifiers').side = 'Right'
            box_modifiers.separator()
            box_modifiers.operator("blenrig.guide_transfer_test_rig", text = 'Test Defomation').bone = 'look'
        if context.scene.blenrig_guide.guide_current_step == 'DT_Inner_Mouth':
            steps = layout.column(align=True)
            box_modifiers = steps.box()
            box_modifiers.label(text='Inner Mouth Deformation')
            box_modifiers.operator("blenrig.add_teeth_modifiers", text = 'Add Inner Mouth Modifiers')
        if context.scene.blenrig_guide.guide_current_step == 'DT_Clean_Symmetry':
            steps = layout.column(align=True)
            box_modifiers = steps.box()
            box_modifiers.label(text='Clean Symmetry')
            box_modifiers.operator("blenrig.mirror_vertex_groups", text = 'Mirror All Vertex Groups').All=True


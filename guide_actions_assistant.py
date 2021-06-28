import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide_actions

####### Actions assistant Guide

class BLENRIG_PT_actions_guide(bpy.types.Panel):
    bl_label = "Actions Assistant Guide"
    bl_idname = "BLENRIG_PT_actions_guide"
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
        arm_obj_props = bpy.context.scene.blenrig_guide
        arm = context.active_object
        if hasattr(arm, 'pose'):
            pose = arm.pose

        layout = self.layout

        Face_Steps = ['ACTIONS_Eyelids_Up_Up', 'ACTIONS_Eyelids_Up_Down_1', 'ACTIONS_Eyelids_Up_Down_2', 'ACTIONS_Eyelids_Low_Down', 'ACTIONS_Eyelids_Low_Up_1', 'ACTIONS_Eyelids_Low_Up_2', 'ACTIONS_Eyelids_Out', 'ACTIONS_Eyelids_In',
        'ACTIONS_Cheek_Up', 'ACTIONS_Cheek_Down', 'ACTIONS_Cheek_Frown', 'ACTIONS_Nose_Frown', 'ACTIONS_Nose_Frown_Max', 'ACTIONS_Jaw_Down', 'ACTIONS_Jaw_Up', 'ACTIONS_Mouth_Corner_Out', 'ACTIONS_Mouth_Corner_In', 'ACTIONS_Mouth_Corner_Up',
        'ACTIONS_Mouth_Corner_Down', 'ACTIONS_Mouth_Corner_Back', 'ACTIONS_Mouth_Corner_Forw', 'ACTIONS_Mouth_Corner_Up_Out_Corrective', 'ACTIONS_Mouth_Corner_Down_Out_Corrective', 'ACTIONS_U_Thicker_Lips', 'ACTIONS_U_Thinner_Lips',
        'ACTIONS_U', 'ACTIONS_O', 'ACTIONS_M', 'ACTIONS_Mouth_Frown', 'ACTIONS_Chin_Frown_Up', 'ACTIONS_Chin_Frown_Down']

        if VIEW3D_OT_blenrig_guide_actions.instance:
            steps = layout.column(align=True)
            box = steps.box()
            box.prop(pose, "use_mirror_x")
            layout.row().prop(bpy.context.scene.blenrig_guide.arm_obj.data, "pose_position",text='Toggle Rest Pose', expand=True)
            for step in Face_Steps:
                if step == bpy.context.scene.blenrig_guide.guide_current_step:
                    box.prop(bpy.context.scene.blenrig_guide.arm_obj.data, "layers", index=27, text='Show Deformation Bones')

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Eyelids_Up_Up_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_eyelid_up_up")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Eyelids_Up_Down_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_eyelid_up_down")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Eyelids_Low_Down_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_eyelid_low_down")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Eyelids_Low_Up_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_eyelid_low_up")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Cheek_Up_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_cheek_up")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Cheek_Down_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_cheek_down")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Eyelids_Out':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_eyelid_out")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Eyelids_In':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_eyelid_in")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Nose_Frown_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_nose_frown")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Jaw_Down_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_jaw_down")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Jaw_Up_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_jaw_up")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Corner_Out_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_corner_out")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Corner_Up_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_corner_up")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Corner_Down_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_corner_down")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Corner_Back_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_corner_back")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Corner_Forw_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_corner_forw")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Corner_In_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_corner_in")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_U_O_M_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_u_o_m")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Mouth_Frown_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_mouth_frown")

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Chin_Frown_Range':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Range of Motion')
            box_set.prop(arm_obj_props, "guide_chin_frown")






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
        'ACTIONS_Cheek_Up', 'ACTIONS_Cheek_Down', 'ACTIONS_Cheek_Frown', 'ACTIONS_Nose_Frown', 'ACTIONS_Nose_Frown_Max']

        if VIEW3D_OT_blenrig_guide_actions.instance:
            steps = layout.column(align=True)
            box = steps.box()
            box.prop(pose, "use_mirror_x")
            box.prop(bpy.context.scene.blenrig_guide.arm_obj.data, "pose_position",text='Toggle Rest Pose')
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

            # box_set.prop(arm_obj_props, "guide_mouth_corner_out")
            # box_set.prop(arm_obj_props, "guide_mouth_corner_in")
            # box_set.prop(arm_obj_props, "guide_mouth_corner_up")
            # box_set.prop(arm_obj_props, "guide_mouth_corner_down")
            # box_set.prop(arm_obj_props, "guide_mouth_corner_back")
            # box_set.prop(arm_obj_props, "guide_mouth_corner_forw")
            # box_set.prop(arm_obj_props, "guide_jaw_up")
            # box_set.prop(arm_obj_props, "guide_jaw_down")
            # box_set.prop(arm_obj_props, "")
            # box_set.prop(arm_obj_props, "")
            # box_set.prop(arm_obj_props, "")
            # box_set.prop(arm_obj_props, "guide_mouth_frown")
            # box_set.prop(arm_obj_props, "guide_chin_frown")






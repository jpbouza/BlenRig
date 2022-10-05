import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_rig_settings
from . assistant_base import BLENRIG_PT_guide_assistant

####### Rig Advanced Settings assistant Guide

class BLENRIG_PT_rig_settings_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Rig Advanced Settings Assistant Guide"
    bl_idname = "BLENRIG_PT_rig_settings_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_rig_settings.is_instantiated(context):
            return

        guide_props = context.scene.blenrig_guide
        active = context.active_object
        active_mode = active.mode
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        steps = layout.column(align=True)
        box_display = steps.box()
        box_display.label(text='Display Options')
        row_display = box_display.row()
        row_display.prop(guide_props.arm_obj, "show_in_front")
        row_display.prop(guide_props.arm_obj.data, "display_type")
        steps.separator()
        #Shoulder Automatic Movement
        if guide_props.guide_current_step == 'SETTINGS_Shoulder_Movement':
            box_pose = steps.box()
            box_pose.label(text='Shoulder Automatic Movement', icon='MOD_ARMATURE')
            box_pose.prop(guide_props, 'guide_shoulder_auto_forw', text="Shoulder_L Forwards", toggle=True)
            box_pose.prop(guide_props, 'guide_shoulder_auto_back', text="Shoulder_L Backwards", toggle=True)
            box_pose.prop(guide_props, 'guide_shoulder_auto_up', text="Shoulder_L Upwards", toggle=True)
            box_pose.prop(guide_props, 'guide_shoulder_auto_down', text="Shoulder_L Downwards", toggle=True)
        #Torso Rotation
        if guide_props.guide_current_step == 'SETTINGS_Torso_Rotation':
            box_pose = steps.box()
            box_pose.label(text='Torso Rotation Rate:')
            box_pose.prop(p_bones['spine_3_fk'], '["fk_follow_main"]', text="Spine 3", toggle=True)
            box_pose.prop(p_bones['spine_2_fk'], '["fk_follow_main"]', text="Spine 2", toggle=True)
            box_pose.prop(p_bones['spine_1_fk'], '["fk_follow_main"]', text="Spine 1", toggle=True)
        #Neck Rotation
        if guide_props.guide_current_step == 'SETTINGS_Neck_Rotation':
            box_pose = steps.box()
            box_pose.label(text='Neck Rotation Rate:')
            box_pose.prop(p_bones['neck_3_fk'], '["fk_follow_main"]', text="Neck 3", toggle=True)
            box_pose.prop(p_bones['neck_2_fk'], '["fk_follow_main"]', text="Neck 2", toggle=True)
            box_pose.prop(p_bones['neck_1_fk'], '["fk_follow_main"]', text="Neck 1", toggle=True)
        #Torso Rotation
        if guide_props.guide_current_step == 'SETTINGS_Torso_Inv_Rotation':
            box_pose = steps.box()
            box_pose.label(text='Torso Rotation Rate:')
            box_pose.prop(p_bones['spine_3_fk_inv'], '["fk_follow_main"]', text="Spine 3", toggle=True)
            box_pose.prop(p_bones['spine_2_fk_inv'], '["fk_follow_main"]', text="Spine 2", toggle=True)
            box_pose.prop(p_bones['pelvis_ctrl'], '["fk_follow_main"]', text="Pelvis", toggle=True)
        #Torso Stretching
        if guide_props.guide_current_step == 'SETTINGS_Torso_Stretching':
            box_pose = steps.box()
            box_pose.label(text='Torso Stretching Curvature:')
            box_pose.prop(p_bones['properties_torso'], '["spine_mid_follow"]', text="Curve", toggle=True)
        #Pelvis Compensation
        if guide_props.guide_current_step == 'SETTINGS_Pelvis_Compensation':
            box_pose = steps.box()
            box_pose.label(text='Pelvis Compensation Movement:')
            box_pose.prop(p_bones['properties_torso'], '["pelvis_compensation"]', text="Rate", toggle=True)
        #Foot Roll
        if guide_props.guide_current_step == 'SETTINGS_Foot_Roll':
            box_pose = steps.box()
            box_pose.label(text='Foot Roll:')
            box_pose.prop(guide_props, 'guide_foot_roll_amp', text="Controller Rotation", toggle=True)
            box_pose.prop(guide_props, 'guide_foot_roll_toe_1', text="Joint 1 Raising Start Angle", toggle=True)
            box_pose.prop(guide_props, 'guide_foot_roll_toe_2', text="Joint 2 Raising Start Angle", toggle=True)
        #Volume Variation
        if guide_props.guide_current_step == 'SETTINGS_Volume_Variation':
            box_pose = steps.box()
            box_pose.label(text='Squash & Stretch Volume Variation:')
            box_pose.prop(guide_props, 'guide_vol_var_arms', text="Arm_L", toggle=True)
            box_pose.prop(guide_props, 'guide_vol_var_fingers', text="Fingers_L", toggle=True)
            box_pose.prop(guide_props, 'guide_vol_var_legs', text="Leg_L", toggle=True)
            box_pose.prop(guide_props, 'guide_vol_var_toes', text="Toes_L", toggle=True)
            box_pose.prop(p_bones['properties_torso'], 'volume_variation_torso', text="Torso", toggle=True)
            box_pose.prop(p_bones['properties_head'], 'volume_variation_neck', text="Neck", toggle=True)
            box_pose.prop(p_bones['properties_head'], 'volume_variation_head', text="Head", toggle=True)
        #Feet Floor
        if guide_props.guide_current_step == 'SETTINGS_Feet_Floor':
            box_pose = steps.box()
            box_pose.label(text='Feet Collision:')
            box_pose.prop(guide_props, 'guide_feet_floor', text="Foot_L", toggle=True)
        #Eyelids Floor
        if guide_props.guide_current_step == 'SETTINGS_Eyelids_Floor':
            box_pose = steps.box()
            box_pose.label(text='Eyelids Collision:')
            box_pose.prop(guide_props, 'guide_eyelid_1_floor', toggle=True)
            box_pose.prop(guide_props, 'guide_eyelid_2_floor', toggle=True)
            box_pose.prop(guide_props, 'guide_eyelid_3_floor', toggle=True)
        #Blink Rate
        if guide_props.guide_current_step == 'SETTINGS_Blink':
            box_pose = steps.box()
            box_pose.label(text='Blink Rate:')
            box_pose.prop(guide_props, 'blink_rate', toggle=True)
        #Eyelids Eye Follow
        if guide_props.guide_current_step == 'SETTINGS_Eyelids_Follow':
            box_pose = steps.box()
            box_pose.label(text='Eye Upwards Movement Follow:', icon='SORT_DESC')
            box_pose.prop(guide_props, 'guide_eyelid_up_up_follow', text='Upper Eyelid', toggle=True)
            box_pose.prop(guide_props, 'guide_eyelid_low_up_follow', text='Lower Eyelid', toggle=True)
            box_pose.label(text='Eye Upwards Downwards Follow:', icon='SORT_ASC')
            box_pose.prop(guide_props, 'guide_eyelid_up_down_follow', text='Upper Eyelid', toggle=True)
            box_pose.prop(guide_props, 'guide_eyelid_low_down_follow', text='Lower Eyelid', toggle=True)
        #Fleshy Eyes
        if guide_props.guide_current_step == 'SETTINGS_Fleshy_Eyes':
            box_pose = steps.box()
            box_pose.label(text='Fleshy Eyes:')
            box_pose.prop(guide_props, 'fleshy_eyes_rate', toggle=True)
        #Eyelid Cheek Follow
        if guide_props.guide_current_step == 'SETTINGS_Eyelids_Cheek_Follow':
            box_pose = steps.box()
            box_pose.label(text='Lower Eyelid Cheek Movement Follow:', icon='SORT_DESC')
            box_pose.prop(guide_props, 'guide_eyelid_auto_cheek', text='Cheek Follow', toggle=True)
        #Cheek Smile Follow
        if guide_props.guide_current_step == 'SETTINGS_Cheek_Smile_Follow':
            box_pose = steps.box()
            box_pose.label(text='Cheek Smile Movement Follow:', icon='SORT_DESC')
            box_pose.prop(guide_props, 'guide_cheek_auto_smile', text='Smile Follow', toggle=True)
        #Mouth Corner Auto Back
        if guide_props.guide_current_step == 'SETTINGS_Coner_Auto_Back':
            box_pose = steps.box()
            box_pose.label(text='Mouth Corner Backwards Tension:', icon='SORT_DESC')
            box_pose.prop(guide_props, 'guide_mouth_corner_auto_back', text='Backwards Tension', toggle=True)
        #Lips Floor
        if guide_props.guide_current_step == 'SETTINGS_Lips_Floor':
            box_pose = steps.box()
            box_pose.label(text='Lip Joints Collision:')
            box_pose.prop(p_bones["lip_up_ctrl_mstr_mid"].constraints["Floor_Lips"], 'offset', text='Lip Mid Floor Offset', toggle=True)
            box_pose.prop(guide_props, 'guide_lip_1_floor', toggle=True)
            box_pose.prop(guide_props, 'guide_lip_2_floor', toggle=True)
            box_pose.prop(guide_props, 'guide_lip_3_floor', toggle=True)
            box_pose.label(text='Lip Controller Collision:')
            box_pose.prop(p_bones["lip_up_ctrl"].constraints["Floor_Lips_NOREP"], 'offset', text='Lip Ctrl Floor Offset', toggle=True)
        #Lip Curvature
        if guide_props.guide_current_step == 'SETTINGS_Lip_Curvature':
            box_pose = steps.box()
            box_pose.label(text='Lip Curvature:')
            box_pose.prop(guide_props, 'guide_lips_motion_curvature', toggle=True)
            box_pose.label(text='Lip Joints Rigidity:')
            box_pose.prop(guide_props, 'guide_lip_1_rigidity', text='Joint 1 Rigidity', toggle=True)
            box_pose.prop(guide_props, 'guide_lip_2_rigidity', text='Joint 2 Rigidity', toggle=True)
            box_pose.prop(guide_props, 'guide_lip_3_rigidity', text='Joint 3 Rigidity', toggle=True)
            box_pose.label(text='Joints Override:')
            row_label = box_pose.row()
            row_label.label(text='')
            row_label.label(text='X')
            row_label.label(text='Y')
            row_label.label(text='Z')
            row_1 = box_pose.row()
            row_1.prop(guide_props, 'guide_lip_1_curvature_override', text='Joint 1 Override', toggle=True)
            row_2 = box_pose.row()
            row_2.prop(guide_props, 'guide_lip_2_curvature_override', text='Joint 2 Override', toggle=True)
            row_3 = box_pose.row()
            row_3.prop(guide_props, 'guide_lip_3_curvature_override', text='Joint 3 Override', toggle=True)


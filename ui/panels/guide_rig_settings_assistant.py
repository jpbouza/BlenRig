import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_rig_settings

####### Rig Advanced Settings assistant Guide

class BLENRIG_PT_rig_settings_guide(bpy.types.Panel):
    bl_label = "Rig Advanced Settings Assistant Guide"
    bl_idname = "BLENRIG_PT_rig_settings_guide"
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
        guide_props = context.scene.blenrig_guide
        active = context.active_object
        active_mode = active.mode
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        if VIEW3D_OT_blenrig_guide_rig_settings.instance:
            steps = layout.column(align=True)
            #Shoulder Automatic Movement
            if guide_props.guide_current_step == 'SETTINGS_Shoulder_Movement':
                box_pose = steps.box()
                box_pose.label(text='Shoulder Automatic Movement', icon='MOD_ARMATURE')
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_FORW_L"]', text="Shoulder_L Forwards", toggle=True)
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_BACK_L"]', text="Shoulder_L Backwards", toggle=True)
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_UP_L"]', text="Shoulder_L Upwards", toggle=True)
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_DOWN_L"]', text="Shoulder_L Downwards", toggle=True)
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
            #Pelvis Compensation
            if guide_props.guide_current_step == 'SETTINGS_Foot_Roll':
                box_pose = steps.box()
                box_pose.label(text='Foot Roll:')
                box_pose.prop(p_bones['foot_roll_ctrl_L'], '["FOOT_ROLL_AMPLITUD_L"]', text="Controller Rotation", toggle=True)
                box_pose.prop(p_bones['foot_roll_ctrl_L'], '["TOE_1_ROLL_START_L"]', text="Joint 1 Raising Start Angle", toggle=True)
                box_pose.prop(p_bones['foot_roll_ctrl_L'], '["TOE_2_ROLL_START_L"]', text="Joint 2 Raising Start Angle", toggle=True)
            #Volume Variation
            if guide_props.guide_current_step == 'SETTINGS_Volume_Variation':
                box_pose = steps.box()
                box_pose.label(text='Squash & Stretch Volume Variation:')
                box_pose.prop(p_bones['properties_arm_L'], 'volume_variation_arm_L', text="Arm_L", toggle=True)
                box_pose.prop(p_bones['properties_arm_L'], 'volume_variation_fingers_L', text="Fingers_L", toggle=True)
                box_pose.prop(p_bones['properties_leg_L'], 'volume_variation_leg_L', text="Leg_L", toggle=True)
                box_pose.prop(p_bones['properties_leg_L'], 'volume_variation_toes_L', text="Toes_L", toggle=True)
                box_pose.prop(p_bones['properties_torso'], 'volume_variation_torso', text="Torso", toggle=True)
                box_pose.prop(p_bones['properties_head'], 'volume_variation_neck', text="Neck", toggle=True)
                box_pose.prop(p_bones['properties_head'], 'volume_variation_head', text="Head", toggle=True)
            #Feet Floor
            if guide_props.guide_current_step == 'SETTINGS_Feet_Floor':
                box_pose = steps.box()
                box_pose.label(text='Feet Floor:')
                box_pose.prop(p_bones["sole_ctrl_L"].constraints["Floor_Foot_L_NOREP"], 'offset', text="Foot_L", toggle=True)


import bpy

####### Rig Body Settings

class BLENRIG_PT_Rig_Body_settings(bpy.types.Panel):
    bl_label = "Body Settings"
    bl_idname = "BLENRIG_PT_Rig_Body_settings"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False
        if not context.active_object:
            return False
        if (context.active_object.type in ["ARMATURE"]):
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                    for prop in context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True

    def draw(self, context):
        arm = context.active_object
        arm_data = context.active_object.data
        p_bones = arm.pose.bones
        layout = self.layout


        ####### Body Settings
        if "gui_rig_body" in arm_data:
            props = context.window_manager.blenrig_6_props
            box = layout.column()
            col = box.column()
            row = col.row()
        # expanded box
        # if "gui_rig_body" in arm_data and arm_data["gui_rig_body"]:
        #     row.operator("gui.blenrig_6_tabs", icon="OUTLINER_OB_ARMATURE", emboss = 1).tab = "gui_rig_body"
        #     row.label(text="BODY SETTINGS")
        #     col.separator()

        # IK Initial Rotation
        col.prop(props, "gui_body_ik_rot", text = 'IK:')
        if props.gui_body_ik_rot:
            box = col.box()
            box.label(text="IK Initial Rotation Override (Fix non bending IK):")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if '_R' in b.name:
                    for C in b.constraints:
                        if C.name == 'Ik_Initial_Rotation':
                            col_R.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)
            for b in p_bones:
                if '_L' in b.name:
                    for C in b.constraints:
                        if C.name == 'Ik_Initial_Rotation':
                            col_L.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)

        # Automated Movement
        col.prop(props, "gui_body_auto_move", text = 'Automated Movement:')
        if props.gui_body_auto_move:
            box = col.box()
            box.label(text="Shoulder Automatic Movement:")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_FORW_R"]', text="Shoulder_R Forwards", toggle=True)
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_BACK_R"]', text="Shoulder_R Backwards", toggle=True)
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_UP_R"]', text="Shoulder_R Upwards", toggle=True)
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_DOWN_R"]', text="Shoulder_R Downwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_FORW_L"]', text="Shoulder_L Forwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_BACK_L"]', text="Shoulder_L Backwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_UP_L"]', text="Shoulder_L Upwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_DOWN_L"]', text="Shoulder_L Downwards", toggle=True)
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text='Torso FK Ctrl Influence:')
            col_R.prop(p_bones['spine_1_fk'], '["fk_follow_main"]', text="Spine 1", toggle=True)
            col_R.prop(p_bones['spine_2_fk'], '["fk_follow_main"]', text="Spine 2", toggle=True)
            col_R.prop(p_bones['spine_3_fk'], '["fk_follow_main"]', text="Spine 3", toggle=True)
            col_R.label(text='Torso INV Ctrl Influence:')
            col_R.prop(p_bones['spine_3_fk_inv'], '["fk_follow_main"]', text="Spine 3 Inv", toggle=True)
            col_R.prop(p_bones['spine_2_fk_inv'], '["fk_follow_main"]', text="Spine 2 Inv", toggle=True)
            col_R.prop(p_bones['pelvis_ctrl'], '["fk_follow_main"]', text="Pelvis", toggle=True)
            col_L.label(text='Neck FK Ctrl Influence:')
            col_L.prop(p_bones['neck_1_fk'], '["fk_follow_main"]', text="Neck 1", toggle=True)
            col_L.prop(p_bones['neck_2_fk'], '["fk_follow_main"]', text="Neck 2", toggle=True)
            col_L.prop(p_bones['neck_3_fk'], '["fk_follow_main"]', text="Neck 3", toggle=True)

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text='Foot Roll R:')
            col_L.label(text='Foot Roll L:')
            for b in p_bones:
                if 'foot_roll_ctrl_R' in b.name:
                    for cust_prop in b.keys():
                        if 'ROLL' in cust_prop:
                            col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format((cust_prop).replace('_L', '')),  toggle=True)
            for b in p_bones:
                if 'foot_roll_ctrl_L' in b.name:
                    for cust_prop in b.keys():
                        if 'ROLL' in cust_prop:
                            col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format((cust_prop).replace('_L', '')),  toggle=True)

        # Realistic Joints
        col.prop(props, "gui_body_rj", text = 'Realistic Joints:')
        if props.gui_body_rj:
            box = col.box()
            box.label(text="Bone Displacement On Joint Rotation")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Arm_R")
            col_R.prop(p_bones['properties_arm_R'], '["realistic_joints_elbow_loc_R"]', text="Elbow_R Displacement 1", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], '["realistic_joints_elbow_rot_R"]', text="Elbow_R Displacement 2", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], '["realistic_joints_wrist_rot_R"]', text="Wrist_R Displacement 1", toggle=True)
            col_R.label(text="Fingers_R")
            row_1_R = col_R.row()
            row_1_R.prop(p_bones['properties_arm_R'], '["realistic_joints_fingers_loc_R"]', toggle=True, icon_only=True)
            row_2_R = col_R.row()
            row_2_R.prop(p_bones['properties_arm_R'], '["realistic_joints_fingers_rot_R"]', toggle=True, icon_only=True)

            col_R.separator()

            col_R.label(text="Leg_R")
            col_R.prop(p_bones['properties_leg_R'], '["realistic_joints_knee_loc_R"]', text="Knee_R Displacement 1", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], '["realistic_joints_knee_rot_R"]', text="Knee_R Displacement 2", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], '["realistic_joints_ankle_rot_R"]', text="Ankle_R Displacement 1", toggle=True)
            col_R.label(text="Toes_R")
            row_1_R = col_R.row()
            row_1_R.prop(p_bones['properties_leg_R'], '["realistic_joints_toes_loc_R"]', toggle=True, icon_only=True)
            row_2_R = col_R.row()
            row_2_R.prop(p_bones['properties_leg_R'], '["realistic_joints_toes_rot_R"]', toggle=True, icon_only=True)

            col_R.separator()

            col_L.label(text="Arm_L")
            col_L.prop(p_bones['properties_arm_L'], '["realistic_joints_elbow_loc_L"]', text="Elbow_L Displacement 1", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], '["realistic_joints_elbow_rot_L"]', text="Elbow_L Displacement 2", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], '["realistic_joints_wrist_rot_L"]', text="Wrist_L Displacement 1", toggle=True)
            col_L.label(text="Fingers_L")
            row_1_L = col_L.row()
            row_1_L.prop(p_bones['properties_arm_L'], '["realistic_joints_fingers_loc_L"]', toggle=True, icon_only=True)
            row_2_L = col_L.row()
            row_2_L.prop(p_bones['properties_arm_L'], '["realistic_joints_fingers_rot_L"]', toggle=True, icon_only=True)

            col_L.separator()

            col_L.label(text="Leg_L")
            col_L.prop(p_bones['properties_leg_L'], '["realistic_joints_knee_loc_L"]', text="Knee_L Displacement 1", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], '["realistic_joints_knee_rot_L"]', text="Knee_L Displacement 2", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], '["realistic_joints_ankle_rot_L"]', text="Ankle_L Displacement 1", toggle=True)
            col_L.label(text="Toes_L")
            row_1_L = col_L.row()
            row_1_L.prop(p_bones['properties_leg_L'], '["realistic_joints_toes_loc_L"]', toggle=True, icon_only=True)
            row_2_L = col_L.row()
            row_2_L.prop(p_bones['properties_leg_L'], '["realistic_joints_toes_rot_L"]', toggle=True, icon_only=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_rj_transforms", text = 'Set Realistic Joints')
            col_L.separator()

        # Bbones options
        col.prop(props, "gui_body_bbones", text = 'Bendy Bones Settings:')
        if props.gui_body_bbones:
            box = col.box()
            box.label(text="Volume Variation")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.prop(p_bones['properties_arm_R'], '["volume_variation_arm_R"]', text="Arm_R", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], '["volume_variation_fingers_R"]', text="Fingers_R", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], '["volume_variation_leg_R"]', text="Leg_R", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], '["volume_variation_toes_R"]', text="Toes_R", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], '["volume_variation_arm_L"]', text="Arm_L", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], '["volume_variation_fingers_L"]', text="Fingers_L", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], '["volume_variation_leg_L"]', text="Leg_L", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], '["volume_variation_toes_L"]', text="Toes_L", toggle=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_volume_variation", text = 'Set Volume Variation')

            box.label(text="Twist Rate")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.prop(p_bones['properties_arm_R'], '["twist_rate_arm_R"]', text="Arm_R", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], '["twist_rate_forearm_R"]', text="Forearm_R", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], '["twist_rate_thigh_R"]', text="Thigh_R", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], '["twist_rate_shin_R"]', text="Shin_R", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], '["twist_rate_arm_L"]', text="Arm_L", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], '["twist_rate_forearm_L"]', text="Forearm_L", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], '["twist_rate_thigh_L"]', text="Thigh_L", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], '["twist_rate_shin_L"]', text="Shin_L", toggle=True)

            box.separator()

        # Body Collisions offset
        col.prop(props, "gui_body_collisions", text = 'Body Collisions offset:')
        if props.gui_body_collisions:
            box = col.box()
            box.label(text="Feet Floor Offset")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if b.name == 'sole_ctrl_R':
                    for C in b.constraints:
                        if C.name == 'Floor_Foot_R_NOREP':
                            col_R.prop(C, 'offset', text = "Foot_R", toggle=True)
                if b.name == 'sole_ctrl_L':
                    for C in b.constraints:
                        if C.name == 'Floor_Foot_L_NOREP':
                            col_L.prop(C, 'offset', text = "Foot_L", toggle=True)

        # Body Toggles
        col.prop(props, "gui_body_toggles", text = 'Toggles:')
        if props.gui_body_toggles:
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if 'properties' in b.name:
                    if 'arm' in b.name:
                        if '_R' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_R.prop(b, '{}'.format(cust_prop))
            for b in p_bones:
                if 'properties' in b.name:
                    if 'leg' in b.name:
                        if '_R' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_R.prop(b, '{}'.format(cust_prop))
            for b in p_bones:
                if 'properties' in b.name:
                    if 'arm' in b.name:
                        if '_L' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_L.prop(b, '{}'.format(cust_prop))
            for b in p_bones:
                if 'properties' in b.name:
                    if 'leg' in b.name:
                        if '_L' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_L.prop(b, '{}'.format(cust_prop))

        # else:
        #     row.operator("gui.blenrig_6_tabs", icon="ARMATURE_DATA", emboss = 1).tab = "gui_rig_body"
        #     row.label(text="BODY SETTINGS")

    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='ARMATURE_DATA', icon_only= True)

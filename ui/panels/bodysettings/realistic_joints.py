import bpy

class BLENRIG_PT_Rig_Body_settings_realistic_joints(bpy.types.Panel):
    bl_label = "Realistic Joints:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_realistic_joints"
    bl_parent_id = "BLENRIG_PT_Rig_Body_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        arm = context.active_object
        arm_data = context.active_object.data
        p_bones = arm.pose.bones
        layout = self.layout

        if "gui_rig_body" in arm_data:
            props = context.window_manager.blenrig_6_props
            box = layout.column()
            col = box.column()
            row = col.row()

            # Realistic Joints
            box = col.box()
            box.label(text="Bone Displacement On Joint Rotation")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Arm_R")
            col_R.prop(p_bones['properties_arm_R'], 'realistic_joints_elbow_loc_R', text="Elbow_R Displacement 1", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], 'realistic_joints_elbow_rot_R', text="Elbow_R Displacement 2", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], 'realistic_joints_wrist_rot_R', text="Wrist_R Displacement 1", toggle=True)
            col_R.label(text="Fingers_R")
            row_1_R = col_R.row()
            row_1_R.prop(p_bones['properties_arm_R'], 'realistic_joints_fingers_loc_R', toggle=True, icon_only=True)
            row_2_R = col_R.row()
            row_2_R.prop(p_bones['properties_arm_R'], 'realistic_joints_fingers_rot_R', toggle=True, icon_only=True)

            col_R.separator()

            col_R.label(text="Leg_R")
            col_R.prop(p_bones['properties_leg_R'], 'realistic_joints_knee_loc_R', text="Knee_R Displacement 1", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], 'realistic_joints_knee_rot_R', text="Knee_R Displacement 2", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], 'realistic_joints_ankle_rot_R', text="Ankle_R Displacement 1", toggle=True)
            col_R.label(text="Toes_R")
            row_1_R = col_R.row()
            row_1_R.prop(p_bones['properties_leg_R'], 'realistic_joints_toes_loc_R', toggle=True, icon_only=True)
            row_2_R = col_R.row()
            row_2_R.prop(p_bones['properties_leg_R'], 'realistic_joints_toes_rot_R', toggle=True, icon_only=True)

            col_R.separator()

            col_R.operator("mirror.rj_constraints", text="Mirror Values to the Left Side", icon='MOD_MIRROR').to_side = 'R to L'

            col_R.separator()

            col_L.label(text="Arm_L")
            col_L.prop(p_bones['properties_arm_L'], 'realistic_joints_elbow_loc_L', text="Elbow_L Displacement 1", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], 'realistic_joints_elbow_rot_L', text="Elbow_L Displacement 2", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], 'realistic_joints_wrist_rot_L', text="Wrist_L Displacement 1", toggle=True)
            col_L.label(text="Fingers_L")
            row_1_L = col_L.row()
            row_1_L.prop(p_bones['properties_arm_L'], 'realistic_joints_fingers_loc_L', toggle=True, icon_only=True)
            row_2_L = col_L.row()
            row_2_L.prop(p_bones['properties_arm_L'], 'realistic_joints_fingers_rot_L', toggle=True, icon_only=True)

            col_L.separator()

            col_L.label(text="Leg_L")
            col_L.prop(p_bones['properties_leg_L'], 'realistic_joints_knee_loc_L', text="Knee_L Displacement 1", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], 'realistic_joints_knee_rot_L', text="Knee_L Displacement 2", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], 'realistic_joints_ankle_rot_L', text="Ankle_L Displacement 1", toggle=True)
            col_L.label(text="Toes_L")
            row_1_L = col_L.row()
            row_1_L.prop(p_bones['properties_leg_L'], 'realistic_joints_toes_loc_L', toggle=True, icon_only=True)
            row_2_L = col_L.row()
            row_2_L.prop(p_bones['properties_leg_L'], 'realistic_joints_toes_rot_L', toggle=True, icon_only=True)

            col_L.separator()

            col_L.operator("mirror.rj_constraints", text="Mirror Values to the Right Side", icon='MOD_MIRROR').to_side = 'L to R'

            col_L.separator()
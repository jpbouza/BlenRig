import bpy

class BLENRIG_PT_Rig_Body_settings_bendy_bones_settings(bpy.types.Panel):
    bl_label = "Body BBones Settings:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_bendy_bones_settings"
    bl_parent_id = "BLENRIG_PT_Rig_Body_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        
        if bpy.app.version < (3,0,0):
            bbone_curveiny = "bbone_curveiny"
            bbone_curveouty = "bbone_curveouty"
        else:
            bbone_curveouty = "bbone_curveoutz"
            bbone_curveiny = "bbone_curveinz"

        arm = context.active_object
        arm_data = context.active_object.data
        p_bones = arm.pose.bones
        layout = self.layout

        if "gui_rig_body" in arm_data:
            props = context.window_manager.blenrig_6_props
            box = layout.column()
            col = box.column()
            row = col.row()

            # Bbones options

            box = col.box()
            box.label(text="Volume Variation")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.prop(p_bones['properties_arm_R'], 'volume_variation_arm_R', text="Arm_R", toggle=True)
            col_R.prop(p_bones['properties_arm_R'], 'volume_variation_fingers_R', text="Fingers_R", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], 'volume_variation_leg_R', text="Leg_R", toggle=True)
            col_R.prop(p_bones['properties_leg_R'], 'volume_variation_toes_R', text="Toes_R", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], 'volume_variation_arm_L', text="Arm_L", toggle=True)
            col_L.prop(p_bones['properties_arm_L'], 'volume_variation_fingers_L', text="Fingers_L", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], 'volume_variation_leg_L', text="Leg_L", toggle=True)
            col_L.prop(p_bones['properties_leg_L'], 'volume_variation_toes_L', text="Toes_L", toggle=True)
            col_R.prop(p_bones['properties_torso'], 'volume_variation_torso', text="Torso", toggle=True)
            col_R.prop(p_bones['properties_head'], 'volume_variation_neck', text="Neck", toggle=True)
            col_L.prop(p_bones['properties_head'], 'volume_variation_head', text="Head", toggle=True)
            box.separator()

            box = col.box()
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

            box = col.box()
            box.label(text="Spine Curvature")
            row_props = box.row()
            col = row_props.column()
            try:
                col.prop(p_bones['spine_line'].bone, bbone_curveouty, text="Upper Curvature")
                col.prop(p_bones['spine_line'].bone, bbone_curveiny,  text="Lower Curvature")
            except:
                pass

            box.separator()
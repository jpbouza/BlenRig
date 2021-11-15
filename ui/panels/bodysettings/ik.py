import bpy

class BLENRIG_PT_Rig_Body_settings_ik(bpy.types.Panel):
    bl_label = "IK:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_ik"
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

        # IK Initial Rotation

            box = col.box()
            box.label(text="IK Initial Rotation Override (Fix non bending IK):")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if '_R' in b.name:
                    for C in b.constraints:
                        if C.name == 'IK_Initial_Rotation':
                            col_R.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)
            for b in p_bones:
                if '_L' in b.name:
                    for C in b.constraints:
                        if C.name == 'IK_Initial_Rotation':
                            col_L.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)
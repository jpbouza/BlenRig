import bpy

class BLENRIG_PT_Rig_Body_settings_body_collisions_offset(bpy.types.Panel):
    bl_label = "Body Collisions Offset:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_body_collisions_offset"
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

            # Body Collisions offset
            
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
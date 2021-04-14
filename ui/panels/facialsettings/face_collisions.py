import bpy

class BLENRIG_PT_Rig_Body_settings_face_collisions(bpy.types.Panel):
    bl_label = "Face Collisions offset:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_face_collisions"
    bl_parent_id = "BLENRIG_PT_Rig_Facial_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        arm_data = context.active_object.data
        if "gui_rig_face" in arm_data:
            layout = self.layout
            props = context.window_manager.blenrig_6_props
            p_bones = context.active_object.pose.bones
            box = layout.column()
            col = box.column()
            row = col.row()

            box = col.box()
            box.label(text="Eyelids Floor Offset")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.prop(p_bones['properties_head'], '["floor_offset_eyelid_R"]', text="Eyelids_R", toggle=True)
            col_L.prop(p_bones['properties_head'], '["floor_offset_eyelid_L"]', text="Eyelids_L", toggle=True)

            box.label(text="Lips Floor Offset")
            row_label = box.row()
            row_label.scale_y = 0.5
            row_label.label(text="Lip_3_R")
            row_label.label(text="Lip_2_R")
            row_label.label(text="Lip_1_R")
            row_label.label(text="Lip_Mid")
            row_label.label(text="Lip_1_L")
            row_label.label(text="Lip_2_L")
            row_label.label(text="Lip_1_L")
            row_lips = box.row()
            for b in p_bones:
                if b.name == 'lip_up_ctrl_3_mstr_R':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)
            for b in p_bones:
                if b.name == 'lip_up_ctrl_2_mstr_R':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)
            for b in p_bones:
                if b.name == 'lip_up_ctrl_1_mstr_R':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)
            for b in p_bones:
                if b.name == 'lip_up_ctrl_mstr_mid':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)
            for b in p_bones:
                if b.name == 'lip_up_ctrl_1_mstr_L':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)
            for b in p_bones:
                if b.name == 'lip_up_ctrl_2_mstr_L':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)
            for b in p_bones:
                if b.name == 'lip_up_ctrl_3_mstr_L':
                    for C in b.constraints:
                        if C.name == 'Floor_Lips':
                            row_lips.prop(C, 'offset', icon_only=True, toggle=True)

            col.separator()
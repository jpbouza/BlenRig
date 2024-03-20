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
            row_label = box.row()
            row_label.alignment = 'CENTER'
            row_label.label(text='Eyelids Floor Offset')
            row_props = box.row()
            col_R = row_props.column()
            col_R.alignment = 'CENTER'
            col_L = row_props.column()
            col_L.alignment = 'CENTER'
            row_props_R = col_R.row()
            row_props_L = col_L.row()
            #Right Side
            try:
                col_1 = row_props_R.column()
                col_1.label(text="Eyelid 3 R")
                col_1.prop(p_bones['eyelid_low_ctrl_3_mstr_R'].constraints["Floor_Eyelids_NOREP"], 'offset', text = ' ')
            except:
                pass
            try:
                col_2 = row_props_R.column()
                col_2.label(text="Eyelid 2 R")
                col_2.prop(p_bones['eyelid_low_ctrl_2_mstr_R'].constraints["Floor_Eyelids_NOREP"], 'offset', text = ' ')
            except:
                pass
            try:
                col_3 = row_props_R.column()
                col_3.label(text="Eyelid 1 R")
                col_3.prop(p_bones['eyelid_low_ctrl_1_mstr_R'].constraints["Floor_Eyelids_NOREP"], 'offset', text = ' ')
            except:
                pass
            #Left Side
            try:
                col_1 = row_props_L.column()
                col_1.label(text="Eyelid 3 L")
                col_1.prop(p_bones['eyelid_low_ctrl_3_mstr_L'].constraints["Floor_Eyelids_NOREP"], 'offset', text = ' ')
            except:
                pass
            try:
                col_2 = row_props_L.column()
                col_2.label(text="Eyelid 2 L")
                col_2.prop(p_bones['eyelid_low_ctrl_2_mstr_L'].constraints["Floor_Eyelids_NOREP"], 'offset', text = ' ')
            except:
                pass
            try:
                col_3 = row_props_L.column()
                col_3.label(text="Eyelid 1 L")
                col_3.prop(p_bones['eyelid_low_ctrl_1_mstr_L'].constraints["Floor_Eyelids_NOREP"], 'offset', text = ' ')
            except:
                pass

            row_label = box.row()
            row_label.alignment = 'CENTER'
            row_label.label(text='Lips Floor Offset')
            row_label = box.row()
            row_label.scale_y = 0.5
            row_label.label(text="Lip_3_R")
            row_label.label(text="Lip_2_R")
            row_label.label(text="Lip_1_R")
            row_label.label(text="Lip_Mid")
            row_label.label(text="Lip_1_L")
            row_label.label(text="Lip_2_L")
            row_label.label(text="Lip_3_L")
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
            row_lip_up = box.row()
            col_1 = row_lip_up.column()
            col_2 = row_lip_up.column()
            col_3 = row_lip_up.column()
            row_lip_up_ctrl = col_2.row()
            row_lip_up_ctrl.alignment = 'CENTER'
            row_lip_up_ctrl.scale_x = 0.33
            row_props = row_lip_up_ctrl.column()
            row_props.label(text='Lip Up Ctrl')
            try:
                row_props.prop(p_bones['lip_up_ctrl'].constraints["Floor_Lips_NOREP"], 'offset', text = ' ')
            except:
                pass
            col.separator()

            # Collisions Toggle
            head_col = col.box()
            head_col.scale_x = 1
            head_col.scale_y = 1
            head_col.alignment = 'CENTER'
            head_col.label(text='Collisions Toggles')
            teeth_row = head_col.row()
            col_1 = teeth_row.column()
            col_1.scale_x = 1
            col_1.scale_y = 1
            col_1.alignment = 'CENTER'
            col_2 = teeth_row.column()
            col_2.scale_x = 1
            col_2.scale_y = 1
            col_2.alignment = 'CENTER'
            col_1.prop(p_bones['eyelid_low_ctrl_R'], '["EYELID_FLOOR_TOGGLE_R"]', text="Eyelids R Floor", toggle=True)
            col_2.prop(p_bones['eyelid_low_ctrl_L'], '["EYELID_FLOOR_TOGGLE_L"]', text="Eyelids L Floor", toggle=True)
            col_1.prop(p_bones['mouth_ctrl'], '["LIPS_FLOOR_TOGGLE"]', text="Lips Floor", toggle=True)
            head_col.separator()

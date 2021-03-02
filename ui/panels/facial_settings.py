import bpy

####### Rig Facial Settings

class BLENRIG_PT_Rig_Facial_settings(bpy.types.Panel):
    bl_label = "Facial Settings"
    bl_idname = "BLENRIG_PT_Rig_Facial_settings"
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
        arm_data = context.active_object.data
        layout = self.layout

        ####### Facial Settings
        if "gui_rig_face" in arm_data:
            props = context.window_manager.blenrig_6_props
            p_bones = context.active_object.pose.bones
            box = layout.column()
            col = box.column()
            row = col.row()
        # expanded box
        # if "gui_rig_face" in arm_data and arm_data["gui_rig_face"]:
        #     row.operator("gui.blenrig_6_tabs", icon="MONKEY", emboss = 1).tab = "gui_rig_face"
        #     row.label(text="FACIAL SETTINGS")
        #     col.separator
        # Face movement ranges
        col.prop(props, "gui_face_movement_ranges", text = 'Facial Movement Ranges:')
        if props.gui_face_movement_ranges:
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Mouth_Corner_R")
            for b in p_bones:
                if 'mouth_corner' in b.name:
                    if '_R' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_R', '')),  toggle=True)
            col_L.label(text="Mouth_Corner_L")
            for b in p_bones:
                if 'mouth_corner' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_mouth_corners", text = 'Set Mouth Corners')

            box = col.box()
            box.label(text="Mouth_Ctrl")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if 'mouth_ctrl' in b.name:
                    for cust_prop in b.keys():
                        if 'OUT' in cust_prop:
                            col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                        if 'SMILE' in cust_prop:
                            col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                        if 'IN' in cust_prop:
                            col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                        if 'JAW' in cust_prop:
                            col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                        if 'U_M' in cust_prop:
                            col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                if 'maxi' in b.name:
                    for cust_prop in b.keys():
                        if 'ACTION' not in cust_prop:
                            if 'UP' in cust_prop:
                                col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                            if 'DOWN' in cust_prop:
                                col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_mouth_ctrl", text = 'Set Mouth Ctrl')

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Cheek_Ctrl_R")
            col_L.label(text="Cheek_Ctrl_L")
            for b in p_bones:
                if 'cheek_ctrl' in b.name:
                    if '_R'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_R', '').replace('_LIMIT', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_cheeks", text = 'Set Cheeks')

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Frowns_R")
            for b in p_bones:
                if 'mouth_frown' in b.name:
                    if '_R' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format('MOUTH_' + cust_prop.replace('_LIMIT_R', '')),  toggle=True)
            col_L.label(text="Frowns_L")
            for b in p_bones:
                if 'mouth_frown' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format('MOUTH_' + cust_prop.replace('_LIMIT_L', '')),  toggle=True)
            for b in p_bones:
                if 'nose_frown' in b.name:
                    if '_R' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format('NOSE_' + cust_prop.replace('_LIMIT_R', '')),  toggle=True)
            for b in p_bones:
                if 'nose_frown' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format('NOSE_' + cust_prop.replace('_LIMIT_L', '')),  toggle=True)
            for b in p_bones:
                if 'chin_frown' in b.name:
                    for cust_prop in b.keys():
                        if '_RNA_UI' not in cust_prop:
                            if 'ACTION' not in cust_prop:
                                col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format('CHIN_' + cust_prop.replace('_LIMIT', '')),  toggle=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_frowns", text = 'Set Frowns')

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Eyelid_Low_R")
            col_L.label(text="Eyelid_Low_L")
            for b in p_bones:
                if 'eyelid_low_ctrl' in b.name:
                    if '_R'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_R', '').replace('_LIMIT', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)
            col_R.label(text="Eyelid_Up_R")
            col_L.label(text="Eyelid_Up_L")
            for b in p_bones:
                if 'eyelid_up_ctrl' in b.name:
                    if '_R'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_R', '').replace('_LIMIT', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)
            row_set = box.row()
            row_set.alignment =  'CENTER'
            row_set.scale_x = 1
            row_set.operator("operator.set_eyelids", text = 'Set Eyelids')

        # Face action toggles
        col.prop(props, "gui_face_action_toggles", text = 'Action Toggles:')
        if props.gui_face_action_toggles:
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Mouth_Corner_R")
            for b in p_bones:
                if 'mouth_corner' in b.name:
                    if '_R' in b.name:
                        for cust_prop in b.keys():
                            if 'ACTION' in cust_prop:
                                col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '').replace('_R', '')),  toggle=True)
            col_L.label(text="Mouth_Corner_L")
            for b in p_bones:
                if 'mouth_corner' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if 'ACTION'in cust_prop:
                                col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '').replace('_L', '')),  toggle=True)
            box = col.box()
            box.label(text="Mouth_Ctrl")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if 'mouth_ctrl' in b.name:
                    for cust_prop in b.keys():
                        if 'ACTION' in cust_prop:
                            col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '')),  toggle=True)
                if 'maxi' in b.name:
                    for cust_prop in b.keys():
                        if 'ACTION' in cust_prop:
                            col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION', 'JAW')),  toggle=True)
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Cheek_Ctrl_R")
            col_L.label(text="Cheek_Ctrl_L")
            for b in p_bones:
                if 'cheek_ctrl' in b.name:
                    if '_R'in b.name:
                        for cust_prop in b.keys():
                            if 'ACTION' in cust_prop:
                                col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_R', '').replace('ACTION_', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if 'ACTION' in cust_prop:
                                col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '').replace('_L', '')),  toggle=True)

        # Lip Shaping
        col.prop(props, "gui_face_lip_shaping", text = 'Lip Shaping:')
        if props.gui_face_lip_shaping:
            box = col.box()
            row_props = box.row()
            col_1 = row_props.column()
            col_1.label(text="Follow Left Corner")
            col_2 = row_props.column()
            col_2.scale_x = 0.6
            col_2.label(text="X:")
            col_3 = row_props.column()
            col_3.label(text="Y:")
            col_3.scale_x = 0.6
            col_4 = row_props.column()
            col_4.label(text="Z:")
            col_4.scale_x = 0.6
            for b in p_bones:
                if 'lip_up_ctrl_1_mstr_L' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_low_ctrl_1_mstr_L' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_up_ctrl_2_mstr_L' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_low_ctrl_2_mstr_L' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_up_ctrl_3_mstr_L' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_low_ctrl_3_mstr_L' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            row_props = box.row()
            col_1 = row_props.column()
            col_1.label(text="Follow Right Corner")
            col_2 = row_props.column()
            col_2.scale_x = 0.6
            col_2.label(text="X:")
            col_3 = row_props.column()
            col_3.label(text="Y:")
            col_3.scale_x = 0.6
            col_4 = row_props.column()
            col_4.label(text="Z:")
            col_4.scale_x = 0.6
            for b in p_bones:
                if 'lip_up_ctrl_1_mstr_R' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_low_ctrl_1_mstr_R' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_up_ctrl_2_mstr_R' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_low_ctrl_2_mstr_R' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_up_ctrl_3_mstr_R' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
            for b in p_bones:
                if 'lip_low_ctrl_3_mstr_R' in b.name:
                    col_1.label(text="{}".format(b.name.replace('_mstr', '')))
                    for cust_prop in b.keys():
                        if '_X_' in cust_prop:
                            col_2.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True, toggle=True)
                        if '_Y_' in cust_prop:
                            col_3.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)
                        if '_Z_' in cust_prop:
                            col_4.prop(b, '["{}"]'.format(cust_prop), text = '%', icon_only = True,  toggle=True)

        # Face Collisions offset
        col.prop(props, "gui_face_collisions", text = 'Face Collisions offset:')
        if props.gui_face_collisions:
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

            # col.separator()

        # else:
        #     row.operator("gui.blenrig_6_tabs", icon="MESH_MONKEY", emboss = 1).tab = "gui_rig_face"
        #     row.label(text="FACIAL SETTINGS")


    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='MESH_MONKEY', icon_only= True)
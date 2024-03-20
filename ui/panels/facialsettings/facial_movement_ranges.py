import bpy

class BLENRIG_PT_Rig_Body_settings_facial_movement_ranges(bpy.types.Panel):
    bl_label = "Facial Movement Ranges:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_facial_movement_ranges"
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
                                    col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_R', '')),  toggle=True)
            col_L.label(text="Mouth_Corner_L")
            for b in p_bones:
                if 'mouth_corner' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)

            box = col.box()
            box.label(text="Mouth_Ctrl")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if 'mouth_ctrl' in b.name:
                    for cust_prop in b.keys():
                        if 'ACTION' not in cust_prop:
                            if 'FLESHY' not in cust_prop:
                                if 'OUT' in cust_prop:
                                    col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                                if 'SMILE' in cust_prop:
                                    col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                                if 'IN' in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                                if 'JAW' in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                                if 'U_M' in cust_prop:
                                    col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                if 'maxi' in b.name:
                    for cust_prop in b.keys():
                        if 'ACTION' not in cust_prop:
                            if 'UP' in cust_prop:
                                col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)
                            if 'DOWN' in cust_prop:
                                col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '')),  toggle=True)

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
                                    col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_R', '').replace('_LIMIT', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)

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
                                    col_R.prop(b, cust_prop, text = "{}".format('MOUTH_' + cust_prop.replace('_LIMIT_R', '')),  toggle=True)
            col_L.label(text="Frowns_L")
            for b in p_bones:
                if 'mouth_frown' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format('MOUTH_' + cust_prop.replace('_LIMIT_L', '')),  toggle=True)
            for b in p_bones:
                if 'nose_frown' in b.name:
                    if '_R' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, cust_prop, text = "{}".format('NOSE_' + cust_prop.replace('_LIMIT_R', '')),  toggle=True)
            for b in p_bones:
                if 'nose_frown' in b.name:
                    if '_L' in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format('NOSE_' + cust_prop.replace('_LIMIT_L', '')),  toggle=True)
            for b in p_bones:
                if 'chin_frown' in b.name:
                    for cust_prop in b.keys():
                        if '_RNA_UI' not in cust_prop:
                            if 'ACTION' not in cust_prop:
                                col_R.prop(b, cust_prop, text = "{}".format('CHIN_' + cust_prop.replace('_LIMIT', '')),  toggle=True)

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Eyelid_Up_R")
            col_L.label(text="Eyelid_Up_L")
            for b in p_bones:
                if 'eyelid_up_ctrl' in b.name:
                    if '_R'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_R', '').replace('_LIMIT', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)
            col_R.label(text="Eyelid_Low_R")
            col_L.label(text="Eyelid_Low_L")
            for b in p_bones:
                if 'eyelid_low_ctrl' in b.name:
                    if '_R'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    if 'FLOOR' not in cust_prop:
                                        col_R.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_R', '').replace('_LIMIT', '')),  toggle=True)
                    if '_L'in b.name:
                        for cust_prop in b.keys():
                            if '_RNA_UI' not in cust_prop:
                                if 'ACTION' not in cust_prop:
                                    if 'FLOOR' not in cust_prop:
                                        col_L.prop(b, cust_prop, text = "{}".format(cust_prop.replace('_LIMIT', '').replace('_L', '')),  toggle=True)

            # Fleshy Eyes
            box = col.box()
            box.label(text='Fleshy Eyes Rate')
            fleshy_row = box.row()
            col_1 = fleshy_row.column()
            col_1.scale_x = 1
            col_1.scale_y = 1
            col_1.alignment = 'CENTER'
            col_2 = fleshy_row.column()
            col_2.scale_x = 1
            col_2.scale_y = 1
            col_2.alignment = 'CENTER'
            col_1.prop(p_bones['look_R'], '["FLESHY_EYE_R"]', text="Eye_R", slider=True)
            col_2.prop(p_bones['look_L'], '["FLESHY_EYE_L"]', text="Eye_L", slider=True)
            box.separator()

            # Fleshy Mouth
            box = col.box()
            fleshy_row = box.row()
            col_2 = fleshy_row.column()
            col_2.label(text='Fleshy Mouth Rate')
            col_2.scale_x = 1
            col_2.scale_y = 1
            col_2.alignment = 'CENTER'
            try:
                col_2.prop(p_bones['mouth_ctrl'], '["FLESHY_MOUTH"]', text="Rate", slider=True)
            except:
                pass
            # Fleshy Nose
            col_1 = fleshy_row.column()
            col_1.label(text='Fleshy Nose Rate')
            col_1.scale_x = 1
            col_1.scale_y = 1
            col_1.alignment = 'CENTER'
            try:
                col_1.prop(p_bones['nose_ctrl'], '["FLESHY_NOSE"]', text="Rate", slider=True)
            except:
                pass

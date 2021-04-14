import bpy

class BLENRIG_PT_Rig_Body_settings_face_lip_shaping(bpy.types.Panel):
    bl_label = "Lip Shaping:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_face_lip_shaping"
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
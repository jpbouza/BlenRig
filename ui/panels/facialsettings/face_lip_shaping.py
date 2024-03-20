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

            #### Lips Rigidity ####
            box = col.box()
            row_label = box.row()
            row_label.alignment = 'CENTER'
            row_label.label(text='Lip Rigidity')
            row_props = box.row()
            col_R = row_props.column()
            col_R.alignment = 'CENTER'
            col_R.label(text = 'Right Side')
            col_L = row_props.column()
            col_L.alignment = 'CENTER'
            col_L.label(text = 'Left Side')
            row_props_R = col_R.row()
            row_props_L = col_L.row()
            #Right Side
            try:
                col_1 = row_props_R.column()
                col_1.label(text="Lip Up 3 R")
                col_1.prop(p_bones['lip_up_ctrl_3_str_R'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_2 = row_props_R.column()
                col_2.label(text="Lip Up 2 R")
                col_2.prop(p_bones['lip_up_ctrl_2_str_R'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_3 = row_props_R.column()
                col_3.label(text="Lip Up 1 R")
                col_3.prop(p_bones['lip_up_ctrl_1_str_R'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            row_props_R = col_R.row()
            try:
                col_1 = row_props_R.column()
                col_1.label(text="Lip Low 3 R")
                col_1.prop(p_bones['lip_low_ctrl_3_str_R'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_2 = row_props_R.column()
                col_2.label(text="Lip Low 2 R")
                col_2.prop(p_bones['lip_low_ctrl_2_str_R'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_3 = row_props_R.column()
                col_3.label(text="Lip Low 1 R")
                col_3.prop(p_bones['lip_low_ctrl_1_str_R'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            #Left Side
            try:
                col_1 = row_props_L.column()
                col_1.label(text="Lip Up 1 L")
                col_1.prop(p_bones['lip_up_ctrl_1_str_L'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_2 = row_props_L.column()
                col_2.label(text="Lip Up 2 L")
                col_2.prop(p_bones['lip_up_ctrl_2_str_L'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_3 = row_props_L.column()
                col_3.label(text="Lip Up 3 L")
                col_3.prop(p_bones['lip_up_ctrl_3_str_L'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            row_props_L = col_L.row()
            try:
                col_1 = row_props_L.column()
                col_1.label(text="Lip Low 1 L")
                col_1.prop(p_bones['lip_low_ctrl_1_str_L'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_2 = row_props_L.column()
                col_2.label(text="Lip Low 2 L")
                col_2.prop(p_bones['lip_low_ctrl_2_str_L'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass
            try:
                col_3 = row_props_L.column()
                col_3.label(text="Lip Low 3 L")
                col_3.prop(p_bones['lip_low_ctrl_3_str_L'].constraints["Limit Distance_NOREP"], 'influence', text = ' ')
            except:
                pass

            #### Lips Curvature ####
            box = col.box()
            row_label = box.row()
            row_label.alignment = 'CENTER'
            row_label.label(text='Lip Curvature')
            row_props = box.row()
            col_R = row_props.column()
            col_R.alignment = 'CENTER'
            col_R.label(text = 'Right Side')
            col_L = row_props.column()
            col_L.alignment = 'CENTER'
            col_L.label(text = 'Left Side')
            row_props_R = col_R.column()
            row_props_L = col_L.column()
            #Right Side
            try:
                row_props_R.prop(p_bones['lip_up_line_R'].bone, "bbone_easeout", text="Upper Lip R Curve Roundness")
            except:
                pass
            try:
                row_props_R.prop(p_bones['lip_zipper_line_R'].bone, "bbone_easeout", text="Zipper Lip R Curve Roundness")
            except:
                pass
            try:
                row_props_R.prop(p_bones['lip_low_line_R'].bone, "bbone_easeout", text="Lower Lip R Curve Roundness")
            except:
                pass
            #Left Side
            try:
                row_props_L.prop(p_bones['lip_up_line_L'].bone, "bbone_easeout", text="Upper Lip L Curve Roundness")
            except:
                pass
            try:
                row_props_L.prop(p_bones['lip_zipper_line_L'].bone, "bbone_easeout", text="Zipper Lip L Curve Roundness")
            except:
                pass
            try:
                row_props_L.prop(p_bones['lip_low_line_L'].bone, "bbone_easeout", text="Lower Lip L Curve Roundness")
            except:
                pass
            #### Movement Override ####
            box = col.box()
            row_label = box.row()
            row_label.alignment = 'CENTER'
            row_label.label(text='Movement Override')
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
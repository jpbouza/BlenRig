import bpy

class BLENRIG_PT_Rig_Body_settings_automated_movement(bpy.types.Panel):
    bl_label = "Automated Movement:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_automated_movement"
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

            box = col.box()
            box.label(text="Shoulder Automatic Movement:")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_FORW_R"]', text="Shoulder_R Forwards", toggle=True)
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_BACK_R"]', text="Shoulder_R Backwards", toggle=True)
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_UP_R"]', text="Shoulder_R Upwards", toggle=True)
            col_R.prop(p_bones['shoulder_R'], '["SHLDR_AUTO_DOWN_R"]', text="Shoulder_R Downwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_FORW_L"]', text="Shoulder_L Forwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_BACK_L"]', text="Shoulder_L Backwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_UP_L"]', text="Shoulder_L Upwards", toggle=True)
            col_L.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_DOWN_L"]', text="Shoulder_L Downwards", toggle=True)
            box = col.box()
            box.label(text="Elbow Pin:")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            try:
                col_R.prop(p_bones['shoulder_mstr_R'], 'ik_max_z', text="Shoulder L Down Limit", toggle=True)
            except:
                pass
            try:
                col_L.prop(p_bones['shoulder_mstr_L'], 'ik_min_z', text="Shoulder L Down Limit", toggle=True)
            except:
                pass
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text='Torso FK Ctrl Influence:')
            col_R.prop(p_bones['spine_1_fk'], '["fk_follow_main"]', text="Spine 1", toggle=True)
            col_R.prop(p_bones['spine_2_fk'], '["fk_follow_main"]', text="Spine 2", toggle=True)
            col_R.prop(p_bones['spine_3_fk'], '["fk_follow_main"]', text="Spine 3", toggle=True)
            col_R.label(text='Torso INV Ctrl Influence:')
            col_R.prop(p_bones['spine_3_fk_inv'], '["fk_follow_main"]', text="Spine 3 Inv", toggle=True)
            col_R.prop(p_bones['spine_2_fk_inv'], '["fk_follow_main"]', text="Spine 2 Inv", toggle=True)
            col_R.prop(p_bones['pelvis_ctrl'], '["fk_follow_main"]', text="Pelvis", toggle=True)
            col_L.label(text='Neck FK Ctrl Influence:')
            col_L.prop(p_bones['neck_1_fk'], '["fk_follow_main"]', text="Neck 1", toggle=True)
            col_L.prop(p_bones['neck_2_fk'], '["fk_follow_main"]', text="Neck 2", toggle=True)
            col_L.prop(p_bones['neck_3_fk'], '["fk_follow_main"]', text="Neck 3", toggle=True)
            try:
                col_L.label(text='Torso Stretching Curvature:')
                col_L.prop(p_bones['properties_torso'], '["spine_mid_follow"]', text="Curve", toggle=True)
            except:
                pass
            try:
                col_L.label(text='Pelvis Compensation Movement:')
                col_L.prop(p_bones['properties_torso'], '["pelvis_compensation"]', text="Rate", toggle=True)
            except:
                pass
            try:
                col_R.label(text='Organic Twisting:')
                col_R.prop(p_bones['properties_torso'], '["organic_spine"]', text="Spine", toggle=True)
                col_R.prop(p_bones['properties_head'], '["organic_neck"]', text="Neck", toggle=True)
            except:
                pass

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text='Foot Roll R:')
            col_L.label(text='Foot Roll L:')
            for b in p_bones:
                if 'foot_roll_ctrl_R' in b.name:
                    for cust_prop in b.keys():
                        if 'ROLL' in cust_prop:
                            col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format((cust_prop).replace('_L', '')),  toggle=True)
            for b in p_bones:
                if 'foot_roll_ctrl_L' in b.name:
                    for cust_prop in b.keys():
                        if 'ROLL' in cust_prop:
                            col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format((cust_prop).replace('_L', '')),  toggle=True)
import bpy

class BLENRIG_PT_Rig_Body_settings_face_action_toggles(bpy.types.Panel):
    bl_label = "Action Toggles:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_face_action_toggles"
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
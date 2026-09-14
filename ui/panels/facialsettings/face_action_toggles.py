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
            # for b in p_bones:
            #     if 'mouth_corner' in b.name:
            #         if '_R' in b.name:
            #             for cust_prop in b.keys():
            #                 if 'ACTION' in cust_prop:
            #                     col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '').replace('_R', '')),  toggle=True)

            col_R.prop(p_bones['properties_mouth'], '["ACTION_UP_TOGGLE_R"]', text="UP TOGGLE", toggle=True)
            col_R.prop(p_bones['properties_mouth'], '["ACTION_DOWN_TOGGLE_R"]', text="DOWN TOGGLE", toggle=True)
            col_R.prop(p_bones['properties_mouth'], '["ACTION_FORW_TOGGLE_R"]', text="FORW TOGGLE", toggle=True)
            col_R.prop(p_bones['properties_mouth'], '["ACTION_BACK_TOGGLE_R"]', text="BACK TOGGLE", toggle=True)
            col_R.prop(p_bones['properties_mouth'], '["ACTION_IN_TOGGLE_R"]', text="IN TOGGLE", toggle=True)
            col_R.prop(p_bones['properties_mouth'], '["ACTION_OUT_TOGGLE_R"]', text="OUT TOGGLE", toggle=True)   

            col_L.label(text="Mouth_Corner_L")
            # for b in p_bones:
            #     if 'mouth_corner' in b.name:
            #         if '_L' in b.name:
            #             for cust_prop in b.keys():
            #                 if 'ACTION'in cust_prop:
            #                     col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '').replace('_L', '')),  toggle=True)

            col_L.prop(p_bones['properties_mouth'], '["ACTION_UP_TOGGLE_L"]', text="UP TOGGLE", toggle=True)
            col_L.prop(p_bones['properties_mouth'], '["ACTION_DOWN_TOGGLE_L"]', text="DOWN TOGGLE", toggle=True)
            col_L.prop(p_bones['properties_mouth'], '["ACTION_FORW_TOGGLE_L"]', text="FORW TOGGLE", toggle=True)
            col_L.prop(p_bones['properties_mouth'], '["ACTION_BACK_TOGGLE_L"]', text="BACK TOGGLE", toggle=True)
            col_L.prop(p_bones['properties_mouth'], '["ACTION_IN_TOGGLE_L"]', text="IN TOGGLE", toggle=True)
            col_L.prop(p_bones['properties_mouth'], '["ACTION_OUT_TOGGLE_L"]', text="OUT TOGGLE", toggle=True)   

            box = col.box()
            box.label(text="Mouth_Ctrl")
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            # for b in p_bones:
            #     if 'mouth_ctrl' in b.name:
            #         for cust_prop in b.keys():
            #             if 'ACTION' in cust_prop:
            #                 col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '')),  toggle=True)

            col_R.prop(p_bones['properties_mouth'], '["CORRECTIVE_ACTIONS_TOGGLE"]', text="CORRECTIVE ACTIONS TOGGLE", toggle=True)
            col_R.prop(p_bones['properties_mouth'], '["U_O_M_ACTION_TOGGLE"]', text="U_O_M TOGGLE", toggle=True)

                # if 'maxi' in b.name:
                #     for cust_prop in b.keys():
                #         if 'ACTION' in cust_prop:
                #             col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION', 'JAW')),  toggle=True)

            col_L.prop(p_bones['properties_mouth'], '["ACTION_UP_DOWN_TOGGLE"]', text="JAW UP DOWN TOGGLE", toggle=True)

            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            col_R.label(text="Cheek_Ctrl_R")
            col_L.label(text="Cheek_Ctrl_L")
            # for b in p_bones:
            #     if 'cheek_ctrl' in b.name:
            #         if '_R'in b.name:
            #             for cust_prop in b.keys():
            #                 if 'ACTION' in cust_prop:
            #                     col_R.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('_R', '').replace('ACTION_', '')),  toggle=True)

            col_R.prop(p_bones['properties_cheek_R'], '["ACTION_CHEEK_TOGGLE_R"]', text="CHEEK TOGGLE", toggle=True)

                    # if '_L'in b.name:
                    #     for cust_prop in b.keys():
                    #         if 'ACTION' in cust_prop:
                    #             col_L.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('ACTION_', '').replace('_L', '')),  toggle=True)

            col_L.prop(p_bones['properties_cheek_L'], '["ACTION_CHEEK_TOGGLE_L"]', text="CHEEK TOGGLE", toggle=True)

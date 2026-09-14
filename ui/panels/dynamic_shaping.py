import bpy

####### Dynamic Shaping

class BLENRIG_PT_Dynamic_shaping(bpy.types.Panel):
    bl_label = "Dynamic Shaping"
    bl_idname = "BLENRIG_PT_Dynamic_shaping"
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
        arm = context.active_object
        arm_data = context.active_object.data
        p_bones = arm.pose.bones
        layout = self.layout

        ####### Dynamic Shaping
        if arm_data['rig_type'] == 'Biped':
            if str(arm_data['rig_version']) >= "1.1.0":
                if "gui_rig_dynamic" in arm_data:
                    box = layout.column()
                    col = box.column()
                    row = col.row()
                # expanded box
                # if "gui_rig_dynamic" in arm_data and arm_data["gui_rig_dynamic"]:
                #     row.operator("gui.blenrig_6_tabs", icon="OUTLINER_OB_ARMATURE", emboss = 1).tab = "gui_rig_dynamic"
                #     row.label(text="DYNAMIC SHAPING")
                #     col.separator
                #     box = col.box()
                row_props = row
                col_1 = row_props.column()
                col_1.scale_x = 0.5
                col_2 = row_props.column()
                col_2.label(text="Head:")
                col_2.scale_x = 2
                col_3 = row_props.column()
                col_3.scale_x = 0.5
                for b in p_bones:
                    if 'properties_head' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'head' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_head_', '')),  toggle=True)
                col_2.label(text="Neck:")
                for b in p_bones:
                    if 'properties_head' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'neck' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_neck_', '')),  toggle=True)
                row_props = box.row()
                col_1 = row_props.column()
                col_1.label(text="Arm_R:")
                col_2 = row_props.column()
                col_2.label(text="Torso:")
                col_3 = row_props.column()
                col_3.label(text="Arm_L:")
                for b in p_bones:
                    if 'properties_arm_R' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'forearm' not in cust_prop:
                                    if 'hand' not in  cust_prop:
                                        col_1.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_arm_', '')),  toggle=True)
                col_1.label(text="Forearm_R:")
                for b in p_bones:
                    if 'properties_arm_R' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'forearm' in cust_prop:
                                    col_1.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_forearm_', '')),  toggle=True)
                col_1.label(text="Hand_R:")
                for b in p_bones:
                    if 'properties_arm_R' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'hand' in cust_prop:
                                    col_1.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_hand_', '')),  toggle=True)
                for b in p_bones:
                    if 'properties_torso' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'torso' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_torso_', '')),  toggle=True)
                col_2.label(text="Chest:")
                for b in p_bones:
                    if 'properties_torso' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'chest' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_chest_', '')),  toggle=True)
                col_2.label(text="Ribs:")
                for b in p_bones:
                    if 'properties_torso' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'ribs' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_ribs_', '')),  toggle=True)
                col_2.label(text="waist:")
                for b in p_bones:
                    if 'properties_torso' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'waist' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_waist_', '')),  toggle=True)
                col_2.label(text="pelvis:")
                for b in p_bones:
                    if 'properties_torso' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'pelvis' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_pelvis_', '')),  toggle=True)
                for b in p_bones:
                    if 'properties_arm_L' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'forearm' not in cust_prop:
                                    if 'hand' not in  cust_prop:
                                        col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_arm_', '')),  toggle=True)
                col_3.label(text="Forearm_L:")
                for b in p_bones:
                    if 'properties_arm_L' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'forearm' in cust_prop:
                                    col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_forearm_', '')),  toggle=True)
                col_3.label(text="Hand_L:")
                for b in p_bones:
                    if 'properties_arm_L' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'hand' in cust_prop:
                                    col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_hand_', '')),  toggle=True)
                row_props = box.row()
                col_1 = row_props.column()
                col_2 = row_props.column()
                col_2.label(text="Leg_R:")
                col_2.scale_x = 4
                col_3 = row_props.column()
                col_3.label(text="Leg_L:")
                col_3.scale_x = 4
                col_4 = row_props.column()
                for b in p_bones:
                    if 'properties_leg_R' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'leg' in  cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_leg_', '')),  toggle=True)
                                if 'thigh' in  cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_thigh_', '')),  toggle=True)
                col_2.label(text="Shin_R:")
                for b in p_bones:
                    if 'properties_leg_R' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'shin' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_shin_', '')),  toggle=True)
                col_2.label(text="Foot_R:")
                for b in p_bones:
                    if 'properties_leg_R' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'foot' in cust_prop:
                                    col_2.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_foot_', '')),  toggle=True)
                for b in p_bones:
                    if 'properties_leg_L' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'leg' in  cust_prop:
                                    col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_leg_', '')),  toggle=True)
                                if 'thigh' in  cust_prop:
                                    col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_thigh_', '')),  toggle=True)
                col_3.label(text="Shin_L:")
                for b in p_bones:
                    if 'properties_leg_L' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'shin' in cust_prop:
                                    col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_shin_', '')),  toggle=True)
                col_3.label(text="Foot_L:")
                for b in p_bones:
                    if 'properties_leg_L' in b.name:
                        for cust_prop in b.keys():
                            if 'dynamic' in cust_prop:
                                if 'foot' in cust_prop:
                                    col_3.prop(b, '["{}"]'.format(cust_prop), text = "{}".format(cust_prop.replace('dynamic_foot_', '')),  toggle=True)
                box.separator()
                row_reset = box.row()
                row_reset.alignment =  'CENTER'
                row_reset.scale_x = 1
                row_reset.operator("blenrig.reset_dynamic_shaping")

            else:
                row.operator("gui.blenrig_6_tabs", icon="OUTLINER_DATA_ARMATURE", emboss = 1).tab = "gui_rig_dynamic"
                row.label(text="DYNAMIC SHAPING")

    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='OUTLINER_DATA_ARMATURE', icon_only= True)
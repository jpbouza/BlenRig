import bpy

class BLENRIG_PT_Rig_Body_settings_toggles(bpy.types.Panel):
    bl_label = "Toggles:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_toggles"
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

            # Body Toggles
            box = col.box()
            row_props = box.row()
            col_R = row_props.column()
            col_L = row_props.column()
            for b in p_bones:
                if 'properties' in b.name:
                    if 'arm' in b.name:
                        if '_R' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_R.prop(b, '{}'.format(cust_prop))
            for b in p_bones:
                if 'properties' in b.name:
                    if 'leg' in b.name:
                        if '_R' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_R.prop(b, '{}'.format(cust_prop))
            for b in p_bones:
                if 'properties' in b.name:
                    if 'arm' in b.name:
                        if '_L' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_L.prop(b, '{}'.format(cust_prop))
            for b in p_bones:
                if 'properties' in b.name:
                    if 'leg' in b.name:
                        if '_L' in b.name:
                            for cust_prop in b.keys():
                                if 'toggle' in cust_prop:
                                    col_L.prop(b, '{}'.format(cust_prop))
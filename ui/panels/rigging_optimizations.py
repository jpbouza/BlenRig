import bpy

####### Rig Optimizations

class BLENRIG_PT_Rigging_optimizations(bpy.types.Panel):
    bl_label = "Rigging Optimizations"
    bl_idname = "BLENRIG_PT_rigging_optimizations"
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

        # if "gui_rig_optimize" in arm_data:
        #     box = layout.column()
        #     col = box.column()
        #     row = col.row()
        # expanded box
        # if "gui_rig_optimize" in arm_data and arm_data["gui_rig_optimize"]:
            # row.operator("gui.blenrig_6_tabs", icon="TOOL_SETTINGS", emboss = 1).tab = "gui_rig_optimize"
            # row.label(text="RIG OPTIMIZATIONS")

        box = layout.column()
        col = box.column()

        col.separator
        row_props = col.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.prop(arm_data, 'toggle_face_drivers', text="Enable Face Drivers",)
        col_L.prop(arm_data, 'toggle_body_drivers', text="Enable Body Drivers",)

        if arm_data['rig_type'] == 'Biped':
            if str(arm_data['rig_version']) < "1.1.0":
                col_R.prop(arm_data, 'toggle_flex_drivers', text="Enable Flex Scaling",)
        if arm_data['rig_type'] == 'Biped':
            if str(arm_data['rig_version']) >= "1.1.0":
                col_R.prop(arm_data, 'toggle_dynamic_drivers', text="Enable Dynamic Scaling",)

    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='TOOL_SETTINGS', icon_only= True)
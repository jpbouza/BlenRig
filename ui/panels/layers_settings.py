import bpy

####### Layers Settings

class BLENRIG_PT_Rig_Layers_settings(bpy.types.Panel):
    bl_label = "Layers Settings"
    bl_idname = "BLENRIG_PT_Rig_Layers_settings"
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
        layout = self.layout
        arm_data = context.active_object.data

        # Layers Settings
        if "gui_rig_layers" in arm_data:
            box = layout.column()
            col = box.column()
            row = col.row()
        col.separator

        row_props = col.row()
        row_props.scale_y = 0.75
        row_props.scale_x = 1
        row_props.alignment = 'LEFT'
        row_props.prop(arm_data, '["layers_count"]', text="Layers", toggle=True)
        col.separator()
        col.label(text='Layers Names: (Always keep 32 items)')
        row_layers = col.row()
        row_layers.prop(arm_data, '["layer_list"]', text="", toggle=True)

    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='OUTLINER_OB_LATTICE', icon_only= True)

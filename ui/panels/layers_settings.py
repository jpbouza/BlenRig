import bpy

####### Layers Settings

class BLENRIG_PT_Rig_Layers_settings(bpy.types.Panel):
    bl_label = "Layers Settings"
    bl_idname = "BLENRIG_PT_Rig_Layers_settings"
    bl_parent_id = "BLENRIG_PT_BlenRig_5_general"
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
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
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
        # expanded box
        # if "gui_rig_layers" in arm_data and arm_data["gui_rig_layers"]:
            # row.operator("gui.blenrig_5_tabs", icon="RENDERLAYERS", emboss = 1).tab = "gui_rig_layers"
            # row.label(text="LAYERS SETTING")
        col.separator

        row_props = col.row()
        row_props.scale_y = 0.75
        row_props.scale_x = 1
        row_props.alignment = 'LEFT'
        row_props.prop(arm_data, '["layers_count"]', text="Layers", toggle=True)
        if arm_data['bone_auto_hide'] == 1:
            row_props.operator("gui.blenrig_5_tabs",text = "  Bone Auto Hiding", icon="CHECKBOX_HLT", emboss = 0).tab = "bone_auto_hide"
        else:
            row_props.operator("gui.blenrig_5_tabs",text = "  Bone Auto Hiding", icon="CHECKBOX_DEHLT", emboss = 0).tab = "bone_auto_hide"
        col.label(text='Layers Schemes:')
        row_schemes = col.row()
        row_schemes.operator("blenrig.layers_scheme_compact", text="Compact")
        row_schemes.operator("blenrig.layers_scheme_expanded", text="Expanded")
        col.label(text='Layers Names: (Always keep 32 items)')
        row_layers = col.row()
        row_layers.prop(arm_data, '["layer_list"]', text="", toggle=True)
        # else:
        #     row.operator("gui.blenrig_5_tabs", icon="RENDER_RESULT", emboss = 1).tab = "gui_rig_layers"
        #     row.label(text="LAYERS SETTING")

        def draw_header(self, context):
            scene  = context.scene
            layout = self.layout
            layout.emboss = 'NONE'
            row = layout.row(align=True)
            row.prop(scene, "name", icon='RENDER_RESULT', icon_only= True)
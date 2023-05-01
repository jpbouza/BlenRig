import bpy

# Layers Settings


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
        wm = context.window_manager
        blenrig_6_props = wm.blenrig_6_props

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
        # row_props.prop(arm_data, '["layers_count"]', text="Layers", toggle=True)
        # col.separator()
        # col.label(text='Layers Names: (Always keep 32 items)')
        # row_layers = col.row()
        # row_layers.prop(arm_data, '["layer_list"]', text="", toggle=True)

        renaming = col.box()
        renaming.label(text="Renaming Layers")
        renaming.prop(arm_data, '["layers_count"]', text="Maximum Layers", toggle=True)
        arm_layers = renaming.grid_flow(row_major=True, even_columns=True, even_rows=True, align=True, columns=3)
        arm_layers.scale_y = 0.9

        armature_names_layers = ["arm_layers_renaming_facial1",
                                 "arm_layers_renaming_facial2",
                                 "arm_layers_renaming_facial3",
                                 "arm_layers_renaming_arm_r_fk",
                                 "arm_layers_renaming_neck_fk",
                                 "arm_layers_renaming_arm_l_fk",
                                 "arm_layers_renaming_arm_r_ik",
                                 "arm_layers_renaming_torso_fk",
                                 "arm_layers_renaming_arm_l_ik",
                                 "arm_layers_renaming_fingers",
                                 "arm_layers_renaming_torso_inv",
                                 "arm_layers_renaming_fingers_ik",
                                 "arm_layers_renaming_leg_r_fk",
                                 "arm_layers_renaming_props",
                                 "arm_layers_renaming_leg_l_fk",
                                 "arm_layers_renaming_leg_r_ik",
                                 "arm_layers_renaming_extras",
                                 "arm_layers_renaming_leg_l_ik",
                                 "arm_layers_renaming_toes",
                                 "arm_layers_renaming_properties",
                                 "arm_layers_renaming_toes_fk",
                                 "arm_layers_renaming_toon_1",
                                 "arm_layers_renaming_toon_2",
                                 "arm_layers_renaming_scale",
                                 "arm_layers_renaming_optionals",
                                 "arm_layers_renaming_protected",
                                 "arm_layers_renaming_mech",
                                 "arm_layers_renaming_deformation",
                                 "arm_layers_renaming_actions",
                                 "arm_layers_renaming_bone_rolls",
                                 "arm_layers_renaming_snapping",
                                 "arm_layers_renaming_reproportion"]

        arm = context.active_object.data
        layers_count = arm["layers_count"]
        for idx, arm_prop in enumerate(armature_names_layers):
            if idx < layers_count:
                arm_layers.prop(blenrig_6_props, arm_prop, index=idx, text="")

    def draw_header(self, context):
        scene = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='OUTLINER_OB_LATTICE', icon_only=True)

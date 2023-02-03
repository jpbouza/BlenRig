import bpy

####### Rigging & Baking

class BLENRIG_PT_Rigging_and_baking(bpy.types.Panel):
    bl_label = "Rigging & Baking"
    bl_idname = "BLENRIG_PT_rigging_and_baking"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

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

        if "gui_rig_bake" in arm_data:
            props = context.window_manager.blenrig_6_props
            box = layout.column()
            col = box.column()
            row = col.row()

            box = col.row()
            box.prop(arm_data, 'reproportion', text="Reproportion Mode", toggle=True, icon_only=True, icon='SHADERFX')

            if context.mode in ['POSE','OBJECT']:
                if context.active_object.data.reproportion:
                    box = col.box()
                    row = box.row()
                    row.scale_x = 0.5
                    row.scale_y = 1.8
                    row.operator("blenrig.armature_baker_all_part_1", text="Bake All")

            elif context.mode in ['EDIT_ARMATURE']:
                if context.active_object.data.reproportion:
                    box = col.box()
                    row = box.row()
                    row.scale_x = 0.5
                    row.scale_y = 1.8
                    row.operator("blenrig.armature_baker_all_part_2", text="Custom Aligns")

        else:
            box.enabled = False

    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='PREFERENCES', icon_only= True)

################### Visual Assistant ##########################
class BLENRIG_PT_visual_assistant(bpy.types.Panel):
    bl_label = "Visual Assistant"
    bl_idname = "BLENRIG_PT_visual_assistant"
    bl_parent_id = "BLENRIG_PT_rigging_and_baking"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False
        if not context.active_object.data.layers[27]:
            return False
        if not context.mode in ['OBJECT','EDIT_ARMATURE']:
            return True

    def draw(self, context):
        arm_data = context.active_object.data
        layout = self.layout

        if "gui_rig_bake" in arm_data:
            box = layout.column()
            col = box.column()
            row = col.row()
            box = col.row()

            box = col.row()
            box.enabled = True
            ao = context.active_object
            if ao.type in ['ARMATURE']:
                visual_assistant = context.active_object.data.visual_assistant
            row = box.row(align=True)

            icon = 'HIDE_OFF' if not visual_assistant.right_side else 'HIDE_ON'
            row.prop(visual_assistant, "right_side", text="R_Side", icon=icon, toggle=True)
            icon = 'HIDE_OFF' if not visual_assistant.left_side else 'HIDE_ON'
            row.prop(visual_assistant, "left_side", text="L_Side", icon=icon, toggle=True)

            box = col.row()
            box.use_property_split = True
            box.use_property_decorate = False

            flow = box.grid_flow(align=True)

            col = flow.column()
            icon = 'HIDE_ON' if not visual_assistant.eyes else 'HIDE_OFF'
            col.prop(visual_assistant, "eyes", icon=icon, text="Eyes", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.face else 'HIDE_OFF'
            col.prop(visual_assistant, "face", icon=icon, text="Face", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.face_controls else 'HIDE_OFF'
            col.prop(visual_assistant, "face_controls", icon=icon , text="Face Controls", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.eyebrows else 'HIDE_OFF'
            col.prop(visual_assistant, "eyebrows", icon=icon, text="Eyerbrows", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.lips else 'HIDE_OFF'
            col.prop(visual_assistant, "lips", icon=icon , text="Lips", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.face_mech else 'HIDE_OFF'
            col.prop(visual_assistant, "face_mech", icon=icon, text="Face Mech", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.inner_mouth else 'HIDE_OFF'
            col.prop(visual_assistant, "inner_mouth", icon=icon, text="Inner Mouth", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.hands else 'HIDE_OFF'
            col.prop(visual_assistant, "hands", icon=icon, text="Hands", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.toes else 'HIDE_OFF'
            col.prop(visual_assistant, "toes", icon=icon, text="Toes", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.body else 'HIDE_OFF'
            col.prop(visual_assistant, "body", icon=icon, text="Body", toggle=True)

            icon = 'HIDE_ON' if not visual_assistant.others else 'HIDE_OFF'
            col.prop(visual_assistant, "others", icon=icon, text="Others", toggle=True)

class BLENRIG_PT_baking(bpy.types.Panel):
    bl_label = "Advanced Baking"
    bl_idname = "BLENRIG_PT_baking"
    bl_parent_id = "BLENRIG_PT_rigging_and_baking"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if not context.mode in ['OBJECT']:
            return True

    def draw(self, context):
        arm_data = context.active_object.data
        layout = self.layout

        if "gui_rig_bake" in arm_data:
            props = context.window_manager.blenrig_6_props
            box = layout.column()
            col = box.column()
            row = col.row()

            box = col.row()

            box.enabled = True
            col.label(text="Baking:")

            box = col.row()
            row = box.row()
            row.operator("blenrig.advanced_armature_baker", text="Bake Armature")

            box = col.row()
            box.label(text="Fix Alignment:")
            box = col.row()

            row = box.row()
            row.operator("blenrig.fix_misaligned_bones", text="Fix Joints")
            row.operator("blenrig.auto_bone_roll", text="Calc Rolls")
            row.operator("blenrig.custom_bone_roll", text="Custom Aligns")

            box = col.row()
            row = box.row()
            row.operator("blenrig.store_roll_angles", text="Store Roll Angles")
            row.operator("blenrig.restore_roll_angles", text="Restore Roll Angles")

            box = col.row()
            box.use_property_split = True
            box.use_property_decorate = False

            flow = box.grid_flow(align=True)
            col = flow.column()

            col.prop(props, "align_selected_only", text="Selected Bones Only")
            col.prop(arm_data, "use_mirror_x", text="X-Axis Mirror")
            col.prop(arm_data, "show_axes", text="Display Axes")

            col.label(text="Extras:")
            box = layout.column()
            row = box.row()
            row.operator("blenrig.reset_constraints", text="BlenRig 6 Reset Constraints")
            row.operator("blenrig.reset_deformers", text="Reset Deformers")
            row = box.row()
            row.operator("blenrig.calculate_pole_angles", text="Calculate Pole Angles")
            row.operator("blenrig.calculate_floor_offsets", text="Calculate Floor Offsets")
            row = box.row()
            row.operator("blenrig.set_blenrig_armature", text="Set Armature as BlenRig Armature")
        else:
            box.enabled = False
import json
import bpy
from ...custom_selection import *
from ...guides.utils import BL_Ver
from ...singleton import SingletonClass

# global group lists
all_bones = hand_l = hand_r = arm_l = arm_r = leg_l = leg_r = foot_l = foot_r = head = torso = []



class BLENRIG_PT_blenrig_6_Interface(bpy.types.Panel):
    bl_label = 'BlenRig 6 Controls'
    bl_space_type = 'VIEW_3D'
    bl_idname = "BLENRIG_PT_blenrig_6_Interface"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_region_type = 'UI'
    bl_category = "BlenRig 6"
    bl_options = {"HIDE_HEADER", }

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'PICKER':
            return False

        elif not context.active_object:
            return False
        elif (context.active_object.type in ["ARMATURE"]):
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                    for prop in context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            if context.mode in ["OBJECT", "EDIT_MESH"]:
                if (context.active_object.type in ["MESH"]):
                    for mod in context.active_object.modifiers:
                        if (mod.type in ["ARMATURE", "MESH_DEFORM"]):
                            return True

    def draw(self, context):
        if context.mode in ["POSE", "EDIT_ARMATURE"]:
            layout = self.layout
            global all_bones, hand_l, hand_r, arm_l, arm_r, leg_l, leg_r, foot_l, foot_r, head, torso
            props = context.window_manager.blenrig_6_props
            arm = context.active_object.data
            armobj = context.active_object
            arm_bones = context.active_object.pose.bones
            act_bone = context.active_pose_bone
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
        except:
            selected_bones = []
        else:
            if context.mode in ["OBJECT", "EDIT_MESH"]:
                layout = self.layout

                armobj = context.active_object
                ovlay = context.space_data.overlay

                box = layout.column()
                col = box.column()
                row = col.row()

                picker_col = box.box()
                picker_row = picker_col.row(align=True)
                col_3 = picker_row.row()
                col_3.alignment = 'CENTER'
                col_3.prop(armobj, "show_in_front")
                col_3.prop(ovlay, "show_bones")
                col_3.prop(ovlay, "show_overlays")
                col_3.separator()

        def is_selected(names):
            for name in names:
                if name in selected_bones:
                    return True
            return False

        if context.mode in ["POSE", "EDIT_ARMATURE"]:

            # Bone groups used for Inherit Scale Checkboxes & Sensible to Selection Sliders Display
            if not all_bones:
                all_bones = []
                for bone in armobj.pose.bones:
                    all_bones.append(bone.name)

                hand_l = []
                for bone in all_bones[:]:
                    if bone.count("_L"):
                        if bone.count("fing"):
                            hand_l.append(bone)
                hand_r = []
                for bone in all_bones[:]:
                    if bone.count("_R"):
                        if bone.count("fing"):
                            hand_r.append(bone)

                arm_l = []
                for bone in all_bones[:]:
                    if bone.count("_L"):
                        if bone.count("arm") or bone.count("elbow") or bone.count("shoulder") or bone.count("hand") or bone.count("wrist"):
                            arm_l.append(bone)

                arm_r = []
                for bone in all_bones[:]:
                    if bone.count("_R"):
                        if bone.count("arm") or bone.count("elbow") or bone.count("shoulder") or bone.count("hand") or bone.count("wrist"):
                            arm_r.append(bone)

                leg_l = []
                for bone in all_bones[:]:
                    if bone.count("_L"):
                        if bone.count("butt") or bone.count("knee") or bone.count("thigh") or bone.count("shin"):
                            leg_l.append(bone)

                leg_r = []
                for bone in all_bones[:]:
                    if bone.count("_R"):
                        if bone.count("butt") or bone.count("knee") or bone.count("thigh") or bone.count("shin"):
                            leg_r.append(bone)

                foot_l = []
                for bone in all_bones[:]:
                    if bone.count("_L"):
                        if bone.count("toe") or bone.count("foot") or bone.count("heel") or bone.count("sole") or bone.count("floor"):
                            foot_l.append(bone)

                foot_r = []
                for bone in all_bones[:]:
                    if bone.count("_R"):
                        if bone.count("toe") or bone.count("foot") or bone.count("heel") or bone.count("sole") or bone.count("floor"):
                            foot_r.append(bone)

                head = []
                for bone in all_bones[:]:
                    if bone.count("look") or bone.count("head") or bone.count("neck") or bone.count("maxi") or bone.count("cheek") or bone.count("chin") or bone.count("lip") or bone.count("ear_") or bone.count("tongue") or bone.count("eyelid") or bone.count("forehead") or bone.count("brow") or bone.count("nose") or bone.count("nostril") or bone.count("mouth") or bone.count("eye") or bone.count("gorro") or bone.count("teeth") or bone.count("hat") or bone.count("glasses") or bone.count("anteojos") or bone.count("hair") or bone.count("pelo"):
                        head.append(bone)

                torso = ['master']
                for bone in all_bones[:]:
                    if bone.count("spine") or bone.count("pelvis") or bone.count("torso") or bone.count("omoplate") or bone.count("chest") or bone.count("body") or bone.count("ball") or bone.count("dicky") or bone.count("butt") or bone.count("back") or bone.count("clavi") or bone.count("look") or bone.count("hip"):
                        torso.append(bone)

            # PANEL ####################################################################################################

            # Armature Layers:
            if "gui_layers" in arm:
                main_col = layout.box().column(align=True)
                col = main_col.column(align=True)
                row = col.row(align=True)

                row.operator("gui.blenrig_6_tabs", icon="RENDERLAYERS", emboss=1).tab = "gui_layers"
                row.label(text=" Armature Layers")

                # zebus3d
                if arm["gui_layers"]:
                    col.separator()

                    slider = col.row(align=True)
                    slider.prop(arm, '["layers_count"]', text="Maximum Layers", toggle=True)
                    col.separator()

                    arm_layers = col.grid_flow(row_major=True, even_columns=True, even_rows=True, align=True, columns=3)
                    arm_layers.scale_y = 0.9

                    layers_count = arm["layers_count"]

                    # read ui data from singleton:
                    # instancio el singleton para usarlo:
                    singleton = SingletonClass()
                    if singleton.armature_layers:
                        for key, value in singleton.armature_layers.items():
                            idx = value[0]
                            if idx < layers_count:
                                arm_layers.prop(arm, "layers", index=idx, toggle=True, text=key)


                    # sin json pero desordenados por no tener el index en el mismo orden:
                    # for key, value in arm.items():
                    #     if key != "layer_list":
                    #         continue
                    #     valid_names = value.split(", ")
                    # for idx, name in enumerate(valid_names):
                    #     if idx < layers_count:
                    #         arm_layers.prop(arm, "layers", index=idx, toggle=True, text=name)

            # gui custom layers panel ############################################################

            col = layout.box().column(align=True)
            row = col.row(align=True)

            row.operator("gui.blenrig_6_tabs", icon="RENDERLAYERS", emboss=1).tab = "gui_custom_layers"
            row.label(text=" Armature Custom Layers")

            if props.gui_custom_layers:

                arm2 = context.object

                col.separator()
                row_list = col.row(align=True)
                row_list.enabled = (context.mode == 'POSE')

                # UI list
                rows = 4 if len(arm2.blenrig_selection_sets) > 0 else 2
                row_list.template_list(
                    "BLENRIG_UL_selection_set", "",  # type and unique id
                    arm2, "blenrig_selection_sets",  # pointer to the CollectionProperty
                    arm2, "blenrig_active_selection_set",  # pointer to the active identifier
                    rows=rows
                )

                # add/remove/specials UI list Menu
                col_list = row_list.column(align=True)
                col_list.operator("blenrig.selection_set_add", icon='ADD', text="")
                col_list.operator("blenrig.selection_set_remove", icon='REMOVE', text="")
                col_list.menu("BLENRIG_MT_selection_sets_context_menu", icon='DOWNARROW_HLT', text="")

                # move up/down arrows
                if len(arm2.blenrig_selection_sets) > 0:
                    # col_list.separator()
                    col_list.operator("blenrig.selection_set_move", icon='TRIA_UP', text="").direction = 'UP'
                    col_list.operator("blenrig.selection_set_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

                # buttons
                col.separator()
                buttons = col.row()

                sub = buttons.row(align=True)
                sub.operator("blenrig.selection_set_assign", text="Assign")
                sub.operator("blenrig.selection_set_unassign", text="Remove")

                # sub = buttons.row(align=True)
                # sub.operator("blenrig.selection_set_select", text="Select")
                # sub.operator("blenrig.selection_set_deselect", text="Deselect")

             # End gui custom layers ############################################################

            # expanded box
            box = layout.column()
            col2 = box.column(align=1)
            row_layers = col2.row(align=1)

            animation_col = box.box()
            animation_col.scale_x = 1
            animation_col.scale_y = 1
            animation_col.alignment = 'CENTER'
            animation_col.label(text='Pose Copy-Paste bottons')
            animation_row = animation_col.row(align=True)
            col_1 = animation_row.column()
            col_1.scale_x = 1
            col_1.scale_y = 1
            col_1.alignment = 'LEFT'

            animation_row.operator("pose.copy", icon="COPYDOWN", text="")
            animation_row.operator("pose.paste", icon="PASTEDOWN", text="")
            col_1.separator()
            animation_row.operator('pose.paste', icon="PASTEFLIPDOWN", text="").flipped = True

            col_2 = animation_row.column()
            col_2.scale_x = 0.9
            col_2.scale_y = 1
            col_2.alignment = 'LEFT'
            # col_2.operator("blenrig.paste_pose_flipped", text="Quick Pose Flipped")

            ovlay = context.space_data.overlay
            col_3 = animation_row.column()
            col_3.scale_x = 1
            col_3.scale_y = 1
            col_3 = animation_row.row(align=False)
            col_3.alignment = 'RIGHT'

            col_3.prop(armobj.pose, "use_mirror_x")
            col_3.prop(armobj, "show_in_front")
            col_3.prop(ovlay, "show_bones")
            col_3.prop(ovlay, "show_overlays")
            col_1.separator()
            col_1.separator()
            col_1.separator()

    ################# BLENRIG PICKER BODY #############################################
            if context.mode == "POSE":

                if "gui_picker_body" in arm:
                    box = layout.column()
                    col = box.column()
                    row = col.row()
                    row.alignment = "LEFT"
                # expanded box
                if "gui_picker_body" in arm and arm["gui_picker_body"]:
                    row.operator("gui.blenrig_6_tabs", icon="OUTLINER_OB_ARMATURE", emboss=1).tab = "gui_picker_body"
                    row.label(text="BODY PICKER & PROPERTIES")

                    row_props = col.row()
                    row_props.alignment = 'LEFT'
                    row_props.prop(props, "gui_picker_body_props", text="PROPERTIES")
                    row_props.prop(props, "gui_picker_body_picker", text="PICKER")

                    # 3 Columns
                    box_row = box.row()

                    if props.gui_picker_body_picker:
                        if props.gui_picker_body_props:
                            box_R = box_row.column(align=1)
                            box_R.scale_x = 0.2
                            box_R.scale_y = 1
                            box_R.alignment = 'LEFT'

                            box_body = box_row.column(align=1)

                            box_L = box_row.column(align=1)
                            box_L.scale_x = 0.2
                            box_L.scale_y = 1
                            box_L.alignment = 'RIGHT'
                        else:
                            box_body = box_row.column(align=1)
                        # Look slider

                        if props.gui_picker_body_props:
                            row_key = box_body.row(align=True)
                            row_key.alignment = 'CENTER'
                            row_key.scale_x = 1
                            row_key.scale_y = 1
                            row_key.operator("keyframe.main_props", text='Keyframe All Properties',
                                             icon='KEYINGSET', emboss=1)

                            box_body.separator()
                            box_body.separator()

                            row_look_title = box_body.row(align=1)
                            row_look_title.scale_x = 1
                            row_look_title.scale_y = 1
                            row_look_title.alignment = 'CENTER'
                            row_look_title.label(text="Eye Target")

                            row_switch = box_body.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 0.8
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.look_list", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_head']['look_switch'] == 0
                                    else (
                                        "Follow Body"
                                        if arm_bones['properties_head']['look_switch'] == 1
                                        else (
                                            "Follow Torso"
                                            if arm_bones['properties_head']['look_switch'] == 2 else "Follow Head"))),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_head'], 'look_switch',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = box_body.column()
                            col_space.scale_x = 1
                            col_space.scale_y = 4
                            col_space.separator()
                        else:
                            col_space = box_body.column()
                            col_space.scale_x = 1
                            col_space.scale_y = 10
                            col_space.separator()

                        # Head

                        col_head_main = box_body.column(align=1)
                        col_head_main.alignment = 'CENTER'

                        col_toon = col_head_main.row()
                        col_toon.scale_x = 0.5
                        col_toon.scale_y = 0.5
                        col_toon.alignment = 'CENTER'
                        col_toon.operator("operator.head_stretch", text="", icon="KEYFRAME_HLT", emboss=0)
                        col_toon.operator("operator.head_toon", text="", icon="KEYFRAME", emboss=0)

                        row_head_main = col_head_main.row(align=1)
                        row_head_main.alignment = 'CENTER'

                        col_1 = row_head_main.column()
                        col_1.scale_x = 0.5
                        col_1.scale_y = 0.5
                        col_1.alignment = 'CENTER'
                        col_1.operator("operator.head_top_ctrl", text="", icon="KEYFRAME_HLT", emboss=0)
                        col_1.operator("operator.head_mid_ctrl", text="", icon="KEYFRAME_HLT", emboss=0)
                        col_1.operator("operator.head_mid_curve", text="", icon="KEYFRAME_HLT", emboss=0)
                        col_1.operator("operator.mouth_str_ctrl", text="", icon="KEYFRAME_HLT", emboss=0)

                        col_2 = row_head_main.column(align=1)
                        col_2.scale_x = 1
                        col_2.scale_y = 1
                        col_2.alignment = 'CENTER'

                        row_eyes = col_2.row()
                        row_eyes.scale_x = 1.1
                        row_eyes.scale_y = 0.75
                        row_eyes.alignment = 'CENTER'
                        box_eyes = row_eyes.box()

                        row = box_eyes.row()
                        row = box_eyes.row()
                        row.alignment = 'CENTER'

                        col_eye_R = row.column()
                        col_eye_R.scale_x = 1
                        col_eye_R.scale_y = 1
                        col_eye_R.alignment = 'CENTER'
                        col_eye_R.operator("operator.look_r", text="", icon="HIDE_OFF")

                        col_look = row.column()
                        col_look.scale_x = 0.7
                        col_look.scale_y = 1.6
                        col_look.alignment = 'CENTER'
                        col_look.operator("operator.look", text="")

                        col_eye_L = row.column()
                        col_eye_L.scale_x = 1
                        col_eye_L.scale_y = 1
                        col_eye_L.alignment = 'CENTER'
                        col_eye_L.operator("operator.look_l", text="", icon="HIDE_OFF")

                        col_fk = col_2.row(align=1)
                        col_fk.scale_x = 1.1
                        col_fk.scale_y = 1.5
                        col_fk.alignment = 'CENTER'
                        col_fk.operator("operator.head_fk", text="Head FK")

                        col_3 = row_head_main.column()
                        col_3.scale_x = 0.5
                        col_3.scale_y = 0.5
                        col_3.alignment = 'CENTER'
                        col_3.operator("operator.face_toon_up", text="", icon="KEYFRAME", emboss=0)
                        col_3.operator("operator.face_toon_mid", text="", icon="KEYFRAME", emboss=0)
                        col_3.operator("operator.face_toon_low", text="", icon="KEYFRAME", emboss=0)

                        # Neck

                        row_neck_main = box_body.row(align=1)
                        row_neck_main.scale_x = 0.75
                        row_neck_main.scale_y = 1
                        row_neck_main.alignment = 'CENTER'

                        col_neck_fk = row_neck_main.column(align=1)
                        col_neck_fk.scale_x = 2
                        col_neck_fk.scale_y = 1
                        col_neck_fk.alignment = 'CENTER'

                        row_neck_1 = col_neck_fk.row(align=0)
                        row_neck_1.scale_x = 1
                        row_neck_1.scale_y = 0.35
                        row_neck_1.alignment = 'CENTER'
                        row_neck_1.operator("operator.neck_3", text="")

                        col_toon_2 = col_neck_fk.row(align=1)
                        col_toon_2.scale_x = 1
                        col_toon_2.scale_y = 0.15
                        col_toon_2.alignment = 'CENTER'
                        col_toon_2.operator("operator.neck_3_toon", text="", icon="KEYFRAME_HLT", emboss=0)

                        row_neck_2 = col_neck_fk.row(align=1)
                        row_neck_2.scale_x = 1
                        row_neck_2.scale_y = 0.3
                        row_neck_2.alignment = 'CENTER'
                        row_neck_2.operator("operator.neck_2", text="")

                        col_toon_3 = col_neck_fk.column(align=1)
                        col_toon_3.scale_x = 1
                        col_toon_3.scale_y = 0.15
                        col_toon_3.alignment = 'CENTER'
                        col_toon_3.operator("operator.neck_2_toon", text="", icon="KEYFRAME_HLT", emboss=0)

                        row_neck_3 = col_neck_fk.row(align=1)
                        row_neck_3.scale_x = 1
                        row_neck_3.scale_y = 0.3
                        row_neck_3.alignment = 'CENTER'
                        row_neck_3.operator("operator.neck_1", text="")

                        row_ctrl = col_neck_fk.row(align=1)
                        row_ctrl.scale_x = 1
                        row_ctrl.scale_y = 0.5
                        row_ctrl.alignment = 'CENTER'
                        row_ctrl.operator("operator.neck_ctrl", text="Neck Ctrl")

                        # Shoulders

                        row_shoulder = box_body.row(align=0)

                        col_2 = row_shoulder.row(align=1)
                        col_2.scale_x = 0.8
                        col_2.scale_y = 1
                        col_2.alignment = 'CENTER'

                        row_shoulder_R = col_2.row(align=1)
                        row_shoulder_R.scale_x = 1
                        row_shoulder_R.scale_y = 0.75
                        row_shoulder_R.alignment = 'CENTER'

                        col_toon = row_shoulder_R.column(align=1)
                        col_toon.scale_x = 0.25
                        col_toon.scale_y = 0.75
                        col_toon.alignment = 'CENTER'
                        col_toon.operator("operator.clavi_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                        col_ik = row_shoulder_R.column(align=1)
                        col_ik.scale_x = 1
                        col_ik.scale_y = 0.8
                        col_ik.alignment = 'CENTER'
                        col_ik.operator("operator.arm_scale_r", text="", icon="UV_SYNC_SELECT", emboss=1)

                        col_fk = row_shoulder_R.column(align=1)
                        col_fk.scale_x = 1.2
                        col_fk.scale_y = 0.75
                        col_fk.alignment = 'CENTER'
                        col_fk.operator("operator.shoulder_r", text="Shldr FK")

                        row_neck_scale = col_2.row(align=1)
                        row_neck_scale.scale_x = 1
                        row_neck_scale.scale_y = 0.75
                        row_neck_scale.alignment = 'CENTER'
                        row_neck_scale.operator("operator.head_scale", text="", icon="UV_SYNC_SELECT", emboss=1)

                        row_shoulder_L = col_2.row(align=1)
                        row_shoulder_L.scale_x = 1
                        row_shoulder_L.scale_y = 0.75
                        row_shoulder_L.alignment = 'CENTER'

                        col_fk = row_shoulder_L.column(align=1)
                        col_fk.scale_x = 1.2
                        col_fk.scale_y = 0.75
                        col_fk.alignment = 'CENTER'
                        col_fk.operator("operator.shoulder_l", text="Shldr FK")

                        col_ik = row_shoulder_L.column(align=1)
                        col_ik.scale_x = 1
                        col_ik.scale_y = 0.8
                        col_ik.alignment = 'CENTER'
                        col_ik.operator("operator.arm_scale_l", text="", icon="UV_SYNC_SELECT", emboss=1)

                        col_toon = row_shoulder_L.column(align=1)
                        col_toon.scale_x = 0.25
                        col_toon.scale_y = 0.75
                        col_toon.alignment = 'CENTER'
                        col_toon.operator("operator.clavi_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Arm R
                        if arm['rig_type'] == "Biped":
                            row_torso = box_body.row()
                            row_torso.scale_x = 1
                            row_torso.scale_y = 1
                            row_torso.alignment = 'CENTER'

                            col_arm_R = row_torso.row(align=1)
                            col_arm_R.scale_x = 0.5
                            col_arm_R.scale_y = 1
                            col_arm_R.alignment = 'CENTER'

                            col_arm_toon_R = col_arm_R.column()
                            col_arm_toon_R.scale_x = 1
                            col_arm_toon_R.scale_y = 1
                            col_arm_toon_R.alignment = 'CENTER'
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.arm_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.elbow_pole_r", text="", icon="PROP_ON", emboss=0)
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.forearm_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_arm_main_R = col_arm_R.column(align=1)
                            col_arm_main_R.scale_x = 1.2
                            col_arm_main_R.scale_y = 1
                            col_arm_main_R.alignment = 'CENTER'

                            col_arm_scale_R = col_arm_main_R.row(align=1)
                            col_arm_scale_R.scale_x = 1.2
                            col_arm_scale_R.scale_y = 1
                            col_arm_scale_R.alignment = 'CENTER'
                            col_arm_scale_R.operator("operator.arm_fk_ctrl_r", text="Ctrl", emboss=1)

                            col_arm_fk_R = col_arm_main_R.row(align=1)
                            col_arm_fk_R.scale_x = 1
                            col_arm_fk_R.scale_y = 2.5
                            col_arm_fk_R.alignment = 'CENTER'
                            col_arm_fk_R.operator("operator.arm_fk_r", text="FK")

                            col_arm_ik_R = col_arm_main_R.row(align=1)
                            col_arm_ik_R.scale_x = 1
                            col_arm_ik_R.scale_y = 1
                            col_arm_ik_R.alignment = 'CENTER'
                            col_arm_ik_R.operator("operator.arm_ik_r", text="IK")

                            col_elbow_toon_R = col_arm_main_R.column()
                            col_elbow_toon_R.scale_x = 1
                            col_elbow_toon_R.scale_y = 0.25
                            col_elbow_toon_R.alignment = 'CENTER'
                            col_elbow_toon_R.operator("operator.elbow_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_forearm_fk_R = col_arm_main_R.row(align=1)
                            col_forearm_fk_R.scale_x = 1
                            col_forearm_fk_R.scale_y = 3
                            col_forearm_fk_R.alignment = 'CENTER'
                            col_forearm_fk_R.operator("operator.forearm_fk_r", text="FK")

                            col_forearm_ik_R = col_arm_main_R.row(align=1)
                            col_forearm_ik_R.scale_x = 1
                            col_forearm_ik_R.scale_y = 1
                            col_forearm_ik_R.alignment = 'CENTER'
                            col_forearm_ik_R.operator("operator.forearm_ik_r", text="IK")

                            col_hand_toon_R = col_arm_main_R.column()
                            col_hand_toon_R.scale_x = 1
                            col_hand_toon_R.scale_y = 0.25
                            col_hand_toon_R.alignment = 'CENTER'
                            col_hand_toon_R.operator("operator.hand_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Arm R Quadruped

                        if arm['rig_type'] == "Quadruped":
                            row_torso = box_body.row()
                            row_torso.scale_x = 1
                            row_torso.scale_y = 1
                            row_torso.alignment = 'CENTER'
                            col_arm_R = row_torso.row(align=1)
                            col_arm_R.scale_x = 0.5
                            col_arm_R.scale_y = 1
                            col_arm_R.alignment = 'CENTER'

                            col_arm_toon_R = col_arm_R.column()
                            col_arm_toon_R.scale_x = 1
                            col_arm_toon_R.scale_y = 1
                            col_arm_toon_R.alignment = 'CENTER'
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.arm_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.elbow_pole_r", text="", icon="PROP_ON", emboss=0)
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.forearm_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.separator()
                            col_arm_toon_R.operator("operator.carpal_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_arm_main_R = col_arm_R.column(align=1)
                            col_arm_main_R.scale_x = 1.2
                            col_arm_main_R.scale_y = 1
                            col_arm_main_R.alignment = 'CENTER'

                            col_arm_scale_R = col_arm_main_R.row(align=1)
                            col_arm_scale_R.scale_x = 1.2
                            col_arm_scale_R.scale_y = 1
                            col_arm_scale_R.alignment = 'CENTER'
                            col_arm_scale_R.operator("operator.arm_scale_r", text="", icon="UV_SYNC_SELECT", emboss=1)

                            col_arm_fk_R = col_arm_main_R.row(align=1)
                            col_arm_fk_R.scale_x = 1
                            col_arm_fk_R.scale_y = 1.5
                            col_arm_fk_R.alignment = 'CENTER'
                            col_arm_fk_R.operator("operator.arm_fk_r", text="FK")

                            col_arm_ik_R = col_arm_main_R.row(align=1)
                            col_arm_ik_R.scale_x = 1
                            col_arm_ik_R.scale_y = 1
                            col_arm_ik_R.alignment = 'CENTER'
                            col_arm_ik_R.operator("operator.arm_ik_r", text="IK")

                            col_elbow_toon_R = col_arm_main_R.column()
                            col_elbow_toon_R.scale_x = 1
                            col_elbow_toon_R.scale_y = 0.25
                            col_elbow_toon_R.alignment = 'CENTER'
                            col_elbow_toon_R.operator("operator.elbow_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_forearm_fk_R = col_arm_main_R.row(align=1)
                            col_forearm_fk_R.scale_x = 1
                            col_forearm_fk_R.scale_y = 1.5
                            col_forearm_fk_R.alignment = 'CENTER'
                            col_forearm_fk_R.operator("operator.forearm_fk_r", text="FK")

                            col_forearm_ik_R = col_arm_main_R.row(align=1)
                            col_forearm_ik_R.scale_x = 1
                            col_forearm_ik_R.scale_y = 1
                            col_forearm_ik_R.alignment = 'CENTER'
                            col_forearm_ik_R.operator("operator.forearm_ik_r", text="IK")

                            col_ankle_toon_R = col_arm_main_R.column()
                            col_ankle_toon_R.scale_x = 1
                            col_ankle_toon_R.scale_y = 0.25
                            col_ankle_toon_R.alignment = 'CENTER'
                            col_ankle_toon_R.operator("operator.ankle_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_carpal_fk_R = col_arm_main_R.row(align=1)
                            col_carpal_fk_R.scale_x = 1
                            col_carpal_fk_R.scale_y = 1.5
                            col_carpal_fk_R.alignment = 'CENTER'
                            col_carpal_fk_R.operator("operator.carpal_fk_r", text="FK")

                            col_carpal_ik_R = col_arm_main_R.row(align=1)
                            col_carpal_ik_R.scale_x = 1
                            col_carpal_ik_R.scale_y = 1
                            col_carpal_ik_R.alignment = 'CENTER'
                            col_carpal_ik_R.operator("operator.carpal_ik_r", text="IK")

                            col_hand_toon_R = col_arm_main_R.column()
                            col_hand_toon_R.scale_x = 1
                            col_hand_toon_R.scale_y = 0.25
                            col_hand_toon_R.alignment = 'CENTER'
                            col_hand_toon_R.operator("operator.hand_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Spine

                        row_torso_main = row_torso.row(align=1)
                        row_torso_main.alignment = 'CENTER'
                        row_torso_main.scale_x = 1
                        row_torso_main.scale_y = 1.0

                        col_torso = row_torso_main.column(align=1)
                        col_torso.alignment = 'CENTER'
                        col_torso.scale_x = 0.92
                        col_torso.scale_y = 1.0

                        col_torso_ctrl = col_torso.row(align=1)
                        col_torso_ctrl.alignment = 'CENTER'
                        col_torso_ctrl.scale_x = 1
                        col_torso_ctrl.scale_y = 1.0

                        col_torso_ctrl_fk = col_torso_ctrl.row(align=0)
                        col_torso_ctrl_fk.scale_x = 1
                        col_torso_ctrl_fk.scale_y = 0.75
                        col_torso_ctrl_fk.alignment = 'CENTER'
                        col_torso_ctrl_fk.operator("operator.torso_ctrl", text="Torso FK Ctrl")

                        col_torso_ctrl_inv = col_torso_ctrl.row(align=0)
                        col_torso_ctrl_inv.scale_x = 0.75
                        col_torso_ctrl_inv.scale_y = 0.75
                        col_torso_ctrl_inv.alignment = 'CENTER'
                        col_torso_ctrl_inv.operator("operator.torso_fk_ctrl_inv", text="Inv")

                        col_spine_toon_4 = col_torso.row(align=1)
                        col_spine_toon_4.scale_x = 1
                        col_spine_toon_4.scale_y = 0.35
                        col_spine_toon_4.alignment = 'CENTER'
                        col_spine_toon_4.operator("operator.spine_4_toon", text="", icon="KEYFRAME_HLT", emboss=0)

                        col_spine_3 = col_torso.row(align=1)
                        col_spine_3.scale_x = 3.8
                        col_spine_3.scale_y = 1
                        col_spine_3.alignment = 'CENTER'

                        col_spine_3_fk = col_spine_3.column(align=1)
                        col_spine_3_fk.scale_x = 0.5
                        col_spine_3_fk.scale_y = 1
                        col_spine_3_fk.alignment = 'CENTER'
                        col_spine_3_fk.operator("operator.spine_3", text="Spine 3")

                        col_spine_3_inv = col_spine_3.column(align=1)
                        col_spine_3_inv.scale_x = 0.25
                        col_spine_3_inv.scale_y = 1
                        col_spine_3_inv.alignment = 'CENTER'
                        col_spine_3_inv.operator("operator.spine_3_fk_inv", text="Inv")

                        col_spine_toon_3 = col_torso.row(align=1)
                        col_spine_toon_3.scale_x = 1
                        col_spine_toon_3.scale_y = 0.35
                        col_spine_toon_3.alignment = 'CENTER'
                        col_spine_toon_3.operator("operator.spine_3_toon", text="", icon="KEYFRAME_HLT", emboss=0)

                        col_spine_2 = col_torso.row(align=1)
                        col_spine_2.scale_x = 1.35
                        col_spine_2.scale_y = 1
                        col_spine_2.alignment = 'CENTER'

                        col_spine_2_fk = col_spine_2.column(align=1)
                        col_spine_2_fk.scale_x = 0.5
                        col_spine_2_fk.scale_y = 1
                        col_spine_2_fk.alignment = 'CENTER'
                        col_spine_2.operator("operator.spine_2", text="Spine 2")

                        col_spine_2_inv = col_spine_2.column(align=1)
                        col_spine_2_inv.scale_x = 0.5
                        col_spine_2_inv.scale_y = 1
                        col_spine_2_inv.alignment = 'CENTER'
                        col_spine_2_inv.operator("operator.spine_2_fk_inv", text="Inv")

                        col_spine_toon_2 = col_torso.row(align=1)
                        col_spine_toon_2.scale_x = 1
                        col_spine_toon_2.scale_y = 0.35
                        col_spine_toon_2.alignment = 'CENTER'
                        col_spine_toon_2.operator("operator.spine_2_toon", text="", icon="KEYFRAME_HLT", emboss=0)

                        col_spine_1 = col_torso.row(align=1)
                        col_spine_1.scale_x = 1.5
                        col_spine_1.scale_y = 0.75
                        col_spine_1.alignment = 'CENTER'
                        col_spine_1.operator("operator.spine_1", text="Spine 1")

                        col_spine_toon_1 = col_torso.row(align=1)
                        col_spine_toon_1.scale_x = 1
                        col_spine_toon_1.scale_y = 0.25
                        col_spine_toon_1.alignment = 'CENTER'
                        col_spine_toon_1.operator("operator.spine_1_toon", text="", icon="KEYFRAME_HLT", emboss=0)
                        col_torso_props = col_torso.row(align=1)
                        col_torso_props.scale_x = 1.5
                        col_torso_props.scale_y = 0.75
                        col_torso_props.alignment = 'CENTER'

                        row_torso_props = col_torso.row(align=True)
                        row_torso_props.alignment = 'CENTER'
                        row_torso_props.scale_x = 1
                        row_torso_props.scale_y = 0.8
                        row_torso_props.operator("snap.torso_fk_to_ik", text="", icon='PLAY_REVERSE', emboss=True)
                        row_torso_props.label(text="{}".format(
                            " FK" if arm_bones['properties_torso']['ik_torso'] == 1 else " IK"),)
                        row_torso_props.operator("snap.torso_ik_to_fk", text="", icon='PLAY', emboss=True)
                        col_prop = row_torso_props.column(align=True)
                        col_prop.scale_x = BL_Ver(0.45, 0.4)
                        col_prop.prop(arm_bones['properties_torso'], 'ik_torso', toggle=True, icon_only=1, emboss=1)

                        if props.gui_picker_body_props:

                            col_mstr_torso_ctrls = col_torso.row(align=1)
                            col_mstr_torso_ctrls.scale_x = 4.5
                            col_mstr_torso_ctrls.scale_y = 1
                            col_mstr_torso_ctrls.alignment = 'CENTER'

                            col_mstr_torso = col_mstr_torso_ctrls.column(align=1)
                            col_mstr_torso.scale_x = 0.37
                            col_mstr_torso.scale_y = 1
                            col_mstr_torso.alignment = 'CENTER'
                            col_mstr_torso.operator("operator.master_torso", text="Mstr Torso")

                            col_mstr_torso_pivot = col_mstr_torso_ctrls.column(align=1)
                            col_mstr_torso_pivot.scale_x = 0.5
                            col_mstr_torso_pivot.scale_y = 1
                            col_mstr_torso_pivot.alignment = 'CENTER'
                            col_mstr_torso_pivot.operator("operator.master_torso_pivot_point", text="")

                            row_pivot = col_torso.row(align=True)
                            row_pivot.alignment = 'CENTER'
                            row_pivot.scale_x = 1.2
                            row_pivot.scale_y = 0.75
                            row_pivot.operator("reset.master_torso_pivot", text='Reset Pivot',
                                               icon='PIVOT_CURSOR', emboss=True)

                            row_align = col_torso.row(align=True)
                            row_align.alignment = 'CENTER'
                            row_align.scale_x = 1.2
                            row_align.scale_y = 0.75
                            row_align.operator("align.spine", text='Align Spine', icon='PIVOT_CURSOR', emboss=True)

                        else:
                            col_mstr_torso_ctrls = col_torso.row(align=1)
                            col_mstr_torso_ctrls.scale_x = 4.5
                            col_mstr_torso_ctrls.scale_y = 1
                            col_mstr_torso_ctrls.alignment = 'CENTER'

                            col_mstr_torso = col_mstr_torso_ctrls.column(align=1)
                            col_mstr_torso.scale_x = 0.37
                            col_mstr_torso.scale_y = 1
                            col_mstr_torso.alignment = 'CENTER'
                            col_mstr_torso.operator("operator.master_torso", text="Mstr Torso")

                            col_mstr_torso_pivot = col_mstr_torso_ctrls.column(align=1)
                            col_mstr_torso_pivot.scale_x = 0.5
                            col_mstr_torso_pivot.scale_y = 1
                            col_mstr_torso_pivot.alignment = 'CENTER'
                            col_mstr_torso_pivot.operator("operator.master_torso_pivot_point", text="")

                            row_pivot = col_torso.row(align=True)
                            row_pivot.alignment = 'CENTER'
                            row_pivot.scale_x = 1.2
                            row_pivot.scale_y = 0.75
                            row_pivot.operator("reset.master_torso_pivot", text='Reset Pivot',
                                               icon='PIVOT_CURSOR', emboss=True)

                        col_pelvis_toon = col_torso.row(align=1)
                        col_pelvis_toon.scale_x = 1
                        col_pelvis_toon.scale_y = 0.25
                        col_pelvis_toon.alignment = 'CENTER'
                        col_pelvis_toon.operator("operator.pelvis_toon", text="", icon="KEYFRAME_HLT", emboss=0)

                        col_pelvis = col_torso.row(align=0)
                        col_pelvis.scale_x = 1.8
                        col_pelvis.scale_y = 1.5
                        col_pelvis.alignment = 'CENTER'
                        col_pelvis.operator("operator.pelvis_ctrl", text="Pelivs Ctrl")

                        # Arm L
                        if arm['rig_type'] == "Biped":
                            col_arm_L = row_torso.row(align=1)
                            col_arm_L.scale_x = 0.5
                            col_arm_L.scale_y = 1
                            col_arm_L.alignment = 'CENTER'

                            col_arm_main_L = col_arm_L.column(align=1)
                            col_arm_main_L.scale_x = 1.2
                            col_arm_main_L.scale_y = 1
                            col_arm_main_L.alignment = 'CENTER'

                            col_arm_scale_L = col_arm_main_L.row(align=1)
                            col_arm_scale_L.scale_x = 1.2
                            col_arm_scale_L.scale_y = 1
                            col_arm_scale_L.alignment = 'CENTER'
                            col_arm_scale_L.operator("operator.arm_fk_ctrl_l", text="Ctrl", emboss=1)

                            col_arm_fk_L = col_arm_main_L.row(align=1)
                            col_arm_fk_L.scale_x = 1
                            col_arm_fk_L.scale_y = 2.5
                            col_arm_fk_L.alignment = 'CENTER'
                            col_arm_fk_L.operator("operator.arm_fk_l", text="FK")

                            col_arm_ik_L = col_arm_main_L.row(align=1)
                            col_arm_ik_L.scale_x = 1
                            col_arm_ik_L.scale_y = 1
                            col_arm_ik_L.alignment = 'CENTER'
                            col_arm_ik_L.operator("operator.arm_ik_l", text="IK")

                            col_elbow_toon_L = col_arm_main_L.column()
                            col_elbow_toon_L.scale_x = 1
                            col_elbow_toon_L.scale_y = 0.25
                            col_elbow_toon_L.alignment = 'CENTER'
                            col_elbow_toon_L.operator("operator.elbow_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_forearm_fk_L = col_arm_main_L.row(align=1)
                            col_forearm_fk_L.scale_x = 1
                            col_forearm_fk_L.scale_y = 3
                            col_forearm_fk_L.alignment = 'CENTER'
                            col_forearm_fk_L.operator("operator.forearm_fk_l", text="FK")

                            col_forearm_ik_L = col_arm_main_L.row(align=1)
                            col_forearm_ik_L.scale_x = 1
                            col_forearm_ik_L.scale_y = 1
                            col_forearm_ik_L.alignment = 'CENTER'
                            col_forearm_ik_L.operator("operator.forearm_ik_l", text="IK")

                            col_hand_toon_L = col_arm_main_L.column()
                            col_hand_toon_L.scale_x = 1
                            col_hand_toon_L.scale_y = 0.25
                            col_hand_toon_L.alignment = 'CENTER'
                            col_hand_toon_L.operator("operator.hand_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_arm_toon_L = col_arm_L.column()
                            col_arm_toon_L.scale_x = 1
                            col_arm_toon_L.scale_y = 1
                            col_arm_toon_L.alignment = 'CENTER'
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.arm_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.elbow_pole_l", text="", icon="PROP_ON", emboss=0)
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()

                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.forearm_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Arm L Quadruped

                        if arm['rig_type'] == "Quadruped":
                            col_arm_L = row_torso.row(align=1)
                            col_arm_L.scale_x = 0.5
                            col_arm_L.scale_y = 1
                            col_arm_L.alignment = 'CENTER'

                            col_arm_main_L = col_arm_L.column(align=1)
                            col_arm_main_L.scale_x = 1.2
                            col_arm_main_L.scale_y = 1
                            col_arm_main_L.alignment = 'CENTER'

                            col_arm_scale_L = col_arm_main_L.row(align=1)
                            col_arm_scale_L.scale_x = 1.2
                            col_arm_scale_L.scale_y = 1
                            col_arm_scale_L.alignment = 'CENTER'
                            col_arm_scale_L.operator("operator.arm_scale_l", text="", icon="UV_SYNC_SELECT", emboss=1)

                            col_arm_fk_L = col_arm_main_L.row(align=1)
                            col_arm_fk_L.scale_x = 1
                            col_arm_fk_L.scale_y = 1.5
                            col_arm_fk_L.alignment = 'CENTER'
                            col_arm_fk_L.operator("operator.arm_fk_l", text="FK")

                            col_arm_ik_L = col_arm_main_L.row(align=1)
                            col_arm_ik_L.scale_x = 1
                            col_arm_ik_L.scale_y = 1
                            col_arm_ik_L.alignment = 'CENTER'
                            col_arm_ik_L.operator("operator.arm_ik_l", text="IK")

                            col_elbow_toon_L = col_arm_main_L.column()
                            col_elbow_toon_L.scale_x = 1
                            col_elbow_toon_L.scale_y = 0.25
                            col_elbow_toon_L.alignment = 'CENTER'
                            col_elbow_toon_L.operator("operator.elbow_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_forearm_fk_L = col_arm_main_L.row(align=1)
                            col_forearm_fk_L.scale_x = 1
                            col_forearm_fk_L.scale_y = 1.5
                            col_forearm_fk_L.alignment = 'CENTER'
                            col_forearm_fk_L.operator("operator.forearm_fk_l", text="FK")

                            col_forearm_ik_L = col_arm_main_L.row(align=1)
                            col_forearm_ik_L.scale_x = 1
                            col_forearm_ik_L.scale_y = 1
                            col_forearm_ik_L.alignment = 'CENTER'
                            col_forearm_ik_L.operator("operator.forearm_ik_l", text="IK")

                            col_ankle_toon_L = col_arm_main_L.column()
                            col_ankle_toon_L.scale_x = 1
                            col_ankle_toon_L.scale_y = 0.25
                            col_ankle_toon_L.alignment = 'CENTER'
                            col_ankle_toon_L.operator("operator.ankle_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_carpal_fk_L = col_arm_main_L.row(align=1)
                            col_carpal_fk_L.scale_x = 1
                            col_carpal_fk_L.scale_y = 1.5
                            col_carpal_fk_L.alignment = 'CENTER'
                            col_carpal_fk_L.operator("operator.carpal_fk_l", text="FK")

                            col_carpal_ik_L = col_arm_main_L.row(align=1)
                            col_carpal_ik_L.scale_x = 1
                            col_carpal_ik_L.scale_y = 1
                            col_carpal_ik_L.alignment = 'CENTER'
                            col_carpal_ik_L.operator("operator.carpal_ik_l", text="IK")

                            col_hand_toon_L = col_arm_main_L.column()
                            col_hand_toon_L.scale_x = 1
                            col_hand_toon_L.scale_y = 0.25
                            col_hand_toon_L.alignment = 'CENTER'
                            col_hand_toon_L.operator("operator.hand_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_arm_toon_L = col_arm_L.column()
                            col_arm_toon_L.scale_x = 1
                            col_arm_toon_L.scale_y = 1
                            col_arm_toon_L.alignment = 'CENTER'
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.arm_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.elbow_pole_l", text="", icon="PROP_ON", emboss=0)
                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.forearm_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.separator()
                            col_arm_toon_L.operator("operator.carpal_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Hand R

                        row_legs = box_body.row(align=0)
                        row_legs.scale_x = 1.2
                        row_legs.scale_y = 1
                        row_legs.alignment = 'CENTER'

                        row_hand_R = row_legs.row(align=1)
                        row_hand_R.scale_x = 1
                        row_hand_R.scale_y = 1
                        row_hand_R.alignment = 'CENTER'

                        if arm['rig_type'] == "Biped":
                            col_bend_R = row_hand_R.row(align=1)
                            col_bend_R.scale_x = 0.5
                            col_bend_R.scale_y = 2
                            col_bend_R.alignment = 'CENTER'
                            col_bend_R.operator("operator.hand_roll_r", text="", icon="LOOP_FORWARDS", emboss=0)

                            row_hand_main_R = row_hand_R.row(align=1)
                            row_hand_main_R.scale_x = 1
                            row_hand_main_R.scale_y = 1
                            row_hand_main_R.alignment = 'CENTER'

                            col_spread_R = row_hand_main_R.column(align=0)
                            col_spread_R.scale_x = 0.8
                            col_spread_R.scale_y = 2
                            col_spread_R.alignment = 'CENTER'
                            col_spread_R.operator("operator.fing_spread_r", text="")

                            col_hand_main_R = row_hand_main_R.column(align=1)
                            col_hand_main_R.scale_x = 0.8
                            col_hand_main_R.scale_y = 1
                            col_hand_main_R.alignment = 'CENTER'

                            col_hand_pivot_R = col_hand_main_R.column(align=1)
                            col_hand_pivot_R.scale_x = 0.75
                            col_hand_pivot_R.scale_y = 0.35
                            col_hand_pivot_R.alignment = 'CENTER'
                            col_hand_pivot_R.operator("operator.hand_ik_pivot_point_r", text="")

                            col_hand_ik_R = col_hand_main_R.column(align=1)
                            col_hand_ik_R.scale_x = 1
                            col_hand_ik_R.scale_y = 1
                            col_hand_ik_R.alignment = 'CENTER'
                            col_hand_ik_R.operator("operator.hand_ik_ctrl_r", text="Hand IK")

                            col_hand_fk_R = col_hand_main_R.column(align=1)
                            col_hand_fk_R.scale_x = 1
                            col_hand_fk_R.scale_y = 1
                            col_hand_fk_R.alignment = 'CENTER'
                            col_hand_fk_R.operator("operator.hand_fk_r", text="Hand FK")

                            col_fingers_R = col_hand_main_R.row(align=1)
                            col_fingers_R.scale_x = 0.25
                            col_fingers_R.scale_y = 1
                            col_fingers_R.alignment = 'CENTER'

                        # Hand R Quadruped

                        if arm['rig_type'] == "Quadruped":
                            row_hand_main_R = row_hand_R.row(align=1)
                            row_hand_main_R.scale_x = 0.5
                            row_hand_main_R.scale_y = 1
                            row_hand_main_R.alignment = 'CENTER'

                            col_hand_main_R = row_hand_main_R.column(align=1)
                            col_hand_main_R.scale_x = 1
                            col_hand_main_R.scale_y = 1
                            col_hand_main_R.alignment = 'CENTER'

                            col_foot_R = col_hand_main_R.column(align=0)
                            col_foot_R.scale_x = 1
                            col_foot_R.scale_y = 1
                            col_foot_R.alignment = 'CENTER'

                            row_foot_R = col_foot_R.row(align=1)
                            row_foot_R.scale_x = 1
                            row_foot_R.scale_y = 1
                            row_foot_R.alignment = 'CENTER'

                            col_toe_1_R = row_foot_R.column(align=1)
                            col_toe_1_R.scale_x = 1
                            col_toe_1_R.scale_y = 0.75
                            col_toe_1_R.alignment = 'CENTER'
                            col_toe_1_R.operator("operator.fing_2_fk_r", text="")

                            col_toe_roll_2_R = row_foot_R.column(align=1)
                            col_toe_roll_2_R.scale_x = 0.75
                            col_toe_roll_2_R.scale_y = 0.75
                            col_toe_roll_2_R.alignment = 'CENTER'
                            col_toe_roll_2_R.operator("operator.fing_roll_2_r", text="", icon="LOOP_BACK", emboss=0)

                            col_toe_2_R = row_foot_R.column(align=1)
                            col_toe_2_R.scale_x = 1
                            col_toe_2_R.scale_y = 0.75
                            col_toe_2_R.alignment = 'CENTER'
                            col_toe_2_R.operator("operator.fing_1_fk_r", text="")

                            col_toe_roll_1_R = row_foot_R.column(align=1)
                            col_toe_roll_1_R.scale_x = 0.75
                            col_toe_roll_1_R.scale_y = 0.75
                            col_toe_roll_1_R.alignment = 'CENTER'
                            col_toe_roll_1_R.operator("operator.fing_roll_1_r", text="", icon="LOOP_BACK", emboss=0)

                            # Foot R

                            col_foot_R = row_foot_R.column(align=1)
                            col_foot_R.scale_x = 1
                            col_foot_R.scale_y = 0.75
                            col_foot_R.alignment = 'CENTER'
                            col_foot_R.operator("operator.hand_r", text="Hand R")

                            # FootRoll R

                            col_foot_roll_R = row_foot_R.column(align=0)
                            col_foot_roll_R.scale_x = 0.5
                            col_foot_roll_R.scale_y = 0.75
                            col_foot_roll_R.alignment = 'CENTER'
                            col_foot_roll_R.operator("operator.hand_roll_ctrl_r", text="", icon="LOOP_BACK", emboss=0)

                            col_fingers_R = col_hand_main_R.row(align=1)
                            col_fingers_R.scale_x = 0.25
                            col_fingers_R.scale_y = 1
                            col_fingers_R.alignment = 'CENTER'

                        # Fingers Option
                        if arm_bones['properties_arm_R']["toggle_fingers_R"] == 1:
                            col_lit_ctrl_R = col_fingers_R.column(align=0)
                            col_lit_ctrl_R.scale_x = 1.5
                            col_lit_ctrl_R.scale_y = 2
                            col_lit_ctrl_R.alignment = 'CENTER'
                            col_lit_ctrl_R.operator("operator.fing_lit_ctrl_r", text="")

                            col_lit_R = col_fingers_R.column(align=0)
                            col_lit_R.scale_x = 1.5
                            col_lit_R.scale_y = 0.7
                            col_lit_R.alignment = 'CENTER'
                            col_lit_R.operator("operator.fing_lit_2_r", text="")
                            col_lit_R.operator("operator.fing_lit_3_r", text="")
                            col_lit_R.operator("operator.fing_lit_4_r", text="")

                            col_ring_ctrl_R = col_fingers_R.column(align=0)
                            col_ring_ctrl_R.scale_x = 1.5
                            col_ring_ctrl_R.scale_y = 2.5
                            col_ring_ctrl_R.alignment = 'CENTER'
                            col_ring_ctrl_R.operator("operator.fing_ring_ctrl_r", text="")

                            col_ring_R = col_fingers_R.column(align=0)
                            col_ring_R.scale_x = 1.5
                            col_ring_R.scale_y = 0.85
                            col_ring_R.alignment = 'CENTER'
                            col_ring_R.operator("operator.fing_ring_2_r", text="")
                            col_ring_R.operator("operator.fing_ring_3_r", text="")
                            col_ring_R.operator("operator.fing_ring_4_r", text="")

                            col_mid_ctrl_R = col_fingers_R.column(align=0)
                            col_mid_ctrl_R.scale_x = 1.5
                            col_mid_ctrl_R.scale_y = 3
                            col_mid_ctrl_R.alignment = 'CENTER'
                            col_mid_ctrl_R.operator("operator.fing_mid_ctrl_r", text="")

                            col_mid_R = col_fingers_R.column(align=0)
                            col_mid_R.scale_x = 1.5
                            col_mid_R.scale_y = 1
                            col_mid_R.alignment = 'CENTER'
                            col_mid_R.operator("operator.fing_mid_2_r", text="")
                            col_mid_R.operator("operator.fing_mid_3_r", text="")
                            col_mid_R.operator("operator.fing_mid_4_r", text="")

                            col_index_ctrl_R = col_fingers_R.column(align=0)
                            col_index_ctrl_R.scale_x = 1.5
                            col_index_ctrl_R.scale_y = 2.7
                            col_index_ctrl_R.alignment = 'CENTER'
                            col_index_ctrl_R.operator("operator.fing_ind_ctrl_r", text="")

                            col_index_R = col_fingers_R.column(align=0)
                            col_index_R.scale_x = 1.5
                            col_index_R.scale_y = 0.8
                            col_index_R.alignment = 'CENTER'
                            col_index_R.operator("operator.fing_ind_2_r", text="")
                            col_index_R.operator("operator.fing_ind_3_r", text="")
                            col_index_R.operator("operator.fing_ind_4_r", text="")

                            col_thumb_ctrl_R = col_fingers_R.column(align=0)
                            col_thumb_ctrl_R.scale_x = 1.5
                            col_thumb_ctrl_R.scale_y = 1.5
                            col_thumb_ctrl_R.alignment = 'CENTER'
                            col_thumb_ctrl_R.operator("operator.fing_thumb_ctrl_r", text="")

                            col_thumb_R = col_fingers_R.column(align=0)
                            col_thumb_R.scale_x = 1.5
                            col_thumb_R.scale_y = 0.5
                            col_thumb_R.alignment = 'CENTER'
                            col_thumb_R.operator("operator.fing_thumb_1_r", text="")
                            col_thumb_R.operator("operator.fing_thumb_2_r", text="")
                            col_thumb_R.operator("operator.fing_thumb_3_r", text="")

                            col_fing_ik_R = col_hand_main_R.row(align=0)
                            col_fing_ik_R.scale_x = 0.25
                            col_fing_ik_R.scale_y = 0.5
                            col_fing_ik_R.alignment = 'CENTER'
                            col_fing_ik_R.operator("operator.fing_lit_ik_r", text="")
                            col_fing_ik_R.operator("operator.fing_ring_ik_r", text="")
                            col_fing_ik_R.operator("operator.fing_mid_ik_r", text="")
                            col_fing_ik_R.operator("operator.fing_ind_ik_r", text="")
                            col_fing_ik_R.operator("operator.fing_thumb_ik_r", text="")

                            col_hand_close_R = col_hand_main_R.column(align=0)
                            col_hand_close_R.scale_x = 1
                            col_hand_close_R.scale_y = 0.5
                            col_hand_close_R.alignment = 'CENTER'
                            col_hand_close_R.separator()
                            col_hand_close_R.operator("operator.hand_close_r", text="")
                        else:
                            if arm['rig_type'] == "Biped":
                                col_hand_main_R.scale_x = 0.112
                            if arm['rig_type'] == "Quadruped":
                                row_hand_main_R.scale_x = 1
                                col_hand_main_R.scale_x = 0.25

                            # Hand Sole R

                        if arm['rig_type'] == "Quadruped":
                            row_sole_R = col_hand_main_R.row(align=1)
                            row_sole_R.scale_x = 2
                            row_sole_R.scale_y = 1
                            row_sole_R.alignment = 'CENTER'

                            col_sole_R = row_sole_R.column(align=1)
                            col_sole_R.scale_x = 1
                            col_sole_R.scale_y = 0.75
                            col_sole_R.alignment = 'CENTER'
                            col_sole_R.operator("operator.hand_sole_ctrl_r", text="Hand Sole R")

                            col_sole_pivot_R = row_sole_R.column(align=1)
                            col_sole_pivot_R.scale_x = 0.25
                            col_sole_pivot_R.scale_y = 0.75
                            col_sole_pivot_R.alignment = 'CENTER'
                            col_sole_pivot_R.operator("operator.hand_sole_pivot_point_r", text="")

                        # Leg R
                        if arm['rig_type'] == "Biped":
                            row_legs_main = row_legs.row(align=0)
                            row_legs_main.scale_x = 0.75
                            row_legs_main.scale_y = 1
                            row_legs_main.alignment = 'CENTER'

                            row_leg_main_R = row_legs_main.row(align=1)
                            row_leg_main_R.scale_x = 1
                            row_leg_main_R.scale_y = 1
                            row_leg_main_R.alignment = 'CENTER'

                            col_leg_toon_R = row_leg_main_R.column()
                            col_leg_toon_R.scale_x = 0.5
                            col_leg_toon_R.scale_y = 1
                            col_leg_toon_R.alignment = 'CENTER'
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.thigh_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.knee_pole_r", text="", icon="PROP_ON", emboss=0)
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.shin_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_main_R = row_leg_main_R.column(align=1)
                            col_leg_main_R.scale_x = 1
                            col_leg_main_R.scale_y = 1
                            col_leg_main_R.alignment = 'CENTER'

                            col_pelvis_toon_R = col_leg_main_R.column()
                            col_pelvis_toon_R.scale_x = 1
                            col_pelvis_toon_R.scale_y = 0.1
                            col_pelvis_toon_R.alignment = 'CENTER'
                            col_pelvis_toon_R.operator("operator.pelvis_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_scale_R = col_leg_main_R.row(align=1)
                            col_leg_scale_R.scale_x = 2
                            col_leg_scale_R.scale_y = 1
                            col_leg_scale_R.alignment = 'CENTER'
                            col_leg_scale_R.operator("operator.leg_scale_r", text="", icon="UV_SYNC_SELECT", emboss=1)

                            col_leg_fk_ctrl_R = col_leg_main_R.row(align=1)
                            col_leg_fk_ctrl_R.scale_x = 1
                            col_leg_fk_ctrl_R.scale_y = 1
                            col_leg_fk_ctrl_R.alignment = 'CENTER'
                            col_leg_fk_ctrl_R.operator("operator.thigh_fk_ctrl_r", text="Ctrl")

                            col_leg_fk_R = col_leg_main_R.row(align=1)
                            col_leg_fk_R.scale_x = 1
                            col_leg_fk_R.scale_y = 3.5
                            col_leg_fk_R.alignment = 'CENTER'
                            col_leg_fk_R.operator("operator.thigh_fk_r", text="FK")

                            col_leg_ik_R = col_leg_main_R.row(align=1)
                            col_leg_ik_R.scale_x = 1
                            col_leg_ik_R.scale_y = 1
                            col_leg_ik_R.alignment = 'CENTER'
                            col_leg_ik_R.operator("operator.thigh_ik_r", text="IK")

                            col_knee_toon_R = col_leg_main_R.column()
                            col_knee_toon_R.scale_x = 1
                            col_knee_toon_R.scale_y = 0.25
                            col_knee_toon_R.alignment = 'CENTER'
                            col_knee_toon_R.operator("operator.knee_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_shin_fk_R = col_leg_main_R.row(align=1)
                            col_shin_fk_R.scale_x = 1
                            col_shin_fk_R.scale_y = 4
                            col_shin_fk_R.alignment = 'CENTER'
                            col_shin_fk_R.operator("operator.shin_fk_r", text="FK")

                            col_shin_ik_R = col_leg_main_R.row(align=1)
                            col_shin_ik_R.scale_x = 1
                            col_shin_ik_R.scale_y = 1
                            col_shin_ik_R.alignment = 'CENTER'
                            col_shin_ik_R.operator("operator.shin_ik_r", text="IK")

                            col_foot_toon_R = col_leg_main_R.column()
                            col_foot_toon_R.scale_x = 1
                            col_foot_toon_R.scale_y = 0.25
                            col_foot_toon_R.alignment = 'CENTER'
                            col_foot_toon_R.operator("operator.foot_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Quadruped Leg R
                        if arm['rig_type'] == "Quadruped":
                            row_legs_main = row_legs.row(align=0)
                            row_legs_main.scale_x = 0.75
                            row_legs_main.scale_y = 1
                            row_legs_main.alignment = 'CENTER'

                            row_leg_main_R = row_legs_main.row(align=1)
                            row_leg_main_R.scale_x = 1
                            row_leg_main_R.scale_y = 1
                            row_leg_main_R.alignment = 'CENTER'

                            col_leg_toon_R = row_leg_main_R.column()
                            col_leg_toon_R.scale_x = 0.5
                            col_leg_toon_R.scale_y = 1
                            col_leg_toon_R.alignment = 'CENTER'
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.thigh_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.knee_pole_r", text="", icon="PROP_ON", emboss=0)
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.shin_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.separator()
                            col_leg_toon_R.operator("operator.tarsal_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_main_R = row_leg_main_R.column(align=1)
                            col_leg_main_R.scale_x = 1
                            col_leg_main_R.scale_y = 1
                            col_leg_main_R.alignment = 'CENTER'

                            col_pelvis_toon_R = col_leg_main_R.column()
                            col_pelvis_toon_R.scale_x = 1
                            col_pelvis_toon_R.scale_y = 0.1
                            col_pelvis_toon_R.alignment = 'CENTER'
                            col_pelvis_toon_R.operator("operator.pelvis_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_scale_R = col_leg_main_R.row(align=1)
                            col_leg_scale_R.scale_x = 2
                            col_leg_scale_R.scale_y = 1
                            col_leg_scale_R.alignment = 'CENTER'
                            col_leg_scale_R.operator("operator.leg_scale_r", text="", icon="UV_SYNC_SELECT", emboss=1)

                            col_leg_fk_R = col_leg_main_R.row(align=1)
                            col_leg_fk_R.scale_x = 1
                            col_leg_fk_R.scale_y = 2
                            col_leg_fk_R.alignment = 'CENTER'
                            col_leg_fk_R.operator("operator.thigh_fk_r", text="FK")

                            col_leg_ik_R = col_leg_main_R.row(align=1)
                            col_leg_ik_R.scale_x = 1
                            col_leg_ik_R.scale_y = 1
                            col_leg_ik_R.alignment = 'CENTER'
                            col_leg_ik_R.operator("operator.thigh_ik_r", text="IK")

                            col_knee_toon_R = col_leg_main_R.column()
                            col_knee_toon_R.scale_x = 1
                            col_knee_toon_R.scale_y = 0.25
                            col_knee_toon_R.alignment = 'CENTER'
                            col_knee_toon_R.operator("operator.knee_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_shin_fk_R = col_leg_main_R.row(align=1)
                            col_shin_fk_R.scale_x = 1
                            col_shin_fk_R.scale_y = 2
                            col_shin_fk_R.alignment = 'CENTER'
                            col_shin_fk_R.operator("operator.shin_fk_r", text="FK")

                            col_shin_ik_R = col_leg_main_R.row(align=1)
                            col_shin_ik_R.scale_x = 1
                            col_shin_ik_R.scale_y = 1
                            col_shin_ik_R.alignment = 'CENTER'
                            col_shin_ik_R.operator("operator.shin_ik_r", text="IK")

                            col_hock_toon_R = col_leg_main_R.column()
                            col_hock_toon_R.scale_x = 1
                            col_hock_toon_R.scale_y = 0.25
                            col_hock_toon_R.alignment = 'CENTER'
                            col_hock_toon_R.operator("operator.hock_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_tarsal_fk_R = col_leg_main_R.row(align=1)
                            col_tarsal_fk_R.scale_x = 1
                            col_tarsal_fk_R.scale_y = 2
                            col_tarsal_fk_R.alignment = 'CENTER'
                            col_tarsal_fk_R.operator("operator.tarsal_fk_r", text="FK")

                            col_tarsal_ik_R = col_leg_main_R.row(align=1)
                            col_tarsal_ik_R.scale_x = 1
                            col_tarsal_ik_R.scale_y = 1
                            col_tarsal_ik_R.alignment = 'CENTER'
                            col_tarsal_ik_R.operator("operator.tarsal_ik_r", text="IK")

                            col_foot_toon_R = col_leg_main_R.column()
                            col_foot_toon_R.scale_x = 1
                            col_foot_toon_R.scale_y = 0.25
                            col_foot_toon_R.alignment = 'CENTER'
                            col_foot_toon_R.operator("operator.foot_toon_r", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Leg L
                        if arm['rig_type'] == "Biped":
                            row_leg_main_L = row_legs_main.row(align=1)
                            row_leg_main_R.scale_x = 1
                            row_leg_main_R.scale_y = 1
                            row_leg_main_R.alignment = 'CENTER'

                            col_leg_main_L = row_leg_main_L.column(align=1)
                            col_leg_main_L.scale_x = 1
                            col_leg_main_L.scale_y = 1
                            col_leg_main_L.alignment = 'CENTER'

                            col_pelvis_toon_L = col_leg_main_L.column()
                            col_pelvis_toon_L.scale_x = 1
                            col_pelvis_toon_L.scale_y = 0.1
                            col_pelvis_toon_L.alignment = 'CENTER'
                            col_pelvis_toon_L.operator("operator.pelvis_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_scale_L = col_leg_main_L.row(align=1)
                            col_leg_scale_L.scale_x = 2
                            col_leg_scale_L.scale_y = 1
                            col_leg_scale_L.alignment = 'CENTER'
                            col_leg_scale_L.operator("operator.leg_scale_l", text="", icon="UV_SYNC_SELECT", emboss=1)

                            col_leg_fk_ctrl_L = col_leg_main_L.row(align=1)
                            col_leg_fk_ctrl_L.scale_x = 1
                            col_leg_fk_ctrl_L.scale_y = 1
                            col_leg_fk_ctrl_L.alignment = 'CENTER'
                            col_leg_fk_ctrl_L.operator("operator.thigh_fk_ctrl_l", text="Ctrl")

                            col_leg_fk_L = col_leg_main_L.row(align=1)
                            col_leg_fk_L.scale_x = 1
                            col_leg_fk_L.scale_y = 3.5
                            col_leg_fk_L.alignment = 'CENTER'
                            col_leg_fk_L.operator("operator.thigh_fk_l", text="FK")

                            col_leg_ik_L = col_leg_main_L.row(align=1)
                            col_leg_ik_L.scale_x = 1
                            col_leg_ik_L.scale_y = 1
                            col_leg_ik_L.alignment = 'CENTER'
                            col_leg_ik_L.operator("operator.thigh_ik_l", text="IK")

                            col_knee_toon_L = col_leg_main_L.column()
                            col_knee_toon_L.scale_x = 1
                            col_knee_toon_L.scale_y = 0.25
                            col_knee_toon_L.alignment = 'CENTER'
                            col_knee_toon_L.operator("operator.knee_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_shin_fk_L = col_leg_main_L.row(align=1)
                            col_shin_fk_L.scale_x = 1
                            col_shin_fk_L.scale_y = 4
                            col_shin_fk_L.alignment = 'CENTER'
                            col_shin_fk_L.operator("operator.shin_fk_l", text="FK")

                            col_shin_ik_L = col_leg_main_L.row(align=1)
                            col_shin_ik_L.scale_x = 1
                            col_shin_ik_L.scale_y = 1
                            col_shin_ik_L.alignment = 'CENTER'
                            col_shin_ik_L.operator("operator.shin_ik_l", text="IK")

                            col_foot_toon_L = col_leg_main_L.column()
                            col_foot_toon_L.scale_x = 1
                            col_foot_toon_L.scale_y = 0.25
                            col_foot_toon_L.alignment = 'CENTER'
                            col_foot_toon_L.operator("operator.foot_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_toon_L = row_leg_main_L.column()
                            col_leg_toon_L.scale_x = 0.5
                            col_leg_toon_L.scale_y = 1
                            col_leg_toon_L.alignment = 'CENTER'
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.thigh_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.knee_pole_l", text="", icon="PROP_ON", emboss=0)
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.shin_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Quadruped Leg L
                        if arm['rig_type'] == "Quadruped":
                            row_legs_main = row_legs.row(align=0)
                            row_legs_main.scale_x = 0.75
                            row_legs_main.scale_y = 1
                            row_legs_main.alignment = 'CENTER'

                            row_leg_main_L = row_legs_main.row(align=1)
                            row_leg_main_L.scale_x = 1
                            row_leg_main_L.scale_y = 1
                            row_leg_main_L.alignment = 'CENTER'

                            col_leg_main_L = row_leg_main_L.column(align=1)
                            col_leg_main_L.scale_x = 1
                            col_leg_main_L.scale_y = 1
                            col_leg_main_L.alignment = 'CENTER'

                            col_pelvis_toon_L = col_leg_main_L.column()
                            col_pelvis_toon_L.scale_x = 1
                            col_pelvis_toon_L.scale_y = 0.1
                            col_pelvis_toon_L.alignment = 'CENTER'
                            col_pelvis_toon_L.operator("operator.pelvis_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_scale_L = col_leg_main_L.row(align=1)
                            col_leg_scale_L.scale_x = 2
                            col_leg_scale_L.scale_y = 1
                            col_leg_scale_L.alignment = 'CENTER'
                            col_leg_scale_L.operator("operator.leg_scale_l", text="", icon="UV_SYNC_SELECT", emboss=1)

                            col_leg_fk_L = col_leg_main_L.row(align=1)
                            col_leg_fk_L.scale_x = 1
                            col_leg_fk_L.scale_y = 2
                            col_leg_fk_L.alignment = 'CENTER'
                            col_leg_fk_L.operator("operator.thigh_fk_l", text="FK")

                            col_leg_ik_L = col_leg_main_L.row(align=1)
                            col_leg_ik_L.scale_x = 1
                            col_leg_ik_L.scale_y = 1
                            col_leg_ik_L.alignment = 'CENTER'
                            col_leg_ik_L.operator("operator.thigh_ik_l", text="IK")

                            col_knee_toon_L = col_leg_main_L.column()
                            col_knee_toon_L.scale_x = 1
                            col_knee_toon_L.scale_y = 0.25
                            col_knee_toon_L.alignment = 'CENTER'
                            col_knee_toon_L.operator("operator.knee_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_shin_fk_L = col_leg_main_L.row(align=1)
                            col_shin_fk_L.scale_x = 1
                            col_shin_fk_L.scale_y = 2
                            col_shin_fk_L.alignment = 'CENTER'
                            col_shin_fk_L.operator("operator.shin_fk_l", text="FK")

                            col_shin_ik_L = col_leg_main_L.row(align=1)
                            col_shin_ik_L.scale_x = 1
                            col_shin_ik_L.scale_y = 1
                            col_shin_ik_L.alignment = 'CENTER'
                            col_shin_ik_L.operator("operator.shin_ik_l", text="IK")

                            col_hock_toon_L = col_leg_main_L.column()
                            col_hock_toon_L.scale_x = 1
                            col_hock_toon_L.scale_y = 0.25
                            col_hock_toon_L.alignment = 'CENTER'
                            col_hock_toon_L.operator("operator.hock_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_tarsal_fk_L = col_leg_main_L.row(align=1)
                            col_tarsal_fk_L.scale_x = 1
                            col_tarsal_fk_L.scale_y = 2
                            col_tarsal_fk_L.alignment = 'CENTER'
                            col_tarsal_fk_L.operator("operator.tarsal_fk_l", text="FK")

                            col_tarsal_ik_L = col_leg_main_L.row(align=1)
                            col_tarsal_ik_L.scale_x = 1
                            col_tarsal_ik_L.scale_y = 1
                            col_tarsal_ik_L.alignment = 'CENTER'
                            col_tarsal_ik_L.operator("operator.tarsal_ik_l", text="IK")

                            col_foot_toon_L = col_leg_main_L.column()
                            col_foot_toon_L.scale_x = 1
                            col_foot_toon_L.scale_y = 0.25
                            col_foot_toon_L.alignment = 'CENTER'
                            col_foot_toon_L.operator("operator.foot_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                            col_leg_toon_L = row_leg_main_L.column()
                            col_leg_toon_L.scale_x = 0.5
                            col_leg_toon_L.scale_y = 1
                            col_leg_toon_L.alignment = 'CENTER'
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.thigh_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.knee_pole_l", text="", icon="PROP_ON", emboss=0)
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.shin_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.separator()
                            col_leg_toon_L.operator("operator.tarsal_toon_l", text="", icon="KEYFRAME_HLT", emboss=0)

                        # Hand L

                        col_hand_L = row_legs.column(align=1)
                        col_hand_L.scale_x = 1
                        col_hand_L.scale_y = 1
                        col_hand_L.alignment = 'CENTER'

                        row_hand_L = col_hand_L.row(align=1)
                        row_hand_L.scale_x = 1
                        row_hand_L.scale_y = 1
                        row_hand_L.alignment = 'CENTER'

                        if arm['rig_type'] == "Biped":
                            row_hand_main_L = row_hand_L.row(align=1)
                            row_hand_main_L.scale_x = 1
                            row_hand_main_L.scale_y = 1
                            row_hand_main_L.alignment = 'CENTER'

                            col_hand_main_L = row_hand_main_L.column(align=1)
                            col_hand_main_L.scale_x = 0.8
                            col_hand_main_L.scale_y = 1
                            col_hand_main_L.alignment = 'CENTER'

                            col_hand_pivot_L = col_hand_main_L.column(align=1)
                            col_hand_pivot_L.scale_x = 0.75
                            col_hand_pivot_L.scale_y = 0.35
                            col_hand_pivot_L.alignment = 'CENTER'
                            col_hand_pivot_L.operator("operator.hand_ik_pivot_point_l", text="")

                            col_hand_ik_L = col_hand_main_L.column(align=1)
                            col_hand_ik_L.scale_x = 1
                            col_hand_ik_L.scale_y = 1
                            col_hand_ik_L.alignment = 'CENTER'
                            col_hand_ik_L.operator("operator.hand_ik_ctrl_l", text="Hand IK")

                            col_hand_fk_L = col_hand_main_L.column(align=1)
                            col_hand_fk_L.scale_x = 1
                            col_hand_fk_L.scale_y = 1
                            col_hand_fk_L.alignment = 'CENTER'
                            col_hand_fk_L.operator("operator.hand_fk_l", text="Hand FK")

                            col_fingers_L = col_hand_main_L.row(align=1)
                            col_fingers_L.scale_x = 0.25
                            col_fingers_L.scale_y = 1
                            col_fingers_L.alignment = 'CENTER'

                        # Hand L Quadruped

                        if arm['rig_type'] == "Quadruped":
                            row_hand_main_L = row_hand_L.row(align=1)
                            row_hand_main_L.scale_x = 0.5
                            row_hand_main_L.scale_y = 1
                            row_hand_main_L.alignment = 'CENTER'

                            col_hand_main_L = row_hand_main_L.column(align=1)
                            col_hand_main_L.scale_x = 1
                            col_hand_main_L.scale_y = 1
                            col_hand_main_L.alignment = 'CENTER'

                            # Foot_L

                            col_foot_L = col_hand_main_L.column(align=0)
                            col_foot_L.scale_x = 1
                            col_foot_L.scale_y = 1
                            col_foot_L.alignment = 'CENTER'

                            row_foot_L = col_foot_L.row(align=1)
                            row_foot_L.scale_x = 1
                            row_foot_L.scale_y = 1
                            row_foot_L.alignment = 'CENTER'

                            # FootRoll L

                            col_foot_roll_L = row_foot_L.column(align=0)
                            col_foot_roll_L.scale_x = 0.5
                            col_foot_roll_L.scale_y = 0.75
                            col_foot_roll_L.alignment = 'CENTER'
                            col_foot_roll_L.operator("operator.hand_roll_ctrl_l", text="",
                                                     icon="LOOP_FORWARDS", emboss=0)

                            # Foot L

                            col_foot_L = row_foot_L.column(align=1)
                            col_foot_L.scale_x = 1
                            col_foot_L.scale_y = 0.75
                            col_foot_L.alignment = 'CENTER'
                            col_foot_L.operator("operator.hand_l", text="Hand L")

                            # Toes L

                            col_toe_roll_1_L = row_foot_L.row(align=1)
                            col_toe_roll_1_L.scale_x = 0.75
                            col_toe_roll_1_L.scale_y = 0.75
                            col_toe_roll_1_L.alignment = 'CENTER'
                            col_toe_roll_1_L.operator("operator.fing_roll_1_l", text="", icon="LOOP_FORWARDS", emboss=0)

                            col_toe_1_L = row_foot_L.row(align=1)
                            col_toe_1_L.scale_x = 1
                            col_toe_1_L.scale_y = 0.75
                            col_toe_1_L.alignment = 'CENTER'
                            col_toe_1_L.operator("operator.fing_1_fk_l", text="")

                            col_toe_roll_2_L = row_foot_L.row(align=1)
                            col_toe_roll_2_L.scale_x = 0.75
                            col_toe_roll_2_L.scale_y = 0.75
                            col_toe_roll_2_L.alignment = 'CENTER'
                            col_toe_roll_2_L.operator("operator.fing_roll_2_l", text="", icon="LOOP_FORWARDS", emboss=0)

                            col_toe_2_L = row_foot_L.row(align=1)
                            col_toe_2_L.scale_x = 1
                            col_toe_2_L.scale_y = 0.75
                            col_toe_2_L.alignment = 'CENTER'
                            col_toe_2_L.operator("operator.fing_2_fk_l", text="")

                            col_fingers_L = col_hand_main_L.row(align=1)
                            col_fingers_L.scale_x = 0.25
                            col_fingers_L.scale_y = 1
                            col_fingers_L.alignment = 'CENTER'

                        # Fingers Option
                        if arm_bones['properties_arm_L']["toggle_fingers_L"] == 1:
                            col_thumb_L = col_fingers_L.column(align=0)
                            col_thumb_L.scale_x = 1.5
                            col_thumb_L.scale_y = 0.5
                            col_thumb_L.alignment = 'CENTER'
                            col_thumb_L.operator("operator.fing_thumb_1_l", text="")
                            col_thumb_L.operator("operator.fing_thumb_2_l", text="")
                            col_thumb_L.operator("operator.fing_thumb_3_l", text="")

                            col_thumb_ctrl_L = col_fingers_L.column(align=0)
                            col_thumb_ctrl_L.scale_x = 1.5
                            col_thumb_ctrl_L.scale_y = 1.5
                            col_thumb_ctrl_L.alignment = 'CENTER'
                            col_thumb_ctrl_L.operator("operator.fing_thumb_ctrl_l", text="")

                            col_index_L = col_fingers_L.column(align=0)
                            col_index_L.scale_x = 1.5
                            col_index_L.scale_y = 0.8
                            col_index_L.alignment = 'CENTER'
                            col_index_L.operator("operator.fing_ind_2_l", text="")
                            col_index_L.operator("operator.fing_ind_3_l", text="")
                            col_index_L.operator("operator.fing_ind_4_l", text="")

                            col_index_ctrl_L = col_fingers_L.column(align=0)
                            col_index_ctrl_L.scale_x = 1.5
                            col_index_ctrl_L.scale_y = 2.7
                            col_index_ctrl_L.alignment = 'CENTER'
                            col_index_ctrl_L.operator("operator.fing_ind_ctrl_l", text="")

                            col_mid_L = col_fingers_L.column(align=0)
                            col_mid_L.scale_x = 1.5
                            col_mid_L.scale_y = 1
                            col_mid_L.alignment = 'CENTER'
                            col_mid_L.operator("operator.fing_mid_2_l", text="")
                            col_mid_L.operator("operator.fing_mid_3_l", text="")
                            col_mid_L.operator("operator.fing_mid_4_l", text="")

                            col_mid_ctrl_L = col_fingers_L.column(align=0)
                            col_mid_ctrl_L.scale_x = 1.5
                            col_mid_ctrl_L.scale_y = 3
                            col_mid_ctrl_L.alignment = 'CENTER'
                            col_mid_ctrl_L.operator("operator.fing_mid_ctrl_l", text="")

                            col_ring_L = col_fingers_L.column(align=0)
                            col_ring_L.scale_x = 1.5
                            col_ring_L.scale_y = 0.85
                            col_ring_L.alignment = 'CENTER'
                            col_ring_L.operator("operator.fing_ring_2_l", text="")
                            col_ring_L.operator("operator.fing_ring_3_l", text="")
                            col_ring_L.operator("operator.fing_ring_4_l", text="")

                            col_ring_ctrl_L = col_fingers_L.column(align=0)
                            col_ring_ctrl_L.scale_x = 1.5
                            col_ring_ctrl_L.scale_y = 2.5
                            col_ring_ctrl_L.alignment = 'CENTER'
                            col_ring_ctrl_L.operator("operator.fing_ring_ctrl_l", text="")

                            col_lit_L = col_fingers_L.column(align=0)
                            col_lit_L.scale_x = 1.5
                            col_lit_L.scale_y = 0.7
                            col_lit_L.alignment = 'CENTER'
                            col_lit_L.operator("operator.fing_lit_2_l", text="")
                            col_lit_L.operator("operator.fing_lit_3_l", text="")
                            col_lit_L.operator("operator.fing_lit_4_l", text="")

                            col_lit_ctrl_L = col_fingers_L.column(align=0)
                            col_lit_ctrl_L.scale_x = 1.5
                            col_lit_ctrl_L.scale_y = 2
                            col_lit_ctrl_L.alignment = 'CENTER'
                            col_lit_ctrl_L.operator("operator.fing_lit_ctrl_l", text="")

                            col_fing_ik_L = col_hand_main_L.row(align=0)
                            col_fing_ik_L.scale_x = 0.25
                            col_fing_ik_L.scale_y = 0.5
                            col_fing_ik_L.alignment = 'CENTER'
                            col_fing_ik_L.operator("operator.fing_thumb_ik_l", text="")
                            col_fing_ik_L.operator("operator.fing_ind_ik_l", text="")
                            col_fing_ik_L.operator("operator.fing_mid_ik_l", text="")
                            col_fing_ik_L.operator("operator.fing_ring_ik_l", text="")
                            col_fing_ik_L.operator("operator.fing_lit_ik_l", text="")

                            col_hand_close_L = col_hand_main_L.column(align=0)
                            col_hand_close_L.scale_x = 1
                            col_hand_close_L.scale_y = 0.5
                            col_hand_close_L.alignment = 'CENTER'
                            col_hand_close_L.separator()
                            col_hand_close_L.operator("operator.hand_close_l", text="")

                        else:
                            if arm['rig_type'] == "Biped":
                                col_hand_main_L.scale_x = 0.112
                            if arm['rig_type'] == "Quadruped":
                                row_hand_main_L.scale_x = 1
                                col_hand_main_L.scale_x = 0.25

                            # Hand Sole L

                        if arm['rig_type'] == "Quadruped":
                            row_sole_L = col_hand_main_L.row(align=1)
                            row_sole_L.scale_x = 2
                            row_sole_L.scale_y = 1
                            row_sole_L.alignment = 'CENTER'

                            col_sole_pivot_L = row_sole_L.column(align=1)
                            col_sole_pivot_L.scale_x = 0.25
                            col_sole_pivot_L.scale_y = 0.75
                            col_sole_pivot_L.alignment = 'CENTER'
                            col_sole_pivot_L.operator("operator.hand_sole_pivot_point_l", text="")

                            col_sole_L = row_sole_L.column(align=1)
                            col_sole_L.scale_x = 1
                            col_sole_L.scale_y = 0.75
                            col_sole_L.alignment = 'CENTER'
                            col_sole_L.operator("operator.hand_sole_ctrl_l", text="Hand Sole L")

                        # Hand Spread L
                        if arm['rig_type'] == "Biped":
                            col_spread_R = row_hand_main_L.column(align=0)
                            col_spread_R.scale_x = 0.8
                            col_spread_R.scale_y = 2
                            col_spread_R.alignment = 'CENTER'
                            col_spread_R.operator("operator.fing_spread_l", text="")

                            col_bend_L = row_hand_L.row(align=1)
                            col_bend_L.scale_x = 0.5
                            col_bend_L.scale_y = 2
                            col_bend_L.alignment = 'CENTER'
                            col_bend_L.operator("operator.hand_roll_l", text="", icon="LOOP_BACK", emboss=0)

                        # Toes R

                        row_feet = box_body.row(align=0)
                        row_feet.scale_x = 1
                        row_feet.scale_y = 1
                        row_feet.alignment = 'CENTER'

                        col_foot_R = row_feet.column(align=0)
                        col_foot_R.scale_x = 1
                        col_foot_R.scale_y = 1
                        col_foot_R.alignment = 'CENTER'

                        row_foot_R = col_foot_R.row(align=1)
                        row_foot_R.scale_x = 1
                        row_foot_R.scale_y = 1
                        row_foot_R.alignment = 'CENTER'

                        col_toe_1_R = row_foot_R.row(align=1)
                        col_toe_1_R.scale_x = 0.8
                        col_toe_1_R.scale_y = 0.75
                        col_toe_1_R.alignment = 'CENTER'
                        col_toe_1_R.operator("operator.toes_ik_ctrl_r", text="")
                        col_toe_1_R.operator("operator.toe_2_fk_r", text="")

                        col_toe_roll_2_R = row_foot_R.row(align=1)
                        col_toe_roll_2_R.scale_x = 0.8
                        col_toe_roll_2_R.scale_y = 0.75
                        col_toe_roll_2_R.alignment = 'CENTER'
                        col_toe_roll_2_R.operator("operator.toe_roll_2_r", text="", icon="LOOP_BACK", emboss=0)

                        col_toe_2_R = row_foot_R.row(align=1)
                        col_toe_2_R.scale_x = 0.8
                        col_toe_2_R.scale_y = 0.75
                        col_toe_2_R.alignment = 'CENTER'
                        col_toe_2_R.operator("operator.toes_ik_ctrl_mid_r", text="")
                        col_toe_2_R.operator("operator.toe_1_fk_r", text="")

                        col_toe_roll_1_R = row_foot_R.row(align=1)
                        col_toe_roll_1_R.scale_x = 0.8
                        col_toe_roll_1_R.scale_y = 0.75
                        col_toe_roll_1_R.alignment = 'CENTER'
                        col_toe_roll_1_R.operator("operator.toe_roll_1_r", text="", icon="LOOP_BACK", emboss=0)

                        # Foot R

                        col_foot_ctrl_R = row_foot_R.column(align=1)
                        col_foot_ctrl_R.scale_x = 1
                        col_foot_ctrl_R.scale_y = 0.75
                        col_foot_ctrl_R.alignment = 'CENTER'
                        col_foot_ctrl_R.operator("operator.foot_r", text="Foot R")

                        # FootRoll R

                        col_foot_roll_R = row_foot_R.column(align=0)
                        col_foot_roll_R.scale_x = 0.8
                        col_foot_roll_R.scale_y = 0.75
                        col_foot_roll_R.alignment = 'CENTER'
                        col_foot_roll_R.operator("operator.foot_roll_ctrl_r", text="", icon="LOOP_BACK", emboss=0)

                        # Individual Toes R

                        # Toes Toggle
                        if arm_bones['properties_leg_R']["toggle_toes_R"] == 1:
                            # Spread R
                            row_toes_spread_R = col_foot_R.row(align=1)
                            row_toes_spread_R.scale_x = 4.5
                            row_toes_spread_R.scale_y = 0.35
                            row_toes_spread_R.alignment = 'CENTER'
                            row_toes_spread_R.operator("operator.toes_spread_r", text="")

                            # Toes R

                            row_toes_R = col_foot_R.row(align=1)
                            row_toes_R.scale_x = 0.4
                            row_toes_R.scale_y = 1
                            row_toes_R.alignment = 'CENTER'

                            col_lit_ctrl_R = row_toes_R.column(align=0)
                            col_lit_ctrl_R.scale_x = 1.2
                            col_lit_ctrl_R.scale_y = 2
                            col_lit_ctrl_R.alignment = 'CENTER'
                            col_lit_ctrl_R.operator("operator.toe_lit_ctrl_r", text="")

                            col_lit_R = row_toes_R.column(align=1)
                            col_lit_R.scale_x = 1
                            col_lit_R.scale_y = 1
                            col_lit_R.alignment = 'CENTER'
                            col_lit_R.operator("operator.toe_lit_2_r", text="")
                            col_lit_R.operator("operator.toe_lit_3_r", text="")

                            col_ring_ctrl_R = row_toes_R.column(align=0)
                            col_ring_ctrl_R.scale_x = 1.2
                            col_ring_ctrl_R.scale_y = 2.5
                            col_ring_ctrl_R.alignment = 'CENTER'
                            col_ring_ctrl_R.operator("operator.toe_fourth_ctrl_r", text="")

                            col_ring_R = row_toes_R.column(align=1)
                            col_ring_R.scale_x = 1
                            col_ring_R.scale_y = 0.85
                            col_ring_R.alignment = 'CENTER'
                            col_ring_R.operator("operator.toe_fourth_2_r", text="")
                            col_ring_R.operator("operator.toe_fourth_3_r", text="")
                            col_ring_R.operator("operator.toe_fourth_4_r", text="")

                            col_mid_ctrl_R = row_toes_R.column(align=0)
                            col_mid_ctrl_R.scale_x = 1.2
                            col_mid_ctrl_R.scale_y = 3
                            col_mid_ctrl_R.alignment = 'CENTER'
                            col_mid_ctrl_R.operator("operator.toe_mid_ctrl_r", text="")

                            col_mid_R = row_toes_R.column(align=1)
                            col_mid_R.scale_x = 1
                            col_mid_R.scale_y = 1
                            col_mid_R.alignment = 'CENTER'
                            col_mid_R.operator("operator.toe_mid_2_r", text="")
                            col_mid_R.operator("operator.toe_mid_3_r", text="")
                            col_mid_R.operator("operator.toe_mid_4_r", text="")

                            col_index_ctrl_R = row_toes_R.column(align=0)
                            col_index_ctrl_R.scale_x = 1.2
                            col_index_ctrl_R.scale_y = 2.7
                            col_index_ctrl_R.alignment = 'CENTER'
                            col_index_ctrl_R.operator("operator.toe_ind_ctrl_r", text="")

                            col_index_R = row_toes_R.column(align=1)
                            col_index_R.scale_x = 1
                            col_index_R.scale_y = 0.9
                            col_index_R.alignment = 'CENTER'
                            col_index_R.operator("operator.toe_ind_2_r", text="")
                            col_index_R.operator("operator.toe_ind_3_r", text="")
                            col_index_R.operator("operator.toe_ind_4_r", text="")

                            col_thumb_ctrl_R = row_toes_R.column(align=0)
                            col_thumb_ctrl_R.scale_x = 1.2
                            col_thumb_ctrl_R.scale_y = 2
                            col_thumb_ctrl_R.alignment = 'CENTER'
                            col_thumb_ctrl_R.operator("operator.toe_big_ctrl_r", text="")

                            col_thumb_R = row_toes_R.column(align=1)
                            col_thumb_R.scale_x = 1
                            col_thumb_R.scale_y = 1
                            col_thumb_R.alignment = 'CENTER'
                            col_thumb_R.operator("operator.toe_big_2_r", text="")
                            col_thumb_R.operator("operator.toe_big_3_r", text="")

                            # Toes IK R

                            row_toes_ik_R = col_foot_R.row(align=0)
                            row_toes_ik_R.scale_x = 0.6
                            row_toes_ik_R.scale_y = 0.5
                            row_toes_ik_R.alignment = 'CENTER'
                            row_toes_ik_R.operator("operator.toe_lit_ik_r", text="")
                            row_toes_ik_R.operator("operator.toe_fourth_ik_r", text="")
                            row_toes_ik_R.operator("operator.toe_mid_ik_r", text="")
                            row_toes_ik_R.operator("operator.toe_ind_ik_r", text="")
                            row_toes_ik_R.operator("operator.toe_big_ik_r", text="")

                        # Foot_L

                        col_foot_L = row_feet.column(align=0)
                        col_foot_L.scale_x = 1
                        col_foot_L.scale_y = 1
                        col_foot_L.alignment = 'CENTER'

                        row_foot_L = col_foot_L.row(align=1)
                        row_foot_L.scale_x = 1
                        row_foot_L.scale_y = 1
                        row_foot_L.alignment = 'CENTER'

                        # FootRoll L

                        col_foot_roll_L = row_foot_L.column(align=0)
                        col_foot_roll_L.scale_x = 0.5
                        col_foot_roll_L.scale_y = 0.75
                        col_foot_roll_L.alignment = 'CENTER'
                        col_foot_roll_L.operator("operator.foot_roll_ctrl_l", text="", icon="LOOP_FORWARDS", emboss=0)

                        # Foot L

                        col_foot_ctrl_L = row_foot_L.column(align=1)
                        col_foot_ctrl_L.scale_x = 1
                        col_foot_ctrl_L.scale_y = 0.75
                        col_foot_ctrl_L.alignment = 'CENTER'
                        col_foot_ctrl_L.operator("operator.foot_l", text="Foot L")

                        # Toes L

                        col_toe_roll_1_L = row_foot_L.row(align=1)
                        col_toe_roll_1_L.scale_x = 0.8
                        col_toe_roll_1_L.scale_y = 0.75
                        col_toe_roll_1_L.alignment = 'CENTER'
                        col_toe_roll_1_L.operator("operator.toe_roll_1_l", text="", icon="LOOP_FORWARDS", emboss=0)

                        col_toe_1_L = row_foot_L.row(align=1)
                        col_toe_1_L.scale_x = 0.8
                        col_toe_1_L.scale_y = 0.75
                        col_toe_1_L.alignment = 'CENTER'
                        col_toe_1_L.operator("operator.toe_1_fk_l", text="")
                        col_toe_1_L.operator("operator.toes_ik_ctrl_mid_l", text="")

                        col_toe_roll_2_L = row_foot_L.row(align=1)
                        col_toe_roll_2_L.scale_x = 0.8
                        col_toe_roll_2_L.scale_y = 0.75
                        col_toe_roll_2_L.alignment = 'CENTER'
                        col_toe_roll_2_L.operator("operator.toe_roll_2_l", text="", icon="LOOP_FORWARDS", emboss=0)

                        col_toe_2_L = row_foot_L.row(align=1)
                        col_toe_2_L.scale_x = 0.8
                        col_toe_2_L.scale_y = 0.75
                        col_toe_2_L.alignment = 'CENTER'
                        col_toe_2_L.operator("operator.toe_2_fk_l", text="")
                        col_toe_2_L.operator("operator.toes_ik_ctrl_l", text="")

                        # Individual Toes L

                        # Toes Toggle
                        if arm_bones['properties_leg_L']["toggle_toes_L"] == 1:
                            # Spread L
                            row_toes_spread_L = col_foot_L.row(align=1)
                            row_toes_spread_L.scale_x = 4.5
                            row_toes_spread_L.scale_y = 0.35
                            row_toes_spread_L.alignment = 'CENTER'
                            row_toes_spread_L.operator("operator.toes_spread_l", text="")

                            # Toes L

                            row_toes_L = col_foot_L.row(align=1)
                            row_toes_L.scale_x = 0.4
                            row_toes_L.scale_y = 1
                            row_toes_L.alignment = 'CENTER'

                            col_thumb_L = row_toes_L.column(align=1)
                            col_thumb_L.scale_x = 1
                            col_thumb_L.scale_y = 1
                            col_thumb_L.alignment = 'CENTER'
                            col_thumb_L.operator("operator.toe_big_2_l", text="")
                            col_thumb_L.operator("operator.toe_big_3_l", text="")

                            col_thumb_ctrl_L = row_toes_L.column(align=0)
                            col_thumb_ctrl_L.scale_x = 1.2
                            col_thumb_ctrl_L.scale_y = 2
                            col_thumb_ctrl_L.alignment = 'CENTER'
                            col_thumb_ctrl_L.operator("operator.toe_big_ctrl_l", text="")

                            col_index_L = row_toes_L.column(align=1)
                            col_index_L.scale_x = 1
                            col_index_L.scale_y = 0.9
                            col_index_L.alignment = 'CENTER'
                            col_index_L.operator("operator.toe_ind_2_l", text="")
                            col_index_L.operator("operator.toe_ind_3_l", text="")
                            col_index_L.operator("operator.toe_ind_4_l", text="")

                            col_index_ctrl_L = row_toes_L.column(align=0)
                            col_index_ctrl_L.scale_x = 1.2
                            col_index_ctrl_L.scale_y = 2.7
                            col_index_ctrl_L.alignment = 'CENTER'
                            col_index_ctrl_L.operator("operator.toe_ind_ctrl_l", text="")

                            col_mid_L = row_toes_L.column(align=1)
                            col_mid_L.scale_x = 1
                            col_mid_L.scale_y = 1
                            col_mid_L.alignment = 'CENTER'
                            col_mid_L.operator("operator.toe_mid_2_l", text="")
                            col_mid_L.operator("operator.toe_mid_3_l", text="")
                            col_mid_L.operator("operator.toe_mid_4_l", text="")

                            col_mid_ctrl_L = row_toes_L.column(align=0)
                            col_mid_ctrl_L.scale_x = 1.2
                            col_mid_ctrl_L.scale_y = 3
                            col_mid_ctrl_L.alignment = 'CENTER'
                            col_mid_ctrl_L.operator("operator.toe_mid_ctrl_l", text="")

                            col_ring_L = row_toes_L.column(align=1)
                            col_ring_L.scale_x = 1
                            col_ring_L.scale_y = 0.85
                            col_ring_L.alignment = 'CENTER'
                            col_ring_L.operator("operator.toe_fourth_2_l", text="")
                            col_ring_L.operator("operator.toe_fourth_3_l", text="")
                            col_ring_L.operator("operator.toe_fourth_4_l", text="")

                            col_ring_ctrl_L = row_toes_L.column(align=0)
                            col_ring_ctrl_L.scale_x = 1.2
                            col_ring_ctrl_L.scale_y = 2.5
                            col_ring_ctrl_L.alignment = 'CENTER'
                            col_ring_ctrl_L.operator("operator.toe_fourth_ctrl_l", text="")

                            col_lit_L = row_toes_L.column(align=1)
                            col_lit_L.scale_x = 1
                            col_lit_L.scale_y = 1
                            col_lit_L.alignment = 'CENTER'
                            col_lit_L.operator("operator.toe_lit_2_l", text="")
                            col_lit_L.operator("operator.toe_lit_3_l", text="")

                            col_lit_ctrl_L = row_toes_L.column(align=0)
                            col_lit_ctrl_L.scale_x = 1.2
                            col_lit_ctrl_L.scale_y = 2
                            col_lit_ctrl_L.alignment = 'CENTER'
                            col_lit_ctrl_L.operator("operator.toe_lit_ctrl_l", text="")

                            # Toes IK R

                            row_toes_ik_L = col_foot_L.row(align=0)
                            row_toes_ik_L.scale_x = 0.6
                            row_toes_ik_L.scale_y = 0.5
                            row_toes_ik_L.alignment = 'CENTER'
                            row_toes_ik_L.operator("operator.toe_big_ik_l", text="")
                            row_toes_ik_L.operator("operator.toe_ind_ik_l", text="")
                            row_toes_ik_L.operator("operator.toe_mid_ik_l", text="")
                            row_toes_ik_L.operator("operator.toe_fourth_ik_l", text="")
                            row_toes_ik_L.operator("operator.toe_lit_ik_l", text="")

                        # Sole R

                        row_sole = box_body.row(align=0)
                        row_sole.scale_x = 1
                        row_sole.scale_y = 1
                        row_sole.alignment = 'CENTER'

                        row_sole_R = row_sole.row(align=1)
                        row_sole_R.scale_x = 2
                        row_sole_R.scale_y = 1
                        row_sole_R.alignment = 'CENTER'

                        col_sole_R = row_sole_R.column(align=1)
                        col_sole_R.scale_x = 1
                        col_sole_R.scale_y = 0.75
                        col_sole_R.alignment = 'CENTER'
                        col_sole_R.operator("operator.sole_ctrl_r", text="Sole R")

                        col_sole_pivot_R = row_sole_R.column(align=1)
                        col_sole_pivot_R.scale_x = 0.5
                        col_sole_pivot_R.scale_y = 0.75
                        col_sole_pivot_R.alignment = 'CENTER'
                        col_sole_pivot_R.operator("operator.sole_pivot_point_r", text="")

                        # Sole L

                        row_sole_L = row_sole.row(align=1)
                        row_sole_L.scale_x = 2
                        row_sole_L.scale_y = 1
                        row_sole_L.alignment = 'CENTER'

                        col_sole_pivot_L = row_sole_L.column(align=1)
                        col_sole_pivot_L.scale_x = 0.5
                        col_sole_pivot_L.scale_y = 0.75
                        col_sole_pivot_L.alignment = 'CENTER'
                        col_sole_pivot_L.operator("operator.sole_pivot_point_l", text="")

                        col_sole_L = row_sole_L.column(align=1)
                        col_sole_L.scale_x = 1
                        col_sole_L.scale_y = 0.75
                        col_sole_L.alignment = 'CENTER'
                        col_sole_L.operator("operator.sole_ctrl_l", text="Sole L")

                        # Master

                        row_master = box_body.row(align=1)
                        row_master.scale_x = 5
                        row_master.scale_y = 1
                        row_master.alignment = 'CENTER'
                        row_master.separator

                        col_master_pivot = row_master.column(align=1)
                        col_master_pivot.scale_x = 0.5
                        col_master_pivot.scale_y = 0.75
                        col_master_pivot.alignment = 'CENTER'
                        col_master_pivot.separator()
                        col_master_pivot.operator("operator.master", text="Master")
                        col_master_pivot.separator()
                        col_master_pivot.separator()

                        col_master = row_master.column(align=1)
                        col_master.scale_x = 0.3
                        col_master.scale_y = 0.75
                        col_master.alignment = 'CENTER'
                        col_master.separator()
                        col_master.operator("operator.master_extra", text="Master Extra")

                        col_master = row_master.column(align=1)
                        col_master.scale_x = 0.4
                        col_master.scale_y = 0.75
                        col_master.alignment = 'CENTER'
                        col_master.separator()
                        col_master.operator("operator.master_pivot_point", text="")
                        col_master.separator()
                        col_master.separator()

                        row_pivot = row_master.column(align=1)
                        row_pivot.alignment = 'CENTER'
                        row_pivot.scale_x = 0.3
                        row_pivot.scale_y = 0.75
                        row_pivot.separator()
                        row_pivot.operator("reset.master_pivot", text='Reset Pivot', icon='PIVOT_CURSOR')
                        row_pivot.separator()
                        row_pivot.separator()

                    # View

                        row_view_main = box_body.row(align=0)
                        row_view_main.scale_x = 1
                        row_view_main.scale_y = 1
                        row_view_main.alignment = 'CENTER'

                        row_view = row_view_main.row(align=0)
                        row_view.scale_x = 1
                        row_view.scale_y = 1
                        row_view.alignment = 'CENTER'
                        row_view.operator("operator.zoom", text="Zoom to Selected", icon='ZOOM_IN')

                        row_model_res = row_view_main.row(align=0)
                        row_model_res.scale_x = 0.7
                        row_model_res.scale_y = 1
                        row_model_res.alignment = 'CENTER'
                        row_model_res.prop(arm_bones['properties'], '["model_res"]', text="Model_Res", toggle=True)

                        if props.gui_picker_body_props:

                            # Sliders_R

                            col_sliders_R = box_R.column()
                            col_sliders_R.scale_x = 1
                            col_sliders_R.scale_y = 0.75
                            col_sliders_R.alignment = 'CENTER'

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 13
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_head_props = col_sliders_R.row()
                            row_head_props.scale_x = BL_Ver(4, 2.5)
                            row_head_props.scale_y = 1
                            row_head_props.alignment = 'CENTER'
                            row_head_props.label(text="HEAD")
                            row_switch = col_sliders_R.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.head_list", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_head']['space_head'] == 0 else "Follow Torso"),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_head'], 'space_head',
                                          toggle=True, icon_only=1, emboss=1)
                            col_sliders_R.separator()

                            row_head_props = col_sliders_R.row()
                            row_head_props.scale_x = BL_Ver(4, 2.5)
                            row_head_props.scale_y = 1
                            row_head_props.alignment = 'CENTER'
                            row_head_props.label(text="NECK")
                            row_neck_switch = col_sliders_R.row(align=True)
                            row_neck_switch.alignment = 'CENTER'
                            row_neck_switch.scale_x = 2.5
                            row_neck_switch.scale_y = 1
                            row_neck_switch.operator(
                                "show.neck_list", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_head']['space_neck'] == 0 else "Follow Torso"),
                                emboss=True)
                            col_prop = row_neck_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_head'], 'space_neck',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 6
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_arm_R_props = col_sliders_R.row()
                            row_arm_R_props.scale_x = BL_Ver(4, 2.5)
                            row_arm_R_props.scale_y = 1
                            row_arm_R_props.alignment = 'CENTER'
                            row_arm_R_props.label(text="ARM RIGHT")
                            row_fk = col_sliders_R.row(align=True)
                            row_fk.alignment = 'CENTER'
                            row_fk.scale_y = 1
                            row_fk_1 = row_fk.row()
                            row_fk_1.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_1.operator("snap.arm_fk_to_ik_r", text="", icon='PLAY_REVERSE', emboss=True)
                            row_fk_2 = row_fk.row()
                            row_fk_2.scale_x = BL_Ver(0.7, 0.7)
                            row_fk_2.label(text="{}".format(
                                "FK" if arm_bones['properties_arm_R']['ik_arm_R'] == 1 else "IK"),)
                            row_fk_3 = row_fk.row()
                            row_fk_3.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_3.operator("snap.arm_ik_to_fk_r", text="", icon='PLAY', emboss=True)
                            row_fk_4 = row_fk.row()
                            row_fk_4.scale_x = BL_Ver(2, 2)
                            col_prop = row_fk_4.column(align=True)
                            col_prop.scale_x = 0.6
                            col_prop.prop(arm_bones['properties_arm_R'], 'ik_arm_R', toggle=True, icon_only=1, emboss=1)
                            row_switch = col_sliders_R.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.arm_list_r", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_R']['space_arm_R'] == 0
                                    else (
                                        "Follow Pelvis"
                                        if arm_bones['properties_arm_R']['space_arm_R'] == 1
                                        else (
                                            "Follow Torso"
                                            if arm_bones['properties_arm_R']['space_arm_R'] == 2 else "Follow Head"))),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_R'], 'space_arm_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_stretchy = col_sliders_R.row(align=True)
                            row_stretchy.alignment = 'CENTER'
                            row_stretchy.scale_x = 2.5
                            row_stretchy.scale_y = 1
                            row_stretchy.prop(arm_bones['properties_arm_R'], 'toon_arm_R',
                                              text="Stretchy IK", toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 8
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_pole_R_props = col_sliders_R.row()
                            row_pole_R_props.scale_x = BL_Ver(4, 2.5)
                            row_pole_R_props.scale_y = 1.5
                            row_pole_R_props.alignment = 'CENTER'
                            row_pole_R_props.label(text="ELBOW POLE")
                            row_pole_R_prop = row_pole_R_props.row()
                            row_pole_R_prop.prop(arm_bones['properties_arm_R'], 'toggle_arm_ik_pole_R', text="")
                            row_switch = col_sliders_R.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.arm_pole_list_r", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_R']['space_arm_ik_pole_R'] == 0 else "Follow Torso"),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_R'], 'space_arm_ik_pole_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_pin = col_sliders_R.row(align=True)
                            row_pin.scale_x = BL_Ver(3.8, 2.2)
                            row_pin.scale_y = 1
                            row_pin.alignment = 'CENTER'
                            row_pin.label(text="Pin Elbow")
                            row_pin_op = row_pin.row()
                            row_pin_op.scale_x = BL_Ver(1, 1.5)
                            if arm_bones['properties_arm_R']['pin_elbow_R'] < 0.1:
                                row_pin_op.operator("pin.elbow_r", emboss=0, icon="CHECKBOX_DEHLT", text="")
                            else:
                                row_pin_op.operator("unpin.elbow_r", emboss=0, icon="CHECKBOX_HLT", text="")
                            col_prop = row_pin.column(align=True)
                            col_prop.scale_x = BL_Ver(0.45, 0.55)
                            col_prop.prop(arm_bones['properties_arm_R'], 'pin_elbow_R',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 9
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_hand_R_props = col_sliders_R.row()
                            col_hand_R_props.scale_x = BL_Ver(4, 2.5)
                            col_hand_R_props.scale_y = 1
                            col_hand_R_props.alignment = 'CENTER'
                            col_hand_R_props.label(text="HAND RIGHT")
                            row_hand = col_sliders_R.row(align=True)
                            row_hand.alignment = 'CENTER'
                            row_hand.scale_x = 2.5
                            row_hand.scale_y = 1
                            row_hand.operator(
                                "show.hand_list_r", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_R']['space_hand_R'] == 0 else "Follow Arm"),
                                emboss=True)
                            col_prop = row_hand.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_R'], 'space_hand_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_pivot = col_sliders_R.row(align=True)
                            row_pivot.alignment = 'CENTER'
                            row_pivot.scale_x = 2.8
                            row_pivot.scale_y = 1.2
                            row_pivot.operator("reset.hand_r_pivot", text='Reset Pivot',
                                               icon='PIVOT_CURSOR', emboss=True)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 4
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_fing_R_props = col_sliders_R.row()
                            col_fing_R_props.scale_x = BL_Ver(4, 2.5)
                            col_fing_R_props.scale_y = 1
                            col_fing_R_props.alignment = 'CENTER'
                            col_fing_R_props.label(text="FINGERS")
                            row_fing = col_sliders_R.row(align=True)
                            row_fing.alignment = 'CENTER'
                            row_fing.scale_x = 2.5
                            row_fing.scale_y = 1
                            row_fing.operator(
                                "show.fing_all_list_r", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_R']['space_fing_all_R'] == 0 else "Follow Hand"),
                                emboss=True)
                            col_prop = row_fing.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_R'], 'space_fing_thumb_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop = col_sliders_R.row(align=True)
                            row_prop.scale_y = 1
                            row_prop.scale_x = 0.8
                            row_prop.prop(arm_bones['properties_arm_R'], 'space_fing_lit_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop.prop(arm_bones['properties_arm_R'], 'space_fing_ring_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop.prop(arm_bones['properties_arm_R'], 'space_fing_mid_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop.prop(arm_bones['properties_arm_R'], 'space_fing_ind_R',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 8
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_leg_R_props = col_sliders_R.row()
                            col_leg_R_props.scale_x = BL_Ver(4, 2.5)
                            col_leg_R_props.scale_y = 1
                            col_leg_R_props.alignment = 'CENTER'
                            col_leg_R_props.label(text="LEG RIGHT")
                            row_fk = col_sliders_R.row(align=True)
                            row_fk.alignment = 'CENTER'
                            row_fk.scale_y = 1
                            row_fk_1 = row_fk.row()
                            row_fk_1.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_1.operator("snap.leg_fk_to_ik_r", text="", icon='PLAY_REVERSE', emboss=True)
                            row_fk_2 = row_fk.row()
                            row_fk_2.scale_x = BL_Ver(0.7, 0.7)
                            row_fk_2.label(text="{}".format(
                                "FK" if arm_bones['properties_leg_R']['ik_leg_R'] == 1 else "IK"))
                            row_fk_3 = row_fk.row()
                            row_fk_3.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_3.operator("snap.leg_ik_to_fk_r", text="", icon='PLAY', emboss=True)
                            row_fk_4 = row_fk.row()
                            row_fk_4.scale_x = BL_Ver(2, 2)
                            col_prop = row_fk_4.column(align=True)
                            col_prop.scale_x = 0.6
                            col_prop.prop(arm_bones['properties_leg_R'], 'ik_leg_R', toggle=True, icon_only=1, emboss=1)
                            row_switch = col_sliders_R.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.leg_list_r", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_leg_R']['space_leg_R'] == 0 else "Follow Torso"),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.6
                            col_prop.prop(arm_bones['properties_leg_R'], 'space_leg_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_stretchy = col_sliders_R.row(align=True)
                            row_stretchy.alignment = 'CENTER'
                            row_stretchy.scale_x = 2.5
                            row_stretchy.scale_y = 1
                            row_stretchy.prop(arm_bones['properties_leg_R'], 'toon_leg_R',
                                              text="Stretchy IK", toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 2
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_pole_R_props = col_sliders_R.row()
                            row_pole_R_props.scale_x = BL_Ver(4, 2.5)
                            row_pole_R_props.scale_y = 1.5
                            row_pole_R_props.alignment = 'CENTER'
                            row_pole_R_props.label(text="KNEE POLE")
                            row_pole_R_prop = row_pole_R_props.row()
                            row_pole_R_prop.prop(arm_bones['properties_leg_R'], 'toggle_leg_ik_pole_R', text="")
                            row_switch = col_sliders_R.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.leg_pole_list_r", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_leg_R']['space_leg_ik_pole_R'] == 0
                                    else (
                                        "Follow Torso"
                                        if arm_bones['properties_leg_R']['space_leg_ik_pole_R'] == 1 else
                                        "Follow Foot")),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_leg_R'], 'space_leg_ik_pole_R',
                                          toggle=True, icon_only=1, emboss=1)
                            row_pin = col_sliders_R.row(align=True)
                            row_pin.scale_x = BL_Ver(3.8, 2.2)
                            row_pin.scale_y = 1
                            row_pin.alignment = 'CENTER'
                            row_pin.label(text="Pin Knee")
                            row_pin_op = row_pin.row()
                            row_pin_op.scale_x = BL_Ver(1, 1.5)
                            if arm_bones['properties_leg_R']['pin_knee_R'] < 0.1:
                                row_pin_op.operator("pin.knee_r", emboss=0, icon="CHECKBOX_DEHLT", text="")
                            else:
                                row_pin_op.operator("unpin.knee_r", emboss=0, icon="CHECKBOX_HLT", text="")
                            col_prop = row_pin.column(align=True)
                            col_prop.scale_x = BL_Ver(0.45, 0.55)
                            col_prop.prop(arm_bones['properties_leg_R'], 'pin_knee_R',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_R.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 5
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_foot_R_props = col_sliders_R.row()
                            col_foot_R_props.scale_x = BL_Ver(4, 2.5)
                            col_foot_R_props.scale_y = 1
                            col_foot_R_props.alignment = 'CENTER'
                            col_foot_R_props.label(text="TOES")
                            col_sliders_R.prop(
                                arm_bones['properties_leg_R'],
                                'ik_toes_all_R', text="{}".format(
                                    "FK" if arm_bones['properties_leg_R']['ik_toes_all_R'] == 1 else "IK"),
                                toggle=True, icon_only=1, emboss=1)

                        # Sliders_L

                            col_sliders_L = box_L.column()
                            col_sliders_L.scale_x = 1
                            col_sliders_L.scale_y = 0.75
                            col_sliders_L.alignment = 'CENTER'

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 35
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_arm_L_props = col_sliders_L.row()
                            row_arm_L_props.scale_x = BL_Ver(4, 2.5)
                            row_arm_L_props.scale_y = 1
                            row_arm_L_props.alignment = 'CENTER'
                            row_arm_L_props.label(text="ARM LEFT")
                            row_fk = col_sliders_L.row(align=True)
                            row_fk.alignment = 'CENTER'
                            row_fk.scale_y = 1
                            row_fk_1 = row_fk.row()
                            row_fk_1.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_1.operator("snap.arm_fk_to_ik_l", text="", icon='PLAY_REVERSE', emboss=True)
                            row_fk_2 = row_fk.row()
                            row_fk_2.scale_x = BL_Ver(0.7, 0.7)
                            row_fk_2.label(text="{}".format(
                                "FK" if arm_bones['properties_arm_L']['ik_arm_L'] == 1 else "IK"),)
                            row_fk_3 = row_fk.row()
                            row_fk_3.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_3.operator("snap.arm_ik_to_fk_l", text="", icon='PLAY', emboss=True)
                            row_fk_4 = row_fk.row()
                            row_fk_4.scale_x = BL_Ver(2, 2)
                            col_prop = row_fk_4.column(align=True)
                            col_prop.scale_x = 0.6
                            col_prop.prop(arm_bones['properties_arm_L'], 'ik_arm_L', toggle=True, icon_only=1, emboss=1)
                            row_switch = col_sliders_L.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.arm_list_l", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_L']['space_arm_L'] == 0
                                    else (
                                        "Follow Pelvis"
                                        if arm_bones['properties_arm_L']['space_arm_L'] == 1
                                        else (
                                            "Follow Torso"
                                            if arm_bones['properties_arm_L']['space_arm_L'] == 2 else "Follow Head"))),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_L'], 'space_arm_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_stretchy = col_sliders_L.row(align=True)
                            row_stretchy.alignment = 'CENTER'
                            row_stretchy.scale_x = 2.5
                            row_stretchy.scale_y = 1
                            row_stretchy.prop(arm_bones['properties_arm_L'], 'toon_arm_L',
                                              text="Stretchy IK", toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 8
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_pole_L_props = col_sliders_L.row()
                            row_pole_L_props.scale_x = BL_Ver(4, 2.5)
                            row_pole_L_props.scale_y = 1.5
                            row_pole_L_props.alignment = 'CENTER'
                            row_pole_L_props.label(text="ELBOW POLE")
                            row_pole_L_prop = row_pole_L_props.row()
                            row_pole_L_prop.prop(arm_bones['properties_arm_L'], 'toggle_arm_ik_pole_L', text="")
                            row_switch = col_sliders_L.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.arm_pole_list_l", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_L']['space_arm_ik_pole_L'] == 0 else "Follow Torso"),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_L'], 'space_arm_ik_pole_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_pin = col_sliders_L.row(align=True)
                            row_pin.scale_x = BL_Ver(3.8, 2.2)
                            row_pin.scale_y = 1
                            row_pin.alignment = 'CENTER'
                            row_pin.label(text="Pin Elbow")
                            row_pin_op = row_pin.row()
                            row_pin_op.scale_x = BL_Ver(1, 1.5)
                            if arm_bones['properties_arm_L']['pin_elbow_L'] < 0.1:
                                row_pin_op.operator("pin.elbow_l", emboss=0, icon="CHECKBOX_DEHLT", text="")
                            else:
                                row_pin_op.operator("unpin.elbow_l", emboss=0, icon="CHECKBOX_HLT", text="")
                            col_prop = row_pin.column(align=True)
                            col_prop.scale_x = BL_Ver(0.45, 0.55)
                            col_prop.prop(arm_bones['properties_arm_L'], 'pin_elbow_L',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 9
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_hand_L_props = col_sliders_L.row()
                            col_hand_L_props.scale_x = BL_Ver(4, 2.5)
                            col_hand_L_props.scale_y = 1
                            col_hand_L_props.alignment = 'CENTER'
                            col_hand_L_props.label(text="HAND LEFT")
                            row_hand = col_sliders_L.row(align=True)
                            row_hand.alignment = 'CENTER'
                            row_hand.scale_x = 2.5
                            row_hand.scale_y = 1
                            row_hand.operator(
                                "show.hand_list_l", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_L']['space_hand_L'] == 0 else "Follow Arm"),
                                emboss=True)
                            col_prop = row_hand.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_L'], 'space_hand_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_pivot = col_sliders_L.row(align=True)
                            row_pivot.alignment = 'CENTER'
                            row_pivot.scale_x = 2.8
                            row_pivot.scale_y = 1.2
                            row_pivot.operator("reset.hand_l_pivot", text='Reset Pivot',
                                               icon='PIVOT_CURSOR', emboss=True)

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 4
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_fing_L_props = col_sliders_L.row()
                            col_fing_L_props.scale_x = BL_Ver(4, 2.5)
                            col_fing_L_props.scale_y = 1
                            col_fing_L_props.alignment = 'CENTER'
                            col_fing_L_props.label(text="FINGERS")
                            row_fing = col_sliders_L.row(align=True)
                            row_fing.alignment = 'CENTER'
                            row_fing.scale_x = 2.5
                            row_fing.scale_y = 1
                            col_prop = row_fing.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_arm_L'], 'space_fing_thumb_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_fing.operator(
                                "show.fing_all_list_l", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_arm_L']['space_fing_all_L'] == 0 else "Follow Hand"),
                                emboss=True)
                            row_prop = col_sliders_L.row(align=True)
                            row_prop.scale_y = 1
                            row_prop.scale_x = 0.8
                            row_prop.prop(arm_bones['properties_arm_L'], 'space_fing_ind_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop.prop(arm_bones['properties_arm_L'], 'space_fing_mid_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop.prop(arm_bones['properties_arm_L'], 'space_fing_ring_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_prop.prop(arm_bones['properties_arm_L'], 'space_fing_lit_L',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 8
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_leg_L_props = col_sliders_L.row()
                            col_leg_L_props.scale_x = BL_Ver(4, 2.5)
                            col_leg_L_props.scale_y = 1
                            col_leg_L_props.alignment = 'CENTER'
                            col_leg_L_props.label(text="LEG LEFT")
                            row_fk = col_sliders_L.row(align=True)
                            row_fk.alignment = 'CENTER'
                            row_fk.scale_y = 1
                            row_fk_1 = row_fk.row()
                            row_fk_1.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_1.operator("snap.leg_fk_to_ik_l", text="", icon='PLAY_REVERSE', emboss=True)
                            row_fk_2 = row_fk.row()
                            row_fk_2.scale_x = BL_Ver(0.7, 0.7)
                            row_fk_2.label(text="{}".format(
                                "FK" if arm_bones['properties_leg_L']['ik_leg_L'] == 1 else "IK"))
                            row_fk_3 = row_fk.row()
                            row_fk_3.scale_x = BL_Ver(2.1, 2.1)
                            row_fk_3.operator("snap.leg_ik_to_fk_l", text="", icon='PLAY', emboss=True)
                            row_fk_4 = row_fk.row()
                            row_fk_4.scale_x = BL_Ver(2, 2)
                            col_prop = row_fk_4.column(align=True)
                            col_prop.scale_x = 0.6
                            col_prop.prop(arm_bones['properties_leg_L'], 'ik_leg_L', toggle=True, icon_only=1, emboss=1)
                            row_switch = col_sliders_L.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.leg_list_l", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_leg_L']['space_leg_L'] == 0 else "Follow Torso"),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.6
                            col_prop.prop(arm_bones['properties_leg_L'], 'space_leg_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_stretchy = col_sliders_L.row(align=True)
                            row_stretchy.alignment = 'CENTER'
                            row_stretchy.scale_x = 2.5
                            row_stretchy.scale_y = 1
                            row_stretchy.prop(arm_bones['properties_leg_L'], 'toon_leg_L',
                                              text="Stretchy IK", toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 2
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            row_pole_L_props = col_sliders_L.row()
                            row_pole_L_props.scale_x = BL_Ver(4, 2.5)
                            row_pole_L_props.scale_y = 1.5
                            row_pole_L_props.alignment = 'CENTER'
                            row_pole_L_props.label(text="KNEE POLE")
                            row_pole_L_prop = row_pole_L_props.row()
                            row_pole_L_prop.prop(arm_bones['properties_leg_L'], 'toggle_leg_ik_pole_L', text="")
                            row_switch = col_sliders_L.row(align=True)
                            row_switch.alignment = 'CENTER'
                            row_switch.scale_x = 2.5
                            row_switch.scale_y = 1
                            row_switch.operator(
                                "show.leg_pole_list_l", text="{}".format(
                                    "      Free      "
                                    if arm_bones['properties_leg_L']['space_leg_ik_pole_L'] == 0
                                    else (
                                        "Follow Torso"
                                        if arm_bones['properties_leg_L']['space_leg_ik_pole_L'] == 1 else
                                        "Follow Foot")),
                                emboss=True)
                            col_prop = row_switch.column(align=True)
                            col_prop.scale_x = 0.5
                            col_prop.prop(arm_bones['properties_leg_L'], 'space_leg_ik_pole_L',
                                          toggle=True, icon_only=1, emboss=1)
                            row_pin = col_sliders_L.row(align=True)
                            row_pin.scale_x = BL_Ver(3.8, 2.2)
                            row_pin.scale_y = 1
                            row_pin.alignment = 'CENTER'
                            row_pin.label(text="Pin Knee")
                            row_pin_op = row_pin.row()
                            row_pin_op.scale_x = BL_Ver(1, 1.5)
                            if arm_bones['properties_leg_L']['pin_knee_L'] < 0.1:
                                row_pin_op.operator("pin.knee_l", emboss=0, icon="CHECKBOX_DEHLT", text="")
                            else:
                                row_pin_op.operator("unpin.knee_l", emboss=0, icon="CHECKBOX_HLT", text="")
                            col_prop = row_pin.column(align=True)
                            col_prop.scale_x = BL_Ver(0.45, 0.55)
                            col_prop.prop(arm_bones['properties_leg_L'], 'pin_knee_L',
                                          toggle=True, icon_only=1, emboss=1)

                            col_space = col_sliders_L.column()
                            col_space.scale_x = 2.5
                            col_space.scale_y = 5
                            col_space.alignment = 'CENTER'
                            col_space.separator()

                            col_foot_L_props = col_sliders_L.row()
                            col_foot_L_props.scale_x = BL_Ver(4, 2.5)
                            col_foot_L_props.scale_y = 1
                            col_foot_L_props.alignment = 'CENTER'
                            col_foot_L_props.label(text="TOES")
                            col_sliders_L.prop(
                                arm_bones['properties_leg_L'],
                                'ik_toes_all_L', text="{}".format(
                                    "FK" if arm_bones['properties_leg_L']['ik_toes_all_L'] == 1 else "IK"),
                                toggle=True, icon_only=1, emboss=1)

                    elif props.gui_picker_body_props:
                        # Properties Only GUI
                        col_key = box.column()
                        col_key.alignment = 'CENTER'
                        row_key = col_key.row(align=1)
                        row_key.scale_x = 1
                        row_key.scale_y = 1
                        row_key.alignment = 'CENTER'
                        row_key.operator("keyframe.main_props", text='Keyframe All Properties',
                                         icon='KEYINGSET', emboss=1)

                        # Look slider

                        col.separator()

                        col_look = box.column()
                        col_look.alignment = 'CENTER'
                        row_look_title = col_look.row(align=1)
                        row_look_title.scale_x = 0.7
                        row_look_title.scale_y = 1
                        row_look_title.alignment = 'CENTER'

                        row_label = row_look_title.row(align=1)
                        row_label.scale_x = 1
                        row_label.scale_y = 1
                        row_label.alignment = 'LEFT'
                        row_label.label(text="Free")

                        row_label = row_look_title.row(align=1)
                        row_label.scale_x = 1
                        row_label.scale_y = 1
                        row_label.alignment = 'CENTER'
                        row_label.label(text="Body")

                        row_label = row_look_title.row(align=1)
                        row_label.scale_x = 1
                        row_label.scale_y = 1
                        row_label.alignment = 'CENTER'
                        row_label.label(text="Torso")

                        row_label = row_look_title.column(align=1)
                        row_label.scale_x = 1
                        row_label.scale_y = 1
                        row_label.alignment = 'RIGHT'
                        row_label.label(text="Head")

                        row_look = col_look.row()
                        row_look.scale_x = 1
                        row_look.scale_y = 1
                        row_look.alignment = 'CENTER'
                        row_look.prop(arm_bones['properties_head'], 'look_switch', text="Eyes Target", slider=True)

                        # Head sliders

                        row_head = box.row()
                        row_head.alignment = 'CENTER'
                        col_head = row_head.column()
                        col_head.scale_x = 1
                        col_head.scale_y = 0.75
                        col_head.alignment = 'CENTER'
                        col_head.label(text="HEAD")
                        col_head.prop(
                            arm_bones['properties_head'],
                            'space_head', text="{}".format(
                                "Free" if arm_bones['properties_head']['space_head'] == 0 else "Follow Torso"),
                            toggle=True, icon_only=1, emboss=1)
                        col_head.label(text="NECK")
                        col_head.prop(
                            arm_bones['properties_head'],
                            'space_neck', text="{}".format(
                                "Free" if arm_bones['properties_head']['space_neck'] == 0 else "Follow Torso"),
                            toggle=True, icon_only=1, emboss=1)

                        # Body sliders R

                        row_body = box.row()

                        box_R = row_body.column(align=1)
                        box_R.scale_x = 1
                        box_R.scale_y = 1
                        box_R.alignment = 'LEFT'

                        col_arm_R_props = box_R.column()
                        col_arm_R_props.scale_x = 2.5
                        col_arm_R_props.scale_y = 0.75
                        col_arm_R_props.alignment = 'CENTER'
                        col_arm_R_props.label(text="ARM_R")
                        col_arm_R_props.prop(
                            arm_bones['properties_arm_R'],
                            'ik_arm_R', text="{}".format(
                                "FK" if arm_bones['properties_arm_R']['ik_arm_R'] == 1 else "IK"),
                            toggle=True, icon_only=1, emboss=1)
                        col_arm_R_props.prop(
                            arm_bones['properties_arm_R'],
                            'space_arm_R', text="{}".format(
                                "Free" if arm_bones['properties_arm_R']['space_arm_R'] == 0 else "Follow Torso"),
                            toggle=True, icon_only=1, emboss=1)
                        col_arm_R_props.prop(arm_bones['properties_arm_R'], 'toon_arm_R',
                                             text="Str IK", toggle=True, icon_only=1, emboss=1)

                        col_space = box_R.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 8
                        col_space.alignment = 'CENTER'

                        col_hand_R_props = box_R.column()
                        col_hand_R_props.scale_x = 2.5
                        col_hand_R_props.scale_y = 0.75
                        col_hand_R_props.alignment = 'CENTER'
                        col_hand_R_props.label(text="HAND_R")
                        col_hand_R_props.prop(
                            arm_bones['properties_arm_R'],
                            'space_hand_R', text="{}".format(
                                "Free" if arm_bones['properties_arm_R']['space_hand_R'] == 0 else "Follow Arm"),
                            toggle=True, icon_only=1, emboss=1)

                        col_space = box_R.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 4
                        col_space.alignment = 'CENTER'

                        col_fing_R_props = box_R.column()
                        col_fing_R_props.scale_x = 2.5
                        col_fing_R_props.scale_y = 0.75
                        col_fing_R_props.alignment = 'CENTER'
                        col_fing_R_props.label(text="FING_R")
                        col_fing_R_props.prop(
                            arm_bones['properties_arm_R'],
                            'space_fing_all_R', text="{}".format(
                                "Free" if arm_bones['properties_arm_R']['space_fing_all_R'] == 0 else "Follow Hand"),
                            toggle=True, icon_only=1, emboss=1)

                        col_space = box_R.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 4
                        col_space.alignment = 'CENTER'

                        col_leg_R_props = box_R.column()
                        col_leg_R_props.scale_x = 2.5
                        col_leg_R_props.scale_y = 0.75
                        col_leg_R_props.alignment = 'CENTER'
                        col_leg_R_props.label(text="LEG_R")
                        col_leg_R_props.prop(
                            arm_bones['properties_leg_R'],
                            'ik_leg_R', text="{}".format(
                                "FK" if arm_bones['properties_leg_R']['ik_leg_R'] == 1 else "IK"),
                            toggle=True, icon_only=1, emboss=1)
                        col_leg_R_props.prop(
                            arm_bones['properties_leg_R'],
                            'space_leg_R', text="{}".format(
                                "Free" if arm_bones['properties_leg_R']['space_leg_R'] == 0 else "Follow Torso"),
                            toggle=True, icon_only=1, emboss=1)
                        col_leg_R_props.prop(arm_bones['properties_leg_R'], 'toon_leg_R',
                                             text="Str IK", toggle=True, icon_only=1, emboss=1)

                        col_space = box_R.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 3
                        col_space.alignment = 'CENTER'

                        col_foot_R_props = box_R.column()
                        col_foot_R_props.scale_x = 2.5
                        col_foot_R_props.scale_y = 0.75
                        col_foot_R_props.alignment = 'CENTER'
                        col_foot_R_props.label(text="TOES_R")
                        col_foot_R_props.prop(
                            arm_bones['properties_leg_R'],
                            'ik_toes_all_R', text="{}".format(
                                "FK" if arm_bones['properties_leg_R']['ik_toes_all_R'] == 1 else "IK"),
                            toggle=True, icon_only=1, emboss=1)

                        # Body Sliders_L

                        box_L = row_body.column(align=1)
                        box_L.scale_x = 1
                        box_L.scale_y = 1
                        box_L.alignment = 'LEFT'

                        col_arm_L_props = box_L.column()
                        col_arm_L_props.scale_x = 2.5
                        col_arm_L_props.scale_y = 0.75
                        col_arm_L_props.alignment = 'CENTER'
                        col_arm_L_props.label(text="ARM_L")
                        col_arm_L_props.prop(
                            arm_bones['properties_arm_L'],
                            'ik_arm_L', text="{}".format(
                                "FK" if arm_bones['properties_arm_L']['ik_arm_L'] == 1 else "IK"),
                            toggle=True, icon_only=1, emboss=1)
                        col_arm_L_props.prop(
                            arm_bones['properties_arm_L'],
                            'space_arm_L', text="{}".format(
                                "Free" if arm_bones['properties_arm_L']['space_arm_L'] == 0 else "Follow Torso"),
                            toggle=True, icon_only=1, emboss=1)
                        col_arm_L_props.prop(arm_bones['properties_arm_L'], 'toon_arm_L',
                                             text="Str IK", toggle=True, icon_only=1, emboss=1)

                        col_space = box_L.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 8
                        col_space.alignment = 'CENTER'

                        col_hand_L_props = box_L.column()
                        col_hand_L_props.scale_x = 2.5
                        col_hand_L_props.scale_y = 0.75
                        col_hand_L_props.alignment = 'CENTER'
                        col_hand_L_props.label(text="HAND_L")
                        col_hand_L_props.prop(
                            arm_bones['properties_arm_L'],
                            'space_hand_L', text="{}".format(
                                "Free" if arm_bones['properties_arm_L']['space_hand_L'] == 0 else "Follow Arm"),
                            toggle=True, icon_only=1, emboss=1)

                        col_space = box_L.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 4
                        col_space.alignment = 'CENTER'

                        col_fing_L_props = box_L.column()
                        col_fing_L_props.scale_x = 2.5
                        col_fing_L_props.scale_y = 0.75
                        col_fing_L_props.alignment = 'CENTER'
                        col_fing_L_props.label(text="FING_L")
                        col_fing_L_props.prop(
                            arm_bones['properties_arm_L'],
                            'space_fing_all_L', text="{}".format(
                                "Free" if arm_bones['properties_arm_L']['space_fing_all_L'] == 0 else "Follow Hand"),
                            toggle=True, icon_only=1, emboss=1)

                        col_space = box_L.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 4
                        col_space.alignment = 'CENTER'

                        col_leg_L_props = box_L.column()
                        col_leg_L_props.scale_x = 2.5
                        col_leg_L_props.scale_y = 0.75
                        col_leg_L_props.alignment = 'CENTER'
                        col_leg_L_props.label(text="LEG_L")
                        col_leg_L_props.prop(
                            arm_bones['properties_leg_L'],
                            'ik_leg_L', text="{}".format(
                                "FK" if arm_bones['properties_leg_L']['ik_leg_L'] == 1 else "IK"),
                            toggle=True, icon_only=1, emboss=1)
                        col_leg_L_props.prop(
                            arm_bones['properties_leg_L'],
                            'space_leg_L', text="{}".format(
                                "Free" if arm_bones['properties_leg_L']['space_leg_L'] == 0 else "Follow Torso"),
                            toggle=True, icon_only=1, emboss=1)
                        col_leg_L_props.prop(arm_bones['properties_leg_L'], 'toon_leg_L',
                                             text="Str IK", toggle=True, icon_only=1, emboss=1)

                        col_space = box_L.column()
                        col_space.scale_x = 2.5
                        col_space.scale_y = 3
                        col_space.alignment = 'CENTER'

                        col_foot_L_props = box_L.column()
                        col_foot_L_props.scale_x = 2.5
                        col_foot_L_props.scale_y = 0.75
                        col_foot_L_props.alignment = 'CENTER'
                        col_foot_L_props.label(text="TOES_L")
                        col_foot_L_props.prop(
                            arm_bones['properties_leg_L'],
                            'ik_toes_all_L', text="{}".format(
                                "FK" if arm_bones['properties_leg_L']['ik_toes_all_L'] == 1 else "IK"),
                            toggle=True, icon_only=1, emboss=1)

                        # Model Resolution

                        box.separator()

                        row_model_res = box.row()
                        row_model_res.alignment = 'CENTER'
                        col_model_res = row_model_res.column()
                        col_model_res.scale_x = 1
                        col_model_res.scale_y = 0.75
                        col_model_res.alignment = 'CENTER'
                        col_model_res.prop(arm_bones['properties'], '["model_res"]', text="Model_Res", toggle=True)

                # collapsed box
                elif "gui_picker_body" in arm:
                    row.operator("gui.blenrig_6_tabs", icon="MOD_ARMATURE", emboss=1).tab = "gui_picker_body"
                    row.label(text="BODY PICKER & PROPERTIES")

    ################ FACE #######################################
            if context.mode == "POSE":

                if "gui_picker_face" in arm:
                    box = layout.column()
                    col = box.column()
                    row = col.row()
                # expanded box
                if "gui_picker_face" in arm and arm["gui_picker_face"]:
                    row.operator("gui.blenrig_6_tabs", icon="MONKEY", emboss=1).tab = "gui_picker_face"
                    row.label(text="FACE PICKER")
                    box.separator()

                    # Columns
                    face_row = box.row(align=1)
                    face_row.scale_x = 1
                    face_row.scale_y = 1
                    face_row.alignment = 'CENTER'

                    # Right Column
                    right_col = face_row.column(align=1)
                    right_col.scale_x = 0.5
                    right_col.scale_y = 1
                    right_col.alignment = 'CENTER'

                    col_space = right_col.column()
                    col_space.scale_y = 15
                    col_space.separator()

                    # Ear Up R
                    ear_up_R = right_col.column()
                    ear_up_R.scale_x = 1
                    ear_up_R.scale_y = 0.5
                    ear_up_R.alignment = 'CENTER'
                    ear_up_R.operator("operator.ear_up_r", text="")

                    # Ear R
                    ear_R = right_col.column()
                    ear_R.scale_x = 1
                    ear_R.scale_y = 2
                    ear_R.alignment = 'CENTER'
                    ear_R.operator("operator.ear_r", text="")

                    # Ear Low R
                    ear_low_R = right_col.column()
                    ear_low_R.scale_x = 1
                    ear_low_R.scale_y = 0.5
                    ear_low_R.alignment = 'CENTER'
                    ear_low_R.operator("operator.ear_low_r", text="")

                    # Main Face
                    box_face = face_row.column(align=1)
                    box_face.alignment = 'CENTER'

                    # Head_Stretch
                    head_toon = box_face.row(align=1)
                    head_toon.scale_x = 4
                    head_toon.scale_y = 0.5
                    head_toon.alignment = 'CENTER'
                    head_toon.operator("operator.head_stretch", text="")

                    # Head Top Ctrl
                    head_toon = box_face.row()
                    head_toon.scale_x = 5
                    head_toon.scale_y = 0.5
                    head_toon.alignment = 'CENTER'
                    head_toon.operator("operator.head_top_ctrl", text="")
                    box_face.separator()
                    box_face.separator()

                    # Brows
                    brows = box_face.row()
                    brows.scale_x = 0.75
                    brows.scale_y = 0.75
                    brows.alignment = 'CENTER'

                    brow_R = brows.column()
                    brow_R.scale_x = 1.2
                    brow_R.scale_y = 0.75
                    brow_R.alignment = 'CENTER'

                    brow_mid = brows.column()
                    brow_mid.scale_x = 0.5
                    brow_mid.scale_y = 0.75
                    brow_mid.alignment = 'CENTER'

                    brow_L = brows.column()
                    brow_L.scale_x = 1.2
                    brow_L.scale_y = 0.75
                    brow_L.alignment = 'CENTER'

                    # Brow Ctrls R
                    brow_ctrls_R = brow_R.row(align=1)
                    brow_ctrls_R.scale_x = 1
                    brow_ctrls_R.scale_y = 0.5
                    brow_ctrls_R.alignment = 'CENTER'
                    brow_ctrls_R.operator("operator.brow_ctrl_4_r", text="", icon='DOT', emboss=0)
                    brow_ctrls_R.operator("operator.brow_ctrl_3_r", text="", icon='DOT', emboss=0)
                    brow_ctrls_R.operator("operator.brow_ctrl_2_r", text="", icon='DOT', emboss=0)
                    brow_ctrls_R.operator("operator.brow_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Brow Ctrl R
                    brow_ctrl_R = brow_R.row()
                    brow_ctrl_R.scale_x = 1
                    brow_ctrl_R.scale_y = 0.8
                    brow_ctrl_R.alignment = 'CENTER'
                    brow_ctrl_R.operator("operator.brow_ctrl_r", text="Brow R")

                    # Brow Toon R
                    brow_toon_R = brow_R.row()
                    brow_toon_R.scale_x = 2
                    brow_toon_R.scale_y = 0.5
                    brow_toon_R.alignment = 'CENTER'
                    brow_toon_R.operator("operator.toon_brow_r", text="", icon='KEYFRAME_HLT', emboss=0)

                    # Brow Frown
                    brow_frown = brow_mid.column()
                    brow_frown.scale_x = 2
                    brow_frown.scale_y = 0.5
                    brow_frown.alignment = 'CENTER'
                    brow_frown.operator("operator.frown_ctrl", text="", icon='DOT', emboss=0)
                    brow_frown.separator()
                    brow_frown.operator("operator.nose_bridge_1_ctrl", text="")

                    # Brow Ctrls R
                    brow_ctrls_L = brow_L.row(align=1)
                    brow_ctrls_L.scale_x = 1
                    brow_ctrls_L.scale_y = 0.5
                    brow_ctrls_L.alignment = 'CENTER'
                    brow_ctrls_L.operator("operator.brow_ctrl_1_l", text="", icon='DOT', emboss=0)
                    brow_ctrls_L.operator("operator.brow_ctrl_2_l", text="", icon='DOT', emboss=0)
                    brow_ctrls_L.operator("operator.brow_ctrl_3_l", text="", icon='DOT', emboss=0)
                    brow_ctrls_L.operator("operator.brow_ctrl_4_l", text="", icon='DOT', emboss=0)

                    # Brow Ctrl R
                    brow_ctrl_L = brow_L.row()
                    brow_ctrl_L.scale_x = 1
                    brow_ctrl_L.scale_y = 0.8
                    brow_ctrl_L.alignment = 'CENTER'
                    brow_ctrl_L.operator("operator.brow_ctrl_l", text="Brow L")

                    # Brow Toon R
                    brow_toon_L = brow_L.row()
                    brow_toon_L.scale_x = 2
                    brow_toon_L.scale_y = 0.5
                    brow_toon_L.alignment = 'CENTER'
                    brow_toon_L.operator("operator.toon_brow_l", text="", icon='KEYFRAME_HLT', emboss=0)
                    box_face.separator()

                    col_space = box_face.column()
                    col_space.scale_y = 2
                    col_space.separator()

                    # Eyes
                    eyes = box_face.row()
                    eyes.scale_x = 1
                    eyes.scale_y = 0.75
                    eyes.alignment = 'CENTER'

                    col_R = eyes.column()
                    col_R.scale_x = 1
                    col_R.scale_y = 0.75
                    col_R.alignment = 'CENTER'

                    col_mid = eyes.column()
                    col_mid.scale_x = 1
                    col_mid.scale_y = 0.75
                    col_mid.alignment = 'CENTER'

                    col_L = eyes.column()
                    col_L.scale_x = 1
                    col_L.scale_y = 0.75
                    col_L.alignment = 'CENTER'

                    # Eyelid Up Ctrl R
                    eyelid_up_R = col_R.row()
                    eyelid_up_R.scale_x = 1
                    eyelid_up_R.scale_y = 0.8
                    eyelid_up_R.alignment = 'CENTER'
                    eyelid_up_R.operator("operator.eyelid_up_ctrl_r", text="Eyelid up R")

                    # Eyelid Up Ctrls R
                    eyelid_up_ctrls_R = col_R.row()
                    eyelid_up_ctrls_R.scale_x = 1.2
                    eyelid_up_ctrls_R.scale_y = 0.5
                    eyelid_up_ctrls_R.alignment = 'CENTER'
                    eyelid_up_ctrls_R.operator("operator.eyelid_up_ctrl_3_r", text="", icon='DOT', emboss=0)
                    eyelid_up_ctrls_R.operator("operator.eyelid_up_ctrl_2_r", text="", icon='DOT', emboss=0)
                    eyelid_up_ctrls_R.operator("operator.eyelid_up_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Eye_R
                    eye_R_row_1 = col_R.row()
                    eye_R_row_1.scale_x = 0.8
                    eye_R_row_1.scale_y = 1
                    eye_R_row_1.alignment = 'CENTER'
                    eye_R_row_1.operator("operator.toon_eye_up_r", text="", icon='KEYFRAME_HLT', emboss=0)

                    eye_R_row_2 = col_R.row()
                    eye_R_row_2.scale_x = 0.5
                    eye_R_row_2.scale_y = 1
                    eye_R_row_2.alignment = 'CENTER'
                    eye_R_row_2.operator("operator.toon_eye_out_r", text="", icon='KEYFRAME_HLT', emboss=0)

                    eye_R_box = eye_R_row_2.box()
                    eye_R_box.scale_x = 1.2
                    eye_R_box.scale_y = 1
                    eye_R_box.alignment = 'CENTER'
                    eye_R = eye_R_box.row()
                    eye_R.operator("operator.pupil_ctrl_r", text="", icon='RADIOBUT_ON', emboss=0)
                    eye_R.operator("operator.eye_ctrl_r", text="", icon='HIDE_OFF', emboss=0)
                    eye_R.operator("operator.iris_ctrl_r", text="", icon='PROP_ON', emboss=0)
                    eye_R_row_2.operator("operator.toon_eye_in_r", text="", icon='KEYFRAME_HLT', emboss=0)

                    eye_R_row_3 = col_R.row()
                    eye_R_row_3.scale_x = 0.8
                    eye_R_row_3.scale_y = 1
                    eye_R_row_3.alignment = 'CENTER'
                    eye_R_row_3.operator("operator.toon_eye_low_r", text="", icon='KEYFRAME_HLT', emboss=0)

                    # Eyelid Low Ctrls R
                    eyelid_low_ctrls_R = col_R.row()
                    eyelid_low_ctrls_R.scale_x = 0.8
                    eyelid_low_ctrls_R.scale_y = 0.5
                    eyelid_low_ctrls_R.alignment = 'CENTER'
                    eyelid_low_ctrls_R.operator("operator.eyelid_ctrl_out_r", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_R.operator("operator.eyelid_low_ctrl_3_r", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_R.operator("operator.eyelid_low_ctrl_2_r", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_R.operator("operator.eyelid_low_ctrl_1_r", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_R.operator("operator.eyelid_ctrl_in_r", text="", icon='DOT', emboss=0)

                    # Eyelid Low Ctrl R
                    eyelid_low_R = col_R.row()
                    eyelid_low_R.scale_x = 1
                    eyelid_low_R.scale_y = 0.8
                    eyelid_low_R.alignment = 'CENTER'
                    eyelid_low_R.operator("operator.eyelid_low_ctrl_r", text="Eyelid low R")

                    # Nose Bridge
                    nose_bridge = col_mid.column()
                    nose_bridge.scale_x = 0.5
                    nose_bridge.scale_y = 1
                    nose_bridge.separator()
                    nose_bridge.separator()
                    nose_bridge.separator()
                    nose_bridge.separator()
                    nose_bridge.separator()
                    nose_bridge.alignment = 'CENTER'
                    nose_bridge.operator("operator.nose_bridge_2_ctrl", text="")

                    # Nose Frown
                    nose_frown = nose_bridge.row()
                    nose_frown.operator("operator.nose_frown_ctrl_r", text="", icon='PMARKER', emboss=0)
                    nose_frown.operator("operator.nose_frown_ctrl_l", text="", icon='PMARKER', emboss=0)

                    # Eyelid Up Ctrl L
                    eyelid_up_L = col_L.row()
                    eyelid_up_L.scale_x = 1
                    eyelid_up_L.scale_y = 0.8
                    eyelid_up_L.alignment = 'CENTER'
                    eyelid_up_L.operator("operator.eyelid_up_ctrl_l", text="Eyelid up L")

                    # Eyelid Up Ctrls L
                    eyelid_up_ctrls_L = col_L.row()
                    eyelid_up_ctrls_L.scale_x = 1.2
                    eyelid_up_ctrls_L.scale_y = 0.5
                    eyelid_up_ctrls_L.alignment = 'CENTER'
                    eyelid_up_ctrls_L.operator("operator.eyelid_up_ctrl_1_l", text="", icon='DOT', emboss=0)
                    eyelid_up_ctrls_L.operator("operator.eyelid_up_ctrl_2_l", text="", icon='DOT', emboss=0)
                    eyelid_up_ctrls_L.operator("operator.eyelid_up_ctrl_3_l", text="", icon='DOT', emboss=0)

                    # Eye_L
                    eye_L_row_1 = col_L.row()
                    eye_L_row_1.scale_x = 0.8
                    eye_L_row_1.scale_y = 1
                    eye_L_row_1.alignment = 'CENTER'
                    eye_L_row_1.operator("operator.toon_eye_up_l", text="", icon='KEYFRAME_HLT', emboss=0)

                    eye_L_row_2 = col_L.row()
                    eye_L_row_2.scale_x = 0.5
                    eye_L_row_2.scale_y = 1
                    eye_L_row_2.alignment = 'CENTER'
                    eye_L_row_2.operator("operator.toon_eye_in_l", text="", icon='KEYFRAME_HLT', emboss=0)

                    eye_L_box = eye_L_row_2.box()
                    eye_L_box.scale_x = 1.2
                    eye_L_box.scale_y = 1
                    eye_L_box.alignment = 'CENTER'
                    eye_L = eye_L_box.row()
                    eye_L.operator("operator.iris_ctrl_l", text="", icon='PROP_ON', emboss=0)
                    eye_L.operator("operator.eye_ctrl_l", text="", icon='HIDE_OFF', emboss=0)
                    eye_L.operator("operator.pupil_ctrl_l", text="", icon='RADIOBUT_ON', emboss=0)
                    eye_L_row_2.operator("operator.toon_eye_out_l", text="", icon='KEYFRAME_HLT', emboss=0)

                    eye_L_row_3 = col_L.row()
                    eye_L_row_3.scale_x = 0.8
                    eye_L_row_3.scale_y = 1
                    eye_L_row_3.alignment = 'CENTER'
                    eye_L_row_3.operator("operator.toon_eye_low_l", text="", icon='KEYFRAME_HLT', emboss=0)

                    # Eyelid Low Ctrls L
                    eyelid_low_ctrls_L = col_L.row()
                    eyelid_low_ctrls_L.scale_x = 0.8
                    eyelid_low_ctrls_L.scale_y = 0.5
                    eyelid_low_ctrls_L.alignment = 'CENTER'
                    eyelid_low_ctrls_L.operator("operator.eyelid_ctrl_in_l", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_L.operator("operator.eyelid_low_ctrl_1_l", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_L.operator("operator.eyelid_low_ctrl_2_l", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_L.operator("operator.eyelid_low_ctrl_3_l", text="", icon='DOT', emboss=0)
                    eyelid_low_ctrls_L.operator("operator.eyelid_ctrl_out_l", text="", icon='DOT', emboss=0)

                    # Eyelid Low Ctrl L
                    eyelid_low_L = col_L.row()
                    eyelid_low_L.scale_x = 1
                    eyelid_low_L.scale_y = 0.8
                    eyelid_low_L.alignment = 'CENTER'
                    eyelid_low_L.operator("operator.eyelid_low_ctrl_l", text="Eyelid low L")

                    box_face.separator()

                    col_space = box_face.column()
                    col_space.scale_y = 4
                    col_space.separator()

                    # Head Top Stretch
                    head_mid_str = box_face.column(align=1)
                    head_mid_row = head_mid_str.row(align=1)
                    head_mid_row.scale_x = 9
                    head_mid_row.scale_y = 0.3
                    head_mid_row.alignment = 'CENTER'
                    head_mid_row.operator("operator.head_mid_stretch", text="")

                    # Head Stretch Ctrls
                    head_str_ctrls = box_face.column(align=1)
                    head_str_ctrls.scale_x = 0.8
                    head_str_ctrls.scale_y = 0.3
                    head_str_ctrls.alignment = 'CENTER'
                    head_str_ctrls.operator("operator.head_mid_ctrl", text="")
                    head_str_ctrls.operator("operator.head_mid_curve", text="")

                    # Head Low Stretch
                    head_low_str = box_face.column(align=1)
                    head_low_row = head_low_str.row(align=1)
                    head_low_row.scale_x = 9
                    head_low_row.scale_y = 0.3
                    head_low_row.alignment = 'CENTER'
                    head_low_row.operator("operator.head_low_stretch", text="")

                    # Cheeks
                    cheeks = box_face.row()
                    cheeks.scale_x = 1
                    cheeks.scale_y = 0.75
                    cheeks.alignment = 'CENTER'

                    col_R = cheeks.column()
                    col_R.scale_x = 1
                    col_R.scale_y = 0.75
                    col_R.alignment = 'CENTER'

                    col_mid = cheeks.column()
                    col_mid.scale_x = 0.5
                    col_mid.scale_y = 0.75
                    col_mid.alignment = 'CENTER'

                    col_L = cheeks.column()
                    col_L.scale_x = 1
                    col_L.scale_y = 0.75
                    col_L.alignment = 'CENTER'

                    # Cheek Ctrl R
                    cheek_ctrl_R = col_R.row()
                    cheek_ctrl_R.scale_x = 1.5
                    cheek_ctrl_R.scale_y = 0.8
                    cheek_ctrl_R.alignment = 'CENTER'
                    cheek_ctrl_R.operator("operator.cheek_ctrl_r", text="Cheek R")

                    # Cheek Ctrls R
                    cheek_ctrls_R = col_R.row()
                    cheek_ctrls_R.scale_x = 1.5
                    cheek_ctrls_R.scale_y = 0.5
                    cheek_ctrls_R.alignment = 'CENTER'
                    cheek_ctrls_R.operator("operator.cheek_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_R.operator("operator.cheek_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_R.operator("operator.cheek_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Cheek Ctrls 2 R
                    col_R.separator()
                    cheek_ctrls_2_R = col_R.row()
                    cheek_ctrls_2_R.scale_x = 1.5
                    cheek_ctrls_2_R.scale_y = 0.5
                    cheek_ctrls_2_R.alignment = 'CENTER'
                    cheek_ctrls_2_R.operator("operator.cheek2_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_R.operator("operator.cheek2_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_R.operator("operator.cheek2_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Cheek Ctrls 3 R
                    col_R.separator()
                    cheek_ctrls_3_R = col_R.row()
                    cheek_ctrls_3_R.scale_x = 1.5
                    cheek_ctrls_3_R.scale_y = 0.5
                    cheek_ctrls_3_R.alignment = 'CENTER'
                    cheek_ctrls_3_R.operator("operator.lip_up3_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_R.operator("operator.lip_up3_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_R.operator("operator.lip_up3_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Cheek Ctrls 4 R
                    col_R.separator()
                    cheek_ctrls_4_R = col_R.row()
                    cheek_ctrls_4_R.scale_x = 1.5
                    cheek_ctrls_4_R.scale_y = 0.5
                    cheek_ctrls_4_R.alignment = 'CENTER'
                    cheek_ctrls_4_R.operator("operator.lip_up2_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_4_R.operator("operator.lip_up2_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_4_R.operator("operator.lip_up2_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Nose
                    col_mid.separator()
                    col_mid.separator()
                    col_mid.separator()
                    nose = col_mid.row(align=1)
                    nose.scale_x = 1.2
                    nose.scale_y = 0.8
                    nose.alignment = 'CENTER'
                    nose.operator("operator.nostril_ctrl_r", text="", icon='DOT', emboss=0)
                    nose.operator("operator.nose_ctrl", text="")
                    nose.operator("operator.nostril_ctrl_l", text="", icon='DOT', emboss=0)

                    # Lip Up Ctrls
                    col_mid.separator()
                    lip_up_ctrls = col_mid.column()
                    lip_up_ctrls.scale_x = 0.25
                    lip_up_ctrls.scale_y = 0.5
                    lip_up_ctrls.operator("operator.lip_up3_ctrl_mid", text="", icon='DOT', emboss=0)

                    lip_up_3_ctrl = col_mid.column()
                    lip_up_3_ctrl.scale_x = 0.25
                    lip_up_3_ctrl.scale_y = 0.3
                    lip_up_3_ctrl.operator("operator.lip_up3_ctrl", text="")

                    lip_up_2_ctrl = col_mid.column()
                    lip_up_2_ctrl.scale_x = 0.25
                    lip_up_2_ctrl.scale_y = 0.3
                    lip_up_2_ctrl.operator("operator.lip_up2_ctrl_mid", text="", icon='DOT', emboss=0)
                    lip_up_2_ctrl.operator("operator.lip_up2_ctrl", text="")

                    # Cheek Ctrl L
                    cheek_ctrl_L = col_L.row()
                    cheek_ctrl_L.scale_x = 1.5
                    cheek_ctrl_L.scale_y = 0.8
                    cheek_ctrl_L.alignment = 'CENTER'
                    cheek_ctrl_L.operator("operator.cheek_ctrl_l", text="Cheek L")

                    # Cheek Ctrls L
                    cheek_ctrls_L = col_L.row()
                    cheek_ctrls_L.scale_x = 1.5
                    cheek_ctrls_L.scale_y = 0.5
                    cheek_ctrls_L.alignment = 'CENTER'
                    cheek_ctrls_L.operator("operator.cheek_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_L.operator("operator.cheek_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_L.operator("operator.cheek_ctrl_3_l", text="", icon='DOT', emboss=0)

                    # Cheek Ctrls 2 L
                    col_L.separator()
                    cheek_ctrls_2_L = col_L.row()
                    cheek_ctrls_2_L.scale_x = 1.5
                    cheek_ctrls_2_L.scale_y = 0.5
                    cheek_ctrls_2_L.alignment = 'CENTER'
                    cheek_ctrls_2_L.operator("operator.cheek2_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_L.operator("operator.cheek2_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_L.operator("operator.cheek2_ctrl_3_l", text="", icon='DOT', emboss=0)

                    # Cheek Ctrls 3 L
                    col_L.separator()
                    cheek_ctrls_3_L = col_L.row()
                    cheek_ctrls_3_L.scale_x = 1.5
                    cheek_ctrls_3_L.scale_y = 0.5
                    cheek_ctrls_3_L.alignment = 'CENTER'
                    cheek_ctrls_3_L.operator("operator.lip_up3_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_L.operator("operator.lip_up3_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_L.operator("operator.lip_up3_ctrl_3_l", text="", icon='DOT', emboss=0)

                    # Cheek Ctrls 4 L
                    col_L.separator()
                    cheek_ctrls_4_L = col_L.row()
                    cheek_ctrls_4_L.scale_x = 1.5
                    cheek_ctrls_4_L.scale_y = 0.5
                    cheek_ctrls_4_L.alignment = 'CENTER'
                    cheek_ctrls_4_L.operator("operator.lip_up2_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_4_L.operator("operator.lip_up2_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_4_L.operator("operator.lip_up2_ctrl_3_l", text="", icon='DOT', emboss=0)

                    col_space = box_face.column()
                    col_space.scale_y = 4
                    col_space.separator()

                    # Mouth
                    mouth = box_face.row()
                    mouth.scale_x = 1
                    mouth.scale_y = 1
                    mouth.alignment = 'CENTER'

                    col_R = mouth.column()
                    col_R.scale_x = 0.5
                    col_R.scale_y = 1
                    col_R.alignment = 'CENTER'

                    col_mid = mouth.column(align=1)
                    col_mid.scale_x = 1
                    col_mid.scale_y = 1
                    col_mid.alignment = 'CENTER'

                    col_L = mouth.column()
                    col_L.scale_x = 0.5
                    col_L.scale_y = 1
                    col_L.alignment = 'CENTER'

                    # Lip Mid Ctrls R
                    col_R.separator()
                    col_R.separator()
                    col_R.separator()
                    col_R.separator()
                    col_R.separator()
                    col_R.separator()
                    col_R.separator()
                    lip_mid_ctrls_R = col_R.row()
                    lip_mid_ctrls_R.scale_x = 1.5
                    lip_mid_ctrls_R.scale_y = 0.5
                    lip_mid_ctrls_R.alignment = 'CENTER'
                    lip_mid_ctrls_R.operator("operator.cheek_ctrl_4_r", text="", icon='DOT', emboss=0)
                    lip_mid_ctrls_R.operator("operator.cheek2_ctrl_4_r", text="", icon='DOT', emboss=0)
                    lip_mid_ctrls_R.operator("operator.lip_up3_ctrl_4_r", text="", icon='DOT', emboss=0)
                    lip_mid_ctrls_R.operator("operator.lip_up2_ctrl_4_r", text="", icon='DOT', emboss=0)

                    # Mouth Ctrls

                    # Mouth Mstr Up
                    mouth_mstr_up = col_mid.column(align=1)
                    mouth_mstr_up.scale_x = 1
                    mouth_mstr_up.scale_y = 0.5
                    mouth_mstr_up.alignment = 'CENTER'
                    mouth_mstr_up.operator("operator.mouth_mstr_up", text="")

                    mouth_box = col_mid.box()
                    mouth_box.scale_x = 1
                    mouth_box.scale_y = 1
                    mouth_box.alignment = 'CENTER'

                    mouth_row = mouth_box.row(align=1)
                    mouth_row.scale_x = 1
                    mouth_row.scale_y = 1
                    mouth_row.alignment = 'CENTER'

                    mouth_col_R = mouth_row.column()
                    mouth_col_R.scale_x = 1
                    mouth_col_R.scale_y = 1
                    mouth_col_R.alignment = 'CENTER'

                    mouth_col_mid = mouth_row.column()
                    mouth_col_mid.scale_x = 3
                    mouth_col_mid.scale_y = 1
                    mouth_col_mid.alignment = 'CENTER'

                    mouth_col_L = mouth_row.column()
                    mouth_col_L.scale_x = 1
                    mouth_col_L.scale_y = 1
                    mouth_col_L.alignment = 'CENTER'

                    # Mouth Corner R
                    mouth_col_R.separator()
                    mouth_col_R.separator()
                    mouth_col_R.separator()
                    mouth_col_R.separator()
                    corner_R = mouth_col_R.column()
                    corner_R.scale_x = 0.5
                    corner_R.scale_y = 1
                    corner_R.alignment = 'CENTER'
                    corner_R.operator("operator.mouth_corner_r", text="")

                    # Lips Ctrls
                    lip_up = mouth_col_mid.column(align=1)
                    lip_up.scale_x = 1
                    lip_up.scale_y = 0.4
                    lip_up.alignment = 'CENTER'
                    lip_up.operator("operator.lip_up_ctrl", text="")
                    lip_up.operator("operator.lip_up_ctrl_collision", text="")

                    # Lip Up Ctrls
                    lip_up_col = mouth_col_mid.column()
                    lip_up_col.scale_x = 0.3
                    lip_up_col.scale_y = 0.4
                    lip_up_col.alignment = 'CENTER'
                    lip_up_ctrls = lip_up_col.row()
                    lip_up_ctrls.scale_x = 0.3
                    lip_up_ctrls.scale_y = 0.4
                    lip_up_ctrls.alignment = 'CENTER'
                    lip_up_ctrls.operator("operator.lip_up_ctrl_3_r", text="", icon='DOT', emboss=0)
                    lip_up_ctrls.operator("operator.lip_up_ctrl_2_r", text="", icon='DOT', emboss=0)
                    lip_up_ctrls.operator("operator.lip_up_ctrl_1_r", text="", icon='DOT', emboss=0)
                    lip_up_ctrls.operator("operator.lip_up_ctrl_mid", text="", icon='DOT', emboss=0)
                    lip_up_ctrls.operator("operator.lip_up_ctrl_1_l", text="", icon='DOT', emboss=0)
                    lip_up_ctrls.operator("operator.lip_up_ctrl_2_l", text="", icon='DOT', emboss=0)
                    lip_up_ctrls.operator("operator.lip_up_ctrl_3_l", text="", icon='DOT', emboss=0)
                    lip_up_col.separator()

                    # Mouth Ctrl
                    mouth_ctrl_col = mouth_col_mid.column()
                    mouth_ctrl_col.scale_x = 0.3
                    mouth_ctrl_col.scale_y = .8
                    mouth_ctrl_col.alignment = 'CENTER'

                    mouth_up_ctrl = mouth_ctrl_col.row()
                    mouth_up_ctrl.scale_x = 1.5
                    mouth_up_ctrl.scale_y = 0.4
                    mouth_up_ctrl.alignment = 'CENTER'
                    mouth_up_ctrl.operator("operator.mouth_up_ctrl", text="")

                    mouth_ctrl_col_2 = mouth_ctrl_col.column(align=1)
                    mouth_ctrl_row = mouth_ctrl_col_2.row(align=1)
                    mouth_ctrl_row_1 = mouth_ctrl_row.row(align=1)
                    mouth_ctrl_row_1.scale_x = 0.5
                    mouth_ctrl_row_1.scale_y = 1
                    mouth_ctrl_row_1.alignment = 'CENTER'
                    mouth_ctrl_row_1.operator("operator.lip_up_ctrl_4_r", text="", icon='DOT', emboss=0)

                    mouth_ctrl_row_2 = mouth_ctrl_row.row(align=1)
                    mouth_ctrl_row_2.scale_x = 1
                    mouth_ctrl_row_2.scale_y = 1
                    mouth_ctrl_row_2.alignment = 'CENTER'
                    mouth_ctrl_row_2.operator("operator.mouth_ctrl", text="Mouth ctrl")

                    mouth_ctrl_row_3 = mouth_ctrl_row.row(align=1)
                    mouth_ctrl_row_3.scale_x = 0.5
                    mouth_ctrl_row_3.scale_y = 1
                    mouth_ctrl_row_3.alignment = 'CENTER'
                    mouth_ctrl_row_3.operator("operator.lip_up_ctrl_4_l", text="", icon='DOT', emboss=0)

                    mouth_low_ctrl = mouth_ctrl_col.row()
                    mouth_low_ctrl.scale_x = 1.5
                    mouth_low_ctrl.scale_y = 0.4
                    mouth_low_ctrl.alignment = 'CENTER'
                    mouth_low_ctrl.operator("operator.mouth_low_ctrl", text="")

                    # Lip Low Ctrls
                    lip_low_col = mouth_col_mid.column()
                    lip_low_col.scale_x = 0.3
                    lip_low_col.scale_y = 1
                    lip_low_col.alignment = 'CENTER'
                    lip_low_ctrls = lip_low_col.row()
                    lip_low_ctrls.scale_x = 0.3
                    lip_low_ctrls.scale_y = 0.5
                    lip_low_ctrls.alignment = 'CENTER'
                    lip_low_ctrls.operator("operator.lip_low_ctrl_3_r", text="", icon='DOT', emboss=0)
                    lip_low_ctrls.operator("operator.lip_low_ctrl_2_r", text="", icon='DOT', emboss=0)
                    lip_low_ctrls.operator("operator.lip_low_ctrl_1_r", text="", icon='DOT', emboss=0)
                    lip_low_ctrls.operator("operator.lip_low_ctrl_mid", text="", icon='DOT', emboss=0)
                    lip_low_ctrls.operator("operator.lip_low_ctrl_1_l", text="", icon='DOT', emboss=0)
                    lip_low_ctrls.operator("operator.lip_low_ctrl_2_l", text="", icon='DOT', emboss=0)
                    lip_low_ctrls.operator("operator.lip_low_ctrl_3_l", text="", icon='DOT', emboss=0)

                    mouth_mstr_low = mouth_col_mid.column(align=1)
                    mouth_mstr_low.scale_x = 1
                    mouth_mstr_low.scale_y = 0.4
                    mouth_mstr_low.alignment = 'CENTER'
                    mouth_mstr_low.operator("operator.lip_low_ctrl_collision", text="")
                    mouth_mstr_low.operator("operator.lip_low_ctrl", text="")

                    # Mouth Mstr Low
                    mouth_mstr_low = col_mid.column(align=1)
                    mouth_mstr_low.scale_x = 1
                    mouth_mstr_low.scale_y = 0.5
                    mouth_mstr_low.alignment = 'CENTER'
                    mouth_mstr_low.operator("operator.mouth_mstr_low", text="")

                    # Mouth Mstr Ctrl
                    mouth_mstr_ctrl = col_mid.column(align=1)
                    mouth_mstr_ctrl.scale_x = 1
                    mouth_mstr_ctrl.scale_y = 0.8
                    mouth_mstr_ctrl.alignment = 'CENTER'
                    mouth_mstr_ctrl.operator("operator.mouth_mstr_ctrl", text="Mouth mstr ctrl")

                    # Mouth Corner L
                    mouth_col_L.separator()
                    mouth_col_L.separator()
                    mouth_col_L.separator()
                    mouth_col_L.separator()
                    corner_L = mouth_col_L.column()
                    corner_L.scale_x = 0.5
                    corner_L.scale_y = 1
                    corner_L.alignment = 'CENTER'
                    corner_L.operator("operator.mouth_corner_l", text="")

                    # Lip Mid Ctrls L
                    col_L.separator()
                    col_L.separator()
                    col_L.separator()
                    col_L.separator()
                    col_L.separator()
                    col_L.separator()
                    col_L.separator()
                    lip_mid_ctrls_L = col_L.row()
                    lip_mid_ctrls_L.scale_x = 1.5
                    lip_mid_ctrls_L.scale_y = 0.5
                    lip_mid_ctrls_L.alignment = 'CENTER'
                    lip_mid_ctrls_L.operator("operator.lip_up2_ctrl_4_l", text="", icon='DOT', emboss=0)
                    lip_mid_ctrls_L.operator("operator.lip_up3_ctrl_4_l", text="", icon='DOT', emboss=0)
                    lip_mid_ctrls_L.operator("operator.cheek2_ctrl_4_l", text="", icon='DOT', emboss=0)
                    lip_mid_ctrls_L.operator("operator.cheek_ctrl_4_l", text="", icon='DOT', emboss=0)

                    # Jaw
                    jaw = box_face.row()
                    jaw.scale_x = 0.8
                    jaw.scale_y = 0.75
                    jaw.alignment = 'CENTER'

                    col_R = jaw.column()
                    col_R.scale_x = 1
                    col_R.scale_y = 0.75
                    col_R.alignment = 'CENTER'

                    col_mid = jaw.column()
                    col_mid.scale_x = 1
                    col_mid.scale_y = 0.75
                    col_mid.alignment = 'CENTER'

                    col_L = jaw.column()
                    col_L.scale_x = 1
                    col_L.scale_y = 0.75
                    col_L.alignment = 'CENTER'

                    # Mouth Frown R
                    cheek_ctrl_R = col_R.row()
                    cheek_ctrl_R.scale_x = 1.5
                    cheek_ctrl_R.scale_y = 1
                    cheek_ctrl_R.alignment = 'CENTER'
                    cheek_ctrl_R.operator("operator.mouth_frown_ctrl_r", text="", icon='PMARKER', emboss=0)

                    # Jaw Ctrls R
                    cheek_ctrls_R = col_R.row()
                    cheek_ctrls_R.scale_x = 1.5
                    cheek_ctrls_R.scale_y = 0.5
                    cheek_ctrls_R.alignment = 'CENTER'
                    cheek_ctrls_R.operator("operator.lip_low2_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_R.operator("operator.lip_low2_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_R.operator("operator.lip_low2_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Jaw Ctrls 2 R
                    col_R.separator()
                    cheek_ctrls_2_R = col_R.row()
                    cheek_ctrls_2_R.scale_x = 1.5
                    cheek_ctrls_2_R.scale_y = 0.5
                    cheek_ctrls_2_R.alignment = 'CENTER'
                    cheek_ctrls_2_R.operator("operator.lip_low3_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_R.operator("operator.lip_low3_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_R.operator("operator.lip_low3_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Jaw Ctrls 3 R
                    col_R.separator()
                    cheek_ctrls_3_R = col_R.row()
                    cheek_ctrls_3_R.scale_x = 1
                    cheek_ctrls_3_R.scale_y = 0.5
                    cheek_ctrls_3_R.alignment = 'CENTER'
                    cheek_ctrls_3_R.operator("operator.cheek_ctrl_5_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_R.operator("operator.chin_ctrl_3_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_R.operator("operator.chin_ctrl_2_r", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_R.operator("operator.chin_ctrl_1_r", text="", icon='DOT', emboss=0)

                    # Lip Low Ctrls
                    col_mid.separator()
                    col_mid.separator()
                    lip_low_ctrls = col_mid.column()
                    lip_low_ctrls.scale_x = 0.25
                    lip_low_ctrls.scale_y = 1
                    lip_low_ctrls.operator("operator.lip_low2_ctrl_mid", text="", icon='DOT', emboss=0)

                    lip_low_2_ctrl = col_mid.column()
                    lip_low_2_ctrl.scale_x = 0.25
                    lip_low_2_ctrl.scale_y = 0.3
                    lip_low_2_ctrl.operator("operator.lip_low2_ctrl", text="")

                    lip_low_3_ctrl = col_mid.column()
                    lip_low_3_ctrl.scale_x = 0.25
                    lip_low_3_ctrl.scale_y = 0.3
                    lip_low_3_ctrl.operator("operator.lip_low3_ctrl_mid", text="", icon='DOT', emboss=0)
                    lip_low_3_ctrl.operator("operator.lip_low3_ctrl", text="")
                    lip_low_3_ctrl.operator("operator.chin_ctrl_mid", text="", icon='DOT', emboss=0)

                    # Mouth Frown L
                    cheek_ctrl_L = col_L.row()
                    cheek_ctrl_L.scale_x = 1.5
                    cheek_ctrl_L.scale_y = 1
                    cheek_ctrl_L.alignment = 'CENTER'
                    cheek_ctrl_L.operator("operator.mouth_frown_ctrl_l", text="", icon='PMARKER', emboss=0)

                    # Jaw Ctrls L
                    cheek_ctrls_L = col_L.row()
                    cheek_ctrls_L.scale_x = 1.5
                    cheek_ctrls_L.scale_y = 0.5
                    cheek_ctrls_L.alignment = 'CENTER'
                    cheek_ctrls_L.operator("operator.lip_low2_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_L.operator("operator.lip_low2_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_L.operator("operator.lip_low2_ctrl_3_l", text="", icon='DOT', emboss=0)

                    # Jaw Ctrls 2 L
                    col_L.separator()
                    cheek_ctrls_2_L = col_L.row()
                    cheek_ctrls_2_L.scale_x = 1.5
                    cheek_ctrls_2_L.scale_y = 0.5
                    cheek_ctrls_2_L.alignment = 'CENTER'
                    cheek_ctrls_2_L.operator("operator.lip_low3_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_L.operator("operator.lip_low3_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_2_L.operator("operator.lip_low3_ctrl_3_l", text="", icon='DOT', emboss=0)

                    # Jaw Ctrls 3 L
                    col_L.separator()
                    cheek_ctrls_3_L = col_L.row()
                    cheek_ctrls_3_L.scale_x = 1
                    cheek_ctrls_3_L.scale_y = 0.5
                    cheek_ctrls_3_L.alignment = 'CENTER'
                    cheek_ctrls_3_L.operator("operator.chin_ctrl_1_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_L.operator("operator.chin_ctrl_2_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_L.operator("operator.chin_ctrl_3_l", text="", icon='DOT', emboss=0)
                    cheek_ctrls_3_L.operator("operator.cheek_ctrl_5_l", text="", icon='DOT', emboss=0)

                    col_space = box_face.column()
                    col_space.scale_y = 4
                    col_space.separator()

                    # Chin
                    jaw_row = box_face.row()
                    jaw_row.scale_x = 2
                    jaw_row.scale_y = 0.75
                    jaw_row.alignment = 'CENTER'

                    jaw_ctrls = jaw_row.column(align=1)
                    jaw_ctrls.scale_x = 1
                    jaw_ctrls.scale_y = 1
                    jaw_ctrls.alignment = 'CENTER'

                    chin = jaw_ctrls.row(align=1)
                    chin.scale_x = 1
                    chin.scale_y = 0.5
                    chin.alignment = 'CENTER'
                    chin.operator("operator.chin_ctrl", text="")

                    # Maxi
                    maxi = jaw_ctrls.column(align=1)
                    maxi.scale_x = 0.5
                    maxi.scale_y = 0.8
                    maxi.alignment = 'CENTER'
                    maxi.operator("operator.maxi", text="Maxi")

                    # Mouth Str
                    mouth_str = jaw_ctrls.row(align=1)
                    mouth_str.scale_x = 2
                    mouth_str.scale_y = 0.5
                    mouth_str.alignment = 'CENTER'
                    mouth_str.operator("operator.mouth_str_ctrl", text="")

                    # Left Column
                    left_col = face_row.column(align=1)
                    left_col.scale_x = 0.5
                    left_col.scale_y = 1
                    left_col.alignment = 'CENTER'

                    col_space = left_col.column()
                    col_space.scale_y = 15
                    col_space.separator()

                    # Ear Up L
                    ear_up_L = left_col.column()
                    ear_up_L.scale_x = 1
                    ear_up_L.scale_y = 0.5
                    ear_up_L.alignment = 'CENTER'
                    ear_up_L.operator("operator.ear_up_l", text="")

                    # Ear L
                    ear_L = left_col.column()
                    ear_L.scale_x = 1
                    ear_L.scale_y = 2
                    ear_L.alignment = 'CENTER'
                    ear_L.operator("operator.ear_l", text="")

                    # Ear Low L
                    ear_low_L = left_col.column()
                    ear_low_L.scale_x = 1
                    ear_low_L.scale_y = 0.5
                    ear_low_L.alignment = 'CENTER'
                    ear_low_L.operator("operator.ear_low_l", text="")

                    box_face.separator()
                    box_face.separator()

                    # Inner Mouth
                    inner_col = box.column(align=1)
                    inner_col.scale_x = 1
                    inner_col.scale_y = 1
                    inner_col.alignment = 'CENTER'
                    inner_col.label(text='Inner Mouth')
                    inner_col.separator()

                    inner_row = inner_col.row(align=1)
                    inner_row.scale_x = 1
                    inner_row.scale_y = 1
                    inner_row.alignment = 'CENTER'

                    # Teeth Column
                    teeth_col = inner_row.column(align=1)
                    teeth_col.scale_x = 1
                    teeth_col.scale_y = 1
                    teeth_col.alignment = 'CENTER'

                    # Teeth Up Ctrls
                    teeth_up_ctrls = teeth_col.row(align=1)
                    teeth_up_ctrls.scale_x = 0.6
                    teeth_up_ctrls.scale_y = 0.5
                    teeth_up_ctrls.alignment = 'CENTER'
                    teeth_up_ctrls.operator("operator.teeth_up_ctrl_r", text="")
                    teeth_up_ctrls.operator("operator.teeth_up_ctrl_mid_r", text="")
                    teeth_up_ctrls.operator("operator.teeth_up_ctrl_mid", text="")
                    teeth_up_ctrls.operator("operator.teeth_up_ctrl_mid_l", text="")
                    teeth_up_ctrls.operator("operator.teeth_up_ctrl_l", text="")

                    # Teeth Up
                    teeth_up = teeth_col.row()
                    teeth_up.scale_x = 1.2
                    teeth_up.scale_y = 0.8
                    teeth_up.alignment = 'CENTER'
                    teeth_up.operator("operator.teeth_up", text="Teeth up  ")

                    # Teeth Low
                    teeth_low = teeth_col.row()
                    teeth_low.scale_x = 1.2
                    teeth_low.scale_y = 0.8
                    teeth_low.alignment = 'CENTER'
                    teeth_low.operator("operator.teeth_low", text="Teeth low")

                    # Teeth Low Ctrls
                    teeth_low_ctrls = teeth_col.row(align=1)
                    teeth_low_ctrls.scale_x = 0.6
                    teeth_low_ctrls.scale_y = 0.5
                    teeth_low_ctrls.alignment = 'CENTER'
                    teeth_low_ctrls.operator("operator.teeth_low_ctrl_r", text="")
                    teeth_low_ctrls.operator("operator.teeth_low_ctrl_mid_r", text="")
                    teeth_low_ctrls.operator("operator.teeth_low_ctrl_mid", text="")
                    teeth_low_ctrls.operator("operator.teeth_low_ctrl_mid_l", text="")
                    teeth_low_ctrls.operator("operator.teeth_low_ctrl_l", text="")

                    inner_row.separator()
                    inner_row.separator()
                    inner_row.separator()
                    inner_row.separator()

                    # Tongue Column
                    tongue_col = inner_row.column(align=1)
                    tongue_col.scale_x = 1
                    tongue_col.scale_y = 1
                    tongue_col.alignment = 'CENTER'
                    tongue_col.separator()

                    tongue_row = tongue_col.row(align=1)
                    tongue_row.scale_x = 0.6
                    tongue_row.scale_y = 1
                    tongue_row.alignment = 'CENTER'

                    # Uvula
                    uvula = tongue_row.column(align=1)
                    uvula.scale_x = 0.5
                    uvula.scale_y = 1
                    uvula.alignment = 'CENTER'
                    uvula.operator("operator.uvula_1", text="")
                    uvula.operator("operator.uvula_2", text="")

                    # Tongue Ctrls
                    tongue_ctrl_col = tongue_row.column()
                    tongue_ctrl_col.scale_x = 1
                    tongue_ctrl_col.scale_y = 1
                    tongue_ctrl_col.alignment = 'CENTER'

                    teeth_low_ctrls = tongue_ctrl_col.row(align=1)
                    teeth_low_ctrls.scale_x = 1
                    teeth_low_ctrls.scale_y = 0.8
                    teeth_low_ctrls.alignment = 'CENTER'
                    teeth_low_ctrls.operator("operator.tongue_1_fk", text="FK")
                    teeth_low_ctrls.operator("operator.tongue_2_fk", text="FK")
                    teeth_low_ctrls.operator("operator.tongue_1_ik", text="IK")
                    teeth_low_ctrls.operator("operator.tongue_2_ik", text="IK")
                    teeth_low_ctrls.operator("operator.tongue_3_ik", text="IK")

                    # Tongue Mstr
                    tongue_mstr = tongue_ctrl_col.column()
                    tongue_mstr.operator("operator.tongue_mstr", text="Tongue mstr")

                    # View
                    box.separator()
                    row_view_main = box.row(align=0)
                    row_view_main.scale_x = 1
                    row_view_main.scale_y = 1
                    row_view_main.alignment = 'CENTER'

                    row_view = row_view_main.row(align=0)
                    row_view.scale_x = 1
                    row_view.scale_y = 1
                    row_view.alignment = 'CENTER'
                    row_view.operator("operator.zoom", text="Zoom to Selected", icon='ZOOM_IN')

                    row_model_res = row_view_main.row(align=0)
                    row_model_res.scale_x = 0.7
                    row_model_res.scale_y = 1
                    row_model_res.alignment = 'CENTER'
                    row_model_res.prop(arm_bones['properties'], '["model_res"]', text="Model Res", toggle=True)

                # collapsed box

                elif "gui_picker_face" in arm:
                    row.operator("gui.blenrig_6_tabs", icon="MOD_MASK", emboss=1).tab = "gui_picker_face"
                    row.label(text="FACE PICKER")

    # Extra Properties
            if context.mode == "POSE":

                if "gui_misc" in arm:
                    box = layout.column()
                    col = box.column()
                    row = col.row()
                # expanded box
                if "gui_misc" in arm and arm["gui_misc"]:
                    row.operator("gui.blenrig_6_tabs", icon="SETTINGS", emboss=1).tab = "gui_misc"
                    row.label(text="EXTRA PROPERTIES")

                    # Teeth - Follow Smile
                    box.prop(props, "gui_extra_props_face", text='Face')
                    if props.gui_extra_props_face:
                        head_col = box.box()
                        head_col.scale_x = 1
                        head_col.scale_y = 1
                        head_col.alignment = 'CENTER'
                        head_col.label(text='Teeth - Stretch along with the Smile')
                        teeth_row = head_col.row()
                        col_1 = teeth_row.column()
                        col_1.scale_x = 1
                        col_1.scale_y = 1
                        col_1.alignment = 'CENTER'
                        col_2 = teeth_row.column()
                        col_2.scale_x = 1
                        col_2.scale_y = 1
                        col_2.alignment = 'CENTER'
                        # Follow Mouth Orientation
                        col_1.prop(arm_bones['properties_head'], '["toon_teeth_up"]', text="Upper Teeth", slider=True)
                        col_2.prop(arm_bones['properties_head'], '["toon_teeth_low"]', text="Lower Teeth", slider=True)
                        head_col.label(text='Follow Mouth Orientation')
                        teeth_row = head_col.row()
                        col_1 = teeth_row.column()
                        col_1.scale_x = 1
                        col_1.scale_y = 1
                        col_1.alignment = 'CENTER'
                        col_2 = teeth_row.column()
                        col_2.scale_x = 1
                        col_2.scale_y = 1
                        col_2.alignment = 'CENTER'
                        try:
                            col_1.prop(
                                arm_bones['properties_head'],
                                '["teeth_up_follow_mouth"]', text="Upper Teeth", slider=True)
                            col_2.prop(
                                arm_bones['properties_head'],
                                '["teeth_low_follow_mouth"]', text="Lower Teeth", slider=True)
                            col_1.prop(
                                arm_bones['properties_head'],
                                '["tongue_follow_mouth"]', text="Tongue", slider=True)
                        except:
                            pass
                        head_col.separator()
                        # Arms
                    box.prop(props, "gui_extra_props_arms", text='Arms')
                    if props.gui_extra_props_arms:
                        arms_col = box.box()
                        arms_col.scale_x = 1
                        arms_col.scale_y = 1
                        arms_col.alignment = 'CENTER'
                        arms_col.label(text='Curved Arms')
                        arms_row = arms_col.row()
                        col_1 = arms_row.column()
                        col_1.scale_x = 1
                        col_1.scale_y = 1
                        col_1.alignment = 'CENTER'
                        col_2 = arms_row.column()
                        col_2.scale_x = 1
                        col_2.scale_y = 1
                        col_2.alignment = 'CENTER'
                        col_1.prop(arm_bones['properties_arm_R'], '["curved_arm_R"]', text="Curve_R", slider=True)
                        col_1.prop(arm_bones['properties_arm_R'], '["curved_arm_tweak_R"]', text="Tweak_R", slider=True)
                        col_2.prop(arm_bones['properties_arm_L'], '["curved_arm_L"]', text="Curve_L", slider=True)
                        col_2.prop(arm_bones['properties_arm_L'], '["curved_arm_tweak_L"]', text="Tweak_L", slider=True)
                        arms_col.separator()

                # Fingers
                    box.prop(props, "gui_extra_props_fingers", text='Fingers')
                    if props.gui_extra_props_fingers:

                        hands_col = box.box()
                        hands_col.scale_x = 1
                        hands_col.scale_y = 1
                        hands_col.alignment = 'CENTER'
                        hands_row = hands_col.row()
                        col_1 = hands_row.column()
                        col_1.scale_x = 1
                        col_1.scale_y = 1
                        col_1.alignment = 'CENTER'
                        col_3 = hands_row.column()
                        col_3.scale_x = 1
                        col_3.scale_y = 1
                        col_3.alignment = 'CENTER'
                        col_3.label(text='RIGHT FINGERS SPACE')
                        col_5 = hands_row.column()
                        col_5.scale_x = 1
                        col_5.scale_y = 1
                        col_5.alignment = 'CENTER'
                        col_5.label(text='LEFT FINGERS SPACE')
                        col_1.separator()
                        col_1.separator()
                        col_1.separator()
                        col_1.label(text='Thumb')
                        col_1.label(text='Index')
                        col_1.label(text='Middle')
                        col_1.label(text='Ring')
                        col_1.label(text='Little')
                        row_thumb = col_3.row(align=True)
                        row_thumb.alignment = 'CENTER'
                        row_thumb.scale_x = 2.5
                        row_thumb.scale_y = 1
                        row_thumb.operator(
                            "show.fing_thumb_list_r", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_R']['space_fing_thumb_R'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_thumb.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_R'], 'space_fing_thumb_R',
                                      toggle=True, icon_only=1, emboss=1)
                        row_ind = col_3.row(align=True)
                        row_ind.alignment = 'CENTER'
                        row_ind.scale_x = 2.5
                        row_ind.scale_y = 1
                        row_ind.operator(
                            "show.fing_ind_list_r", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_R']['space_fing_ind_R'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_ind.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_R'], 'space_fing_ind_R',
                                      toggle=True, icon_only=1, emboss=1)
                        row_mid = col_3.row(align=True)
                        row_mid.alignment = 'CENTER'
                        row_mid.scale_x = 2.5
                        row_mid.scale_y = 1
                        row_mid.operator(
                            "show.fing_mid_list_r", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_R']['space_fing_mid_R'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_mid.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_R'], 'space_fing_mid_R',
                                      toggle=True, icon_only=1, emboss=1)
                        row_ring = col_3.row(align=True)
                        row_ring.alignment = 'CENTER'
                        row_ring.scale_x = 2.5
                        row_ring.scale_y = 1
                        row_ring.operator(
                            "show.fing_ring_list_r", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_R']['space_fing_ring_R'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_ring.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_R'], 'space_fing_ring_R',
                                      toggle=True, icon_only=1, emboss=1)
                        row_lit = col_3.row(align=True)
                        row_lit.alignment = 'CENTER'
                        row_lit.scale_x = 2.5
                        row_lit.scale_y = 1
                        row_lit.operator(
                            "show.fing_lit_list_r", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_R']['space_fing_lit_R'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_lit.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_R'], 'space_fing_lit_R',
                                      toggle=True, icon_only=1, emboss=1)
                        row_thumb = col_5.row(align=True)
                        row_thumb.alignment = 'CENTER'
                        row_thumb.scale_x = 2.5
                        row_thumb.scale_y = 1
                        row_thumb.operator(
                            "show.fing_thumb_list_l", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_L']['space_fing_thumb_L'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_thumb.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_L'], 'space_fing_thumb_L',
                                      toggle=True, icon_only=1, emboss=1)
                        row_ind = col_5.row(align=True)
                        row_ind.alignment = 'CENTER'
                        row_ind.scale_x = 2.5
                        row_ind.scale_y = 1
                        row_ind.operator(
                            "show.fing_ind_list_l", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_L']['space_fing_ind_L'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_ind.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_L'], 'space_fing_ind_L',
                                      toggle=True, icon_only=1, emboss=1)
                        row_mid = col_5.row(align=True)
                        row_mid.alignment = 'CENTER'
                        row_mid.scale_x = 2.5
                        row_mid.scale_y = 1
                        row_mid.operator(
                            "show.fing_mid_list_l", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_L']['space_fing_mid_L'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_mid.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_L'], 'space_fing_mid_L',
                                      toggle=True, icon_only=1, emboss=1)
                        row_ring = col_5.row(align=True)
                        row_ring.alignment = 'CENTER'
                        row_ring.scale_x = 2.5
                        row_ring.scale_y = 1
                        row_ring.operator(
                            "show.fing_ring_list_l", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_L']['space_fing_ring_L'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_ring.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_L'], 'space_fing_ring_L',
                                      toggle=True, icon_only=1, emboss=1)
                        row_lit = col_5.row(align=True)
                        row_lit.alignment = 'CENTER'
                        row_lit.scale_x = 2.5
                        row_lit.scale_y = 1
                        row_lit.operator(
                            "show.fing_lit_list_l", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_L']['space_fing_lit_L'] == 0 else "Follow Hand"),
                            emboss=True)
                        col_prop = row_lit.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_L'], 'space_fing_lit_L',
                                      toggle=True, icon_only=1, emboss=1)

                        hands_col.separator()

                    # Legs
                    box.prop(props, "gui_extra_props_legs", text='Legs')
                    if props.gui_extra_props_legs:
                        legs_col = box.box()
                        legs_col.scale_x = 1
                        legs_col.scale_y = 1
                        legs_col.alignment = 'CENTER'
                        legs_col.label(text='Curved Legs')
                        legs_row = legs_col.row()
                        col_1 = legs_row.column()
                        col_1.scale_x = 1
                        col_1.scale_y = 1
                        col_1.alignment = 'CENTER'
                        col_2 = legs_row.column()
                        col_2.scale_x = 1
                        col_2.scale_y = 1
                        col_2.alignment = 'CENTER'
                        col_1.prop(arm_bones['properties_leg_R'], '["curved_leg_R"]', text="Curve_R", slider=True)
                        col_1.prop(arm_bones['properties_leg_R'], '["curved_leg_tweak_R"]', text="Tweak_R", slider=True)
                        col_2.prop(arm_bones['properties_leg_L'], '["curved_leg_L"]', text="Curve_L", slider=True)
                        col_2.prop(arm_bones['properties_leg_L'], '["curved_leg_tweak_L"]', text="Tweak_L", slider=True)
                        legs_col.separator()

                    # Props
                    box.prop(props, "gui_extra_props_props", text='Props')
                    if props.gui_extra_props_props:
                        accessories_col = box.box()
                        accessories_col.scale_x = 1
                        accessories_col.scale_y = 1
                        accessories_col.alignment = 'CENTER'
                        accessories_col.label(text='Props Space')
                        accessories_row = accessories_col.row()
                        col_1 = accessories_row.column()
                        col_1.scale_x = 1
                        col_1.scale_y = 1
                        col_1.alignment = 'CENTER'
                        col_3 = accessories_row.column()
                        col_3.scale_x = 1
                        col_3.scale_y = 1
                        col_3.alignment = 'CENTER'
                        col_1.label(text='Hat')
                        col_1.label(text='Eyeglasses')
                        col_1.label(text='Hand Accessory')
                        row_hat = col_3.row(align=True)
                        row_hat.alignment = 'CENTER'
                        row_hat.scale_x = 2.5
                        row_hat.scale_y = 1
                        row_hat.operator(
                            "show.hat_list", text="{}".format(
                                "      Free      " if arm_bones['properties_head']["hat_free"] == 0 else "Follow Head"),
                            emboss=True)
                        col_prop = row_hat.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_head'], '["hat_free"]', toggle=True, icon_only=1, emboss=1)
                        row_eyeglasses = col_3.row(align=True)
                        row_eyeglasses.alignment = 'CENTER'
                        row_eyeglasses.scale_x = 2.5
                        row_eyeglasses.scale_y = 1
                        row_eyeglasses.operator(
                            "show.eyeglasses_list", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_head']["glasses_free"] == 0 else "Follow Head"),
                            emboss=True)
                        col_prop = row_eyeglasses.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_head'], '["glasses_free"]',
                                      toggle=True, icon_only=1, emboss=1)
                        row_accessory = col_3.row(align=True)
                        row_accessory.alignment = 'CENTER'
                        row_accessory.scale_x = 2.5
                        row_accessory.scale_y = 1
                        row_accessory.operator(
                            "show.hand_accessory_list", text="{}".format(
                                "      Free      "
                                if arm_bones['properties_arm_L']['hand_accessory_L'] == 0 and
                                arm_bones['properties_arm_R']['hand_accessory_R'] == 0
                                else (
                                    "Follow Hand_L"
                                    if arm_bones['properties_arm_R']['hand_accessory_R'] == 0 else "Follow Hand_R")),
                            emboss=True)
                        col_prop = row_accessory.column(align=True)
                        col_prop.scale_x = 0.25
                        col_prop.prop(arm_bones['properties_arm_L'], '["hand_accessory_L"]',
                                      toggle=True, icon_only=1, emboss=1)
                        col_prop2 = row_accessory.column(align=True)
                        col_prop2.scale_x = 0.25
                        col_prop2.prop(arm_bones['properties_arm_R'], '["hand_accessory_R"]',
                                       toggle=True, icon_only=1, emboss=1)

                        accessories_col.separator()
                        accessories_col.separator()

                    box.separator()
                    box.separator()

                # collapsed box
                elif "gui_misc" in arm:
                    row.operator("gui.blenrig_6_tabs", icon="SETTINGS", emboss=1).tab = "gui_misc"
                    row.label(text="EXTRA PROPERTIES")

    # Custom Properties
            if context.mode == "POSE":

                if "gui_cust_props" in arm:
                    box = layout.column()
                    col = box.column()
                    row = col.row()
                # expanded box
                if "gui_cust_props" in arm and arm["gui_cust_props"]:
                    row.operator("gui.blenrig_6_tabs", icon="SETTINGS", emboss=1).tab = "gui_cust_props"
                    row.label(text="CUSTOM PROPERTIES")

                    # Head Accessories
                    col = box.column()
                    row_rot = col.row()
                    col_rot = row_rot.column()
                    if act_bone is not None:
                        for cust_prop in act_bone.keys():
                            if cust_prop == 'ROT_MODE':
                                col_rot.separator()
                                col_rot.label(text='ACTIVE BONE ROTATION ORDER', icon="AXIS_TOP")
                                box_rot = col_rot.box()
                                box_rot.prop(act_bone, '["ROT_MODE"]', toggle=True)
                                col_rot.separator()
                                col_rot.separator()

                    row_props = col.row()
                    col_props = row_props.column()
                    col_props.label(text='CUSTOM PROPERTIES', icon="BONE_DATA")
                    row_all = col_props.row()
                    row_all.alignment = "LEFT"
                    row_all.prop(props, "gui_cust_props_all", text="All")
                    col_props.separator()
                    if not props.gui_cust_props_all:
                        if act_bone is not None:
                            if ('properties' not in act_bone.name):
                                for cust_prop in act_bone.keys():
                                    excluded = ['_RNA_UI', 'ROT_MODE']
                                    if (cust_prop not in excluded):
                                        box_props = col_props.box()
                                        box_props.prop(act_bone, '["{}"]'.format(cust_prop))
                    if props.gui_cust_props_all:
                        for b in arm_bones:
                            if ('properties' not in b.name):
                                for cust_prop in b.keys():
                                    if cust_prop != '_RNA_UI' and cust_prop != 'ROT_MODE':
                                        box_props = col_props.box()
                                        box_props.prop(
                                            b, '["{}"]'.format(cust_prop),
                                            text='["{} {}"]'.format(b.name, cust_prop))
                    col_props.separator()

                # collapsed box
                elif "gui_cust_props" in arm:
                    row.operator("gui.blenrig_6_tabs", icon="SETTINGS", emboss=1).tab = "gui_cust_props"
                    row.label(text="CUSTOM PROPERTIES")

    # Muscle System box
            if context.mode == "POSE":

                if "gui_muscle" in arm:
                    box = layout.column()
                    col = box.column()
                    row = col.row()
                # expanded box
                if "gui_muscle" in arm and arm["gui_muscle"]:
                    row.operator("gui.blenrig_6_tabs", icon="FORCE_LENNARDJONES", emboss=1).tab = "gui_muscle"
                    row.label(text="MUSCLE SYSTEM")
                    # System Toggle
                    col = box.column()
                    row = col.row()
                    row.label(text="Off")
                    row = row.row()
                    row.alignment = "RIGHT"
                    row.label(text="On")
                    col.prop(arm_bones['properties'], '["muscle_system"]', text="Muscles", toggle=True)

                    box.separator()

                    # Resolution
                    col = box.column()
                    col.prop(arm_bones['properties'], '["muscle_res"]', text="Muscle Resolution", toggle=True)

                    box.separator()

                    # Extras Deformation
                    col = box.column()
                    col.prop(arm_bones['properties'], '["deformation_extras"]', text="Deformation Extras", toggle=True)

                # collapsed box
                elif "gui_muscle" in arm:
                    row.operator("gui.blenrig_6_tabs", icon="FORCE_LENNARDJONES", emboss=1).tab = "gui_muscle"
                    row.label(text="MUSCLE SYSTEM")

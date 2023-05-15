import bpy
from math import radians
import numpy as np

####### Bones Hiding System #######

from bpy.props import FloatProperty, IntProperty, BoolProperty

import os
import json
target_bones = None
script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
toggle_bones_names_file = os.path.join(directory, "data_jsons", "toggle_bones_names.json")

with open(toggle_bones_names_file, "r") as jsonFile:
    target_bones = json.load(jsonFile)


def bone_auto_hide(context):

    if context:

        if not bpy.context.screen:
            return False

        if bpy.context.screen.is_animation_playing == True and not bpy.context.active_object:
            return False

        if not bpy.context.active_object:
            return

        if bpy.context.active_object.type == "ARMATURE" and bpy.context.active_object.mode == 'POSE':
            for b_prop in bpy.context.active_object.data.items():
                if b_prop[0] == 'bone_auto_hide' and b_prop[1] == 0:
                    return False

            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                    arm = bpy.context.active_object.data
                    p_bones = bpy.context.active_object.pose.bones

                    for b in p_bones:
                        if ('properties' in b.name):
                            if ('torso' in b.name):

                                # Torso FK/IK
                                prop = int(b.ik_torso)
                                prop_inv = int(b.inv_torso)

                                for bone in arm.bones:
                                    if (bone.name in b['bones_ik']):
                                        if prop == 1 or prop_inv == 1:
                                            bone.hide = 1
                                        else:
                                            bone.hide = 0
                                    if (bone.name in b['bones_fk']):
                                        if prop != 1 or prop_inv == 1:
                                            bone.hide = 1
                                        else:
                                            bone.hide = 0

                            # Torso INV
                                for bone in arm.bones:
                                    if (bone.name in b['bones_inv']):
                                        if prop_inv == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1
                            if ('head' in b.name):
                                # Neck FK/IK
                                prop = int(b.ik_head)
                                for bone in arm.bones:
                                    if (bone.name in b['bones_fk']):
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1
                                    if (bone.name in b['bones_ik']):
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1

                            # Head Hinge
                                prop_hinge = int(b.hinge_head)
                                for bone in arm.bones:
                                    if (bone.name in b['bones_fk_hinge']):
                                        if prop == 1 or prop_hinge == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1
                                    if (bone.name in b['bones_ik_hinge']):
                                        if prop == 0 or prop_hinge == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1
                            # Left Properties
                            if ('_L' in b.name):
                                if ('arm' in b.name):

                                    # Arm_L FK/IK
                                    prop = int(b.ik_arm_L)
                                    prop_hinge = int(b.hinge_hand_L)
                                    for bone in arm.bones:
                                        if (bone.name in b['bones_fk_L']):
                                            if prop == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1
                                        if (bone.name in b['bones_ik_L']):
                                            if prop == 0:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1

                                # HAND_L
                                        if arm['rig_type'] == "Biped":
                                            if (bone.name in b['bones_ik_hand_L']):
                                                if prop == 1 and prop_hinge == 0:
                                                    bone.hide = 1
                                                else:
                                                    bone.hide = 0
                                            if (bone.name in b['bones_fk_hand_L']):
                                                if prop_hinge == 1:
                                                    bone.hide = 1
                                                else:
                                                    bone.hide = 0
                                            if (bone.name in b['bones_ik_palm_L']):
                                                if prop == 1 or prop_hinge == 0:
                                                    bone.hide = 1
                                                else:
                                                    bone.hide = 0
                                            if (bone.name in b['bones_fk_palm_L']):
                                                if prop == 1 or prop_hinge == 0:
                                                    bone.hide = 0
                                                else:
                                                    bone.hide = 1

                                # Fingers_L
                                    prop_ik_all = int(b.ik_fing_all_L)
                                    prop_hinge_all = int(b.hinge_fing_all_L)

                                    def fingers_hide(b_name):
                                        for bone in arm.bones:
                                            ik_bones = [b_name]
                                            if (bone.name == b_name):
                                                if prop == 1 or prop_hinge == 1 or prop_ik_all == 1 or prop_hinge_all == 1:
                                                    bone.hide = 0
                                                if prop == 0 and prop_hinge == 0 and prop_ik_all == 0 and prop_hinge_all == 0:
                                                    bone.hide = 1
                                        return {"FINISHED"}

                                    prop_hinge = int(b.hinge_fing_ind_L)
                                    prop = int(b.ik_fing_ind_L)
                                    fingers_hide('fing_ind_ik_L')
                                    prop_hinge = int(b.hinge_fing_mid_L)
                                    prop = int(b.ik_fing_mid_L)
                                    fingers_hide('fing_mid_ik_L')
                                    prop_hinge = int(b.hinge_fing_ring_L)
                                    prop = int(b.ik_fing_ring_L)
                                    fingers_hide('fing_ring_ik_L')
                                    prop_hinge = int(b.hinge_fing_lit_L)
                                    prop = int(b.ik_fing_lit_L)
                                    fingers_hide('fing_lit_ik_L')
                                    prop_hinge = int(b.hinge_fing_thumb_L)
                                    prop = int(b.ik_fing_thumb_L)
                                    fingers_hide('fing_thumb_ik_L')

                                if ('leg' in b.name):
                                    # Leg_L FK/IK
                                    prop = int(b.ik_leg_L)
                                    for bone in arm.bones:
                                        if (bone.name in b['bones_fk_L']):
                                            if prop == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1
                                        if (bone.name in b['bones_ik_L']):
                                            if prop == 0:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1

                                # Toes_L FK/IK
                                    prop = int(b.ik_toes_all_L)
                                    prop_hinge = int(b.hinge_toes_all_L)
                                    for bone in arm.bones:
                                        if (bone.name in b['bones_fk_foot_L']):
                                            if prop == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1
                                        if (bone.name in b['bones_ik_foot_L']):
                                            if prop == 0 or prop_hinge == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1

                            # Right Properties
                            if ('_R' in b.name):
                                if ('arm' in b.name):

                                    # Arm_R FK/IK
                                    prop = int(b.ik_arm_R)
                                    prop_hinge = int(b.hinge_hand_R)
                                    for bone in arm.bones:
                                        if (bone.name in b['bones_fk_R']):
                                            if prop == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1
                                        if (bone.name in b['bones_ik_R']):
                                            if prop == 0:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1

                                # HAND_R
                                        if arm['rig_type'] == "Biped":
                                            if (bone.name in b['bones_ik_hand_R']):
                                                if prop == 1 and prop_hinge == 0:
                                                    bone.hide = 1
                                                else:
                                                    bone.hide = 0
                                            if (bone.name in b['bones_fk_hand_R']):
                                                if prop_hinge == 1:
                                                    bone.hide = 1
                                                else:
                                                    bone.hide = 0
                                            if (bone.name in b['bones_ik_palm_R']):
                                                if prop == 1 or prop_hinge == 0:
                                                    bone.hide = 1
                                                else:
                                                    bone.hide = 0
                                            if (bone.name in b['bones_fk_palm_R']):
                                                if prop == 1 or prop_hinge == 0:
                                                    bone.hide = 0
                                                else:
                                                    bone.hide = 1

                                # Fingers_R
                                    prop_ik_all = int(b.ik_fing_all_R)
                                    prop_hinge_all = int(b.hinge_fing_all_R)

                                    def fingers_hide(b_name):
                                        for bone in arm.bones:
                                            ik_bones = [b_name]
                                            if (bone.name == b_name):
                                                if prop == 1 or prop_hinge == 1 or prop_ik_all == 1 or prop_hinge_all == 1:
                                                    bone.hide = 0
                                                if prop == 0 and prop_hinge == 0 and prop_ik_all == 0 and prop_hinge_all == 0:
                                                    bone.hide = 1
                                        return {"FINISHED"}

                                    prop_hinge = int(b.hinge_fing_ind_R)
                                    prop = int(b.ik_fing_ind_R)
                                    fingers_hide('fing_ind_ik_R')
                                    prop_hinge = int(b.hinge_fing_mid_R)
                                    prop = int(b.ik_fing_mid_R)
                                    fingers_hide('fing_mid_ik_R')
                                    prop_hinge = int(b.hinge_fing_ring_R)
                                    prop = int(b.ik_fing_ring_R)
                                    fingers_hide('fing_ring_ik_R')
                                    prop_hinge = int(b.hinge_fing_lit_R)
                                    prop = int(b.ik_fing_lit_R)
                                    fingers_hide('fing_lit_ik_R')
                                    prop_hinge = int(b.hinge_fing_thumb_R)
                                    prop = int(b.ik_fing_thumb_R)
                                    fingers_hide('fing_thumb_ik_R')

                                if ('leg' in b.name):
                                    # Leg_R FK/IK
                                    prop = int(b.ik_leg_R)
                                    for bone in arm.bones:
                                        if (bone.name in b['bones_fk_R']):
                                            if prop == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1
                                        if (bone.name in b['bones_ik_R']):
                                            if prop == 0:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1

                                # Toes_R FK/IK
                                    prop = int(b.ik_toes_all_R)
                                    prop_hinge = int(b.hinge_toes_all_R)
                                    for bone in arm.bones:
                                        if (bone.name in b['bones_fk_foot_R']):
                                            if prop == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1
                                        if (bone.name in b['bones_ik_foot_R']):
                                            if prop == 0 or prop_hinge == 1:
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1


####### Reproportion Toggle #######
listaDeEstados = []
# Auto mode for reproportion now is in ARMATURE_OT_blenrig_6_gui in __init__.py for gui_rig_bake button.

mode = []
layers = []


def reproportion_toggle(self, context):

    if context:
        mode.append(context.active_object.mode)
        layers.append(context.active_object.data.layers[:])

        if context.active_object.data.reproportion:
            bpy.ops.object.mode_set(mode='POSE')

        else:
            # if len(mode) > 1:
            #     bpy.ops.object.mode_set(mode=mode[-2])
            if len(layers) > 1:
                context.active_object.data.layers = layers[-2]

        if len(mode) > 1:
            del mode[0]
        if len(layers) > 1:
            del layers[0]

        if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
            return False

        if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                    prop = bool(context.active_object.data.reproportion)
                    p_bones = context.active_object.pose.bones
                    if prop:
                        contador = 0
                        for layer in context.active_object.data.layers:
                            listaDeEstados.insert(contador, layer)
                            contador += 1

                        contador = 0
                        for layer in context.active_object.data.layers:
                            if layer:
                                context.active_object.data.layers[contador] = not context.active_object.data.layers[contador]

                            contador += 1
                            context.active_object.data.layers[31] = True

                        for b in p_bones:
                            for C in b.constraints:
                                if ('REPROP' in C.name):
                                    C.mute = False
                                if ('NOREP' in C.name):
                                    C.mute = True
                    else:
                        contador = 0
                        try:
                            for layer in context.active_object.data.layers:
                                context.active_object.data.layers[contador] = listaDeEstados[contador]
                                contador += 1

                            for b in p_bones:
                                for C in b.constraints:
                                    if ('REPROP' in C.name):
                                        C.mute = True
                                    if ('NOREP' in C.name):
                                        C.mute = False
                        except:
                            pass

####### Rig Toggles #######

# Legacy Function for BlenRig 5 Rigs


def rig_toggles(context, call_from: str, call_from_side: str):
    # zebus 1
    from datetime import datetime
    start = datetime.now()

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        amr_obj = context.active_object
        arm = amr_obj.data
        p_bones = amr_obj.pose.bones

        # valid_bones = []
        # for b in p_bones:

        #     # si no contiene ni el sufijo _L ni _R pasamos al siguiente:
        #     if all([not b.name.endswith("_L"), not b.name.endswith("_R")]):
        #         continue

        #     valid_bones.append(b)

        # Para poder optimizar el computo a la mitad:
        # como solo se llama desde toes (pies) y fingers (manos) lo he acotado tanto al tipo como a si es Left o Right:
        # valid_bones_phase_1 = [b for b in p_bones if b.name.endswith(call_from_side)]
        pack_bones_1 = [p_bones[finger_name+call_from_side] for finger_name in target_bones["HUMANOID"]["PROPERTIES"]]

        if call_from == "fingers":
            target_key = "HAND"
        elif call_from == "toes":
            target_key = "TOES"

        pack_bones_2 = [p_bones[finger_name+call_from_side] for finger_name in target_bones["HUMANOID"][target_key]]

        def set_bone_layers(bone_list, layer_list, constraints_state, side):

            for bl in bone_list:
                for b in pack_bones_2:

                    if b.name != str(bl + side):
                        continue

                    b.bone.layers = [i in layer_list for i in range(len(b.bone.layers))]

                    for const in b.constraints:
                        if 'REPROP' in const.name:
                            const.mute = not arm.reproportion
                        elif 'NOREP' in const.name:
                            const.mute = arm.reproportion
                        else:
                            const.mute = not constraints_state

        fingers_bones = ['hand_close', 'fing_spread']
        foot_toes_str = ['toes_str_1', 'toes_str_2', 'toes_str_3']

        for b in pack_bones_1:

            # # si no empieza por properties pasamos al siguiente:
            # if not b.name.startswith("properties"):
            #     continue

            # # si no contiene ni arm ni leg pasamos al siguiente:
            # if all(["arm" not in b.name, "leg" not in b.name]):
            #     continue

            toggle_fingers_L = b.toggle_fingers_L
            toggle_fingers_R = b.toggle_fingers_R
            toggle_toes_L = b.toggle_toes_L
            toggle_toes_R = b.toggle_toes_R

            if b.name.endswith('_L'):
                side = '_L'
            elif b.name.endswith('_R'):
                side = '_R'

            if side == '_L':
                # Fingers_L
                if "arm" in b.name:

                    b.toggle_fingers_thumb_L = toggle_fingers_L
                    b.toggle_fingers_index_L = toggle_fingers_L
                    b.toggle_fingers_middle_L = toggle_fingers_L
                    b.toggle_fingers_ring_L = toggle_fingers_L
                    b.toggle_fingers_little_L = toggle_fingers_L

                    if toggle_fingers_L:
                        layers_hardcoded = [5, 16, 24, 25, 31]
                    else:
                        layers_hardcoded = [24]

                    set_bone_layers(fingers_bones, layers_hardcoded, toggle_fingers_L, side)

                # Toes_L
                elif 'leg' in b.name:
                    b.toggle_toes_big_L = toggle_toes_L
                    b.toggle_toes_index_L = toggle_toes_L
                    b.toggle_toes_middle_L = toggle_toes_L
                    b.toggle_toes_fourth_L = toggle_toes_L
                    b.toggle_toes_little_L = toggle_toes_L

                    if toggle_toes_L:
                        layers_hardcoded_1 = [10, 24, 25, 31]
                        layers_hardcoded_2 = [9, 24, 25]
                        layers_hardcoded_3 = [24, 31]
                    else:
                        layers_hardcoded_1 = [24]
                        layers_hardcoded_2 = [24]
                        layers_hardcoded_3 = [24]

                    set_bone_layers(['toes_spread'], layers_hardcoded_1, toggle_toes_L, side)
                    set_bone_layers(['toes_ik_ctrl'], layers_hardcoded_2, toggle_toes_L, side)
                    set_bone_layers(foot_toes_str, layers_hardcoded_3, toggle_toes_L, side)

            else:
                # Fingers_R
                if "arm" in b.name:
                    b.toggle_fingers_thumb_R = toggle_fingers_R
                    b.toggle_fingers_index_R = toggle_fingers_R
                    b.toggle_fingers_middle_R = toggle_fingers_R
                    b.toggle_fingers_ring_R = toggle_fingers_R
                    b.toggle_fingers_little_R = toggle_fingers_R

                    if toggle_fingers_R:
                        layers_hardcoded = [3, 6, 24, 25, 31]
                    else:
                        layers_hardcoded = [24]

                    set_bone_layers(fingers_bones, layers_hardcoded, toggle_fingers_R, side)

                # Toes_R
                elif 'leg' in b.name:
                    b.toggle_toes_big_R = toggle_toes_R
                    b.toggle_toes_index_R = toggle_toes_R
                    b.toggle_toes_middle_R = toggle_toes_R
                    b.toggle_toes_fourth_R = toggle_toes_R
                    b.toggle_toes_little_R = toggle_toes_R

                    if toggle_toes_R:
                        layers_hardcoded_1 = [10, 24, 25, 31]
                        layers_hardcoded_2 = [23, 24, 25]
                        layers_hardcoded_3 = [24, 31]
                    else:
                        layers_hardcoded_1 = [24]
                        layers_hardcoded_2 = [24]
                        layers_hardcoded_3 = [24]

                    set_bone_layers(['toes_spread'], layers_hardcoded_1, toggle_toes_R, side)
                    set_bone_layers(['toes_ik_ctrl'], layers_hardcoded_2, toggle_toes_R, side)
                    set_bone_layers(foot_toes_str, layers_hardcoded_3, toggle_toes_R, side)

    print('[###] zebus TIME rig_toggles:', datetime.now()-start)


def fingers_toggles(self, context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                amr_obj = context.active_object
                arm = amr_obj.data
                p_bones = amr_obj.pose.bones

                # Fingers List
                thumb_fk_list = ['fing_thumb_1_L', 'fing_thumb_2_L', 'fing_thumb_3_L']
                thumb_ctrl_list = ['fing_thumb_ctrl_L']
                thumb_toon_list = ['fing_thumb_4_toon_L', 'fing_thumb_3_toon_L',
                                   'fing_thumb_2_toon_L', 'fing_thumb_1_toon_1_L']
                thumb_ik_list = ['fing_thumb_ik_L']
                thumb_str_list = ['fing_thumb_str_1_L', 'fing_thumb_str_2_L',
                                  'fing_thumb_str_3_L', 'fing_thumb_str_4_L']
                thumb_def_list = ['fing_thumb_3_def_L', 'fing_thumb_2_def_L', 'fing_thumb_1_def_L']
                thumb_fix_list = ['fing_thumb_fix_low_2_L', 'fing_thumb_fix_up_2_L',
                                  'fing_thumb_fix_up_1_L', 'fing_thumb_fix_low_1_L']
                thumb_action_list = ['fing_thumb_ctrl_mstr_L']
                thumb_mech_list = ['fing_thumb_ctrl_track_L', 'fing_thumb_shp_at_L', 'fing_thumb_2_ik_L',
                                   'fing_thumb_3_ik_L', 'fing_thumb_1_ik_L', 'fing_thumb_2_rot_L', 'fing_thumb_ctrl_shp_at_L']

                index_fk_list = ['fing_ind_2_L', 'fing_ind_3_L', 'fing_ind_4_L']
                index_ctrl_list = ['fing_ind_ctrl_L']
                index_toon_list = ['fing_ind_5_toon_L', 'fing_ind_4_toon_L',
                                   'fing_ind_3_toon_L', 'fing_ind_2_toon_L', 'fing_ind_1_toon_L']
                index_ik_list = ['fing_ind_ik_L']
                index_str_list = ['fing_ind_str_1_L', 'fing_ind_str_2_L',
                                  'fing_ind_str_3_L', 'fing_ind_str_4_L', 'fing_ind_str_5_L']
                index_def_list = ['fing_ind_4_def_L', 'fing_ind_3_def_L', 'fing_ind_2_def_L', 'fing_ind_1_def_L']
                index_fix_list = ['fing_ind_fix_low_3_L', 'fing_ind_fix_up_3_L', 'fing_ind_fix_low_2_L',
                                  'fing_ind_fix_up_2_L', 'fing_ind_fix_up_1_L', 'fing_ind_fix_low_1_L']
                index_action_list = ['fing_ind_ctrl_mstr_L']
                index_mech_list = [
                    'fing_ind_ctrl_loc_L', 'fing_ind_ctrl_track_L', 'fing_ind_2_ik_L', 'fing_ind_3_ik_L',
                    'fing_ind_4_ik_L', 'fing_ind_shp_at_L', 'fing_ind_1_L', 'fing_ind_2_rot_L',
                    'fing_ind_ctrl_shp_at_L', 'fing_ind_ctrl_bend_loc_L']

                middle_fk_list = ['fing_mid_2_L', 'fing_mid_3_L', 'fing_mid_4_L']
                middle_ctrl_list = ['fing_mid_ctrl_L']
                middle_toon_list = ['fing_mid_5_toon_L', 'fing_mid_4_toon_L',
                                    'fing_mid_3_toon_L', 'fing_mid_2_toon_L', 'fing_mid_1_toon_L']
                middle_ik_list = ['fing_mid_ik_L']
                middle_str_list = ['fing_mid_str_1_L', 'fing_mid_str_2_L',
                                   'fing_mid_str_3_L', 'fing_mid_str_4_L', 'fing_mid_str_5_L']
                middle_def_list = ['fing_mid_4_def_L', 'fing_mid_3_def_L', 'fing_mid_2_def_L', 'fing_mid_1_def_L']
                middle_fix_list = ['fing_mid_fix_low_3_L', 'fing_mid_fix_up_3_L', 'fing_mid_fix_low_2_L',
                                   'fing_mid_fix_up_2_L', 'fing_mid_fix_up_1_L', 'fing_mid_fix_low_1_L']
                middle_action_list = ['fing_mid_ctrl_mstr_L']
                middle_mech_list = ['fing_mid_ctrl_loc_L', 'fing_mid_ctrl_track_L', 'fing_mid_2_ik_L',
                                    'fing_mid_3_ik_L', 'fing_mid_4_ik_L', 'fing_mid_shp_at_L', 'fing_mid_1_L',
                                    'fing_mid_2_rot_L', 'fing_mid_ctrl_shp_at_L', 'fing_mid_ctrl_bend_loc_L']

                ring_fk_list = ['fing_ring_2_L', 'fing_ring_3_L', 'fing_ring_4_L']
                ring_ctrl_list = ['fing_ring_ctrl_L']
                ring_toon_list = ['fing_ring_5_toon_L', 'fing_ring_4_toon_L',
                                  'fing_ring_3_toon_L', 'fing_ring_2_toon_L', 'fing_ring_1_toon_L']
                ring_ik_list = ['fing_ring_ik_L']
                ring_str_list = ['fing_ring_str_1_L', 'fing_ring_str_2_L',
                                 'fing_ring_str_3_L', 'fing_ring_str_4_L', 'fing_ring_str_5_L']
                ring_def_list = ['fing_ring_4_def_L', 'fing_ring_3_def_L', 'fing_ring_2_def_L', 'fing_ring_1_def_L']
                ring_fix_list = ['fing_ring_fix_low_3_L', 'fing_ring_fix_up_3_L', 'fing_ring_fix_low_2_L',
                                 'fing_ring_fix_up_2_L', 'fing_ring_fix_up_1_L', 'fing_ring_fix_low_1_L']
                ring_action_list = ['fing_ring_ctrl_mstr_L']
                ring_mech_list = ['fing_ring_ctrl_loc_L', 'fing_ring_ctrl_track_L', 'fing_ring_2_ik_L',
                                  'fing_ring_3_ik_L', 'fing_ring_4_ik_L', 'fing_ring_shp_at_L', 'fing_ring_1_L',
                                  'fing_ring_2_rot_L', 'fing_ring_ctrl_shp_at_L', 'fing_ring_ctrl_bend_loc_L']

                little_fk_list = ['fing_lit_2_L', 'fing_lit_3_L', 'fing_lit_4_L']
                little_ctrl_list = ['fing_lit_ctrl_L']
                little_toon_list = ['fing_lit_5_toon_L', 'fing_lit_4_toon_L',
                                    'fing_lit_3_toon_L', 'fing_lit_2_toon_L', 'fing_lit_1_toon_L']
                little_ik_list = ['fing_lit_ik_L']
                little_str_list = ['fing_lit_str_1_L', 'fing_lit_str_2_L',
                                   'fing_lit_str_3_L', 'fing_lit_str_4_L', 'fing_lit_str_5_L']
                little_def_list = ['fing_lit_4_def_L', 'fing_lit_3_def_L', 'fing_lit_2_def_L', 'fing_lit_1_def_L']
                little_fix_list = ['fing_lit_fix_low_3_L', 'fing_lit_fix_up_3_L', 'fing_lit_fix_low_2_L',
                                   'fing_lit_fix_up_2_L', 'fing_lit_fix_up_1_L', 'fing_lit_fix_low_1_L']
                little_action_list = ['fing_lit_ctrl_mstr_L']
                little_mech_list = ['fing_lit_ctrl_loc_L', 'fing_lit_ctrl_track_L', 'fing_lit_2_ik_L',
                                    'fing_lit_3_ik_L', 'fing_lit_4_ik_L', 'fing_lit_shp_at_L', 'fing_lit_1_L',
                                    'fing_lit_2_rot_L', 'fing_lit_ctrl_shp_at_L', 'fing_lit_ctrl_bend_loc_L']

                def set_bone_layers(bone_list, layer_list, constraints_state, side):
                    bones = bone_list
                    layers = layer_list
                    for B in bones:
                        for b in p_bones:
                            if b.name == str(B[0:-2] + side):
                                for L in layers:
                                    b.bone.layers[L] = 1
                                    for l in range(len(b.bone.layers)):
                                        if l not in layers:
                                            b.bone.layers[l] = 0
                                if constraints_state == 'On':
                                    for C in b.constraints:
                                        C.mute = False
                                        if arm.reproportion:
                                            if ('REPROP' in C.name):
                                                C.mute = False
                                            if ('NOREP' in C.name):
                                                C.mute = True
                                        else:
                                            if ('REPROP' in C.name):
                                                C.mute = True
                                            if ('NOREP' in C.name):
                                                C.mute = False
                                if constraints_state == 'Off':
                                    for C in b.constraints:
                                        C.mute = True

                for b in p_bones:
                    if ('properties' in b.name):
                        # Fingers_L
                        if b.name.endswith('_L'):
                            if ('arm' in b.name):
                                if b.toggle_fingers_thumb_L:
                                    set_bone_layers(thumb_fk_list, [17, 24, 25], 'On', '_L')
                                    set_bone_layers(thumb_ctrl_list, [5, 16, 24, 25, 28, 29], 'On', '_L')
                                    set_bone_layers(thumb_toon_list, [14, 24, 25], 'On', '_L')
                                    set_bone_layers(thumb_ik_list, [19, 24, 25], 'On', '_L')
                                    set_bone_layers(thumb_str_list, [24, 25, 31], 'On', '_L')
                                    set_bone_layers(thumb_def_list, [24, 27, 29, 31], 'On', '_L')
                                    set_bone_layers(thumb_fix_list, [24, 27], 'On', '_L')
                                    set_bone_layers(thumb_action_list, [24, 28], 'On', '_L')
                                    set_bone_layers(thumb_mech_list, [26, 24], 'On', '_L')
                                else:
                                    set_bone_layers(thumb_fk_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_ctrl_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_toon_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_ik_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_str_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_def_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_fix_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_action_list, [24], 'Off', '_L')
                                    set_bone_layers(thumb_mech_list, [24], 'Off', '_L')
                                if b.toggle_fingers_index_L:
                                    set_bone_layers(index_fk_list, [17, 24, 25], 'On', '_L')
                                    set_bone_layers(index_ctrl_list, [5, 16, 24, 25, 28, 29], 'On', '_L')
                                    set_bone_layers(index_toon_list, [14, 24, 25], 'On', '_L')
                                    set_bone_layers(index_ik_list, [19, 24, 25], 'On', '_L')
                                    set_bone_layers(index_str_list, [24, 25, 31], 'On', '_L')
                                    set_bone_layers(index_def_list, [24, 27, 29, 31], 'On', '_L')
                                    set_bone_layers(index_fix_list, [24, 27], 'On', '_L')
                                    set_bone_layers(index_action_list, [24, 28], 'On', '_L')
                                    set_bone_layers(index_mech_list, [26, 24], 'On', '_L')
                                else:
                                    set_bone_layers(index_fk_list, [24], 'Off', '_L')
                                    set_bone_layers(index_ctrl_list, [24], 'Off', '_L')
                                    set_bone_layers(index_toon_list, [24], 'Off', '_L')
                                    set_bone_layers(index_ik_list, [24], 'Off', '_L')
                                    set_bone_layers(index_str_list, [24], 'Off', '_L')
                                    set_bone_layers(index_def_list, [24], 'Off', '_L')
                                    set_bone_layers(index_fix_list, [24], 'Off', '_L')
                                    set_bone_layers(index_action_list, [24], 'Off', '_L')
                                    set_bone_layers(index_mech_list, [24], 'Off', '_L')
                                if b.toggle_fingers_middle_L:
                                    set_bone_layers(middle_fk_list, [17, 24, 25], 'On', '_L')
                                    set_bone_layers(middle_ctrl_list, [5, 16, 24, 25, 28, 29], 'On', '_L')
                                    set_bone_layers(middle_toon_list, [14, 24, 25], 'On', '_L')
                                    set_bone_layers(middle_ik_list, [19, 24, 25], 'On', '_L')
                                    set_bone_layers(middle_str_list, [24, 25, 31], 'On', '_L')
                                    set_bone_layers(middle_def_list, [24, 27, 29, 31], 'On', '_L')
                                    set_bone_layers(middle_fix_list, [24, 27], 'On', '_L')
                                    set_bone_layers(middle_action_list, [24, 28], 'On', '_L')
                                    set_bone_layers(middle_mech_list, [26, 24], 'On', '_L')
                                else:
                                    set_bone_layers(middle_fk_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_ctrl_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_toon_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_ik_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_str_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_def_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_fix_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_action_list, [24], 'Off', '_L')
                                    set_bone_layers(middle_mech_list, [24], 'Off', '_L')
                                if b.toggle_fingers_ring_L:
                                    set_bone_layers(ring_fk_list, [17, 24, 25], 'On', '_L')
                                    set_bone_layers(ring_ctrl_list, [5, 16, 24, 25, 28, 29], 'On', '_L')
                                    set_bone_layers(ring_toon_list, [14, 24, 25], 'On', '_L')
                                    set_bone_layers(ring_ik_list, [19, 24, 25], 'On', '_L')
                                    set_bone_layers(ring_str_list, [24, 25, 31], 'On', '_L')
                                    set_bone_layers(ring_def_list, [24, 27, 29, 31], 'On', '_L')
                                    set_bone_layers(ring_fix_list, [24, 27], 'On', '_L')
                                    set_bone_layers(ring_action_list, [24, 28], 'On', '_L')
                                    set_bone_layers(ring_mech_list, [26, 24], 'On', '_L')
                                else:
                                    set_bone_layers(ring_fk_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_ctrl_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_toon_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_ik_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_str_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_def_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_fix_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_action_list, [24], 'Off', '_L')
                                    set_bone_layers(ring_mech_list, [24], 'Off', '_L')
                                if b.toggle_fingers_little_L:
                                    set_bone_layers(little_fk_list, [17, 24, 25], 'On', '_L')
                                    set_bone_layers(little_ctrl_list, [5, 16, 24, 25, 28, 29], 'On', '_L')
                                    set_bone_layers(little_toon_list, [14, 24, 25], 'On', '_L')
                                    set_bone_layers(little_ik_list, [19, 24, 25], 'On', '_L')
                                    set_bone_layers(little_str_list, [24, 25, 31], 'On', '_L')
                                    set_bone_layers(little_def_list, [24, 27, 29, 31], 'On', '_L')
                                    set_bone_layers(little_fix_list, [24, 27], 'On', '_L')
                                    set_bone_layers(little_action_list, [24, 28], 'On', '_L')
                                    set_bone_layers(little_mech_list, [26, 24], 'On', '_L')
                                else:
                                    set_bone_layers(little_fk_list, [24], 'Off', '_L')
                                    set_bone_layers(little_ctrl_list, [24], 'Off', '_L')
                                    set_bone_layers(little_toon_list, [24], 'Off', '_L')
                                    set_bone_layers(little_ik_list, [24], 'Off', '_L')
                                    set_bone_layers(little_str_list, [24], 'Off', '_L')
                                    set_bone_layers(little_def_list, [24], 'Off', '_L')
                                    set_bone_layers(little_fix_list, [24], 'Off', '_L')
                                    set_bone_layers(little_action_list, [24], 'Off', '_L')
                                    set_bone_layers(little_mech_list, [24], 'Off', '_L')
                        # Fingers_R
                        if b.name.endswith('_R'):
                            if ('arm' in b.name):
                                if b.toggle_fingers_thumb_R:
                                    set_bone_layers(thumb_fk_list, [17, 24, 25], 'On', '_R')
                                    set_bone_layers(thumb_ctrl_list, [3, 6, 24, 25, 28, 29], 'On', '_R')
                                    set_bone_layers(thumb_toon_list, [14, 24, 25], 'On', '_R')
                                    set_bone_layers(thumb_ik_list, [19, 24, 25], 'On', '_R')
                                    set_bone_layers(thumb_str_list, [24, 25, 31], 'On', '_R')
                                    set_bone_layers(thumb_def_list, [24, 27, 29, 31], 'On', '_R')
                                    set_bone_layers(thumb_fix_list, [24, 27], 'On', '_R')
                                    set_bone_layers(thumb_action_list, [24, 28], 'On', '_R')
                                    set_bone_layers(thumb_mech_list, [26, 24], 'On', '_R')
                                else:
                                    set_bone_layers(thumb_fk_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_ctrl_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_toon_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_ik_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_str_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_def_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_fix_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_action_list, [24], 'Off', '_R')
                                    set_bone_layers(thumb_mech_list, [24], 'Off', '_R')
                                if b.toggle_fingers_index_R:
                                    set_bone_layers(index_fk_list, [17, 24, 25], 'On', '_R')
                                    set_bone_layers(index_ctrl_list, [3, 6, 24, 25, 28, 29], 'On', '_R')
                                    set_bone_layers(index_toon_list, [14, 24, 25], 'On', '_R')
                                    set_bone_layers(index_ik_list, [19, 24, 25], 'On', '_R')
                                    set_bone_layers(index_str_list, [24, 25, 31], 'On', '_R')
                                    set_bone_layers(index_def_list, [24, 27, 29, 31], 'On', '_R')
                                    set_bone_layers(index_fix_list, [24, 27], 'On', '_R')
                                    set_bone_layers(index_action_list, [24, 28], 'On', '_R')
                                    set_bone_layers(index_mech_list, [26, 24], 'On', '_R')
                                else:
                                    set_bone_layers(index_fk_list, [24], 'Off', '_R')
                                    set_bone_layers(index_ctrl_list, [24], 'Off', '_R')
                                    set_bone_layers(index_toon_list, [24], 'Off', '_R')
                                    set_bone_layers(index_ik_list, [24], 'Off', '_R')
                                    set_bone_layers(index_str_list, [24], 'Off', '_R')
                                    set_bone_layers(index_def_list, [24], 'Off', '_R')
                                    set_bone_layers(index_fix_list, [24], 'Off', '_R')
                                    set_bone_layers(index_action_list, [24], 'Off', '_R')
                                    set_bone_layers(index_mech_list, [24], 'Off', '_R')
                                if b.toggle_fingers_middle_R:
                                    set_bone_layers(middle_fk_list, [17, 24, 25], 'On', '_R')
                                    set_bone_layers(middle_ctrl_list, [3, 6, 24, 25, 28, 29], 'On', '_R')
                                    set_bone_layers(middle_toon_list, [14, 24, 25], 'On', '_R')
                                    set_bone_layers(middle_ik_list, [19, 24, 25], 'On', '_R')
                                    set_bone_layers(middle_str_list, [24, 25, 31], 'On', '_R')
                                    set_bone_layers(middle_def_list, [24, 27, 29, 31], 'On', '_R')
                                    set_bone_layers(middle_fix_list, [24, 27], 'On', '_R')
                                    set_bone_layers(middle_action_list, [24, 28], 'On', '_R')
                                    set_bone_layers(middle_mech_list, [26, 24], 'On', '_R')
                                else:
                                    set_bone_layers(middle_fk_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_ctrl_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_toon_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_ik_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_str_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_def_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_fix_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_action_list, [24], 'Off', '_R')
                                    set_bone_layers(middle_mech_list, [24], 'Off', '_R')
                                if b.toggle_fingers_ring_R:
                                    set_bone_layers(ring_fk_list, [17, 24, 25], 'On', '_R')
                                    set_bone_layers(ring_ctrl_list, [3, 6, 24, 25, 28, 29], 'On', '_R')
                                    set_bone_layers(ring_toon_list, [14, 24, 25], 'On', '_R')
                                    set_bone_layers(ring_ik_list, [19, 24, 25], 'On', '_R')
                                    set_bone_layers(ring_str_list, [24, 25, 31], 'On', '_R')
                                    set_bone_layers(ring_def_list, [24, 27, 29, 31], 'On', '_R')
                                    set_bone_layers(ring_fix_list, [24, 27], 'On', '_R')
                                    set_bone_layers(ring_action_list, [24, 28], 'On', '_R')
                                    set_bone_layers(ring_mech_list, [26, 24], 'On', '_R')
                                else:
                                    set_bone_layers(ring_fk_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_ctrl_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_toon_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_ik_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_str_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_def_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_fix_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_action_list, [24], 'Off', '_R')
                                    set_bone_layers(ring_mech_list, [24], 'Off', '_R')
                                if b.toggle_fingers_little_R:
                                    set_bone_layers(little_fk_list, [17, 24, 25], 'On', '_R')
                                    set_bone_layers(little_ctrl_list, [3, 6, 24, 25, 28, 29], 'On', '_R')
                                    set_bone_layers(little_toon_list, [14, 24, 25], 'On', '_R')
                                    set_bone_layers(little_ik_list, [19, 24, 25], 'On', '_R')
                                    set_bone_layers(little_str_list, [24, 25, 31], 'On', '_R')
                                    set_bone_layers(little_def_list, [24, 27, 29, 31], 'On', '_R')
                                    set_bone_layers(little_fix_list, [24, 27], 'On', '_R')
                                    set_bone_layers(little_action_list, [24, 28], 'On', '_R')
                                    set_bone_layers(little_mech_list, [26, 24], 'On', '_R')
                                else:
                                    set_bone_layers(little_fk_list, [24], 'Off', '_R')
                                    set_bone_layers(little_ctrl_list, [24], 'Off', '_R')
                                    set_bone_layers(little_toon_list, [24], 'Off', '_R')
                                    set_bone_layers(little_ik_list, [24], 'Off', '_R')
                                    set_bone_layers(little_str_list, [24], 'Off', '_R')
                                    set_bone_layers(little_def_list, [24], 'Off', '_R')
                                    set_bone_layers(little_fix_list, [24], 'Off', '_R')
                                    set_bone_layers(little_action_list, [24], 'Off', '_R')
                                    set_bone_layers(little_mech_list, [24], 'Off', '_R')


def toes_toggles(self, context, call_from: str, call_from_side: str):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        amr_obj = context.active_object
        arm = amr_obj.data
        p_bones = amr_obj.pose.bones

        # pack_bones_1 = [b for b in p_bones if all([not b.name.endswith("_L"), not b.name.endswith("_R")])]
        pack_bones_1 = [p_bones[finger_name+call_from_side] for finger_name in target_bones["HUMANOID"]["PROPERTIES"]]

        # if call_from == "fingers":
        #     target_key = "HAND"
        # elif call_from == "toes":
        #     target_key = "TOES"

        # print('call_from_side', call_from_side)
        # pack_bones_2 = [p_bones[finger_name+call_from_side] for finger_name in target_bones["HUMANOID"][target_key]]
        # print(pack_bones_2)

        def set_bone_layers(bone_list, layer_list, constraints_state, side):

            for bl in bone_list:
                for b in p_bones:

                    # print('b.name != str(bl + side)', b.name != str(bl + side))
                    if b.name != str(bl + side):
                        continue

                    if "toes_spread" in bl:
                        print(b.name, bl + side)

                    b.bone.layers = [i in layer_list for i in range(len(b.bone.layers))]

                    for const in b.constraints:
                        if 'REPROP' in const.name:
                            const.mute = not arm.reproportion
                        elif 'NOREP' in const.name:
                            const.mute = arm.reproportion
                        else:
                            const.mute = not constraints_state

        # zebus 0
        toe_big_fk_list = target_bones["HUMANOID"]["TOE_BIG_FK"]
        toe_big_ctrl_list = target_bones["HUMANOID"]["TOE_BIG_CRTL"]
        toe_big_toon_list = target_bones["HUMANOID"]["TOE_BIG_TOON"]
        toe_big_ik_list = target_bones["HUMANOID"]["TOE_BIG_IK"]
        toe_big_str_list = target_bones["HUMANOID"]["TOE_BIG_STR"]

        toe_big_def_list = target_bones["HUMANOID"]["TOE_BIG_DEF"]
        toe_big_fix_list = target_bones["HUMANOID"]["TOE_BIG_FIX"]
        toe_big_mech_list = target_bones["HUMANOID"]["TOE_BIG_MECH"]

        toe_index_fk_list = target_bones["HUMANOID"]["TOE_INDEX_FK"]
        toe_index_ctrl_list = target_bones["HUMANOID"]["TOE_INDEX_CTRL"]
        toe_index_toon_list = target_bones["HUMANOID"]["TOE_INDEX_TOON"]
        toe_index_ik_list = target_bones["HUMANOID"]["TOE_INDEX_IK"]
        toe_index_str_list = target_bones["HUMANOID"]["TOE_INDEX_STR"]

        toe_index_def_list = target_bones["HUMANOID"]["TOE_INDEX_DEF"]
        toe_index_fix_list = target_bones["HUMANOID"]["TOE_INDEX_FIX"]
        toe_index_mech_list = target_bones["HUMANOID"]["TOE_INDEX_MECH"]

        toe_middle_fk_list = target_bones["HUMANOID"]["TOE_MIDDLE_FK"]
        toe_middle_ctrl_list = target_bones["HUMANOID"]["TOE_MIDDLE_CTRL"]
        toe_middle_toon_list = target_bones["HUMANOID"]["TOE_MIDDLE_TOON"]
        toe_middle_ik_list = target_bones["HUMANOID"]["TOE_MIDDLE_IK"]
        toe_middle_str_list = target_bones["HUMANOID"]["TOE_MIDDLE_STR"]
        toe_middle_def_list = target_bones["HUMANOID"]["TOE_MIDDLE_DEF"]
        toe_middle_fix_list = target_bones["HUMANOID"]["TOE_MIDDLE_FIX"]
        toe_middle_mech_list = target_bones["HUMANOID"]["TOE_MIDDLE_MECH"]

        toe_fourth_fk_list = target_bones["HUMANOID"]["TOE_FOURTH_FK"]
        toe_fourth_ctrl_list = target_bones["HUMANOID"]["TOE_FOURTH_CRTL"]
        toe_fourth_toon_list = target_bones["HUMANOID"]["TOE_FOURTH_TOON"]
        toe_fourth_ik_list = target_bones["HUMANOID"]["TOE_FOURTH_IK"]
        toe_fourth_str_list = target_bones["HUMANOID"]["TOE_FOURTH_STR"]
        toe_fourth_def_list = target_bones["HUMANOID"]["TOE_FOURTH_DEF"]
        toe_fourth_fix_list = target_bones["HUMANOID"]["TOE_FOURTH_FIX"]
        toe_fourth_mech_list = target_bones["HUMANOID"]["TOE_FOURTH_MECH"]

        toe_little_fk_list = target_bones["HUMANOID"]["TOE_LITTLE_FK"]
        toe_little_ctrl_list = target_bones["HUMANOID"]["TOE_LITTLE_CTRL"]
        toe_little_toon_list = target_bones["HUMANOID"]["TOE_LITTLE_TOON"]
        toe_little_ik_list = target_bones["HUMANOID"]["TOE_LITTLE_IK"]
        toe_little_str_list = target_bones["HUMANOID"]["TOE_LITTLE_STR"]
        toe_little_def_list = target_bones["HUMANOID"]["TOE_LITTLE_DEF"]
        toe_little_fix_list = target_bones["HUMANOID"]["TOE_LITTLE_FIX"]
        toe_little_mech_list = target_bones["HUMANOID"]["TOE_LITTLE_MECH"]

        for b in pack_bones_1:

            # si no contiene leg pasamos al siguiente:
            if "leg" not in b.name:
                continue

            if b.name.endswith('_L'):
                side = '_L'
                toggle_toes_big_L = b.toggle_toes_big_L
                toggle_toes_index_L = b.toggle_toes_index_L
                toggle_toes_middle_L = b.toggle_toes_middle_L
                toggle_toes_fourth_L = b.toggle_toes_fourth_L
                toggle_toes_little_L = b.toggle_toes_little_L
            elif b.name.endswith('_R'):
                side = '_R'
                toggle_toes_big_R = b.toggle_toes_big_R
                toggle_toes_index_R = b.toggle_toes_index_R
                toggle_toes_middle_R = b.toggle_toes_middle_R
                toggle_toes_fourth_R = b.toggle_toes_fourth_R
                toggle_toes_little_R = b.toggle_toes_little_R

            # Toes_L
            if side == '_L':

                if toggle_toes_big_L:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_big_fk_list, layers_hardcoded1, toggle_toes_big_L, side)
                set_bone_layers(toe_big_ctrl_list, layers_hardcoded2, toggle_toes_big_L, side)
                set_bone_layers(toe_big_toon_list, layers_hardcoded3, toggle_toes_big_L, side)
                set_bone_layers(toe_big_ik_list, layers_hardcoded4, toggle_toes_big_L, side)
                set_bone_layers(toe_big_str_list, layers_hardcoded5, toggle_toes_big_L, side)
                set_bone_layers(toe_big_def_list, layers_hardcoded6, toggle_toes_big_L, side)
                set_bone_layers(toe_big_fix_list, layers_hardcoded7, toggle_toes_big_L, side)
                set_bone_layers(toe_big_mech_list, layers_hardcoded8, toggle_toes_big_L, side)

                if toggle_toes_index_L:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_index_fk_list, layers_hardcoded1, toggle_toes_index_L, side)
                set_bone_layers(toe_index_ctrl_list, layers_hardcoded2, toggle_toes_index_L, side)
                set_bone_layers(toe_index_toon_list, layers_hardcoded3, toggle_toes_index_L, side)
                set_bone_layers(toe_index_ik_list, layers_hardcoded4, toggle_toes_index_L, side)
                set_bone_layers(toe_index_str_list, layers_hardcoded5, toggle_toes_index_L, side)
                set_bone_layers(toe_index_def_list, layers_hardcoded6, toggle_toes_index_L, side)
                set_bone_layers(toe_index_fix_list, layers_hardcoded7, toggle_toes_index_L, side)
                set_bone_layers(toe_index_mech_list, layers_hardcoded8, toggle_toes_index_L, side)

                if toggle_toes_middle_L:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_middle_fk_list, layers_hardcoded1, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_ctrl_list, layers_hardcoded2, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_toon_list, layers_hardcoded3, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_ik_list, layers_hardcoded4, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_str_list, layers_hardcoded5, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_def_list, layers_hardcoded6, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_fix_list, layers_hardcoded7, toggle_toes_middle_L, side)
                set_bone_layers(toe_middle_mech_list, layers_hardcoded8, toggle_toes_middle_L, side)

                if toggle_toes_fourth_L:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_fourth_fk_list, layers_hardcoded1, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_ctrl_list, layers_hardcoded2, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_toon_list, layers_hardcoded3, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_ik_list, layers_hardcoded4, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_str_list, layers_hardcoded5, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_def_list, layers_hardcoded6, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_fix_list, layers_hardcoded7, toggle_toes_fourth_L, side)
                set_bone_layers(toe_fourth_mech_list, layers_hardcoded8, toggle_toes_fourth_L, side)

                if toggle_toes_little_L:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_little_fk_list, layers_hardcoded1, toggle_toes_little_L, side)
                set_bone_layers(toe_little_ctrl_list, layers_hardcoded2, toggle_toes_little_L, side)
                set_bone_layers(toe_little_toon_list, layers_hardcoded3, toggle_toes_little_L, side)
                set_bone_layers(toe_little_ik_list, layers_hardcoded4, toggle_toes_little_L, side)
                set_bone_layers(toe_little_str_list, layers_hardcoded5, toggle_toes_little_L, side)
                set_bone_layers(toe_little_def_list, layers_hardcoded6, toggle_toes_little_L, side)
                set_bone_layers(toe_little_fix_list, layers_hardcoded7, toggle_toes_little_L, side)
                set_bone_layers(toe_little_mech_list, layers_hardcoded8, toggle_toes_little_L, side)

            # Toes_R
            elif side == '_R':

                if toggle_toes_big_R:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_big_fk_list, layers_hardcoded1, toggle_toes_big_R, side)
                set_bone_layers(toe_big_ctrl_list, layers_hardcoded2, toggle_toes_big_R, side)
                set_bone_layers(toe_big_toon_list, layers_hardcoded3, toggle_toes_big_R, side)
                set_bone_layers(toe_big_ik_list, layers_hardcoded4, toggle_toes_big_R, side)
                set_bone_layers(toe_big_str_list, layers_hardcoded5, toggle_toes_big_R, side)
                set_bone_layers(toe_big_def_list, layers_hardcoded6, toggle_toes_big_R, side)
                set_bone_layers(toe_big_fix_list, layers_hardcoded7, toggle_toes_big_R, side)
                set_bone_layers(toe_big_mech_list, layers_hardcoded8, toggle_toes_big_R, side)

                if toggle_toes_index_R:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_index_fk_list, layers_hardcoded1, toggle_toes_index_R, side)
                set_bone_layers(toe_index_ctrl_list, layers_hardcoded2, toggle_toes_index_R, side)
                set_bone_layers(toe_index_toon_list, layers_hardcoded3, toggle_toes_index_R, side)
                set_bone_layers(toe_index_ik_list, layers_hardcoded4, toggle_toes_index_R, side)
                set_bone_layers(toe_index_str_list, layers_hardcoded5, toggle_toes_index_R, side)
                set_bone_layers(toe_index_def_list, layers_hardcoded6, toggle_toes_index_R, side)
                set_bone_layers(toe_index_fix_list, layers_hardcoded7, toggle_toes_index_R, side)
                set_bone_layers(toe_index_mech_list, layers_hardcoded8, toggle_toes_index_R, side)

                if toggle_toes_middle_R:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_middle_fk_list, layers_hardcoded1, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_ctrl_list, layers_hardcoded2, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_toon_list, layers_hardcoded3, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_ik_list, layers_hardcoded4, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_str_list, layers_hardcoded5, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_def_list, layers_hardcoded6, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_fix_list, layers_hardcoded7, toggle_toes_middle_R, side)
                set_bone_layers(toe_middle_mech_list, layers_hardcoded8, toggle_toes_middle_R, side)

                if toggle_toes_fourth_R:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_fourth_fk_list, layers_hardcoded1, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_ctrl_list, layers_hardcoded2, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_toon_list, layers_hardcoded3, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_ik_list, layers_hardcoded4, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_str_list, layers_hardcoded5, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_def_list, layers_hardcoded6, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_fix_list, layers_hardcoded7, toggle_toes_fourth_R, side)
                set_bone_layers(toe_fourth_mech_list, layers_hardcoded8, toggle_toes_fourth_R, side)

                if toggle_toes_little_R:
                    layers_hardcoded1 = [12, 24, 25]
                    layers_hardcoded2 = [10, 24, 25, 29]
                    layers_hardcoded3 = [14, 24, 25]
                    layers_hardcoded4 = [10, 24, 25]
                    layers_hardcoded5 = [24, 25, 31]
                    layers_hardcoded6 = [24, 27, 29, 31]
                    layers_hardcoded7 = [24, 27]
                    layers_hardcoded8 = [26, 24]
                else:
                    layers_hardcoded1 = [24]
                    layers_hardcoded2 = [24]
                    layers_hardcoded3 = [24]
                    layers_hardcoded4 = [24]
                    layers_hardcoded5 = [24]
                    layers_hardcoded6 = [24]
                    layers_hardcoded7 = [24]
                    layers_hardcoded8 = [24]

                set_bone_layers(toe_little_fk_list, layers_hardcoded1, toggle_toes_little_R, side)
                set_bone_layers(toe_little_ctrl_list, layers_hardcoded2, toggle_toes_little_R, side)
                set_bone_layers(toe_little_toon_list, layers_hardcoded3, toggle_toes_little_R, side)
                set_bone_layers(toe_little_ik_list, layers_hardcoded4, toggle_toes_little_R, side)
                set_bone_layers(toe_little_str_list, layers_hardcoded5, toggle_toes_little_R, side)
                set_bone_layers(toe_little_def_list, layers_hardcoded6, toggle_toes_little_R, side)
                set_bone_layers(toe_little_fix_list, layers_hardcoded7, toggle_toes_little_R, side)
                set_bone_layers(toe_little_mech_list, layers_hardcoded8, toggle_toes_little_R, side)


####### Rig Optimizations #######

####### Toggle Face Drivers #######


def toggle_face_drivers(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object and not context.armature:
        return False

    for prop in context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
            prop = bool(context.active_object.data.toggle_face_drivers)
            armobj = context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["mouth_corner_R"]["BACK_LIMIT_R"]',
                              'pose.bones["mouth_corner_R"]["DOWN_LIMIT_R"]',
                              'pose.bones["mouth_corner_R"]["FORW_LIMIT_R"]',
                              'pose.bones["mouth_corner_R"]["IN_LIMIT_R"]',
                              'pose.bones["mouth_corner_R"]["OUT_LIMIT_R"]',
                              'pose.bones["mouth_corner_R"]["UP_LIMIT_R"]',
                              'pose.bones["mouth_corner_L"]["UP_LIMIT_L"]',
                              'pose.bones["mouth_corner_L"]["OUT_LIMIT_L"]',
                              'pose.bones["mouth_corner_L"]["IN_LIMIT_L"]',
                              'pose.bones["mouth_corner_L"]["FORW_LIMIT_L"]',
                              'pose.bones["mouth_corner_L"]["DOWN_LIMIT_L"]',
                              'pose.bones["mouth_corner_L"]["BACK_LIMIT_L"]',
                              'pose.bones["mouth_ctrl"]["OUT_LIMIT"]',
                              'pose.bones["mouth_ctrl"]["IN_LIMIT"]',
                              'pose.bones["mouth_ctrl"]["SMILE_LIMIT"]',
                              'pose.bones["mouth_ctrl"]["JAW_ROTATION"]',
                              'pose.bones["maxi"]["JAW_UP_LIMIT"]',
                              'pose.bones["maxi"]["JAW_DOWN_LIMIT"]',
                              'pose.bones["cheek_ctrl_R"]["CHEEK_DOWN_LIMIT_R"]',
                              'pose.bones["cheek_ctrl_L"]["CHEEK_DOWN_LIMIT_L"]',
                              'pose.bones["cheek_ctrl_R"]["CHEEK_UP_LIMIT_R"]',
                              'pose.bones["cheek_ctrl_L"]["CHEEK_UP_LIMIT_L"]',
                              'pose.bones["cheek_ctrl_R"]["AUTO_SMILE_R"]',
                              'pose.bones["cheek_ctrl_L"]["AUTO_SMILE_L"]',
                              'pose.bones["eyelid_low_ctrl_L"]["AUTO_CHEEK_L"]',
                              'pose.bones["eyelid_low_ctrl_R"]["AUTO_CHEEK_R"]',
                              'pose.bones["eyelid_low_ctrl_R"]["EYELID_DOWN_LIMIT_R"]',
                              'pose.bones["eyelid_low_ctrl_L"]["EYELID_DOWN_LIMIT_L"]',
                              'pose.bones["eyelid_low_ctrl_R"]["EYELID_UP_LIMIT_R"]',
                              'pose.bones["eyelid_low_ctrl_L"]["EYELID_UP_LIMIT_L"]',
                              'pose.bones["eyelid_up_ctrl_R"]["EYELID_DOWN_LIMIT_R"]',
                              'pose.bones["eyelid_up_ctrl_L"]["EYELID_DOWN_LIMIT_L"]',
                              'pose.bones["eyelid_up_ctrl_R"]["EYELID_UP_LIMIT_R"]',
                              'pose.bones["eyelid_up_ctrl_L"]["EYELID_UP_LIMIT_L"]',
                              'pose.bones["mouth_frown_ctrl_R"]["DOWN_LIMIT_R"]',
                              'pose.bones["mouth_frown_ctrl_L"]["DOWN_LIMIT_L"]',
                              'pose.bones["nose_frown_ctrl_R"]["UP_LIMIT_R"]',
                              'pose.bones["nose_frown_ctrl_L"]["UP_LIMIT_L"]',
                              'pose.bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"]',
                              'pose.bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"]',
                              'pose.bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"]',
                              'pose.bones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"]',
                              'pose.bones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"]',
                              'pose.bones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"]',
                              'pose.bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"]',
                              'pose.bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"]',
                              'pose.bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"]',
                              'pose.bones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"]',
                              'pose.bones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"]',
                              'pose.bones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"]',
                              'pose.bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"]',
                              'pose.bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"]',
                              'pose.bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"]',
                              'pose.bones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"]',
                              'pose.bones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"]',
                              'pose.bones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"]',
                              'pose.bones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_X_R"]',
                              'pose.bones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_Y_R"]',
                              'pose.bones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_Z_R"]',
                              'pose.bones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_X_R"]',
                              'pose.bones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_Y_R"]',
                              'pose.bones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_Z_R"]',
                              'pose.bones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_X_R"]',
                              'pose.bones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_Y_R"]',
                              'pose.bones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_Z_R"]',
                              'pose.bones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_X_R"]',
                              'pose.bones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_Y_R"]',
                              'pose.bones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_Z_R"]',
                              'pose.bones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_X_R"]',
                              'pose.bones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_Y_R"]',
                              'pose.bones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_Z_R"]',
                              'pose.bones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_X_R"]',
                              'pose.bones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_Y_R"]',
                              'pose.bones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_Z_R"]',
                              'pose.bones["mouth_corner_R"]["ACTION_BACK_TOGGLE_R"]',
                              'pose.bones["mouth_corner_L"]["ACTION_BACK_TOGGLE_L"]',
                              'pose.bones["mouth_corner_R"]["ACTION_DOWN_TOGGLE_R"]',
                              'pose.bones["mouth_corner_L"]["ACTION_DOWN_TOGGLE_L"]',
                              'pose.bones["mouth_corner_R"]["ACTION_FORW_TOGGLE_R"]',
                              'pose.bones["mouth_corner_L"]["ACTION_FORW_TOGGLE_L"]',
                              'pose.bones["mouth_corner_R"]["ACTION_IN_TOGGLE_R"]',
                              'pose.bones["mouth_corner_L"]["ACTION_IN_TOGGLE_L"]',
                              'pose.bones["mouth_corner_R"]["ACTION_OUT_TOGGLE_R"]',
                              'pose.bones["mouth_corner_L"]["ACTION_OUT_TOGGLE_L"]',
                              'pose.bones["mouth_corner_R"]["ACTION_UP_TOGGLE_R"]',
                              'pose.bones["mouth_corner_L"]["ACTION_UP_TOGGLE_L"]',
                              'pose.bones["maxi"]["ACTION_UP_DOWN_TOGGLE"]',
                              'pose.bones["cheek_ctrl_R"]["ACTION_CHEEK_TOGGLE_R"]',
                              'pose.bones["cheek_ctrl_L"]["ACTION_CHEEK_TOGGLE_L"]',
                              'pose.bones["mouth_corner_L"]["AUTO_BACK_L"]',
                              'pose.bones["mouth_corner_R"]["AUTO_BACK_R"]']

            for C in drivers:
                for vars in C.driver.variables:
                    for T in vars.targets:
                        for D in data_path_list:
                            if D in T.data_path:
                                if prop == 1:
                                    C.mute = False
                                else:
                                    C.mute = True

####### Toggle Flex Drivers (Legacy Rig)#######


def toggle_flex_drivers(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object and not context.armature:
        return False

    for prop in context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
            prop = bool(context.active_object.data.toggle_flex_drivers)
            armobj = context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["properties_head"]["flex_head_scale"]',
                              'pose.bones["properties_head"]["flex_neck_length"]',
                              'pose.bones["properties_head"]["flex_neck_width"]',
                              'pose.bones["properties_arm_R"]["flex_arm_length_R"]',
                              'pose.bones["properties_arm_R"]["flex_arm_uniform_scale_R"]',
                              'pose.bones["properties_arm_R"]["flex_arm_width_R"]',
                              'pose.bones["properties_arm_R"]["flex_forearm_length_R"]',
                              'pose.bones["properties_arm_R"]["flex_forearm_width_R"]',
                              'pose.bones["properties_arm_R"]["flex_hand_scale_R"]',
                              'pose.bones["properties_torso"]["flex_torso_height"]',
                              'pose.bones["properties_torso"]["flex_torso_scale"]',
                              'pose.bones["properties_torso"]["flex_chest_width"]',
                              'pose.bones["properties_torso"]["flex_ribs_width"]',
                              'pose.bones["properties_torso"]["flex_waist_width"]',
                              'pose.bones["properties_torso"]["flex_pelvis_width"]',
                              'pose.bones["properties_arm_L"]["flex_arm_length_L"]',
                              'pose.bones["properties_arm_L"]["flex_arm_uniform_scale_L"]',
                              'pose.bones["properties_arm_L"]["flex_arm_width_L"]',
                              'pose.bones["properties_arm_L"]["flex_forearm_length_L"]',
                              'pose.bones["properties_arm_L"]["flex_forearm_width_L"]',
                              'pose.bones["properties_arm_L"]["flex_hand_scale_L"]',
                              'pose.bones["properties_leg_R"]["flex_leg_uniform_scale_R"]',
                              'pose.bones["properties_leg_R"]["flex_thigh_length_R"]',
                              'pose.bones["properties_leg_R"]["flex_thigh_width_R"]',
                              'pose.bones["properties_leg_R"]["flex_shin_length_R"]',
                              'pose.bones["properties_leg_R"]["flex_shin_width_R"]',
                              'pose.bones["properties_leg_R"]["flex_foot_scale_R"]',
                              'pose.bones["properties_leg_R"]["flex_foot_loc_R"]',
                              'pose.bones["properties_leg_L"]["flex_leg_uniform_scale_L"]',
                              'pose.bones["properties_leg_L"]["flex_thigh_length_L"]',
                              'pose.bones["properties_leg_L"]["flex_thigh_width_L"]',
                              'pose.bones["properties_leg_L"]["flex_shin_length_L"]',
                              'pose.bones["properties_leg_L"]["flex_shin_width_L"]',
                              'pose.bones["properties_leg_L"]["flex_foot_scale_L"]',
                              'pose.bones["properties_leg_L"]["flex_foot_loc_L"]']

            for C in drivers:
                for vars in C.driver.variables:
                    for T in vars.targets:
                        for D in data_path_list:
                            if D in T.data_path:
                                if prop == 1:
                                    C.mute = False
                                else:
                                    C.mute = True

####### Toggle Dynamic Shaping Drivers #######


def toggle_dynamic_drivers(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object and not context.armature:
        return False

    for prop in context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
            prop = bool(context.active_object.data.toggle_dynamic_drivers)
            armobj = context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["properties_head"]["dynamic_head_scale"]',
                              'pose.bones["properties_head"]["dynamic_neck_length"]',
                              'pose.bones["properties_head"]["dynamic_neck_width"]',
                              'pose.bones["properties_arm_R"]["dynamic_arm_length_R"]',
                              'pose.bones["properties_arm_R"]["dynamic_arm_uniform_scale_R"]',
                              'pose.bones["properties_arm_R"]["dynamic_arm_width_R"]',
                              'pose.bones["properties_arm_R"]["dynamic_forearm_length_R"]',
                              'pose.bones["properties_arm_R"]["dynamic_forearm_width_R"]',
                              'pose.bones["properties_arm_R"]["dynamic_hand_scale_R"]',
                              'pose.bones["properties_torso"]["dynamic_torso_height"]',
                              'pose.bones["properties_torso"]["dynamic_torso_scale"]',
                              'pose.bones["properties_torso"]["dynamic_chest_width"]',
                              'pose.bones["properties_torso"]["dynamic_ribs_width"]',
                              'pose.bones["properties_torso"]["dynamic_waist_width"]',
                              'pose.bones["properties_torso"]["dynamic_pelvis_width"]',
                              'pose.bones["properties_arm_L"]["dynamic_arm_length_L"]',
                              'pose.bones["properties_arm_L"]["dynamic_arm_uniform_scale_L"]',
                              'pose.bones["properties_arm_L"]["dynamic_arm_width_L"]',
                              'pose.bones["properties_arm_L"]["dynamic_forearm_length_L"]',
                              'pose.bones["properties_arm_L"]["dynamic_forearm_width_L"]',
                              'pose.bones["properties_arm_L"]["dynamic_hand_scale_L"]',
                              'pose.bones["properties_leg_R"]["dynamic_leg_uniform_scale_R"]',
                              'pose.bones["properties_leg_R"]["dynamic_thigh_length_R"]',
                              'pose.bones["properties_leg_R"]["dynamic_thigh_width_R"]',
                              'pose.bones["properties_leg_R"]["dynamic_shin_length_R"]',
                              'pose.bones["properties_leg_R"]["dynamic_shin_width_R"]',
                              'pose.bones["properties_leg_R"]["dynamic_foot_scale_R"]',
                              'pose.bones["properties_leg_R"]["dynamic_foot_loc_R"]',
                              'pose.bones["properties_leg_L"]["dynamic_leg_uniform_scale_L"]',
                              'pose.bones["properties_leg_L"]["dynamic_thigh_length_L"]',
                              'pose.bones["properties_leg_L"]["dynamic_thigh_width_L"]',
                              'pose.bones["properties_leg_L"]["dynamic_shin_length_L"]',
                              'pose.bones["properties_leg_L"]["dynamic_shin_width_L"]',
                              'pose.bones["properties_leg_L"]["dynamic_foot_scale_L"]',
                              'pose.bones["properties_leg_L"]["dynamic_foot_loc_L"]']

            for C in drivers:
                for vars in C.driver.variables:
                    for T in vars.targets:
                        for D in data_path_list:
                            if D in T.data_path:
                                if prop == 1:
                                    C.mute = False
                                else:
                                    C.mute = True


####### Toggle Body Drivers #######

def toggle_body_drivers(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object and not context.armature:
        return False

    for prop in context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
            prop = bool(context.active_object.data.toggle_body_drivers)
            armobj = context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["forearm_ik_R"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
                              'pose.bones["forearm_ik_L"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
                              'pose.bones["shin_ik_R"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
                              'pose.bones["shin_ik_L"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
                              'pose.bones["properties_arm_R"]["realistic_joints_wrist_R"]',
                              'pose.bones["properties_arm_L"]["realistic_joints_hand_L"]',
                              'pose.bones["properties_arm_R"]["realistic_joints_hand_R"]',
                              'pose.bones["properties_arm_L"]["realistic_joints_wrist_L"]',
                              'pose.bones["properties_arm_R"]["realistic_joints_elbow_R"]',
                              'pose.bones["properties_arm_L"]["realistic_joints_elbow_L"]',
                              'pose.bones["properties_leg_R"]["realistic_joints_knee_R"]',
                              'pose.bones["properties_leg_L"]["realistic_joints_knee_L"]',
                              'pose.bones["properties_leg_R"]["realistic_joints_ankle_R"]',
                              'pose.bones["properties_leg_L"]["realistic_joints_foot_L"]',
                              'pose.bones["properties_leg_R"]["realistic_joints_foot_R"]',
                              'pose.bones["properties_leg_L"]["realistic_joints_ankle_L"]',
                              'pose.bones["foot_roll_ctrl_R"]["FOOT_ROLL_AMPLITUD_R"]',
                              'pose.bones["foot_roll_ctrl_L"]["FOOT_ROLL_AMPLITUD_L"]',
                              'pose.bones["foot_roll_ctrl_R"]["TOE_1_ROLL_START_R"]',
                              'pose.bones["foot_roll_ctrl_L"]["TOE_1_ROLL_START_L"]',
                              'pose.bones["foot_roll_ctrl_R"]["TOE_2_ROLL_START_R"]',
                              'pose.bones["foot_roll_ctrl_L"]["TOE_2_ROLL_START_L"]',
                              'pose.bones["neck_1_fk"]["fk_follow_main"]',
                              'pose.bones["neck_2_fk"]["fk_follow_main"]',
                              'pose.bones["neck_3_fk"]["fk_follow_main"]',
                              'pose.bones["spine_1_fk"]["fk_follow_main"]',
                              'pose.bones["spine_2_fk"]["fk_follow_main"]',
                              'pose.bones["spine_3_fk"]["fk_follow_main"]',
                              'pose.bones["spine_2_inv"]["fk_follow_main"]',
                              'pose.bones["spine_1_inv"]["fk_follow_main"]',
                              'pose.bones["pelvis_inv"]["fk_follow_main"]']

            for C in drivers:
                for vars in C.driver.variables:
                    for T in vars.targets:
                        for D in data_path_list:
                            if D in T.data_path:
                                if prop == 1:
                                    C.mute = False
                                else:
                                    C.mute = True

####### Pole Toggles #######


def pole_toggles(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                p_bones = context.active_object.pose.bones
                arm = context.active_object.data

                for b in p_bones:
                    # Arm Pole L
                    if b.name == 'properties_arm_L':
                        prop_pole = int(b.toggle_arm_ik_pole_L)
                        if prop_pole == 1:
                            for bone in arm.bones:
                                if bone.name == 'elbow_pole_L':
                                    bone.layers[16] = 1
                                if bone.name == 'elbow_line_L':
                                    bone.layers[16] = 1
                        else:
                            for bone in arm.bones:
                                if bone.name == 'elbow_pole_L':
                                    bone.layers[16] = 0
                                if bone.name == 'elbow_line_L':
                                    bone.layers[16] = 0
                    # Arm Pole R
                    if b.name == 'properties_arm_R':
                        prop_pole = int(b.toggle_arm_ik_pole_R)
                        if prop_pole == 1:
                            for bone in arm.bones:
                                if bone.name == 'elbow_pole_R':
                                    bone.layers[6] = 1
                                if bone.name == 'elbow_line_R':
                                    bone.layers[6] = 1
                        else:
                            for bone in arm.bones:
                                if bone.name == 'elbow_pole_R':
                                    bone.layers[6] = 0
                                if bone.name == 'elbow_line_R':
                                    bone.layers[6] = 0

                    # Leg Pole L
                    if b.name == 'properties_leg_L':
                        prop_pole = int(b.toggle_leg_ik_pole_L)
                        if prop_pole == 1:
                            for bone in arm.bones:
                                if bone.name == 'knee_pole_L':
                                    bone.layers[9] = 1
                                if bone.name == 'knee_line_L':
                                    bone.layers[9] = 1
                        else:
                            for bone in arm.bones:
                                if bone.name == 'knee_pole_L':
                                    bone.layers[9] = 0
                                if bone.name == 'knee_line_L':
                                    bone.layers[9] = 0

                    # Leg Pole R
                    if b.name == 'properties_leg_R':
                        prop_pole = int(b.toggle_leg_ik_pole_R)
                        if prop_pole == 1:
                            for bone in arm.bones:
                                if bone.name == 'knee_pole_R':
                                    bone.layers[23] = 1
                                if bone.name == 'knee_line_R':
                                    bone.layers[23] = 1
                        else:
                            for bone in arm.bones:
                                if bone.name == 'knee_pole_R':
                                    bone.layers[23] = 0
                                if bone.name == 'knee_line_R':
                                    bone.layers[23] = 0

#################################### BLENRIG SET CONSTRAINTS VALUES FUNCTIONS ####################################################

################### MAIN FUNCTIONS ##################################

# Function for setting values on Action Constraints


def Set_Movement_Ranges_Actions(b_name, prop_name, C_name, min_factor, max_factor):

    armobj = bpy.context.active_object
    arm = bpy.context.active_object.data
    p_bones = bpy.context.active_object.pose.bones
    constraint_value = []

    for b in p_bones:
        if b.name == b_name:
            for cust_prop in b.items():
                if cust_prop[0] == prop_name:
                    constraint_value = []
                    constraint_value.append(cust_prop[1])
                    for b in p_bones:
                        for C in b.constraints:
                            if C.type == 'ACTION':
                                if C.name == C_name:
                                    C.min = constraint_value[0] * min_factor
                                    C.max = constraint_value[0] * max_factor

# Functions for setting values on Realistic Joints Transform Constraints


def Set_RJ_Transforms_Limbs(b_name, prop_name, C_name, x_loc_factor, z_loc_factor, x_rot_factor, z_rot_factor):

    if bpy.context.active_object.type == 'ARMATURE':
        armobj = bpy.context.active_object
    else:
        armobj = bpy.context.scene.blenrig_guide.arm_obj
    p_bones = armobj.pose.bones
    constraint_value = []

    for b in p_bones:
        if b.name == b_name:
            for cust_prop in b.items():
                if cust_prop[0] == prop_name:
                    constraint_value = []
                    constraint_value.append(cust_prop[1])
                    for b in p_bones:
                        for C in b.constraints:
                            if C.type == 'TRANSFORM':
                                if C.name == C_name:
                                    C.to_max_x = constraint_value[0] * x_loc_factor
                                    C.to_max_z = constraint_value[0] * z_loc_factor
                                    C.to_max_x_rot = radians(constraint_value[0] * x_rot_factor)
                                    C.to_max_z_rot = radians(constraint_value[0] * z_rot_factor)


def Set_RJ_Transforms_Fing_Toes(b_name, prop_name, C_name, z_loc_factor, x_rot_factor, Loc_Array_n, Rot_Array_n):

    if bpy.context.active_object.type == 'ARMATURE':
        armobj = bpy.context.active_object
    else:
        armobj = bpy.context.scene.blenrig_guide.arm_obj
    p_bones = armobj.pose.bones
    constraint_value = []

    for b in p_bones:
        if b.name == b_name:
            for cust_prop in b.items():
                if cust_prop[0] == prop_name:
                    constraint_value = []
                    constraint_value.append(cust_prop[1][0])
                    constraint_value.append(cust_prop[1][1])
                    constraint_value.append(cust_prop[1][2])
                    for b in p_bones:
                        for C in b.constraints:
                            if C.type == 'TRANSFORM':
                                if C.name == C_name:
                                    C.to_max_z = constraint_value[Loc_Array_n] * z_loc_factor
                                    C.to_max_x_rot = radians(constraint_value[Rot_Array_n] * x_rot_factor)

# Function for setting values on Volume Variation Constraints


def Set_Volume_Variation_Stretch_To(b_name, prop_name, C_name):

    armobj = bpy.context.active_object
    arm = bpy.context.active_object.data
    p_bones = bpy.context.active_object.pose.bones
    constraint_value = []

    for b in p_bones:
        if b.name == b_name:
            for cust_prop in b.items():
                if cust_prop[0] == prop_name:
                    constraint_value = []
                    constraint_value.append(cust_prop[1])
                    for b in p_bones:
                        for C in b.constraints:
                            if C.type == 'STRETCH_TO':
                                if C.name == C_name:
                                    C.bulge = constraint_value[0]

# Functions for setting values on Volume Preservation bones Constraints


def Set_VP_Transforms(b_name, prop_name, C_name, to_mapping, factor):

    if bpy.context.active_object.type == 'ARMATURE':
        armobj = bpy.context.active_object
    else:
        armobj = bpy.context.scene.blenrig_guide.arm_obj
    p_bones = armobj.pose.bones
    constraint_value = []

    for b in p_bones:
        if b.name == b_name:
            for cust_prop in b.items():
                if cust_prop[0] == prop_name:
                    constraint_value = []
                    constraint_value.append(cust_prop[1])
                    for b in p_bones:
                        for C in b.constraints:
                            if C.type == 'TRANSFORM':
                                if C.name == C_name:
                                    if to_mapping == 'to_max_x':
                                        C.to_max_x = constraint_value[0] * factor
                                    if to_mapping == 'to_max_y':
                                        C.to_max_y = constraint_value[0] * factor
                                    if to_mapping == 'to_max_z':
                                        C.to_max_z = constraint_value[0] * factor
                                    if to_mapping == 'to_min_x':
                                        C.to_min_x = constraint_value[0] * factor
                                    if to_mapping == 'to_min_y':
                                        C.to_min_y = constraint_value[0] * factor
                                    if to_mapping == 'to_min_z':
                                        C.to_min_z = constraint_value[0] * factor

######## SET FUNCTIONS ###########################################

### FACIAL CONSTRAINTS ####

# EYELIDS


def set_eyelids(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                # Eyelid Up L
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_L', 'EYELID_UP_LIMIT_L', 'Eyelid_Upper_Up_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_L', 'EYELID_DOWN_LIMIT_L',
                                            'Eyelid_Upper_Down_L_NOREP', 0, -1)
                # Eyelid Up R
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_R', 'EYELID_UP_LIMIT_R', 'Eyelid_Upper_Up_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_R', 'EYELID_DOWN_LIMIT_R',
                                            'Eyelid_Upper_Down_R_NOREP', 0, -1)
                # Eyelid Low L
                Set_Movement_Ranges_Actions('eyelid_low_ctrl_L', 'EYELID_UP_LIMIT_L', 'Eyelid_Lower_Up_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('eyelid_low_ctrl_L', 'EYELID_DOWN_LIMIT_L',
                                            'Eyelid_Lower_Down_L_NOREP', 0, -1)
                # Eyelid Low R
                Set_Movement_Ranges_Actions('eyelid_low_ctrl_R', 'EYELID_UP_LIMIT_R', 'Eyelid_Lower_Up_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('eyelid_low_ctrl_R', 'EYELID_DOWN_LIMIT_R',
                                            'Eyelid_Lower_Down_R_NOREP', 0, -1)
                # Eyelid Sides L
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_L', 'EYELID_OUT_LIMIT_L', 'Eyelid_Out_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_L', 'EYELID_IN_LIMIT_L', 'Eyelid_In_L_NOREP', 0, -1)
                # Eyelid Sides R
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_R', 'EYELID_OUT_LIMIT_R', 'Eyelid_Out_R_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('eyelid_up_ctrl_R', 'EYELID_IN_LIMIT_R', 'Eyelid_In_R_NOREP', 0, 1)
                return {"FINISHED"}

# FROWNS


def set_frowns(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                # Nose Frown L
                Set_Movement_Ranges_Actions('nose_frown_ctrl_L', 'FROWN_LIMIT_L', 'Nose_Frown_L_NOREP', -1, 1)
                # Mouth Frown L
                Set_Movement_Ranges_Actions('mouth_frown_ctrl_L', 'FROWN_LIMIT_L', 'Mouth_Frown_L_NOREP', 0, -1)
                # Nose Frown R
                Set_Movement_Ranges_Actions('nose_frown_ctrl_R', 'FROWN_LIMIT_R', 'Nose_Frown_R_NOREP', -1, 1)
                # Mouth Frown R
                Set_Movement_Ranges_Actions('mouth_frown_ctrl_R', 'FROWN_LIMIT_R', 'Mouth_Frown_R_NOREP', 0, -1)
                # Chin Frown
                Set_Movement_Ranges_Actions('chin_frown_ctrl', 'FROWN_LIMIT', 'Chin_Frown_NOREP', -1, 1)
                return {"FINISHED"}

# CHEEKS


def set_cheeks(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                # Cheeks L
                Set_Movement_Ranges_Actions('cheek_ctrl_L', 'CHEEK_UP_LIMIT_L', 'Cheek_Up_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('cheek_ctrl_L', 'CHEEK_DOWN_LIMIT_L', 'Cheek_Down_L_NOREP', 0, -1)
                # Cheeks R
                Set_Movement_Ranges_Actions('cheek_ctrl_R', 'CHEEK_UP_LIMIT_R', 'Cheek_Up_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('cheek_ctrl_R', 'CHEEK_DOWN_LIMIT_R', 'Cheek_Down_R_NOREP', 0, -1)
                return {"FINISHED"}

# MOUTH CORNERS


def set_mouth_corners(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                # Mouth Corner L
                Set_Movement_Ranges_Actions('mouth_corner_L', 'IN_LIMIT_L', 'Mouth_Corner_In_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'IN_LIMIT_L', 'U_Up_Narrow_Corrective_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'OUT_LIMIT_L', 'Mouth_Corner_Out_L_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'UP_LIMIT_L', 'Mouth_Corner_Up_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'UP_LIMIT_L',
                                            'Mouth_Corner_Up_Out_Corrective_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'DOWN_LIMIT_L', 'Mouth_Corner_Down_L_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'DOWN_LIMIT_L',
                                            'Mouth_Corner_Down_Out_Corrective_L_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'FORW_LIMIT_L', 'Mouth_Corner_Forw_L_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_L', 'BACK_LIMIT_L', 'Mouth_Corner_Back_L_NOREP', 0, -1)
                # Mouth Corner R
                Set_Movement_Ranges_Actions('mouth_corner_R', 'IN_LIMIT_R', 'Mouth_Corner_In_R_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'IN_LIMIT_R', 'U_Up_Narrow_Corrective_R_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'OUT_LIMIT_R', 'Mouth_Corner_Out_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'OUT_LIMIT_R',
                                            'Mouth_Corner_Up_Out_Corrective_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'UP_LIMIT_R', 'Mouth_Corner_Up_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'UP_LIMIT_R',
                                            'Mouth_Corner_Up_Out_Corrective_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'DOWN_LIMIT_R', 'Mouth_Corner_Down_R_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'DOWN_LIMIT_R',
                                            'Mouth_Corner_Down_Out_Corrective_R_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'FORW_LIMIT_R', 'Mouth_Corner_Forw_R_NOREP', 0, 1)
                Set_Movement_Ranges_Actions('mouth_corner_R', 'BACK_LIMIT_R', 'Mouth_Corner_Back_R_NOREP', 0, -1)
                return {"FINISHED"}

# MOUTH CTRL


def set_mouth_ctrl(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                # Mouth Ctrl
                # Set_Movement_Ranges_Actions('mouth_ctrl', 'IN_LIMIT', 'Mouth_Corner_In_L_NOREP', 0, 1)
                # Set_Movement_Ranges_Actions('mouth_ctrl', 'OUT_LIMIT', 'Mouth_Corner_Out_L_NOREP', 0, -1)
                # Set_Movement_Ranges_Actions('mouth_ctrl', 'SMILE_LIMIT', 'Mouth_Corner_Up_L_NOREP', 0, 1)
                # Set_Movement_Ranges_Actions('mouth_ctrl', 'JAW_ROTATION', 'Mouth_Corner_Down_L_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('mouth_ctrl', 'U_M_CTRL_LIMIT', 'U_O_M_Up_NOREP', -1, 1)
                Set_Movement_Ranges_Actions('mouth_ctrl', 'U_M_CTRL_LIMIT', 'U_O_M_Low_NOREP', -1, 1)
                # Jaw
                Set_Movement_Ranges_Actions('maxi', 'JAW_DOWN_LIMIT', 'Maxi_Down_NOREP', 0, -1)
                Set_Movement_Ranges_Actions('maxi', 'JAW_UP_LIMIT', 'Maxi_Up_NOREP', 0, 1)
                return {"FINISHED"}

### REALISTIC JOINTS CONSTRAINTS ####


def set_rj_transforms(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    # if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
    #     for prop in context.active_object.data.items():
    #         if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

    # Arms L
    Set_RJ_Transforms_Limbs('properties_arm_L', 'realistic_joints_elbow_loc_L', 'Elbow_RJ_Loc_L_NOREP', 0, 1, 0, 0)
    Set_RJ_Transforms_Limbs('properties_arm_L', 'realistic_joints_elbow_rot_L', 'Elbow_RJ_Rot_L_NOREP', 0, 0, -1, 0)
    Set_RJ_Transforms_Limbs('properties_arm_L', 'realistic_joints_wrist_rot_L', 'Wrist_RJ_Rot_L_NOREP', 0, 0, -1, 1)
    # Arms R
    Set_RJ_Transforms_Limbs('properties_arm_R', 'realistic_joints_elbow_loc_R', 'Elbow_RJ_Loc_R_NOREP', 0, 1, 0, 0)
    Set_RJ_Transforms_Limbs('properties_arm_R', 'realistic_joints_elbow_rot_R', 'Elbow_RJ_Rot_R_NOREP', 0, 0, -1, 0)
    Set_RJ_Transforms_Limbs('properties_arm_R', 'realistic_joints_wrist_rot_R', 'Wrist_RJ_Rot_R_NOREP', 0, 0, 1, -1)
    # Legs L
    Set_RJ_Transforms_Limbs('properties_leg_L', 'realistic_joints_knee_loc_L', 'Knee_RJ_Loc_L_NOREP', 0, 1, 0, 0)
    Set_RJ_Transforms_Limbs('properties_leg_L', 'realistic_joints_knee_rot_L', 'Knee_RJ_Rot_L_NOREP', 0, 0, -1, 0)
    Set_RJ_Transforms_Limbs('properties_leg_L', 'realistic_joints_ankle_rot_L', 'Ankle_RJ_Rot_L_NOREP', 0, 0, -1, -1)
    # Legs R
    Set_RJ_Transforms_Limbs('properties_leg_R', 'realistic_joints_knee_loc_R', 'Knee_RJ_Loc_R_NOREP', 0, 1, 0, 0)
    Set_RJ_Transforms_Limbs('properties_leg_R', 'realistic_joints_knee_rot_R', 'Knee_RJ_Rot_R_NOREP', 0, 0, -1, 0)
    Set_RJ_Transforms_Limbs('properties_leg_R', 'realistic_joints_ankle_rot_R', 'Ankle_RJ_Rot_R_NOREP', 0, 0, -1, -1)
    # Fingers L
    Set_RJ_Transforms_Fing_Toes('properties_arm_L', 'realistic_joints_fingers_rot_L',
                                'Fing_1_RJ_Rot_L_NOREP', 0, -1, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_arm_L', 'realistic_joints_fingers_rot_L',
                                'Fing_2_RJ_Rot_L_NOREP', 0, -1, 0, 1)
    Set_RJ_Transforms_Fing_Toes('properties_arm_L', 'realistic_joints_fingers_rot_L',
                                'Fing_3_RJ_Rot_L_NOREP', 0, -1, 0, 2)
    Set_RJ_Transforms_Fing_Toes('properties_arm_L', 'realistic_joints_fingers_loc_L',
                                'Fing_2_RJ_Loc_L_NOREP', 1, 0, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_arm_L', 'realistic_joints_fingers_loc_L',
                                'Fing_3_RJ_Loc_L_NOREP', 1, 0, 1, 0)
    Set_RJ_Transforms_Fing_Toes('properties_arm_L', 'realistic_joints_fingers_loc_L',
                                'Fing_4_RJ_Loc_L_NOREP', 1, 0, 2, 0)
    # Fingers R
    Set_RJ_Transforms_Fing_Toes('properties_arm_R', 'realistic_joints_fingers_rot_R',
                                'Fing_1_RJ_Rot_R_NOREP', 0, -1, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_arm_R', 'realistic_joints_fingers_rot_R',
                                'Fing_2_RJ_Rot_R_NOREP', 0, -1, 0, 1)
    Set_RJ_Transforms_Fing_Toes('properties_arm_R', 'realistic_joints_fingers_rot_R',
                                'Fing_3_RJ_Rot_R_NOREP', 0, -1, 0, 2)
    Set_RJ_Transforms_Fing_Toes('properties_arm_R', 'realistic_joints_fingers_loc_R',
                                'Fing_2_RJ_Loc_R_NOREP', 1, 0, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_arm_R', 'realistic_joints_fingers_loc_R',
                                'Fing_3_RJ_Loc_R_NOREP', 1, 0, 1, 0)
    Set_RJ_Transforms_Fing_Toes('properties_arm_R', 'realistic_joints_fingers_loc_R',
                                'Fing_4_RJ_Loc_R_NOREP', 1, 0, 2, 0)
    # Toes L
    Set_RJ_Transforms_Fing_Toes('properties_leg_L', 'realistic_joints_toes_rot_L', 'Toes_1_RJ_Rot_L_NOREP', 0, -1, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_leg_L', 'realistic_joints_toes_rot_L', 'Toes_2_RJ_Rot_L_NOREP', 0, -1, 0, 1)
    Set_RJ_Transforms_Fing_Toes('properties_leg_L', 'realistic_joints_toes_rot_L', 'Toes_3_RJ_Rot_L_NOREP', 0, -1, 0, 2)
    Set_RJ_Transforms_Fing_Toes('properties_leg_L', 'realistic_joints_toes_loc_L', 'Toes_2_RJ_Loc_L_NOREP', 1, 0, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_leg_L', 'realistic_joints_toes_loc_L', 'Toes_3_RJ_Loc_L_NOREP', 1, 0, 1, 0)
    Set_RJ_Transforms_Fing_Toes('properties_leg_L', 'realistic_joints_toes_loc_L', 'Toes_4_RJ_Loc_L_NOREP', 1, 0, 2, 0)
    # Toes R
    Set_RJ_Transforms_Fing_Toes('properties_leg_R', 'realistic_joints_toes_rot_R', 'Toes_1_RJ_Rot_R_NOREP', 0, -1, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_leg_R', 'realistic_joints_toes_rot_R', 'Toes_2_RJ_Rot_R_NOREP', 0, -1, 0, 1)
    Set_RJ_Transforms_Fing_Toes('properties_leg_R', 'realistic_joints_toes_rot_R', 'Toes_3_RJ_Rot_R_NOREP', 0, -1, 0, 2)
    Set_RJ_Transforms_Fing_Toes('properties_leg_R', 'realistic_joints_toes_loc_R', 'Toes_2_RJ_Loc_R_NOREP', 1, 0, 0, 0)
    Set_RJ_Transforms_Fing_Toes('properties_leg_R', 'realistic_joints_toes_loc_R', 'Toes_3_RJ_Loc_R_NOREP', 1, 0, 1, 0)
    Set_RJ_Transforms_Fing_Toes('properties_leg_R', 'realistic_joints_toes_loc_R', 'Toes_4_RJ_Loc_R_NOREP', 1, 0, 2, 0)
    return {"FINISHED"}

### VOLUME VARIATION CONSTRAINTS ####


def set_vol_variation(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                # Arms L
                Set_Volume_Variation_Stretch_To(
                    'properties_arm_L', 'volume_variation_arm_L', 'Vol_Var_Arm_L_Stretch_To')
                Set_Volume_Variation_Stretch_To(
                    'properties_arm_L', 'volume_variation_fingers_L', 'Vol_Var_Hand_L_Stretch_To')
                # Arms R
                Set_Volume_Variation_Stretch_To(
                    'properties_arm_R', 'volume_variation_arm_R', 'Vol_Var_Arm_R_Stretch_To')
                Set_Volume_Variation_Stretch_To(
                    'properties_arm_R', 'volume_variation_fingers_R', 'Vol_Var_Hand_R_Stretch_To')
                # Legs L
                Set_Volume_Variation_Stretch_To(
                    'properties_leg_L', 'volume_variation_leg_L', 'Vol_Var_Leg_L_Stretch_To')
                Set_Volume_Variation_Stretch_To(
                    'properties_leg_L', 'volume_variation_toes_L', 'Vol_Var_Foot_L_Stretch_To')
                # Legs R
                Set_Volume_Variation_Stretch_To(
                    'properties_leg_R', 'volume_variation_leg_R', 'Vol_Var_Leg_R_Stretch_To')
                Set_Volume_Variation_Stretch_To(
                    'properties_leg_R', 'volume_variation_toes_R', 'Vol_Var_Foot_R_Stretch_To')
                # Torso
                Set_Volume_Variation_Stretch_To(
                    'properties_torso', 'volume_variation_torso', 'Vol_Var_Torso_Stretch_To')
                # Neck
                Set_Volume_Variation_Stretch_To('properties_head', 'volume_variation_neck', 'Vol_Var_Neck_Stretch_To')
                # Head
                Set_Volume_Variation_Stretch_To('properties_head', 'volume_variation_head', 'Vol_Var_Head_Stretch_To')
                return {"FINISHED"}

### VOLUME PRESERVATION CONSTRAINTS ####

def set_vol_preservation(context):

    if not context.screen and context.screen.is_animation_playing == True and not context.active_object:
        return False

    # if context.active_object.type == "ARMATURE" and context.active_object.mode == 'POSE':
    #     for prop in context.active_object.data.items():
    #         if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

    # Fingers Down L
    Set_VP_Transforms('properties_arm_L', 'volume_preservation_fingers_down_L', 'Fing_VP_Down_L_NOREP', 'to_max_y', 1)
    # Kunckles Down L
    Set_VP_Transforms('properties_arm_L', 'volume_preservation_knuckles_down_L',
                      'Fing_Knuckles_VP_Down_L_NOREP', 'to_max_z', -1)
    # Kunckles Up L
    Set_VP_Transforms('properties_arm_L', 'volume_preservation_knuckles_up_L',
                      'Fing_Knuckles_VP_Up_L_NOREP', 'to_min_y', 1)
    # Palm Down L
    Set_VP_Transforms('properties_arm_L', 'volume_preservation_palm_down_L', 'Fing_Palm_VP_Down_L_NOREP', 'to_max_y', 1)
    # Fingers Down R
    Set_VP_Transforms('properties_arm_R', 'volume_preservation_fingers_down_R', 'Fing_VP_Down_R_NOREP', 'to_max_y', 1)
    # Kunckles Down R
    Set_VP_Transforms('properties_arm_R', 'volume_preservation_knuckles_down_R',
                      'Fing_Knuckles_VP_Down_R_NOREP', 'to_max_z', -1)
    # Kunckles Up R
    Set_VP_Transforms('properties_arm_R', 'volume_preservation_knuckles_up_R',
                      'Fing_Knuckles_VP_Up_R_NOREP', 'to_min_y', 1)
    # Palm Down R
    Set_VP_Transforms('properties_arm_R', 'volume_preservation_palm_down_R', 'Fing_Palm_VP_Down_R_NOREP', 'to_max_y', 1)
    # Sole Down L
    Set_VP_Transforms('properties_leg_L', 'volume_preservation_sole_down_L', 'Toe_Sole_VP_Down_L_NOREP', 'to_max_y', 1)
    # Toe Knuckles Up L
    Set_VP_Transforms('properties_leg_L', 'volume_preservation_toe_knuckles_up_L',
                      'Toe_Knuckles_VP_Up_L_NOREP', 'to_min_y', 1)
    # Toes Down L
    Set_VP_Transforms('properties_leg_L', 'volume_preservation_toes_down_L', 'Toes_VP_Down_L_NOREP', 'to_max_y', 1)
    # Sole Down R
    Set_VP_Transforms('properties_leg_R', 'volume_preservation_sole_down_R', 'Toe_Sole_VP_Down_R_NOREP', 'to_max_y', 1)
    # Toe Knuckles Up R
    Set_VP_Transforms('properties_leg_R', 'volume_preservation_toe_knuckles_up_R',
                      'Toe_Knuckles_VP_Up_R_NOREP', 'to_min_y', 1)
    # Toes Down R
    Set_VP_Transforms('properties_leg_R', 'volume_preservation_toes_down_R', 'Toes_VP_Down_R_NOREP', 'to_max_y', 1)
    return {"FINISHED"}

### Get Only Insert Available State

def get_state_only_insert_available(context):
    bpy.context.scene.blenrig_guide.state_keyframe_insert_available = bpy.context.preferences.edit.use_keyframe_insert_available


##############
# Pole Angle #
# by Jerryno #
##############

def calculate_pole_angle(upper_bone, lower_bone, pole_bone):

    arm_obj = bpy.context.active_object

    def signed_angle(vector_u, vector_v, normal):
        # Normal specifies orientation
        angle = vector_u.angle(vector_v)
        if vector_u.cross(vector_v).angle(normal) < 1:
            angle = -angle
        return angle

    def get_pole_angle(base_bone, ik_bone, pole_location):
        pole_normal = (ik_bone.tail - base_bone.head).cross(pole_location - base_bone.head)
        projected_pole_axis = pole_normal.cross(base_bone.tail - base_bone.head)
        return signed_angle(base_bone.x_axis, projected_pole_axis, base_bone.tail - base_bone.head)

    base_bone = arm_obj.pose.bones[upper_bone]
    ik_bone = arm_obj.pose.bones[lower_bone]
    pole_bone = arm_obj.pose.bones[pole_bone]

    pole_angle_in_radians = get_pole_angle(
        base_bone,
        ik_bone,
        pole_bone.matrix.translation)

    return np.rad2deg(pole_angle_in_radians)

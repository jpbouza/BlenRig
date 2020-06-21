import bpy

#### File to append to the rig via game logic when the intention is to use it in a system that doesn't have the BlenRig addon installed

####### Bones Hiding System #######

from bpy.props import FloatProperty, IntProperty, BoolProperty


def bone_auto_hide(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for b_prop in bpy.context.active_object.data.items():
            if b_prop[0] == 'bone_auto_hide' and b_prop[1] == 0:
                return False
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':

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
                        #Left Properties
                        if ('_L' in b.name):
                            if ('arm' in b.name):

                            # Arm_L FK/IK
                                prop = int(b.ik_arm_L)
                                prop_hinge = int(b.space_hand_L)
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

                        #Right Properties
                        if ('_R' in b.name):
                            if ('arm' in b.name):

                            # Arm_R FK/IK
                                prop = int(b.ik_arm_R)
                                prop_hinge = int(b.space_hand_R)
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
mode = []
def reproportion_toggle(context):
    if context:
        mode.append(context.active_object.mode)
        # print(mode)
        if context.active_object.data.reproportion:
            bpy.ops.object.mode_set(mode='POSE')
        else:
            if len(mode) > 1:
                bpy.ops.object.mode_set(mode=mode[-2])
        if len(mode) > 1:
            del mode[0]

    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                prop = bool(bpy.context.active_object.data.reproportion)
                p_bones = bpy.context.active_object.pose.bones
                if prop:
                    contador = 0
                    for layer in bpy.context.active_object.data.layers:
                        listaDeEstados.insert(contador, layer)
                        contador += 1

                    contador = 0
                    for layer in bpy.context.active_object.data.layers:
                        if layer:
                            bpy.context.active_object.data.layers[contador] = not bpy.context.active_object.data.layers[contador]

                        contador += 1
                        bpy.context.active_object.data.layers[31] = True


                    for b in p_bones:
                        for C in b.constraints:
                            if ('REPROP' in C.name):
                                C.mute = False
                            if ('NOREP' in C.name):
                                C.mute = True

                else:
                    contador = 0
                    try :
                        for layer in bpy.context.active_object.data.layers:
                            bpy.context.active_object.data.layers[contador] = listaDeEstados[contador]
                            contador += 1

                        for b in p_bones:
                            for C in b.constraints:
                                if ('REPROP' in C.name):
                                    C.mute = True
                                if ('NOREP' in C.name):
                                    C.mute = False
                        rig_toggles(context)
                    except:
                        pass

####### Rig Toggles #######

def rig_toggles(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                p_bones = bpy.context.active_object.pose.bones
                arm = bpy.context.active_object.data

                for b in p_bones:
                    if ('properties' in b.name):
                        # Left Properties
                        #Fingers_L
                        if ('L' in b.name):
                            if ('arm'in b.name):
                                prop_fing = int(b.toggle_fingers_L)
                                for bone in arm.bones:
                                    if (bone.name in b['bones_fingers_def_1_L']):
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0
                                    if (bone.name in b['bones_fingers_def_2_L']):
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[27] = 0
                                            bone.layers[31] = 0
                                    if (bone.name in b['bones_fingers_str_L']):
                                        if prop_fing == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:
                                            if (bone.name in b['bones_fingers_ctrl_1_L']):
                                                if prop_fing == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0
                                            if (bone.name in b['bones_fingers_ctrl_2_L']):
                                                if prop_fing == 1:
                                                    bone.layers[2] = 1
                                                else:
                                                    bone.layers[2] = 0
                                    if (bone.name in b['bones_fingers_ctrl_2_L']):
                                        if prop_fing == 1:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True
                        #Toes_L
                        if ('L' in b.name):
                            if ('leg'in b.name):
                                prop_toes = int(b.toggle_toes_L)
                                for bone in arm.bones:
                                    if (bone.name in b['bones_toes_def_1_L']):
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0
                                    if (bone.name in b['bones_toes_def_2_L']):
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[27] = 0
                                            bone.layers[31] = 0
                                    if (bone.name in b['bones_no_toes_def_L']):
                                        if prop_toes == 1:
                                            bone.layers[27] = 0
                                        else:
                                            bone.layers[27] = 1
                                    if (bone.name in b['bones_toes_str_L']):
                                        if prop_toes == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:
                                            if (bone.name in b['bones_toes_ctrl_1_L']):
                                                if prop_toes == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0
                                            if (bone.name in b['bones_no_toes_ctrl_L']):
                                                if prop_toes == 1:
                                                    bone.layers[0] = 0
                                                else:
                                                    bone.layers[0] = 1
                                            if (bone.name in b['bones_toes_ctrl_2_L']):
                                                if prop_toes == 1:
                                                    bone.layers[2] = 1
                                                else:
                                                    bone.layers[2] = 0
                                    if (bone.name in b['bones_toes_ctrl_2_L']):
                                        if prop_toes == 1:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True

                        # Right Properties
                        #Fingers_R
                        if ('R' in b.name):
                            if ('arm'in b.name):
                                prop_fing = int(b.toggle_fingers_R)
                                for bone in arm.bones:
                                    if (bone.name in b['bones_fingers_def_1_R']):
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0
                                    if (bone.name in b['bones_fingers_def_2_R']):
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[27] = 0
                                            bone.layers[31] = 0
                                    if (bone.name in b['bones_fingers_str_R']):
                                        if prop_fing == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:
                                            if (bone.name in b['bones_fingers_ctrl_1_R']):
                                                if prop_fing == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0
                                            if (bone.name in b['bones_fingers_ctrl_2_R']):
                                                if prop_fing == 1:
                                                    bone.layers[2] = 1
                                                else:
                                                    bone.layers[2] = 0
                                    if (bone.name in b['bones_fingers_ctrl_2_R']):
                                        if prop_fing == 1:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True
                        #Toes_R
                        if ('R' in b.name):
                            if ('leg'in b.name):
                                prop_toes = int(b.toggle_toes_R)
                                for bone in arm.bones:
                                    if (bone.name in b['bones_toes_def_1_R']):
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0
                                    if (bone.name in b['bones_toes_def_2_R']):
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[27] = 0
                                            bone.layers[31] = 0
                                    if (bone.name in b['bones_no_toes_def_R']):
                                        if prop_toes == 1:
                                            bone.layers[27] = 0
                                        else:
                                            bone.layers[27] = 1
                                    if (bone.name in b['bones_toes_str_R']):
                                        if prop_toes == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:
                                            if (bone.name in b['bones_toes_ctrl_1_R']):
                                                if prop_toes == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0
                                            if (bone.name in b['bones_no_toes_ctrl_R']):
                                                if prop_toes == 1:
                                                    bone.layers[0] = 0
                                                else:
                                                    bone.layers[0] = 1
                                            if (bone.name in b['bones_toes_ctrl_2_R']):
                                                if prop_toes == 1:
                                                    bone.layers[2] = 1
                                                else:
                                                    bone.layers[2] = 0
                                    if (bone.name in b['bones_toes_ctrl_2_R']):
                                        if prop_toes == 1:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True

####### Rig Optimizations #######

####### Toggle Face Drivers #######

def toggle_face_drivers(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
            prop = bool(bpy.context.active_object.data.toggle_face_drivers)
            armobj = bpy.context.active_object
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
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
            prop = bool(bpy.context.active_object.data.toggle_flex_drivers)
            armobj = bpy.context.active_object
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
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
            prop = bool(bpy.context.active_object.data.toggle_dynamic_drivers)
            armobj = bpy.context.active_object
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
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
            prop = bool(bpy.context.active_object.data.toggle_body_drivers)
            armobj = bpy.context.active_object
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
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                p_bones = bpy.context.active_object.pose.bones
                arm = bpy.context.active_object.data

                for b in p_bones:
                    #Arm Pole L
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
                    #Arm Pole R
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

                    #Leg Pole L
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

                    #Leg Pole R
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
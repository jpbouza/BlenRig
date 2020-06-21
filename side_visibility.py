
import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup

#################################################
##### el ui esta en ui_panel_rigging_2_0.py #####
#################################################

def get_properties(context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility
    if side_visibility:
        return side_visibility

def get_bones_from_group(target):
    arm_name = bpy.context.active_object.name
    armature = bpy.data.objects[arm_name]
    grupo_target = armature.pose.bone_groups[target]
    bones = []
    for b in armature.pose.bones:
        if b.bone_group == grupo_target:
            bones.append(b)
    return bones


def show_eyes(self, context):
    side_visibility = get_properties(context)
    huesos = get_bones_from_group(g_EYES)
    for h in huesos:
        if not side_visibility.right_side and h.name[-2:len(h.name)] != '_L':
            bpy.context.object.data.bones[h.name].hide = not bpy.context.object.data.bones[h.name].hide
        if not side_visibility.left_side and h.name[-2:len(h.name)] != '_R':
            bpy.context.object.data.bones[h.name].hide = not bpy.context.object.data.bones[h.name].hide

def show_face(self, context):
    side_visibility = get_properties(context)

    if side_visibility.face:
        for g in g_FACIAL:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False

        for h in g_FACIAL_EXTRAS:
                bpy.context.object.data.bones[h].hide = False
    else:
        for g in g_FACIAL:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True

        for h in g_FACIAL_EXTRAS:
                bpy.context.object.data.bones[h].hide = True

def show_lips(self, context):
    side_visibility = get_properties(context)

    if side_visibility.lips:
        for g in g_LIPS:
            huesos = get_bones_from_group(g)
            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False

        for h in g_LIPS_EXTRAS:
            bpy.context.object.data.bones[h].hide = False
    else:
        for g in g_LIPS:
            huesos = get_bones_from_group(g)
            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True

        for h in g_LIPS_EXTRAS:
            bpy.context.object.data.bones[h].hide = True

def show_eyebrows(self, context):
    side_visibility = get_properties(context)

    if side_visibility.eyebrows:
        huesos = get_bones_from_group(g_EYEBROWS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
        for h in ex_huesos:
            bpy.context.object.data.bones[h].hide = False
    else:
        huesos = get_bones_from_group(g_EYEBROWS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True
        for h in ex_huesos:
            bpy.context.object.data.bones[h].hide = True

def show_face_mech(self, context):
    side_visibility = get_properties(context)

    if side_visibility.face_mech:
        huesos = get_bones_from_group(g_STR_FACE_MECH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False

        for h in g_FACE_MECH_EXTRA :
            bpy.context.object.data.bones[h].hide = False
    else:
        huesos = get_bones_from_group(g_STR_FACE_MECH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True

        for h in g_FACE_MECH_EXTRA :
            bpy.context.object.data.bones[h].hide = True

def show_inner_mouth(self, context):
    side_visibility = get_properties(context)

    if side_visibility.inner_mouth:
        huesos = get_bones_from_group(g_STR_INNER_MOUTH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_INNER_MOUTH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True

def show_hands(self, context):
    side_visibility = get_properties(context)

    if side_visibility.hands:
        huesos = get_bones_from_group(g_STR_HANDS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_HANDS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True

def show_body(self, context):
    side_visibility = get_properties(context)

    if side_visibility.body:
        for g in g_STR:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False

        for h in g_BODY:
            bpy.context.object.data.bones[h].hide = False
    else:
        for g in g_STR:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True

        for h in g_BODY:
            bpy.context.object.data.bones[h].hide = True

def show_face_controls(self, context):
    side_visibility = get_properties(context)

    if side_visibility.face_controls:
        for h in g_FACE_CONTROLS :
            bpy.context.object.data.bones[h].hide = False
    else:
        for h in g_FACE_CONTROLS :
            bpy.context.object.data.bones[h].hide = True


r_side= []
def show_right_side (self, context):
    side_visibility = get_properties(context)

    if side_visibility.right_side:
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_R"):
                    r_side.append(bone.name)

        for bones_r in r_side:
            bpy.context.object.data.bones[bones_r].hide = True
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_R"):
                    r_side.remove(bone.name)

    else:
        for bones_r in r_side:
            bpy.context.object.data.bones[bones_r].hide = False
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_R"):
                    r_side.remove(bone.name)


l_side= []
def show_left_side (self, context):
    side_visibility = get_properties(context)

    if side_visibility.left_side:
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_L"):
                    l_side.append(bone.name)

        for bones_l in l_side:
            bpy.context.object.data.bones[bones_l].hide = True
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_L"):
                    l_side.remove(bone.name)
    else:
        for bones_l in l_side:
            bpy.context.object.data.bones[bones_l].hide = False
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_L"):
                    l_side.remove(bone.name)


class side_visibility_props(PropertyGroup):
    eyes: BoolProperty(name="eyes", default=True, update=show_eyes)
    face: BoolProperty(name="face", default=True, update=show_face)
    eyebrows: BoolProperty(name="eyebrows", default=True, update=show_eyebrows)
    face_mech: BoolProperty(name="face_mech", default=True, update=show_face_mech)
    inner_mouth: BoolProperty(name="inner_mouth", default=True, update=show_inner_mouth)
    hands: BoolProperty(name="hands", default=True, update=show_hands)
    body: BoolProperty(name="body", default=True, update=show_body)
    lips: BoolProperty(name="body", default=True, update=show_lips)
    face_controls: BoolProperty(name="body", default=True, update=show_face_controls)
    left_side: BoolProperty(name="left_side", default=False, update=show_left_side)
    right_side: BoolProperty(name="right_side", default=False, update=show_right_side)

########################## FACIAL ##################################
g_FACIAL = ['FACIAL_MAIN_MID',
            'STR_FACE',
            'FACIAL_MAIN_R',
            'FACIAL_MAIN_L',
            'FACIAL_MID',
            'FACIAL_MID',
            'FACIAL_R',
            'FACIAL_L']

g_FACIAL_EXTRAS = ('chin_ctrl_mid',
                    'lip_low_outer_ctrl_mid',
                    'nose_bridge_ctrl_2',
                    'nose_root_ctrl_mid',
                    'frown_ctrl'
)

####################### LIPS ####################################

g_LIPS = ['STR_LIPS']
g_LIPS_EXTRAS = ('lip_low_rim_ctrl_mid',
                'lip_low_line_ctrl_mid',
                'lip_up_rim_ctrl_mid',
                'lip_up_line_ctrl_mid',

                'lip_low_rim_ctrl_1_L',
                'lip_low_rim_ctrl_2_L',
                'lip_low_rim_ctrl_3_L',
                'lip_low_rim_ctrl_1_R',
                'lip_low_rim_ctrl_2_R',
                'lip_low_rim_ctrl_3_R',

                'lip_up_rim_ctrl_1_L',
                'lip_up_rim_ctrl_2_L',
                'lip_up_rim_ctrl_3_L',
                'lip_up_rim_ctrl_4_L',
                'lip_up_rim_ctrl_1_R',
                'lip_up_rim_ctrl_2_R',
                'lip_up_rim_ctrl_3_R',
                'lip_up_rim_ctrl_4_R',

                'lip_low_line_ctrl_1_L',
                'lip_low_line_ctrl_2_L',
                'lip_low_line_ctrl_3_L',
                'lip_low_line_ctrl_1_R',
                'lip_low_line_ctrl_2_R',
                'lip_low_line_ctrl_3_R',

                'lip_up_line_ctrl_1_L',
                'lip_up_line_ctrl_2_L',
                'lip_up_line_ctrl_3_L',
                'lip_up_line_ctrl_4_L',
                'lip_up_line_ctrl_1_R',
                'lip_up_line_ctrl_2_R',
                'lip_up_line_ctrl_3_R',
                'lip_up_line_ctrl_4_R',
)

############################## FACE CONTROLS ############################
g_FACE_CONTROLS = ('mouth_corner_L',
                    'mouth_corner_R',
                    'mouth_frown_ctrl_L',
                    'mouth_frown_ctrl_R',
                    'cheek_ctrl_L',
                    'cheek_ctrl_R',
                    'nose_frown_ctrl_L',
                    'nose_frown_ctrl_R',
                    'eyelid_up_ctrl_L',
                    'eyelid_up_ctrl_R',
                    'eyelid_low_ctrl_L',
                    'eyelid_low_ctrl_R',
                    'cheek_puff_mstr_L',
                    'cheek_puff_mstr_R',
                    'cheek_puff_ctrl_L',
                    'cheek_puff_ctrl_R',
                    'eyelid_up_rim_ctrl_L',
                    'eyelid_up_rim_ctrl_R',
                    # 'old_eyelid_up_ctrl_L',
                    # 'old_eyelid_up_ctrl_R',
                    # 'old_eyelid_low_rim_ctrl_L',
                    # 'old_eyelid_low_rim_ctrl_R',
                    # 'old_eyelid_low_ctrl_L',
                    # 'old_eyelid_low_ctrl_R'
)

############################## EYES #####################################

g_EYES = ('STR_EYES')

############################## EYEBROWS ############################

g_EYEBROWS = ('STR_EYEBROWS')

############################## FACE MECH ############################

g_STR_FACE_MECH = ('STR_FACE_MECH')
g_FACE_MECH_EXTRA = ('lip_low_ctrl_collision',
                    'lip_up_ctrl_collision'
                    )
############################## INNER MOUTH ############################

g_STR_INNER_MOUTH = ('STR_INNER_MOUTH')

############################## HANDS ############################

g_STR_HANDS = ('STR_HANDS')

############################## REST ############################

g_STR = ('STR','GEN','IK_L','IK_R','PIVOT_POINTS')

ex_huesos= ('brow_ctrl_3_L',
            'brow_ctrl_2_L',
            'brow_ctrl_1_L',
            'brow_ctrl_4_L',
            'brow_ctrl_5_L',
            'brow_ctrl_3_R',
            'brow_ctrl_2_R',
            'brow_ctrl_1_R',
            'brow_ctrl_4_R',
            'brow_ctrl_5_R')


############################## BODY ############################

g_BODY = ('neck_1_def',
        'neck_2_def',
        'neck_3_def',
        'head_def_mstr',
        'head_def_2',
        'head_def_3',
        'head_def_1',
        'thigh_twist_def_L',
        'foot_def_L',
        'shin_def_L',
        'shin_twist_def_L',
        'thigh_twist_def_R',
        'foot_def_R',
        'shin_def_R',
        'shin_twist_def_R',
        'arm_twist_def_L',
        'hand_def_L',
        'forearm_twist_def_L',
        'forearm_def_L',
        'arm_twist_def_R',
        'hand_def_R',
        'forearm_twist_def_R',
        'forearm_def_R',
        'knee_line_L',
        'knee_line_R',
        'pelvis_def',
        'pelvis_def_L',
        'thigh_def_L',
        'pelvis_def_R',
        'thigh_def_R',
        'spine_1_def',
        'spine_2_def',
        'elbow_line_R',
        'clavi_def_R',
        'arm_def_R',
        'elbow_line_L',
        'clavi_def_L',
        'arm_def_L',
        'spine_3_def',
        'mouth_mstr_ik_copy_loc',
        'foot_toe_2_def_L',
        'foot_toe_1_def_L',
        'foot_toe_2_def_R',
        'foot_toe_1_def_R',
        'neck_1_def.001',
        'neck_2_def.001',
        'neck_3_def.001'
        )

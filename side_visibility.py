
import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup
import json, os

json_path_file = os.path.join("data_jsons", "bones_from_bone_groups.json")


#################################################
##### el ui esta en ui_panel_rigging_2_0.py #####
#################################################

def get_bones(target_groups):
    bones = []
    with open(json_path_file) as json_file:
        data = json.load(json_file)
        for bg in data['bone_groups']:
            if bg['name'] in target_groups:
                for bone in bg['bones']:
                    bones.append(bone)
    return bones

def toggle_bone_visibility(left_side, right_side, target, bones):
    for bone in bones:
        if target:
            if not left_side and bone.endswith('_L'):
                bpy.context.object.data.bones[bone].hide = False
            if not right_side and bone.endswith('_R'):
                bpy.context.object.data.bones[bone].hide = False
            if not left_side and bone.endswith('_mid'):
                bpy.context.object.data.bones[bone].hide = False
            if bone.endswith('_mid'):
                bpy.context.object.data.bones[bone].hide = False
        else:
            if not left_side and bone.endswith('_L'):
                bpy.context.object.data.bones[bone].hide = True
            if not right_side and bone.endswith('_R'):
                bpy.context.object.data.bones[bone].hide = True
            if bone.endswith('_mid'):
                bpy.context.object.data.bones[bone].hide = True


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

    target_groups = ['STR_EYES']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.eyes, bones)

def show_face(self, context):
    side_visibility = get_properties(context)

    target_groups = ['STR_SMILE_LINE','STR_FACE', 'FACIAL_L', 'FACIAL_R', 'FACIAL_MID', 'FACIAL_MAIN_L', 'FACIAL_MAIN_R', 'FACIAL_MAIN_MID']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.face, bones)


def show_lips(self, context):
    side_visibility = get_properties(context)

    target_groups = ['STR_LIPS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.lips, bones)


def show_eyebrows(self, context):
    side_visibility = get_properties(context)

    target_groups = ['STR_EYEBROWS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.eyebrows, bones)

def show_face_mech(self, context):
    side_visibility = get_properties(context)

    # FACE_MECH_EXTRA no existe como tal
    target_groups = ['STR_FACE_MECH', 'STR_FACE_MECH']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.face_mech, bones)


def show_inner_mouth(self, context):
    side_visibility = get_properties(context)

    target_groups = ['STR_INNER_MOUTH']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.inner_mouth, bones)

def show_hands(self, context):
    side_visibility = get_properties(context)

    target_groups = ['STR_HANDS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.hands, bones)

def show_body(self, context):
    side_visibility = get_properties(context)

    target_groups = ['STR', 'BODY']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.body, bones)

def show_face_controls(self, context):
    side_visibility = get_properties(context)

    # FACE_CONTROLS no existe como tal
    target_groups = ['FACE_CONTROLS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(side_visibility.left_side, side_visibility.right_side, side_visibility.face_controls, bones)


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
    lips: BoolProperty(name="lips", default=True, update=show_lips)
    face_controls: BoolProperty(name="face_controls", default=True, update=show_face_controls)
    left_side: BoolProperty(name="left_side", default=False, update=show_left_side)
    right_side: BoolProperty(name="right_side", default=False, update=show_right_side)

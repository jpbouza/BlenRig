
import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup
import json, os

script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
json_path_file = os.path.join(directory, "data_jsons", "bones_from_bone_groups.json")


#################################################
##### the ui is in ui_panel_rigging_2_0.py #####
#################################################


## for register and unregister in the fly with blender events ##
################################################################
from bpy.utils import register_class
from bpy.utils import unregister_class

from bpy.app.handlers import persistent
from .ui.panels.rigging_and_baking import BLENRIG_PT_visual_assistant, BLENRIG_PT_baking

def register_panel(class_name):
    try:
        register_class(class_name)
    except:
        pass

def unregister_panel(class_name):
    try:
        unregister_class(class_name)
    except:
        pass

# handle panel events ################################################
def handle_panel_events():
    for arm in bpy.data.armatures:
        owner = object()
        subscribe_to = arm.layers

        def msgbus_callback():
            if bpy.context.active_object.data.layers[27]:
                unregister_panel(BLENRIG_PT_visual_assistant)
                register_panel(BLENRIG_PT_visual_assistant)

                unregister_panel(BLENRIG_PT_baking)

            elif bpy.context.active_object.data.reproportion:
                unregister_panel(BLENRIG_PT_visual_assistant)
                register_panel(BLENRIG_PT_visual_assistant)

                unregister_panel(BLENRIG_PT_baking)                
                register_class(BLENRIG_PT_baking)

            else:
                unregister_panel(BLENRIG_PT_visual_assistant)
                unregister_panel(BLENRIG_PT_baking)

        bpy.msgbus.subscribe_rna(
            key=subscribe_to,
            owner=owner,
            args=(),
            notify=msgbus_callback,
        )

################################################################







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
        if bone in bpy.context.object.data.bones:
            if target:
                if not left_side and bone.endswith('_L') or bone.endswith(".L"):
                    bpy.context.object.data.bones[bone].hide = False
                elif not right_side and bone.endswith('_R') or bone.endswith(".R"):
                    bpy.context.object.data.bones[bone].hide = False
                else:
                    bpy.context.object.data.bones[bone].hide = False
            else:
                if not left_side and bone.endswith('_L') or bone.endswith(".L"):                
                    bpy.context.object.data.bones[bone].hide = True
                elif not right_side and bone.endswith('_R') or bone.endswith(".R"):
                    bpy.context.object.data.bones[bone].hide = True
                else:
                    bpy.context.object.data.bones[bone].hide = True



def get_properties(context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        visual_assistant = context.active_object.data.visual_assistant
    if visual_assistant:
        return visual_assistant


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
    visual_assistant = get_properties(context)

    target_groups = ['EYES']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.eyes, bones)

def show_face(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['FACE','SMILE_LINE']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.face, bones)


def show_lips(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['LIPS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.lips, bones)


def show_eyebrows(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['EYEBROWS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.eyebrows, bones)

def show_face_mech(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['FACE_MECH']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.face_mech, bones)


def show_inner_mouth(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['INNER_MOUTH']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.inner_mouth, bones)

def show_hands(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['HANDS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.hands, bones)

def show_toes(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['TOES']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.toes, bones)

def show_body(self, context):
    visual_assistant = get_properties(context)

    target_groups = ['BODY']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.body, bones)

def show_face_controls(self, context):
    visual_assistant = get_properties(context)

    # FACE_CONTROLS does not exist as such
    target_groups = ['FACE_CONTROLS']
    bones = get_bones(target_groups)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.face_controls, bones)

def show_others(self, context):
    visual_assistant = get_properties(context)

    controled_bones = ['EYEBROWS', 'EYES', 'FACE', 'FACE_MECH', 'INNER_MOUTH', 'HANDS', 'LIPS', 'SMILE_LINE', 'FACE_CONTROLS', 'BODY', 'TOES']
    bones = get_bones(controled_bones)

    # get the other bones:
    other_bones = []
    for b in context.active_object.data.bones:
        if b.name not in bones:
            other_bones.append(b.name)

    toggle_bone_visibility(visual_assistant.left_side, visual_assistant.right_side, visual_assistant.others, other_bones)


r_side= []
def show_right_side (self, context):
    visual_assistant = get_properties(context)

    if visual_assistant.right_side:
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_R") or bone.name.endswith(".R"):
                    r_side.append(bone.name)

        for bones_r in r_side:
            bpy.context.object.data.bones[bones_r].hide = True
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_R") or bone.name.endswith(".R"):
                    r_side.remove(bone.name)

    else:
        for bones_r in r_side:
            bpy.context.object.data.bones[bones_r].hide = False
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_R") or bone.name.endswith(".R"):
                    r_side.remove(bone.name)


l_side= []
def show_left_side (self, context):
    visual_assistant = get_properties(context)

    if visual_assistant.left_side:
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_L") or bone.name.endswith(".L") :
                    l_side.append(bone.name)

        for bones_l in l_side:
            bpy.context.object.data.bones[bones_l].hide = True
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_L") or bone.name.endswith(".L"):
                    l_side.remove(bone.name)
    else:
        for bones_l in l_side:
            bpy.context.object.data.bones[bones_l].hide = False
        if bpy.context.visible_pose_bones:
            for bone in bpy.context.visible_pose_bones:
                if bone.name.endswith("_L") or bone.name.endswith(".L"):
                    l_side.remove(bone.name)


class visual_assistant_props(PropertyGroup):
    left_side: BoolProperty(name="left_side", default=False, update=show_left_side)
    right_side: BoolProperty(name="right_side", default=False, update=show_right_side)
    eyes: BoolProperty(name="eyes", default=True, update=show_eyes)
    face: BoolProperty(name="face", default=True, update=show_face)
    eyebrows: BoolProperty(name="eyebrows", default=True, update=show_eyebrows)
    face_mech: BoolProperty(name="face_mech", default=True, update=show_face_mech)
    inner_mouth: BoolProperty(name="inner_mouth", default=True, update=show_inner_mouth)
    hands: BoolProperty(name="hands", default=True, update=show_hands)
    toes: BoolProperty(name="toes", default=True, update=show_toes)
    body: BoolProperty(name="body", default=True, update=show_body)
    lips: BoolProperty(name="lips", default=True, update=show_lips)
    face_controls: BoolProperty(name="face_controls", default=True, update=show_face_controls)
    others: BoolProperty(name="others", default=True, update=show_others)


import bpy
from bpy.props import BoolProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup


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
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

    if side_visibility.eyes:
        huesos = get_bones_from_group(g_EYES)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_EYES)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True


def show_face(self, context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

    if side_visibility.face:
        for g in g_FACIAL:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False
    else:
        for g in g_FACIAL:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True


def show_eyebrows(self, context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

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
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

    if side_visibility.face_mech:
        huesos = get_bones_from_group(g_STR_FACE_MECH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_FACE_MECH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True


def show_inner_mouth(self, context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

    if side_visibility.inner_mouth:
        huesos = get_bones_from_group(g_STR_INNER_MOUTH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_INNER_MOUTH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True


def show_hands(self, context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

    if side_visibility.hands:
        huesos = get_bones_from_group(g_STR_HANDS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_HANDS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True


def show_body(self, context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

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


r_side= []
def show_right_side (self, context):
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

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
    ao = context.active_object
    if ao.type == 'ARMATURE':
        side_visibility = context.active_object.data.side_visibility

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
    left_side: BoolProperty(name="left_side", default=False, update=show_left_side)
    right_side: BoolProperty(name="right_side", default=False, update=show_right_side)

g_FACIAL = ['FACIAL_MAIN_MID',
            'STR_FACE',
            'FACIAL_MAIN_R',
            'FACIAL_MAIN_L',
            'FACIAL_MID',
            'FACIAL_MID',
            'FACIAL_R',
            'FACIAL_L']
g_EYES = ('STR_EYES')
g_EYEBROWS = ('STR_EYEBROWS')
g_STR_FACE_MECH = ('STR_FACE_MECH')
g_STR_INNER_MOUTH = ('STR_INNER_MOUTH')
g_STR_HANDS = ('STR_HANDS')
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
g_BODY = ('neck_1_def',
        'neck_2_def',
        'neck_3_def',
        'head_def_mstr',
        'head_def_2',
        'head_def_3',
        'head_def_1',
        'thigh_twist_def_L',
        # 'toe_2_def_L',
        # 'toe_1_def_L',
        'toe_2_toon_L',
        'toe_1_toon_L',
        'foot_def_L',
        'shin_def_L',
        'shin_twist_def_L',
        'thigh_twist_def_R',
        # 'toe_2_def_R',
        # 'toe_1_def_R',
        'toe_2_toon_R',
        'toe_1_toon_R',
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
        'mouth_mstr_ik_copy_loc')


class SIDE_PT_visibility(Panel):
    bl_label = "Side Visibility"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        else:
            if context.object.mode == 'POSE':
                if (bpy.context.active_object.type in ["ARMATURE"]):
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                                return True
            else:
                return False

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        ao = context.active_object
        if ao.type == 'ARMATURE':
            side_visibility = context.active_object.data.side_visibility

            row = layout.row(align=True)

            icon = 'HIDE_OFF' if not side_visibility.right_side else 'HIDE_ON'
            row.prop(side_visibility, "right_side", text="R_Side", icon=icon, toggle=True)
            icon = 'HIDE_OFF' if not side_visibility.left_side else 'HIDE_ON'
            row.prop(side_visibility, "left_side", text="L_Side", icon=icon, toggle=True)

            layout.use_property_split = True
            layout.use_property_decorate = False

            flow = layout.grid_flow(align=True)
            col = flow.column()

            icon = 'HIDE_ON' if not side_visibility.eyes else 'HIDE_OFF'
            col.prop(side_visibility, "eyes", icon=icon, text="EYES", toggle=True)

            icon = 'HIDE_ON' if not side_visibility.face else 'HIDE_OFF'
            col.prop(side_visibility, "face", icon=icon, text="FACE", toggle=True)

            icon = 'HIDE_ON' if not side_visibility.eyebrows else 'HIDE_OFF'
            col.prop(side_visibility, "eyebrows", icon=icon, text="EYEBROWS", toggle=True)

            icon = 'HIDE_ON' if not side_visibility.face_mech else 'HIDE_OFF'
            col.prop(side_visibility, "face_mech", icon=icon, text="FACE MECH", toggle=True)

            icon = 'HIDE_ON' if not side_visibility.inner_mouth else 'HIDE_OFF'
            col.prop(side_visibility, "inner_mouth", icon=icon, text="INNER MOUTH", toggle=True)

            icon = 'HIDE_ON' if not side_visibility.hands else 'HIDE_OFF'
            col.prop(side_visibility, "hands", icon=icon, text="HANDS", toggle=True)

            icon = 'HIDE_ON' if not side_visibility.body else 'HIDE_OFF'
            col.prop(side_visibility, "body", icon=icon, text="BODY", toggle=True)

from bpy.types import PoseBone
from bpy.props import FloatProperty, BoolProperty, IntProperty, FloatVectorProperty
from ..rig_functions import (
    bone_auto_hide, pole_toggles, rig_toggles, fingers_toggles, 
    toes_toggles, toggle_face_drivers, toggle_flex_drivers, toggle_dynamic_drivers, 
    toggle_body_drivers, set_eyelids, set_frowns, set_cheeks, set_mouth_corners, 
    set_mouth_ctrl, set_rj_transforms, set_vol_variation, set_vol_preservation
)


def prop_update(self, context):
    bone_auto_hide(context)


def pole_toggles_update(self, context):
    pole_toggles(context)


def rig_toggles_update(self, context, call_from:str, call_from_side:str):
    rig_toggles(context, call_from, call_from_side)

def fingers_toggles_update(self, context):
    fingers_toggles(self, context)

def toes_toggles_update(self, context, call_from:str, call_from_side:str):
    toes_toggles(self, context, call_from, call_from_side)

def optimize_face(self, context):
    toggle_face_drivers(context)

def optimize_flex(self, context):
    toggle_flex_drivers(context)

def optimize_dynamic(self, context):
    toggle_dynamic_drivers(context)

def optimize_body(self, context):
    toggle_body_drivers(context)

def pole_toggles_update(self, context):
    pole_toggles(context)

def eyelids_update(self, context):
    set_eyelids(context)

def frowns_update(self, context):
    set_frowns(context)

def cheeks_update(self, context):
    set_cheeks(context)

def mouth_corners_update(self, context):
    set_mouth_corners(context)

def mouth_ctrl_update(self, context):
    set_mouth_ctrl(context)

def rj_transforms_update(self, context):
    set_rj_transforms(context)

def vol_variation_update(self, context):
    set_vol_variation(context)

def vol_prservation_update(self, context):
    set_vol_preservation(context)


def pbones_props_register():

    #FK/IK

    PoseBone.ik_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_head"
    )
    PoseBone.ik_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_torso"
    )
    PoseBone.inv_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Invert Torso Hierarchy",
        update=prop_update,
        name="inv_torso"
    )
    PoseBone.ik_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_arm_L"
    )
    PoseBone.ik_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_arm_R"
    )
    PoseBone.ik_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_leg_L"
    )
    PoseBone.ik_toes_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_toes_all_L"
    )
    PoseBone.ik_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_leg_R"
    )
    PoseBone.ik_toes_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_toes_all_R"
    )
    PoseBone.ik_fing_ind_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_ind_L"
    )
    PoseBone.ik_fing_mid_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_L"
    )
    PoseBone.ik_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_L"
    )
    PoseBone.ik_fing_lit_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_lit_L"
    )
    PoseBone.ik_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_thumb_L"
    )
    PoseBone.ik_fing_ind_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_ind_R"
    )
    PoseBone.ik_fing_mid_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_R"
    )
    PoseBone.ik_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_R"
    )
    PoseBone.ik_fing_lit_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_lit_R"
    )
    PoseBone.ik_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_thumb_R"
    )
    PoseBone.ik_fing_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_all_R"
    )
    PoseBone.ik_fing_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_all_L"
    )

    # LEGACY HINGE

    PoseBone.hinge_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_head"
    )
    PoseBone.hinge_neck = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_neck"
    )
    PoseBone.hinge_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_arm_L"
    )
    PoseBone.hinge_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_arm_R"
    )
    PoseBone.hinge_hand_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_hand_L"
    )
    PoseBone.hinge_hand_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_hand_R"
    )
    PoseBone.hinge_fing_ind_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_ind_L"
    )
    PoseBone.hinge_fing_mid_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_mid_L"
    )
    PoseBone.hinge_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_mid_L"
    )
    PoseBone.hinge_fing_lit_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_lit_L"
    )
    PoseBone.hinge_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_thumb_L"
    )
    PoseBone.hinge_fing_ind_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_ind_R"
    )
    PoseBone.hinge_fing_mid_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_mid_R"
    )
    PoseBone.hinge_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_mid_R"
    )
    PoseBone.hinge_fing_lit_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_lit_R"
    )
    PoseBone.hinge_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_thumb_R"
    )
    PoseBone.hinge_fing_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_all_R"
    )
    PoseBone.hinge_fing_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_fing_all_L"
    )
    PoseBone.hinge_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_leg_L"
    )
    PoseBone.hinge_toes_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_toes_all_L"
    )
    PoseBone.hinge_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_leg_R"
    )
    PoseBone.hinge_toes_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Isolate Rotation",
        update=prop_update,
        name="hinge_toes_all_R"
    )

    # SPACE

    PoseBone.space_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_head"
    )
    PoseBone.space_neck = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_neck"
    )
    PoseBone.space_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=3.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_arm_L"
    )
    PoseBone.space_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=3.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_arm_R"
    )
    PoseBone.space_hand_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_hand_L"
    )
    PoseBone.space_hand_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_hand_R"
    )
    PoseBone.space_fing_ind_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ind_L"
    )
    PoseBone.space_fing_mid_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_mid_L"
    )
    PoseBone.space_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ring_L"
    )
    PoseBone.space_fing_lit_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_lit_L"
    )
    PoseBone.space_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_thumb_L"
    )
    PoseBone.space_fing_ind_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ind_R"
    )
    PoseBone.space_fing_mid_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_mid_R"
    )
    PoseBone.space_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ring_R"
    )
    PoseBone.space_fing_lit_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_lit_R"
    )
    PoseBone.space_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_thumb_R"
    )
    PoseBone.space_fing_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_all_R"
    )
    PoseBone.space_fing_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_all_L"
    )
    PoseBone.space_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_leg_L"
    )
    PoseBone.space_toes_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_toes_all_L"
    )
    PoseBone.space_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_leg_R"
    )
    PoseBone.space_toes_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_toes_all_R"
    )

    # Poles

    PoseBone.space_arm_ik_pole_L = FloatProperty(
        default=1.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_arm_ik_pole_L"
    )
    PoseBone.space_arm_ik_pole_R = FloatProperty(
        default=1.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_arm_ik_pole_R"
    )
    PoseBone.space_leg_ik_pole_L = FloatProperty(
        default=1.000,
        min=0.000,
        max=2.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_leg_ik_pole_L"
    )
    PoseBone.space_leg_ik_pole_R = FloatProperty(
        default=1.000,
        min=0.000,
        max=2.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_leg_ik_pole_R"
    )
    PoseBone.toggle_arm_ik_pole_L = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_arm_ik_pole_L"
    )
    PoseBone.toggle_arm_ik_pole_R = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_arm_ik_pole_R"
    )
    PoseBone.toggle_leg_ik_pole_L = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_leg_ik_pole_L"
    )
    PoseBone.toggle_leg_ik_pole_R = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_leg_ik_pole_R"
    )

    #Stretchy IK

    PoseBone.toon_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_head"
    )

    PoseBone.toon_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_torso"
    )

    PoseBone.toon_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_arm_L"
    )

    PoseBone.toon_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_arm_R"
    )

    PoseBone.toon_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_leg_L"
    )

    PoseBone.toon_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_leg_R"
    )

    #Stretchy Fingers

    PoseBone.toon_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_thumb_L"
    )

    PoseBone.toon_fing_index_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_index_L"
    )

    PoseBone.toon_fing_middle_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_middle_L"
    )

    PoseBone.toon_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_ring_L"
    )

    PoseBone.toon_fing_little_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_little_L"
    )

    PoseBone.toon_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_thumb_R"
    )

    PoseBone.toon_fing_index_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_index_R"
    )

    PoseBone.toon_fing_middle_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_middle_R"
    )

    PoseBone.toon_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_ring_R"
    )

    PoseBone.toon_fing_little_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_little_R"
    )

    #Pin

    PoseBone.pin_elbow_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Elbow_L",
        update=prop_update,
        name="pin_elbow_L"
    )

    PoseBone.pin_elbow_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Elbow_R",
        update=prop_update,
        name="pin_elbow_R"
    )

    PoseBone.pin_knee_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Knee_L",
        update=prop_update,
        name="pin_knee_L"
    )

    PoseBone.pin_knee_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Knee_R",
        update=prop_update,
        name="pin_knee_R"
    )

    # LOOK SWITCH
    PoseBone.look_switch = FloatProperty(
        default=3.000,
        min=0.000,
        max=3.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Target of Eyes",
        update=prop_update,
        name="look_switch"
    )

    ### TOGGLES
    #Fingers L
    PoseBone.toggle_fingers_L = BoolProperty(
        default=0,
        description="Toggle fingers in rig",
        update=lambda self, context: rig_toggles_update(
                self,
                context,
                'fingers',
                '_L',
            ),
        name="toggle_fingers_L"
    )
    PoseBone.toggle_fingers_index_L = BoolProperty(
        default=1,
        description="Toggle index finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_index_L"
    )
    PoseBone.toggle_fingers_middle_L = BoolProperty(
        default=1,
        description="Toggle middle finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_middle_L"
    )
    PoseBone.toggle_fingers_ring_L = BoolProperty(
        default=1,
        description="Toggle ring finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_ring_L"
    )
    PoseBone.toggle_fingers_little_L = BoolProperty(
        default=1,
        description="Toggle little finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_little_L"
    )
    PoseBone.toggle_fingers_thumb_L = BoolProperty(
        default=1,
        description="Toggle thumb finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_thumb_L"
    )

    #Toes L
    PoseBone.toggle_toes_L = BoolProperty(
        default=0,
        description="Toggle toes in rig",
        update=lambda self, context: rig_toggles_update(
                self,
                context,
                'toes',
                '_L',
            ),
        name="toggle_toes_L"
    )
    PoseBone.toggle_toes_index_L = BoolProperty(
        default=1,
        description="Toggle index toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_L',
            ),
        name="toggle_toes_index_L"
    )
    PoseBone.toggle_toes_middle_L = BoolProperty(
        default=1,
        description="Toggle middle toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_L',
            ),
        name="toggle_toes_middle_L"
    )
    PoseBone.toggle_toes_fourth_L = BoolProperty(
        default=1,
        description="Toggle fourth toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_L',
            ),
        name="toggle_toes_fourth_L"
    )
    PoseBone.toggle_toes_little_L = BoolProperty(
        default=1,
        description="Toggle little toe in rig",
            update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_L',
            ),
        name="toggle_toe_little_L"
    )
    PoseBone.toggle_toes_big_L = BoolProperty(
        default=1,
        description="Toggle big toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_L',
            ),
        name="toggle_toes_big_L"
    )

    #Fingers R
    PoseBone.toggle_fingers_R = BoolProperty(
        default=0,
        description="Toggle fingers in rig",
        update=lambda self, context: rig_toggles_update(
                self,
                context,
                'fingers',
                '_R',
            ),
        name="toggle_fingers_R"
    )
    PoseBone.toggle_fingers_index_R = BoolProperty(
        default=1,
        description="Toggle index finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_index_R"
    )
    PoseBone.toggle_fingers_middle_R = BoolProperty(
        default=1,
        description="Toggle middle finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_middle_R"
    )
    PoseBone.toggle_fingers_ring_R = BoolProperty(
        default=1,
        description="Toggle ring finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_ring_R"
    )
    PoseBone.toggle_fingers_little_R = BoolProperty(
        default=1,
        description="Toggle little finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_little_R"
    )
    PoseBone.toggle_fingers_thumb_R = BoolProperty(
        default=1,
        description="Toggle thumb finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_thumb_R"
    )

    #Toes R
    PoseBone.toggle_toes_R = BoolProperty(
        default=0,
        description="Toggle toes in rig",
        update=lambda self, context: rig_toggles_update(
                self,
                context,
                'toes',
                '_R',
            ),
        name="toggle_toes_R"
    )
    PoseBone.toggle_toes_index_R = BoolProperty(
        default=1,
        description="Toggle index toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_R',
            ),
        name="toggle_toes_index_R"
    )
    PoseBone.toggle_toes_middle_R = BoolProperty(
        default=1,
        description="Toggle middle toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_R',
            ),
        name="toggle_toes_middle_R"
    )
    PoseBone.toggle_toes_fourth_R = BoolProperty(
        default=1,
        description="Toggle fourth toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_R',
            ),
        name="toggle_toes_fourth_R"
    )
    PoseBone.toggle_toes_little_R = BoolProperty(
        default=1,
        description="Toggle little toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_R',
            ),
        name="toggle_toe_little_R"
    )
    PoseBone.toggle_toes_big_R = BoolProperty(
        default=1,
        description="Toggle big toe in rig",
        update=lambda self, context: toes_toggles_update(
                self,
                context,
                'toes',
                '_R',
            ),
        name="toggle_toes_big_R"
    )

    #### FACIAL PROPERTIES ####

    # EYELIDS

    PoseBone.EYELID_DOWN_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        update=eyelids_update,
        name="EYELID_DOWN_LIMIT_L"
    )

    PoseBone.EYELID_UP_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        update=eyelids_update,
        name="EYELID_UP_LIMIT_L"
    )

    PoseBone.EYELID_OUT_LIMIT_L = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Outwards Movement Limit",
        update=eyelids_update,
        name="EYELID_OUT_LIMIT_L"
    )

    PoseBone.EYELID_IN_LIMIT_L = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Inwards Movement Limit",
        update=eyelids_update,
        name="EYELID_IN_LIMIT_L"
    )

    PoseBone.EYE_DOWN_FOLLOW_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        update=eyelids_update,
        name="EYE_DOWN_FOLLOW_L"
    )

    PoseBone.EYE_UP_FOLLOW_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        update=eyelids_update,
        name="EYE_UP_FOLLOW_L"
    )

    PoseBone.AUTO_CHEEK_L = IntProperty(
        default=0,
        min=0,
        max=1000,
        description="Automaic movement range for when cheek moves up",
        update=eyelids_update,
        name="AUTO_CHEEK_L"
    )

    PoseBone.EYELID_DOWN_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        update=eyelids_update,
        name="EYELID_DOWN_LIMIT_R"
    )

    PoseBone.EYELID_UP_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        update=eyelids_update,
        name="EYELID_UP_LIMIT_R"
    )

    PoseBone.EYELID_OUT_LIMIT_R = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Outwards Movement Limit",
        update=eyelids_update,
        name="EYELID_OUT_LIMIT_R"
    )

    PoseBone.EYELID_IN_LIMIT_R = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Inwards Movement Limit",
        update=eyelids_update,
        name="EYELID_IN_LIMIT_R"
    )

    PoseBone.EYE_DOWN_FOLLOW_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        update=eyelids_update,
        name="EYE_DOWN_FOLLOW_R"
    )

    PoseBone.EYE_UP_FOLLOW_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        update=eyelids_update,
        name="EYE_UP_FOLLOW_R"
    )

    PoseBone.AUTO_CHEEK_R = IntProperty(
        default=0,
        min=0,
        max=1000,
        description="Automaic movement range for when cheek moves up",
        update=eyelids_update,
        name="AUTO_CHEEK_R"
    )

    #FROWNS

    PoseBone.FROWN_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="FROWN_LIMIT_L"
    )

    PoseBone.FROWN_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="FROWN_LIMIT_R"
    )

    PoseBone.FROWN_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="FROWN_LIMIT"
    )

    #CHEEKS

    PoseBone.AUTO_SMILE_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=3,
        description="Automaic movement range for when mouth corner moves up",
        update=cheeks_update,
        name="AUTO_SMILE_L"
    )

    PoseBone.CHEEK_DOWN_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=cheeks_update,
        name="CHEEK_DOWN_LIMIT_L"
    )

    PoseBone.CHEEK_UP_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=cheeks_update,
        name="CHEEK_UP_LIMIT_L"
    )

    PoseBone.AUTO_SMILE_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=3,
        description="Automaic movement range for when mouth corner moves up",
        update=cheeks_update,
        name="AUTO_SMILE_R"
    )

    PoseBone.CHEEK_DOWN_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=cheeks_update,
        name="CHEEK_DOWN_LIMIT_R"
    )

    PoseBone.CHEEK_UP_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=cheeks_update,
        name="CHEEK_UP_LIMIT_R"
    )

    #MOUTH CORNERS

    PoseBone.AUTO_BACK_L = FloatProperty(
        default=0.000,
        min=-1000.000,
        max=1000.000,
        description="Automatic backwards movement when corner moves out",
        update=mouth_corners_update,
        name="AUTO_BACK_L"
    )

    PoseBone.IN_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Inwards movement limit",
        update=mouth_corners_update,
        name="IN_LIMIT_L"
    )

    PoseBone.OUT_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Outwards movement limit",
        update=mouth_corners_update,
        name="OUT_LIMIT_L"
    )

    PoseBone.UP_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=mouth_corners_update,
        name="UP_LIMIT_L"
    )

    PoseBone.DOWN_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=mouth_corners_update,
        name="DOWN_LIMIT_L"
    )

    PoseBone.FORW_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Forwards movement limit",
        update=mouth_corners_update,
        name="FORW_LIMIT_L"
    )

    PoseBone.BACK_LIMIT_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Backwards movement limit",
        update=mouth_corners_update,
        name="BACK_LIMIT_L"
    )

    PoseBone.AUTO_BACK_R = FloatProperty(
        default=0.000,
        min=-1000.000,
        max=1000.000,
        description="Automatic backwards movement when corner moves out",
        update=mouth_corners_update,
        name="AUTO_BACK_R"
    )

    PoseBone.IN_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Inwards movement limit",
        update=mouth_corners_update,
        name="IN_LIMIT_R"
    )

    PoseBone.OUT_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Outwards movement limit",
        update=mouth_corners_update,
        name="OUT_LIMIT_R"
    )

    PoseBone.UP_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=mouth_corners_update,
        name="UP_LIMIT_R"
    )

    PoseBone.DOWN_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=mouth_corners_update,
        name="DOWN_LIMIT_R"
    )

    PoseBone.FORW_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Forwards movement limit",
        update=mouth_corners_update,
        name="FORW_LIMIT_R"
    )

    PoseBone.BACK_LIMIT_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Backwards movement limit",
        update=mouth_corners_update,
        name="BACK_LIMIT_R"
    )

    #MOUTH CTRL

    PoseBone.IN_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Inwards movement limit",
        update=mouth_ctrl_update,
        name="IN_LIMIT"
    )

    PoseBone.OUT_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Outwards movement limit",
        update=mouth_ctrl_update,
        name="OUT_LIMIT"
    )

    PoseBone.SMILE_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Smile rate for mouth_ctrl roatation",
        update=mouth_ctrl_update,
        name="SMILE_LIMIT"
    )

    PoseBone.U_M_CTRL_LIMIT = FloatProperty(
        default=0.02,
        min=0.0001,
        max=1.000,
        precision=3,
        description="Transformation amount for U_M controllers",
        update=mouth_ctrl_update,
        name="U_M_CTRL_LIMIT"
    )

    PoseBone.JAW_ROTATION = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Jaw rotation rate for mouth_ctrl vertical movement",
        update=mouth_ctrl_update,
        name="JAW_ROTATION"
    )

    PoseBone.JAW_DOWN_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Jaw downwards rotation limit",
        update=mouth_ctrl_update,
        name="JAW_DOWN_LIMIT"
    )

    PoseBone.JAW_UP_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Jaw upwards rotation limit",
        update=mouth_ctrl_update,
        name="JAW_UP_LIMIT"
    )

    #REALISTIC JOINTS

    PoseBone.realistic_joints_fingers_rot_L = FloatVectorProperty(
        default=(5.0, 5.0, 5.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_rot_L",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_fingers_loc_L = FloatVectorProperty(
        default=(0.004, 0.004, 0.004),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_loc_L",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_toes_rot_L = FloatVectorProperty(
        default=(4.0, 4.0, 4.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_rot_L",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_toes_loc_L = FloatVectorProperty(
        default=(0.002, 0.002, 0.002),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_loc_L",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_elbow_loc_L = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_loc_L"
    )

    PoseBone.realistic_joints_elbow_rot_L = FloatProperty(
        default=0.000,
        min=-0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_rot_L"
    )

    PoseBone.realistic_joints_wrist_rot_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_wrist_rot_L"
    )

    PoseBone.realistic_joints_ankle_rot_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_ankle_rot_L"
    )

    PoseBone.realistic_joints_knee_loc_L = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_loc_L"
    )

    PoseBone.realistic_joints_knee_rot_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_rot_L"
    )

    PoseBone.realistic_joints_fingers_rot_R = FloatVectorProperty(
        default=(5.0, 5.0, 5.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_rot_R",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_fingers_loc_R = FloatVectorProperty(
        default=(0.004, 0.004, 0.004),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_loc_R",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_toes_rot_R = FloatVectorProperty(
        default=(4.0, 4.0, 4.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_rot_R",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_toes_loc_R = FloatVectorProperty(
        default=(0.002, 0.002, 0.002),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_loc_R",
        subtype='NONE',
        size=3
    )

    PoseBone.realistic_joints_elbow_loc_R = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_loc_R"
    )

    PoseBone.realistic_joints_elbow_rot_R = FloatProperty(
        default=0.000,
        min=-0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_rot_R"
    )

    PoseBone.realistic_joints_wrist_rot_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_wrist_rot_R"
    )

    PoseBone.realistic_joints_ankle_rot_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_ankle_rot_R"
    )

    PoseBone.realistic_joints_knee_loc_R = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_loc_R"
    )

    PoseBone.realistic_joints_knee_rot_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_rot_R"
    )

    # VOLUME VARIATION

    PoseBone.volume_variation_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_arm_L"
    )

    PoseBone.volume_variation_fingers_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_fingers_L"
    )

    PoseBone.volume_variation_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_leg_L"
    )

    PoseBone.volume_variation_toes_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_toes_L"
    )

    PoseBone.volume_variation_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_arm_R"
    )

    PoseBone.volume_variation_fingers_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_fingers_R"
    )

    PoseBone.volume_variation_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_leg_R"
    )

    PoseBone.volume_variation_toes_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_toes_R"
    )

    PoseBone.volume_variation_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_torso"
    )

    PoseBone.volume_variation_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_head"
    )

    PoseBone.volume_variation_neck = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_neck"
    )

    # VOLUME PRESERVATION BONES MOVEMENT

    PoseBone.volume_preservation_fingers_down_L = FloatProperty(
        default=0.025,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_fingers_down_L"
    )

    PoseBone.volume_preservation_knuckles_down_L = FloatProperty(
        default=0.01,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_down_L"
    )

    PoseBone.volume_preservation_knuckles_up_L = FloatProperty(
        default=0.075,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_up_L"
    )

    PoseBone.volume_preservation_palm_down_L = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_palm_down_L"
    )

    PoseBone.volume_preservation_fingers_down_R = FloatProperty(
        default=0.025,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_fingers_down_R"
    )

    PoseBone.volume_preservation_knuckles_down_R = FloatProperty(
        default=0.01,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_down_R"
    )

    PoseBone.volume_preservation_knuckles_up_R = FloatProperty(
        default=0.075,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_up_R"
    )

    PoseBone.volume_preservation_palm_down_R = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_palm_down_R"
    )

    PoseBone.volume_preservation_sole_down_L = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_sole_down_L"
    )

    PoseBone.volume_preservation_toe_knuckles_up_L = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toe_knuckles_up_L"
    )

    PoseBone.volume_preservation_toes_down_L = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toes_down_L"
    )

    PoseBone.volume_preservation_sole_down_R = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_sole_down_R"
    )

    PoseBone.volume_preservation_toe_knuckles_up_R = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toe_knuckles_up_R"
    )

    PoseBone.volume_preservation_toes_down_R = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toes_down_R"
    )


def pbones_props_unregister():
    del PoseBone.ik_head
    del PoseBone.ik_torso
    del PoseBone.inv_torso
    del PoseBone.ik_arm_L
    del PoseBone.ik_arm_R
    del PoseBone.ik_leg_L
    del PoseBone.ik_toes_all_L
    del PoseBone.ik_leg_R
    del PoseBone.ik_toes_all_R
    del PoseBone.ik_fing_ind_L
    del PoseBone.ik_fing_mid_L
    del PoseBone.ik_fing_ring_L
    del PoseBone.ik_fing_lit_L
    del PoseBone.ik_fing_thumb_L
    del PoseBone.ik_fing_ind_R
    del PoseBone.ik_fing_mid_R
    del PoseBone.ik_fing_ring_R
    del PoseBone.ik_fing_lit_R
    del PoseBone.ik_fing_thumb_R
    del PoseBone.ik_fing_all_R
    del PoseBone.ik_fing_all_L
    del PoseBone.hinge_head
    del PoseBone.hinge_neck
    del PoseBone.hinge_arm_L
    del PoseBone.hinge_arm_R
    del PoseBone.hinge_hand_L
    del PoseBone.hinge_hand_R
    del PoseBone.hinge_fing_ind_L
    del PoseBone.hinge_fing_mid_L
    del PoseBone.hinge_fing_ring_L
    del PoseBone.hinge_fing_lit_L
    del PoseBone.hinge_fing_thumb_L
    del PoseBone.hinge_fing_ind_R
    del PoseBone.hinge_fing_mid_R
    del PoseBone.hinge_fing_ring_R
    del PoseBone.hinge_fing_lit_R
    del PoseBone.hinge_fing_thumb_R
    del PoseBone.hinge_fing_all_R
    del PoseBone.hinge_fing_all_L
    del PoseBone.hinge_leg_L
    del PoseBone.hinge_toes_all_L
    del PoseBone.hinge_leg_R
    del PoseBone.hinge_toes_all_R
    del PoseBone.space_head
    del PoseBone.space_neck
    del PoseBone.space_arm_L
    del PoseBone.space_arm_R
    del PoseBone.space_hand_L
    del PoseBone.space_hand_R
    del PoseBone.space_fing_ind_L
    del PoseBone.space_fing_mid_L
    del PoseBone.space_fing_ring_L
    del PoseBone.space_fing_lit_L
    del PoseBone.space_fing_thumb_L
    del PoseBone.space_fing_ind_R
    del PoseBone.space_fing_mid_R
    del PoseBone.space_fing_ring_R
    del PoseBone.space_fing_lit_R
    del PoseBone.space_fing_thumb_R
    del PoseBone.space_fing_all_R
    del PoseBone.space_fing_all_L
    del PoseBone.space_leg_L
    del PoseBone.space_toes_all_L
    del PoseBone.space_leg_R
    del PoseBone.space_toes_all_R
    del PoseBone.space_arm_ik_pole_L
    del PoseBone.space_arm_ik_pole_R
    del PoseBone.space_leg_ik_pole_L
    del PoseBone.space_leg_ik_pole_R
    del PoseBone.toggle_arm_ik_pole_L
    del PoseBone.toggle_arm_ik_pole_R
    del PoseBone.toggle_leg_ik_pole_L
    del PoseBone.toggle_leg_ik_pole_R
    del PoseBone.toon_head
    del PoseBone.toon_torso
    del PoseBone.toon_arm_L
    del PoseBone.toon_arm_R
    del PoseBone.toon_leg_L
    del PoseBone.toon_leg_R
    del PoseBone.toon_fing_thumb_L
    del PoseBone.toon_fing_index_L
    del PoseBone.toon_fing_middle_L
    del PoseBone.toon_fing_ring_L
    del PoseBone.toon_fing_little_L
    del PoseBone.toon_fing_thumb_R
    del PoseBone.toon_fing_index_R
    del PoseBone.toon_fing_middle_R
    del PoseBone.toon_fing_ring_R
    del PoseBone.toon_fing_little_R
    del PoseBone.pin_elbow_L
    del PoseBone.pin_elbow_R
    del PoseBone.pin_knee_L
    del PoseBone.pin_knee_R
    del PoseBone.look_switch
    del PoseBone.toggle_fingers_L
    del PoseBone.toggle_fingers_index_L
    del PoseBone.toggle_fingers_middle_L
    del PoseBone.toggle_fingers_ring_L
    del PoseBone.toggle_fingers_little_L
    del PoseBone.toggle_fingers_thumb_L
    del PoseBone.toggle_toes_L
    del PoseBone.toggle_toes_index_L
    del PoseBone.toggle_toes_middle_L
    del PoseBone.toggle_toes_fourth_L
    del PoseBone.toggle_toes_little_L
    del PoseBone.toggle_toes_big_L
    del PoseBone.toggle_fingers_R
    del PoseBone.toggle_fingers_index_R
    del PoseBone.toggle_fingers_middle_R
    del PoseBone.toggle_fingers_ring_R
    del PoseBone.toggle_fingers_little_R
    del PoseBone.toggle_fingers_thumb_R
    del PoseBone.toggle_toes_R
    del PoseBone.toggle_toes_index_R
    del PoseBone.toggle_toes_middle_R
    del PoseBone.toggle_toes_fourth_R
    del PoseBone.toggle_toes_little_R
    del PoseBone.toggle_toes_big_R
    del PoseBone.EYELID_DOWN_LIMIT_L
    del PoseBone.EYELID_UP_LIMIT_L
    del PoseBone.EYELID_OUT_LIMIT_L
    del PoseBone.EYELID_IN_LIMIT_L
    del PoseBone.EYE_DOWN_FOLLOW_L
    del PoseBone.EYE_UP_FOLLOW_L
    del PoseBone.AUTO_CHEEK_L
    del PoseBone.EYELID_DOWN_LIMIT_R
    del PoseBone.EYELID_UP_LIMIT_R
    del PoseBone.EYELID_OUT_LIMIT_R
    del PoseBone.EYELID_IN_LIMIT_R
    del PoseBone.EYE_DOWN_FOLLOW_R
    del PoseBone.EYE_UP_FOLLOW_R
    del PoseBone.AUTO_CHEEK_R
    del PoseBone.FROWN_LIMIT_L
    del PoseBone.FROWN_LIMIT_R
    del PoseBone.FROWN_LIMIT
    del PoseBone.AUTO_SMILE_L
    del PoseBone.CHEEK_DOWN_LIMIT_L
    del PoseBone.CHEEK_UP_LIMIT_L
    del PoseBone.AUTO_SMILE_R
    del PoseBone.CHEEK_DOWN_LIMIT_R
    del PoseBone.CHEEK_UP_LIMIT_R
    del PoseBone.AUTO_BACK_L
    del PoseBone.IN_LIMIT_L
    del PoseBone.OUT_LIMIT_L
    del PoseBone.UP_LIMIT_L
    del PoseBone.DOWN_LIMIT_L
    del PoseBone.FORW_LIMIT_L
    del PoseBone.BACK_LIMIT_L
    del PoseBone.AUTO_BACK_R
    del PoseBone.IN_LIMIT_R
    del PoseBone.OUT_LIMIT_R
    del PoseBone.UP_LIMIT_R
    del PoseBone.DOWN_LIMIT_R
    del PoseBone.FORW_LIMIT_R
    del PoseBone.BACK_LIMIT_R
    del PoseBone.IN_LIMIT
    del PoseBone.OUT_LIMIT
    del PoseBone.SMILE_LIMIT
    del PoseBone.U_M_CTRL_LIMIT
    del PoseBone.JAW_ROTATION
    del PoseBone.JAW_DOWN_LIMIT
    del PoseBone.JAW_UP_LIMIT
    del PoseBone.realistic_joints_fingers_rot_L
    del PoseBone.realistic_joints_fingers_loc_L
    del PoseBone.realistic_joints_toes_rot_L
    del PoseBone.realistic_joints_toes_loc_L
    del PoseBone.realistic_joints_elbow_loc_L
    del PoseBone.realistic_joints_elbow_rot_L
    del PoseBone.realistic_joints_wrist_rot_L
    del PoseBone.realistic_joints_ankle_rot_L
    del PoseBone.realistic_joints_knee_loc_L
    del PoseBone.realistic_joints_knee_rot_L
    del PoseBone.realistic_joints_fingers_rot_R
    del PoseBone.realistic_joints_fingers_loc_R
    del PoseBone.realistic_joints_toes_rot_R
    del PoseBone.realistic_joints_toes_loc_R
    del PoseBone.realistic_joints_elbow_loc_R
    del PoseBone.realistic_joints_elbow_rot_R
    del PoseBone.realistic_joints_wrist_rot_R
    del PoseBone.realistic_joints_ankle_rot_R
    del PoseBone.realistic_joints_knee_loc_R
    del PoseBone.realistic_joints_knee_rot_R
    del PoseBone.volume_variation_arm_L
    del PoseBone.volume_variation_fingers_L
    del PoseBone.volume_variation_leg_L
    del PoseBone.volume_variation_toes_L
    del PoseBone.volume_variation_arm_R
    del PoseBone.volume_variation_fingers_R
    del PoseBone.volume_variation_leg_R
    del PoseBone.volume_variation_toes_R
    del PoseBone.volume_variation_torso
    del PoseBone.volume_variation_head
    del PoseBone.volume_variation_neck
    del PoseBone.volume_preservation_fingers_down_L
    del PoseBone.volume_preservation_knuckles_down_L
    del PoseBone.volume_preservation_knuckles_up_L
    del PoseBone.volume_preservation_palm_down_L
    del PoseBone.volume_preservation_fingers_down_R
    del PoseBone.volume_preservation_knuckles_down_R
    del PoseBone.volume_preservation_knuckles_up_R
    del PoseBone.volume_preservation_palm_down_R
    del PoseBone.volume_preservation_sole_down_L
    del PoseBone.volume_preservation_toe_knuckles_up_L
    del PoseBone.volume_preservation_toes_down_L
    del PoseBone.volume_preservation_sole_down_R
    del PoseBone.volume_preservation_toe_knuckles_up_R
    del PoseBone.volume_preservation_toes_down_R
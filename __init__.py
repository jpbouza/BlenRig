# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
# ##### ACKNOWLEDGEMENTS #####
#
# BlenRig by: Juan Pablo Bouza
# Initial script programming: Bart Crouch
# Current maintainer and developer: Juan Pablo Bouza, Sav Martin.
#
# Synoptic Panel/Rig Picker based on work by: Salvador Artero
#
# Special thanks on python advice to: Campbell Barton, Bassam Kurdali, Daniel Salazar, CodeManX, Patrick Crawford, Gabriel Caraballo, Ines Almeida
# Special thanks for feedback and ideas to: Jorge Rausch, Gabriel Sabsay, Pablo Vázquez, Hjalti Hjálmarsson, Beorn Leonard, Sarah Laufer
#
# #########################################################################################################

# creo un singleton para no estar leyendo constantemente el file armature_layers.json:
import json
from .singleton import SingletonClass

# bpy.utils.user_resource('SCRIPTS')
# '/home/zebus3d/.config/blender/3.4/scripts'
import os
script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
armature_layers_file = os.path.join(directory, "data_jsons", "armature_layers.json")

# intancio y relleno el singleton:
singleton = SingletonClass()
with open(armature_layers_file, "r") as jsonFile:
    singleton.armature_layers = json.load(jsonFile)

bl_info = {
    'name': 'BlenRig 6',
    'author': 'Juan Pablo Bouza , Sav Martin, Jorge Hernández - Meléndez',
    'version': (2,1,0),
    'blender': (2, 92, 0),
    'location': 'Armature, Object and Lattice properties, View3d tools panel, Armature Add menu',
    'description': 'BlenRig 6 rigging system',
    'wiki_url': 'https://cloud.blender.org/p/blenrig/56966411c379cf44546120e8',
    'tracker_url': 'https://gitlab.com/jpbouza/BlenRig/issues',
    'category': 'Rigging'
}


import bpy
import os
import bl_ui
import bmesh
from mathutils import Vector

from bpy.types import PropertyGroup
from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty,EnumProperty, FloatVectorProperty

# Import panels
from .ui.panels.body_settings import BLENRIG_PT_Rig_Body_settings
from .ui.panels.facial_settings import BLENRIG_PT_Rig_Facial_settings
from .ui.panels.layers_settings import BLENRIG_PT_Rig_Layers_settings
from .ui.panels.dynamic_shaping import BLENRIG_PT_Dynamic_shaping
from .ui.panels.rigging_version_info import BLENRIG_PT_Rig_version_info
from .ui.panels.rigging_optimizations import BLENRIG_PT_Rigging_optimizations
from .ui.panels.rigging_and_baking import BLENRIG_PT_Rigging_and_baking, BLENRIG_PT_baking,BLENRIG_PT_visual_assistant
from .ui.panels.guide_reproportion_assistant import BLENRIG_PT_reproportion_guide
from .ui.panels.guide_datatransfer_assistant import BLENRIG_PT_datatransfer_guide
from .ui.panels.guide_mdef_assistant import BLENRIG_PT_mdef_guide
from .ui.panels.guide_lattices_assistant import BLENRIG_PT_lattices_guide
from .ui.panels.guide_actions_assistant import BLENRIG_PT_actions_guide
from .ui.panels.guide_weights_assistant import BLENRIG_PT_weights_guide
from .ui.panels.guide_rig_settings_assistant import BLENRIG_PT_rig_settings_guide
from .ui.panels.guide_shapekeys_assistant import BLENRIG_PT_shapekeys_guide
from .ui.panels.bodysettings.volume_preservation_bones_movement import *
from .ui.panels.bodysettings.ik import BLENRIG_PT_Rig_Body_settings_ik
from .ui.panels.bodysettings.automated_movement import BLENRIG_PT_Rig_Body_settings_automated_movement
from .ui.panels.bodysettings.realistic_joints import BLENRIG_PT_Rig_Body_settings_realistic_joints
from .ui.panels.bodysettings.bendy_bones_settings import BLENRIG_PT_Rig_Body_settings_bendy_bones_settings
from .ui.panels.bodysettings.body_collisions_offset import BLENRIG_PT_Rig_Body_settings_body_collisions_offset
from .ui.panels.bodysettings.toggles import BLENRIG_PT_Rig_Body_settings_toggles
from .ui.panels.facialsettings.facial_movement_ranges import BLENRIG_PT_Rig_Body_settings_facial_movement_ranges
from .ui.panels.facialsettings.face_action_toggles import BLENRIG_PT_Rig_Body_settings_face_action_toggles
from .ui.panels.facialsettings.face_lip_shaping import BLENRIG_PT_Rig_Body_settings_face_lip_shaping
from .ui.panels.facialsettings.face_collisions import BLENRIG_PT_Rig_Body_settings_face_collisions
from .ui.panels.facialsettings.face_bendy_bones_settings import BLENRIG_PT_Rig_Body_settings_face_bendy_bones_settings
from .boneShapes.panels import *

######### Load Rig Functions ##########
from .rig_functions import *

######### Import all from visual_assistant.py #########
from .visual_assistant import visual_assistant_props
from bpy.app.handlers import persistent


######### Update Function for Properties ##########

def prop_update(self, context):
    bone_auto_hide(context)

def reprop_update(self, context):
    reproportion_toggle(self, context)

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

def state_only_insert_available(self, context):
    get_state_only_insert_available(context)

def get_custom_attribute_from_object(obj, attribute):
    if str(attribute) in obj:
        return obj[attribute]

def snap_points_update(self, context):
    props = context.window_manager.blenrig_6_props.adjust_distance_cage
    active_obj = context.active_object
    bm = bmesh.from_edit_mesh(active_obj.data)
    bm.verts.ensure_lookup_table()
    sel_verts = [v for v in bm.verts if v.select]

    for vert in sel_verts:
        old_co = get_custom_attribute_from_object(active_obj, str(vert.index))
        a = old_co.split()
        old_vec = Vector((float(a[0]),float(a[1]),float(a[2])))
        bm.normal_update()
        vert.co = old_vec + vert.normal*float("%f" % props)
        bmesh.update_edit_mesh(active_obj.data)

    bpy.ops.mesh.select_all(action='DESELECT')
    nombre_vertex_group = 'center_loop'
    bpy.context.active_object.vertex_groups.active = bpy.context.active_object.vertex_groups.get(nombre_vertex_group)
    bpy.ops.object.vertex_group_select()
    bm = bmesh.from_edit_mesh(active_obj.data)
    bm.normal_update()
    sel_center_verts = [v for v in bm.verts if v.select]

    for vert in sel_center_verts:
        vert.co[0] = 0
        vert.select = False
        bm.normal_update()
        bmesh.update_edit_mesh(active_obj.data)

    for vert in sel_verts:
        vert.select= True
        bmesh.update_edit_mesh(active_obj.data)

######### Handler for update on load and frame change #########

# from bpy.app.handlers import persistent

@persistent
def load_reprop_handler(self, context):
    bone_auto_hide(context)
    reproportion_toggle(self, context)


@persistent
def load_handler(context):
    bone_auto_hide(context)

@persistent
def load_state_only_insert_available(self, context):
    state_only_insert_available(self, context)


bpy.app.handlers.load_post.append(load_reprop_handler)
bpy.app.handlers.frame_change_post.append(load_handler)
bpy.app.handlers.load_post.append(load_state_only_insert_available)


######### Properties Creation ############

#FK/IK

bpy.types.PoseBone.ik_head = FloatProperty(
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

bpy.types.PoseBone.ik_torso = FloatProperty(
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
bpy.types.PoseBone.inv_torso = FloatProperty(
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
bpy.types.PoseBone.ik_arm_L = FloatProperty(
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
bpy.types.PoseBone.ik_arm_R = FloatProperty(
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
bpy.types.PoseBone.ik_leg_L = FloatProperty(
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
bpy.types.PoseBone.ik_toes_all_L = FloatProperty(
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
bpy.types.PoseBone.ik_leg_R = FloatProperty(
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
bpy.types.PoseBone.ik_toes_all_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_ind_L = FloatProperty(
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
bpy.types.PoseBone.ik_fing_mid_L = FloatProperty(
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
bpy.types.PoseBone.ik_fing_ring_L = FloatProperty(
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
bpy.types.PoseBone.ik_fing_lit_L = FloatProperty(
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
bpy.types.PoseBone.ik_fing_thumb_L = FloatProperty(
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
bpy.types.PoseBone.ik_fing_ind_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_mid_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_ring_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_lit_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_thumb_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_all_R = FloatProperty(
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
bpy.types.PoseBone.ik_fing_all_L = FloatProperty(
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

bpy.types.PoseBone.hinge_head = FloatProperty(
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
bpy.types.PoseBone.hinge_neck = FloatProperty(
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
bpy.types.PoseBone.hinge_arm_L = FloatProperty(
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
bpy.types.PoseBone.hinge_arm_R = FloatProperty(
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
bpy.types.PoseBone.hinge_hand_L = FloatProperty(
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
bpy.types.PoseBone.hinge_hand_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_ind_L = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_mid_L = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_ring_L = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_lit_L = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_thumb_L = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_ind_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_mid_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_ring_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_lit_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_thumb_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_all_R = FloatProperty(
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
bpy.types.PoseBone.hinge_fing_all_L = FloatProperty(
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
bpy.types.PoseBone.hinge_leg_L = FloatProperty(
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
bpy.types.PoseBone.hinge_toes_all_L = FloatProperty(
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
bpy.types.PoseBone.hinge_leg_R = FloatProperty(
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
bpy.types.PoseBone.hinge_toes_all_R = FloatProperty(
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

bpy.types.PoseBone.space_head = FloatProperty(
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
bpy.types.PoseBone.space_neck = FloatProperty(
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
bpy.types.PoseBone.space_arm_L = FloatProperty(
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
bpy.types.PoseBone.space_arm_R = FloatProperty(
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
bpy.types.PoseBone.space_hand_L = FloatProperty(
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
bpy.types.PoseBone.space_hand_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_ind_L = FloatProperty(
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
bpy.types.PoseBone.space_fing_mid_L = FloatProperty(
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
bpy.types.PoseBone.space_fing_ring_L = FloatProperty(
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
bpy.types.PoseBone.space_fing_lit_L = FloatProperty(
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
bpy.types.PoseBone.space_fing_thumb_L = FloatProperty(
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
bpy.types.PoseBone.space_fing_ind_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_mid_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_ring_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_lit_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_thumb_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_all_R = FloatProperty(
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
bpy.types.PoseBone.space_fing_all_L = FloatProperty(
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
bpy.types.PoseBone.space_leg_L = FloatProperty(
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
bpy.types.PoseBone.space_toes_all_L = FloatProperty(
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
bpy.types.PoseBone.space_leg_R = FloatProperty(
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
bpy.types.PoseBone.space_toes_all_R = FloatProperty(
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

bpy.types.PoseBone.space_arm_ik_pole_L = FloatProperty(
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
bpy.types.PoseBone.space_arm_ik_pole_R = FloatProperty(
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
bpy.types.PoseBone.space_leg_ik_pole_L = FloatProperty(
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
bpy.types.PoseBone.space_leg_ik_pole_R = FloatProperty(
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
bpy.types.PoseBone.toggle_arm_ik_pole_L = BoolProperty(
    default=0,
    description="Toggle pole Target",
    override={'LIBRARY_OVERRIDABLE'},
    update=pole_toggles_update,
    name="toggle_arm_ik_pole_L"
)
bpy.types.PoseBone.toggle_arm_ik_pole_R = BoolProperty(
    default=0,
    description="Toggle pole Target",
    override={'LIBRARY_OVERRIDABLE'},
    update=pole_toggles_update,
    name="toggle_arm_ik_pole_R"
)
bpy.types.PoseBone.toggle_leg_ik_pole_L = BoolProperty(
    default=0,
    description="Toggle pole Target",
    override={'LIBRARY_OVERRIDABLE'},
    update=pole_toggles_update,
    name="toggle_leg_ik_pole_L"
)
bpy.types.PoseBone.toggle_leg_ik_pole_R = BoolProperty(
    default=0,
    description="Toggle pole Target",
    override={'LIBRARY_OVERRIDABLE'},
    update=pole_toggles_update,
    name="toggle_leg_ik_pole_R"
)

#Stretchy IK

bpy.types.PoseBone.toon_head = FloatProperty(
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

bpy.types.PoseBone.toon_torso = FloatProperty(
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

bpy.types.PoseBone.toon_arm_L = FloatProperty(
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

bpy.types.PoseBone.toon_arm_R = FloatProperty(
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

bpy.types.PoseBone.toon_leg_L = FloatProperty(
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

bpy.types.PoseBone.toon_leg_R = FloatProperty(
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

bpy.types.PoseBone.toon_fing_thumb_L = FloatProperty(
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

bpy.types.PoseBone.toon_fing_index_L = FloatProperty(
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

bpy.types.PoseBone.toon_fing_middle_L = FloatProperty(
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

bpy.types.PoseBone.toon_fing_ring_L = FloatProperty(
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

bpy.types.PoseBone.toon_fing_little_L = FloatProperty(
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

bpy.types.PoseBone.toon_fing_thumb_R = FloatProperty(
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

bpy.types.PoseBone.toon_fing_index_R = FloatProperty(
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

bpy.types.PoseBone.toon_fing_middle_R = FloatProperty(
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

bpy.types.PoseBone.toon_fing_ring_R = FloatProperty(
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

bpy.types.PoseBone.toon_fing_little_R = FloatProperty(
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

bpy.types.PoseBone.pin_elbow_L = FloatProperty(
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

bpy.types.PoseBone.pin_elbow_R = FloatProperty(
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

bpy.types.PoseBone.pin_knee_L = FloatProperty(
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

bpy.types.PoseBone.pin_knee_R = FloatProperty(
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
bpy.types.PoseBone.look_switch = FloatProperty(
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

# REPROPORTION
bpy.types.Armature.reproportion = BoolProperty(
    default=0,
    description="Toggle Reproportion Mode",
    update=reprop_update,
    name="reproportion"
)
# TOGGLE_FACE_DRIVERS
bpy.types.Armature.toggle_face_drivers = BoolProperty(
    default=1,
    description="Toggle Face Riggin Drivers",
    update=optimize_face,
    name="toggle_face_drivers"
)
# TOGGLE_DYNAMIC_DRIVERS
bpy.types.Armature.toggle_flex_drivers = BoolProperty(
    default=1,
    description="Toggle Flex Drivers",
    update=optimize_flex,
    name="toggle_flex_drivers"
)
# TOGGLE_DYNAMIC_DRIVERS
bpy.types.Armature.toggle_dynamic_drivers = BoolProperty(
    default=1,
    description="Toggle Dynamic Shaping Drivers",
    update=optimize_dynamic,
    name="toggle_dynamic_drivers"
)
# TOGGLE_BODY_DRIVERS
bpy.types.Armature.toggle_body_drivers = BoolProperty(
    default=1,
    description="Toggle Body Rigging Drivers",
    update=optimize_body,
    name="toggle_body_drivers"
)
### TOGGLES
#Fingers L
bpy.types.PoseBone.toggle_fingers_L = BoolProperty(
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
bpy.types.PoseBone.toggle_fingers_index_L = BoolProperty(
    default=1,
    description="Toggle index finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_index_L"
)
bpy.types.PoseBone.toggle_fingers_middle_L = BoolProperty(
    default=1,
    description="Toggle middle finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_middle_L"
)
bpy.types.PoseBone.toggle_fingers_ring_L = BoolProperty(
    default=1,
    description="Toggle ring finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_ring_L"
)
bpy.types.PoseBone.toggle_fingers_little_L = BoolProperty(
    default=1,
    description="Toggle little finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_little_L"
)
bpy.types.PoseBone.toggle_fingers_thumb_L = BoolProperty(
    default=1,
    description="Toggle thumb finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_thumb_L"
)

#Toes L
bpy.types.PoseBone.toggle_toes_L = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_index_L = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_middle_L = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_fourth_L = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_little_L = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_big_L = BoolProperty(
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
bpy.types.PoseBone.toggle_fingers_R = BoolProperty(
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
bpy.types.PoseBone.toggle_fingers_index_R = BoolProperty(
    default=1,
    description="Toggle index finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_index_R"
)
bpy.types.PoseBone.toggle_fingers_middle_R = BoolProperty(
    default=1,
    description="Toggle middle finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_middle_R"
)
bpy.types.PoseBone.toggle_fingers_ring_R = BoolProperty(
    default=1,
    description="Toggle ring finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_ring_R"
)
bpy.types.PoseBone.toggle_fingers_little_R = BoolProperty(
    default=1,
    description="Toggle little finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_little_R"
)
bpy.types.PoseBone.toggle_fingers_thumb_R = BoolProperty(
    default=1,
    description="Toggle thumb finger in rig",
    update=fingers_toggles_update,
    name="toggle_fingers_thumb_R"
)

#Toes R
bpy.types.PoseBone.toggle_toes_R = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_index_R = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_middle_R = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_fourth_R = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_little_R = BoolProperty(
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
bpy.types.PoseBone.toggle_toes_big_R = BoolProperty(
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

bpy.types.PoseBone.EYELID_DOWN_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upper Eyelid Downwards Movement Limit",
    update=eyelids_update,
    name="EYELID_DOWN_LIMIT_L"
)

bpy.types.PoseBone.EYELID_UP_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upper Eyelid Upwards Movement Limit",
    update=eyelids_update,
    name="EYELID_UP_LIMIT_L"
)

bpy.types.PoseBone.EYELID_OUT_LIMIT_L = FloatProperty(
    default=60.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Eyelid Outwards Movement Limit",
    update=eyelids_update,
    name="EYELID_OUT_LIMIT_L"
)

bpy.types.PoseBone.EYELID_IN_LIMIT_L = FloatProperty(
    default=60.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Eyelid Inwards Movement Limit",
    update=eyelids_update,
    name="EYELID_IN_LIMIT_L"
)

bpy.types.PoseBone.EYE_DOWN_FOLLOW_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Automatic movement for when eye looks down",
    update=eyelids_update,
    name="EYE_DOWN_FOLLOW_L"
)

bpy.types.PoseBone.EYE_UP_FOLLOW_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Automatic movement for when eye looks up",
    update=eyelids_update,
    name="EYE_UP_FOLLOW_L"
)

bpy.types.PoseBone.AUTO_CHEEK_L = IntProperty(
    default=0,
    min=0,
    max=1000,
    description="Automaic movement range for when cheek moves up",
    update=eyelids_update,
    name="AUTO_CHEEK_L"
)

bpy.types.PoseBone.EYELID_DOWN_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upper Eyelid Downwards Movement Limit",
    update=eyelids_update,
    name="EYELID_DOWN_LIMIT_R"
)

bpy.types.PoseBone.EYELID_UP_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upper Eyelid Upwards Movement Limit",
    update=eyelids_update,
    name="EYELID_UP_LIMIT_R"
)

bpy.types.PoseBone.EYELID_OUT_LIMIT_R = FloatProperty(
    default=60.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Eyelid Outwards Movement Limit",
    update=eyelids_update,
    name="EYELID_OUT_LIMIT_R"
)

bpy.types.PoseBone.EYELID_IN_LIMIT_R = FloatProperty(
    default=60.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Eyelid Inwards Movement Limit",
    update=eyelids_update,
    name="EYELID_IN_LIMIT_R"
)

bpy.types.PoseBone.EYE_DOWN_FOLLOW_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Automatic movement for when eye looks down",
    update=eyelids_update,
    name="EYE_DOWN_FOLLOW_R"
)

bpy.types.PoseBone.EYE_UP_FOLLOW_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Automatic movement for when eye looks up",
    update=eyelids_update,
    name="EYE_UP_FOLLOW_R"
)

bpy.types.PoseBone.AUTO_CHEEK_R = IntProperty(
    default=0,
    min=0,
    max=1000,
    description="Automaic movement range for when cheek moves up",
    update=eyelids_update,
    name="AUTO_CHEEK_R"
)

#FROWNS

bpy.types.PoseBone.FROWN_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Transform range for frown action",
    update=frowns_update,
    name="FROWN_LIMIT_L"
)

bpy.types.PoseBone.FROWN_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Transform range for frown action",
    update=frowns_update,
    name="FROWN_LIMIT_R"
)

bpy.types.PoseBone.FROWN_LIMIT = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Transform range for frown action",
    update=frowns_update,
    name="FROWN_LIMIT"
)

#CHEEKS

bpy.types.PoseBone.AUTO_SMILE_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=3,
    description="Automaic movement range for when mouth corner moves up",
    update=cheeks_update,
    name="AUTO_SMILE_L"
)

bpy.types.PoseBone.CHEEK_DOWN_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Downwards movement limit",
    update=cheeks_update,
    name="CHEEK_DOWN_LIMIT_L"
)

bpy.types.PoseBone.CHEEK_UP_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upwards movement limit",
    update=cheeks_update,
    name="CHEEK_UP_LIMIT_L"
)

bpy.types.PoseBone.AUTO_SMILE_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=3,
    description="Automaic movement range for when mouth corner moves up",
    update=cheeks_update,
    name="AUTO_SMILE_R"
)

bpy.types.PoseBone.CHEEK_DOWN_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Downwards movement limit",
    update=cheeks_update,
    name="CHEEK_DOWN_LIMIT_R"
)

bpy.types.PoseBone.CHEEK_UP_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upwards movement limit",
    update=cheeks_update,
    name="CHEEK_UP_LIMIT_R"
)

#MOUTH CORNERS

bpy.types.PoseBone.AUTO_BACK_L = FloatProperty(
    default=0.000,
    min=-1000.000,
    max=1000.000,
    description="Automatic backwards movement when corner moves out",
    update=mouth_corners_update,
    name="AUTO_BACK_L"
)

bpy.types.PoseBone.IN_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Inwards movement limit",
    update=mouth_corners_update,
    name="IN_LIMIT_L"
)

bpy.types.PoseBone.OUT_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Outwards movement limit",
    update=mouth_corners_update,
    name="OUT_LIMIT_L"
)

bpy.types.PoseBone.UP_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upwards movement limit",
    update=mouth_corners_update,
    name="UP_LIMIT_L"
)

bpy.types.PoseBone.DOWN_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Downwards movement limit",
    update=mouth_corners_update,
    name="DOWN_LIMIT_L"
)

bpy.types.PoseBone.FORW_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Forwards movement limit",
    update=mouth_corners_update,
    name="FORW_LIMIT_L"
)

bpy.types.PoseBone.BACK_LIMIT_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Backwards movement limit",
    update=mouth_corners_update,
    name="BACK_LIMIT_L"
)

bpy.types.PoseBone.AUTO_BACK_R = FloatProperty(
    default=0.000,
    min=-1000.000,
    max=1000.000,
    description="Automatic backwards movement when corner moves out",
    update=mouth_corners_update,
    name="AUTO_BACK_R"
)

bpy.types.PoseBone.IN_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Inwards movement limit",
    update=mouth_corners_update,
    name="IN_LIMIT_R"
)

bpy.types.PoseBone.OUT_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Outwards movement limit",
    update=mouth_corners_update,
    name="OUT_LIMIT_R"
)

bpy.types.PoseBone.UP_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Upwards movement limit",
    update=mouth_corners_update,
    name="UP_LIMIT_R"
)

bpy.types.PoseBone.DOWN_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Downwards movement limit",
    update=mouth_corners_update,
    name="DOWN_LIMIT_R"
)

bpy.types.PoseBone.FORW_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Forwards movement limit",
    update=mouth_corners_update,
    name="FORW_LIMIT_R"
)

bpy.types.PoseBone.BACK_LIMIT_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Backwards movement limit",
    update=mouth_corners_update,
    name="BACK_LIMIT_R"
)

#MOUTH CTRL

bpy.types.PoseBone.IN_LIMIT = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Inwards movement limit",
    update=mouth_ctrl_update,
    name="IN_LIMIT"
)

bpy.types.PoseBone.OUT_LIMIT = FloatProperty(
    default=0.000,
    min=0.000,
    max=10.000,
    precision=3,
    description="Outwards movement limit",
    update=mouth_ctrl_update,
    name="OUT_LIMIT"
)

bpy.types.PoseBone.SMILE_LIMIT = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Smile rate for mouth_ctrl roatation",
    update=mouth_ctrl_update,
    name="SMILE_LIMIT"
)

bpy.types.PoseBone.U_M_CTRL_LIMIT = FloatProperty(
    default=0.02,
    min=0.0001,
    max=1.000,
    precision=3,
    description="Transformation amount for U_M controllers",
    update=mouth_ctrl_update,
    name="U_M_CTRL_LIMIT"
)

bpy.types.PoseBone.JAW_ROTATION = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Jaw rotation rate for mouth_ctrl vertical movement",
    update=mouth_ctrl_update,
    name="JAW_ROTATION"
)

bpy.types.PoseBone.JAW_DOWN_LIMIT = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Jaw downwards rotation limit",
    update=mouth_ctrl_update,
    name="JAW_DOWN_LIMIT"
)

bpy.types.PoseBone.JAW_UP_LIMIT = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="Jaw upwards rotation limit",
    update=mouth_ctrl_update,
    name="JAW_UP_LIMIT"
)

#REALISTIC JOINTS

bpy.types.PoseBone.realistic_joints_fingers_rot_L = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_fingers_loc_L = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_toes_rot_L = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_toes_loc_L = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_elbow_loc_L = FloatProperty(
    default=0.000,
    min=-10.000,
    max=10.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_elbow_loc_L"
)

bpy.types.PoseBone.realistic_joints_elbow_rot_L = FloatProperty(
    default=0.000,
    min=-0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_elbow_rot_L"
)

bpy.types.PoseBone.realistic_joints_wrist_rot_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_wrist_rot_L"
)

bpy.types.PoseBone.realistic_joints_ankle_rot_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_ankle_rot_L"
)

bpy.types.PoseBone.realistic_joints_knee_loc_L = FloatProperty(
    default=0.000,
    min=-10.000,
    max=10.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_knee_loc_L"
)

bpy.types.PoseBone.realistic_joints_knee_rot_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_knee_rot_L"
)

bpy.types.PoseBone.realistic_joints_fingers_rot_R = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_fingers_loc_R = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_toes_rot_R = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_toes_loc_R = FloatVectorProperty(
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

bpy.types.PoseBone.realistic_joints_elbow_loc_R = FloatProperty(
    default=0.000,
    min=-10.000,
    max=10.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_elbow_loc_R"
)

bpy.types.PoseBone.realistic_joints_elbow_rot_R = FloatProperty(
    default=0.000,
    min=-0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_elbow_rot_R"
)

bpy.types.PoseBone.realistic_joints_wrist_rot_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_wrist_rot_R"
)

bpy.types.PoseBone.realistic_joints_ankle_rot_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_ankle_rot_R"
)

bpy.types.PoseBone.realistic_joints_knee_loc_R = FloatProperty(
    default=0.000,
    min=-10.000,
    max=10.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_knee_loc_R"
)

bpy.types.PoseBone.realistic_joints_knee_rot_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=180.000,
    precision=3,
    description="joint displacement simulation",
    update=rj_transforms_update,
    name="realistic_joints_knee_rot_R"
)

# VOLUME VARIATION

bpy.types.PoseBone.volume_variation_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_arm_L"
)

bpy.types.PoseBone.volume_variation_fingers_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_fingers_L"
)

bpy.types.PoseBone.volume_variation_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_leg_L"
)

bpy.types.PoseBone.volume_variation_toes_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_toes_L"
)

bpy.types.PoseBone.volume_variation_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_arm_R"
)

bpy.types.PoseBone.volume_variation_fingers_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_fingers_R"
)

bpy.types.PoseBone.volume_variation_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_leg_R"
)

bpy.types.PoseBone.volume_variation_toes_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_toes_R"
)

bpy.types.PoseBone.volume_variation_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_torso"
)

bpy.types.PoseBone.volume_variation_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_head"
)

bpy.types.PoseBone.volume_variation_neck = FloatProperty(
    default=0.000,
    min=0.000,
    max=100.000,
    precision=3,
    description="Volume Variation for stretch and squash",
    update=vol_variation_update,
    name="volume_variation_neck"
)

# VOLUME PRESERVATION BONES MOVEMENT

bpy.types.PoseBone.volume_preservation_fingers_down_L = FloatProperty(
    default=0.025,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_fingers_down_L"
)

bpy.types.PoseBone.volume_preservation_knuckles_down_L = FloatProperty(
    default=0.01,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_knuckles_down_L"
)

bpy.types.PoseBone.volume_preservation_knuckles_up_L = FloatProperty(
    default=0.075,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_knuckles_up_L"
)

bpy.types.PoseBone.volume_preservation_palm_down_L = FloatProperty(
    default=0.05,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_palm_down_L"
)

bpy.types.PoseBone.volume_preservation_fingers_down_R = FloatProperty(
    default=0.025,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_fingers_down_R"
)

bpy.types.PoseBone.volume_preservation_knuckles_down_R = FloatProperty(
    default=0.01,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_knuckles_down_R"
)

bpy.types.PoseBone.volume_preservation_knuckles_up_R = FloatProperty(
    default=0.075,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_knuckles_up_R"
)

bpy.types.PoseBone.volume_preservation_palm_down_R = FloatProperty(
    default=0.05,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_palm_down_R"
)

bpy.types.PoseBone.volume_preservation_sole_down_L = FloatProperty(
    default=0.1,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_sole_down_L"
)

bpy.types.PoseBone.volume_preservation_toe_knuckles_up_L = FloatProperty(
    default=0.1,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_toe_knuckles_up_L"
)

bpy.types.PoseBone.volume_preservation_toes_down_L = FloatProperty(
    default=0.05,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_toes_down_L"
)

bpy.types.PoseBone.volume_preservation_sole_down_R = FloatProperty(
    default=0.1,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_sole_down_R"
)

bpy.types.PoseBone.volume_preservation_toe_knuckles_up_R = FloatProperty(
    default=0.1,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_toe_knuckles_up_R"
)

bpy.types.PoseBone.volume_preservation_toes_down_R = FloatProperty(
    default=0.05,
    min=0.000,
    max=10.000,
    precision=3,
    description="Volume Preservation Bones Movement Rage",
    update=vol_prservation_update,
    name="volume_preservation_toes_down_R"
)

####### Load BlenRig 6 Controls Panel
from .ui.panels.ui_legacy_panel_controls import BLENRIG_PT_legacy_blenrig_5_Interface
from .ui.panels.ui_panel_blenrig import BLENRIG_PT_blenrig_6_general,BLENRIG_PT_blenrig_6_general_SubPanel
from .ui.panels.ui_panel_controls import BLENRIG_PT_blenrig_6_Interface
from .ui.panels.ui_legacy_panel_controls_1_5 import BLENRIG_PT_legacy_blenrig_5_5_Interface
from .snap_points import BLENRIG_OT_SnapPoints,BLENRIG_OT_center_loop_cage
from .ui.panels.cage_snapping_panel import BLENRIG_PT_Cage_snapping_panel

####### Load BlenRig 6 Rigging Panel
from .ui.panels.ui_legacy_panel_rigging import BLENRIG_PT_legacy_blenrig_5_rigging_panel

####### Load BlenRig 6 Objects Panel
from .ui.panels.ui_panel_objects import (
    BLENRIG_PT_blenrig_6_mesh_panel,
    BLENRIG_PT_blenrig_6_lattice_panel
    )

####### Load BlenRig 6 Boneshapes Operators and Preferences
from .boneShapes.operators import (
    BLENRIG_OT_removeShapes,
    BLENRIG_OT_addShapes,
    BLENRIG_OT_matchSymmetrizeShape,
    BLENRIG_OT_matchBoneTransforms,
    BLENRIG_OT_returnToArmature,
    BLENRIG_OT_editShapes,
    BLENRIG_OT_createShapes,
    BLENRIG_OT_toggleCollectionVisibility,
    BLENRIG_OT_deleteUnusedShapes,
    BLENRIG_OT_clearBoneShapes,
    BLENRIG_OT_resyncShapesNames,
    BLENRIG_OT_shape_scale,
    BLENRIG_OT_Make_Unique
)
from .boneShapes.prefs import (BoneShapesPreferences)

####### Load BlenRig 6 Shape Keys+ Operators and Preferences

from .shape_Keys.shape_keys_plus import (
    Selection,
    KeyProperties,
    SceneProperties,
    OBJECT_OT_blenrig_folder_icon,
    OBJECT_OT_blenrig_shape_key_parent,
    OBJECT_OT_blenrig_shape_key_add,
    OBJECT_OT_blenrig_shape_key_remove,
    OBJECT_OT_blenrig_shape_key_copy,
    OBJECT_OT_blenrig_shape_key_move,
    OBJECT_OT_blenrig_shape_key_select,
    OBJECT_OT_blenrig_folder_toggle,
    OBJECT_OT_blenrig_folder_ungroup,
    DRIVER_OT_blenrig_driver_update,
    DRIVER_OT_blenrig_variable_add,
    DRIVER_OT_blenrig_variable_remove,
    DRIVER_OT_blenrig_variable_copy,
    DRIVER_OT_blenrig_variable_move,
    OBJECT_OT_blenrig_debug_folder_data
)
from .shape_Keys.panels import (
    MESH_MT_blenrig_shape_key_add_specials,
    MESH_MT_blenrig_shape_key_add_specials_selected,
    MESH_MT_blenrig_shape_key_copy_specials,
    MESH_MT_blenrig_shape_key_copy_specials_selected,
    # MESH_MT_blenrig_shape_key_remove_specials,
    # MESH_MT_blenrig_shape_key_remove_specials_selected,
    MESH_MT_blenrig_shape_key_other_specials,
    MESH_MT_blenrig_shape_key_other_specials_selected,
    OBJECT_MT_blenrig_shape_key_parent,
    OBJECT_MT_blenrig_shape_key_parent_selected,
    OBJECT_MT_blenrig_folder_icon,
    OBJECT_MT_blenrig_folder_icons_standard,
    OBJECT_MT_blenrig_folder_icons_special,
    OBJECT_MT_blenrig_folder_icons_misc,
    MESH_UL_BlenRig_shape_keys_plus,
    BLENRIG_PT_shape_keys_plus
)

####### Load BlenRig 6 Bake Operators
from .ops_baking import (
    ARMATURE_OT_mesh_pose_baker,
    ARMATURE_OT_reset_hooks,
    ARMATURE_OT_disable_hooks_modif,
    ARMATURE_OT_reset_deformers,
    ARMATURE_OT_advanced_armature_baker,
    ARMATURE_OT_armature_baker_all_part_1,
    ARMATURE_OT_armature_baker_all_part_2,
    ARMATURE_OT_reset_constraints
    )

####### Load BlenRig 6 Alignment Operators
from .ops_alignment import (
    Operator_BlenRig_Fix_Misaligned_Bones,
    Operator_BlenRig_Auto_Bone_Roll,
    Operator_BlenRig_Custom_Bone_Roll,
    Operator_BlenRig_Store_Roll_Angles,
    Operator_BlenRig_Restore_Roll_Angles,
    Operator_BlenRig_Reset_Dynamic,
    Operator_Mirror_VP_Constraints,
    Operator_Mirror_RJ_Constraints,
    Operator_blenrig_calculate_pole_angles,
    Operator_blenrig_calculate_floor_offsets
    )

####### Load BlenRig 6 Snapping Operators
from .ops_snapping import (
    Operator_Snap_TorsoFKtoIK,
    Operator_Snap_TorsoIKtoFK,
    Operator_Align_Spine,
    Operator_Knee_UnPin_L,
    Operator_Knee_UnPin_R,
    Operator_Knee_Pin_L,
    Operator_Knee_Pin_R,
    Operator_Elbow_UnPin_R,
    Operator_Elbow_UnPin_L,
    Operator_Elbow_Pin_L,
    Operator_Elbow_Pin_R,
    Operator_Reset_Master_Pivot,
    Operator_Reset_Master_Body_Pivot,
    Operator_Reset_Master_Torso_Pivot,
    Operator_Reset_Hand_R_Pivot,
    Operator_Reset_Hand_L_Pivot,
    Operator_Switch_Fing_Lit_Space_R,
    Operator_Show_Fing_Lit_Space_List_R,
    Operator_Switch_Fing_Ring_Space_R,
    Operator_Show_Fing_Ring_Space_List_R,
    Operator_Switch_Fing_Mid_Space_R,
    Operator_Show_Fing_Mid_Space_List_R,
    Operator_Switch_Fing_Ind_Space_R,
    Operator_Show_Fing_Ind_Space_List_R,
    Operator_Switch_Fing_Thumb_Space_R,
    Operator_Show_Fing_Thumb_Space_List_R,
    Operator_Switch_Fing_All_Space_R,
    Operator_Show_Fing_All_Space_List_R,
    Operator_Switch_Fing_Lit_Space_L,
    Operator_Show_Fing_Lit_Space_List_L,
    Operator_Switch_Fing_Ring_Space_L,
    Operator_Show_Fing_Ring_Space_List_L,
    Operator_Switch_Fing_Mid_Space_L,
    Operator_Show_Fing_Mid_Space_List_L,
    Operator_Switch_Fing_Ind_Space_L,
    Operator_Show_Fing_Ind_Space_List_L,
    Operator_Switch_Fing_Thumb_Space_L,
    Operator_Show_Fing_Thumb_Space_List_L,
    Operator_Switch_Fing_All_Space_L,
    Operator_Show_Fing_All_Space_List_L,
    Operator_Switch_Look_Space,
    Operator_Show_Look_Space_List,
    Operator_Switch_Neck_Space,
    Operator_Show_Neck_Space_List,
    Operator_Switch_Head_Space,
    Operator_Show_Head_Space_List,
    Operator_Switch_Hand_Accessory_Space,
    Operator_Show_Hand_Accessory_Space_List,
    Operator_Switch_Hat_Space,
    Operator_Show_Hat_Space_List,
    Operator_Switch_Eyeglasses_Space,
    Operator_Show_Eyeglasses_Space_List,
    Operator_Switch_Leg_Pole_Space_L,
    Operator_Show_Leg_Pole_Space_List_L,
    Operator_Switch_Arm_Pole_Space_L,
    Operator_Show_Arm_Pole_Space_List_L,
    Operator_Switch_Leg_Space_L,
    Operator_Show_Leg_Space_List_L,
    Operator_Snap_LegIKtoFK_L,
    Operator_Snap_LegFKtoIK_L,
    Operator_Switch_Hand_Space_L,
    Operator_Show_Hand_Space_List_L,
    Operator_Switch_Arm_Space_L,
    Operator_Show_Arm_Space_List_L,
    Operator_Snap_ArmIKtoFK_L,
    Operator_Snap_ArmFKtoIK_L,
    Operator_Switch_Leg_Pole_Space_R,
    Operator_Show_Leg_Pole_Space_List_R,
    Operator_Switch_Arm_Pole_Space_R,
    Operator_Show_Arm_Pole_Space_List_R,
    Operator_Switch_Leg_Space_R,
    Operator_Show_Leg_Space_List_R,
    Operator_Snap_LegIKtoFK_R,
    Operator_Snap_LegFKtoIK_R,
    Operator_Switch_Hand_Space_R,
    Operator_Show_Hand_Space_List_R,
    Operator_Switch_Arm_Space_R,
    Operator_Show_Arm_Space_List_R,
    Operator_Snap_ArmIKtoFK_R,
    Operator_Snap_ArmFKtoIK_R,
    Operator_Torso_Snap_FK_IK,
    Operator_Torso_Snap_IK_FK,
    Operator_Head_Snap_FK_IK,
    Operator_Head_Snap_IK_FK,
    Operator_Torso_Snap_UP_INV,
    Operator_Torso_Snap_INV_UP,
    Operator_Arm_L_Snap_FK_IK,
    Operator_Arm_L_Snap_IK_FK,
    Operator_Arm_R_Snap_FK_IK,
    Operator_Arm_R_Snap_IK_FK,
    Operator_Leg_L_Snap_FK_IK,
    Operator_Leg_L_Snap_IK_FK,
    Operator_Leg_R_Snap_FK_IK,
    Operator_Leg_R_Snap_IK_FK
    )

####### Load BlenRig 6 Body Picker Operators
# Biped
from .ops_picker_body import (
    Operator_Keyframe_Main_Props,
    Operator_Head_Stretch,
    Operator_Head_Toon,
    Operator_Head_Top_Ctrl,
    Operator_Head_Mid_Ctrl,
    Operator_Head_Mid_Curve,
    Operator_Mouth_Str_Ctrl,
    Operator_Head_FK,
    Operator_Head_IK,
    Operator_Neck_4_Toon,
    Operator_Face_Toon_Up,
    Operator_Face_Toon_Mid,
    Operator_Face_Toon_Low,
    Operator_Neck_3_Legacy,
    Operator_Neck_2_Legacy,
    Operator_Neck_3,
    Operator_Neck_2,
    Operator_Neck_1,
    Operator_Neck_3_Toon,
    Operator_Neck_2_Toon,
    Operator_Neck_Ctrl_Legacy,
    Operator_Neck_Ctrl,
    Operator_Shoulder_L,
    Operator_Shoulder_R,
    Operator_Shoulder_Rot_L,
    Operator_Shoulder_Rot_R,
    Operator_Clavi_Toon_L,
    Operator_Clavi_Toon_R,
    Operator_Head_Scale,
    Operator_Arm_Toon_L,
    Operator_Elbow_Pole_L,
    Operator_Forearm_Toon_L,
    Operator_Arm_Scale_L,
    Operator_Arm_FK_L,
    Operator_Arm_FK_Ctrl_L,
    Operator_Arm_IK_L,
    Operator_Elbow_Toon_L,
    Operator_Forearm_FK_L,
    Operator_Forearm_IK_L,
    Operator_Hand_Toon_L,
    Operator_Arm_Toon_R,
    Operator_Elbow_Pole_R,
    Operator_Forearm_Toon_R,
    Operator_Arm_Scale_R,
    Operator_Arm_FK_R,
    Operator_Arm_FK_Ctrl_R,
    Operator_Arm_IK_R,
    Operator_Elbow_Toon_R,
    Operator_Forearm_FK_R,
    Operator_Forearm_IK_R,
    Operator_Hand_Toon_R,
    Operator_Torso_Ctrl_Legacy,
    Operator_Spine_3_Legacy,
    Operator_Spine_2_Legacy,
    Operator_Spine_1_Legacy,
    Operator_Torso_Ctrl,
    Operator_Spine_3,
    Operator_Spine_2,
    Operator_Spine_1,
    Operator_Spine_3_FK_Inv,
    Operator_Spine_2_FK_Inv,
    Operator_Torso_FK_Ctrl_Inv,
    Operator_Master_Torso_Pivot_Point,
    Operator_Master_Torso,
    Operator_Pelvis_Ctrl,
    Operator_Pelvis_Ctrl_Legacy,
    Operator_Spine_4_Toon,
    Operator_Spine_3_Toon,
    Operator_Spine_2_Toon,
    Operator_Spine_1_Toon,
    Operator_Pelvis_Toon,
    Operator_Spine_3_Inv_Ctrl,
    Operator_Hand_Roll_L,
    Operator_Fing_Spread_L,
    Operator_Hand_IK_Pivot_Point_L,
    Operator_Hand_IK_Ctrl_L,
    Operator_Hand_FK_L,
    Operator_Fing_Lit_Ctrl_L,
    Operator_Fing_Lit_2_L,
    Operator_Fing_Lit_3_L,
    Operator_Fing_Lit_4_L,
    Operator_Fing_Ring_Ctrl_L,
    Operator_Fing_Ring_2_L,
    Operator_Fing_Ring_3_L,
    Operator_Fing_Ring_4_L,
    Operator_Fing_Mid_Ctrl_L,
    Operator_Fing_Mid_2_L,
    Operator_Fing_Mid_3_L,
    Operator_Fing_Mid_4_L,
    Operator_Fing_Ind_Ctrl_L,
    Operator_Fing_Ind_2_L,
    Operator_Fing_Ind_3_L,
    Operator_Fing_Ind_4_L,
    Operator_Fing_Thumb_Ctrl_L,
    Operator_Fing_Thumb_2_L,
    Operator_Fing_Thumb_3_L,
    Operator_Fing_Thumb_1_L,
    Operator_Fing_Lit_IK_L,
    Operator_Fing_Ring_IK_L,
    Operator_Fing_Mid_IK_L,
    Operator_Fing_Ind_IK_L,
    Operator_Fing_Thumb_IK_L,
    Operator_Hand_Close_L,
    Operator_Hand_Roll_R,
    Operator_Fing_Spread_R,
    Operator_Hand_IK_Pivot_Point_R,
    Operator_Hand_IK_Ctrl_R,
    Operator_Hand_FK_R,
    Operator_Fing_Lit_Ctrl_R,
    Operator_Fing_Lit_2_R,
    Operator_Fing_Lit_3_R,
    Operator_Fing_Lit_4_R,
    Operator_Fing_Ring_Ctrl_R,
    Operator_Fing_Ring_2_R,
    Operator_Fing_Ring_3_R,
    Operator_Fing_Ring_4_R,
    Operator_Fing_Mid_Ctrl_R,
    Operator_Fing_Mid_2_R,
    Operator_Fing_Mid_3_R,
    Operator_Fing_Mid_4_R,
    Operator_Fing_Ind_Ctrl_R,
    Operator_Fing_Ind_2_R,
    Operator_Fing_Ind_3_R,
    Operator_Fing_Ind_4_R,
    Operator_Fing_Thumb_Ctrl_R,
    Operator_Fing_Thumb_2_R,
    Operator_Fing_Thumb_3_R,
    Operator_Fing_Thumb_1_R,
    Operator_Fing_Lit_IK_R,
    Operator_Fing_Ring_IK_R,
    Operator_Fing_Mid_IK_R,
    Operator_Fing_Ind_IK_R,
    Operator_Fing_Thumb_IK_R,
    Operator_Hand_Close_R,
    Operator_Thigh_Toon_L,
    Operator_Knee_Pole_L,
    Operator_Shin_Toon_L,
    Operator_Pelvis_Toon_L,
    Operator_Leg_Scale_L,
    Operator_Thigh_FK_L,
    Operator_Thigh_FK_Ctrl_L,
    Operator_Thigh_IK_L,
    Operator_Knee_Toon_L,
    Operator_Shin_FK_L,
    Operator_Shin_IK_L,
    Operator_Foot_Toon_L,
    Operator_Thigh_Toon_R,
    Operator_Knee_Pole_R,
    Operator_Shin_Toon_R,
    Operator_Pelvis_Toon_R,
    Operator_Leg_Scale_R,
    Operator_Thigh_FK_R,
    Operator_Thigh_FK_Ctrl_R,
    Operator_Thigh_IK_R,
    Operator_Knee_Toon_R,
    Operator_Shin_FK_R,
    Operator_Shin_IK_R,
    Operator_Foot_Toon_R,
    Operator_Toe_2_FK_L,
    Operator_Toe_Roll_1_L,
    Operator_Toe_1_FK_L,
    Operator_Toe_Roll_2_L,
    Operator_Foot_L,
    Operator_Foot_Roll_Ctrl_L,
    Operator_Toe_Big_Ctrl_L,
    Operator_Toe_Big_2_L,
    Operator_Toe_Big_3_L,
    Operator_Toe_Big_IK_L,
    Operator_Toe_Ind_Ctrl_L,
    Operator_Toe_Ind_2_L,
    Operator_Toe_Ind_3_L,
    Operator_Toe_Ind_4_L,
    Operator_Toe_Ind_IK_L,
    Operator_Toe_Mid_Ctrl_L,
    Operator_Toe_Mid_2_L,
    Operator_Toe_Mid_3_L,
    Operator_Toe_Mid_4_L,
    Operator_Toe_Mid_IK_L,
    Operator_Toe_Fourth_Ctrl_L,
    Operator_Toe_Fourth_2_L,
    Operator_Toe_Fourth_3_L,
    Operator_Toe_Fourth_4_L,
    Operator_Toe_Fourth_IK_L,
    Operator_Toe_Lit_Ctrl_L,
    Operator_Toe_Lit_2_L,
    Operator_Toe_Lit_3_L,
    Operator_Toe_Lit_IK_L,
    Operator_Toes_Spread_L,
    Operator_Toes_IK_Ctrl_Mid_L,
    Operator_Toes_IK_Ctrl_L,
    Operator_Sole_Ctrl_L,
    Operator_Sole_Pivot_Point_L,
    Operator_Toe_2_FK_R,
    Operator_Toe_Roll_1_R,
    Operator_Toe_1_FK_R,
    Operator_Toe_Roll_2_R,
    Operator_Foot_R,
    Operator_Foot_Roll_Ctrl_R,
    Operator_Toe_Big_Ctrl_R,
    Operator_Toe_Big_2_R,
    Operator_Toe_Big_3_R,
    Operator_Toe_Big_IK_R,
    Operator_Toe_Ind_Ctrl_R,
    Operator_Toe_Ind_2_R,
    Operator_Toe_Ind_3_R,
    Operator_Toe_Ind_4_R,
    Operator_Toe_Ind_IK_R,
    Operator_Toe_Mid_Ctrl_R,
    Operator_Toe_Mid_2_R,
    Operator_Toe_Mid_3_R,
    Operator_Toe_Mid_4_R,
    Operator_Toe_Mid_IK_R,
    Operator_Toe_Fourth_Ctrl_R,
    Operator_Toe_Fourth_2_R,
    Operator_Toe_Fourth_3_R,
    Operator_Toe_Fourth_4_R,
    Operator_Toe_Fourth_IK_R,
    Operator_Toe_Lit_Ctrl_R,
    Operator_Toe_Lit_2_R,
    Operator_Toe_Lit_3_R,
    Operator_Toe_Lit_IK_R,
    Operator_Toes_Spread_R,
    Operator_Toes_IK_Ctrl_Mid_R,
    Operator_Toes_IK_Ctrl_R,
    Operator_Sole_Ctrl_R,
    Operator_Sole_Pivot_Point_R,
    Operator_Master,
    Operator_Master_Pivot_Point,
    Operator_Master_extra,
    Operator_Look,
    Operator_Look_L,
    Operator_Look_R,
    Operator_Zoom_Selected
    )

#Quadruped
from .ops_picker_body import (
    Operator_Ankle_Toon_L,
    Operator_Carpal_FK_L,
    Operator_Carpal_IK_L,
    Operator_Carpal_Toon_L,
    Operator_Ankle_Toon_R,
    Operator_Carpal_FK_R,
    Operator_Carpal_IK_R,
    Operator_Carpal_Toon_R,
    Operator_Hock_Toon_L,
    Operator_Tarsal_FK_L,
    Operator_Tarsal_IK_L,
    Operator_Tarsal_Toon_L,
    Operator_Hock_Toon_R,
    Operator_Tarsal_FK_R,
    Operator_Tarsal_IK_R,
    Operator_Tarsal_Toon_R,
    Operator_Fing_2_FK_L,
    Operator_Fing_1_FK_L,
    Operator_Fing_Roll_2_L,
    Operator_Fing_Roll_1_L,
    Operator_Hand_L,
    Operator_Hand_Roll_Ctrl_L,
    Operator_Hand_Sole_Ctrl_L,
    Operator_Hand_Sole_Pivot_Point_L,
    Operator_Fing_2_FK_R,
    Operator_Fing_1_FK_R,
    Operator_Fing_Roll_2_R,
    Operator_Fing_Roll_1_R,
    Operator_Hand_R,
    Operator_Hand_Roll_Ctrl_R,
    Operator_Hand_Sole_Ctrl_R,
    Operator_Hand_Sole_Pivot_Point_R
    )

####### Load BlenRig 6 Face Picker Operators
from .ops_picker_face import (
    Operator_Ear_Up_R,
    Operator_Ear_R,
    Operator_Ear_Low_R,
    Operator_Brow_Ctrl_1_R,
    Operator_Brow_Ctrl_2_R,
    Operator_Brow_Ctrl_3_R,
    Operator_Brow_Ctrl_4_R,
    Operator_Brow_Ctrl_R,
    Operator_Toon_Brow_R,
    Operator_Ear_Up_L,
    Operator_Ear_L,
    Operator_Ear_Low_L,
    Operator_Brow_Ctrl_1_L,
    Operator_Brow_Ctrl_2_L,
    Operator_Brow_Ctrl_3_L,
    Operator_Brow_Ctrl_4_L,
    Operator_Brow_Ctrl_L,
    Operator_Toon_Brow_L,
    Operator_Frown_Ctrl,
    Operator_Nose_Bridge_1_Ctrl,
    Operator_Eyelid_Up_Ctrl_R,
    Operator_Eyelid_Up_Ctrl_3_R,
    Operator_Eyelid_Up_Ctrl_2_R,
    Operator_Eyelid_Up_Ctrl_1_R,
    Operator_Toon_Eye_Out_R,
    Operator_Toon_Eye_Up_R,
    Operator_Pupil_Ctrl_R,
    Operator_Eye_Ctrl_R,
    Operator_Iris_Ctrl_R,
    Operator_Toon_Eye_In_R,
    Operator_Toon_Eye_Low_R,
    Operator_Eyelid_Ctrl_Out_R,
    Operator_Eyelid_Low_Ctrl_3_R,
    Operator_Eyelid_Low_Ctrl_2_R,
    Operator_Eyelid_Low_Ctrl_1_R,
    Operator_Eyelid_Ctrl_In_R,
    Operator_Eyelid_Low_Ctrl_R,
    Operator_Eyelid_Up_Ctrl_L,
    Operator_Eyelid_Up_Ctrl_3_L,
    Operator_Eyelid_Up_Ctrl_2_L,
    Operator_Eyelid_Up_Ctrl_1_L,
    Operator_Toon_Eye_Out_L,
    Operator_Toon_Eye_Up_L,
    Operator_Pupil_Ctrl_L,
    Operator_Eye_Ctrl_L,
    Operator_Iris_Ctrl_L,
    Operator_Toon_Eye_In_L,
    Operator_Toon_Eye_Low_L,
    Operator_Eyelid_Ctrl_Out_L,
    Operator_Eyelid_Low_Ctrl_3_L,
    Operator_Eyelid_Low_Ctrl_2_L,
    Operator_Eyelid_Low_Ctrl_1_L,
    Operator_Eyelid_Ctrl_In_L,
    Operator_Eyelid_Low_Ctrl_L,
    Operator_Nose_Bridge_2_Ctrl,
    Operator_Nose_Frown_Ctrl_R,
    Operator_Nose_Frown_Ctrl_L,
    Operator_Cheek_Ctrl_R,
    Operator_Cheek_Ctrl_3_R,
    Operator_Cheek_Ctrl_2_R,
    Operator_Cheek_Ctrl_1_R,
    Operator_Cheek2_Ctrl_3_R,
    Operator_Cheek2_Ctrl_2_R,
    Operator_Cheek2_Ctrl_1_R,
    Operator_Lip_Up3_Ctrl_3_R,
    Operator_Lip_Up3_Ctrl_2_R,
    Operator_Lip_Up3_Ctrl_1_R,
    Operator_Lip_Up2_Ctrl_3_R,
    Operator_Lip_Up2_Ctrl_2_R,
    Operator_Lip_Up2_Ctrl_1_R,
    Operator_Cheek_Ctrl_L,
    Operator_Cheek_Ctrl_3_L,
    Operator_Cheek_Ctrl_2_L,
    Operator_Cheek_Ctrl_1_L,
    Operator_Cheek2_Ctrl_3_L,
    Operator_Cheek2_Ctrl_2_L,
    Operator_Cheek2_Ctrl_1_L,
    Operator_Lip_Up3_Ctrl_3_L,
    Operator_Lip_Up3_Ctrl_2_L,
    Operator_Lip_Up3_Ctrl_1_L,
    Operator_Lip_Up2_Ctrl_3_L,
    Operator_Lip_Up2_Ctrl_2_L,
    Operator_Lip_Up2_Ctrl_1_L,
    Operator_Nostril_Ctrl_R,
    Operator_Nose_Ctrl,
    Operator_Nostril_Ctrl_L,
    Operator_Lip_Up3_Ctrl_Mid,
    Operator_Lip_Up3_Ctrl,
    Operator_Lip_Up2_Ctrl_Mid,
    Operator_lip_up2_ctrl,
    Operator_Cheek_Ctrl_4_R,
    Operator_Cheek2_Ctrl_4_R,
    Operator_Lip_Up3_Ctrl_4_R,
    Operator_Lip_Up2_Ctrl_4_R,
    Operator_Cheek_Ctrl_4_L,
    Operator_Cheek2_Ctrl_4_L,
    Operator_Lip_Up3_Ctrl_4_L,
    Operator_Lip_Up2_Ctrl_4_L,
    Operator_Mouth_Mstr_Up,
    Operator_Mouth_Corner_R,
    Operator_Mouth_Corner_L,
    Operator_Lip_Up_Ctrl,
    Operator_Lip_Up_Ctrl_Collision,
    Operator_Lip_Up_Ctrl_3_R,
    Operator_Lip_Up_Ctrl_2_R,
    Operator_Lip_Up_Ctrl_1_R,
    Operator_Lip_Up_Ctrl_Mid,
    Operator_Lip_Up_Ctrl_3_L,
    Operator_Lip_Up_Ctrl_2_L,
    Operator_Lip_Up_Ctrl_1_L,
    Operator_Mouth_Up_Ctrl,
    Operator_Lip_Up_Ctrl_4_R,
    Operator_Lip_Up_Ctrl_4_L,
    Operator_Mouth_Ctrl,
    Operator_Mouth_Low_Ctrl,
    Operator_Lip_Low_Ctrl_3_R,
    Operator_Lip_Low_Ctrl_2_R,
    Operator_Lip_Low_Ctrl_1_R,
    Operator_Lip_Low_Ctrl_Mid,
    Operator_Lip_Low_Ctrl_1_L,
    Operator_Lip_Low_Ctrl_2_L,
    Operator_Lip_Low_Ctrl_3_L,
    Operator_Lip_Low_Ctrl_Collision,
    Operator_Lip_Low_Ctrl,
    Operator_Mouth_Mstr_Low,
    Operator_Mouth_Mstr_Ctrl,
    Operator_Mouth_Frown_Ctrl_R,
    Operator_Lip_Low2_Ctrl_3_R,
    Operator_Lip_Low2_Ctrl_2_R,
    Operator_Lip_Low2_Ctrl_1_R,
    Operator_Lip_Low3_Ctrl_3_R,
    Operator_Lip_Low3_Ctrl_2_R,
    Operator_Lip_Low3_Ctrl_1_R,
    Operator_Cheek_Ctrl_5_R,
    Operator_Chin_Ctrl_3_R,
    Operator_Chin_Ctrl_2_R,
    Operator_Chin_Ctrl_1_R,
    Operator_Mouth_Frown_Ctrl_L,
    Operator_Lip_Low2_Ctrl_3_L,
    Operator_Lip_Low2_Ctrl_2_L,
    Operator_Lip_Low2_Ctrl_1_L,
    Operator_Lip_Low3_Ctrl_3_L,
    Operator_Lip_Low3_Ctrl_2_L,
    Operator_Lip_Low3_Ctrl_1_L,
    Operator_Cheek_Ctrl_5_L,
    Operator_Chin_Ctrl_3_L,
    Operator_Chin_Ctrl_2_L,
    Operator_Chin_Ctrl_1_L,
    Operator_Lip_Low2_Ctrl_Mid,
    Operator_Lip_Low2_Ctrl,
    Operator_Lip_Low3_Ctrl_Mid,
    Operator_Lip_Low3_Ctrl,
    Operator_Chin_Ctrl_Mid,
    Operator_Chin_Ctrl,
    Operator_Maxi,
    Operator_Head_Mid_Stretch,
    Operator_Head_Low_Stretch,
    Operator_Teeth_Up_Ctrl_R,
    Operator_Teeth_Up_Ctrl_L,
    Operator_Teeth_Up_Ctrl_Mid_R,
    Operator_Teeth_Up_Ctrl_Mid_L,
    Operator_Teeth_Up_Ctrl_Mid,
    Operator_Teeth_Up,
    Operator_Teeth_Low_Ctrl_R,
    Operator_Teeth_Low_Ctrl_L,
    Operator_Teeth_Low_Ctrl_Mid_R,
    Operator_Teeth_Low_Ctrl_Mid_L,
    Operator_Teeth_Low_Ctrl_Mid,
    Operator_Teeth_Low,
    Operator_Uvula_1,
    Operator_Uvula_2,
    Operator_Tongue_1_FK,
    Operator_Tongue_2_FK,
    Operator_Tongue_1_IK,
    Operator_Tongue_2_IK,
    Operator_Tongue_3_IK,
    Operator_Tongue_Mstr
    )

####### Load BlenRig 6 Layers Schemes Operators
from .blenrig_biped.ops_biped_layers_scheme import (
    Operator_BlenRig_Layers_Scheme_Compact,
    Operator_BlenRig_Layers_Scheme_Expanded
)

####### Load BlenRig 6 Rig Updater Operators
from .ops_rig_updater import (
    Operator_Biped_Updater,
    Operator_Set_Lib_Override_On
)

####### Load BlenRig 6 Rig Presets Operators
from .blenrig_biped.ops_blenrig_biped_add import (
    Operator_BlenRig5_Add_Biped
)

#################### Blenrig Object Add Menu ###############

class INFO_MT_blenrig5_add_rig(bpy.types.Menu):
    # Define the menu
    bl_idname = "BlenRig 6 add rigs"
    bl_label = "BlenRig 6 add rigs"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("blenrig.add_biped_rig", text="BlenRig 6 Biped Rig", icon='POSE_HLT')

# Define menu
def blenrig5_add_menu_func(self, context):
    self.layout.operator("blenrig.add_biped_rig", text="BlenRig 6 Biped Rig", icon='POSE_HLT')

######### GUI OPERATORS ###########################################
# Display or hide tabs (sets the appropriate id-property)
class ARMATURE_OT_blenrig_6_gui(bpy.types.Operator):
    "Display tab"
    bl_label = ""
    bl_idname = "gui.blenrig_6_tabs"

    tab: bpy.props.StringProperty(name="Tab", description="Tab of the gui to expand")

    # for gui_rig_bake Toggle:
    # mode = []
    # layers = []

    def invoke(self, context, event):
        arm = context.active_object.data
        if self.properties.tab in arm:
            arm[self.properties.tab] = not arm[self.properties.tab]
        if self.properties.tab == 'gui_custom_layers':
            context.window_manager.blenrig_6_props.gui_custom_layers = not context.window_manager.blenrig_6_props.gui_custom_layers

        # Auto mode for gui_rig_bake Toggle:
        # if self.properties.tab == 'gui_rig_bake':
            # self.mode.append(context.active_object.mode)
            # self.layers.append(bpy.context.active_object.data.layers[:])
            # if context.active_object.mode == 'POSE':
            #     if len(self.mode) > 1:
            #         bpy.ops.object.mode_set(mode= self.mode[-2])
            #     if len(self.layers) > 1:
            #         bpy.context.active_object.data.layers = self.layers[-2]
            # else:
            #     bpy.ops.object.mode_set(mode='POSE')

            ## print(self.mode)
            ## print(self.layers)
            # if len(self.mode) > 1:
            #     del self.mode[0]
            # if len(self.layers) > 1:
            #     del self.layers[0]
        # end Auto mode for gui_rig_bake Toggle


        return{'FINISHED'}

####### REGISTRATION ##############################################

# Needed for property registration
class blenrig_6_props(PropertyGroup):
    gui_picker_body_props: BoolProperty(default=True, description="Toggle properties display")
    gui_picker_body_picker: BoolProperty(default=True, description="Toggle properties display")
    gui_snap_all: BoolProperty(default=False, description="Display ALL Snapping Buttons")
    gui_snap: BoolProperty(default=False, description="Display Snapping Buttons")
    gui_cust_props_all: BoolProperty(default=False, description="Show ALL Custom Properties")
    gui_extra_props_face: BoolProperty(default=False, description="Tweak head extra options")
    gui_extra_props_arms: BoolProperty(default=False, description="Tweak arms extra options")
    gui_extra_props_fingers: BoolProperty(default=False, description="Tweak fingers extra options")
    gui_extra_props_legs: BoolProperty(default=False, description="Tweak legs extra options")
    gui_extra_props_props: BoolProperty(default=False, description="Tweak accessories options")
    gui_face_movement_ranges: BoolProperty(default=False, description="Set limits to facial movement")
    gui_face_lip_shaping: BoolProperty(default=False, description="Parameters to define lips curvature")
    gui_face_action_toggles: BoolProperty(default=False, description="Toggle facial actions off for editing")
    gui_face_collisions: BoolProperty(default=False, description="Face Collisions Offset")
    gui_face_bbones: BoolProperty(default=False, description="Face Bendy Bones Settings")
    gui_body_ik_rot: BoolProperty(default=False, description="Set the initial rotation of IK bones")
    gui_body_auto_move: BoolProperty(default=False, description="Parameters for automated movement")
    gui_body_rj: BoolProperty(default=False, description="Simulate how bone thickness affects joint rotation")
    gui_body_vp: BoolProperty(default=False, description="Volume Preservation Bones Movement Definition")
    gui_body_toggles: BoolProperty(default=False, description="Toggle body parts")
    gui_body_bbones: BoolProperty(default=False, description="Body Bendy Bones Settings")
    gui_body_collisions: BoolProperty(default=False, description="Body Collisions Offset")
    bake_to_shape: BoolProperty(name="Bake to Shape Key", default=False, description="Bake the mesh into a separate Shape Key")
    enable_to_move: BoolProperty(name="Enable to Move Lattice", default=False, description="Let move Lattice disabling modif hoocks")
    align_selected_only: BoolProperty(name="Selected Bones Only", default=False, description="Perform aligning only on selected bones")
    gui_custom_layers: BoolProperty(default = False ,name = "Gui Custom Layers")
    contextOptions = [('PICKER', 'Picker', "Display Rig Picker", 'ARMATURE_DATA', 0),
                        ('RIGTOOLS', 'Rig Tools', "Rig Options and Tools", 'BONE_DATA', 1),
                        ('TOOLS', 'Tools', "Workflow Tools", 'TOOL_SETTINGS', 3),
                        ('GUIDES', 'Rigging Assistant', "Automatic Rigging Assistant Guides", 'HELP', 4)]

    def displayContext_update(self, context):
        # instancio el singleton para ustarlo
        singleton = SingletonClass()
        # actualizo su variable armature_layers con el nuevo data al hacer click en Pircker
        with open(armature_layers_file, "r") as jsonFile:
            singleton.armature_layers = json.load(jsonFile)


    displayContext : EnumProperty(
        name='Display Context',
        description="Type of context to display in this panel.",
        items=contextOptions,
        default='PICKER',
        update=displayContext_update
    )
    contextOptions2 = [('BONESHAPES', 'BoneShapes', "BoneShapes Tools", 'POSE_HLT', 0),
                        ('SHAPEKEYS', 'ShapeKeys', "ShapeKeys Tools", 'SURFACE_NCURVE', 1)]
    displayContext2 : EnumProperty(name='Display Context 2', description="Type of context to display in this panel.",items=contextOptions2, default='BONESHAPES')
    adjust_distance_cage : FloatProperty(name="Distance from object", description="Ajust the distance of Cage to object",update = snap_points_update, min=-10, max=10, default=0.1)

    # renaming aramture layers:
    def arm_layers_renaming_update(self, context):
        arm_props_layers = [self.arm_layers_renaming_facial1,
                                 self.arm_layers_renaming_facial2,
                                 self.arm_layers_renaming_facial3,
                                 self.arm_layers_renaming_arm_r_fk,
                                 self.arm_layers_renaming_neck_fk,
                                 self.arm_layers_renaming_arm_l_fk,
                                 self.arm_layers_renaming_arm_r_ik,
                                 self.arm_layers_renaming_torso_fk,
                                 self.arm_layers_renaming_arm_l_ik,
                                 self.arm_layers_renaming_fingers,
                                 self.arm_layers_renaming_torso_inv,
                                 self.arm_layers_renaming_fingers_ik,
                                 self.arm_layers_renaming_leg_r_fk,
                                 self.arm_layers_renaming_props,
                                 self.arm_layers_renaming_leg_l_fk,
                                 self.arm_layers_renaming_leg_r_ik,
                                 self.arm_layers_renaming_extras,
                                 self.arm_layers_renaming_leg_l_ik,
                                 self.arm_layers_renaming_toes,
                                 self.arm_layers_renaming_properties,
                                 self.arm_layers_renaming_toes_fk,
                                 self.arm_layers_renaming_toon_1,
                                 self.arm_layers_renaming_toon_2,
                                 self.arm_layers_renaming_scale,
                                 self.arm_layers_renaming_optionals,
                                 self.arm_layers_renaming_protected,
                                 self.arm_layers_renaming_mech,
                                 self.arm_layers_renaming_deformation,
                                 self.arm_layers_renaming_actions,
                                 self.arm_layers_renaming_bone_rolls,
                                 self.arm_layers_renaming_snapping,
                                 self.arm_layers_renaming_reproportion]

        # obteniendo el data para reemplazarlo:
        armature_layers = None
        with open(armature_layers_file, "r") as jsonFile:
            armature_layers = json.load(jsonFile)

        # reemplazando el data:
        if armature_layers:
            armature_layers_copy = list(armature_layers.keys())
            for idx, key in enumerate(armature_layers_copy):
                armature_layers[arm_props_layers[idx]] = armature_layers.pop(key)

        # write data:
        json_string = json.dumps(armature_layers, sort_keys=False, indent=4)
        with open(armature_layers_file, 'w') as outfile:
            outfile.write(json_string)

        wm = context.window_manager
        blenrig_6_props = wm.blenrig_6_props
        blenrig_6_props.armature_layers_read = True

    arm_layers_renaming_facial1: StringProperty(default="FACIAL1", update=arm_layers_renaming_update)
    arm_layers_renaming_facial2: StringProperty(default="FACIAL2", update=arm_layers_renaming_update)
    arm_layers_renaming_facial3: StringProperty(default="FACIAL3", update=arm_layers_renaming_update)
    arm_layers_renaming_arm_r_fk: StringProperty(default="ARM_R FK", update=arm_layers_renaming_update)
    arm_layers_renaming_neck_fk: StringProperty(default="NECK FK", update=arm_layers_renaming_update)
    arm_layers_renaming_arm_l_fk: StringProperty(default="ARM_L FK", update=arm_layers_renaming_update)
    arm_layers_renaming_arm_r_ik: StringProperty(default="ARM_R IK", update=arm_layers_renaming_update)
    arm_layers_renaming_torso_fk: StringProperty(default="TORSO FK", update=arm_layers_renaming_update)
    arm_layers_renaming_arm_l_ik: StringProperty(default="ARM_L IK", update=arm_layers_renaming_update)
    arm_layers_renaming_fingers: StringProperty(default="FINGERS", update=arm_layers_renaming_update)
    arm_layers_renaming_torso_inv: StringProperty(default="TORSO INV", update=arm_layers_renaming_update)
    arm_layers_renaming_fingers_ik: StringProperty(default="FINGERS IK", update=arm_layers_renaming_update)
    arm_layers_renaming_leg_r_fk: StringProperty(default="LEG_R_FK", update=arm_layers_renaming_update)
    arm_layers_renaming_props: StringProperty(default="PROPS", update=arm_layers_renaming_update)
    arm_layers_renaming_leg_l_fk: StringProperty(default="LEG_L FK", update=arm_layers_renaming_update)
    arm_layers_renaming_leg_r_ik: StringProperty(default="LEG_R_IK", update=arm_layers_renaming_update)
    arm_layers_renaming_extras: StringProperty(default="EXTRAS", update=arm_layers_renaming_update)
    arm_layers_renaming_leg_l_ik: StringProperty(default="LEG_L IK", update=arm_layers_renaming_update)
    arm_layers_renaming_toes: StringProperty(default="TOES", update=arm_layers_renaming_update)
    arm_layers_renaming_properties: StringProperty(default="PROPERTIES", update=arm_layers_renaming_update)
    arm_layers_renaming_toes_fk: StringProperty(default="TOES FK", update=arm_layers_renaming_update)
    arm_layers_renaming_toon_1: StringProperty(default="TOON 1", update=arm_layers_renaming_update)
    arm_layers_renaming_toon_2: StringProperty(default="TOON 2", update=arm_layers_renaming_update)
    arm_layers_renaming_scale: StringProperty(default="SCALE", update=arm_layers_renaming_update)
    arm_layers_renaming_optionals: StringProperty(default="OPTIONALS", update=arm_layers_renaming_update)
    arm_layers_renaming_protected: StringProperty(default="PROTECTED", update=arm_layers_renaming_update)
    arm_layers_renaming_mech: StringProperty(default="MECH", update=arm_layers_renaming_update)
    arm_layers_renaming_deformation: StringProperty(default="DEFORMATION", update=arm_layers_renaming_update)
    arm_layers_renaming_actions: StringProperty(default="ACTIONS", update=arm_layers_renaming_update)
    arm_layers_renaming_bone_rolls: StringProperty(default="BONE-ROLLS", update=arm_layers_renaming_update)
    arm_layers_renaming_snapping: StringProperty(default="SNAPPING", update=arm_layers_renaming_update)
    arm_layers_renaming_reproportion: StringProperty(default="REPROPORTION", update=arm_layers_renaming_update)

# BlenRig Armature Tools Operator
armature_classes = [
    ARMATURE_OT_reset_constraints,
    ARMATURE_OT_advanced_armature_baker,
    ARMATURE_OT_armature_baker_all_part_1,
    ARMATURE_OT_armature_baker_all_part_2,
    ARMATURE_OT_mesh_pose_baker,
    ARMATURE_OT_reset_hooks,
    ARMATURE_OT_disable_hooks_modif,
    ARMATURE_OT_reset_deformers,
    ARMATURE_OT_blenrig_6_gui
    ]

######## bone selections set ###############

from .custom_selection.custom_selection import *

bone_selecction_set_classes = [
    BLENRIG_MT_selection_set_create,
    BLENRIG_MT_selection_sets_context_menu,
    BLENRIG_MT_selection_sets_select,
    BLENRIG_UL_selection_set,
    SelectionEntry,
    SelectionSet,
    BLENRIG_OT_selection_set_delete_all,
    BLENRIG_OT_selection_set_remove_bones,
    BLENRIG_OT_selection_set_move,
    BLENRIG_OT_selection_set_add,
    BLENRIG_OT_selection_set_remove,
    BLENRIG_OT_selection_set_assign,
    BLENRIG_OT_selection_set_unassign,
    BLENRIG_OT_selection_set_select,
    BLENRIG_OT_selection_set_deselect,
    BLENRIG_OT_selection_set_add_and_assign,
    BLENRIG_OT_selection_set_copy,
    BLENRIG_OT_selection_set_paste
]

# BlenRig BoneShapes
boneshapes_classes = [
    BLENRIG_OT_removeShapes,
    BLENRIG_OT_addShapes,
    BLENRIG_OT_matchSymmetrizeShape,
    BLENRIG_OT_matchBoneTransforms,
    BLENRIG_OT_returnToArmature,
    BLENRIG_OT_editShapes,
    BLENRIG_OT_createShapes,
    BLENRIG_OT_toggleCollectionVisibility,
    BLENRIG_OT_deleteUnusedShapes,
    BLENRIG_OT_clearBoneShapes,
    BLENRIG_OT_resyncShapesNames,
    BLENRIG_OT_shape_scale,
    BLENRIG_OT_Make_Unique,
    BoneShapesPreferences
]

# BlenRig Align Operators
alignment_classes = [
    Operator_BlenRig_Fix_Misaligned_Bones,
    Operator_BlenRig_Auto_Bone_Roll,
    Operator_BlenRig_Custom_Bone_Roll,
    Operator_BlenRig_Store_Roll_Angles,
    Operator_BlenRig_Restore_Roll_Angles,
    Operator_BlenRig_Reset_Dynamic,
    Operator_Mirror_VP_Constraints,
    Operator_Mirror_RJ_Constraints,
    Operator_blenrig_calculate_pole_angles,
    Operator_blenrig_calculate_floor_offsets
]
# BlenRig Layers Schemes Operators
schemes_classes = [
    Operator_BlenRig_Layers_Scheme_Compact,
    Operator_BlenRig_Layers_Scheme_Expanded
]
# BlenRig Rig Updater Operators
rig_updater_classes = [
    Operator_Biped_Updater,
    Operator_Set_Lib_Override_On
]
# BlenRig IK/FK Snapping Operators
snapping_classes = [
    Operator_Snap_TorsoFKtoIK,
    Operator_Snap_TorsoIKtoFK,
    Operator_Align_Spine,
    Operator_Knee_UnPin_L,
    Operator_Knee_UnPin_R,
    Operator_Knee_Pin_L,
    Operator_Knee_Pin_R,
    Operator_Elbow_UnPin_R,
    Operator_Elbow_UnPin_L,
    Operator_Elbow_Pin_L,
    Operator_Elbow_Pin_R,
    Operator_Reset_Master_Pivot,
    Operator_Reset_Master_Body_Pivot,
    Operator_Reset_Master_Torso_Pivot,
    Operator_Reset_Hand_R_Pivot,
    Operator_Reset_Hand_L_Pivot,
    Operator_Switch_Fing_Lit_Space_R,
    Operator_Show_Fing_Lit_Space_List_R,
    Operator_Switch_Fing_Ring_Space_R,
    Operator_Show_Fing_Ring_Space_List_R,
    Operator_Switch_Fing_Mid_Space_R,
    Operator_Show_Fing_Mid_Space_List_R,
    Operator_Switch_Fing_Ind_Space_R,
    Operator_Show_Fing_Ind_Space_List_R,
    Operator_Switch_Fing_Thumb_Space_R,
    Operator_Show_Fing_Thumb_Space_List_R,
    Operator_Switch_Fing_All_Space_R,
    Operator_Show_Fing_All_Space_List_R,
    Operator_Switch_Fing_Lit_Space_L,
    Operator_Show_Fing_Lit_Space_List_L,
    Operator_Switch_Fing_Ring_Space_L,
    Operator_Show_Fing_Ring_Space_List_L,
    Operator_Switch_Fing_Mid_Space_L,
    Operator_Show_Fing_Mid_Space_List_L,
    Operator_Switch_Fing_Ind_Space_L,
    Operator_Show_Fing_Ind_Space_List_L,
    Operator_Switch_Fing_Thumb_Space_L,
    Operator_Show_Fing_Thumb_Space_List_L,
    Operator_Switch_Fing_All_Space_L,
    Operator_Show_Fing_All_Space_List_L,
    Operator_Switch_Look_Space,
    Operator_Show_Look_Space_List,
    Operator_Switch_Neck_Space,
    Operator_Show_Neck_Space_List,
    Operator_Switch_Head_Space,
    Operator_Show_Head_Space_List,
    Operator_Switch_Hand_Accessory_Space,
    Operator_Show_Hand_Accessory_Space_List,
    Operator_Switch_Hat_Space,
    Operator_Show_Hat_Space_List,
    Operator_Switch_Eyeglasses_Space,
    Operator_Show_Eyeglasses_Space_List,
    Operator_Switch_Leg_Pole_Space_L,
    Operator_Show_Leg_Pole_Space_List_L,
    Operator_Switch_Arm_Pole_Space_L,
    Operator_Show_Arm_Pole_Space_List_L,
    Operator_Switch_Leg_Space_L,
    Operator_Show_Leg_Space_List_L,
    Operator_Snap_LegIKtoFK_L,
    Operator_Snap_LegFKtoIK_L,
    Operator_Switch_Hand_Space_L,
    Operator_Show_Hand_Space_List_L,
    Operator_Switch_Arm_Space_L,
    Operator_Show_Arm_Space_List_L,
    Operator_Snap_ArmIKtoFK_L,
    Operator_Snap_ArmFKtoIK_L,
    Operator_Switch_Leg_Pole_Space_R,
    Operator_Show_Leg_Pole_Space_List_R,
    Operator_Switch_Arm_Pole_Space_R,
    Operator_Show_Arm_Pole_Space_List_R,
    Operator_Switch_Leg_Space_R,
    Operator_Show_Leg_Space_List_R,
    Operator_Snap_LegIKtoFK_R,
    Operator_Snap_LegFKtoIK_R,
    Operator_Switch_Hand_Space_R,
    Operator_Show_Hand_Space_List_R,
    Operator_Switch_Arm_Space_R,
    Operator_Show_Arm_Space_List_R,
    Operator_Snap_ArmIKtoFK_R,
    Operator_Snap_ArmFKtoIK_R,
    Operator_Torso_Snap_FK_IK,
    Operator_Torso_Snap_IK_FK,
    Operator_Head_Snap_FK_IK,
    Operator_Head_Snap_IK_FK,
    Operator_Torso_Snap_UP_INV,
    Operator_Torso_Snap_INV_UP,
    Operator_Arm_L_Snap_FK_IK,
    Operator_Arm_L_Snap_IK_FK,
    Operator_Arm_R_Snap_FK_IK,
    Operator_Arm_R_Snap_IK_FK,
    Operator_Leg_L_Snap_FK_IK,
    Operator_Leg_L_Snap_IK_FK,
    Operator_Leg_R_Snap_FK_IK,
    Operator_Leg_R_Snap_IK_FK
]
# BlenRig Picker Operators
body_picker_biped_classes = [
    Operator_Keyframe_Main_Props,
    Operator_Head_Stretch,
    Operator_Head_Toon,
    Operator_Head_Top_Ctrl,
    Operator_Head_Mid_Ctrl,
    Operator_Head_Mid_Curve,
    Operator_Mouth_Str_Ctrl,
    Operator_Head_FK,
    Operator_Head_IK,
    Operator_Neck_4_Toon,
    Operator_Face_Toon_Up,
    Operator_Face_Toon_Mid,
    Operator_Face_Toon_Low,
    Operator_Neck_3_Legacy,
    Operator_Neck_2_Legacy,
    Operator_Neck_3,
    Operator_Neck_2,
    Operator_Neck_1,
    Operator_Neck_3_Toon,
    Operator_Neck_2_Toon,
    Operator_Neck_Ctrl_Legacy,
    Operator_Neck_Ctrl,
    Operator_Shoulder_L,
    Operator_Shoulder_R,
    Operator_Shoulder_Rot_L,
    Operator_Shoulder_Rot_R,
    Operator_Clavi_Toon_L,
    Operator_Clavi_Toon_R,
    Operator_Head_Scale,
    Operator_Arm_Toon_L,
    Operator_Elbow_Pole_L,
    Operator_Forearm_Toon_L,
    Operator_Arm_Scale_L,
    Operator_Arm_FK_L,
    Operator_Arm_FK_Ctrl_L,
    Operator_Arm_IK_L,
    Operator_Elbow_Toon_L,
    Operator_Forearm_FK_L,
    Operator_Forearm_IK_L,
    Operator_Hand_Toon_L,
    Operator_Arm_Toon_R,
    Operator_Elbow_Pole_R,
    Operator_Forearm_Toon_R,
    Operator_Arm_Scale_R,
    Operator_Arm_FK_R,
    Operator_Arm_FK_Ctrl_R,
    Operator_Arm_IK_R,
    Operator_Elbow_Toon_R,
    Operator_Forearm_FK_R,
    Operator_Forearm_IK_R,
    Operator_Hand_Toon_R,
    Operator_Torso_Ctrl_Legacy,
    Operator_Spine_3_Legacy,
    Operator_Spine_2_Legacy,
    Operator_Spine_1_Legacy,
    Operator_Torso_Ctrl,
    Operator_Spine_3,
    Operator_Spine_2,
    Operator_Spine_1,
    Operator_Spine_3_FK_Inv,
    Operator_Spine_2_FK_Inv,
    Operator_Torso_FK_Ctrl_Inv,
    Operator_Master_Torso_Pivot_Point,
    Operator_Master_Torso,
    Operator_Pelvis_Ctrl,
    Operator_Pelvis_Ctrl_Legacy,
    Operator_Spine_4_Toon,
    Operator_Spine_3_Toon,
    Operator_Spine_2_Toon,
    Operator_Spine_1_Toon,
    Operator_Pelvis_Toon,
    Operator_Spine_3_Inv_Ctrl,
    Operator_Hand_Roll_L,
    Operator_Fing_Spread_L,
    Operator_Hand_IK_Pivot_Point_L,
    Operator_Hand_IK_Ctrl_L,
    Operator_Hand_FK_L,
    Operator_Fing_Lit_Ctrl_L,
    Operator_Fing_Lit_2_L,
    Operator_Fing_Lit_3_L,
    Operator_Fing_Lit_4_L,
    Operator_Fing_Ring_Ctrl_L,
    Operator_Fing_Ring_2_L,
    Operator_Fing_Ring_3_L,
    Operator_Fing_Ring_4_L,
    Operator_Fing_Mid_Ctrl_L,
    Operator_Fing_Mid_2_L,
    Operator_Fing_Mid_3_L,
    Operator_Fing_Mid_4_L,
    Operator_Fing_Ind_Ctrl_L,
    Operator_Fing_Ind_2_L,
    Operator_Fing_Ind_3_L,
    Operator_Fing_Ind_4_L,
    Operator_Fing_Thumb_Ctrl_L,
    Operator_Fing_Thumb_2_L,
    Operator_Fing_Thumb_3_L,
    Operator_Fing_Thumb_1_L,
    Operator_Fing_Lit_IK_L,
    Operator_Fing_Ring_IK_L,
    Operator_Fing_Mid_IK_L,
    Operator_Fing_Ind_IK_L,
    Operator_Fing_Thumb_IK_L,
    Operator_Hand_Close_L,
    Operator_Hand_Roll_R,
    Operator_Fing_Spread_R,
    Operator_Hand_IK_Pivot_Point_R,
    Operator_Hand_IK_Ctrl_R,
    Operator_Hand_FK_R,
    Operator_Fing_Lit_Ctrl_R,
    Operator_Fing_Lit_2_R,
    Operator_Fing_Lit_3_R,
    Operator_Fing_Lit_4_R,
    Operator_Fing_Ring_Ctrl_R,
    Operator_Fing_Ring_2_R,
    Operator_Fing_Ring_3_R,
    Operator_Fing_Ring_4_R,
    Operator_Fing_Mid_Ctrl_R,
    Operator_Fing_Mid_2_R,
    Operator_Fing_Mid_3_R,
    Operator_Fing_Mid_4_R,
    Operator_Fing_Ind_Ctrl_R,
    Operator_Fing_Ind_2_R,
    Operator_Fing_Ind_3_R,
    Operator_Fing_Ind_4_R,
    Operator_Fing_Thumb_Ctrl_R,
    Operator_Fing_Thumb_2_R,
    Operator_Fing_Thumb_3_R,
    Operator_Fing_Thumb_1_R,
    Operator_Fing_Lit_IK_R,
    Operator_Fing_Ring_IK_R,
    Operator_Fing_Mid_IK_R,
    Operator_Fing_Ind_IK_R,
    Operator_Fing_Thumb_IK_R,
    Operator_Hand_Close_R,
    Operator_Thigh_Toon_L,
    Operator_Knee_Pole_L,
    Operator_Shin_Toon_L,
    Operator_Pelvis_Toon_L,
    Operator_Leg_Scale_L,
    Operator_Thigh_FK_L,
    Operator_Thigh_FK_Ctrl_L,
    Operator_Thigh_IK_L,
    Operator_Knee_Toon_L,
    Operator_Shin_FK_L,
    Operator_Shin_IK_L,
    Operator_Foot_Toon_L,
    Operator_Thigh_Toon_R,
    Operator_Knee_Pole_R,
    Operator_Shin_Toon_R,
    Operator_Pelvis_Toon_R,
    Operator_Leg_Scale_R,
    Operator_Thigh_FK_R,
    Operator_Thigh_FK_Ctrl_R,
    Operator_Thigh_IK_R,
    Operator_Knee_Toon_R,
    Operator_Shin_FK_R,
    Operator_Shin_IK_R,
    Operator_Foot_Toon_R,
    Operator_Toe_2_FK_L,
    Operator_Toe_Roll_1_L,
    Operator_Toe_1_FK_L,
    Operator_Toe_Roll_2_L,
    Operator_Foot_L,
    Operator_Foot_Roll_Ctrl_L,
    Operator_Toe_Big_Ctrl_L,
    Operator_Toe_Big_2_L,
    Operator_Toe_Big_3_L,
    Operator_Toe_Big_IK_L,
    Operator_Toe_Ind_Ctrl_L,
    Operator_Toe_Ind_2_L,
    Operator_Toe_Ind_3_L,
    Operator_Toe_Ind_4_L,
    Operator_Toe_Ind_IK_L,
    Operator_Toe_Mid_Ctrl_L,
    Operator_Toe_Mid_2_L,
    Operator_Toe_Mid_3_L,
    Operator_Toe_Mid_4_L,
    Operator_Toe_Mid_IK_L,
    Operator_Toe_Fourth_Ctrl_L,
    Operator_Toe_Fourth_2_L,
    Operator_Toe_Fourth_3_L,
    Operator_Toe_Fourth_4_L,
    Operator_Toe_Fourth_IK_L,
    Operator_Toe_Lit_Ctrl_L,
    Operator_Toe_Lit_2_L,
    Operator_Toe_Lit_3_L,
    Operator_Toe_Lit_IK_L,
    Operator_Toes_Spread_L,
    Operator_Toes_IK_Ctrl_Mid_L,
    Operator_Toes_IK_Ctrl_L,
    Operator_Sole_Ctrl_L,
    Operator_Sole_Pivot_Point_L,
    Operator_Toe_2_FK_R,
    Operator_Toe_Roll_1_R,
    Operator_Toe_1_FK_R,
    Operator_Toe_Roll_2_R,
    Operator_Foot_R,
    Operator_Foot_Roll_Ctrl_R,
    Operator_Toe_Big_Ctrl_R,
    Operator_Toe_Big_2_R,
    Operator_Toe_Big_3_R,
    Operator_Toe_Big_IK_R,
    Operator_Toe_Ind_Ctrl_R,
    Operator_Toe_Ind_2_R,
    Operator_Toe_Ind_3_R,
    Operator_Toe_Ind_4_R,
    Operator_Toe_Ind_IK_R,
    Operator_Toe_Mid_Ctrl_R,
    Operator_Toe_Mid_2_R,
    Operator_Toe_Mid_3_R,
    Operator_Toe_Mid_4_R,
    Operator_Toe_Mid_IK_R,
    Operator_Toe_Fourth_Ctrl_R,
    Operator_Toe_Fourth_2_R,
    Operator_Toe_Fourth_3_R,
    Operator_Toe_Fourth_4_R,
    Operator_Toe_Fourth_IK_R,
    Operator_Toe_Lit_Ctrl_R,
    Operator_Toe_Lit_2_R,
    Operator_Toe_Lit_3_R,
    Operator_Toe_Lit_IK_R,
    Operator_Toes_Spread_R,
    Operator_Toes_IK_Ctrl_Mid_R,
    Operator_Toes_IK_Ctrl_R,
    Operator_Sole_Ctrl_R,
    Operator_Sole_Pivot_Point_R,
    Operator_Master,
    Operator_Master_Pivot_Point,
    Operator_Master_extra,
    Operator_Look,
    Operator_Look_L,
    Operator_Look_R,
    Operator_Zoom_Selected
]

body_picker_quadruped_classes = [
    Operator_Ankle_Toon_L,
    Operator_Carpal_FK_L,
    Operator_Carpal_IK_L,
    Operator_Carpal_Toon_L,
    Operator_Ankle_Toon_R,
    Operator_Carpal_FK_R,
    Operator_Carpal_IK_R,
    Operator_Carpal_Toon_R,
    Operator_Hock_Toon_L,
    Operator_Tarsal_FK_L,
    Operator_Tarsal_IK_L,
    Operator_Tarsal_Toon_L,
    Operator_Hock_Toon_R,
    Operator_Tarsal_FK_R,
    Operator_Tarsal_IK_R,
    Operator_Tarsal_Toon_R,
    Operator_Fing_2_FK_L,
    Operator_Fing_1_FK_L,
    Operator_Fing_Roll_2_L,
    Operator_Fing_Roll_1_L,
    Operator_Hand_L,
    Operator_Hand_Roll_Ctrl_L,
    Operator_Hand_Sole_Ctrl_L,
    Operator_Hand_Sole_Pivot_Point_L,
    Operator_Fing_2_FK_R,
    Operator_Fing_1_FK_R,
    Operator_Fing_Roll_2_R,
    Operator_Fing_Roll_1_R,
    Operator_Hand_R,
    Operator_Hand_Roll_Ctrl_R,
    Operator_Hand_Sole_Ctrl_R,
    Operator_Hand_Sole_Pivot_Point_R
]

face_picker_classes = [
    Operator_Ear_Up_R,
    Operator_Ear_R,
    Operator_Ear_Low_R,
    Operator_Brow_Ctrl_1_R,
    Operator_Brow_Ctrl_2_R,
    Operator_Brow_Ctrl_3_R,
    Operator_Brow_Ctrl_4_R,
    Operator_Brow_Ctrl_R,
    Operator_Toon_Brow_R,
    Operator_Ear_Up_L,
    Operator_Ear_L,
    Operator_Ear_Low_L,
    Operator_Brow_Ctrl_1_L,
    Operator_Brow_Ctrl_2_L,
    Operator_Brow_Ctrl_3_L,
    Operator_Brow_Ctrl_4_L,
    Operator_Brow_Ctrl_L,
    Operator_Toon_Brow_L,
    Operator_Frown_Ctrl,
    Operator_Nose_Bridge_1_Ctrl,
    Operator_Eyelid_Up_Ctrl_R,
    Operator_Eyelid_Up_Ctrl_3_R,
    Operator_Eyelid_Up_Ctrl_2_R,
    Operator_Eyelid_Up_Ctrl_1_R,
    Operator_Toon_Eye_Out_R,
    Operator_Toon_Eye_Up_R,
    Operator_Pupil_Ctrl_R,
    Operator_Eye_Ctrl_R,
    Operator_Iris_Ctrl_R,
    Operator_Toon_Eye_In_R,
    Operator_Toon_Eye_Low_R,
    Operator_Eyelid_Ctrl_Out_R,
    Operator_Eyelid_Low_Ctrl_3_R,
    Operator_Eyelid_Low_Ctrl_2_R,
    Operator_Eyelid_Low_Ctrl_1_R,
    Operator_Eyelid_Ctrl_In_R,
    Operator_Eyelid_Low_Ctrl_R,
    Operator_Eyelid_Up_Ctrl_L,
    Operator_Eyelid_Up_Ctrl_3_L,
    Operator_Eyelid_Up_Ctrl_2_L,
    Operator_Eyelid_Up_Ctrl_1_L,
    Operator_Toon_Eye_Out_L,
    Operator_Toon_Eye_Up_L,
    Operator_Pupil_Ctrl_L,
    Operator_Eye_Ctrl_L,
    Operator_Iris_Ctrl_L,
    Operator_Toon_Eye_In_L,
    Operator_Toon_Eye_Low_L,
    Operator_Eyelid_Ctrl_Out_L,
    Operator_Eyelid_Low_Ctrl_3_L,
    Operator_Eyelid_Low_Ctrl_2_L,
    Operator_Eyelid_Low_Ctrl_1_L,
    Operator_Eyelid_Ctrl_In_L,
    Operator_Eyelid_Low_Ctrl_L,
    Operator_Nose_Bridge_2_Ctrl,
    Operator_Nose_Frown_Ctrl_R,
    Operator_Nose_Frown_Ctrl_L,
    Operator_Cheek_Ctrl_R,
    Operator_Cheek_Ctrl_3_R,
    Operator_Cheek_Ctrl_2_R,
    Operator_Cheek_Ctrl_1_R,
    Operator_Cheek2_Ctrl_3_R,
    Operator_Cheek2_Ctrl_2_R,
    Operator_Cheek2_Ctrl_1_R,
    Operator_Lip_Up3_Ctrl_3_R,
    Operator_Lip_Up3_Ctrl_2_R,
    Operator_Lip_Up3_Ctrl_1_R,
    Operator_Lip_Up2_Ctrl_3_R,
    Operator_Lip_Up2_Ctrl_2_R,
    Operator_Lip_Up2_Ctrl_1_R,
    Operator_Cheek_Ctrl_L,
    Operator_Cheek_Ctrl_3_L,
    Operator_Cheek_Ctrl_2_L,
    Operator_Cheek_Ctrl_1_L,
    Operator_Cheek2_Ctrl_3_L,
    Operator_Cheek2_Ctrl_2_L,
    Operator_Cheek2_Ctrl_1_L,
    Operator_Lip_Up3_Ctrl_3_L,
    Operator_Lip_Up3_Ctrl_2_L,
    Operator_Lip_Up3_Ctrl_1_L,
    Operator_Lip_Up2_Ctrl_3_L,
    Operator_Lip_Up2_Ctrl_2_L,
    Operator_Lip_Up2_Ctrl_1_L,
    Operator_Nostril_Ctrl_R,
    Operator_Nose_Ctrl,
    Operator_Nostril_Ctrl_L,
    Operator_Lip_Up3_Ctrl_Mid,
    Operator_Lip_Up3_Ctrl,
    Operator_Lip_Up2_Ctrl_Mid,
    Operator_lip_up2_ctrl,
    Operator_Cheek_Ctrl_4_R,
    Operator_Cheek2_Ctrl_4_R,
    Operator_Lip_Up3_Ctrl_4_R,
    Operator_Lip_Up2_Ctrl_4_R,
    Operator_Cheek_Ctrl_4_L,
    Operator_Cheek2_Ctrl_4_L,
    Operator_Lip_Up3_Ctrl_4_L,
    Operator_Lip_Up2_Ctrl_4_L,
    Operator_Mouth_Mstr_Up,
    Operator_Mouth_Corner_R,
    Operator_Mouth_Corner_L,
    Operator_Lip_Up_Ctrl,
    Operator_Lip_Up_Ctrl_Collision,
    Operator_Lip_Up_Ctrl_3_R,
    Operator_Lip_Up_Ctrl_2_R,
    Operator_Lip_Up_Ctrl_1_R,
    Operator_Lip_Up_Ctrl_Mid,
    Operator_Lip_Up_Ctrl_3_L,
    Operator_Lip_Up_Ctrl_2_L,
    Operator_Lip_Up_Ctrl_1_L,
    Operator_Mouth_Up_Ctrl,
    Operator_Lip_Up_Ctrl_4_R,
    Operator_Lip_Up_Ctrl_4_L,
    Operator_Mouth_Ctrl,
    Operator_Mouth_Low_Ctrl,
    Operator_Lip_Low_Ctrl_3_R,
    Operator_Lip_Low_Ctrl_2_R,
    Operator_Lip_Low_Ctrl_1_R,
    Operator_Lip_Low_Ctrl_Mid,
    Operator_Lip_Low_Ctrl_1_L,
    Operator_Lip_Low_Ctrl_2_L,
    Operator_Lip_Low_Ctrl_3_L,
    Operator_Lip_Low_Ctrl_Collision,
    Operator_Lip_Low_Ctrl,
    Operator_Mouth_Mstr_Low,
    Operator_Mouth_Mstr_Ctrl,
    Operator_Mouth_Frown_Ctrl_R,
    Operator_Lip_Low2_Ctrl_3_R,
    Operator_Lip_Low2_Ctrl_2_R,
    Operator_Lip_Low2_Ctrl_1_R,
    Operator_Lip_Low3_Ctrl_3_R,
    Operator_Lip_Low3_Ctrl_2_R,
    Operator_Lip_Low3_Ctrl_1_R,
    Operator_Cheek_Ctrl_5_R,
    Operator_Chin_Ctrl_3_R,
    Operator_Chin_Ctrl_2_R,
    Operator_Chin_Ctrl_1_R,
    Operator_Mouth_Frown_Ctrl_L,
    Operator_Lip_Low2_Ctrl_3_L,
    Operator_Lip_Low2_Ctrl_2_L,
    Operator_Lip_Low2_Ctrl_1_L,
    Operator_Lip_Low3_Ctrl_3_L,
    Operator_Lip_Low3_Ctrl_2_L,
    Operator_Lip_Low3_Ctrl_1_L,
    Operator_Cheek_Ctrl_5_L,
    Operator_Chin_Ctrl_3_L,
    Operator_Chin_Ctrl_2_L,
    Operator_Chin_Ctrl_1_L,
    Operator_Lip_Low2_Ctrl_Mid,
    Operator_Lip_Low2_Ctrl,
    Operator_Lip_Low3_Ctrl_Mid,
    Operator_Lip_Low3_Ctrl,
    Operator_Chin_Ctrl_Mid,
    Operator_Chin_Ctrl,
    Operator_Maxi,
    Operator_Head_Mid_Stretch,
    Operator_Head_Low_Stretch,
    Operator_Teeth_Up_Ctrl_R,
    Operator_Teeth_Up_Ctrl_L,
    Operator_Teeth_Up_Ctrl_Mid_R,
    Operator_Teeth_Up_Ctrl_Mid_L,
    Operator_Teeth_Up_Ctrl_Mid,
    Operator_Teeth_Up,
    Operator_Teeth_Low_Ctrl_R,
    Operator_Teeth_Low_Ctrl_L,
    Operator_Teeth_Low_Ctrl_Mid_R,
    Operator_Teeth_Low_Ctrl_Mid_L,
    Operator_Teeth_Low_Ctrl_Mid,
    Operator_Teeth_Low,
    Operator_Uvula_1,
    Operator_Uvula_2,
    Operator_Tongue_1_FK,
    Operator_Tongue_2_FK,
    Operator_Tongue_1_IK,
    Operator_Tongue_2_IK,
    Operator_Tongue_3_IK,
    Operator_Tongue_Mstr
]

blenrig_rigs_classes = [
    Operator_BlenRig5_Add_Biped
]

# addon_dependencies = ["space_view3d_copy_attributes"]

panels_classes = [
    BLENRIG_PT_Rig_Body_settings,
    BLENRIG_PT_Rig_Facial_settings,
    BLENRIG_PT_Rig_Body_settings_facial_movement_ranges,
    BLENRIG_PT_Rig_Body_settings_face_action_toggles,
    BLENRIG_PT_Rig_Body_settings_face_lip_shaping,
    BLENRIG_PT_Rig_Body_settings_face_collisions,
    BLENRIG_PT_Rig_Layers_settings,
    BLENRIG_PT_Dynamic_shaping,
    BLENRIG_PT_Rigging_optimizations,
    BLENRIG_PT_Rigging_and_baking,
    BLENRIG_PT_Cage_snapping_panel,
    BLENRIG_PT_baking,
    BLENRIG_PT_visual_assistant,
    BLENRIG_PT_Rig_version_info,
    BLENRIG_PT_blenrig_6_Interface,
    BLENRIG_PT_legacy_blenrig_5_5_Interface,
    BLENRIG_PT_legacy_blenrig_5_Interface,
    BLENRIG_OT_SnapPoints,
    BLENRIG_OT_center_loop_cage,
    blenrig_6_props,
    BLENRIG_PT_legacy_blenrig_5_rigging_panel,
    BLENRIG_PT_blenrig_6_mesh_panel,
    BLENRIG_PT_blenrig_6_lattice_panel,
    BLENRIG_MT_bw_specials,
    BLENRIG_PT_posemode_panel,
    BLENRIG_MT_bw_specials_edit,
    BLENRIG_PT_reproportion_guide,
    BLENRIG_PT_datatransfer_guide,
    BLENRIG_PT_mdef_guide,
    BLENRIG_PT_lattices_guide,
    BLENRIG_PT_actions_guide,
    BLENRIG_PT_weights_guide,
    BLENRIG_PT_rig_settings_guide,
    BLENRIG_PT_shapekeys_guide,
    BLENRIG_PT_Rig_Body_settings_ik,
    BLENRIG_PT_Rig_Body_settings_automated_movement,
    BLENRIG_PT_Rig_Body_settings_vp_bones_movement,
    BLENRIG_PT_VP_forearm_upwards,
    BLENRIG_PT_VP_arm_upwards,
    BLENRIG_PT_VP_arm_downwards,
    BLENRIG_PT_VP_arm_forwards,
    BLENRIG_PT_VP_arm_backwards,
    BLENRIG_PT_VP_shoulder_upwards,
    BLENRIG_PT_VP_hand_upwards,
    BLENRIG_PT_VP_hand_downwards,
    BLENRIG_PT_VP_fingers_backwards,
    BLENRIG_PT_VP_fingers_curl,
    BLENRIG_PT_VP_leg_forwards,
    BLENRIG_PT_VP_leg_outwards,
    BLENRIG_PT_VP_leg_backwards,
    BLENRIG_PT_VP_shin_upwards,
    BLENRIG_PT_VP_foot_downwards,
    BLENRIG_PT_VP_foot_upwards,
    BLENRIG_PT_VP_foot_toe_curl_upwards,
    BLENRIG_PT_VP_foot_toe_curl_downwards,
    BLENRIG_PT_VP_toes_backwards,
    BLENRIG_PT_VP_toes_curl,
    BLENRIG_PT_Rig_Body_settings_realistic_joints,
    BLENRIG_PT_Rig_Body_settings_bendy_bones_settings,
    BLENRIG_PT_Rig_Body_settings_body_collisions_offset,
    BLENRIG_PT_Rig_Body_settings_toggles,
    BLENRIG_PT_Rig_Body_settings_face_bendy_bones_settings
]

############## Shape_Keys+ Classes ################
shape_keys_classes = (
    Selection,
    KeyProperties,
    SceneProperties,
    MESH_MT_blenrig_shape_key_add_specials,
    MESH_MT_blenrig_shape_key_add_specials_selected,
    MESH_MT_blenrig_shape_key_copy_specials,
    MESH_MT_blenrig_shape_key_copy_specials_selected,
    # MESH_MT_blenrig_shape_key_remove_specials,
    # MESH_MT_blenrig_shape_key_remove_specials_selected,
    MESH_MT_blenrig_shape_key_other_specials,
    MESH_MT_blenrig_shape_key_other_specials_selected,
    OBJECT_MT_blenrig_shape_key_parent,
    OBJECT_MT_blenrig_shape_key_parent_selected,
    OBJECT_MT_blenrig_folder_icon,
    OBJECT_MT_blenrig_folder_icons_standard,
    OBJECT_MT_blenrig_folder_icons_special,
    OBJECT_MT_blenrig_folder_icons_misc,
    OBJECT_OT_blenrig_folder_icon,
    OBJECT_OT_blenrig_shape_key_parent,
    OBJECT_OT_blenrig_shape_key_add,
    OBJECT_OT_blenrig_shape_key_remove,
    OBJECT_OT_blenrig_shape_key_copy,
    OBJECT_OT_blenrig_shape_key_move,
    OBJECT_OT_blenrig_shape_key_select,
    OBJECT_OT_blenrig_folder_toggle,
    OBJECT_OT_blenrig_folder_ungroup,
    DRIVER_OT_blenrig_driver_update,
    DRIVER_OT_blenrig_variable_add,
    DRIVER_OT_blenrig_variable_remove,
    DRIVER_OT_blenrig_variable_copy,
    DRIVER_OT_blenrig_variable_move,
    OBJECT_OT_blenrig_debug_folder_data,
    BLENRIG_PT_shape_keys_plus,
    MESH_UL_BlenRig_shape_keys_plus
)

######## bone selections set ###############
# Store keymaps here to access after registration.
addon_keymaps = []
######## bone selections set ###############


def register():

    from bpy.utils import register_class

    register_class(BLENRIG_PT_blenrig_6_general)
    register_class(BLENRIG_PT_blenrig_6_general_SubPanel)

    #######################register Guide ###################
    from .guides.register import register
    register()
    #########################################################

    # load BlenRig internal classes
    for c in armature_classes:
        register_class(c)
    for c in alignment_classes:
        register_class(c)
    for c in schemes_classes:
        register_class(c)
    for c in rig_updater_classes:
        register_class(c)
    for c in snapping_classes:
        register_class(c)
    for c in body_picker_biped_classes:
        register_class(c)
    for c in body_picker_quadruped_classes:
        register_class(c)
    for c in face_picker_classes:
        register_class(c)
    for c in blenrig_rigs_classes:
        register_class(c)
    for c in bone_selecction_set_classes:
        register_class(c)
    for c in panels_classes:
        register_class(c)
    for c in boneshapes_classes:
        register_class(c)
    for c in shape_keys_classes:
        register_class(c)

    register_class(visual_assistant_props)

    # BlenRig Props
    bpy.types.WindowManager.blenrig_6_props = bpy.props.PointerProperty(type = blenrig_6_props)

    BlenRigPanelProperties = bpy.props.PointerProperty(type = blenrig_6_props)
    windowManager = bpy.types.WindowManager
    windowManager.BlenRigPanelSettings = BlenRigPanelProperties
    # Side Visibility Props
    bpy.types.Armature.visual_assistant = bpy.props.PointerProperty(type=visual_assistant_props)
    # BlenRig Object Add Panel
    bpy.types.VIEW3D_MT_armature_add.append(blenrig5_add_menu_func)


######## bone selections set ###############

    # Add properties.
    bpy.types.Object.blenrig_selection_sets = CollectionProperty(
        type=SelectionSet,
        name="Selection Sets",
        description="List of groups of bones for easy selection"
    )
    bpy.types.Object.blenrig_active_selection_set = IntProperty(
        name="Active Selection Set",
        description="Index of the currently active selection set",
        default=0
    )

    # Add shortcuts to the keymap.
    if not bpy.app.background:
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='Pose')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS', alt=True, shift=True)
        kmi.properties.name = 'POSE_MT_selection_sets_select'
        addon_keymaps.append((km, kmi))

    # Add entries to menus.
    bpy.types.VIEW3D_MT_select_pose.append(menu_func_select_selection_set)
############################################

######## Shape Keys+ #######################
    bpy.types.Scene.shape_keys_plus = bpy.props.PointerProperty(type=SceneProperties)
    bpy.types.Key.shape_keys_plus = bpy.props.PointerProperty(type=KeyProperties)
############################################

def unregister():

    from bpy.utils import unregister_class

    unregister_class(BLENRIG_PT_blenrig_6_general)
    unregister_class(BLENRIG_PT_blenrig_6_general_SubPanel)

    # BlenRig Props
    del bpy.types.WindowManager.blenrig_6_props
    # Side Visibility Props
    del bpy.types.Armature.visual_assistant
    # BlenRig Object Add Panel
    bpy.types.VIEW3D_MT_armature_add.remove(blenrig5_add_menu_func)

    # unload BlenRig internal classes
    for c in armature_classes:
        unregister_class(c)
    for c in alignment_classes:
        unregister_class(c)
    for c in schemes_classes:
        unregister_class(c)
    for c in rig_updater_classes:
        unregister_class(c)
    for c in snapping_classes:
        unregister_class(c)
    for c in body_picker_biped_classes:
        unregister_class(c)
    for c in body_picker_quadruped_classes:
        unregister_class(c)
    for c in face_picker_classes:
        unregister_class(c)
    for c in blenrig_rigs_classes:
        unregister_class(c)
    for c in bone_selecction_set_classes:
        unregister_class(c)
    for c in panels_classes:
        unregister_class(c)
    for c in boneshapes_classes:
        unregister_class(c)
    for c in shape_keys_classes:
        unregister_class(c)

    unregister_class(visual_assistant_props)

#######################register Guide ###################
    from .guides.register import unregister
    unregister()
#########################################################

######## bone selections set ###############
    # Clear properties.
    del bpy.types.Object.blenrig_selection_sets
    del bpy.types.Object.blenrig_active_selection_set

    # Clear shortcuts from the keymap.
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # Clear entries from menus.
    bpy.types.VIEW3D_MT_select_pose.remove(menu_func_select_selection_set)
######## bone selections set ###############

# Main variables.
    windowManager = bpy.types.WindowManager

    # Delete window manager's property group references.
    try:
        del windowManager.BlenRigPanelSettings
    except:
        pass
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

bl_info = {
    'name': 'BlenRig 6',
    'author': 'Juan Pablo Bouza , Sav Martin, Jorge Hernández - Meléndez',
    'version': (4,0,1),
    'blender': (4, 00, 0),
    'location': 'Armature, Object and Lattice properties, View3d tools panel, Armature Add menu',
    'description': 'BlenRig 6 rigging system',
    'wiki_url': 'https://cloud.blender.org/p/blenrig/56966411c379cf44546120e8',
    'tracker_url': 'https://gitlab.com/jpbouza/BlenRig/issues',
    'category': 'Rigging'
}


import bpy
import bmesh
from mathutils import Vector

from bpy.types import PropertyGroup, Armature, Menu, Operator, WindowManager, Object, Scene, Key, VIEW3D_MT_select_pose, VIEW3D_MT_armature_add
from bpy.props import StringProperty, FloatProperty, IntProperty, BoolProperty,EnumProperty, PointerProperty
from .props.pbones_props import pbones_props_register, pbones_props_unregister
from .props.armature_props import armature_props_register, armature_props_unregister

# Import panels
from .ui.panels.body_settings import BLENRIG_PT_Rig_Body_settings
from .ui.panels.facial_settings import BLENRIG_PT_Rig_Facial_settings
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

####### Armature Layers Operators
from .ops_arm_layers import BLENRIG_OP_armature_layers_rm, BLENRIG_OP_old_armature_layers_converter

#################### Blenrig Object Add Menu ###############

class INFO_MT_blenrig5_add_rig(Menu):
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
class ARMATURE_OT_blenrig_6_gui(Operator):
    "Display tab"
    bl_label = ""
    bl_idname = "gui.blenrig_6_tabs"

    tab: StringProperty(name="Tab", description="Tab of the gui to expand")

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
            # self.layers.append(bpy.context.active_object.data.collections[:])
            # if context.active_object.mode == 'POSE':
            #     if len(self.mode) > 1:
            #         bpy.ops.object.mode_set(mode= self.mode[-2])
            #     if len(self.layers) > 1:
            #         bpy.context.active_object.data.collections = self.layers[-2]
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

    displayContext : EnumProperty(
        name='Display Context',
        description="Type of context to display in this panel.",
        items=contextOptions,
        default='PICKER',
    )
    contextOptions2 = [('BONESHAPES', 'BoneShapes', "BoneShapes Tools", 'POSE_HLT', 0),
                        ('SHAPEKEYS', 'ShapeKeys', "ShapeKeys Tools", 'SURFACE_NCURVE', 1)]
    displayContext2 : EnumProperty(name='Display Context 2', description="Type of context to display in this panel.",items=contextOptions2, default='BONESHAPES')
    adjust_distance_cage : FloatProperty(name="Distance from object", description="Ajust the distance of Cage to object",update = snap_points_update, min=-10, max=10, default=0.1)

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
    Operator_Zoom_Selected,
    BLENRIG_OP_armature_layers_rm, # <- para eliminar items del listado de layers/collections pero impedir borrar los de BlenRig
    BLENRIG_OP_old_armature_layers_converter,
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

    pbones_props_register()
    armature_props_register()

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
    WindowManager.blenrig_6_props = PointerProperty(type = blenrig_6_props)
    WindowManager.BlenRigPanelSettings = PointerProperty(type = blenrig_6_props)
    # Side Visibility Props
    Armature.visual_assistant = PointerProperty(type=visual_assistant_props)
    # BlenRig Object Add Panel
    VIEW3D_MT_armature_add.append(blenrig5_add_menu_func)


######## bone selections set ###############

    # Add properties.
    Object.blenrig_selection_sets = CollectionProperty(
        type=SelectionSet,
        name="Selection Sets",
        description="List of groups of bones for easy selection"
    )
    Object.blenrig_active_selection_set = IntProperty(
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
    VIEW3D_MT_select_pose.append(menu_func_select_selection_set)
############################################

######## Shape Keys+ #######################
    Scene.shape_keys_plus = PointerProperty(type=SceneProperties)
    Key.shape_keys_plus = PointerProperty(type=KeyProperties)
############################################

def unregister():

    from bpy.utils import unregister_class

    pbones_props_unregister()
    armature_props_unregister()

    unregister_class(BLENRIG_PT_blenrig_6_general)
    unregister_class(BLENRIG_PT_blenrig_6_general_SubPanel)

    # BlenRig Props
    del WindowManager.blenrig_6_props
    # Side Visibility Props
    del Armature.visual_assistant
    # BlenRig Object Add Panel
    VIEW3D_MT_armature_add.remove(blenrig5_add_menu_func)

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
    del Object.blenrig_selection_sets
    del Object.blenrig_active_selection_set

    # Clear shortcuts from the keymap.
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # Clear entries from menus.
    VIEW3D_MT_select_pose.remove(menu_func_select_selection_set)
######## bone selections set ###############

# Main variables.

    # Delete window manager's property group references.
    try:
        del WindowManager.BlenRigPanelSettings
    except:
        pass

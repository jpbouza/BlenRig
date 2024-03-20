# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy

def register():
    from bpy.utils import register_class

    # Registrar los handlers.
    from . handlers import register as REGISTER_HANDLERS
    REGISTER_HANDLERS()

    # Registrar clases de properties.
    from .properties import BlenrigGuideImages, BlenrigGuideData, BlenRigBodyObj, BlenRigJointChain, BlenRigWPBones, BlenRigShapekeysList
    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    register_class(BlenrigGuideImages)
    register_class(BlenrigGuideData)
    scn.blenrig_guide = Pointer(type=BlenrigGuideData, name="Blenrig Guide")
    register_class(BlenRigBodyObj)
    scn.blenrig_character_body_obj = bpy.props.CollectionProperty(type=BlenRigBodyObj, name='BlenRig Character Body Objects')
    register_class(BlenRigJointChain)
    scn.blenrig_joint_chain_list = bpy.props.CollectionProperty(type=BlenRigJointChain, name='Joint List for Weight Painting Guide')
    register_class(BlenRigWPBones)
    scn.blenrig_wp_bones = bpy.props.CollectionProperty(type=BlenRigWPBones, name='Visible bones list for Weight Painting')
    register_class(BlenRigShapekeysList)
    scn.blenrig_shapekeys_list = bpy.props.CollectionProperty(type=BlenRigShapekeysList, name='Active Shapekeys List for Shapekeys Editting')

    # Registrar clases de gizmos.
    from . guide_gzg import BLENRIG_GZG_guide
    from . guide_gz import BLENRIG_GZ_guide
    from . guide_wg import BlenrigGuide_SafeCallStepAction, BlenrigGuide_SafeLoadStepImages
    register_class(BLENRIG_GZG_guide)
    register_class(BLENRIG_GZ_guide)
    register_class(BlenrigGuide_SafeCallStepAction)
    register_class(BlenrigGuide_SafeLoadStepImages)

    # Registrar PANELes y OPERATORs.
    from .panel import BlenRigGuidePanel,BlenRigGuidePanel_options
    from .guide_ops import (
        VIEW3D_OT_blenrig_guide_reproportion,
        VIEW3D_OT_blenrig_guide_datatransfer,
        VIEW3D_OT_blenrig_guide_mdef,
        VIEW3D_OT_blenrig_guide_lattices,
        VIEW3D_OT_blenrig_guide_actions,
        VIEW3D_OT_blenrig_guide_weights,
        VIEW3D_OT_blenrig_guide_rig_settings,
        VIEW3D_OT_blenrig_guide_shapekeys
    )
    from .operator import (Operator_Transfer_VGroups,
    Operator_Guide_Transfer_VGroups, Operator_blenrig_add_head_modifiers, Operator_blenrig_add_hands_modifiers, Operator_blenrig_add_body_shapekeys,
    Operator_blenrig_add_fingers_shapekeys, Operator_blenrig_add_toes_shapekeys, Operator_blenrig_add_face_shapekeys, Operator_blenrig_update_shapekey_driver,
    Operator_blenrig_update_face_shapekeys_drivers, Operator_blenrig_mirror_shapekeys_drivers, Operator_blenrig_mirror_active_shapekey_driver, Operator_blenrig_add_body_modifiers, Operator_blenrig_guide_add_body_modifiers,
    Operator_blenrig_bind_mdef_modifiers, Operator_blenrig_guide_bind_mdef_modifiers, Operator_blenrig_unbind_mdef_modifiers, Operator_blenrig_guide_unbind_mdef_modifiers,
    Operator_blenrig_mirror_lattice_transforms,
    Operator_blenrig_toggle_weight_painting, Operator_blenrigmirror_vp_rj_values, Operator_blenrig_wp_joint_chain_up, Operator_blenrig_wp_joint_chain_down,
    Operator_blenrig_define_body_area, Operator_blenrig_set_blenrig_armature, Operator_blenrig_select_vgroup, Operator_blenrig_edit_corrective_smooth_vgroup,
    Operator_blenrig_toggle_shapekey_editting, Operator_blenrig_blend_from_shape, Operator_blenrig_reset_shapekey, Operator_blenrig_mirror_active_shapekey, Operator_blenrig_mirror_all_shapekeys,
    Operator_Create_Sculpt_Shapekey_Object_From_pose, Operator_Apply_Sculpt_Object_to_Shapekey, Operator_Cancel_Sculpt_Object_to_Shapekey, Operator_blenrig_override_sculpt_objects,
    Operator_blenrig_wp_vgroup_chain_up, Operator_blenrig_wp_vgroup_chain_down, Operator_blenrig_snap_bone_to_cursor, Operator_blenrig_add_eyes_modifiers, Operator_blenrig_add_teeth_modifiers,
    Operator_Guide_Transfer_Test_Rig, Operator_blenrig_guide_edit_mdef_cage, Operator_blenrig_mirror_vertex_groups)

    register_class(VIEW3D_OT_blenrig_guide_reproportion)
    register_class(VIEW3D_OT_blenrig_guide_datatransfer)
    register_class(VIEW3D_OT_blenrig_guide_mdef)
    register_class(VIEW3D_OT_blenrig_guide_lattices)
    register_class(VIEW3D_OT_blenrig_guide_actions)
    register_class(VIEW3D_OT_blenrig_guide_weights)
    register_class(VIEW3D_OT_blenrig_guide_rig_settings)
    register_class(VIEW3D_OT_blenrig_guide_shapekeys)
    register_class(Operator_Transfer_VGroups)
    register_class(Operator_Guide_Transfer_VGroups)
    register_class(Operator_blenrig_add_head_modifiers)
    register_class(Operator_blenrig_add_hands_modifiers)
    register_class(Operator_blenrig_define_body_area)
    register_class(Operator_blenrig_set_blenrig_armature)
    register_class(Operator_blenrig_add_body_shapekeys)
    register_class(Operator_blenrig_add_fingers_shapekeys)
    register_class(Operator_blenrig_add_toes_shapekeys)
    register_class(Operator_blenrig_add_face_shapekeys)
    register_class(Operator_blenrig_update_shapekey_driver)
    register_class(Operator_blenrig_update_face_shapekeys_drivers)
    register_class(Operator_blenrig_mirror_shapekeys_drivers)
    register_class(Operator_blenrig_mirror_active_shapekey_driver)
    register_class(Operator_blenrig_blend_from_shape)
    register_class(Operator_blenrig_reset_shapekey)
    register_class(Operator_Create_Sculpt_Shapekey_Object_From_pose)
    register_class(Operator_Apply_Sculpt_Object_to_Shapekey)
    register_class(Operator_Cancel_Sculpt_Object_to_Shapekey)
    register_class(Operator_blenrig_override_sculpt_objects)
    register_class(Operator_blenrig_mirror_active_shapekey)
    register_class(Operator_blenrig_mirror_all_shapekeys)
    register_class(Operator_blenrig_add_body_modifiers)
    register_class(Operator_blenrig_guide_add_body_modifiers)
    register_class(Operator_blenrig_bind_mdef_modifiers)
    register_class(Operator_blenrig_guide_bind_mdef_modifiers)
    register_class(Operator_blenrig_unbind_mdef_modifiers)
    register_class(Operator_blenrig_guide_unbind_mdef_modifiers)
    register_class(Operator_blenrig_mirror_lattice_transforms)
    register_class(Operator_blenrig_toggle_weight_painting)
    register_class(Operator_blenrig_toggle_shapekey_editting)
    register_class(Operator_blenrigmirror_vp_rj_values)
    register_class(Operator_blenrig_wp_joint_chain_up)
    register_class(Operator_blenrig_wp_joint_chain_down)
    register_class(Operator_blenrig_wp_vgroup_chain_up)
    register_class(Operator_blenrig_wp_vgroup_chain_down)
    register_class(Operator_blenrig_select_vgroup)
    register_class(Operator_blenrig_edit_corrective_smooth_vgroup)
    register_class(Operator_blenrig_snap_bone_to_cursor)
    register_class(Operator_blenrig_add_eyes_modifiers)
    register_class(Operator_blenrig_add_teeth_modifiers)
    register_class(Operator_Guide_Transfer_Test_Rig)
    register_class(Operator_blenrig_guide_edit_mdef_cage)
    register_class(Operator_blenrig_mirror_vertex_groups)
    register_class(BlenRigGuidePanel_options)
    register_class(BlenRigGuidePanel)

def unregister():
    from bpy.utils import unregister_class

    # Unregister handlers.
    from . handlers import unregister as UNREGISTER_HANDLERS
    UNREGISTER_HANDLERS()

    # Unregister gizmos.
    from . guide_gzg import BLENRIG_GZG_guide
    from . guide_gz import BLENRIG_GZ_guide
    from . guide_wg import BlenrigGuide_SafeCallStepAction, BlenrigGuide_SafeLoadStepImages
    unregister_class(BLENRIG_GZG_guide)
    unregister_class(BLENRIG_GZ_guide)
    unregister_class(BlenrigGuide_SafeCallStepAction)
    unregister_class(BlenrigGuide_SafeLoadStepImages)

    # Unregister Operators.
    from .panel import BlenRigGuidePanel, BlenRigGuidePanel_options
    from .guide_ops import (
        VIEW3D_OT_blenrig_guide_reproportion,
        VIEW3D_OT_blenrig_guide_datatransfer,
        VIEW3D_OT_blenrig_guide_mdef,
        VIEW3D_OT_blenrig_guide_lattices,
        VIEW3D_OT_blenrig_guide_actions,
        VIEW3D_OT_blenrig_guide_weights,
        VIEW3D_OT_blenrig_guide_rig_settings,
        VIEW3D_OT_blenrig_guide_shapekeys
    )
    from .operator import (Operator_Transfer_VGroups,
    Operator_Guide_Transfer_VGroups, Operator_blenrig_add_head_modifiers, Operator_blenrig_add_hands_modifiers, Operator_blenrig_add_body_shapekeys,
    Operator_blenrig_add_fingers_shapekeys, Operator_blenrig_add_toes_shapekeys, Operator_blenrig_add_face_shapekeys, Operator_blenrig_update_shapekey_driver,
    Operator_blenrig_update_face_shapekeys_drivers, Operator_blenrig_mirror_shapekeys_drivers, Operator_blenrig_mirror_active_shapekey_driver, Operator_blenrig_add_body_modifiers, Operator_blenrig_guide_add_body_modifiers,
    Operator_blenrig_bind_mdef_modifiers, Operator_blenrig_guide_bind_mdef_modifiers, Operator_blenrig_unbind_mdef_modifiers, Operator_blenrig_guide_unbind_mdef_modifiers,
    Operator_blenrig_mirror_lattice_transforms,
    Operator_blenrig_toggle_weight_painting, Operator_blenrigmirror_vp_rj_values, Operator_blenrig_wp_joint_chain_up, Operator_blenrig_wp_joint_chain_down,
    Operator_blenrig_define_body_area, Operator_blenrig_set_blenrig_armature, Operator_blenrig_select_vgroup, Operator_blenrig_edit_corrective_smooth_vgroup,
    Operator_blenrig_toggle_shapekey_editting, Operator_blenrig_blend_from_shape, Operator_blenrig_reset_shapekey, Operator_blenrig_mirror_active_shapekey, Operator_blenrig_mirror_all_shapekeys,
    Operator_Create_Sculpt_Shapekey_Object_From_pose, Operator_Apply_Sculpt_Object_to_Shapekey, Operator_Cancel_Sculpt_Object_to_Shapekey, Operator_blenrig_override_sculpt_objects,
    Operator_blenrig_wp_vgroup_chain_up, Operator_blenrig_wp_vgroup_chain_down, Operator_blenrig_snap_bone_to_cursor, Operator_blenrig_add_eyes_modifiers, Operator_blenrig_add_teeth_modifiers,
    Operator_Guide_Transfer_Test_Rig, Operator_blenrig_guide_edit_mdef_cage, Operator_blenrig_mirror_vertex_groups)

    unregister_class(BlenRigGuidePanel_options)
    unregister_class(BlenRigGuidePanel)
    unregister_class(VIEW3D_OT_blenrig_guide_reproportion)
    unregister_class(VIEW3D_OT_blenrig_guide_datatransfer)
    unregister_class(VIEW3D_OT_blenrig_guide_mdef)
    unregister_class(VIEW3D_OT_blenrig_guide_lattices)
    unregister_class(VIEW3D_OT_blenrig_guide_actions)
    unregister_class(VIEW3D_OT_blenrig_guide_weights)
    unregister_class(VIEW3D_OT_blenrig_guide_rig_settings)
    unregister_class(VIEW3D_OT_blenrig_guide_shapekeys)
    unregister_class(Operator_Transfer_VGroups)
    unregister_class(Operator_Guide_Transfer_VGroups)
    unregister_class(Operator_blenrig_add_head_modifiers)
    unregister_class(Operator_blenrig_add_hands_modifiers)
    unregister_class(Operator_blenrig_define_body_area)
    unregister_class(Operator_blenrig_set_blenrig_armature)
    unregister_class(Operator_blenrig_add_body_shapekeys)
    unregister_class(Operator_blenrig_add_fingers_shapekeys)
    unregister_class(Operator_blenrig_add_toes_shapekeys)
    unregister_class(Operator_blenrig_add_face_shapekeys)
    unregister_class(Operator_blenrig_update_shapekey_driver)
    unregister_class(Operator_blenrig_update_face_shapekeys_drivers)
    unregister_class(Operator_blenrig_mirror_shapekeys_drivers)
    unregister_class(Operator_blenrig_mirror_active_shapekey_driver)
    unregister_class(Operator_blenrig_blend_from_shape)
    unregister_class(Operator_blenrig_reset_shapekey)
    unregister_class(Operator_Create_Sculpt_Shapekey_Object_From_pose)
    unregister_class(Operator_Apply_Sculpt_Object_to_Shapekey)
    unregister_class(Operator_Cancel_Sculpt_Object_to_Shapekey)
    unregister_class(Operator_blenrig_override_sculpt_objects)
    unregister_class(Operator_blenrig_mirror_active_shapekey)
    unregister_class(Operator_blenrig_mirror_all_shapekeys)
    unregister_class(Operator_blenrig_add_body_modifiers)
    unregister_class(Operator_blenrig_guide_add_body_modifiers)
    unregister_class(Operator_blenrig_bind_mdef_modifiers)
    unregister_class(Operator_blenrig_guide_bind_mdef_modifiers)
    unregister_class(Operator_blenrig_unbind_mdef_modifiers)
    unregister_class(Operator_blenrig_guide_unbind_mdef_modifiers)
    unregister_class(Operator_blenrig_mirror_lattice_transforms)
    unregister_class(Operator_blenrig_toggle_weight_painting)
    unregister_class(Operator_blenrig_toggle_shapekey_editting)
    unregister_class(Operator_blenrigmirror_vp_rj_values)
    unregister_class(Operator_blenrig_wp_joint_chain_up)
    unregister_class(Operator_blenrig_wp_joint_chain_down)
    unregister_class(Operator_blenrig_wp_vgroup_chain_up)
    unregister_class(Operator_blenrig_wp_vgroup_chain_down)
    unregister_class(Operator_blenrig_select_vgroup)
    unregister_class(Operator_blenrig_edit_corrective_smooth_vgroup)
    unregister_class(Operator_blenrig_snap_bone_to_cursor)
    unregister_class(Operator_blenrig_add_eyes_modifiers)
    unregister_class(Operator_blenrig_add_teeth_modifiers)
    unregister_class(Operator_Guide_Transfer_Test_Rig)
    unregister_class(Operator_blenrig_guide_edit_mdef_cage)
    unregister_class(Operator_blenrig_mirror_vertex_groups)
    from .properties import BlenrigGuideImages, BlenrigGuideData, BlenRigBodyObj, BlenRigJointChain, BlenRigWPBones, BlenRigShapekeysList
    from bpy.types import Scene as scn
    del scn.blenrig_guide
    del scn.blenrig_character_body_obj
    del scn.blenrig_joint_chain_list
    del scn.blenrig_wp_bones
    unregister_class(BlenrigGuideData)
    unregister_class(BlenrigGuideImages)
    unregister_class(BlenRigBodyObj)
    unregister_class(BlenRigJointChain)
    unregister_class(BlenRigWPBones)
    unregister_class(BlenRigShapekeysList)
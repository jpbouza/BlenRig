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
    from .properties import BlenrigGuideData, BlenRigBodyObj, BlenRigJointChain, BlenRigWPBones
    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    from bpy.utils import register_class
    register_class(BlenrigGuideData)
    scn.blenrig_guide = Pointer(type=BlenrigGuideData, name="Blenrig Guide")
    register_class(BlenRigBodyObj)
    scn.blenrig_character_body_obj = bpy.props.CollectionProperty(type=BlenRigBodyObj, name='BlenRig Character Body Objects')
    register_class(BlenRigJointChain)
    scn.blenrig_joint_chain_list = bpy.props.CollectionProperty(type=BlenRigJointChain, name='Joint List for Weight Painting Guide')
    register_class(BlenRigWPBones)
    scn.blenrig_wp_bones = bpy.props.CollectionProperty(type=BlenRigWPBones, name='Visible bones list for Weight Painting')


    from .panel import BlenRigGuidePanel,BlenRigGuidePanel_options
    from .guide_ops import (
        VIEW3D_OT_blenrig_guide_reproportion,
        VIEW3D_OT_blenrig_guide_datatransfer,
        VIEW3D_OT_blenrig_guide_mdef,
        VIEW3D_OT_blenrig_guide_lattices,
        VIEW3D_OT_blenrig_guide_actions,
        VIEW3D_OT_blenrig_guide_weights,
        VIEW3D_OT_blenrig_guide_shapekeys
    )
    from .operator import (Operator_Transfer_VGroups,
    Operator_Guide_Transfer_VGroups, Operator_blenrig_add_head_modifiers, Operator_blenrig_add_hands_modifiers, Operator_blenrig_add_body_shapekeys,
    Operator_blenrig_add_fingers_shapekeys, Operator_blenrig_add_toes_shapekeys, Operator_blenrig_add_face_shapekeys, Operator_blenrig_update_shapekey_driver,
    Operator_blenrig_update_face_shapekeys_drivers, Operator_blenrig_mirror_shapekeys_drivers, Operator_blenrig_mirror_active_shapekey_driver, Operator_blenrig_add_body_modifiers,
    Operator_blenrig_bind_mdef_modifiers, Operator_blenrig_guide_bind_mdef_modifiers, Operator_blenrig_unbind_mdef_modifiers, Operator_blenrig_guide_unbind_mdef_modifiers,
    Operator_blenrig_mirror_lattice_transforms,
    Operator_blenrig_toggle_weight_painting, Operator_blenrigmirror_vp_rj_values, Operator_blenrig_wp_joint_chain_up, Operator_blenrig_wp_joint_chain_down,
    Operator_blenrig_define_body_area, Operator_blenrig_select_vgroup, Operator_blenrig_edit_corrective_smooth_vgroup)

    register_class(VIEW3D_OT_blenrig_guide_reproportion)
    register_class(VIEW3D_OT_blenrig_guide_datatransfer)
    register_class(VIEW3D_OT_blenrig_guide_mdef)
    register_class(VIEW3D_OT_blenrig_guide_lattices)
    register_class(VIEW3D_OT_blenrig_guide_actions)
    register_class(VIEW3D_OT_blenrig_guide_weights)
    register_class(VIEW3D_OT_blenrig_guide_shapekeys)
    register_class(Operator_Transfer_VGroups)
    register_class(Operator_Guide_Transfer_VGroups)
    register_class(Operator_blenrig_add_head_modifiers)
    register_class(Operator_blenrig_add_hands_modifiers)
    register_class(Operator_blenrig_define_body_area)
    register_class(Operator_blenrig_add_body_shapekeys)
    register_class(Operator_blenrig_add_fingers_shapekeys)
    register_class(Operator_blenrig_add_toes_shapekeys)
    register_class(Operator_blenrig_add_face_shapekeys)
    register_class(Operator_blenrig_update_shapekey_driver)
    register_class(Operator_blenrig_update_face_shapekeys_drivers)
    register_class(Operator_blenrig_mirror_shapekeys_drivers)
    register_class(Operator_blenrig_mirror_active_shapekey_driver)
    register_class(Operator_blenrig_add_body_modifiers)
    register_class(Operator_blenrig_bind_mdef_modifiers)
    register_class(Operator_blenrig_guide_bind_mdef_modifiers)
    register_class(Operator_blenrig_unbind_mdef_modifiers)
    register_class(Operator_blenrig_guide_unbind_mdef_modifiers)
    register_class(Operator_blenrig_mirror_lattice_transforms)
    register_class(Operator_blenrig_toggle_weight_painting)
    register_class(Operator_blenrigmirror_vp_rj_values)
    register_class(Operator_blenrig_wp_joint_chain_up)
    register_class(Operator_blenrig_wp_joint_chain_down)
    register_class(Operator_blenrig_select_vgroup)
    register_class(Operator_blenrig_edit_corrective_smooth_vgroup)
    register_class(BlenRigGuidePanel_options)
    register_class(BlenRigGuidePanel)

def unregister():
    from .panel import BlenRigGuidePanel, BlenRigGuidePanel_options
    from .guide_ops import (
        VIEW3D_OT_blenrig_guide_reproportion,
        VIEW3D_OT_blenrig_guide_datatransfer,
        VIEW3D_OT_blenrig_guide_mdef,
        VIEW3D_OT_blenrig_guide_lattices,
        VIEW3D_OT_blenrig_guide_actions,
        VIEW3D_OT_blenrig_guide_weights,
        VIEW3D_OT_blenrig_guide_shapekeys
    )
    from .operator import (Operator_Transfer_VGroups,
    Operator_Guide_Transfer_VGroups, Operator_blenrig_add_head_modifiers, Operator_blenrig_add_hands_modifiers, Operator_blenrig_add_body_shapekeys,
    Operator_blenrig_add_fingers_shapekeys, Operator_blenrig_add_toes_shapekeys, Operator_blenrig_add_face_shapekeys, Operator_blenrig_update_shapekey_driver,
    Operator_blenrig_update_face_shapekeys_drivers, Operator_blenrig_mirror_shapekeys_drivers, Operator_blenrig_mirror_active_shapekey_driver, Operator_blenrig_add_body_modifiers,
    Operator_blenrig_bind_mdef_modifiers, Operator_blenrig_guide_bind_mdef_modifiers, Operator_blenrig_unbind_mdef_modifiers, Operator_blenrig_guide_unbind_mdef_modifiers,
    Operator_blenrig_mirror_lattice_transforms,
    Operator_blenrig_toggle_weight_painting, Operator_blenrigmirror_vp_rj_values, Operator_blenrig_wp_joint_chain_up, Operator_blenrig_wp_joint_chain_down,
    Operator_blenrig_define_body_area, Operator_blenrig_select_vgroup, Operator_blenrig_edit_corrective_smooth_vgroup)

    from bpy.utils import unregister_class
    unregister_class(BlenRigGuidePanel_options)
    unregister_class(BlenRigGuidePanel)
    unregister_class(VIEW3D_OT_blenrig_guide_reproportion)
    unregister_class(VIEW3D_OT_blenrig_guide_datatransfer)
    unregister_class(VIEW3D_OT_blenrig_guide_mdef)
    unregister_class(VIEW3D_OT_blenrig_guide_lattices)
    unregister_class(VIEW3D_OT_blenrig_guide_actions)
    unregister_class(VIEW3D_OT_blenrig_guide_weights)
    unregister_class(VIEW3D_OT_blenrig_guide_shapekeys)
    unregister_class(Operator_Transfer_VGroups)
    unregister_class(Operator_Guide_Transfer_VGroups)
    unregister_class(Operator_blenrig_add_head_modifiers)
    unregister_class(Operator_blenrig_add_hands_modifiers)
    unregister_class(Operator_blenrig_define_body_area)
    unregister_class(Operator_blenrig_add_body_shapekeys)
    unregister_class(Operator_blenrig_add_fingers_shapekeys)
    unregister_class(Operator_blenrig_add_toes_shapekeys)
    unregister_class(Operator_blenrig_add_face_shapekeys)
    unregister_class(Operator_blenrig_update_shapekey_driver)
    unregister_class(Operator_blenrig_update_face_shapekeys_drivers)
    unregister_class(Operator_blenrig_mirror_shapekeys_drivers)
    unregister_class(Operator_blenrig_mirror_active_shapekey_driver)
    unregister_class(Operator_blenrig_add_body_modifiers)
    unregister_class(Operator_blenrig_bind_mdef_modifiers)
    unregister_class(Operator_blenrig_guide_bind_mdef_modifiers)
    unregister_class(Operator_blenrig_unbind_mdef_modifiers)
    unregister_class(Operator_blenrig_guide_unbind_mdef_modifiers)
    unregister_class(Operator_blenrig_mirror_lattice_transforms)
    unregister_class(Operator_blenrig_toggle_weight_painting)
    unregister_class(Operator_blenrigmirror_vp_rj_values)
    unregister_class(Operator_blenrig_wp_joint_chain_up)
    unregister_class(Operator_blenrig_wp_joint_chain_down)
    unregister_class(Operator_blenrig_select_vgroup)
    unregister_class(Operator_blenrig_edit_corrective_smooth_vgroup)
    from .properties import BlenrigGuideData, BlenRigBodyObj, BlenRigJointChain, BlenRigWPBones
    from bpy.types import Scene as scn
    del scn.blenrig_guide
    del scn.blenrig_character_body_obj
    del scn.blenrig_joint_chain_list
    del scn.blenrig_wp_bones
    unregister_class(BlenrigGuideData)
    unregister_class(BlenRigBodyObj)
    unregister_class(BlenRigJointChain)
    unregister_class(BlenRigWPBones)
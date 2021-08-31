import bpy
from .. utils import *

def frame_bones(context, *bone_names):
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bone_names)
    frame_selected()
    deselect_all_pose_bones(context)

def select_armature(operator, context):
    # Select previously active Armature
    go_blenrig_pose_mode(context)

#Generic Function for Editting Actions
def edit_action(operator, context, step_name, frame_bone_1, frame_bone_2, view, action, frame_number, bone_list, active_bone, layer_list):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = step_name

    deselect_all_objects(context)

    #Armature for setting view
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    #Toggle Pose X-Mirror
    toggle_pose_x_mirror(context, True)

    #Reset Transforms
    reset_all_bones_transforms()

    # Adjust view to Bones.
    frame_bones(context, frame_bone_1, frame_bone_2)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint(view)

    #Assign Action
    assign_action(action, frame_number)

    #Turn On Actions Layer
    on_layers = layer_list
    for l in on_layers:
        bpy.context.object.data.layers[l] = True

    #Bones
    bones = bone_list

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)
    deselect_all_pose_bones(context)

    #Set Active Bone
    select_pose_bone(context, active_bone)

    #Lock Object Mode Off
    bpy.context.scene.tool_settings.lock_object_mode = True

def mute_constraints(constraint_name, c_mute):
    guide_props = bpy.context.scene.blenrig_guide
    for b in guide_props.arm_obj.pose.bones:
        for C in b.constraints:
            if C.type == 'ACTION':
                if constraint_name in C.name:
                    C.mute = c_mute

#### ACTIONS STEPS ####

def ACTIONS_Fingers_Spread_X_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_X_Up',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_x', 1,
    ['fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L'],
    'fing_lit_ctrl_mstr_L',
    [28]
    )

def ACTIONS_Fingers_Spread_X_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_X_Down',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_x', -1,
    ['fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L'],
    'fing_lit_ctrl_mstr_L',
    [28]
    )

def ACTIONS_Fingers_Spread_Z_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_Z_Out',
    'hand_ik_ctrl_L', 'hand_close_L',
    'RIGHT',
    'zrig_fing_spread_z', 1,
    ['fing_ind_ctrl_mstr_L', 'fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L'],
    'fing_lit_ctrl_mstr_L',
    [28]
    )

def ACTIONS_Fingers_Spread_Z_In(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_Z_Out',
    'hand_ik_ctrl_L', 'hand_close_L',
    'RIGHT',
    'zrig_fing_spread_z', -1,
    ['fing_ind_ctrl_mstr_L', 'fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L'],
    'fing_lit_ctrl_mstr_L',
    [28]
    )

def ACTIONS_Fingers_Curl_In(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Curl_In',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_scale', 4,
    ['fing_lit_ctrl_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L'],
    'fing_ind_ctrl_L',
    [5, 28]
    )
    #Step Locks
    set_locks(['fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], True, True, True, True, True, True, True, False, True)

def ACTIONS_Fingers_Curl_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Curl_Out',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_scale', -4,
    ['fing_lit_ctrl_mstr_L', 'fing_lit_ctrl_L', 'fing_ring_ctrl_mstr_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_mstr_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_mstr_L', 'fing_mid_ctrl_L'],
    'fing_ind_ctrl_L',
    [5, 28]
    )
    #Step Locks
    set_locks(['fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], True, True, True, True, True, True, True, False, True)

def ACTIONS_Hand_Close(operator, context):
    edit_action(operator, context,
    'ACTIONS_Hand_Close',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_hand_close', 4,
    ['fing_lit_ctrl_mstr_L', 'fing_lit_ctrl_L', 'fing_ring_ctrl_mstr_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_mstr_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_mstr_L', 'fing_mid_ctrl_L', 'fing_thumb_ctrl_mstr_L', 'fing_thumb_ctrl_L'],
    'fing_thumb_ctrl_mstr_L',
    [5, 28]
    )
    #Step Locks
    set_locks(['fing_thumb_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], True, True, True, True, True, True, True, False, True)

def ACTIONS_Hand_Open(operator, context):
    edit_action(operator, context,
    'ACTIONS_Hand_Open',
    'hand_ik_ctrl_L', 'hand_close_L',
    'TOP',
    'zrig_hand_close', -4,
    ['fing_lit_ctrl_mstr_L', 'fing_lit_ctrl_L', 'fing_ring_ctrl_mstr_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_mstr_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_mstr_L', 'fing_mid_ctrl_L', 'fing_thumb_ctrl_mstr_L', 'fing_thumb_ctrl_L'],
    'fing_thumb_ctrl_mstr_L',
    [5, 28]
    )
    #Step Locks
    set_locks(['fing_thumb_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], True, True, True, True, True, True, True, False, True)

def ACTIONS_Breathing_in(operator, context):
    edit_action(operator, context,
    'ACTIONS_Breathing_in',
    'head_stretch', 'pelvis_ctrl',
    'RIGHT',
    'zrig_breathing', 1,
    ['neck_1_fk', 'head_fk', 'spine_2_fk', 'spine_3_toon', 'spine_3_fk', 'spine_4_toon', 'shoulder_R', 'shoulder_toon_R', 'shoulder_L', 'shoulder_toon_L', 'spine_ctrl_curve'],
    'spine_ctrl_curve',
    [4, 7, 13, 28]
    )

def ACTIONS_Breathing_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Breathing_Out',
    'head_stretch', 'pelvis_ctrl',
    'RIGHT',
    'zrig_breathing', -1,
    ['neck_1_fk', 'head_fk', 'spine_2_fk', 'spine_3_toon', 'spine_3_fk', 'spine_4_toon', 'shoulder_R', 'shoulder_toon_R', 'shoulder_L', 'shoulder_toon_L', 'spine_ctrl_curve'],
    'spine_ctrl_curve',
    [4, 7, 13, 28]
    )

def ACTIONS_Eyelids_Up_Up_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Up_Range',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['eyelid_up_ctrl_L'],
    'eyelid_up_ctrl_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_up_up = guide_props.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L

    #Diable Action Constraints
    mute_constraints('Eyelid_Upper_Up', True)

def ACTIONS_Eyelids_Up_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Up',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_upper', -1,
    ['eyelid_up_rot_2_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_up_rot_3_L', 'eyelid_up_ctrl_3_mstr_L', 'eyelid_up_rot_1_L', 'eyelid_up_ctrl_1_mstr_L'],
    'eyelid_up_ctrl_2_mstr_L',
    [28]
    )

def ACTIONS_Eyelids_Up_Down_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Down_Range',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['eyelid_up_ctrl_L'],
    'eyelid_up_ctrl_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_up_down = guide_props.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L

    #Diable Action Constraints
    mute_constraints('Eyelid_Upper_Down', True)

def ACTIONS_Eyelids_Up_Down_1(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Down_1',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_upper', 1,
    ['eyelid_up_rot_2_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_up_rot_3_L', 'eyelid_up_ctrl_3_mstr_L', 'eyelid_up_rot_1_L', 'eyelid_up_ctrl_1_mstr_L'],
    'eyelid_up_ctrl_2_mstr_L',
    [28]
    )

def ACTIONS_Eyelids_Up_Down_2(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Down_2',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_upper', 2,
    ['eyelid_up_rot_2_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_up_rot_3_L', 'eyelid_up_ctrl_3_mstr_L', 'eyelid_up_rot_1_L', 'eyelid_up_ctrl_1_mstr_L'],
    'eyelid_up_ctrl_2_mstr_L',
    [28]
    )

def ACTIONS_Eyelids_Low_Down_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Low_Down_Range',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['eyelid_low_ctrl_L'],
    'eyelid_low_ctrl_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_low_down = guide_props.arm_obj.pose.bones["eyelid_low_ctrl_L"].EYELID_DOWN_LIMIT_L

    #Diable Action Constraints
    mute_constraints('Eyelid_Lower_Down', True)

def ACTIONS_Eyelids_Low_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Low_Down',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_lower', -1,
    ['eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_low_rot_2_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_rot_3_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_low_rot_1_L', 'eyelid_low_ctrl_1_mstr_L'],
    'eyelid_low_ctrl_2_mstr_L',
    [28]
    )

def ACTIONS_Eyelids_Low_Up_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Low_Up_Range',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['eyelid_low_ctrl_L'],
    'eyelid_low_ctrl_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_low_up = guide_props.arm_obj.pose.bones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L

    #Diable Action Constraints
    mute_constraints('Eyelid_Lower_Up', True)

def ACTIONS_Eyelids_Low_Up_1(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Low_Up_1',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_lower', 1,
    ['eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_low_rot_2_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_rot_3_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_low_rot_1_L', 'eyelid_low_ctrl_1_mstr_L'],
    'eyelid_low_ctrl_2_mstr_L',
    [28]
    )

def ACTIONS_Eyelids_Low_Up_2(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Low_Up_2',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_lower', 2,
    ['eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_low_rot_2_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_rot_3_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_low_rot_1_L', 'eyelid_low_ctrl_1_mstr_L'],
    'eyelid_low_ctrl_2_mstr_L',
    [28]
    )

def ACTIONS_Eyelids_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Out',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_sides', 1,
    ['eyelid_up_rot_2_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_up_rot_3_L', 'eyelid_up_ctrl_3_mstr_L',
    'eyelid_up_rot_1_L', 'eyelid_up_ctrl_1_mstr_L', 'eyelid_low_rot_2_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_rot_3_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_low_rot_1_L', 'eyelid_low_ctrl_1_mstr_L'],
    'eyelid_up_ctrl_2_mstr_L',
    [28]
    )

    #Diable Action Constraints
    mute_constraints('Eyelid_Out', True)

    #Disable Eye Constraint
    guide_props = bpy.context.scene.blenrig_guide
    for C in guide_props.arm_obj.pose.bones["eye_def_L"].constraints:
        C.mute = True
    for C in guide_props.arm_obj.pose.bones["eye_def_R"].constraints:
        C.mute = True

    #Change Rotation Mode
    guide_props.arm_obj.pose.bones["eye_def_L"].rotation_mode = 'XYZ'
    guide_props.arm_obj.pose.bones["eye_def_R"].rotation_mode = 'XYZ'

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_out = guide_props.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_OUT_LIMIT_L

def ACTIONS_Eyelids_In(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_In',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_sides', 3,
    ['eyelid_up_rot_2_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_up_rot_3_L', 'eyelid_up_ctrl_3_mstr_L',
    'eyelid_up_rot_1_L', 'eyelid_up_ctrl_1_mstr_L', 'eyelid_low_rot_2_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_rot_3_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_low_rot_1_L', 'eyelid_low_ctrl_1_mstr_L'],
    'eyelid_up_ctrl_2_mstr_L',
    [28]
    )

    #Diable Action Constraints
    mute_constraints('Eyelid_In', True)

    #Disable Eye Constraint
    guide_props = bpy.context.scene.blenrig_guide
    for C in guide_props.arm_obj.pose.bones["eye_def_L"].constraints:
        C.mute = True
    for C in guide_props.arm_obj.pose.bones["eye_def_R"].constraints:
        C.mute = True

    #Change Rotation Mode
    guide_props.arm_obj.pose.bones["eye_def_L"].rotation_mode = 'XYZ'
    guide_props.arm_obj.pose.bones["eye_def_R"].rotation_mode = 'XYZ'

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_in = guide_props.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_IN_LIMIT_L

def ACTIONS_Cheek_Up_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Cheek_Up_Range',
    'brow_ctrl_curve_L', 'nostril_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['cheek_ctrl_L'],
    'cheek_ctrl_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_cheek_up = guide_props.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L

def ACTIONS_Cheek_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Cheek_Up',
    'brow_ctrl_curve_L', 'nostril_ctrl_L',
    'FRONT',
    'zrig_cheeks', 1,
    ['cheek_line_ctrl_2_L', 'cheek_line_ctrl_3_L', 'eyelid_rim_low_ctrl_1_L', 'eyelid_rim_low_ctrl_3_L', 'eyelid_rim_low_ctrl_2_L', 'cheekbone_ctrl_3_L', 'cheekbone_ctrl_2_L', 'cheekbone_ctrl_1_L'],
    'cheekbone_ctrl_3_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_cheek_up = guide_props.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["cheek_ctrl_L"]["ACTION_CHEEK_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["cheek_ctrl_R"]["ACTION_CHEEK_TOGGLE_R"] = 0

def ACTIONS_Cheek_Down_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Cheek_Down_Range',
    'brow_ctrl_curve_L', 'nostril_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['cheek_ctrl_L'],
    'cheek_ctrl_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_cheek_down = guide_props.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_DOWN_LIMIT_L

def ACTIONS_Cheek_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Cheek_Down',
    'brow_ctrl_curve_L', 'nostril_ctrl_L',
    'FRONT',
    'zrig_cheeks', -1,
    ['cheek_line_ctrl_2_L', 'cheek_line_ctrl_3_L', 'eyelid_rim_low_ctrl_1_L', 'eyelid_rim_low_ctrl_3_L', 'eyelid_rim_low_ctrl_2_L', 'cheekbone_ctrl_3_L', 'cheekbone_ctrl_2_L', 'cheekbone_ctrl_1_L'],
    'cheekbone_ctrl_3_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_cheek_down = guide_props.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_DOWN_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["cheek_ctrl_L"]["ACTION_CHEEK_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["cheek_ctrl_R"]["ACTION_CHEEK_TOGGLE_R"] = 0

def ACTIONS_Cheek_Frown(operator, context):
    edit_action(operator, context,
    'ACTIONS_Cheek_Frown',
    'brow_ctrl_curve_L', 'nostril_ctrl_L',
    'FRONT',
    'zrig_cheeks_frown', 1,
    ['cheek_line_ctrl_2_L', 'cheek_line_ctrl_3_L', 'eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_out_mstr_L',
    'eyelid_up_ctrl_3_mstr_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_rim_low_ctrl_3_L', 'eyelid_rim_low_ctrl_2_L',
    'brow_ctrl_5_L', 'brow_ctrl_2_L', 'brow_ctrl_3_L', 'brow_ctrl_4_L', 'cheekbone_ctrl_3_L', 'cheekbone_ctrl_2_L'],
    'cheekbone_ctrl_3_L',
    [0, 1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_cheek_up = guide_props.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L

def ACTIONS_Nose_Frown_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Nose_Frown_Range',
    'brow_ctrl_curve_L', 'nose_tip_ctrl_mstr',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['nose_frown_ctrl_L'],
    'nose_frown_ctrl_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_nose_frown = guide_props.arm_obj.pose.bones["nose_frown_ctrl_L"].FROWN_LIMIT_L

def ACTIONS_Nose_Frown(operator, context):
    edit_action(operator, context,
    'ACTIONS_Nose_Frown',
    'brow_ctrl_curve_L', 'nose_tip_ctrl_mstr',
    'FRONT',
    'zrig_nose_frown', 1,
    ['cheek_line_ctrl_1_L', 'cheek_line_ctrl_2_L', 'eyelid_rim_low_ctrl_1_L', 'eyelid_rim_low_ctrl_2_L', 'nose_bridge_up_ctrl_L',
    'smile_line_ctrl_1_L', 'nose_bridge_low_ctrl_L', 'nostril_up_ctrl_L', 'nose_root_ctrl_L', 'cheekbone_ctrl_2_L', 'cheekbone_ctrl_1_L', 'nostril_ctrl_L'],
    'cheek_line_ctrl_1_L',
    [28]
    )

def ACTIONS_Nose_Frown_Max(operator, context):
    edit_action(operator, context,
    'ACTIONS_Nose_Frown_Max',
    'brow_ctrl_curve_L', 'nose_tip_ctrl_mstr',
    'FRONT',
    'zrig_nose_frown_max', 1,
    ['cheek_line_ctrl_1_L', 'cheek_line_ctrl_2_L', 'eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_up_ctrl_1_mstr_L',
    'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_ctrl_1_mstr_L', 'frown_ctrl', 'eyelid_rim_low_ctrl_1_L', 'eyelid_rim_low_ctrl_2_L', 'brow_low_ctrl_1_L', 'brow_low_ctrl_2_L', 'brow_low_ctrl_3_L',
    'nose_bridge_up_ctrl_L', 'smile_line_ctrl_1_L', 'nostril_up_ctrl_L', 'nose_root_ctrl_L', 'cheekbone_ctrl_2_L', 'cheekbone_ctrl_1_L', 'nostril_ctrl_L'],
    'cheek_line_ctrl_1_L',
    [0, 1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_nose_frown = guide_props.arm_obj.pose.bones["nose_frown_ctrl_L"].FROWN_LIMIT_L

def ACTIONS_Jaw_Down_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Jaw_Down_Range',
    'head_stretch', 'head_fk',
    'RIGHT',
    'No_Action_For_This_Step', 0,
    ['maxi'],
    'maxi',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_jaw_down = guide_props.arm_obj.pose.bones["maxi"].JAW_DOWN_LIMIT

def ACTIONS_Jaw_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Jaw_Down',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_maxi_up_down', -1,
    ['mouth_low', 'lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L', 'mouth_up', 'smile_line_ctrl_2_L', 'teeth_low', 'teeth_up', 'lip_low_ctrl_3_mstr_L',
    'lip_up_ctrl_4_mstr_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_3_mstr_L'],
    'lip_up_ctrl_3_mstr_L',
    [0, 1, 2, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_jaw_down = guide_props.arm_obj.pose.bones["maxi"].JAW_DOWN_LIMIT

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["maxi"]["ACTION_UP_DOWN_TOGGLE"] = 0

def ACTIONS_Jaw_Up_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Jaw_Up_Range',
    'head_stretch', 'head_fk',
    'RIGHT',
    'No_Action_For_This_Step', 0,
    ['maxi'],
    'maxi',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_jaw_up = guide_props.arm_obj.pose.bones["maxi"].JAW_UP_LIMIT

def ACTIONS_Jaw_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Jaw_Up',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_maxi_up_down', 1,
    ['mouth_low', 'lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L', 'mouth_up','lip_up_outer_ctrl', 'smile_line_ctrl_2_L', 'teeth_low', 'teeth_up',
    'lip_up_ctrl_4_mstr_L', 'smile_line_ctrl_1_L', 'nose_base_ctrl'],
    'nose_base_ctrl',
    [0, 1, 2, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_jaw_up = guide_props.arm_obj.pose.bones["maxi"].JAW_UP_LIMIT

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["maxi"]["ACTION_UP_DOWN_TOGGLE"] = 0

def ACTIONS_Mouth_Corner_Out_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Out_Range',
    'head_stretch', 'head_fk',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['mouth_corner_L'],
    'mouth_corner_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_out = guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

def ACTIONS_Mouth_Corner_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Out',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_corner_out', 1,
    ['cheek_line_ctrl_2_L', 'cheek_line_ctrl_3_L', 'lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L',
    'jaw_line_ctrl_4_L', 'lip_low_outer_ctrl_4_L', 'cheek_line_ctrl_4_L', 'smile_line_ctrl_3_L', 'cheek_side_ctrl_L', 'chin_ctrl_3_L',
    'chin_ctrl_2_L', 'chin_ctrl_1_L', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L',
    'lip_up_outer_ctrl_2_L', 'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L', 'lip_low_rim_ctrl_2_L',
    'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'jaw_line_ctrl_3_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L',
    'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L',
    'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L', 'nostril_ctrl_L'],
    'smile_line_ctrl_3_L',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_out = guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_OUT_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_OUT_TOGGLE_R"] = 0

def ACTIONS_Mouth_Corner_Up_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Up_Range',
    'head_stretch', 'head_fk',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['mouth_corner_L'],
    'mouth_corner_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_up = guide_props.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_L"].location[0] = -0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_R"].location[0] = 0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

def ACTIONS_Mouth_Corner_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Up',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_corner_up', 1,
    ['cheek_line_ctrl_2_L', 'cheek_line_ctrl_3_L', 'lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'jaw_line_ctrl_4_L', 'lip_low_outer_ctrl_4_L',
    'cheek_line_ctrl_4_L', 'smile_line_ctrl_3_L', 'cheek_side_ctrl_L', 'chin_ctrl_3_L', 'chin_ctrl_2_L', 'chin_ctrl_1_L', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L',
    'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L', 'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L', 'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L',
    'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'jaw_line_ctrl_3_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L',
    'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L',
    'lip_up_line_ctrl_3_L', 'nostril_ctrl_L'],
    'smile_line_ctrl_2_L',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_up = guide_props.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_L"].location[0] = -0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_R"].location[0] = 0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_UP_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_UP_TOGGLE_R"] = 0

def ACTIONS_Mouth_Corner_Down_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Down_Range',
    'head_stretch', 'head_fk',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['mouth_corner_L'],
    'mouth_corner_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_down = guide_props.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_L"].location[0] = -0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_R"].location[0] = 0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

def ACTIONS_Mouth_Corner_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Down',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_corner_down', 1,
    ['lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'jaw_line_ctrl_4_L', 'lip_low_outer_ctrl_4_L', 'cheek_line_ctrl_4_L',
    'smile_line_ctrl_3_L', 'cheek_side_ctrl_L', 'chin_ctrl_3_L', 'chin_ctrl_2_L', 'chin_ctrl_1_L', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L',
    'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L', 'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L', 'lip_low_rim_ctrl_2_L',
    'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'jaw_line_ctrl_3_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L',
    'smile_line_ctrl_1_L', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L',
    'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L', 'nostril_ctrl_L'],
    'jaw_line_ctrl_3_L',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_down = guide_props.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_L"].location[0] = -0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_R"].location[0] = 0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_DOWN_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_DOWN_TOGGLE_R"] = 0

def ACTIONS_Mouth_Corner_Back_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Back_Range',
    'head_stretch', 'head_fk',
    'RIGHT',
    'No_Action_For_This_Step', 0,
    ['mouth_corner_L'],
    'mouth_corner_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_back = guide_props.arm_obj.pose.bones["mouth_corner_L"].BACK_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_L"].location[0] = -0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_R"].location[0] = 0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

def ACTIONS_Mouth_Corner_Back(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Back',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_mouth_corner_back', 1,
    ['cheek_line_ctrl_2_L', 'cheek_line_ctrl_3_L', 'lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'jaw_line_ctrl_4_L',
    'lip_low_outer_ctrl_4_L', 'cheek_line_ctrl_4_L', 'smile_line_ctrl_3_L', 'cheek_side_ctrl_L', 'chin_ctrl_3_L', 'chin_ctrl_2_L', 'chin_ctrl_1_L', 'lip_up_outer_ctrl_1_L',
    'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L', 'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L',
    'lip_low_ctrl_2_mstr_L', 'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'jaw_line_ctrl_3_L', 'lip_up_ctrl_4_mstr_L',
    'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L',
    'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L', 'nostril_ctrl_L'],
    'lip_up_rim_ctrl_4_L',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_back = guide_props.arm_obj.pose.bones["mouth_corner_L"].BACK_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_L"].location[0] = -0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_corner_R"].location[0] = 0.25 * guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_BACK_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_BACK_TOGGLE_R"] = 0

def ACTIONS_Mouth_Corner_Forw_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Forw_Range',
    'head_stretch', 'head_fk',
    'RIGHT',
    'No_Action_For_This_Step', 0,
    ['mouth_corner_L'],
    'mouth_corner_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_forw = guide_props.arm_obj.pose.bones["mouth_corner_L"].FORW_LIMIT_L

def ACTIONS_Mouth_Corner_Forw(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Forw',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_mouth_corner_forw', 1,
    ['lip_up_ctrl_4_mstr_L'],
    'lip_up_ctrl_4_mstr_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_forw = guide_props.arm_obj.pose.bones["mouth_corner_L"].FORW_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_FORW_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_FORW_TOGGLE_R"] = 0

def ACTIONS_Mouth_Corner_In_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_In_Range',
    'head_stretch', 'head_fk',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['mouth_corner_L'],
    'mouth_corner_L',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_in = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

def ACTIONS_Mouth_Corner_In(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_In',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_corner_in', 1,
    ['lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'lip_low_outer_ctrl_4_L', 'cheek_line_ctrl_4_L', 'smile_line_ctrl_3_L',
    'chin_ctrl_3_L', 'chin_ctrl_2_L', 'chin_ctrl_1_L', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L',
    'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L', 'lip_low_rim_ctrl_2_L',
    'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'mouth_corner_mstr_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L',
    'smile_line_ctrl_1_L', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L',
    'lip_up_line_ctrl_3_L', 'nostril_ctrl_L'],
    'lip_up_ctrl_1_mstr_L',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_in = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_IN_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_IN_TOGGLE_R"] = 0

def ACTIONS_Mouth_Corner_In_Zipper(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_In_Zipper',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_corner_in', 1,
    ['lip_zipper_ctrl_mid', 'lip_zipper_ctrl_3_L', 'lip_zipper_ctrl_2_L', 'lip_zipper_ctrl_1_L'],
    'lip_zipper_ctrl_1_L',
    [2, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_in = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_IN_TOGGLE_L"] = 0
    guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_IN_TOGGLE_R"] = 0

    #Activate Zipper
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_corner_L"].scale[2] = 0.5
    guide_props.arm_obj.pose.bones["mouth_corner_R"].scale[2] = 0.5

def ACTIONS_Mouth_Corner_Up_Out_Corrective(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Up_Out_Corrective',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_up_out_corrective', 1,
    ['lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L', 'chin_ctrl_3_L', 'chin_ctrl_2_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'smile_line_ctrl_1_L'],
    'smile_line_ctrl_2_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_out = guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.guide_mouth_corner_up = guide_props.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_ctrl"]["CORRECTIVE_ACTIONS_TOGGLE"] = 0

def ACTIONS_Mouth_Corner_Down_Out_Corrective(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Corner_Down_Out_Corrective',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_mouth_down_out_corrective', 1,
    ['smile_line_ctrl_3_L', 'chin_ctrl_3_L', 'chin_ctrl_2_L', 'smile_line_ctrl_2_L', 'smile_line_ctrl_1_L'],
    'chin_ctrl_3_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_corner_out = guide_props.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L
    guide_props.guide_mouth_corner_down = guide_props.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_ctrl"]["CORRECTIVE_ACTIONS_TOGGLE"] = 0

def ACTIONS_U_O_M_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_U_O_M_Range',
    'head_stretch', 'head_fk',
    'RIGHT',
    'No_Action_For_This_Step', 0,
    ['mouth_up_ctrl', 'mouth_low_ctrl'],
    'mouth_up_ctrl',
    [0, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_u_o_m = guide_props.arm_obj.pose.bones["mouth_ctrl"].U_M_CTRL_LIMIT

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_ctrl"]["U_O_M_ACTION_TOGGLE"] = 0

    #Disable Action Constraints for Editting
    mute_constraints('U_O_M_Up_NOREP', True)
    mute_constraints('U_O_M_Low_NOREP', True)

def ACTIONS_U(operator, context):
    edit_action(operator, context,
    'ACTIONS_U',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_U_O_M', 1,
    ['lip_up_outer_ctrl_mid', 'lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_mid', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'lip_low_outer_ctrl',
    'chin_ctrl', 'lip_low_ctrl', 'lip_low_ctrl_collision_override', 'lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L', 'lip_up_ctrl', 'lip_up_ctrl_collision_override',
    'lip_up_outer_ctrl', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L',
    'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L',
    'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'lip_low_ctrl_mstr_mid', 'lip_low_rim_ctrl_mid',
    'lip_low_line_ctrl_mid', 'mouth_corner_mstr_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_mstr_mid', 'lip_up_rim_ctrl_mid',
    'lip_up_line_ctrl_mid', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L',
    'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L', 'nose_base_ctrl'],
    'lip_up_ctrl',
    [0, 1, 28]
    )

def ACTIONS_U_Zipper(operator, context):
    edit_action(operator, context,
    'ACTIONS_U_Zipper',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_U_O_M', 1,
    ['lip_zipper_ctrl_mid', 'lip_zipper_ctrl_3_L', 'lip_zipper_ctrl_2_L', 'lip_zipper_ctrl_1_L'],
    'lip_zipper_ctrl_1_L',
    [28]
    )

    #Activate Zipper
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_corner_L"].scale[2] = 0.5
    guide_props.arm_obj.pose.bones["mouth_corner_R"].scale[2] = 0.5

def ACTIONS_O(operator, context):
    edit_action(operator, context,
    'ACTIONS_O',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_U_O_M', 2,
    ['lip_up_outer_ctrl_mid', 'lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_mid', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'lip_low_outer_ctrl',
    'chin_ctrl', 'lip_low_ctrl', 'lip_low_ctrl_collision_override', 'lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L', 'lip_up_ctrl', 'lip_up_ctrl_collision_override',
    'lip_up_outer_ctrl', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L',
    'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L',
    'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'lip_low_ctrl_mstr_mid', 'lip_low_rim_ctrl_mid',
    'lip_low_line_ctrl_mid', 'mouth_corner_mstr_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_mstr_mid', 'lip_up_rim_ctrl_mid',
    'lip_up_line_ctrl_mid', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L',
    'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L', 'nose_base_ctrl'],
    'lip_up_ctrl',
    [28]
    )

def ACTIONS_O_Zipper(operator, context):
    edit_action(operator, context,
    'ACTIONS_O_Zipper',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_U_O_M', 2,
    ['lip_zipper_ctrl_mid', 'lip_zipper_ctrl_3_L', 'lip_zipper_ctrl_2_L', 'lip_zipper_ctrl_1_L'],
    'lip_zipper_ctrl_1_L',
    [28]
    )

    #Activate Zipper
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_corner_L"].scale[2] = 0.5
    guide_props.arm_obj.pose.bones["mouth_corner_R"].scale[2] = 0.5

def ACTIONS_U_Narrow_Corrective(operator, context):
    edit_action(operator, context,
    'ACTIONS_U_Narrow_Corrective',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_U_narrow_corrective', 1,
    ['lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L',
    'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L',
    'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L', 'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L',
    'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'lip_low_ctrl_mstr_mid', 'lip_low_rim_ctrl_mid', 'lip_low_line_ctrl_mid', 'mouth_corner_mstr_L',
    'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_mstr_mid', 'lip_up_rim_ctrl_mid', 'lip_up_line_ctrl_mid', 'lip_up_ctrl_1_mstr_L',
    'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L'],
    'lip_up_ctrl_1_mstr_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_ctrl"].location[0] = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_ctrl"]["CORRECTIVE_ACTIONS_TOGGLE"] = 0

def ACTIONS_U_Narrow_Corrective_Zipper(operator, context):
    edit_action(operator, context,
    'ACTIONS_U_Narrow_Corrective_Zipper',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_U_narrow_corrective', 1,
    ['lip_zipper_ctrl_mid', 'lip_zipper_ctrl_3_L', 'lip_zipper_ctrl_2_L', 'lip_zipper_ctrl_1_L'],
    'lip_zipper_ctrl_1_L',
    [28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_ctrl"].location[0] = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

    #Turn off Action Constraint for Editting
    guide_props.arm_obj.pose.bones["mouth_ctrl"]["CORRECTIVE_ACTIONS_TOGGLE"] = 0

    #Activate Zipper
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_corner_L"].scale[2] = 0.5
    guide_props.arm_obj.pose.bones["mouth_corner_R"].scale[2] = 0.5

def ACTIONS_U_Thicker_Lips(operator, context):
    edit_action(operator, context,
    'ACTIONS_U_Thicker_Lips',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_U_thickness', -1,
    ['lip_low_outer_ctrl', 'lip_low_ctrl', 'lip_up_ctrl', 'lip_up_outer_ctrl', 'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L',
    'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'lip_low_ctrl_mstr_mid', 'lip_low_rim_ctrl_mid', 'lip_low_line_ctrl_mid',
    'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'lip_up_ctrl_mstr_mid', 'lip_up_rim_ctrl_mid', 'lip_up_line_ctrl_mid', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L',
    'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L'],
    'lip_up_line_ctrl_1_L',
    [0, 1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_ctrl"].location[0] = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_ctrl"].scale[:] = (0.5, 0.5, 0.5)

def ACTIONS_U_Thinner_Lips(operator, context):
    edit_action(operator, context,
    'ACTIONS_U_Thinner_Lips',
    'head_stretch', 'head_fk',
    'FRONT',
    'zrig_U_thickness', 1,
    ['lip_low_outer_ctrl', 'lip_low_ctrl', 'lip_up_ctrl', 'lip_up_outer_ctrl', 'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L',
    'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'lip_low_ctrl_mstr_mid', 'lip_low_rim_ctrl_mid', 'lip_low_line_ctrl_mid',
    'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'lip_up_ctrl_mstr_mid', 'lip_up_rim_ctrl_mid', 'lip_up_line_ctrl_mid', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L',
    'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L', 'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L'],
    'lip_up_ctrl',
    [0, 1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property so that controller moves
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones["mouth_ctrl"].location[0] = guide_props.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L
    guide_props.arm_obj.pose.bones["mouth_ctrl"].scale[:] = (2.0, 2.0, 2.0)

def ACTIONS_M(operator, context):
    edit_action(operator, context,
    'ACTIONS_M',
    'head_stretch', 'head_fk',
    'RIGHT',
    'zrig_U_O_M', -2,
    ['lip_up_outer_ctrl_mid', 'lip_low_outer_ctrl_1_L', 'lip_low_outer_ctrl_mid', 'lip_low_outer_ctrl_2_L', 'lip_low_outer_ctrl_3_L', 'lip_low_outer_ctrl',
    'chin_ctrl', 'lip_low_ctrl_collision_override', 'lip_low_outer_ctrl_4_L', 'smile_line_ctrl_3_L', 'lip_up_ctrl_collision_override',
    'lip_up_outer_ctrl', 'lip_up_outer_ctrl_1_L', 'lip_up_outer_ctrl_3_L', 'lip_up_outer_ctrl_4_L', 'smile_line_ctrl_2_L', 'lip_up_outer_ctrl_2_L',
    'lip_low_ctrl_3_mstr_L', 'lip_low_rim_ctrl_3_L', 'lip_low_line_ctrl_3_L', 'lip_low_ctrl_2_mstr_L',
    'lip_low_rim_ctrl_2_L', 'lip_low_line_ctrl_2_L', 'lip_low_ctrl_1_mstr_L', 'lip_low_rim_ctrl_1_L', 'lip_low_line_ctrl_1_L', 'lip_low_ctrl_mstr_mid', 'lip_low_rim_ctrl_mid',
    'lip_low_line_ctrl_mid', 'mouth_corner_mstr_L', 'lip_up_ctrl_4_mstr_L', 'lip_up_rim_ctrl_4_L', 'lip_up_line_ctrl_4_L', 'smile_line_ctrl_1_L', 'lip_up_ctrl_mstr_mid', 'lip_up_rim_ctrl_mid',
    'lip_up_line_ctrl_mid', 'lip_up_ctrl_1_mstr_L', 'lip_up_rim_ctrl_1_L', 'lip_up_line_ctrl_1_L', 'lip_up_ctrl_2_mstr_L', 'lip_up_rim_ctrl_2_L', 'lip_up_line_ctrl_2_L', 'lip_up_ctrl_3_mstr_L',
    'lip_up_rim_ctrl_3_L', 'lip_up_line_ctrl_3_L', 'nose_base_ctrl'],
    'lip_up_ctrl_collision_override',
    [0, 1, 28]
    )

def ACTIONS_Mouth_Frown_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Frown_Range',
    'nose_tip_ctrl_mstr', 'chin_frown_ctrl',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['mouth_frown_ctrl_L'],
    'mouth_frown_ctrl_L',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_mouth_frown = guide_props.arm_obj.pose.bones["mouth_frown_ctrl_L"].FROWN_LIMIT_L

    #Disable Action Constraints for Editting
    mute_constraints('Mouth_Frown_L_NOREP', True)
    mute_constraints('Mouth_Frown_R_NOREP', True)

def ACTIONS_Mouth_Frown(operator, context):
    edit_action(operator, context,
    'ACTIONS_Mouth_Frown',
    'nose_tip_ctrl_mstr', 'chin_frown_ctrl',
    'FRONT',
    'zrig_mouth_frown', 2,
    ['chin_ctrl_mstr', 'lip_low_outer_ctrl', 'lip_low_ctrl', 'lip_up_ctrl', 'mouth_corner_L'],
    'mouth_corner_L',
    [0, 1, 28]
    )

def ACTIONS_Chin_Frown_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Chin_Frown_Range',
    'nose_tip_ctrl_mstr', 'chin_frown_ctrl',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['chin_frown_ctrl'],
    'chin_frown_ctrl',
    [1, 28]
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_chin_frown = guide_props.arm_obj.pose.bones["chin_frown_ctrl"].FROWN_LIMIT

    #Disable Action Constraints for Editting
    mute_constraints('Chin_Frown_NOREP', True)


def ACTIONS_Chin_Frown_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Chin_Frown_Up',
    'nose_tip_ctrl_mstr', 'chin_frown_ctrl',
    'FRONT',
    'zrig_chin_frown', 1,
    ['chin_ctrl_mstr', 'lip_low_outer_ctrl', 'chin_ctrl', 'lip_low_ctrl', 'lip_up_ctrl', 'lip_up_outer_ctrl', 'nose_base_ctrl'],
    'lip_low_outer_ctrl',
    [0, 1, 28]
    )

def ACTIONS_Chin_Frown_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Chin_Frown_Down',
    'nose_tip_ctrl_mstr', 'chin_frown_ctrl',
    'FRONT',
    'zrig_chin_frown', -1,
    ['chin_ctrl_mstr', 'lip_low_outer_ctrl', 'chin_ctrl', 'lip_low_ctrl', 'lip_up_ctrl', 'lip_up_outer_ctrl', 'nose_base_ctrl'],
    'chin_ctrl',
    [0, 1, 28]
    )

#### END OF STEP ACTIONS ####

def actions_end_generic(context):
    guide_props = context.scene.blenrig_guide

    #Force Pose Position
    bpy.context.active_object.data.pose_position = 'POSE'

    #Ensure Symmetry
    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Left Side
    for b in context.pose_object.data.bones:
        if b.name.endswith('_L'):
            b.select = True

    if bpy.context.active_object.pose.use_mirror_x == True:
        mirror_pose()
    deselect_all_pose_bones(context)

    #Clear Action and Transforms
    clear_action()

    #Reset Transforms
    reset_all_bones_transforms()

    #Toggle Pose X-Mirror
    toggle_pose_x_mirror(context, False)

    #Turn Layers off
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Lock Object Mode Off
    bpy.context.scene.tool_settings.lock_object_mode = False

#Property for action to be performed after steps
def end_of_step_action(context):
    guide_props = context.scene.blenrig_guide
    current_step = context.scene.blenrig_guide.guide_current_step
    actions_end_generic(context)
    if current_step == 'ACTIONS_Fingers_Curl_In':
        #Step Locks
        set_locks(['fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], False, False, False, False, False, False, True, False, True)
    if current_step == 'ACTIONS_Fingers_Curl_Out':
        #Step Locks
        set_locks(['fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], False, False, False, False, False, False, True, False, True)
    if current_step == 'ACTIONS_Hand_Close':
        #Step Locks
        set_locks(['fing_thumb_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], False, False, False, False, False, False, True, False, True)
    if current_step == 'ACTIONS_Hand_Open':
        #Step Locks
        set_locks(['fing_thumb_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'], False, False, False, False, False, False, True, False, True)
    if current_step == 'ACTIONS_Eyelids_Up_Up_Range':
        #Enable Action Constraints
        mute_constraints('Eyelid_Upper_Up', False)
    if current_step == 'ACTIONS_Eyelids_Up_Down_Range':
        #Enable Action Constraints
        mute_constraints('Eyelid_Upper_Down', False)
    if current_step == 'ACTIONS_Eyelids_Low_Down_Range':
        #Enable Action Constraints
        mute_constraints('Eyelid_Lower_Down', False)
    if current_step == 'ACTIONS_Eyelids_Low_Up_Range':
        #Enable Action Constraints
        mute_constraints('Eyelid_Lower_Up', False)
    if current_step == 'ACTIONS_Eyelids_Out':
        #Enable Action Constraints
        mute_constraints('Eyelid_Out', False)
        #Rotate Eye
        guide_props = context.scene.blenrig_guide
        for C in guide_props.arm_obj.pose.bones["eye_def_L"].constraints:
            C.mute = False
        for C in guide_props.arm_obj.pose.bones["eye_def_R"].constraints:
            C.mute = False
        #Change Rotation Mode
        guide_props.arm_obj.pose.bones["eye_def_L"].rotation_mode = 'QUATERNION'
        guide_props.arm_obj.pose.bones["eye_def_R"].rotation_mode = 'QUATERNION'
    if current_step == 'ACTIONS_Eyelids_In':
        #Enable Action Constraints
        mute_constraints('Eyelid_In', False)
        #Rotate Eye
        guide_props = context.scene.blenrig_guide
        for C in guide_props.arm_obj.pose.bones["eye_def_L"].constraints:
            C.mute = False
        for C in guide_props.arm_obj.pose.bones["eye_def_R"].constraints:
            C.mute = False
        #Change Rotation Mode
        guide_props.arm_obj.pose.bones["eye_def_L"].rotation_mode = 'QUATERNION'
        guide_props.arm_obj.pose.bones["eye_def_R"].rotation_mode = 'QUATERNION'
    if current_step == 'ACTIONS_Cheek_Up' or current_step == 'ACTIONS_Cheek_Down':
        #Turn Action Constraint back On
        guide_props.arm_obj.pose.bones["cheek_ctrl_L"]["ACTION_CHEEK_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["cheek_ctrl_R"]["ACTION_CHEEK_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Jaw_Up' or current_step == 'ACTIONS_Jaw_Down':
        #Turn Action Constraint back On
        guide_props.arm_obj.pose.bones["maxi"]["ACTION_UP_DOWN_TOGGLE"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_Out':
        guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_OUT_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_OUT_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_Up':
        guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_UP_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_UP_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_Down':
        guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_DOWN_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_DOWN_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_Back':
        guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_BACK_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_BACK_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_Forw':
        guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_FORW_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_FORW_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_In' or current_step == 'ACTIONS_Mouth_Corner_In_Zipper':
        guide_props.arm_obj.pose.bones["mouth_corner_L"]["ACTION_IN_TOGGLE_L"] = 1
        guide_props.arm_obj.pose.bones["mouth_corner_R"]["ACTION_IN_TOGGLE_R"] = 1
    if current_step == 'ACTIONS_Mouth_Corner_Up_Out_Corrective' or current_step == 'ACTIONS_Mouth_Corner_Down_Out_Corrective' or current_step == 'ACTIONS_U_Narrow_Corrective' or current_step == 'ACTIONS_U_Narrow_Corrective_Zipper':
        guide_props.arm_obj.pose.bones["mouth_ctrl"]["CORRECTIVE_ACTIONS_TOGGLE"] = 1
    if current_step == 'ACTIONS_U_O_M_Range':
        guide_props.arm_obj.pose.bones["mouth_ctrl"]["U_O_M_ACTION_TOGGLE"] = 1
        #Enable Action Constraints
        mute_constraints('U_O_M_Up_NOREP', False)
        mute_constraints('U_O_M_Low_NOREP', False)
    if current_step == 'ACTIONS_Mouth_Frown_Range':
        #Enable Action Constraints
        mute_constraints('Mouth_Frown_L_NOREP', False)
        mute_constraints('Mouth_Frown_R_NOREP', False)
    if current_step == 'ACTIONS_Chin_Frown_Range':
        #Enable Action Constraints
        mute_constraints('Chin_Frown_NOREP', False)


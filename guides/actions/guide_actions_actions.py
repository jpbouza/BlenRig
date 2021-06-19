import bpy
from .. utils import *

def frame_bones(context, *bone_names):
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bone_names)
    frame_selected()
    deselect_all_pose_bones(context)

def select_armature(operator, context):
    # Select previously active Armature
    if context.mode != 'OBJECT':
        set_mode('OBJECT')
    set_active_object(context, operator.arm_obj)
    set_mode('POSE')

#Generic Function for Editting Actions
def edit_action(operator, context, step_name, frame_bone_1, frame_bone_2, view, action, frame_number, bone_list):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = step_name

    deselect_all_objects(context)

    #Armature for setting view
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

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
    on_layers = [28]
    for l in on_layers:
        bpy.context.object.data.layers[l] = True

    #Bones
    bones = bone_list

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)
    deselect_all_pose_bones(context)


#### ACTIONS STEPS ####

def ACTIONS_Fingers_Spread_X_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_X_Up',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_x', 1,
    ['fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L']
    )

def ACTIONS_Fingers_Spread_X_Down(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_X_Down',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_x', -1,
    ['fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L']
    )

def ACTIONS_Fingers_Spread_Z_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_Z_Out',
    'hand_ik_ctrl_L', 'hand_close_L',
    'RIGHT',
    'zrig_fing_spread_z', 1,
    ['fing_ind_ctrl_mstr_L', 'fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L']
    )

def ACTIONS_Fingers_Spread_Z_In(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Spread_Z_Out',
    'hand_ik_ctrl_L', 'hand_close_L',
    'RIGHT',
    'zrig_fing_spread_z', -1,
    ['fing_ind_ctrl_mstr_L', 'fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L']
    )

def ACTIONS_Fingers_Curl_In(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Curl_In',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_scale', 4,
    ['fing_lit_ctrl_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L']
    )

def ACTIONS_Fingers_Curl_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Fingers_Curl_Out',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_fing_spread_scale', -4,
    ['fing_lit_ctrl_mstr_L', 'fing_lit_ctrl_L', 'fing_ring_ctrl_mstr_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_mstr_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_mstr_L', 'fing_mid_ctrl_L']
    )

def ACTIONS_Hand_Close(operator, context):
    edit_action(operator, context,
    'ACTIONS_Hand_Close',
    'hand_ik_ctrl_L', 'hand_close_L',
    'FRONT',
    'zrig_hand_close', 4,
    ['fing_lit_ctrl_mstr_L', 'fing_lit_ctrl_L', 'fing_ring_ctrl_mstr_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_mstr_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_mstr_L', 'fing_mid_ctrl_L', 'fing_thumb_ctrl_mstr_L', 'fing_thumb_ctrl_L']
    )

def ACTIONS_Hand_Open(operator, context):
    edit_action(operator, context,
    'ACTIONS_Hand_Open',
    'hand_ik_ctrl_L', 'hand_close_L',
    'TOP',
    'zrig_hand_close', -4,
    ['fing_lit_ctrl_mstr_L', 'fing_lit_ctrl_L', 'fing_ring_ctrl_mstr_L', 'fing_ring_ctrl_L', 'fing_ind_ctrl_mstr_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_mstr_L', 'fing_mid_ctrl_L', 'fing_thumb_ctrl_mstr_L', 'fing_thumb_ctrl_L']
    )

def ACTIONS_Breathing_in(operator, context):
    edit_action(operator, context,
    'ACTIONS_Breathing_in',
    'head_stretch', 'pelvis_ctrl',
    'RIGHT',
    'zrig_breathing', 1,
    ['neck_1_fk', 'head_fk', 'spine_2_fk', 'spine_3_toon', 'spine_3_fk', 'spine_4_toon', 'shoulder_R', 'shoulder_toon_R', 'shoulder_L', 'shoulder_toon_L', 'spine_ctrl_curve']
    )

def ACTIONS_Breathing_Out(operator, context):
    edit_action(operator, context,
    'ACTIONS_Breathing_Out',
    'head_stretch', 'pelvis_ctrl',
    'RIGHT',
    'zrig_breathing', -1,
    ['neck_1_fk', 'head_fk', 'spine_2_fk', 'spine_3_toon', 'spine_3_fk', 'spine_4_toon', 'shoulder_R', 'shoulder_toon_R', 'shoulder_L', 'shoulder_toon_L', 'spine_ctrl_curve']
    )

def ACTIONS_Eyelids_Up_Up_Range(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Up_Range',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'No_Action_For_This_Step', 0,
    ['eyelid_up_ctrl_L']
    )

    #Assign value from Facial Movement Ranges to Guide Property
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_eyelid_up_up = guide_props.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L

def ACTIONS_Eyelids_Up_Up(operator, context):
    edit_action(operator, context,
    'ACTIONS_Eyelids_Up_Up',
    'brow_ctrl_curve_L', 'eyelid_low_rim_ctrl_L',
    'FRONT',
    'zrig_eyelids_upper', -1,
    ['eyelid_up_rot_2_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_ctrl_in_mstr_L', 'eyelid_ctrl_out_mstr_L', 'eyelid_up_rot_3_L', 'eyelid_up_ctrl_3_mstr_L', 'eyelid_up_rot_1_L', 'eyelid_up_ctrl_1_mstr_L']
    )

#### END OF STEP ACTIONS ####

def actions_end_generic(context):
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

    #Turn Layers on
    off_layers = [28]
    for l in off_layers:
        bpy.context.object.data.layers[l] = False

#Property for action to be performed after steps
def end_of_step_action(context):
    current_step = bpy.context.scene.blenrig_guide.guide_current_step
    steps = ['ACTIONS_Fingers_Spread_X_Up', 'ACTIONS_Fingers_Spread_X_Down', 'ACTIONS_Fingers_Spread_Z_Out', 'ACTIONS_Fingers_Spread_Z_In',
    'ACTIONS_Fingers_Curl_In', 'ACTIONS_Fingers_Curl_Out', 'ACTIONS_Hand_Close', 'ACTIONS_Hand_Open', 'ACTIONS_Breathing_in', 'ACTIONS_Breathing_Out', 'ACTIONS_Eyelids_Up_Up_Range', 'ACTIONS_Eyelids_Up_Up']
    for step in steps:
        if current_step == step:
            actions_end_generic(context)
            bpy.context.scene.blenrig_guide.guide_current_step = ''

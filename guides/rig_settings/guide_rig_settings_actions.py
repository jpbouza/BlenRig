import bpy
from .. utils import *

def frame_bones(context, *bone_names):
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bone_names)
    frame_selected()
    deselect_all_pose_bones(context)

def select_armature(context):
    # Select previously active Armature
    go_blenrig_pose_mode(context)

def joint_rotations(BONE, LOC_1, ROT_1, SCALE_1, LOC_2, ROT_2, SCALE_2, LOC_3, ROT_3, SCALE_3, LOC_4, ROT_4, SCALE_4, LOC_5, ROT_5, SCALE_5, LOC_6, ROT_6, SCALE_6, PROP_VALUE):
    #Set Bone and Angles
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_transformation_bone = BONE
    guide_props.guide_rotation_1 = ROT_1
    guide_props.guide_rotation_2 = ROT_2
    guide_props.guide_rotation_3 = ROT_3
    guide_props.guide_rotation_4 = ROT_4
    guide_props.guide_rotation_5 = ROT_5
    guide_props.guide_rotation_6 = ROT_6
    guide_props.guide_location_1 = LOC_1
    guide_props.guide_location_2 = LOC_2
    guide_props.guide_location_3 = LOC_3
    guide_props.guide_location_4 = LOC_4
    guide_props.guide_location_5 = LOC_5
    guide_props.guide_location_6 = LOC_6
    guide_props.guide_scale_1 = SCALE_1
    guide_props.guide_scale_2 = SCALE_2
    guide_props.guide_scale_3 = SCALE_3
    guide_props.guide_scale_4 = SCALE_4
    guide_props.guide_scale_5 = SCALE_5
    guide_props.guide_scale_6 = SCALE_6
    #Set Pose property
    if guide_props.guide_transform_steps == 'x6':
        guide_props.guide_joint_transforms_X6 = PROP_VALUE
    elif guide_props.guide_transform_steps == 'x4':
        guide_props.guide_joint_transforms_X4 = PROP_VALUE
    elif guide_props.guide_transform_steps == 'x2'   :
        guide_props.guide_joint_transforms_X2 = PROP_VALUE

def weight_step(operator, context, step_name,
joint_type, joint_parameters,
frame_bone_1, frame_bone_2, view,
bone_list, layers_list, active_bone_list):

    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    #Perform end of step action and set current step name
    end_of_step_action(context)
    guide_props.guide_current_step = step_name

    #Create Joint List and Vgroup List for Scrolling through joints within the step
    joint_list = active_bone_list

    #Clear List
    bpy.context.scene.blenrig_joint_chain_list.clear()

    #Add bones to list
    for i in range(len(joint_list)):
        joint_item = joint_list[i]
        add_item = bpy.context.scene.blenrig_joint_chain_list.add()
        add_item.joint = joint_item

    #Reset Transforms
    reset_all_bones_transforms()

    #Set Bone and Angles
    guide_props.guide_transform_steps = joint_type
    param_list = joint_parameters
    joint_rotations(*param_list)

    deselect_all_objects(context)

    #Show Armature
    show_armature(context)

    #Turn Off Pose Symmetry
    guide_props.arm_obj.pose.use_mirror_x = False

    # Adjust view to Bones.
    frame_bones(context, frame_bone_1, frame_bone_2)
    # Front View.
    set_view_perspective(context, False)
    set_viewpoint(view)

    #Turn On Deformation Layer
    on_layers = layers_list
    for l in on_layers:
        bpy.context.object.data.layers[l] = True

    #Show Bones
    bones = bone_list

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Set Active Bone
    select_pose_bone(context, joint_list[0])

    #Lock Object Mode Off
    bpy.context.scene.tool_settings.lock_object_mode = True

#### RIG SETTTINGS STEPS ####

def SETTINGS_Intro(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'SETTINGS_Intro'

def SETTINGS_Shoulder_Movement(operator, context):
    weight_step(operator, context, 'SETTINGS_Shoulder_Movement',
    'x2', ['arm_fk_ctrl_L',
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'RIGHT',
    ['hand_ik_ctrl_L', 'arm_ik_L', 'clavi_def_L', ],
    [16, 27],
    ['arm_fk_ctrl_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].toggle_arm_ik_pole_L =  0
    bpy.ops.snap.arm_fk_to_ik_l()

    #Select Hand IK
    deselect_all_pose_bones(context)
    select_pose_bone(context, 'hand_ik_ctrl_L')

    #Collect values, then Assign values to scene property
    forw_value = p_bones["shoulder_L"]["SHLDR_AUTO_FORW_L"]
    back_value = p_bones["shoulder_L"]["SHLDR_AUTO_BACK_L"]
    up_value = p_bones["shoulder_L"]["SHLDR_AUTO_UP_L"]
    down_value = p_bones["shoulder_L"]["SHLDR_AUTO_DOWN_L"]

    guide_props.guide_shoulder_auto_forw = forw_value
    guide_props.guide_shoulder_auto_back = back_value
    guide_props.guide_shoulder_auto_up = up_value
    guide_props.guide_shoulder_auto_down = down_value

def SETTINGS_Torso_Rotation(operator, context):
    weight_step(operator, context, 'SETTINGS_Torso_Rotation',
    'x2', ['torso_fk_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, -45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['torso_fk_ctrl', 'spine_1_def', 'spine_2_def', 'spine_3_def'],
    [7, 27],
    ['torso_fk_ctrl'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Set Rig Control Properties
    p_bones["properties_torso"].ik_torso = 1.0

def SETTINGS_Neck_Rotation(operator, context):
    weight_step(operator, context, 'SETTINGS_Neck_Rotation',
    'x2', ['neck_fk_ctrl',
    (0.0, 0.0, 0.0), (45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'neck_1_fk', 'head_stretch', 'RIGHT',
    ['neck_fk_ctrl', 'neck_1_def', 'neck_2_def', 'neck_3_def'],
    [4, 27],
    ['neck_fk_ctrl'])

def SETTINGS_Torso_Inv_Rotation(operator, context):
    weight_step(operator, context, 'SETTINGS_Torso_Inv_Rotation',
    'x2', ['torso_fk_ctrl_inv',
    (0.0, 0.0, 0.0), (0.0, 0.0, 45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['torso_fk_ctrl_inv', 'spine_1_def', 'spine_2_def', 'pelvis_def'],
    [18, 27],
    ['torso_fk_ctrl_inv'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Set Rig Control Properties
    p_bones["properties_torso"].ik_torso = 1.0

def SETTINGS_Torso_Stretching(operator, context):
    weight_step(operator, context, 'SETTINGS_Torso_Stretching',
    'x2', ['pelvis_ctrl',
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones['pelvis_def'].length, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['pelvis_ctrl', 'spine_1_def', 'spine_2_def', 'spine_3_def', 'pelvis_def'],
    [7, 27],
    ['pelvis_ctrl'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Set Rig Control Properties
    p_bones["properties_torso"].ik_torso = 1.0

def SETTINGS_Pelvis_Compensation(operator, context):
    weight_step(operator, context, 'SETTINGS_Pelvis_Compensation',
    'x2', ['pelvis_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 33), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['pelvis_ctrl', 'spine_1_def', 'spine_2_def', 'spine_3_def', 'pelvis_def'],
    [7, 27],
    ['pelvis_ctrl'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Set Rig Control Properties
    p_bones["properties_torso"].ik_torso = 1.0

def SETTINGS_Foot_Roll(operator, context):
    weight_step(operator, context, 'SETTINGS_Foot_Roll',
    'x2', ['foot_roll_ctrl_L',
    (0.0, 0.0, 0.0), (45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_roll_ctrl_L', 'toe_roll_2_L', 'RIGHT',
    ['foot_roll_ctrl_L', 'foot_def_L', 'foot_toe_1_def_L', 'foot_toe_2_def_L'],
    [9, 27],
    ['foot_roll_ctrl_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    amp_value = p_bones["foot_roll_ctrl_L"]["FOOT_ROLL_AMPLITUD_L"]
    toe_1_value = p_bones["foot_roll_ctrl_L"]["TOE_1_ROLL_START_L"]
    toe_2_value = p_bones["foot_roll_ctrl_L"]["TOE_2_ROLL_START_L"]

    guide_props.guide_foot_roll_amp = amp_value
    guide_props.guide_foot_roll_toe_1 = toe_1_value
    guide_props.guide_foot_roll_toe_2 = toe_2_value

def SETTINGS_Volume_Variation(operator, context):
    weight_step(operator, context, 'SETTINGS_Volume_Variation',
    'x2', ['torso_fk_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'master', 'head_stretch', 'FRONT',
    ['head_fk', 'head_stretch', 'torso_fk_ctrl', 'pelvis_ctrl', 'sole_ctrl_L', 'fing_lit_5_toon_L', 'fing_lit_4_toon_L', 'fing_lit_3_toon_L', 'fing_ring_5_toon_L', 'fing_ring_4_toon_L',
    'fing_ring_3_toon_L', 'fing_ind_5_toon_L', 'fing_ind_4_toon_L', 'fing_ind_3_toon_L', 'fing_mid_5_toon_L', 'fing_mid_4_toon_L', 'fing_mid_3_toon_L', 'fing_thumb_4_toon_L', 'fing_thumb_3_toon_L',
    'fing_thumb_2_toon_L', 'hand_ik_ctrl_L', 'toe_3_toon_L', 'toe_2_toon_L', 'toe_lit_4_toon_L', 'toe_lit_3_toon_L', 'toe_big_4_toon_L', 'toe_big_3_toon_L', 'toe_fourth_5_toon_L', 'toe_fourth_3_toon_L',
    'toe_mid_5_toon_L', 'toe_mid_3_toon_L', 'toe_ind_5_toon_L', 'toe_ind_3_toon_L', 'toe_lit_2_toon_L', 'toe_big_2_toon_L', 'toe_fourth_2_toon_L', 'toe_mid_2_toon_L', 'toe_ind_2_toon_L',
    'sole_ctrl_L', 'elbow_toon_L', 'knee_toon_L'],
    [0, 4, 7, 9, 13, 14, 16, 27],
    ['torso_fk_ctrl'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Enable Stretchy IK
    guide_props.arm_obj.pose.bones["properties_arm_L"].toon_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_L"].toon_leg_L =  1.0

    #Collect values, then Assign values to scene property
    arms_value = p_bones["properties_arm_L"].volume_variation_arm_L
    fingers_value = p_bones["properties_arm_L"].volume_variation_fingers_L
    legs_value = p_bones["properties_leg_L"].volume_variation_leg_L
    toes_value = p_bones["properties_leg_L"].volume_variation_toes_L

    guide_props.guide_vol_var_arms = arms_value
    guide_props.guide_vol_var_fingers = fingers_value
    guide_props.guide_vol_var_legs = legs_value
    guide_props.guide_vol_var_toes = toes_value

def SETTINGS_Feet_Floor(operator, context):
    weight_step(operator, context, 'SETTINGS_Feet_Floor',
    'x2', ['foot_floor_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'shin_fk_L', 'foot_floor_L', 'RIGHT',
    ['foot_floor_L'],
    [8, 27],
    ['foot_floor_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Assign values to scene property
    guide_props.guide_feet_floor = p_bones["sole_ctrl_L"].constraints["Floor_Foot_L_NOREP"].offset

def SETTINGS_Eyelids_Floor(operator, context):
    weight_step(operator, context, 'SETTINGS_Eyelids_Floor',
    'x2', ['eyelid_low_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L / 2), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_mstr_L', 'cheek_ctrl_L', 'FRONT',
    ['eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_up_ctrl_2_mstr_L', 'eyelid_up_ctrl_3_mstr_L', 'eyelid_up_ctrl_1_mstr_L', 'eyelid_low_ctrl_2_mstr_L', 'eyelid_low_ctrl_3_mstr_L', 'eyelid_low_ctrl_1_mstr_L'],
    [0, 28],
    ['eyelid_up_ctrl_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    eyelid_1 = p_bones["eyelid_low_ctrl_1_mstr_L"].constraints["Floor_Eyelids_NOREP"].offset
    eyelid_2 = p_bones["eyelid_low_ctrl_2_mstr_L"].constraints["Floor_Eyelids_NOREP"].offset
    eyelid_3 = p_bones["eyelid_low_ctrl_3_mstr_L"].constraints["Floor_Eyelids_NOREP"].offset

    guide_props.guide_eyelid_1_floor = eyelid_1
    guide_props.guide_eyelid_2_floor = eyelid_2
    guide_props.guide_eyelid_3_floor = eyelid_3

def SETTINGS_Blink(operator, context):
    weight_step(operator, context, 'SETTINGS_Blink',
    'x2', ['blink_ctrl_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 0.25),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'blink_ctrl_L', 'blink_ctrl_R', 'FRONT',
    ['blink_ctrl_L'],
    [0],
    ['blink_ctrl_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    blink_L = p_bones["blink_ctrl_L"]["Blink_Rate_L"]

    guide_props.blink_rate = blink_L

def SETTINGS_Eyelids_Follow(operator, context):
    weight_step(operator, context, 'SETTINGS_Eyelids_Follow',
    'x2', ['look',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'eyelid_up_ctrl_L', 'eyelid_up_ctrl_R', 'FRONT',
    ['look'],
    [0],
    ['look'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    up_up = p_bones["eyelid_up_ctrl_L"].EYE_UP_FOLLOW_L
    up_down = p_bones["eyelid_up_ctrl_L"].EYE_DOWN_FOLLOW_L
    low_up = p_bones["eyelid_low_ctrl_L"].EYE_UP_FOLLOW_L
    low_down = p_bones["eyelid_low_ctrl_L"].EYE_DOWN_FOLLOW_L

    guide_props.guide_eyelid_up_up_follow = up_up
    guide_props.guide_eyelid_up_down_follow = up_down
    guide_props.guide_eyelid_low_up_follow = low_up
    guide_props.guide_eyelid_low_down_follow = low_down

def SETTINGS_Fleshy_Eyes(operator, context):
    weight_step(operator, context, 'SETTINGS_Fleshy_Eyes',
    'x2', ['look',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'eyelid_up_ctrl_L', 'eyelid_up_ctrl_R', 'FRONT',
    ['look'],
    [0],
    ['look'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    fleshy_eyes = p_bones["look_L"]["FLESHY_EYE_L"]

    guide_props.fleshy_eyes_rate = fleshy_eyes

def SETTINGS_Eyelids_Cheek_Follow(operator, context):
    weight_step(operator, context, 'SETTINGS_Eyelids_Cheek_Follow',
    'x2', ['cheek_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_mstr_L', 'mouth_corner_L', 'FRONT',
    ['cheek_ctrl_L'],
    [0],
    ['cheek_ctrl_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    cheek_follow = p_bones["eyelid_low_ctrl_L"].AUTO_CHEEK_L

    guide_props.guide_eyelid_auto_cheek = cheek_follow

def SETTINGS_Cheek_Smile_Follow(operator, context):
    weight_step(operator, context, 'SETTINGS_Cheek_Smile_Follow',
    'x2', ['mouth_corner_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L) * 0.25, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L * 0.5), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_mstr_L', 'mouth_corner_L', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    smile_follow = p_bones["cheek_ctrl_L"].AUTO_SMILE_L

    guide_props.guide_cheek_auto_smile = smile_follow

def SETTINGS_Coner_Auto_Back(operator, context):
    weight_step(operator, context, 'SETTINGS_Coner_Auto_Back',
    'x2', ['mouth_ctrl',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L) * 0.5, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_mstr_L', 'mouth_corner_L', 'RIGHT',
    ['mouth_ctrl'],
    [0],
    ['mouth_ctrl'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    auto_back = p_bones["mouth_corner_L"].AUTO_BACK_L

    guide_props.guide_mouth_corner_auto_back = auto_back

def SETTINGS_Lips_Floor(operator, context):
    weight_step(operator, context, 'SETTINGS_Lips_Floor',
    'x2', ['mouth_ctrl',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["lip_low_def_mid"].length), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_mstr_L', 'mouth_corner_L', 'FRONT',
    ['mouth_ctrl'],
    [0, 28],
    ['mouth_ctrl'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    floor_1 = p_bones["lip_up_ctrl_1_mstr_L"].constraints["Floor_Lips"].offset
    floor_2 = p_bones["lip_up_ctrl_2_mstr_L"].constraints["Floor_Lips"].offset
    floor_3 = p_bones["lip_up_ctrl_3_mstr_L"].constraints["Floor_Lips"].offset

    guide_props.guide_lip_1_floor = floor_1
    guide_props.guide_lip_2_floor = floor_2
    guide_props.guide_lip_3_floor = floor_3

def SETTINGS_Lip_Curvature(operator, context):
    weight_step(operator, context, 'SETTINGS_Lip_Curvature',
    'x2', ['mouth_corner_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L) * 0.75, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L * 0.75), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'mouth_corner_L', 'mouth_corner_R', 'FRONT',
    ['mouth_corner_L', 'lip_low_def_3_L', 'lip_low_def_2_L', 'lip_low_rim_def_3_L', 'lip_low_line_def_3_L', 'lip_low_def_1_L', 'lip_low_rim_def_2_L', 'lip_low_line_def_2_L',
    'lip_low_def_mid', 'lip_low_rim_def_1_L', 'lip_low_line_def_1_L', 'lip_low_def_4_L', 'lip_low_rim_def_4_L', 'lip_up_rim_def_4_L', 'lip_low_line_def_4_L', 'lip_up_line_def_4_L',
    'lip_up_def_mid', 'lip_up_rim_def_1_L', 'lip_up_line_def_1_L', 'lip_up_def_1_L', 'lip_up_rim_def_2_L', 'lip_up_line_def_2_L', 'lip_up_def_2_L', 'lip_up_rim_def_3_L', 'lip_up_line_def_3_L', 'lip_up_def_3_L'],
    [0, 27],
    ['mouth_corner_L'])

    guide_props = bpy.context.scene.blenrig_guide
    p_bones =  guide_props.arm_obj.pose.bones

    #Collect values, then Assign values to scene property
    rigidity_1 = p_bones["lip_up_ctrl_1_str_L"].constraints["Limit Distance_NOREP"].influence
    rigidity_2 = p_bones["lip_up_ctrl_2_str_L"].constraints["Limit Distance_NOREP"].influence
    rigidity_3 = p_bones["lip_up_ctrl_3_str_L"].constraints["Limit Distance_NOREP"].influence
    curvature = p_bones["lip_up_line_L"].bone.bbone_easeout
    curvature_override_1_x = p_bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"]
    curvature_override_1_y = p_bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"]
    curvature_override_1_z = p_bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"]
    curvature_override_2_x = p_bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"]
    curvature_override_2_y = p_bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"]
    curvature_override_2_z = p_bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"]
    curvature_override_3_x = p_bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"]
    curvature_override_3_y = p_bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"]
    curvature_override_3_z = p_bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"]

    guide_props.guide_lips_motion_curvature = curvature
    guide_props.guide_lip_1_rigidity = rigidity_1
    guide_props.guide_lip_2_rigidity = rigidity_2
    guide_props.guide_lip_3_rigidity = rigidity_3
    guide_props.guide_lip_1_curvature_override[0] = curvature_override_1_x
    guide_props.guide_lip_1_curvature_override[1] = curvature_override_1_y
    guide_props.guide_lip_1_curvature_override[2] = curvature_override_1_z
    guide_props.guide_lip_2_curvature_override[0] = curvature_override_2_x
    guide_props.guide_lip_2_curvature_override[1] = curvature_override_2_y
    guide_props.guide_lip_2_curvature_override[2] = curvature_override_2_z
    guide_props.guide_lip_3_curvature_override[0] = curvature_override_3_x
    guide_props.guide_lip_3_curvature_override[1] = curvature_override_3_y
    guide_props.guide_lip_3_curvature_override[2] = curvature_override_3_z

def SETTINGS_Finish(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'SETTINGS_Finish'

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

#### END OF STEP ACTIONS ####

def rig_settings_end_generic(context):
    guide_props = context.scene.blenrig_guide
    p_bones = guide_props.arm_obj.pose.bones

    #Select Armature
    if context.active_object.type == 'MESH':
        deselect_all_objects(context)
        select_armature(context)

    show_armature(context)

    #Ensure POSE Mode
    go_blenrig_pose_mode(context)

    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Reset Transforms
    reset_all_bones_transforms()

    #Turn Layers off
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Lock Object Mode Off
    bpy.context.scene.tool_settings.lock_object_mode = False

#Property for action to be performed after steps
def end_of_step_action(context):
    rig_settings_end_generic(context)
    guide_props = context.scene.blenrig_guide
    p_bones = guide_props.arm_obj.pose.bones
    current_step = guide_props.guide_current_step
    if current_step == 'SETTINGS_Shoulder_Movement':
        p_bones["properties_arm_L"].ik_arm_L =  0.0
        p_bones["properties_arm_L"].toggle_arm_ik_pole_L =  1
    if current_step == 'SETTINGS_Volume_Variation':
        p_bones["properties_arm_L"].toon_arm_L =  0.0
        p_bones["properties_leg_L"].toon_leg_L =  0.0
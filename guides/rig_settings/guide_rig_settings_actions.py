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

def show_armature(context):
    #Armature for setting view
    armature = get_armature_object(context)
    armature.hide_viewport = False

    #Select Armature
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

#### RIG SETTTINGS STEPS ####

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
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].toggle_arm_ik_pole_L =  0
    bpy.ops.snap.arm_fk_to_ik_l()

    #Select Hand IK
    deselect_all_pose_bones(context)
    select_pose_bone(context, 'hand_ik_ctrl_L')

def SETTINGS_Torso_Rotation(operator, context):
    weight_step(operator, context, 'SETTINGS_Torso_Rotation',
    'x2', ['torso_fk_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, -45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['torso_fk_ctrl', 'spine_1_def', 'spine_2_def', 'spine_3_def'],
    [7, 27],
    ['torso_fk_ctrl'])

def SETTINGS_Neck_Rotation(operator, context):
    weight_step(operator, context, 'SETTINGS_Neck_Rotation',
    'x2', ['neck_fk_ctrl',
    (0.0, 0.0, 0.0), (45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
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
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['torso_fk_ctrl_inv', 'spine_1_def', 'spine_2_def', 'pelvis_def'],
    [18, 27],
    ['torso_fk_ctrl_inv'])

def SETTINGS_Torso_Stretching(operator, context):
    weight_step(operator, context, 'SETTINGS_Torso_Stretching',
    'x2', ['pelvis_ctrl',
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones['pelvis_def'].length, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['pelvis_ctrl', 'spine_1_def', 'spine_2_def', 'spine_3_def', 'pelvis_def'],
    [7, 27],
    ['pelvis_ctrl'])

def SETTINGS_Pelvis_Compensation(operator, context):
    weight_step(operator, context, 'SETTINGS_Pelvis_Compensation',
    'x2', ['pelvis_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 33), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'head_stretch', 'FRONT',
    ['pelvis_ctrl', 'spine_1_def', 'spine_2_def', 'spine_3_def', 'pelvis_def'],
    [7, 27],
    ['pelvis_ctrl'])

def SETTINGS_Foot_Roll(operator, context):
    weight_step(operator, context, 'SETTINGS_Foot_Roll',
    'x2', ['foot_roll_ctrl_L',
    (0.0, 0.0, 0.0), (45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'foot_roll_ctrl_L', 'toe_roll_2_L', 'RIGHT',
    ['foot_roll_ctrl_L', 'foot_def_L', 'foot_toe_1_def_L', 'foot_toe_2_def_L'],
    [9, 27],
    ['foot_roll_ctrl_L'])

def SETTINGS_Volume_Variation(operator, context):
    weight_step(operator, context, 'SETTINGS_Volume_Variation',
    'x2', ['torso_fk_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
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
    #Enable Stretchy IK
    guide_props.arm_obj.pose.bones["properties_arm_L"].toon_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_L"].toon_leg_L =  1.0

def SETTINGS_Feet_Floor(operator, context):
    weight_step(operator, context, 'SETTINGS_Feet_Floor',
    'x2', ['foot_floor_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -0.0), (1.0, 1.0, 1.0),
    1],
    'shin_fk_L', 'foot_floor_L', 'RIGHT',
    ['foot_floor_L'],
    [8, 27],
    ['foot_floor_L'])

#### END OF STEP ACTIONS ####

def rig_settings_end_generic(context):
    guide_props = context.scene.blenrig_guide
    p_bones = guide_props.arm_obj.pose.bones

    #Select Armature
    if context.active_object.type == 'MESH':
        deselect_all_objects(context)
        select_armature(context)

    #Ensure POSE Mode
    go_blenrig_pose_mode(context)

    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Reset Transforms
    reset_all_bones_transforms()

    #Turn Layers off
    off_layers = [27]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Mirror Parameters
    try:
        p_bones['shoulder_R']["SHLDR_AUTO_FORW_R"] = p_bones['shoulder_L']["SHLDR_AUTO_FORW_L"]
        p_bones['shoulder_R']["SHLDR_AUTO_BACK_R"] = p_bones['shoulder_L']["SHLDR_AUTO_BACK_L"]
        p_bones['shoulder_R']["SHLDR_AUTO_UP_R"] = p_bones['shoulder_L']["SHLDR_AUTO_UP_L"]
        p_bones['shoulder_R']["SHLDR_AUTO_DOWN_R"] = p_bones['shoulder_L']["SHLDR_AUTO_DOWN_L"]
    except:
        pass
    try:
        p_bones['foot_roll_ctrl_R']["FOOT_ROLL_AMPLITUD_R"] = p_bones['foot_roll_ctrl_L']["FOOT_ROLL_AMPLITUD_L"]
        p_bones['foot_roll_ctrl_R']["TOE_1_ROLL_START_R"] = p_bones['foot_roll_ctrl_L']["TOE_1_ROLL_START_L"]
        p_bones['foot_roll_ctrl_R']["TOE_2_ROLL_START_R"] = p_bones['foot_roll_ctrl_L']["TOE_2_ROLL_START_L"]
    except:
        pass
    try:
        p_bones['properties_arm_R']["volume_variation_arm_R"] = p_bones['properties_arm_L']["volume_variation_arm_L"]
        p_bones['properties_arm_R']["volume_variation_fingers_R"] = p_bones['properties_arm_L']["volume_variation_fingers_L"]
        p_bones['properties_leg_R']["volume_variation_leg_R"] = p_bones['properties_leg_L']["volume_variation_leg_L"]
        p_bones['properties_leg_R']["volume_variation_toes_R"] = p_bones['properties_leg_L']["volume_variation_toes_L"]
    except:
        pass
    try:
        p_bones["sole_ctrl_R"].constraints["Floor_Foot_R_NOREP"].offset = p_bones["sole_ctrl_L"].constraints["Floor_Foot_L_NOREP"].offset
    except:
        pass


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
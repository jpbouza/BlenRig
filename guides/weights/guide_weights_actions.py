import bpy
from .. utils import *

def frame_bones(context, *bone_names):
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bone_names)
    frame_selected()
    deselect_all_pose_bones(context)

def select_armature(context):
    # Select previously active Armature
    if context.mode != 'OBJECT':
        set_mode('OBJECT')
    set_active_object(context, bpy.context.scene.blenrig_guide.arm_obj)
    set_mode('POSE')

def show_armature(context):
    #Armature for setting view
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

def show_mdef_cage(context):
    deselect_all_objects(context)
    # Show Mdef
    mdef_cage_objects = collect_cage()
    collect_cage()
    blenrig_temp_link(mdef_cage_objects)

    for ob in mdef_cage_objects:
        set_active_object(context, ob)
        bpy.context.scene.blenrig_guide.mdef_cage_obj = ob
        bpy.context.scene.blenrig_guide.mdef_cage_obj.hide_viewport = False

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

def weight_step(operator, context, step_name, wp_obj,
joint_type, joint_parameters,
frame_bone_1, frame_bone_2, view,
bone_list, layers_list, active_bone_list, wp_active_group_list, mode):

    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    #Perform end of step action and set current step name
    end_of_step_action(context)
    guide_props.guide_current_step = step_name

    #Weight Painting Object
    #Cage
    if wp_obj == 'mdef_cage':
        show_mdef_cage(context)
        paint_obj = guide_props.mdef_cage_obj
        set_active_object(context, paint_obj)
    #Hands
    elif wp_obj == 'hands':
        paint_obj = guide_props.character_hands_obj
        set_active_object(context, paint_obj)
    #Toes
    elif wp_obj == 'toes':
        paint_obj = guide_props.character_toes_obj
        set_active_object(context, paint_obj)
    #Head
    elif wp_obj == 'head':
        paint_obj = guide_props.character_head_obj
        set_active_object(context, paint_obj)

    #Create Joint List and Vgroup List for Scrolling through joints within the step
    joint_list = active_bone_list
    vgroup_list = wp_active_group_list

    #Clear List
    bpy.context.scene.blenrig_joint_chain_list.clear()

    #Add bones to list
    for i in range(len(joint_list)):
        joint_item = joint_list[i]
        vgroup_item = vgroup_list[i]
        add_item = bpy.context.scene.blenrig_joint_chain_list.add()
        add_item.joint = joint_item
        bpy.context.scene.blenrig_joint_chain_list[i].vgroup = vgroup_item

    #Active VGroup
    set_active_vgroup(vgroup_list[0])

    #Set Bone and Angles
    guide_props.guide_transform_steps = joint_type
    param_list = joint_parameters
    joint_rotations(*param_list)

    deselect_all_objects(context)

    #Show Armature
    show_armature(context)

    # Adjust view to Bones.
    frame_bones(context, frame_bone_1, frame_bone_2)
    # Front View.
    set_view_perspective(context, False)
    set_viewpoint(view)

    #Turn On Deformation Layer
    on_layers = layers_list
    for l in on_layers:
        bpy.context.object.data.layers[l] = True

    #Clear Bone List
    scn.blenrig_wp_bones.clear()

    #Add bones to list
    for b in bone_list:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    bones = [b.bone for b in scn.blenrig_wp_bones]

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # #Unhide Bones in Deformation Layer
    # hide_bones_in_layer(context, *on_layers, state=False)
    # deselect_all_pose_bones(context, invert=False)

    #Set Active Bone
    select_pose_bone(context, joint_list[0])

    if wp_obj == 'mdef_cage':
        if mode == 'weight_paint':
            #Set Weight Paint Mode
            set_active_object(context, paint_obj)
            if context.mode != 'WEIGHT_PAINT':
                bpy.ops.blenrig.toggle_weight_painting(paint_object='mdef_cage')

        if mode == 'mdef_mesh':
            #Set Weight Paint Mode
            set_active_object(context, paint_obj)
            if context.mode != 'WEIGHT_PAINT':
                set_mode('WEIGHT_PAINT')
                bpy.ops.blenrig.toggle_weight_painting(paint_object='mdef_cage')

    else:
        if mode == 'weight_paint':
            #Set Weight Paint Mode
            set_active_object(context, paint_obj)
            if context.mode != 'WEIGHT_PAINT':
                bpy.ops.blenrig.toggle_weight_painting(paint_object='char')

        if mode == 'char_mesh':
            #Set Weight Paint Mode
            set_active_object(context, paint_obj)
            if context.mode != 'WEIGHT_PAINT':
                set_mode('WEIGHT_PAINT')
                bpy.ops.blenrig.toggle_weight_painting(paint_object='char')

#### WEIGHTS STEPS ####

def WEIGHTS_Cage_Ankle(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Ankle', 'mdef_cage',
    'x6', ['foot_fk_L',
    (0.0, 0.0, 0.0), (60, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-60, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 60, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -60, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 60), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -60), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'sole_pivot_point_L', 'RIGHT',
    ['foot_fk_L', 'foot_def_L', 'shin_twist_def_L', 'instep_fix_L', 'ankle_fix_L'],
    [27],
    ['foot_fk_L'],
    ['foot_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0


def WEIGHTS_Cage_Foot_Toe(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Foot_Toe', 'mdef_cage',
    'x4', ['foot_toe_1_fk_L',
    (0.0, 0.0, 0.0), (60, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-60, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 00, -45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'sole_pivot_point_L', 'RIGHT',
    ['foot_toe_fix_up_1_L', 'foot_toe_1_fk_L', 'foot_toe_2_fk_L', 'foot_toe_fix_up_2_L', 'foot_toe_fix_low_2_L', 'foot_toe_fix_low_1_L', 'foot_def_L', 'foot_toe_1_def_L', 'foot_toe_2_def_L'],
    [27],
    ['foot_toe_1_fk_L', 'foot_toe_2_fk_L'],
    ['foot_toe_1_def_L', 'foot_toe_2_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0


def WEIGHTS_Cage_Knee(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Knee', 'mdef_cage',
    'x4', ['shin_fk_L',
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-20, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'thigh_fk_L', 'RIGHT',
    ['thigh_def_L', 'thigh_twist_def_L', 'knee_fix_L', 'shin_fix_L', 'shin_fk_L', 'shin_def_L', 'shin_twist_def_L'],
    [27],
    ['shin_fk_L'],
    ['thigh_twist_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0

def WEIGHTS_Cage_Thigh(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Thigh', 'mdef_cage',
    'x4', ['thigh_fk_L',
    (0.0, 0.0, 0.0), (60, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-80, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 20), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -80), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'thigh_fk_L', 'RIGHT',
    ['pelvis_def', 'pelvis_def_L', 'hip_fix_L', 'thigh_fix_L', 'thigh_def_L', 'buttock_fix_L', 'thigh_fk_L', 'thigh_twist_def_L'],
    [27],
    ['thigh_fk_L'],
    ['thigh_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0


def WEIGHTS_Cage_Torso(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Torso', 'mdef_cage',
    'x6', ['pelvis_ctrl',
    (0.0, 0.0, 0.0), (45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 45, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -45, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -35), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'neck_1_fk', 'FRONT',
    ['spine_1_fk', 'spine_2_fk', 'spine_3_fk', 'spine_3_def', 'spine_1_def', 'spine_2_def', 'pelvis_ctrl', 'pelvis_def', 'pelvis_def_L', 'pelvis_def_R',
    'breast_ctrl_L', 'breast_tip_L', 'breast_def_L', 'breast_ctrl_R', 'breast_tip_R', 'breast_def_R'],
    [27],
    ['pelvis_ctrl', 'spine_2_fk', 'spine_3_fk'],
    ['spine_1_def', 'spine_2_def', 'spine_3_def'],
    'weight_paint',)

    #Turn Organic Spine Off in order to preview the correct influence of each Spine Bone
    bpy.context.scene.blenrig_guide.arm_obj.pose.bones["properties_torso"]["organic_spine"] = 0

def WEIGHTS_Cage_Neck(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Neck', 'mdef_cage',
    'x6', ['neck_1_fk',
    (0.0, 0.0, 0.0), (45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 45, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -45, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -35), (1.0, 1.0, 1.0),
    1],
    'neck_1_fk', 'head_stretch', 'FRONT',
    ['neck_1_fk', 'neck_2_fk', 'neck_3_fk', 'head_def_2', 'head_def_3', 'head_def_1', 'maxi', 'head_fk',
    'neck_1_def', 'neck_2_def', 'neck_3_def', 'spine_3_def', 'clavi_def_R', 'shoulder_R', 'clavi_def_L', 'shoulder_L'],
    [27],
    ['neck_1_fk', 'neck_2_fk', 'neck_3_fk', 'head_fk'],
    ['neck_1_def', 'neck_2_def', 'neck_3_def', 'head_def_1'],
    'weight_paint',)

    #Turn Organic Spine Off in order to preview the correct influence of each Spine Bone
    bpy.context.scene.blenrig_guide.arm_obj.pose.bones["properties_head"]["organic_neck"] = 0

def WEIGHTS_Cage_Clavicle(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Clavicle', 'mdef_cage',
    'x4', ['shoulder_L',
    (0.0, 0.0, 0.0), (35, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-35, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -15), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1 ],
    'spine_2_fk', 'shoulder_L', 'TOP',
    ['neck_1_def', 'spine_3_def', 'clavi_def_L', 'shoulder_L'],
    [27],
    ['shoulder_L'],
    ['clavi_def_L'],
    'weight_paint',)

def WEIGHTS_Cage_Shoulder(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Shoulder', 'mdef_cage',
    'x4', ['arm_fk_L',
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 90), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -20), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'arm_fk_L', 'spine_3_fk', 'FRONT',
    ['spine_3_def', 'clavi_def_L', 'back_fix_L', 'chest_fix_L', 'arm_def_L', 'shoulder_fix_L', 'armpit_fix_L', 'arm_fk_L', 'arm_twist_def_L'],
    [27],
    ['arm_fk_L'],
    ['arm_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0


def WEIGHTS_Cage_Elbow(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Elbow', 'mdef_cage',
    'x4', ['forearm_fk_L',
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-20, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'arm_fk_L', 'hand_fk_L', 'RIGHT',
    ['arm_def_L', 'arm_twist_def_L', 'elbow_fix_L', 'forearm_fix_L', 'forearm_fk_L', 'forearm_twist_def_L', 'forearm_def_L'],
    [27],
    ['forearm_fk_L'],
    ['forearm_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0

def WEIGHTS_Cage_Wrist(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Wrist', 'mdef_cage',
    'x6', ['hand_fk_L',
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -90, 0.0), (1.0, 1.0, 1.0),
    1],
    'forearm_fk_L', 'hand_fk_L', 'FRONT',
    ['hand_fk_L', 'hand_def_L', 'wrist_fix_up_L', 'wrist_fix_low_L', 'forearm_twist_def_L', 'forearm_def_L'],
    [27],
    ['hand_fk_L'],
    ['hand_def_L'],
    'mdef_mesh',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0

def WEIGHTS_Char_Wrist(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Wrist', 'hands',
    'x4', ['hand_fk_L',
    (0.0, 0.0, 0.0), (90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-90, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -35), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -90, 0.0), (1.0, 1.0, 1.0),
    1],
    'forearm_fk_L', 'hand_fk_L', 'FRONT',
    ['hand_fk_L', 'hand_def_L'],
    [27],
    ['hand_fk_L'],
    ['no_mdef'],
    'weight_paint',)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0

def WEIGHTS_Char_Hand_VP(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Hand_VP', 'hands',
    'x2', ['hand_close_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.5, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 2.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'forearm_fk_L', 'hand_fk_L', 'FRONT',
    ['hand_close_L', 'fing_lit_ctrl_L', 'fing_lit_fix_low_3_L', 'fing_lit_fix_up_3_L', 'fing_lit_fix_low_2_L', 'fing_lit_fix_up_2_L', 'fing_ring_ctrl_L', 'fing_ring_fix_low_3_L',
    'fing_ring_fix_up_3_L', 'fing_ring_fix_low_2_L', 'fing_ring_fix_up_2_L', 'fing_ind_ctrl_L', 'fing_ind_fix_low_3_L', 'fing_ind_fix_up_3_L', 'fing_ind_fix_low_2_L', 'fing_ind_fix_up_2_L',
    'fing_mid_ctrl_L', 'fing_mid_fix_low_3_L', 'fing_mid_fix_up_3_L', 'fing_mid_fix_low_2_L', 'fing_mid_fix_up_2_L', 'fing_ind_fix_up_1_L', 'fing_ind_fix_low_1_L', 'fing_ring_fix_up_1_L', 'fing_ring_fix_low_1_L',
    'fing_lit_fix_up_1_L', 'fing_lit_fix_low_1_L', 'fing_mid_fix_up_1_L', 'fing_mid_fix_low_1_L', 'fing_thumb_ctrl_L', 'fing_thumb_fix_low_2_L', 'fing_thumb_fix_up_2_L', 'fing_thumb_fix_up_1_L', 'fing_thumb_fix_low_1_L'
    'fing_lit_4_def_L', 'fing_lit_3_def_L', 'fing_lit_2_def_L', 'fing_ring_4_def_L', 'fing_ring_3_def_L', 'fing_ring_2_def_L', 'fing_ind_4_def_L', 'fing_ind_3_def_L', 'fing_ind_2_def_L', 'fing_mid_4_def_L', 'fing_mid_3_def_L',
    'fing_mid_2_def_L', 'fing_ind_1_def_L', 'fing_ring_1_def_L', 'fing_lit_1_def_L', 'fing_mid_1_def_L', 'fing_thumb_3_def_L', 'fing_thumb_2_def_L', 'fing_thumb_1_def_L'],
    [27],
    ['hand_close_L'],
    ['fing_ind_fix_up_1_L'],
    'char_mesh',)

def WEIGHTS_Char_Fings_1(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Fings_1', 'hands',
    'x6', ['fing_thumb_ctrl_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['fing_thumb_3_L'].length) / 2, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones['fing_thumb_3_L'].length / 2, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['fing_thumb_3_L'].length) / 2, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones['fing_thumb_3_L'].length / 2, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (-75, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (75, 0.0, 0.0), (1.0, 1.0, 1.0),
    0],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_lit_ctrl_L', 'fing_lit_2_def_L', 'fing_ring_ctrl_L', 'fing_ring_2_def_L', 'fing_ind_ctrl_L', 'fing_ind_2_def_L', 'fing_mid_ctrl_L', 'fing_mid_2_def_L',
    'hand_def_L', 'fing_ind_1_def_L', 'fing_ind_fix_up_1_L', 'fing_ind_fix_low_1_L', 'fing_ring_fix_up_1_L', 'fing_ring_fix_low_1_L', 'fing_ring_1_def_L', 'fing_lit_fix_up_1_L',
    'fing_lit_fix_low_1_L', 'fing_lit_1_def_L', 'fing_mid_fix_up_1_L', 'fing_mid_fix_low_1_L', 'fing_mid_1_def_L', 'fing_thumb_ctrl_L', 'fing_thumb_2_def_L', 'fing_thumb_fix_up_1_L', 'fing_thumb_fix_low_1_L', 'fing_thumb_1_def_L'],
    [27],
    ['fing_thumb_ctrl_L', 'fing_ind_ctrl_L', 'fing_mid_ctrl_L', 'fing_ring_ctrl_L', 'fing_lit_ctrl_L'],
    ['fing_thumb_1_def_L', 'fing_ind_1_def_L', 'fing_mid_1_def_L', 'fing_ring_1_def_L', 'fing_lit_1_def_L'],
    'weight_paint',)

def WEIGHTS_Char_Fings_2(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Fings_2', 'hands',
    'x2', ['fing_thumb_3_L',
    (0.0, 0.0, 0.0), (-45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (75, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_lit_ctrl_L', 'fing_lit_3_L', 'fing_lit_4_L', 'fing_lit_4_def_L', 'fing_lit_3_def_L', 'fing_lit_fix_low_3_L', 'fing_lit_fix_up_3_L', 'fing_lit_2_def_L',
    'fing_lit_fix_low_2_L', 'fing_lit_fix_up_2_L', 'fing_ring_ctrl_L', 'fing_ring_3_L', 'fing_ring_4_L', 'fing_ring_4_def_L', 'fing_ring_3_def_L', 'fing_ring_fix_low_3_L',
    'fing_ring_fix_up_3_L', 'fing_ring_2_def_L', 'fing_ring_fix_low_2_L', 'fing_ring_fix_up_2_L', 'fing_ind_ctrl_L', 'fing_ind_3_L', 'fing_ind_4_L', 'fing_ind_4_def_L', 'fing_ind_fix_low_3_L',
    'fing_ind_fix_up_3_L', 'fing_ind_3_def_L', 'fing_ind_fix_low_2_L', 'fing_ind_fix_up_2_L', 'fing_ind_2_def_L', 'fing_mid_ctrl_L', 'fing_mid_3_L', 'fing_mid_4_L', 'fing_mid_4_def_L', 'fing_mid_3_def_L',
    'fing_mid_fix_low_3_L', 'fing_mid_fix_up_3_L', 'fing_mid_2_def_L', 'fing_mid_fix_low_2_L', 'fing_mid_fix_up_2_L', 'fing_thumb_ctrl_L', 'fing_thumb_3_L', 'fing_thumb_3_def_L', 'fing_thumb_2_def_L',
    'fing_thumb_fix_low_2_L', 'fing_thumb_fix_up_2_L'],
    [27],
    ['fing_thumb_3_L', 'fing_ind_3_L', 'fing_ind_4_L', 'fing_mid_3_L', 'fing_mid_4_L', 'fing_ring_3_L', 'fing_ring_4_L', 'fing_lit_3_L', 'fing_lit_4_L'],
    ['fing_thumb_2_def_L', 'fing_ind_2_def_L', 'fing_ind_3_def_L', 'fing_mid_2_def_L', 'fing_mid_3_def_L', 'fing_ring_2_def_L', 'fing_ring_3_def_L', 'fing_lit_2_def_L', 'fing_lit_3_def_L'],
    'weight_paint',)

def WEIGHTS_Char_Head(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Head', 'head',
    'x6', ['head_fk',
    (0.0, 0.0, 0.0), (-45, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (20, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 90, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, -90, 0.0), (1.0, 1.0, 1.0),
    1],
    'neck_1_fk', 'head_stretch', 'RIGHT',
    ['head_fk', 'head_def_1', 'maxi'],
    [27],
    ['head_fk'],
    ['no_mdef'],
    'weight_paint',)

def WEIGHTS_Char_Head_Joints(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Head_Joints', 'head',
    'x4', ['head_mid_ctrl',
    (0.0, 0.0, 0.0), (-33, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (15, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 33), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, -33), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'neck_1_fk', 'head_stretch', 'RIGHT',
    ['head_fk', 'head_def_1', 'head_def_2', 'head_def_3', 'head_mid_ctrl', 'head_top_ctrl'],
    [27],
    ['head_mid_ctrl', 'head_top_ctrl'],
    ['head_def_2', 'head_def_3'],
    'weight_paint',)

def WEIGHTS_Char_Ears(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Ears', 'head',
    'x2', ['ear_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, -45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 45), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'neck_1_fk', 'brow_mstr_L', 'RIGHT',
    ['ear_L', 'ear_up_L', 'ear_low_L', 'head_def_1', 'head_def_2', 'head_def_3'],
    [27],
    ['ear_L', 'ear_up_L', 'ear_low_L'],
    ['ear_L', 'ear_up_L', 'ear_low_L'],
    'weight_paint',)

def WEIGHTS_Char_Eyebrows(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Eyebrows', 'head',
    'x2', ['brow_mstr_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones['forehead_def_3_L'].length * 0.75), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['brow_arch_def_3_L'].length * 0.75)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'head_stretch', 'FRONT',
    ['head_def_2', 'head_def_3', 'brow_mstr_L', 'brow_def_5_L', 'brow_arch_def_5_L', 'brow_ctrl_curve_L', 'brow_ctrl_in_L', 'brow_ctrl_out_L', 'cheek_rim_def_1_L', 'eyelid_rim_up_def_1_L',
    'forehead_def_mid', 'frown_ctrl_mstr', 'frown_def', 'nose_def_1_mid', 'head_def_1', 'eyelid_rim_up_def_4_L', 'eyelid_rim_up_def_3_L', 'eyelid_rim_up_def_2_L', 'brow_low_def_4_L', 'brow_up_def_4_L',
    'brow_arch_def_1_L', 'frown_low_def_L', 'nose_side_def_1_L', 'brow_def_1_L', 'frown_up_def_L', 'brow_arch_def_2_L', 'brow_low_def_1_L', 'brow_def_2_L', 'brow_up_def_1_L', 'brow_arch_def_3_L',
    'brow_low_def_2_L', 'brow_def_3_L', 'brow_up_def_2_L', 'brow_arch_def_4_L', 'brow_low_def_3_L', 'brow_def_4_L', 'brow_up_def_3_L', 'nose_root_def_1_L', 'forehead_def_3_L', 'forehead_def_2_L',
    'forehead_def_1_L', 'forehead_def_4_L', 'forehead_def_5_L', 'nose_root_def_2_L', 'brow_low_def_5_L', 'brow_up_def_5_L', 'brow_arch_def_6_L'],
    [27],
    ['brow_mstr_L', 'frown_ctrl_mstr'],
    ['frown_def', 'brow_def_3_L'],
    'weight_paint',)

def WEIGHTS_Char_Eyelids(operator, context):
    weight_step(operator, context, 'WEIGHTS_Char_Eyelids', 'head',
    'x2', ['eyelid_up_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones['forehead_def_3_L'].length * 0.75), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['brow_arch_def_3_L'].length * 0.75)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['brow_mstr_L', 'brow_arch_def_5_L', 'eyelid_up_rim_ctrl_L', 'eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_out_def_L', 'cheek_rim_def_1_L', 'eyelid_rim_up_def_1_L', 'eyelid_rim_low_def_1_L',
    'eyelid_in_def_L', 'eyelid_up_ctrl_2_L', 'eyelid_up_line_def_3_L', 'eyelid_ctrl_in_L', 'eyelid_low_line_def_1_L', 'eyelid_up_line_def_1_L', 'eyelid_ctrl_out_L', 'eyelid_up_line_def_4_L',
    'eyelid_low_line_def_4_L', 'eyelid_up_ctrl_3_L', 'eyelid_up_ctrl_1_L', 'eyelid_up_line_def_2_L', 'eyelid_low_ctrl_2_L', 'eyelid_low_line_def_3_L', 'eyelid_low_ctrl_3_L', 'eyelid_low_ctrl_1_L',
    'eyelid_low_line_def_2_L', 'eyelid_low_rim_ctrl_L', 'nose_def_1_mid', 'cheek_def_1_1_L', 'eyelid_low_def_1_L', 'eyelid_rim_low_def_2_L', 'cheek_def_3_1_L', 'eyelid_low_def_3_L', 'eyelid_rim_low_def_4_L',
    'eyelid_low_def_2_L', 'eyelid_rim_low_def_3_L', 'cheek_def_2_1_L', 'eyelid_rim_up_def_4_L', 'eyelid_up_def_3_L', 'eyelid_rim_up_def_3_L', 'eyelid_up_def_2_L', 'eyelid_rim_up_def_2_L', 'eyelid_up_def_1_L',
    'brow_low_def_4_L', 'brow_arch_def_1_L', 'frown_low_def_L', 'nose_side_def_1_L', 'brow_arch_def_2_L', 'brow_low_def_1_L', 'brow_arch_def_3_L', 'brow_low_def_2_L', 'brow_arch_def_4_L', 'brow_low_def_3_L',
    'nose_frown_up_def_L', 'nose_root_def_2_L', 'cheekbone_line_def_3_L', 'cheekbone_line_def_2_L', 'cheekbone_line_def_1_L', 'brow_low_def_5_L', 'cheek_rim_def_2_L', 'brow_arch_def_6_L', 'nose_root_def_1_L'],
    [27],
    ['eyelid_up_ctrl_L', 'eyelid_low_ctrl_L'],
    ['eyelid_up_line_def_3_L', 'eyelid_low_line_def_3_L'],
    'weight_paint',)




#### END OF STEP ACTIONS ####

def weights_end_generic(context):

    guide_props = bpy.context.scene.blenrig_guide

    #Select Armature
    if bpy.context.active_object.type == 'MESH':
        deselect_all_objects(context)
        select_armature(context)

    #Ensure POSE Mode
    set_active_object(context, guide_props.arm_obj)
    set_mode('POSE')

    #Ensure Properties Symmetry
    bpy.ops.blenrig.mirror_vp_rj_values()
    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Reset Transforms
    reset_all_bones_transforms()

    #Turn Layers on
    off_layers = [27]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Turn Off Wire in Weight Paint Object
    if guide_props.active_wp_obj != None:
        guide_props.active_wp_obj.show_wire = False

    #Unlink Temp Collection
    blenrig_temp_unlink()

#Property for action to be performed after steps
def end_of_step_action(context):
    weights_end_generic(context)
    guide_props = bpy.context.scene.blenrig_guide
    current_step = bpy.context.scene.blenrig_guide.guide_current_step
    Leg_Steps = ['WEIGHTS_Cage_Shoulder', 'WEIGHTS_Cage_Foot_Toe', 'WEIGHTS_Cage_Knee', 'WEIGHTS_Cage_Thigh']
    #Leg IK Switch
    for step in Leg_Steps:
        if current_step == step:
            #Set Rig Control Properties
            guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  0.0
            guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  0.0
            guide_props.guide_current_step = ''
    if current_step == 'WEIGHTS_Cage_Torso':
        #Turn Organic Spine Back On
        guide_props.arm_obj.pose.bones["properties_torso"]["organic_spine"] = 1
    if current_step == 'WEIGHTS_Cage_Neck':
        #Turn Organic Spine Back On
        guide_props.arm_obj.pose.bones["properties_head"]["organic_neck"] = 1
    Arm_Steps = ['WEIGHTS_Cage_Ankle', 'WEIGHTS_Cage_Elbow', 'WEIGHTS_Cage_Wrist', 'WEIGHTS_Char_Wrist']
    #Arm IK Switch
    for step in Arm_Steps:
        if current_step == step:
            #Set Rig Control Properties
            guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  0.0
            guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  0.0
            guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  0.0
            guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  0.0
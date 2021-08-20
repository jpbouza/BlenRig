import bpy
from .. utils import *
from math import radians

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

def shapekey_step(operator, context, step_name, shp_obj,
joint_type, joint_parameters,
frame_bone_1, frame_bone_2, view,
bone_list, layers_list, active_bone_list, wp_active_group_list, mode, shapekeys_list_1, shapekeys_list_2, shapekeys_list_3, shapekeys_list_4, list_index, shapekey, x_mirror):

    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    #Perform end of step action and set current step name
    end_of_step_action(context)
    guide_props.guide_current_step = step_name

    #Shapekeys Object
    #Cage
    if shp_obj == 'mdef_cage':
        show_mdef_cage(context)
        mesh_edit_obj = guide_props.mdef_cage_obj
        set_active_object(context, mesh_edit_obj)
        guide_props.active_shp_obj = mesh_edit_obj
        guide_props.active_wp_obj = mesh_edit_obj
    #Hands
    elif shp_obj == 'hands':
        mesh_edit_obj = guide_props.character_hands_obj
        set_active_object(context, mesh_edit_obj)
        guide_props.active_shp_obj = mesh_edit_obj
        guide_props.active_wp_obj = mesh_edit_obj
    #Toes
    elif shp_obj == 'toes':
        mesh_edit_obj = guide_props.character_toes_obj
        set_active_object(context, mesh_edit_obj)
        guide_props.active_shp_obj = mesh_edit_obj
        guide_props.active_wp_obj = mesh_edit_obj
    #Head
    elif shp_obj == 'head':
        mesh_edit_obj = guide_props.character_head_obj
        set_active_object(context, mesh_edit_obj)
        guide_props.active_shp_obj = mesh_edit_obj
        guide_props.active_wp_obj = mesh_edit_obj

    bpy.context.active_object.data.use_mirror_x = x_mirror

    #Set Active Shapekey Property
    guide_props.active_shapekey_name = shapekey

    #Create Shapekeys List for Scrolling through joints within the step
    shapes_list_1 = shapekeys_list_1
    shapes_list_2 = shapekeys_list_2
    shapes_list_3 = shapekeys_list_3
    shapes_list_4 = shapekeys_list_4

    #Clear List
    bpy.context.scene.blenrig_shapekeys_list.clear()

    #Add bones to list
    for i in range(len(shapes_list_1)):
        shapekey_item_1 = shapes_list_1[i]
        shapekey_item_2 = shapes_list_2[i]
        shapekey_item_3 = shapes_list_3[i]
        shapekey_item_4 = shapes_list_4[i]
        add_item = bpy.context.scene.blenrig_shapekeys_list.add()
        add_item.list_1 = shapekey_item_1
        bpy.context.scene.blenrig_shapekeys_list[i].list_2 = shapekey_item_2
        bpy.context.scene.blenrig_shapekeys_list[i].list_3 = shapekey_item_3
        bpy.context.scene.blenrig_shapekeys_list[i].list_4 = shapekey_item_4

    #Set Current Shapekeys List Number
    guide_props.shapekeys_list_index = list_index

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

    if shp_obj == 'mdef_cage':
        if mode == 'shpaekey_edit':
            #Set Edit Mode
            set_active_object(context, mesh_edit_obj)
            if context.mode != 'EDIT':
                bpy.ops.blenrig.toggle_shapekey_editting(mesh_edit_object='mdef_cage')

        if mode == 'mdef_mesh':
            #Set Edit Mode
            set_active_object(context, mesh_edit_obj)
            if context.mode != 'EDIT':
                set_mode('EDIT')
                bpy.ops.blenrig.toggle_shapekey_editting(mesh_edit_object='mdef_cage')

    else:
        if mode == 'shpaekey_edit':
            #Set Edit Mode
            set_active_object(context, mesh_edit_obj)
            if context.mode != 'EDIT':
                bpy.ops.blenrig.toggle_shapekey_editting(mesh_edit_object='char')

        if mode == 'char_mesh':
            #Set Edit Mode
            set_active_object(context, mesh_edit_obj)
            if context.mode != 'EDIT':
                set_mode('EDIT')
                bpy.ops.blenrig.toggle_shapekey_editting(mesh_edit_object='char')
        if mode == 'weight_paint':
            #Set Weight Paint Mode
            set_active_object(context, mesh_edit_obj)
            if context.mode != 'WEIGHT_PAINT':
                bpy.ops.blenrig.toggle_weight_painting(paint_object='char')

#### SHAPEKEYS STEPS ####

def SHAPEKEYS_Intro(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'SHAPEKEYS_Intro'

    deselect_all_objects(context)

    #Show Armature
    show_armature(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

def SHAPEKEYS_Cage_Add_Body_Shapes(operator, context):

    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    #Perform end of step action and set current step name
    end_of_step_action(context)
    guide_props.guide_current_step = 'SHAPEKEYS_Cage_Add_Body_Shapes'

    #Show Armature
    show_armature(context)

    # Adjust view to Bones.
    frame_bones(context, 'master', 'head_stretch')
    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    deselect_all_objects(context)

    #Cage
    show_mdef_cage(context)
    mesh_edit_obj = guide_props.mdef_cage_obj
    set_active_object(context, mesh_edit_obj)

def SHAPEKEYS_Cage_Ankle(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Ankle', 'mdef_cage',
    'x6', ['foot_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('foot_down_L', 60) , 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('foot_up_L', -60), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('foot_in_L', 60)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('foot_out_L', -60)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('shin_twist_in_L', 60), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('shin_twist_out_L', -60), 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'sole_pivot_point_L', 'RIGHT',
    ['foot_fk_L'],
    [22],
    ['foot_fk_L'],
    ['foot_def_L'],
    'shpaekey_edit',
    ['foot_down_L', 'foot_up_L', 'foot_in_L', 'foot_out_L', 'shin_twist_in_L', 'shin_twist_out_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'foot_down_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0


def SHAPEKEYS_Cage_Foot_Toe(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Foot_Toe', 'mdef_cage',
    'x4', ['foot_toe_1_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('foot_toe_1_down_L', 60), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('foot_toe_1_up_L', -60), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('foot_toe_1_in_L', 45)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 00, get_driver_transform_rot('foot_toe_1_out_L', -45)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'sole_pivot_point_L', 'RIGHT',
    ['foot_toe_1_fk_L', 'foot_toe_2_fk_L'],
    [22],
    ['foot_toe_1_fk_L', 'foot_toe_2_fk_L'],
    ['foot_toe_1_def_L', 'foot_toe_2_def_L'],
    'shpaekey_edit',
    ['foot_toe_1_down_L', 'foot_toe_1_up_L', 'foot_toe_1_in_L', 'foot_toe_1_out_L'],
    ['foot_toe_2_down_L', 'foot_toe_2_up_L', 'foot_toe_2_in_L', 'foot_toe_2_out_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'foot_toe_1_up_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0


def SHAPEKEYS_Cage_Knee(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Knee', 'mdef_cage',
    'x4', ['shin_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('shin_up_L', 90), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('shin_down_L', -20), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('thigh_twist_in_L', 90), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('thigh_twist_out_L', -90), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'thigh_fk_L', 'RIGHT',
    ['thigh_def_L', 'thigh_twist_def_L', 'knee_fix_L', 'shin_fix_L', 'shin_fk_L', 'shin_def_L', 'shin_twist_def_L'],
    [22],
    ['shin_fk_L'],
    ['thigh_twist_def_L'],
    'shpaekey_edit',
    ['shin_up_L', 'shin_down_L', 'thigh_twist_in_L', 'thigh_twist_out_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'shin_up_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0

def SHAPEKEYS_Cage_Thigh(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Thigh', 'mdef_cage',
    'x4', ['thigh_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('thigh_back_L', 60), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('thigh_forw_L', -80), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('thigh_in_L', 30)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('thigh_out_L', -80)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'foot_fk_L', 'thigh_fk_L', 'RIGHT',
    ['pelvis_def', 'pelvis_def_L', 'hip_fix_L', 'thigh_fix_L', 'thigh_def_L', 'buttock_fix_L', 'thigh_fk_L', 'thigh_twist_def_L'],
    [22],
    ['thigh_fk_L'],
    ['thigh_def_L'],
    'shpaekey_edit',
    ['thigh_back_L', 'thigh_forw_L', 'thigh_in_L', 'thigh_out_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'thigh_back_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_leg_L"].ik_leg_L =  1.0
    guide_props.arm_obj.pose.bones["properties_leg_R"].ik_leg_R =  1.0


def SHAPEKEYS_Cage_Torso(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Torso', 'mdef_cage',
    'x4', ['spine_1_fk',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('spine_1_forw', 45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('spine_1_back', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('spine_1_twist_L', -45), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0,get_driver_transform_rot('spine_1_L', -35)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'neck_1_fk', 'RIGHT',
    ['spine_1_fk', 'spine_2_fk', 'spine_3_fk', 'spine_3_def', 'spine_1_def', 'spine_2_def', 'pelvis_ctrl', 'pelvis_def', 'pelvis_def_L', 'pelvis_def_R',
    'breast_ctrl_L', 'breast_tip_L', 'breast_def_L', 'breast_ctrl_R', 'breast_tip_R', 'breast_def_R'],
    [7],
    ['spine_1_fk', 'spine_2_fk', 'spine_3_fk'],
    ['spine_1_def', 'spine_2_def', 'spine_3_def'],
    'shpaekey_edit',
    ['spine_1_forw', 'spine_1_back', 'spine_1_twist_L', 'spine_1_L'],
    ['spine_2_forw', 'spine_2_back', 'spine_2_twist_L', 'spine_2_L'],
    ['spine_3_forw', 'spine_3_back', 'spine_3_twist_L', 'spine_3_L'],
    ['', '', '', '', '', ''], 1,
    'spine_1_forw',
    False)
    #Turn Organic Spine Off in order to preview the correct influence of each Spine Bone
    bpy.context.scene.blenrig_guide.arm_obj.pose.bones["properties_torso"]["organic_spine"] = 0

def SHAPEKEYS_Cage_Breathing(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Breathing', 'mdef_cage',
    'x2', ['torso_fk_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 2.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'pelvis_ctrl', 'neck_1_fk', 'RIGHT',
    ['torso_fk_ctrl'],
    [7],
    ['torso_fk_ctrl'],
    ['torso_fk_ctrl'],
    'shpaekey_edit',
    ['breathing', '', '', ''],
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'breathing',
    True)

def SHAPEKEYS_Cage_Neck(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Neck', 'mdef_cage',
    'x4', ['neck_1_fk',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('neck_1_forw', 45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('neck_1_back', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('neck_1_twist_L', -45), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0,get_driver_transform_rot('neck_1_L', -35)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'neck_1_fk', 'head_stretch', 'RIGHT',
    ['neck_1_fk', 'neck_2_fk', 'neck_3_fk', 'head_def_2', 'head_def_3', 'head_def_1', 'maxi', 'head_fk',
    'neck_1_def', 'neck_2_def', 'neck_3_def', 'spine_3_def', 'clavi_def_R', 'shoulder_R', 'clavi_def_L', 'shoulder_L'],
    [4],
    ['neck_1_fk', 'neck_2_fk', 'neck_3_fk', 'head_fk'],
    ['neck_1_def', 'neck_2_def', 'neck_3_def', 'head_def_1'],
    'shpaekey_edit',
    ['neck_1_forw', 'neck_1_back', 'neck_1_twist_L', 'neck_1_L'],
    ['neck_2_forw', 'neck_2_back', 'neck_2_twist_L', 'neck_2_L'],
    ['neck_3_forw', 'neck_3_back', 'neck_3_twist_L', 'neck_3_L'],
    ['head_forw', 'head_back', 'head_twist_L', 'head_L'], 1,
    'neck_1_forw',
    False)

    #Turn Organic Spine Off in order to preview the correct influence of each Spine Bone
    bpy.context.scene.blenrig_guide.arm_obj.pose.bones["properties_head"]["organic_neck"] = 0

def SHAPEKEYS_Cage_Clavicle(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Clavicle', 'mdef_cage',
    'x4', ['shoulder_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('shoulder_forw_L', 35), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('shoulder_back_L', -35), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('shoulder_up_L', 35)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('shoulder_down_L', -15)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1 ],
    'spine_2_fk', 'shoulder_L', 'TOP',
    ['neck_1_def', 'spine_3_def', 'clavi_def_L', 'shoulder_L'],
    [5],
    ['shoulder_L'],
    ['clavi_def_L'],
    'shpaekey_edit',
    ['shoulder_forw_L', 'shoulder_back_L', 'shoulder_up_L', 'shoulder_down_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'shoulder_forw_L',
    False)

def SHAPEKEYS_Cage_Shoulder(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Shoulder', 'mdef_cage',
    'x4', ['arm_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('arm_forw_L', 90), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('arm_back_L', -90), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('arm_up_L', 90)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('arm_down_L', -20)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'arm_fk_L', 'spine_3_fk', 'FRONT',
    ['spine_3_def', 'clavi_def_L', 'back_fix_L', 'chest_fix_L', 'arm_def_L', 'shoulder_fix_L', 'armpit_fix_L', 'arm_fk_L', 'arm_twist_def_L'],
    [5],
    ['arm_fk_L'],
    ['arm_def_L'],
    'shpaekey_edit',
    ['arm_forw_L', 'arm_back_L', 'arm_up_L', 'arm_down_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'arm_forw_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0


def SHAPEKEYS_Cage_Elbow(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Elbow', 'mdef_cage',
    'x4', ['forearm_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('forearm_up_L', 90), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('forearm_down_L', -20), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('arm_twist_in_L', 90), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('arm_twist_out_L', -90), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'arm_fk_L', 'hand_fk_L', 'RIGHT',
    ['arm_def_L', 'arm_twist_def_L', 'elbow_fix_L', 'forearm_fix_L', 'forearm_fk_L', 'forearm_twist_def_L', 'forearm_def_L'],
    [5],
    ['forearm_fk_L'],
    ['forearm_def_L'],
    'shpaekey_edit',
    ['forearm_up_L', 'forearm_down_L', 'arm_twist_in_L', 'arm_twist_out_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'forearm_up_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0

def SHAPEKEYS_Cage_Wrist(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Cage_Wrist', 'mdef_cage',
    'x6', ['hand_fk_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('hand_down_L', 90), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('hand_up_L', -90), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('hand_forw_L', 35)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('hand_back_L', -35)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('forearm_twist_in_L', 90), 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, get_driver_transform_rot('forearm_twist_out_L', -90), 0.0), (1.0, 1.0, 1.0),
    1],
    'forearm_fk_L', 'hand_fk_L', 'FRONT',
    ['hand_fk_L', 'hand_def_L', 'wrist_fix_up_L', 'wrist_fix_low_L', 'forearm_twist_def_L', 'forearm_def_L'],
    [5],
    ['hand_fk_L'],
    ['hand_def_L'],
    'shpaekey_edit',
    ['hand_down_L', 'hand_up_L', 'hand_forw_L', 'hand_back_L', 'forearm_twist_in_L', 'forearm_twist_out_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'hand_down_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Rig Control Properties
    guide_props.arm_obj.pose.bones["properties_arm_L"].ik_arm_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].ik_arm_R =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_L"].space_hand_L =  1.0
    guide_props.arm_obj.pose.bones["properties_arm_R"].space_hand_R =  1.0

def SHAPEKEYS_Char_Add_Fingers_Shapes(operator, context):

    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    #Perform end of step action and set current step name
    end_of_step_action(context)
    guide_props.guide_current_step = 'SHAPEKEYS_Char_Add_Fingers_Shapes'

    #Show Armature
    show_armature(context)

    # Adjust view to Bones.
    frame_bones(context, 'master', 'head_stretch')
    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    deselect_all_objects(context)

    #Cage
    set_active_object(context, guide_props.character_hands_obj)

def SHAPEKEYS_Char_Thumb_1(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Thumb_1', 'hands',
    'x4', ['fing_thumb_1_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('fing_thumb_1_out_L', 45)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, get_driver_transform_rot('fing_thumb_1_in_L', -45)), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_thumb_1_up_L', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_thumb_1_down_L', 45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_thumb_1_L'],
    [17],
    ['fing_thumb_1_L'],
    ['fing_thumb_1_def_L'],
    'shpaekey_edit',
    ['fing_thumb_1_out_L', 'fing_thumb_1_in_L', 'fing_thumb_1_up_L', 'fing_thumb_1_down_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'fing_thumb_1_out_L',
    False)

def SHAPEKEYS_Char_Lit_1(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Lit_1', 'hands',
    'x2', ['fing_lit_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones['fing_lit_1_def_L'].length / 2), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_lit_ctrl_L'],
    [17],
    ['fing_lit_ctrl_L'],
    ['fing_thumb_1_def_L'],
    'shpaekey_edit',
    ['fing_lit_1_down_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'fing_lit_1_down_L',
    False)

def SHAPEKEYS_Char_Thumb_Joints(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Thumb_Joints', 'hands',
    'x2', ['fing_thumb_2_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_thumb_2_up_L', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_thumb_2_down_L', 75), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_thumb_2_L', 'fing_thumb_3_L'],
    [17],
    ['fing_thumb_2_L', 'fing_thumb_3_L'],
    ['fing_thumb_2_def_L', 'fing_thumb_3_def_L'],
    'shpaekey_edit',
    ['fing_thumb_2_up_L', 'fing_thumb_2_down_L'],
    ['fing_thumb_3_up_L', 'fing_thumb_3_down_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'fing_thumb_2_up_L',
    False)

def SHAPEKEYS_Char_Index_Joints(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Index_Joints', 'hands',
    'x2', ['fing_ind_2_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_ind_2_up_L', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_ind_2_down_L', 75), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_ind_2_L', 'fing_ind_3_L', 'fing_ind_4_L'],
    [17],
    ['fing_ind_2_L', 'fing_ind_3_L', 'fing_ind_4_L'],
    ['fing_ind_2_def_L', 'fing_ind_3_def_L', 'fing_ind_4_def_L'],
    'shpaekey_edit',
    ['fing_ind_2_up_L', 'fing_ind_2_down_L'],
    ['fing_ind_3_up_L', 'fing_ind_3_down_L'],
    ['fing_ind_4_up_L', 'fing_ind_4_down_L'],
    ['', '', '', '', '', ''], 1,
    'fing_ind_2_up_L',
    False)

def SHAPEKEYS_Char_Middle_Joints(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Middle_Joints', 'hands',
    'x2', ['fing_mid_2_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_mid_2_up_L', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_mid_2_down_L', 75), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_mid_2_L', 'fing_mid_3_L', 'fing_mid_4_L'],
    [17],
    ['fing_mid_2_L', 'fing_mid_3_L', 'fing_mid_4_L'],
    ['fing_mid_2_def_L', 'fing_mid_3_def_L', 'fing_mid_4_def_L'],
    'shpaekey_edit',
    ['fing_mid_2_up_L', 'fing_mid_2_down_L'],
    ['fing_mid_3_up_L', 'fing_mid_3_down_L'],
    ['fing_mid_4_up_L', 'fing_mid_4_down_L'],
    ['', '', '', '', '', ''], 1,
    'fing_mid_2_up_L',
    False)

def SHAPEKEYS_Char_Ring_Joints(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Ring_Joints', 'hands',
    'x2', ['fing_ring_2_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_ring_2_up_L', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_ring_2_down_L', 75), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_ring_2_L', 'fing_ring_3_L', 'fing_ring_4_L'],
    [17],
    ['fing_ring_2_L', 'fing_ring_3_L', 'fing_ring_4_L'],
    ['fing_ring_2_def_L', 'fing_ring_3_def_L', 'fing_ring_4_def_L'],
    'shpaekey_edit',
    ['fing_ring_2_up_L', 'fing_ring_2_down_L'],
    ['fing_ring_3_up_L', 'fing_ring_3_down_L'],
    ['fing_ring_4_up_L', 'fing_ring_4_down_L'],
    ['', '', '', '', '', ''], 1,
    'fing_ring_2_up_L',
    False)

def SHAPEKEYS_Char_Little_Joints(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Little_Joints', 'hands',
    'x2', ['fing_lit_2_L',
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_lit_2_up_L', -45), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (get_driver_transform_rot('fing_lit_2_down_L', 75), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'fing_mid_5_toon_L', 'hand_fk_L', 'FRONT',
    ['fing_lit_2_L', 'fing_lit_3_L', 'fing_lit_4_L'],
    [17],
    ['fing_lit_2_L', 'fing_lit_3_L', 'fing_lit_4_L'],
    ['fing_lit_2_def_L', 'fing_lit_3_def_L', 'fing_lit_4_def_L'],
    'shpaekey_edit',
    ['fing_lit_2_up_L', 'fing_lit_2_down_L'],
    ['fing_lit_3_up_L', 'fing_lit_3_down_L'],
    ['fing_lit_4_up_L', 'fing_lit_4_down_L'],
    ['', '', '', '', '', ''], 1,
    'fing_lit_2_up_L',
    False)

def SHAPEKEYS_Char_Add_Face_Shapes(operator, context):

    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    #Perform end of step action and set current step name
    end_of_step_action(context)
    guide_props.guide_current_step = 'SHAPEKEYS_Char_Add_Face_Shapes'

    #Show Armature
    show_armature(context)

    # Adjust view to Bones.
    frame_bones(context, 'master', 'head_stretch')
    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    deselect_all_objects(context)

    #Cage
    set_active_object(context, guide_props.character_head_obj)

def SHAPEKEYS_Char_Eyebrow_Up(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyebrow_Up', 'head',
    'x2', ['brow_mstr_L',
    (0.0, 0.0, get_driver_transform_loc('brow_1_up_L', bpy.context.scene.blenrig_guide.arm_obj.pose.bones['forehead_def_3_L'].length * 0.75)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'head_stretch', 'FRONT',
    ['brow_mstr_L'],
    [2],
    ['brow_mstr_L'],
    ['frown_def', 'brow_def_3_L'],
    'shpaekey_edit',
    ['brow_up_L', 'brow_1_up_L', 'brow_2_up_L', 'brow_3_up_L', 'brow_4_up_L', 'brow_5_up_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'brow_up_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_up_L'].value = 1.0
    except:
        pass
    #Mute actual Brow Shapekeys so that they don't influence the current shape
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_1_up_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_2_up_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_3_up_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_4_up_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_5_up_L'].mute = True
    except:
        pass

def SHAPEKEYS_Char_Eyebrow_Down(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyebrow_Down', 'head',
    'x2', ['brow_mstr_L',
    (0.0, 0.0, get_driver_transform_loc('brow_1_down_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['brow_arch_def_3_L'].length * 0.75))), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'head_stretch', 'FRONT',
    ['brow_mstr_L'],
    [2],
    ['brow_mstr_L'],
    ['frown_def', 'brow_def_3_L'],
    'shpaekey_edit',
    ['brow_down_L', 'brow_1_down_L', 'brow_2_down_L', 'brow_3_down_L', 'brow_4_down_L', 'brow_5_down_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'brow_down_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_down_L'].value = 1.0
    except:
        pass
    #Mute actual Brow Shapekeys so that they don't influence the current shape
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_1_down_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_2_down_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_3_down_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_4_down_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_5_down_L'].mute = True
    except:
        pass

def SHAPEKEYS_Char_Eyebrow_Weight(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyebrow_Weight', 'head',
    'x2', ['brow_mstr_L',
    (0.0, 0.0, get_driver_transform_loc('brow_1_up_L', bpy.context.scene.blenrig_guide.arm_obj.pose.bones['forehead_def_3_L'].length * 0.75)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, get_driver_transform_loc('brow_1_down_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['brow_arch_def_3_L'].length * 0.75))), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    0],
    'nostril_ctrl_L', 'head_stretch', 'FRONT',
    ['brow_mstr_L', 'brow_ctrl_1_L', 'brow_ctrl_2_L', 'brow_ctrl_3_L', 'brow_ctrl_4_L', 'brow_ctrl_5_L'],
    [1, 2],
    ['brow_mstr_L', 'brow_ctrl_1_L', 'brow_ctrl_2_L', 'brow_ctrl_3_L', 'brow_ctrl_4_L', 'brow_ctrl_5_L'],
    ['shapekeys_brow_1_L', 'shapekeys_brow_1_L', 'shapekeys_brow_2_L', 'shapekeys_brow_3_L', 'shapekeys_brow_4_L', 'shapekeys_brow_5_L'],
    'weight_paint',
    ['brow_up_L', 'brow_1_up_L', 'brow_2_up_L', 'brow_3_up_L', 'brow_4_up_L', 'brow_5_up_L'],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'brow_up_L',
    True)

    #Active VGroup Fix
    set_active_vgroup(bpy.context.scene.blenrig_guide.guide_active_wp_group)

def SHAPEKEYS_Char_Frown_Up(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Frown_Up', 'head',
    'x2', ['frown_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_ctrl_out_L', 'brow_ctrl_out_R', 'FRONT',
    ['frown_ctrl', 'brow_mstr_L', 'brow_mstr_R'],
    [1, 2],
    ['frown_ctrl'],
    ['frown_def'],
    'shpaekey_edit',
    ['frown_up', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'frown_up',
    True)

    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones['brow_mstr_L'].location[2] = get_driver_transform_loc('brow_1_up_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['forehead_def_mid'].length * 0.75))
    guide_props.arm_obj.pose.bones['brow_mstr_R'].location[2] = get_driver_transform_loc('brow_1_up_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['forehead_def_mid'].length * 0.75))

def SHAPEKEYS_Char_Frown_Down(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Frown_Up', 'head',
    'x2', ['frown_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_ctrl_out_L', 'brow_ctrl_out_R', 'FRONT',
    ['frown_ctrl', 'brow_mstr_L', 'brow_mstr_R'],
    [1, 2],
    ['frown_ctrl'],
    ['frown_def'],
    'shpaekey_edit',
    ['frown_down', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'frown_down',
    True)

    guide_props = bpy.context.scene.blenrig_guide
    guide_props.arm_obj.pose.bones['brow_mstr_L'].location[2] = get_driver_transform_loc('brow_1_down_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['nose_def_1_mid'].length * 0.75))
    guide_props.arm_obj.pose.bones['brow_mstr_R'].location[2] = get_driver_transform_loc('brow_1_down_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones['nose_def_1_mid'].length * 0.75))

def SHAPEKEYS_Char_Eyebrow_In(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyebrow_In', 'head',
    'x2', ['brow_ctrl_in_L',
    (get_driver_transform_loc('brow_1_in_L', bpy.context.scene.blenrig_guide.arm_obj.pose.bones['frown_low_def_L'].length * 0.5), 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'brow_ctrl_out_L', 'brow_ctrl_out_R', 'FRONT',
    ['brow_ctrl_in_L'],
    [0],
    ['brow_ctrl_in_L'],
    ['frown_def'],
    'shpaekey_edit',
    ['brow_1_in_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'brow_1_in_L',
    False)

def SHAPEKEYS_Char_Eyelid_Up_Up(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyelid_Up_Up', 'head',
    'x2', ['eyelid_up_ctrl_L',
    (0.0, 0.0, get_driver_transform_loc('eyelid_up_up_L', bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['eyelid_up_ctrl_L'],
    [0],
    ['eyelid_up_ctrl_L'],
    ['eyelid_up_def_2_L'],
    'shpaekey_edit',
    ['eyelid_up_up_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'eyelid_up_up_L',
    False)

def SHAPEKEYS_Char_Eyelid_Up_Down_1(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyelid_Up_Down_1', 'head',
    'x2', ['eyelid_up_ctrl_L',
    (0.0, 0.0, get_driver_transform_loc('eyelid_up_down_1_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L / 2))), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['eyelid_up_ctrl_L'],
    [0],
    ['eyelid_up_ctrl_L'],
    ['eyelid_up_def_2_L'],
    'char_mesh',
    ['eyelid_up_down_1_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'eyelid_up_down_1_L',
    False)

def SHAPEKEYS_Char_Eyelid_Up_Down_2(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyelid_Up_Down_2', 'head',
    'x2', ['eyelid_up_ctrl_L',
    (0.0, 0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['eyelid_up_ctrl_L'],
    [0],
    ['eyelid_up_ctrl_L'],
    ['eyelid_up_def_2_L'],
    'shpaekey_edit',
    ['eyelid_up_down_2_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'eyelid_up_down_2_L',
    False)

def SHAPEKEYS_Char_Eyelid_Low_Down(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyelid_Low_Down', 'head',
    'x2', ['eyelid_low_ctrl_L',
    (0.0, 0.0, get_driver_transform_loc('eyelid_low_down_L', -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_low_ctrl_L"].EYELID_DOWN_LIMIT_L))), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['eyelid_low_ctrl_L'],
    [0],
    ['eyelid_low_ctrl_L'],
    ['eyelid_low_def_2_L'],
    'shpaekey_edit',
    ['eyelid_low_down_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'eyelid_low_down_L',
    False)

def SHAPEKEYS_Char_Eyelid_Low_Up_1(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyelid_Low_Up_1', 'head',
    'x2', ['eyelid_low_ctrl_L',
    (0.0, 0.0, get_driver_transform_loc('eyelid_low_up_1_L', bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L / 2)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['eyelid_low_ctrl_L'],
    [0],
    ['eyelid_low_ctrl_L'],
    ['eyelid_low_def_2_L'],
    'char_mesh',
    ['eyelid_low_up_1_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'eyelid_low_up_1_L',
    False)

def SHAPEKEYS_Char_Eyelid_Low_Up_2(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Eyelid_Low_Up_2', 'head',
    'x2', ['eyelid_low_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['eyelid_low_ctrl_L'],
    [0],
    ['eyelid_low_ctrl_L'],
    ['eyelid_low_def_2_L'],
    'shpaekey_edit',
    ['eyelid_low_up_2_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'eyelid_low_up_2_L',
    False)

def SHAPEKEYS_Char_Cheeks(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Cheeks', 'head',
    'x2', ['cheek_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_ctrl_L"].CHEEK_DOWN_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['cheek_ctrl_L'],
    [0],
    ['cheek_ctrl_L'],
    ['cheek_def_3_2_L'],
    'shpaekey_edit',
    ['cheek_up_L', 'cheek_down_L', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'cheek_up_L',
    False)

def SHAPEKEYS_Char_Nose_Frown(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Nose_Frown', 'head',
    'x2', ['nose_frown_ctrl_L',
    (0.0, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["nose_frown_ctrl_L"].FROWN_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['nose_frown_ctrl_L'],
    [0],
    ['nose_frown_ctrl_L'],
    ['nose_side_def_2_L'],
    'shpaekey_edit',
    ['nose_frown_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'nose_frown_L',
    False)

def SHAPEKEYS_Char_Nostril(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Nostril', 'head',
    'x2', ['nostril_ctrl_L',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 2.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.5, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'nostril_ctrl_L', 'brow_mstr_L', 'FRONT',
    ['nostril_ctrl_L'],
    [0],
    ['nostril_ctrl_L'],
    ['nostril_back_def_L'],
    'shpaekey_edit',
    ['nostril_expand_L', 'nostril_collapse_L', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'nostril_expand_L',
    False)

def SHAPEKEYS_Char_Mouth_Corner_Base(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Corner_Base', 'head',
    'x6', ['mouth_corner_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L) * 0.25, 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L) * 0.1, 0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L) * 0.25, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].BACK_LIMIT_L), 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].FORW_LIMIT_L, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'],
    ['lip_low_outer_def_4_1_L'],
    'shpaekey_edit',
    ['mouth_corner_out_L', 'mouth_corner_up_L', 'mouth_corner_down_L', 'mouth_corner_back_L', 'mouth_corner_forw_L', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_corner_out_L',
    False)

def SHAPEKEYS_Char_Mouth_Corner_Fix_1(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Corner_Fix_1', 'head',
    'x4', ['mouth_corner_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), 0.0, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), 0.0, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].BACK_LIMIT_L), 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].FORW_LIMIT_L, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'],
    ['lip_low_outer_def_4_1_L'],
    'shpaekey_edit',
    ['mouth_corner_out_up_fix_L', 'mouth_corner_out_down_fix_L', 'mouth_corner_out_back_fix_L', 'mouth_corner_out_forw_fix_L', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_corner_out_up_fix_L',
    False)

def SHAPEKEYS_Char_Mouth_Corner_Fix_2(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Corner_Fix_2', 'head',
    'x4', ['mouth_corner_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].BACK_LIMIT_L), bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].BACK_LIMIT_L), -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].FORW_LIMIT_L, bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].UP_LIMIT_L), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].FORW_LIMIT_L, -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].DOWN_LIMIT_L)), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'],
    ['lip_low_outer_def_4_1_L'],
    'shpaekey_edit',
    ['mouth_corner_out_back_up_fix_L', 'mouth_corner_out_back_down_fix_L', 'mouth_corner_out_forw_up_fix_L', 'mouth_corner_out_forw_down_fix_L', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_corner_out_back_up_fix_L',
    False)

def SHAPEKEYS_Char_Mouth_Corner_In(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Corner_In', 'head',
    'x2', ['mouth_corner_L',
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'],
    ['lip_low_outer_def_4_1_L'],
    'shpaekey_edit',
    ['mouth_corner_in_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_corner_in_L',
    False)

def SHAPEKEYS_Char_Mouth_Weight(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Weight', 'head',
    'x2', ['maxi',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['maxi'],
    [1, 2],
    ['maxi', 'mouth_corner_L', 'mouth_corner_R', 'mouth_ctrl'],
    ['shapekeys_mouth_up', 'shapekeys_mouth_up_L', 'shapekeys_mouth_low', 'shapekeys_mouth_low_L'],
    'weight_paint',
    ['U', '', '', '', '', ''],
    ['U', '', '', '', '', ''],
    ['U_up_L', '', '', '', '', ''],
    ['U_low_L', '', '', '', '', ''], 1,
    'U',
    True)

    #Active VGroup Fix
    set_active_vgroup(bpy.context.scene.blenrig_guide.guide_active_wp_group)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['maxi'].rotation_euler[0] = radians(-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_DOWN_LIMIT))

def SHAPEKEYS_Char_Mouth_U(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_U', 'head',
    'x2', ['mouth_ctrl',
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_ctrl"].IN_LIMIT, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_ctrl'],
    [0],
    ['mouth_ctrl'],
    ['shapekeys_mouth_up'],
    'shpaekey_edit',
    ['U', 'U_up_L', 'U_low_L', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'U',
    True)

    guide_props = bpy.context.scene.blenrig_guide
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['U'].value = 1.0
    except:
        pass
    #Mute actual Brow Shapekeys so that they don't influence the current shape
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_up_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_low_L'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_up_R'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_low_R'].mute = True
    except:
        pass

def SHAPEKEYS_Char_Mouth_U_Thickness(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_U_Thickness', 'head',
    'x2', ['mouth_ctrl',
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_ctrl"].IN_LIMIT, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 0.5),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_ctrl'],
    [0],
    ['mouth_ctrl'],
    ['shapekeys_mouth_up'],
    'shpaekey_edit',
    ['U_thickness', 'U_thickness_up', 'U_thickness_low', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'U_thickness',
    True)

    guide_props = bpy.context.scene.blenrig_guide
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_thickness'].value = 1.0
    except:
        pass
    #Mute actual Brow Shapekeys so that they don't influence the current shape
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_thickness_up'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['U_thickness_low'].mute = True
    except:
        pass

def SHAPEKEYS_Char_Mouth_M(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_M', 'head',
    'x2', ['mouth_up_ctrl',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_up_ctrl', 'mouth_low_ctrl'],
    [0],
    ['mouth_up_ctrl'],
    ['shapekeys_mouth_up'],
    'shpaekey_edit',
    ['M', 'M_up', 'M_low', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'M',
    True)

    guide_props = bpy.context.scene.blenrig_guide
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['M'].value = 1.0
    except:
        pass
    #Mute actual Brow Shapekeys so that they don't influence the current shape
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['M_up'].mute = True
        guide_props.character_head_obj.data.shape_keys.key_blocks['M_low'].mute = True
    except:
        pass
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_up_ctrl'].location[1] = -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_ctrl"].U_M_CTRL_LIMIT)
    guide_props.arm_obj.pose.bones['mouth_low_ctrl'].location[1] =  -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_ctrl"].U_M_CTRL_LIMIT)

def SHAPEKEYS_Char_Mouth_Open_Close(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Open_Close', 'head',
    'x2', ['maxi',
    (0.0, 0.0, 0.0), (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_DOWN_LIMIT), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_UP_LIMIT, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'RIGHT',
    ['maxi'],
    [0],
    ['maxi'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_open_down', 'mouth_close_up', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_open_down',
    True)

def SHAPEKEYS_Char_Mouth_Open_Out(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Open_Out', 'head',
    'x2', ['maxi',
    (0.0, 0.0, 0.0), (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_DOWN_LIMIT), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['maxi', 'mouth_corner_L'],
    [0],
    ['maxi'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_open_corner_out_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_open_corner_out_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_corner_L'].location[0] = -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L)


def SHAPEKEYS_Char_Mouth_Open_In(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Open_In', 'head',
    'x2', ['maxi',
    (0.0, 0.0, 0.0), (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_DOWN_LIMIT), 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['maxi', 'mouth_corner_L'],
    [0],
    ['maxi'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_open_corner_in_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_open_corner_in_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_corner_L'].location[0] = bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

def SHAPEKEYS_Char_Mouth_Close_Out(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Close_Out', 'head',
    'x2', ['maxi',
    (0.0, 0.0, 0.0), (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_UP_LIMIT, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['maxi', 'mouth_corner_L'],
    [0],
    ['maxi'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_close_corner_out_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_close_corner_out_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_corner_L'].location[0] = -(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L)


def SHAPEKEYS_Char_Mouth_Close_In(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Close_In', 'head',
    'x2', ['maxi',
    (0.0, 0.0, 0.0), (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["maxi"].JAW_UP_LIMIT, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['maxi', 'mouth_corner_L'],
    [0],
    ['maxi'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_close_corner_in_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_close_corner_in_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_corner_L'].location[0] = bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L

def SHAPEKEYS_Char_Mouth_Frown_Side(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Frown_Side', 'head',
    'x2', ['mouth_mstr_ik',
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_mstr_ik'],
    [0, 26],
    ['mouth_mstr_ik'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_frown_side_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_frown_side_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_mode = 'XYZ'
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Copy Transforms'].mute = True
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Damped Track'].mute = True
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_euler[2] = get_driver_transform_loc('mouth_frown_side_L', 45)

def SHAPEKEYS_Char_Mouth_Frown_Side_Out(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Frown_Side_Out', 'head',
    'x2', ['mouth_corner_L',
    (-(bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].OUT_LIMIT_L), 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_frown_side_corner_out_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_frown_side_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_mode = 'XYZ'
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Copy Transforms'].mute = True
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Damped Track'].mute = True
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_euler[2] = get_driver_transform_loc('mouth_frown_side_L', 45)

def SHAPEKEYS_Char_Mouth_Frown_Side_In(operator, context):
    shapekey_step(operator, context, 'SHAPEKEYS_Char_Mouth_Frown_Side_In', 'head',
    'x2', ['mouth_corner_L',
    (bpy.context.scene.blenrig_guide.arm_obj.pose.bones["mouth_corner_L"].IN_LIMIT_L, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 1.0),
    1],
    'jaw_line_ctrl_mid', 'head_stretch', 'FRONT',
    ['mouth_corner_L'],
    [0],
    ['mouth_corner_L'],
    ['shapekeys_mouth_low'],
    'shpaekey_edit',
    ['mouth_frown_side_corner_out_L', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''], 1,
    'mouth_frown_side_L',
    False)

    guide_props = bpy.context.scene.blenrig_guide
    #Set Pose
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_mode = 'XYZ'
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Copy Transforms'].mute = True
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Damped Track'].mute = True
    guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_euler[2] = get_driver_transform_loc('mouth_frown_side_L', 45)

#### END OF STEP ACTIONS ####

def shapekeys_end_generic(context):
    guide_props = context.scene.blenrig_guide
    ob = guide_props.active_shp_obj

    #Mirror Edited Shapekeys
    try:
        blenrig_temp_link(ob)
    except:
        pass
    try:
        if guide_props.auto_mirror_shapekeys:
            ob.hide_viewport = False
            deselect_all_objects(context)
            set_active_object(context, ob)
            if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys'):
                if hasattr(ob.data.shape_keys, 'key_blocks'):
                    shapekeys = ob.data.shape_keys.key_blocks
                    for list in bpy.context.scene.blenrig_shapekeys_list:
                        shapes_1 = list.list_1
                        if shapes_1 in shapekeys:
                            set_active_shapekey(shapes_1)
                            if hasattr(ob.active_shape_key, 'name'):
                                if ob.active_shape_key.name.endswith('_L') or ob.active_shape_key.name.endswith('_R'):
                                    bpy.ops.blenrig.mirror_active_shapekey()
                                    bpy.ops.blenrig.mirror_active_shapekey_driver()
                        shapes_2 = list.list_2
                        if shapes_2 in shapekeys:
                            set_active_shapekey(shapes_2)
                            if hasattr(ob.active_shape_key, 'name'):
                                if ob.active_shape_key.name.endswith('_L') or ob.active_shape_key.name.endswith('_R'):
                                    bpy.ops.blenrig.mirror_active_shapekey()
                                    bpy.ops.blenrig.mirror_active_shapekey_driver()
                        shapes_3 = list.list_3
                        if shapes_3 in shapekeys:
                            set_active_shapekey(shapes_3)
                            if hasattr(ob.active_shape_key, 'name'):
                                if ob.active_shape_key.name.endswith('_L') or ob.active_shape_key.name.endswith('_R'):
                                    bpy.ops.blenrig.mirror_active_shapekey()
                                    bpy.ops.blenrig.mirror_active_shapekey_driver()
                        shapes_4 = list.list_4
                        if shapes_4 in shapekeys:
                            set_active_shapekey(shapes_4)
                            if hasattr(ob.active_shape_key, 'name'):
                                if ob.active_shape_key.name.endswith('_L') or ob.active_shape_key.name.endswith('_R'):
                                    bpy.ops.blenrig.mirror_active_shapekey()
                                    bpy.ops.blenrig.mirror_active_shapekey_driver()
    except:
        pass
    try:
        ob.use_shape_key_edit_mode = True
        ob.show_only_shape_key = False
    except:
        pass

    #Select Armature
    if context.active_object.type == 'MESH':
        deselect_all_objects(context)
        select_armature(context)

    #Ensure POSE Mode
    go_blenrig_pose_mode(context)

    #Reset Transforms
    unhide_all_bones(context)
    deselect_all_pose_bones(context)
    reset_all_bones_transforms()

    #Turn Layers off
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Unlink Temp Collection
    blenrig_temp_unlink()

#Property for action to be performed after steps
def end_of_step_action(context):
    guide_props = context.scene.blenrig_guide
    blenrig_bones = guide_props.arm_obj.pose.bones
    current_step = guide_props.guide_current_step
    shapekeys_end_generic(context)
    Leg_Steps = ['SHAPEKEYS_Cage_Shoulder', 'SHAPEKEYS_Cage_Foot_Toe', 'SHAPEKEYS_Cage_Knee', 'SHAPEKEYS_Cage_Thigh']
    #Leg IK Switch
    for step in Leg_Steps:
        if current_step == step:
            #Set Rig Control Properties
            blenrig_bones["properties_leg_L"].ik_leg_L =  0.0
            blenrig_bones["properties_leg_R"].ik_leg_R =  0.0
            guide_props.guide_current_step = ''
    if current_step == 'SHAPEKEYS_Cage_Torso':
        #Turn Organic Spine Back On
        blenrig_bones["properties_torso"]["organic_spine"] = 1
    if current_step == 'SHAPEKEYS_Cage_Neck':
        #Turn Organic Spine Back On
        blenrig_bones["properties_head"]["organic_neck"] = 1
    Arm_Steps = ['SHAPEKEYS_Cage_Ankle', 'SHAPEKEYS_Cage_Elbow', 'SHAPEKEYS_Cage_Wrist', 'SHAPEKEYS_Char_Wrist']
    #Arm IK Switch
    for step in Arm_Steps:
        if current_step == step:
            #Set Rig Control Properties
            blenrig_bones["properties_arm_L"].ik_arm_L =  0.0
            blenrig_bones["properties_arm_R"].ik_arm_R =  0.0
            blenrig_bones["properties_arm_L"].space_hand_L =  0.0
            blenrig_bones["properties_arm_R"].space_hand_R =  0.0
    if current_step == 'SHAPEKEYS_Char_Eyebrow_Up':
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['brow_up_L'].value = 0.0
            guide_props.character_head_obj.data.shape_keys.key_blocks['brow_up_R'].value = 0.0
        except:
            pass
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_1_up_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_2_up_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_3_up_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_4_up_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_5_up_L'].mute = False
    except:
        pass
    if current_step == 'SHAPEKEYS_Char_Eyebrow_Down':
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['brow_down_L'].value = 0.0
            guide_props.character_head_obj.data.shape_keys.key_blocks['brow_down_R'].value = 0.0
        except:
            pass
    try:
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_1_down_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_2_down_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_3_down_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_4_down_L'].mute = False
        guide_props.character_head_obj.data.shape_keys.key_blocks['brow_5_down_L'].mute = False
    except:
        pass
    if current_step == 'SHAPEKEYS_Char_Mouth_U':
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['U'].value = 0.0
        except:
            pass
        #Mute actual Brow Shapekeys so that they don't influence the current shape
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_up_L'].mute = False
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_low_L'].mute = False
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_up_R'].mute = False
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_low_R'].mute = False
        except:
            pass
    if current_step == 'SHAPEKEYS_Char_Mouth_U_Thickness':
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_thickness'].value = 0.0
        except:
            pass
        #Mute actual Brow Shapekeys so that they don't influence the current shape
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_thickness_up'].mute = False
            guide_props.character_head_obj.data.shape_keys.key_blocks['U_thickness_low'].mute = False
        except:
            pass
    if current_step == 'SHAPEKEYS_Char_Mouth_M':
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['M'].value = 0.0
        except:
            pass
        #Mute actual Brow Shapekeys so that they don't influence the current shape
        try:
            guide_props.character_head_obj.data.shape_keys.key_blocks['M_up'].mute = False
            guide_props.character_head_obj.data.shape_keys.key_blocks['M_low'].mute = False
        except:
            pass
    Frown_Side_Steps = ['SHAPEKEYS_Char_Mouth_Frown_Side', 'SHAPEKEYS_Char_Mouth_Frown_Side_Out', 'SHAPEKEYS_Char_Mouth_Frown_Side_In']
    if current_step in Frown_Side_Steps:
        guide_props.arm_obj.pose.bones['mouth_mstr_ik'].rotation_mode = 'QUATERNION'
        guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Copy Transforms'].mute = False
        guide_props.arm_obj.pose.bones['mouth_mstr_ik'].constraints['Damped Track'].mute = False

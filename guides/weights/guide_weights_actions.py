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

def joint_rotations(BONE, X, X_NEG, Y, Y_NEG, Z, Z_NEG, PROP_VALUE):
    #Set Bone and Angles
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_transformation_bone = BONE
    guide_props.guide_x_rotation = X
    guide_props.guide_y_rotation = Y
    guide_props.guide_z_rotation = Z
    guide_props.guide_x_rotation_neg = X_NEG
    guide_props.guide_y_rotation_neg = Y_NEG
    guide_props.guide_z_rotation_neg = Z_NEG
    #Set Pose property
    if guide_props.guide_rotation_type == 'x6':
        guide_props.guide_joint_rotate_X6 = PROP_VALUE
    elif guide_props.guide_rotation_type == 'x4':
        guide_props.guide_joint_rotate_X4 = PROP_VALUE
    elif guide_props.guide_rotation_type == 'x2'   :
        guide_props.guide_joint_rotate_X2 = PROP_VALUE

def weight_step(operator, context, step_name, wp_obj,
joint_type, joint_parameters, rot_order,
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
    elif wp_obj == 'hands':
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
    guide_props.guide_rotation_order = rot_order
    guide_props.guide_rotation_type = joint_type
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

    if mode == 'weight_paint':
        #Set Weight Paint Mode
        set_active_object(context, paint_obj)
        if context.mode != 'WEIGHT_PAINT':
            set_mode('WEIGHT_PAINT')

    if mode == 'mdef_mesh':
        #Set Weight Paint Mode
        set_active_object(context, paint_obj)
        if context.mode != 'WEIGHT_PAINT':
            set_mode('WEIGHT_PAINT')
            bpy.ops.blenrig.toggle_weight_painting(paint_object='mdef_cage')


#### WEIGHTS STEPS ####

def WEIGHTS_Cage_Ankle(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Ankle', 'mdef_cage',
    'x6', ['foot_fk_L', 60, -60, 45, -45, 60, -60, 1], 'XZY',
    'foot_fk_L', 'sole_pivot_point_L', 'RIGHT',
    ['foot_fk_L', 'foot_def_L', 'shin_twist_def_L', 'instep_fix_L', 'ankle_fix_L'],
    [27],
    ['foot_fk_L'],
    ['foot_def_L'],
    'mdef_mesh',)

    #Set Rig Control Properties
    bpy.ops.snap.leg_ik_to_fk_l()
    bpy.ops.snap.leg_ik_to_fk_r()

def WEIGHTS_Cage_Foot_Toe(operator, context):
    weight_step(operator, context, 'WEIGHTS_Cage_Foot_Toe', 'mdef_cage',
    'x4', ['foot_toe_1_fk_L', 60, -60, 0, 0, 60, -60, 1], 'XZ',
    'foot_fk_L', 'sole_pivot_point_L', 'RIGHT',
    ['foot_toe_fix_up_1_L', 'foot_toe_1_fk_L', 'foot_toe_2_fk_L', 'foot_toe_fix_up_2_L', 'foot_toe_fix_low_2_L', 'foot_toe_fix_low_1_L', 'foot_def_L', 'foot_toe_1_def_L', 'foot_toe_2_def_L'],
    [27],
    ['foot_toe_1_fk_L', 'foot_toe_2_fk_L'],
    ['foot_toe_1_def_L', 'foot_toe_2_def_L'],
    'mdef_mesh',)

    #Set Rig Control Properties
    bpy.ops.snap.leg_ik_to_fk_l()
    bpy.ops.snap.leg_ik_to_fk_r()

#### END OF STEP ACTIONS ####

def weights_end_generic(context):

    guide_props = bpy.context.scene.blenrig_guide

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

#Property for action to be performed after steps
def end_of_step_action(context):
    weights_end_generic(context)
    # guide_props = bpy.context.scene.blenrig_guide
    # current_step = bpy.context.scene.blenrig_guide.guide_current_step
    # steps = ['ACTIONS_Fingers_Spread_X_Up', 'ACTIONS_Fingers_Spread_X_Down', 'ACTIONS_Fingers_Spread_Z_Out', 'ACTIONS_Fingers_Spread_Z_In',
    # 'ACTIONS_Fingers_Curl_In', 'ACTIONS_Fingers_Curl_Out', 'ACTIONS_Hand_Close', 'ACTIONS_Hand_Open', 'ACTIONS_Breathing_in', 'ACTIONS_Breathing_Out',
    # 'ACTIONS_Eyelids_Up_Up_Range', 'ACTIONS_Eyelids_Up_Up', 'ACTIONS_Eyelids_Up_Down_Range', 'ACTIONS_Eyelids_Up_Down_1', 'ACTIONS_Eyelids_Up_Down_2',
    # 'ACTIONS_Eyelids_Low_Down_Range', 'ACTIONS_Eyelids_Low_Down', 'ACTIONS_Eyelids_Low_Up_Range', 'ACTIONS_Eyelids_Low_Up_1', 'ACTIONS_Eyelids_Low_Up_2',
    # 'ACTIONS_Cheek_Up_Range', 'ACTIONS_Cheek_Up', 'ACTIONS_Cheek_Down_Range', 'ACTIONS_Cheek_Down', 'ACTIONS_Cheek_Frown', 'ACTIONS_Eyelids_Out', 'ACTIONS_Eyelids_In',
    # 'ACTIONS_Jaw_Down_Range', 'ACTIONS_Jaw_Up_Range', 'ACTIONS_Jaw_Down', 'ACTIONS_Jaw_Up', 'ACTIONS_Mouth_Corner_Out_Range', 'ACTIONS_Mouth_Corner_Out', 'ACTIONS_Mouth_Corner_Up_Range', 'ACTIONS_Mouth_Corner_Up',
    # 'ACTIONS_Mouth_Corner_Down_Range', 'ACTIONS_Mouth_Corner_Down', 'ACTIONS_Mouth_Corner_Back_Range', 'ACTIONS_Mouth_Corner_Back', 'ACTIONS_Mouth_Corner_Forw_Range', 'ACTIONS_Mouth_Corner_Forw',
    # 'ACTIONS_Mouth_Corner_In_Range', 'ACTIONS_Mouth_Corner_In', 'ACTIONS_Mouth_Corner_Up_Out_Corrective', 'ACTIONS_Mouth_Corner_Down_Out_Corrective'
    # 'ACTIONS_U_O_M_Range', 'ACTIONS_U', 'ACTIONS_O', 'ACTIONS_M', 'ACTIONS_U_Narrow_Corrective', 'ACTIONS_U_Thicker_Lips', 'ACTIONS_U_Thinner_Lips',
    # 'ACTIONS_Mouth_Frown_Range', 'ACTIONS_Mouth_Frown', 'ACTIONS_Chin_Frown_Range','ACTIONS_Chin_Frown_Up', 'ACTIONS_Chin_Frown_Down',
    # 'ACTIONS_Mouth_Corner_In_Zipper', 'ACTIONS_U_Zipper', 'ACTIONS_O_Zipper', 'ACTIONS_U_Narrow_Corrective_Zipper']
    # for step in steps:
    #     if current_step == step:
    #         actions_end_generic(context)
    #         bpy.context.scene.blenrig_guide.guide_current_step = ''
    # if current_step == 'ACTIONS_Eyelids_Up_Up_Range':
    #     #Enable Action Constraints
    #     mute_constraints('Eyelid_Upper_Up', False)
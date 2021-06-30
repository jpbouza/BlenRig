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

def ball_joint_rotations(BONE, X, X_NEG, Y, Y_NEG, Z, Z_NEG, PROP_VALUE):
    #Set Bone and Angles
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_transformation_bone = BONE
    guide_props.guide_x_rotation = X
    guide_props.guide_y_rotation = Y
    guide_props.guide_z_rotation = Z
    guide_props.guide_x_rotation_neg = X_NEG
    guide_props.guide_y_rotation_neg = Y_NEG
    guide_props.guide_z_rotation_neg = Z_NEG
    #Reset rotation property
    guide_props.guide_ball_joint_rotate = PROP_VALUE

#### WEIGHTS STEPS ####

def WEIGHTS_Cage_Ankle(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'WEIGHTS_Cage_Ankle'

    #Cage
    show_mdef_cage(context)
    mdef_cage = bpy.context.scene.blenrig_guide.mdef_cage_obj
    set_active_vgroup('foot_def_L')

    #Set Bone and Angles
    ball_joint_rotations('sole_ctrl_L', 60, -60, 45, -45, 60, -60, 0)

    deselect_all_objects(context)

    #Show Armature
    show_armature(context)

    # Adjust view to Bones.
    frame_bones(context, "foot_fk_L", "sole_pivot_point_L")
    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    #Toggle Pose X-Mirror
    toggle_pose_x_mirror(context, True)

    bones = ('sole_ctrl_L', 'sole_ctrl_R')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Turn On Deformation Layer
    on_layers = [27]
    for l in on_layers:
        bpy.context.object.data.layers[l] = True

    #Unhide Bones in Deformation Layer
    hide_bones_in_layer(context, *on_layers, state=False)
    deselect_all_pose_bones(context, invert=False)

    #Set Active Bone
    select_pose_bone(context, 'sole_ctrl_L')

    #Set Weight Paint Mode
    set_active_object(context, mdef_cage)
    if context.mode != 'WEIGHT_PAINT':
        set_mode('WEIGHT_PAINT')

    #Active VGroup
    set_active_vgroup('foot_def_L')

#### END OF STEP ACTIONS ####

def actions_end_generic(context):
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

    #Turn Layers on
    off_layers = [27, 28]
    for l in off_layers:
        bpy.context.object.data.layers[l] = False

#Property for action to be performed after steps
def end_of_step_action(context):
    print ('kk')
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
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

#### ACTIONS STEPS ####

def ACTIONS_Fingers_Spread_X_Up(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'ACTIONS_Fingers_Spread_X_Up'

    #Set Mdef Cage
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
    frame_bones(context, "hand_ik_ctrl_L", "hand_close_L")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    #Assign Action
    assign_action('zrig_fing_spread_x', 1)

    #Turn On Actions Layer
    on_layers = [28]
    for l in on_layers:
        bpy.context.object.data.layers[l] = True

    #Bones
    bones = ('fing_mid_ctrl_mstr_L', 'fing_ring_ctrl_mstr_L', 'fing_lit_ctrl_mstr_L')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)
    deselect_all_pose_bones(context)

def ACTIONS_Fingers_Spread_X_Down(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'ACTIONS_Fingers_Spread_X_Up'

    #Set Mdef Cage
    deselect_all_objects(context)

    #Armature for setting view
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "hand_ik_ctrl_L", "hand_close_L")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    assign_action('zrig_fing_spread_x', -1)


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
    if current_step == 'ACTIONS_Fingers_Spread_X_Up':
        actions_end_generic(context)
        bpy.context.scene.blenrig_guide.guide_current_step = ''

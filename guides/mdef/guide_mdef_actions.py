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

#### MDEF STEPS ####

def MDEF_Select_Body_Objects(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Select_Body_Objects'

    #Set Mdef Cage
    deselect_all_objects(context)


    #Armature for setting view
    show_armature(context)

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = True

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    #Select Head object
    try:
        bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_head_obj
    except:
        pass

def MDEF_Edit_Mdef_Cage(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Edit_Mdef_Cage'

    deselect_all_objects(context)

    # Show Mdef
    mdef_cage_objects = collect_cage()
    collect_cage()
    blenrig_temp_link(mdef_cage_objects)

    for ob in mdef_cage_objects:
        set_active_object(context, ob)
        bpy.context.scene.blenrig_guide.mdef_cage_obj = ob
        bpy.context.scene.blenrig_guide.mdef_cage_obj.hide_viewport = False
        set_mode('EDIT')

    #Hide Armature
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = True

def MDEF_Binding_Check(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Binding_Check'

    #Set Mdef Cage
    deselect_all_objects(context)

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    #Select Head object
    try:
        bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_head_obj
    except:
        pass



def MDEF_Final_Binding(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Final_Binding'

    #Set Mdef Cage
    deselect_all_objects(context)

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    #Select Head object
    try:
        bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_head_obj
    except:
        pass

#### END OF STEP ACTIONS ####
def mdef_end_generic(context):
    guide_props = context.scene.blenrig_guide

    #Select Armature
    if hasattr(context, 'active_object') and hasattr(context.active_object, 'type'):
        if context.active_object.type == 'MESH':
            deselect_all_objects(context)

    show_armature(context)

    #Ensure POSE Mode
    go_blenrig_pose_mode(context)

    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Reset Transforms
    reset_all_bones_transforms()

    #Turn Layers on
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Unlink Temp Collection
    blenrig_temp_unlink()

#Property for action to be performed after steps
def end_of_step_action(context):
    mdef_end_generic(context)
    #Armature for setting view
    show_armature(context)
    current_step = context.scene.blenrig_guide.guide_current_step
    if current_step == 'MDEF_Edit_Mdef_Cage':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''

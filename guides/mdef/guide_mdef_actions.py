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

def MDEF_Intro(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Intro'

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

    go_blenrig_object_mode(context)
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = True
    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    #Select Head object
    if bpy.context.scene.blenrig_guide.character_head_obj:
        bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_head_obj
    else:
        print("esta vacio")
        BlenRig_Empty(context)

def MDEF_Edit_Mdef_Cage(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Edit_Mdef_Cage'

    deselect_all_objects(context)

    # Show Mdef
    guide_props = bpy.context.scene.blenrig_guide
    mdef_cage = guide_props.mdef_cage_obj

    if mdef_cage != None:
        blenrig_temp_link([mdef_cage])
        set_active_object(context, mdef_cage)
        mdef_cage.hide_viewport = False
        set_mode('EDIT')
    else:
        mdef_cage_objects = collect_cage()
        collect_cage()
        blenrig_temp_link(mdef_cage_objects)

        for ob in mdef_cage_objects:
            set_active_object(context, ob)
            guide_props.mdef_cage_obj = ob
            guide_props.mdef_cage_obj.hide_viewport = False
            set_mode('EDIT')

    #Hide Armature
    guide_props.arm_obj.hide_viewport = True

def MDEF_Binding_Check(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Binding_Check'
    guide_props = bpy.context.scene.blenrig_guide

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
        set_active_object(context, guide_props.character_head_obj)
    except:
        pass

def MDEF_Final_Binding(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Final_Binding'
    guide_props = bpy.context.scene.blenrig_guide

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
        set_active_object(context, guide_props.character_head_obj)
    except:
        pass

def MDEF_Finish(operator, context):
    # Del BlenRig_Empty object
    del_BlenRig_Empty(context)
    
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Finish'

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

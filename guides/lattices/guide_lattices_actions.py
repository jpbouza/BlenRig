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

#### LATTICES STEPS ####

def LATTICES_Adjust_Body(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'LATTICES_Adjust_Body'

    #Set Mdef Cage
    deselect_all_objects(context)
    try:
        blenrig_temp_unlink()
    except:
        pass

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

    # Show Lattices
    lattice_objects = collect_lattice_objects()
    collect_lattice_objects()
    blenrig_temp_link(lattice_objects)

    #Hide other lattices
    Hide_Lattices = ['LATTICE_HEAD', 'LATTICE_BROW', 'LATTICE_MOUTH', 'LATTICE_EYE_L', 'LATTICE_EYE_R']
    for ob in Hide_Lattices:
        try:
            bpy.data.objects[ob].hide_viewport = True
        except:
            pass
    try:
        set_active_object(context, bpy.data.objects['LATTICE_BODY'])
    except:
        pass

def LATTICES_Adjust_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'LATTICES_Adjust_Head'

    #Set Mdef Cage
    deselect_all_objects(context)
    try:
        blenrig_temp_unlink()
    except:
        pass

    #Armature for setting view
    armature = bpy.context.scene.blenrig_guide.arm_obj

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "spine_3_fk")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Show Lattices
    lattice_objects = collect_lattice_objects()
    collect_lattice_objects()
    blenrig_temp_link(lattice_objects)

    #Hide other lattices
    Hide_Lattices = ['LATTICE_BODY', 'LATTICE_BROW', 'LATTICE_MOUTH', 'LATTICE_EYE_L', 'LATTICE_EYE_R']
    for ob in Hide_Lattices:
        try:
            bpy.data.objects[ob].hide_viewport = True
        except:
            pass
    try:
        set_active_object(context, bpy.data.objects['LATTICE_HEAD'])
    except:
        pass

def LATTICES_Adjust_Brow(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'LATTICES_Adjust_Brow'

    #Set Mdef Cage
    deselect_all_objects(context)
    try:
        blenrig_temp_unlink()
    except:
        pass

    #Armature for setting view
    armature = bpy.context.scene.blenrig_guide.arm_obj

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "neck_3_fk")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Show Lattices
    lattice_objects = collect_lattice_objects()
    collect_lattice_objects()
    blenrig_temp_link(lattice_objects)

    #Hide other lattices
    Hide_Lattices = ['LATTICE_HEAD', 'LATTICE_BODY', 'LATTICE_MOUTH', 'LATTICE_EYE_L', 'LATTICE_EYE_R']
    for ob in Hide_Lattices:
        try:
            bpy.data.objects[ob].hide_viewport = True
        except:
            pass
    try:
        set_active_object(context, bpy.data.objects['LATTICE_BROW'])
    except:
        pass

def LATTICES_Adjust_Mouth(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'LATTICES_Adjust_Mouth'

    #Set Mdef Cage
    deselect_all_objects(context)
    try:
        blenrig_temp_unlink()
    except:
        pass

    #Armature for setting view
    armature = bpy.context.scene.blenrig_guide.arm_obj

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "neck_3_fk")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Show Lattices
    lattice_objects = collect_lattice_objects()
    collect_lattice_objects()
    blenrig_temp_link(lattice_objects)

    #Hide other lattices
    Hide_Lattices = ['LATTICE_HEAD', 'LATTICE_BODY', 'LATTICE_BROW', 'LATTICE_EYE_L', 'LATTICE_EYE_R']
    for ob in Hide_Lattices:
        try:
            bpy.data.objects[ob].hide_viewport = True
        except:
            pass
    try:
        set_active_object(context, bpy.data.objects['LATTICE_MOUTH'])
    except:
        pass

def LATTICES_Adjust_Eyes(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'LATTICES_Adjust_Eyes'

    #Set Mdef Cage
    deselect_all_objects(context)
    try:
        blenrig_temp_unlink()
    except:
        pass

    #Armature for setting view
    armature = bpy.context.scene.blenrig_guide.arm_obj

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_str", "neck_3_fk")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Show Lattices
    lattice_objects = collect_lattice_objects()
    collect_lattice_objects()
    blenrig_temp_link(lattice_objects)

    #Hide other lattices
    Hide_Lattices = ['LATTICE_HEAD', 'LATTICE_BODY', 'LATTICE_BROW', 'LATTICE_MOUTH']
    for ob in Hide_Lattices:
        try:
            bpy.data.objects[ob].hide_viewport = True
        except:
            pass
    try:
        set_active_object(context, bpy.data.objects['LATTICE_EYE_L'])
    except:
        pass

#### END OF STEP ACTIONS ####
def lattices_end_generic(context):
    guide_props = context.scene.blenrig_guide

    #Select Armature
    if hasattr(context, 'active_object') and hasattr(context.active_object, 'type'):
        if context.active_object.type in ['MESH', 'LATTICE']:
            deselect_all_objects(context)

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

    #Unlink Temp Collection
    blenrig_temp_unlink()

#Property for action to be performed after steps
def end_of_step_action(context):
    lattices_end_generic(context)
    Hide_Lattices = ['LATTICE_HEAD', 'LATTICE_BROW', 'LATTICE_MOUTH', 'LATTICE_EYE_L', 'LATTICE_EYE_R', 'LATTICE_BODY']
    current_step = context.scene.blenrig_guide.guide_current_step
    if current_step == 'LATTICES_Adjust_Body' or current_step == 'LATTICES_Adjust_Head' or current_step == 'LATTICES_Adjust_Brow' or current_step == 'LATTICES_Adjust_Mouth' or current_step == 'LATTICES_Adjust_Eyes':
        #Unhide Lattices
        for ob in Hide_Lattices:
            try:
                bpy.data.objects[ob].hide_viewport = False
            except:
                pass
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''

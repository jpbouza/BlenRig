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

    #Armature for setting view
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

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
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

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
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

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
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

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
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

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
#Property for action to be performed after steps
def end_of_step_action(context):
    Hide_Lattices = ['LATTICE_HEAD', 'LATTICE_BROW', 'LATTICE_MOUTH', 'LATTICE_EYE_L', 'LATTICE_EYE_R', 'LATTICE_BODY']
    current_step = bpy.context.scene.blenrig_guide.guide_current_step
    if current_step == 'LATTICES_Adjust_Body' or current_step == 'LATTICES_Adjust_Head' or current_step == 'LATTICES_Adjust_Brow' or current_step == 'LATTICES_Adjust_Mouth' or current_step == 'LATTICES_Adjust_Eyes':
        #Unhide Lattices
        for ob in Hide_Lattices:
            try:
                bpy.data.objects[ob].hide_viewport = False
            except:
                pass
        blenrig_temp_unlink()
        bpy.context.scene.blenrig_guide.guide_current_step = ''

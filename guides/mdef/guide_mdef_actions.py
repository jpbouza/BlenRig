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

#### MDEF STEPS ####

def MDEF_Select_Body_Objects(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Select_Body_Objects'

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
    frame_bones(context, "head_str", "master")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

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

def MDEF_Binding_Check(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'MDEF_Binding_Check'

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
    frame_bones(context, "head_str", "master")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    #Select Head object
    try:
        bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_head_obj
    except:
        pass



def DT_Finish(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Finish'

    deselect_all_objects(context)

    # Hide MDefWeightsModel
    blenrig_temp_unlink()

    #Turn off Tranfer Shapekeys on Character's Objects
    try:
        bpy.context.scene.blenrig_guide.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 0.0
    except:
        pass
    try:
        bpy.context.scene.blenrig_guide.character_head_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 0.0
    except:
        pass

    #Add Deform Modifiers to Character's head
    bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_head_obj
    active = bpy.context.active_object

    bpy.ops.blenrig.add_head_modifiers()

    #Add Deform Modifiers to Character's hands
    bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_hands_obj
    active = bpy.context.active_object

    bpy.ops.blenrig.add_hands_modifiers()

    #Select Armature
    deselect_all_objects(context)
    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_fk", "master_torso")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

#### END OF STEP ACTIONS ####
#Property for action to be performed after steps
def end_of_step_action(context):
    current_step = bpy.context.scene.blenrig_guide.guide_current_step
    if current_step == 'MDEF_Edit_Mdef_Cage':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        blenrig_temp_unlink()
        bpy.context.scene.blenrig_guide.guide_current_step = ''

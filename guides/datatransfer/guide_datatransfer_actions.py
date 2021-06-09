import bpy
from .. utils import *

def reproportion_on(context):
    # 0. Make sure Armature is active and in Pose Mode.
    if context.mode != 'POSE':
        set_mode('OBJECT')
        set_active_object(context, operator.arm_obj)
        set_mode('POSE')

    # Set Armature to Reproportion mode
    set_reproportion_on(context)
    unhide_all_bones(context)


def reproportion_off(context):
    # 0. Make sure Armature is active and in Pose Mode.
    if context.mode != 'POSE':
        set_mode('OBJECT')
        set_active_object(context, operator.arm_obj)
        set_mode('POSE')

    # Set Armature to Reproportion mode
    set_reproportion_off(context)
    unhide_all_bones(context)

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

#### DATATRANSFER STEPS ####

def DT_Weight_Mesh_Shapekey_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Head'

    # #Select Armature
    # armature = bpy.context.scene.blenrig_guide.arm_obj
    # armature.select_set(state=True)
    # bpy.context.view_layer.objects.active = armature
    # if context.mode != 'POSE':
    #     set_mode('POSE')

    # # Adjust view to Bones.
    # frame_bones(context, "head_str", "neck_ctrl_4_str")

    deselect_all_objects(context)

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)

    for ob in mdef_weights_model_objects:
        set_active_object(context, ob)
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj = ob
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj.hide_viewport = False
        set_mode('EDIT')

    #Add and Edit Face Shapekey
    add_shapekey(context, 'Weights_Transfer_Head')

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

def DT_Weight_Mesh_Shapekey_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Hands'

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)

    for ob in mdef_weights_model_objects:
        set_active_object(context, ob)
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj = ob
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj.hide_viewport = False
        set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    add_shapekey(context, 'Weights_Transfer_Hands')

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

def DT_Select_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Select_Head'

    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "neck_1_fk")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Hide MDefWeightsModel
    blenrig_temp_unlink()

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

def DT_Edit_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Edit_Head'

    #SaveHead Object
    bpy.context.scene.blenrig_guide.character_head_obj = bpy.context.active_object

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)
    for ob in mdef_weights_model_objects:
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj = ob
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj.hide_viewport = False

    set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    add_shapekey(context, 'Weights_Transfer_Head')

    #Set to Local_View
    switch_out_local_view()

def DT_Select_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Select_Hands'

    bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False

    #Select Armature
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.select_set(state=True)
    bpy.context.view_layer.objects.active = armature
    if context.mode != 'POSE':
        set_mode('POSE')

    # Adjust view to Bones.
    frame_bones(context, "hand_fk_L", "hand_fk_R")

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Hide MDefWeightsModel
    blenrig_temp_unlink()

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

def DT_Edit_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Edit_Hands'

    #SaveHead Object
    bpy.context.scene.blenrig_guide.character_hands_obj = bpy.context.active_object

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)
    for ob in mdef_weights_model_objects:
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj = ob
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj.hide_viewport = False

    set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    add_shapekey(context, 'Weights_Transfer_Hands')

    #Set to Local_View
    switch_out_local_view()

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
    if current_step == 'DT_Weight_Mesh_Shapekey_Head':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        bpy.context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Weight_Mesh_Shapekey_Hands':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        bpy.context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Edit_Head':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False
        bpy.context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Edit_Hands':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False
        bpy.context.scene.blenrig_guide.guide_current_step = ''
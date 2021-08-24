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

#### DATATRANSFER STEPS ####

def DT_Weight_Mesh_Shapekey_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Head'

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
    basis_shapekey_fix(context)
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

    #Add and Edit Fingers Shapekey
    basis_shapekey_fix(context)
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

    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

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

    guide_props = bpy.context.scene.blenrig_guide
    armature =guide_props.arm_obj

    deselect_all_objects(context)

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)
    for ob in mdef_weights_model_objects:
        guide_props.mdef_weights_transfer_obj = ob
        guide_props.mdef_weights_transfer_obj.hide_viewport = False

    #Select Head Object
    set_active_object(context, guide_props.character_head_obj)

    #Add and Edit Head Shapekey
    basis_shapekey_fix(context)
    add_shapekey(context, 'Weights_Transfer_Head')
    set_active_shapekey('Weights_Transfer_Head')
    guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 1.0
    guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].mute = False
    set_mode('EDIT')

    #Set to Local_View
    switch_out_local_view()

    armature.hide_viewport = True

def DT_Select_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Select_Hands'

    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

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

    guide_props = bpy.context.scene.blenrig_guide
    armature =guide_props.arm_obj

    deselect_all_objects(context)

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)
    for ob in mdef_weights_model_objects:
        guide_props.mdef_weights_transfer_obj = ob
        guide_props.mdef_weights_transfer_obj.hide_viewport = False

    #Select Hands Object
    set_active_object(context, guide_props.character_hands_obj)

    set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    basis_shapekey_fix(context)
    add_shapekey(context, 'Weights_Transfer_Hands')
    set_active_shapekey('Weights_Transfer_Hands')
    guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 1.0
    guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].mute = False
    set_mode('EDIT')

    #Set to Local_View
    switch_out_local_view()

    armature.hide_viewport = True

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
    set_active_object(context, bpy.context.scene.blenrig_guide.character_head_obj)
    bpy.ops.blenrig.add_head_modifiers()

    #Add Deform Modifiers to Character's hands
    set_active_object(context, bpy.context.scene.blenrig_guide.character_hands_obj)
    bpy.ops.blenrig.add_hands_modifiers()

    #Select Armature
    deselect_all_objects(context)
    armature = bpy.context.scene.blenrig_guide.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_fk", "master_torso")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

#### END OF STEP ACTIONS ####
def datatransfer_end_generic(context):
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

    #Turn Layers off
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in off_layers:
        guide_props.arm_obj.data.layers[l] = False

    #Unlink Temp Collection
    blenrig_temp_unlink()

#Property for action to be performed after steps
def end_of_step_action(context):
    datatransfer_end_generic(context)
    guide_props = bpy.context.scene.blenrig_guide
    current_step = context.scene.blenrig_guide.guide_current_step
    if current_step == 'DT_Weight_Mesh_Shapekey_Head':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Weight_Mesh_Shapekey_Hands':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Edit_Head':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 0.0
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Edit_Hands':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        blenrig_temp_unlink()
        guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 0.0
        context.scene.blenrig_guide.guide_current_step = ''

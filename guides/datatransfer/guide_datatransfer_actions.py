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

def DT_Intro(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Intro'

def DT_Weight_Mesh_Shapekey_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Head'

    guide_props = bpy.context.scene.blenrig_guide
    head_weights_obj = guide_props.mdef_head_weights_transfer_obj

    deselect_all_objects(context)

    if head_weights_obj == None:
        # Show MDefHeadWeightsModel
        mdef_weights_model_objects = collect_mdef_head_weights_model()
        collect_mdef_head_weights_model()
        blenrig_temp_link(mdef_weights_model_objects)

        for ob in mdef_weights_model_objects:
            set_active_object(context, ob)
            head_weights_obj = ob
            head_weights_obj.hide_viewport = False
    else:
        blenrig_temp_link([head_weights_obj])
        head_weights_obj.hide_viewport = False
        set_active_object(context, head_weights_obj)

    #Add and Edit Face Shapekey
    if hasattr(head_weights_obj, 'data'):
        basis_shapekey_fix(context)
        add_shapekey(context, 'Weights_Transfer_Head')
        head_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 1.0
        head_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].mute = False

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

    #Turn Off modifiers for proper Editing
    if hasattr(head_weights_obj, 'modifiers'):
        for mod in head_weights_obj.modifiers:
            mod.show_in_editmode = False

    set_mode('EDIT')

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

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

    BlenRig_Empty(context)

    armature.hide_viewport = True

    deselect_all_objects(context)

    # Hide MDefHeadWeightsModel
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
    head_weights_obj = guide_props.mdef_head_weights_transfer_obj

    deselect_all_objects(context)

    if head_weights_obj == None:
        # Show MDefHeadWeightsModel
        mdef_weights_model_objects = collect_mdef_head_weights_model()
        collect_mdef_head_weights_model()
        blenrig_temp_link(mdef_weights_model_objects)

        for ob in mdef_weights_model_objects:
            set_active_object(context, ob)
            head_weights_obj = ob
            head_weights_obj.hide_viewport = False
    else:
        blenrig_temp_link([head_weights_obj])
        head_weights_obj.hide_viewport = False
        set_active_object(context, head_weights_obj)

    head_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 1.0
    head_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].mute = False

    #Select Head Object
    set_active_object(context, guide_props.character_head_obj)

    #Add and Edit Head Shapekey
    if hasattr(guide_props.character_head_obj, 'data'):
        basis_shapekey_fix(context)
        add_shapekey(context, 'Weights_Transfer_Head')
        set_active_shapekey('Weights_Transfer_Head')
        guide_props.character_head_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 1.0
        guide_props.character_head_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].mute = False

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

    deselect_all_objects(context)
    set_active_object(context, guide_props.character_head_obj)
    set_mode('EDIT')

    armature.hide_viewport = True

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

    #Turn Off modifiers for proper Editing
    if hasattr(head_weights_obj, 'modifiers'):
        for mod in head_weights_obj.modifiers:
            mod.show_in_editmode = False
    if hasattr(guide_props.character_head_obj, 'modifiers'):
        for mod in guide_props.character_head_obj.modifiers:
            mod.show_in_editmode = False

def DT_Test_Face(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Test_Face'

    guide_props = bpy.context.scene.blenrig_guide

    #Select Armature
    deselect_all_objects(context)
    armature = guide_props.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_fk", "head_stretch")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Bones
    bones = ['cheek_ctrl_L', 'cheek_ctrl_R', 'nose_frown_ctrl_L', 'nose_frown_ctrl_R', 'brow_ctrl_curve_L', 'brow_ctrl_in_L', 'brow_ctrl_out_L',
    'brow_ctrl_curve_R', 'brow_ctrl_in_R', 'brow_ctrl_out_R', 'eyelid_up_rim_ctrl_L', 'eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_low_rim_ctrl_L',
    'blink_ctrl_L', 'eyelid_up_rim_ctrl_R', 'eyelid_low_ctrl_R', 'eyelid_up_ctrl_R', 'eyelid_low_rim_ctrl_R', 'blink_ctrl_R', 'mouth_str_ctrl', 'mouth_ctrl',
    'mouth_up_ctrl', 'mouth_low_ctrl', 'chin_ctrl_mstr', 'lip_low_ctrl', 'lip_up_ctrl', 'mouth_mstr_ctrl', 'tongue_3_ik', 'mouth_corner_R', 'mouth_corner_L',
    'ear_R', 'ear_up_R', 'ear_low_R', 'ear_L', 'ear_up_L', 'ear_low_L', 'nose_ctrl']

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    deselect_all_objects(context)
    armature.hide_viewport = True

    # Hide MDefHeadWeightsModel
    blenrig_temp_unlink()

    #Select Character's Head
    try:
        set_active_object(context, guide_props.character_head_obj)
    except:
        pass

def DT_Weight_Mesh_Shapekey_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Hands'

    guide_props = bpy.context.scene.blenrig_guide
    hands_weights_obj = guide_props.mdef_hands_weights_transfer_obj

    deselect_all_objects(context)

    if hands_weights_obj == None:
        # Show MDefHandsWeightsModel
        mdef_weights_model_objects = collect_mdef_hands_weights_model()
        collect_mdef_hands_weights_model()
        blenrig_temp_link(mdef_weights_model_objects)

        for ob in mdef_weights_model_objects:
            set_active_object(context, ob)
            hands_weights_obj = ob
            hands_weights_obj.hide_viewport = False
            set_mode('EDIT')
    else:
        blenrig_temp_link([hands_weights_obj])
        hands_weights_obj.hide_viewport = False
        set_active_object(context, hands_weights_obj)

    #Add and Edit Fingers Shapekey
    if hasattr(hands_weights_obj, 'data'):
        basis_shapekey_fix(context)
        add_shapekey(context, 'Weights_Transfer_Hands')
        hands_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 1.0
        hands_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].mute = False

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

    #Turn Off modifiers for proper Editing
    if hasattr(hands_weights_obj, 'modifiers'):
        for mod in hands_weights_obj.modifiers:
            mod.show_in_editmode = False

    set_mode('EDIT')

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

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

    # Hide MDefHeadWeightsModel
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
    hands_weights_obj = guide_props.mdef_hands_weights_transfer_obj

    deselect_all_objects(context)

    if hands_weights_obj == None:
        # Show MDefHandsWeightsModel
        mdef_weights_model_objects = collect_mdef_hands_weights_model()
        collect_mdef_hands_weights_model()
        blenrig_temp_link(mdef_weights_model_objects)

        for ob in mdef_weights_model_objects:
            set_active_object(context, ob)
            hands_weights_obj = ob
            hands_weights_obj.hide_viewport = False
            set_mode('EDIT')
    else:
        blenrig_temp_link([hands_weights_obj])
        hands_weights_obj.hide_viewport = False
        set_active_object(context, hands_weights_obj)

    hands_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 1.0
    hands_weights_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].mute = False

    #Select Hands Object
    set_active_object(context, guide_props.character_hands_obj)

    #Add and Edit Fingers Shapekey
    if hasattr(guide_props.character_hands_obj, 'data'):
        basis_shapekey_fix(context)
        add_shapekey(context, 'Weights_Transfer_Hands')
        set_active_shapekey('Weights_Transfer_Hands')
        guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 1.0
        guide_props.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].mute = False
        set_mode('EDIT')

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

    deselect_all_objects(context)
    set_active_object(context, guide_props.character_head_obj)
    set_mode('EDIT')

    armature.hide_viewport = True

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

    #Turn Off modifiers for proper Editing
    if hasattr(hands_weights_obj, 'modifiers'):
        for mod in hands_weights_obj.modifiers:
            mod.show_in_editmode = False
    if hasattr(guide_props.character_hands_obj, 'modifiers'):
        for mod in guide_props.character_hands_obj.modifiers:
            mod.show_in_editmode = False

def DT_Test_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Test_Hands'

    guide_props = bpy.context.scene.blenrig_guide

    #Select Armature
    deselect_all_objects(context)
    armature = guide_props.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "hand_ik_ctrl_L", "hand_close_L")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Bones
    bones = ['hand_close_R', 'fing_lit_ctrl_R', 'fing_lit_2_R', 'fing_lit_3_R', 'fing_lit_4_R', 'fing_ring_ctrl_R', 'fing_ring_2_R', 'fing_ring_3_R', 'fing_ring_4_R',
    'fing_ind_ctrl_R', 'fing_ind_2_R', 'fing_ind_3_R', 'fing_ind_4_R', 'fing_mid_ctrl_R', 'fing_mid_2_R', 'fing_mid_3_R', 'fing_mid_4_R', 'fing_spread_R', 'fing_thumb_1_R',
    'fing_thumb_ctrl_R', 'fing_thumb_2_R', 'fing_thumb_3_R', 'hand_close_L', 'palm_bend_fk_ctrl_L', 'fing_lit_ctrl_L', 'fing_lit_2_L', 'fing_lit_3_L', 'fing_lit_4_L', 'fing_ring_ctrl_L',
    'fing_ring_2_L', 'fing_ring_3_L', 'fing_ring_4_L', 'fing_ind_ctrl_L', 'fing_ind_2_L', 'fing_ind_3_L', 'fing_ind_4_L', 'fing_mid_ctrl_L', 'fing_mid_2_L', 'fing_mid_3_L', 'fing_mid_4_L',
    'fing_spread_L', 'fing_thumb_1_L', 'fing_thumb_ctrl_L', 'fing_thumb_2_L', 'fing_thumb_3_L']
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    deselect_all_objects(context)
    armature.hide_viewport = True

    # Hide MDefHeadWeightsModel
    blenrig_temp_unlink()

    #Select Character's Hands
    try:
        set_active_object(context, guide_props.character_hands_obj)
    except:
        pass

def DT_Eyes(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Eyes'

    guide_props = bpy.context.scene.blenrig_guide

    #Select Armature
    deselect_all_objects(context)
    armature = guide_props.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_fk", "head_stretch")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Bones
    bones = ['look', 'look_L', 'look_R']

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    deselect_all_objects(context)
    armature.hide_viewport = True

    # Hide MDefHeadWeightsModel
    blenrig_temp_unlink()

    #Select Character's Head
    try:
        set_active_object(context, guide_props.character_head_obj)
    except:
        pass

def DT_Inner_Mouth(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Inner_Mouth'

    guide_props = bpy.context.scene.blenrig_guide

    #Select Armature
    deselect_all_objects(context)
    armature = guide_props.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "head_fk", "head_stretch")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    deselect_all_objects(context)
    armature.hide_viewport = True

    # Hide MDefHeadWeightsModel
    blenrig_temp_unlink()

    #Select Character's Head
    try:
        set_active_object(context, guide_props.character_head_obj)
    except:
        pass

def DT_Clean_Symmetry(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Clean_Symmetry'

    guide_props = bpy.context.scene.blenrig_guide

    #Select Armature
    deselect_all_objects(context)
    armature = guide_props.arm_obj
    armature.hide_viewport = False

    #Select Armature
    go_blenrig_pose_mode(context)

    # Adjust view to Bones.
    frame_bones(context, "master", "head_stretch")

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    deselect_all_objects(context)
    armature.hide_viewport = True

    # Hide MDefHeadWeightsModel
    blenrig_temp_unlink()

    #Select Character's Head
    try:
        set_active_object(context, guide_props.character_head_obj)
    except:
        pass

def DT_Finish(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Finish'

    deselect_all_objects(context)

    # Hide MDefHeadWeightsModel
    blenrig_temp_unlink()

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

    #Set to Local_View
    switch_out_local_view()

    #Set back Object Mode
    if context.mode != 'OBJECT':
        set_mode('OBJECT')

    #Select Armature
    if hasattr(context, 'active_object') and hasattr(context.active_object, 'type'):
        if context.active_object.type == 'MESH':
            deselect_all_objects(context)

    #Turn off Tranfer Shapekeys on All Objects
    try:
        bpy.context.scene.blenrig_guide.character_hands_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 0.0
    except:
        pass
    try:
        bpy.context.scene.blenrig_guide.character_head_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 0.0
    except:
        pass
    try:
        bpy.context.scene.blenrig_guide.mdef_hands_weights_transfer_obj.data.shape_keys.key_blocks['Weights_Transfer_Hands'].value = 0.0
    except:
        pass
    try:
        bpy.context.scene.blenrig_guide.mdef_head_weights_transfer_obj.data.shape_keys.key_blocks['Weights_Transfer_Head'].value = 0.0
    except:
        pass

    show_armature(context)

    #Ensure POSE Mode
    go_blenrig_pose_mode(context)

    unhide_all_bones(context)
    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Reset Transforms
    reset_all_bones_transforms()

    #Turn Layers off
    on_layers = [0, 1, 3, 4, 5, 6, 7, 9, 16, 17, 18, 20, 22, 23]
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in on_layers:
        context.object.data.layers[l] = True
    for l in off_layers:
        context.object.data.layers[l] = False

    #Unlink Temp Collection
    blenrig_temp_unlink()

#Property for action to be performed after steps
def end_of_step_action(context):
    datatransfer_end_generic(context)
    guide_props = bpy.context.scene.blenrig_guide
    head_weights_obj = guide_props.mdef_head_weights_transfer_obj
    hands_weights_obj = guide_props.mdef_hands_weights_transfer_obj
    current_step = context.scene.blenrig_guide.guide_current_step
    if current_step == 'DT_Weight_Mesh_Shapekey_Head':
        #Turn Off modifiers for proper Editing
        if hasattr(head_weights_obj, 'modifiers'):
            for mod in head_weights_obj.modifiers:
                mod.show_in_editmode = True
    if current_step == 'DT_Edit_Head':
        #Turn Off modifiers for proper Editing
        if hasattr(head_weights_obj, 'modifiers'):
            for mod in head_weights_obj.modifiers:
                mod.show_in_editmode = True
        if hasattr(guide_props.character_head_obj, 'modifiers'):
            for mod in guide_props.character_head_obj.modifiers:
                mod.show_in_editmode = True
    if current_step == 'DT_Weight_Mesh_Shapekey_Hands':
        #Turn Off modifiers for proper Editing
        if hasattr(hands_weights_obj, 'modifiers'):
            for mod in hands_weights_obj.modifiers:
                mod.show_in_editmode = True
    if current_step == 'DT_Edit_Hands':
        #Turn Off modifiers for proper Editing
        if hasattr(hands_weights_obj, 'modifiers'):
            for mod in hands_weights_obj.modifiers:
                mod.show_in_editmode = True
        if hasattr(guide_props.character_hands_obj, 'modifiers'):
            for mod in guide_props.character_hands_obj.modifiers:
                mod.show_in_editmode = True
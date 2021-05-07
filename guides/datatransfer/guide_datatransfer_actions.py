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

def DT_Weight_Mesh_Shapekey_Face(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Face'

    deselect_all_objects(context)

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)

    context.scene.blenrig_guide.mdef_weights_obj = bpy.context.object

    for ob in mdef_weights_model_objects:
        set_active_object(context, ob)
        bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj = ob
        set_mode('EDIT')

    #Add and Edit Face Shapekey
    add_shapekey(context, 'Weights_Transfer_Face')

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

def DT_Weight_Mesh_Shapekey_Fingers(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Weight_Mesh_Shapekey_Fingers'

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)

    for ob in mdef_weights_model_objects:
        set_active_object(context, ob)
        set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    add_shapekey(context, 'Weights_Transfer_Fingers')

    #Set to Local_View
    switch_out_local_view()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()

def DT_Select_Face(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Select_Face'

    deselect_all_objects(context)

    # Hide MDefWeightsModel
    blenrig_temp_unlink()

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

def DT_Edit_Face(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Edit_Face'

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)

    set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    add_shapekey(context, 'Weights_Transfer_Face')

    #Set to Local_View
    switch_out_local_view()

def DT_Select_Fingers(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Select_Fingers'

    deselect_all_objects(context)

    # Hide MDefWeightsModel
    blenrig_temp_unlink()

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

def DT_Edit_Fingers(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'DT_Edit_Fingers'

    # Show MDefWeightsModel
    mdef_weights_model_objects = collect_mdef_weights_model()
    collect_mdef_weights_model()
    blenrig_temp_link(mdef_weights_model_objects)

    set_mode('EDIT')

    #Add and Edit Fingers Shapekey
    add_shapekey(context, 'Weights_Transfer_Fingers')

    #Set to Local_View
    switch_out_local_view()

#### END OF STEP ACTIONS ####
#Property for action to be performed after steps
def end_of_step_action(context):
    current_step = bpy.context.scene.blenrig_guide.guide_current_step
    if current_step == 'DT_Weight_Mesh_Shapekey_Face':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        bpy.context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Weight_Mesh_Shapekey_Fingers':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        bpy.context.scene.blenrig_guide.guide_current_step = ''
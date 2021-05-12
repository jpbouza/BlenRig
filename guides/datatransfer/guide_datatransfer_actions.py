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

def check_mod_type(mod_type):
    active = bpy.context.active_object
    if hasattr(active, 'modifiers'):
        for mod in active.modifiers:
            if hasattr(mod, 'type'):
                if mod.type == mod_type:
                    return True

def check_mod_type_name(mod_type, mod_name):
    active = bpy.context.active_object
    if hasattr(active, 'modifiers'):
        for mod in active.modifiers:
            if hasattr(mod, 'type'):
                if mod.type == mod_type:
                    if mod.name == mod_name:
                        return True

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

    #Armature
    if check_mod_type('ARMATURE'):
        pass
    else:
        mod = active.modifiers.new(name= "Armature",type= 'ARMATURE')
        # set modifier properties
        mod.object = bpy.context.scene.blenrig_guide.arm_obj
        mod.use_deform_preserve_volume = True
        mod.vertex_group = 'no_mdef'
        mod.show_expanded = True
        mod.show_in_editmode = True
        mod.show_on_cage = True
    #Mesh Deform
    if check_mod_type('MESH_DEFORM'):
        pass
    else:
        mod = active.modifiers.new(name= "MeshDeform",type= 'MESH_DEFORM')
        # set modifier properties
        mod.object = bpy.context.scene.blenrig_guide.mdef_cage_obj
        mod.invert_vertex_group = True
        mod.vertex_group = 'no_mdef'
        mod.show_expanded = True
        mod.show_in_editmode = True
        mod.show_on_cage = True

    #Corrective Smooth
    if check_mod_type('CORRECTIVE_SMOOTH'):
        pass
    else:
        mod = active.modifiers.new(name= "CorrectiveSmooth",type= 'CORRECTIVE_SMOOTH')
        # set modifier properties
        mod.smooth_type = 'SIMPLE'
        mod.rest_source = 'ORCO'
        mod.vertex_group = 'corrective_smooth'
        mod.show_expanded = False

    #Cheek Puffs
    if check_mod_type_name('WARP', 'Cheek_Puff_L'):
        pass
    else:
        mod = active.modifiers.new(name= "Cheek_Puff_L",type= 'WARP')
        # set modifier properties
        mod.object_from = bpy.context.scene.blenrig_guide.arm_obj
        mod.bone_from = 'cheek_puff_mstr_L'
        mod.object_to = bpy.context.scene.blenrig_guide.arm_obj
        mod.bone_to = 'cheek_puff_ctrl_L'
        mod.vertex_group = 'no_mdef'
        mod.falloff_radius = bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_puff_ctrl_L"]["PUFF_RADIUS_L"]
        mod.show_expanded = False

    if check_mod_type_name('WARP', 'Cheek_Puff_R'):
        pass
    else:
        mod = active.modifiers.new(name= "Cheek_Puff_R",type= 'WARP')
        # set modifier properties
        mod.object_from = bpy.context.scene.blenrig_guide.arm_obj
        mod.bone_from = 'cheek_puff_mstr_R'
        mod.object_to = bpy.context.scene.blenrig_guide.arm_obj
        mod.bone_to = 'cheek_puff_ctrl_R'
        mod.vertex_group = 'no_mdef'
        mod.falloff_radius = bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_puff_ctrl_R"]["PUFF_RADIUS_R"]
        mod.show_expanded = False

    #Lattices
    if check_mod_type_name('LATTICE', 'LATTICE_EYE_L'):
        pass
    else:
        mod = active.modifiers.new(name= "LATTICE_EYE_L",type= 'LATTICE')
        # set modifier properties
        for ob in bpy.data.objects:
            if ob.type == 'LATTICE':
                if 'LATTICE_EYE_L' in ob.name:
                    if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                        mod.object = ob
        mod.vertex_group = 'lattice_eye_L'
        mod.show_expanded = False

    if check_mod_type_name('LATTICE', 'LATTICE_EYE_R'):
        pass
    else:
        mod = active.modifiers.new(name= "LATTICE_EYE_R",type= 'LATTICE')
        # set modifier properties
        for ob in bpy.data.objects:
            if ob.type == 'LATTICE':
                if 'LATTICE_EYE_R' in ob.name:
                    if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                        mod.object = ob
        mod.vertex_group = 'lattice_eye_R'
        mod.show_expanded = False

    if check_mod_type_name('LATTICE', 'LATTICE_BROW'):
        pass
    else:
        mod = active.modifiers.new(name= "LATTICE_BROW",type= 'LATTICE')
        # set modifier properties
        for ob in bpy.data.objects:
            if ob.type == 'LATTICE':
                if 'LATTICE_BROW' in ob.name:
                    if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                        mod.object = ob
        mod.vertex_group = 'lattice_brow'
        mod.show_expanded = False

    if check_mod_type_name('LATTICE', 'LATTICE_MOUTH'):
        pass
    else:
        mod = active.modifiers.new(name= "LATTICE_MOUTH",type= 'LATTICE')
        # set modifier properties
        for ob in bpy.data.objects:
            if ob.type == 'LATTICE':
                if 'LATTICE_MOUTH' in ob.name:
                    if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                        mod.object = ob
        mod.vertex_group = 'lattice_mouth'
        mod.show_expanded = False

    if check_mod_type_name('LATTICE', 'LATTICE_HEAD'):
        pass
    else:
        mod = active.modifiers.new(name= "LATTICE_HEAD",type= 'LATTICE')
        # set modifier properties
        for ob in bpy.data.objects:
            if ob.type == 'LATTICE':
                if 'LATTICE_HEAD' in ob.name:
                    if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                        mod.object = ob
        mod.vertex_group = 'lattice_head'
        mod.show_expanded = False

    #Subsurf
    subsurf_mods = [mod for mod in active.modifiers if mod.type == 'SUBSURF']
    if subsurf_mods:
        active.modifiers.remove(subsurf_mods[-1])
    mod = active.modifiers.new(name= "Subdivision",type= 'SUBSURF')
    # set modifier properties
    mod.subdivision_type = 'CATMULL_CLARK'
    mod.levels = 0
    mod.render_levels = 3
    mod.show_expanded = True

    #Add Drivers
    #Delete Drivers if present
    if hasattr(active, 'modifiers') and hasattr(active.modifiers, 'data') and hasattr(active.modifiers.data, 'animation_data') and hasattr(active.modifiers.data.animation_data, 'drivers'):
        fcurves = active.modifiers.data.animation_data.drivers
        for fc in fcurves:
            if fc.data_path == 'modifiers["Cheek_Puff_L"].falloff_radius':
                fcurves.remove(fcurves[0])
            if fc.data_path == 'modifiers["Cheek_Puff_R"].falloff_radius':
                fcurves.remove(fcurves[0])
    #Cheek_Puff_L
    active_driver = add_drivers(active.modifiers["Cheek_Puff_L"], 'falloff_radius', 0, 'no_array', 'CONSTANT', False, False, False, '1.000', 'MAX')
    add_vars(active_driver, 'var', 'SINGLE_PROP', bpy.context.scene.blenrig_guide.arm_obj, 'cheek_puff_ctrl_L', 'pose.bones["cheek_puff_ctrl_L"]["PUFF_RADIUS_L"]', 'WORLD_SPACE', 'LOC_X', 'AUTO')
    add_mod_generator(active_driver, 'GENERATOR', 0.0, 0.0, 0.0, 0.0, 'POLYNOMIAL', False, 1, False, False, False, 0.0, 1.0)
    #Cheek_Puff_R
    active_driver = add_drivers(active.modifiers["Cheek_Puff_R"], 'falloff_radius', 0, 'no_array', 'CONSTANT', False, False, False, '1.000', 'MAX')
    add_vars(active_driver, 'var', 'SINGLE_PROP', bpy.context.scene.blenrig_guide.arm_obj, 'cheek_puff_ctrl_R', 'pose.bones["cheek_puff_ctrl_R"]["PUFF_RADIUS_R"]', 'WORLD_SPACE', 'LOC_X', 'AUTO')
    add_mod_generator(active_driver, 'GENERATOR', 0.0, 0.0, 0.0, 0.0, 'POLYNOMIAL', False, 1, False, False, False, 0.0, 1.0)

    #Add Deform Modifiers to Character's hands
    bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_hands_obj
    active = bpy.context.active_object

    #Armature
    if check_mod_type('ARMATURE'):
        pass
    else:
        mod = active.modifiers.new(name= "Armature",type= 'ARMATURE')
        # set modifier properties
        mod.object = bpy.context.scene.blenrig_guide.arm_obj
        mod.use_deform_preserve_volume = True
        mod.vertex_group = 'no_mdef'
        mod.show_expanded = True
        mod.show_in_editmode = True
        mod.show_on_cage = True
    #Mesh Deform
    if check_mod_type('MESH_DEFORM'):
        pass
    else:
        mod = active.modifiers.new(name= "MeshDeform",type= 'MESH_DEFORM')
        # set modifier properties
        mod.object = bpy.context.scene.blenrig_guide.mdef_cage_obj
        mod.invert_vertex_group = True
        mod.vertex_group = 'no_mdef'
        mod.show_expanded = True
        mod.show_in_editmode = True
        mod.show_on_cage = True

    #Corrective Smooth
    if check_mod_type('CORRECTIVE_SMOOTH'):
        pass
    else:
        mod = active.modifiers.new(name= "CorrectiveSmooth",type= 'CORRECTIVE_SMOOTH')
        # set modifier properties
        mod.smooth_type = 'SIMPLE'
        mod.rest_source = 'ORCO'
        mod.vertex_group = 'corrective_smooth'
        mod.show_expanded = False

    #Subsurf
    subsurf_mods = [mod for mod in active.modifiers if mod.type == 'SUBSURF']
    if subsurf_mods:
        active.modifiers.remove(subsurf_mods[-1])
    mod = active.modifiers.new(name= "Subdivision",type= 'SUBSURF')
    # set modifier properties
    mod.subdivision_type = 'CATMULL_CLARK'
    mod.levels = 0
    mod.render_levels = 3
    mod.show_expanded = True

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
        bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False
        bpy.context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'DT_Edit_Hands':
        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')
        #Switch Local_View off
        switch_out_local_view()
        bpy.context.scene.blenrig_guide.arm_obj.hide_viewport = False
        bpy.context.scene.blenrig_guide.guide_current_step = ''
import bpy

########### Update 1.05 ###########

#### Drivers update ####

def biped_update_1005_drivers(self, context):        
    arm = bpy.context.active_object
    arm_data = arm.data

    driver_data_path = []
    driver_array_index = []

    # Generic Driver add function
    def add_drivers(d_data_path, d_array_index, array_check, d_extrapolation, d_hide, d_lock, d_mute, d_expression, d_show_debug_info, d_type):
        driver_data_path[:] = []
        driver_array_index[:] = []
        if array_check == 'no_array':                 
            fcurve = arm.driver_add(d_data_path)  
        if array_check == 'array':               
            fcurve = arm.driver_add(d_data_path, d_array_index)                
        fcurve.extrapolation = d_extrapolation
        fcurve.hide = d_hide
        fcurve.lock = d_lock
        fcurve.mute = d_mute
        fcurve.driver.expression = d_expression
        fcurve.driver.show_debug_info = d_show_debug_info
        fcurve.driver.type = d_type
        for m in fcurve.modifiers:
            fcurve.modifiers.remove(m)
        driver_data_path.append(fcurve.data_path)
        driver_array_index.append(fcurve.array_index)

    # Generic Variable add function        
    def add_vars(v_name, v_type, t_id_type, t_id, t_bone_target, t_data_path, t_transform_space, t_transform_type):
        for d in arm.animation_data.drivers:  
            if d.data_path == driver_data_path[0]:
                if d.array_index == driver_array_index[0]:
                    var = d.driver.variables.new()
                    var.name = v_name
                    var.type = v_type
                    target = var.targets[0]
                    target.id_type = t_id_type                
                    if 'Armature' in t_id:
                        target.id = arm_data
                    if 'Object' in t_id:
                        target.id = arm       
                    target.bone_target = t_bone_target
                    target.data_path = t_data_path
                    target.transform_space = t_transform_space
                    target.transform_type = t_transform_type                  

    # Generic Modifier add function    
    def add_generator(m_type, m_blend_in, m_blend_out, m_frame_start, m_frame_end, m_mode, m_mute, m_poly_order, m_use_additive, m_use_influence, m_use_restricted_range, m_co_0, m_co_1):
        for d in arm.animation_data.drivers:  
            if d.data_path == driver_data_path[0]:
                if d.array_index == driver_array_index[0]:   
                    mod = d.modifiers.new(m_type)
                    mod.blend_in = m_blend_in
                    mod.blend_out = m_blend_out
                    mod.frame_start = m_frame_start
                    mod.frame_end = m_frame_end
                    mod.mode = m_mode
                    mod.mute = m_mute
                    mod.poly_order = m_poly_order
                    mod.use_additive = m_use_additive
                    mod.use_influence = m_use_influence
                    mod.use_restricted_range = m_use_restricted_range
                    mod.coefficients[0] = m_co_0
                    mod.coefficients[1] = m_co_1     

    # Check for existing drivers on targets
    for d in arm.animation_data.drivers:  
        if d.data_path == 'pose.bones["hand_ik_shoulder_L"].constraints["Copy Location"].influence':
            arm.driver_remove(d.data_path)
        if d.data_path == 'pose.bones["hand_ik_shoulder_R"].constraints["Copy Location"].influence':
            arm.driver_remove(d.data_path)     
    # Add drivers
    add_drivers('pose.bones["hand_ik_shoulder_L"].constraints["Copy Location"].influence', 0, 'no_array', 'CONSTANT', False, False, False, '', False, 'MAX')
    add_vars('var_1', 'SINGLE_PROP', 'OBJECT', '<bpy_struct, Object("biped_blenrig")>', 'torso ik', 'pose.bones["properties_arm_L"].["ik_arm_L"]', 'WORLD_SPACE', 'LOC_X')
    add_generator('GENERATOR', 0.0, 0.0, 0.0, 0.0, 'POLYNOMIAL', False, 1, False, False, False, 1.0, -1.0)
    add_drivers('pose.bones["hand_ik_shoulder_R"].constraints["Copy Location"].influence', 0, 'no_array', 'CONSTANT', False, False, False, '', False, 'MAX')
    add_vars('var_1', 'SINGLE_PROP', 'OBJECT', '<bpy_struct, Object("biped_blenrig")>', 'torso ik', 'pose.bones["properties_arm_R"].["ik_arm_R"]', 'WORLD_SPACE', 'LOC_X')
    add_generator('GENERATOR', 0.0, 0.0, 0.0, 0.0, 'POLYNOMIAL', False, 1, False, False, False, 1.0, -1.0)

#### Remove nnecessary locks ####  

def biped_update_1005_locks(self, context):
    arm = bpy.context.active_object
    arm_data = arm.data    
    for b in arm.pose.bones:
        bone_list = ['forearm_fk_L', 'forearm_fk_R', 'shin_fk_L', 'shin_fk_R', 'lattice_eye_L', 'lattice_eye_R']
        if b.name in bone_list:
            b.lock_rotation[:] = (False, False, False) 
            b.lock_location[:] = (False, False, False) 
            b.lock_scale[:] = (False, False, False)                 

#### Move bones to layers ####  

def biped_update_1005_bone_layers(self, context):
    # Generic layer assigner
    def set_layers(N, L):
        pbones = bpy.context.active_object.pose.bones
        for b in pbones:
            layers =  L
            if b.name == N: 
                b.bone.layers = [(x in layers) for x in range(32)]

    # Changes
    set_layers('lattice_eye_R', [7, 25, 26])     
    set_layers('lattice_eye_L', [7, 25, 26])    
    set_layers('mouth_mstr_low', [5, 25, 28])    
    set_layers('mouth_mstr_up', [5, 25, 28])            

#### Bone Groups ####      

def biped_update_1005_bone_groups(self, context):
    # New Groups
    bgroups = bpy.context.object.pose.bone_groups    

    new_group = bgroups.new('B-BONE_MECH')
    new_group.color_set = 'THEME09'

    # Bone Asignment 
    arm = bpy.context.active_object
    pbones = arm.pose.bones

    # Get Group index

    TOON_L_index = []
    TOON_R_index = []
    BBONE_MECH_index = []

    for i in range(len(arm.pose.bone_groups)):
        g = arm.pose.bone_groups[i]
        if g.name == 'TOON_L':
            TOON_L_index.append(i)
        if g.name == 'TOON_R':
            TOON_R_index.append(i)
        if g.name == 'B-BONE_MECH':
            BBONE_MECH_index.append(i)                
    #print (TOON_L_index, TOON_R_index, BBONE_MECH_index)

    # Assign Groups

    for b in pbones:
        TOON_L_bones = ['lattice_eye_L']
        TOON_R_bones = ['lattice_eye_R']    
        BBONE_MECH_bones = ['spine_1_def_bbone', 'brow_low_1_bezier_out_L', 'brow_low_1_bbone_out_L', 'brow_up_1_bezier_out_L', 'brow_up_1_bbone_out_L', 'brow_low_1_bezier_out_R', 'brow_low_1_bbone_out_R', 'brow_up_1_bezier_out_R', 'brow_up_1_bbone_out_R', 'brow_low_3_bezier_out_L', 'brow_low_3_bbone_out_L', 'brow_up_3_bezier_out_L', 'brow_up_3_bbone_out_L', 'brow_1_bezier_in_mstr_L', 'brow_1_bezier_in_L', 'brow_1_bbone_in_L', 'brow_3_bezier_out_mstr_L', 'brow_3_bezier_out_L', 'brow_2_bezier_out_mstr_L', 'brow_2_bezier_out_L', 'brow_low_2_bezier_out_L', 'brow_low_2_bbone_out_L', 'brow_up_2_bezier_out_L', 'brow_up_2_bbone_out_L', 'brow_2_bezier_in_mstr_L', 'brow_2_bezier_in_L', 'brow_2_bbone_in_L', 'brow_2_bbone_out_L', 'brow_low_4_bezier_out_L', 'brow_low_4_bbone_out_L', 'brow_up_4_bezier_out_L', 'brow_up_4_bbone_out_L', 'brow_3_bezier_in_L', 'brow_3_bbone_in_L', 'brow_3_bbone_out_L', 'lip_low_1_bezier_in_mstr_R', 'lip_low_1_bezier_in_R', 'lip_low_1_bbone_in_R', 'lip_low_2_bezier_in_mstr_L', 'lip_low_2_bezier_in_L', 'lip_low_2_bbone_in_L', 'lip_low_1_bezier_out_mstr_L', 'lip_low_1_bezier_out_L', 'lip_low_3_bezier_in_mstr_L', 'lip_low_3_bezier_in_L', 'lip_low_3_bbone_in_L', 'lip_low_2_bezier_out_mstr_L', 'lip_low_2_bezier_out_L', 'lip_low_4_bezier_in_mstr_L', 'lip_low_4_bezier_in_L', 'lip_low_4_bbone_in_L', 'lip_low_2_bbone_out_L', 'lip_up_1_bezier_in_mstr_R', 'lip_up_1_bezier_in_R', 'lip_up_1_bbone_in_R', 'lip_up_2_bezier_in_mstr_L', 'lip_up_2_bezier_in_L', 'lip_up_2_bbone_in_L', 'lip_up_1_bezier_out_mstr_L', 'lip_up_3_bezier_in_mstr_L', 'lip_up_3_bezier_in_L', 'lip_up_3_bbone_in_L', 'lip_up_1_bezier_out_L', 'lip_up_4_bezier_in_mstr_L', 'lip_up_4_bezier_in_L', 'lip_up_4_bbone_in_L', 'lip_up_2_bezier_out_mstr_L', 'lip_up_2_bezier_out_L', 'lip_low_3_bezier_out_mstr_L', 'lip_low_3_bezier_out_L', 'lip_low_3_bbone_out_L', 'lip_low_4_bbone_out_L', 'lip_up_3_bezier_out_mstr_L', 'lip_up_3_bezier_out_L', 'brow_low_3_bezier_out_R', 'brow_low_3_bbone_out_R', 'brow_up_3_bezier_out_R', 'brow_up_3_bbone_out_R', 'brow_1_bezier_in_mstr_R', 'brow_1_bezier_in_R', 'brow_1_bbone_in_R', 'brow_3_bezier_out_mstr_R', 'brow_3_bezier_out_R', 'brow_2_bezier_out_mstr_R', 'brow_2_bezier_out_R', 'brow_low_2_bezier_out_R', 'brow_low_2_bbone_out_R', 'brow_up_2_bezier_out_R', 'brow_up_2_bbone_out_R', 'brow_2_bezier_in_mstr_R', 'brow_2_bezier_in_R', 'brow_2_bbone_in_R', 'brow_2_bbone_out_R', 'brow_low_4_bezier_out_R', 'brow_low_4_bbone_out_R', 'brow_up_4_bezier_out_R', 'brow_up_4_bbone_out_R', 'brow_3_bezier_in_R', 'brow_3_bbone_in_R', 'brow_3_bbone_out_R', 'lip_low_1_bezier_in_mstr_L', 'lip_low_2_bezier_in_mstr_R', 'lip_low_2_bezier_in_R', 'lip_low_2_bbone_in_R', 'lip_low_1_bezier_out_mstr_R', 'lip_low_1_bezier_out_R', 'lip_low_3_bezier_in_mstr_R', 'lip_low_3_bezier_in_R', 'lip_low_3_bbone_in_R', 'lip_low_1_bezier_in_L', 'lip_low_1_bbone_in_L', 'lip_low_1_bbone_out_L', 'lip_low_1_bbone_out_R', 'lip_low_2_bezier_out_mstr_R', 'lip_low_2_bezier_out_R', 'lip_low_4_bezier_in_mstr_R', 'lip_low_4_bezier_in_R', 'lip_low_4_bbone_in_R', 'lip_low_2_bbone_out_R', 'lip_up_1_bezier_out_mstr_R', 'lip_up_1_bezier_out_R', 'lip_up_3_bezier_in_mstr_R', 'lip_up_3_bezier_in_R', 'lip_up_3_bbone_in_R', 'lip_up_2_bezier_in_mstr_R', 'lip_up_2_bezier_in_R', 'lip_up_2_bbone_in_R', 'lip_up_1_bezier_in_mstr_L', 'lip_up_1_bezier_in_L', 'lip_up_1_bbone_in_L', 'lip_up_2_bezier_out_mstr_R', 'lip_up_2_bezier_out_R', 'lip_up_4_bezier_in_mstr_R', 'lip_up_4_bezier_in_R', 'lip_up_4_bbone_in_R', 'lip_low_3_bezier_out_mstr_R', 'lip_low_3_bezier_out_R', 'lip_low_3_bbone_out_R', 'lip_low_4_bbone_out_R', 'lip_up_3_bezier_out_mstr_R', 'lip_up_3_bezier_out_R', 'lip_up_1_bbone_out_L', 'lip_up_2_bbone_out_L', 'lip_up_3_bbone_out_L', 'lip_up_4_bbone_out_L', 'lip_up_1_bbone_out_R', 'lip_up_2_bbone_out_R', 'lip_up_3_bbone_out_R', 'lip_up_4_bbone_out_R', 'pelvis_def_bbone', 'forearm_twist_bezier_out_mstr_R', 'forearm_twist_bezier_out_R', 'arm_def_bezier_in_R', 'arm_def_bbone_in_R', 'forearm_def_bezier_out_mstr_R', 'forearm_def_bezier_out_R', 'forearm_def_bezier_out_rot_R', 'forearm_twist_bezier_in_mstr_R', 'forearm_twist_bezier_in_R', 'forearm_twist_bbone_in_R', 'forearm_twist_bbone_out_R', 'forearm_no_twist_bezier_in_mstr_R', 'forearm_no_twist_bezier_in_R', 'forearm_no_twist_bbone_in_R', 'arm_def_bezier_out_mstr_R', 'arm_def_bezier_out_R', 'arm_twist_bezier_in_mstr_R', 'arm_twist_bezier_in_R', 'arm_def_bbone_out_R', 'arm_twist_bbone_in_R', 'arm_twist_curved_R', 'arm_twist_bezier_out_mstr_R', 'arm_twist_bezier_out_R', 'arm_twist_bbone_out_rot_R', 'arm_twist_bbone_out_R', 'forearm_def_curved_R', 'forearm_def_bezier_in_mstr_R', 'forearm_def_bezier_in_R', 'forearm_def_bbone_in_R', 'forearm_def_bbone_out_R', 'forearm_def_no_twist_bbone_in_R', 'forearm_def_bbone_out_no_twist_R', 'forearm_twist_bezier_out_mstr_L', 'forearm_twist_bezier_out_L', 'arm_twist_bezier_in_mstr_L', 'arm_twist_bezier_in_L', 'arm_def_bezier_out_mstr_L', 'arm_def_bezier_out_L', 'forearm_def_curved_L', 'forearm_def_bezier_in_mstr_L', 'forearm_def_bezier_in_L', 'forearm_def_bbone_in_L', 'forearm_def_no_twist_bbone_in_L', 'forearm_def_bezier_out_mstr_L', 'forearm_def_bezier_out_L', 'forearm_def_bezier_out_rot_L', 'forearm_twist_bezier_in_mstr_L', 'forearm_twist_bezier_in_L', 'forearm_twist_bbone_in_L', 'forearm_twist_bbone_out_L', 'forearm_no_twist_bezier_in_mstr_L', 'forearm_no_twist_bezier_in_L', 'forearm_no_twist_bbone_in_L', 'forearm_def_bbone_out_L', 'forearm_def_bbone_out_no_twist_L', 'arm_twist_bbone_in_L', 'arm_twist_curved_L', 'arm_twist_bezier_out_mstr_L', 'arm_twist_bezier_out_L', 'arm_twist_bbone_out_rot_L', 'arm_twist_bbone_out_L', 'arm_def_bezier_in_L', 'arm_def_bbone_in_L', 'arm_def_bbone_out_L', 'shin_twist_bezier_out_mstr_R', 'thigh_def_bezier_in_R', 'thigh_def_bbone_in_R', 'thigh_def_bezier_out_mstr_R', 'thigh_def_bezier_out_R', 'thigh_twist_bezier_in_mstr_R', 'thigh_twist_bezier_in_R', 'thigh_twist_bbone_in_R', 'thigh_def_bbone_out_R', 'shin_twist_bezier_out_R', 'shin_def_curved_R', 'shin_def_bezier_in_mstr_R', 'shin_def_bezier_in_R', 'shin_def_bbone_in_R', 'shin_def_no_twist_bbone_in_R', 'shin_def_bezier_out_mstr_R', 'shin_def_bezier_out_R', 'shin_def_bezier_out_rot_R', 'shin_twist_bezier_in_mstr_R', 'shin_twist_bezier_in_R', 'shin_twist_bbone_in_R', 'shin_twist_bbone_out_R', 'shin_no_twist_bezier_in_mstr_R', 'shin_no_twist_bezier_in_R', 'shin_no_twist_bbone_in_R', 'shin_def_bbone_out_R', 'shin_def_no_twist_bbone_out_R', 'thigh_twist_curved_R', 'thigh_twist_bezier_out_mstr_R', 'thigh_twist_bezier_out_R', 'thigh_twist_bbone_out_rot_R', 'thigh_twist_bbone_out_R', 'shin_twist_bezier_out_mstr_L', 'thigh_def_bezier_in_L', 'thigh_def_bbone_in_L', 'thigh_def_bezier_out_mstr_L', 'thigh_def_bezier_out_L', 'thigh_twist_bezier_in_mstr_L', 'thigh_twist_bezier_in_L', 'thigh_twist_bbone_in_L', 'thigh_def_bbone_out_L', 'shin_twist_bezier_out_L', 'shin_def_curved_L', 'shin_def_bezier_in_mstr_L', 'shin_def_bezier_in_L', 'shin_def_bbone_in_L', 'shin_def_no_twist_bbone_in_L', 'shin_def_bezier_out_mstr_L', 'shin_def_bezier_out_L', 'shin_def_bezier_out_rot_L', 'shin_twist_bezier_in_mstr_L', 'shin_twist_bezier_in_L', 'shin_twist_bbone_in_L', 'shin_twist_bbone_out_L', 'shin_no_twist_bezier_in_mstr_L', 'shin_no_twist_bezier_in_L', 'shin_no_twist_bbone_in_L', 'shin_def_bbone_out_L', 'shin_def_no_twist_bbone_out_L', 'thigh_twist_curved_L', 'thigh_twist_bezier_out_mstr_L', 'thigh_twist_bezier_out_L', 'thigh_twist_bbone_out_rot_L', 'thigh_twist_bbone_out_L', 'eyelid_up_vert_def_2_bbone_out_L', 'eyelid_up_3_bezier_in_mstr_L', 'eyelid_up_3_bezier_in_L', 'eyelid_up_3_bbone_in_L', 'eyelid_up_1_bezier_out_mstr_L', 'eyelid_up_1_bezier_out_L', 'eyelid_up_vert_def_1_bbone_out_L', 'eyelid_up_2_bezier_out_mstr_L', 'eyelid_up_2_bezier_out_L', 'eyelid_up_4_bezier_in_mstr_L', 'eyelid_up_4_bezier_in_L', 'eyelid_up_4_bbone_in_L', 'eyelid_up_vert_def_3_bbone_out_L', 'eyelid_out_vert_def_bbone_out_L', 'eyelid_up_3_bezier_out_mstr_L', 'eyelid_up_3_bezier_out_L', 'eyelid_up_3_bbone_out_L', 'eyelid_low_vert_def_2_bbone_out_L', 'eyelid_low_1_bezier_out_mstr_L', 'eyelid_low_1_bezier_out_L', 'eyelid_low_3_bezier_in_mstr_L', 'eyelid_low_3_bezier_in_L', 'eyelid_low_3_bbone_in_L', 'eyelid_low_vert_def_1_bbone_out_L', 'eyelid_low_4_bezier_in_mstr_L', 'eyelid_low_4_bezier_in_L', 'eyelid_low_4_bbone_in_L', 'eyelid_low_2_bezier_out_mstr_L', 'eyelid_low_2_bezier_out_L', 'eyelid_low_vert_def_3_bbone_out_L', 'eyelid_low_3_bezier_out_mstr_L', 'eyelid_low_3_bezier_out_L', 'eyelid_low_3_bbone_out_L', 'eyelid_in_vert_def_bbone_out_L', 'eyelid_low_2_bezier_in_mstr_L', 'eyelid_low_2_bezier_in_L', 'eyelid_low_2_bbone_in_L', 'eyelid_low_2_bbone_out_L', 'eyelid_low_1_L_bezier_in_L', 'eyelid_low_1_L_bbone_in_L', 'eyelid_low_1_bbone_out_L', 'eyelid_up_2_bezier_in_mstr_L', 'eyelid_up_2_bezier_in_L', 'eyelid_up_2_bbone_in_L', 'eyelid_up_2_bbone_out_L', 'eyelid_up_1_L_bezier_in_L', 'eyelid_up_1_L_bbone_in_L', 'eyelid_up_1_bbone_out_L', 'eyelid_low_vert_def_2_bbone_out_R', 'eyelid_up_vert_def_2_bbone_out_R', 'eyelid_low_1_bezier_out_mstr_R', 'eyelid_low_1_bezier_out_R', 'eyelid_low_3_bezier_in_mstr_R', 'eyelid_low_3_bezier_in_R', 'eyelid_low_3_bbone_in_R', 'eyelid_low_vert_def_1_bbone_out_R', 'eyelid_up_3_bezier_in_mstr_R', 'eyelid_up_3_bezier_in_R', 'eyelid_up_3_bbone_in_R', 'eyelid_up_1_bezier_out_mstr_R', 'eyelid_up_1_bezier_out_R', 'eyelid_up_vert_def_1_bbone_out_R', 'eyelid_low_4_bezier_in_mstr_R', 'eyelid_low_4_bezier_in_R', 'eyelid_low_4_bbone_in_R', 'eyelid_low_2_bezier_out_mstr_R', 'eyelid_low_2_bezier_out_R', 'eyelid_low_vert_def_3_bbone_out_R', 'eyelid_up_2_bezier_out_mstr_R', 'eyelid_up_2_bezier_out_R', 'eyelid_up_4_bezier_in_mstr_R', 'eyelid_up_4_bezier_in_R', 'eyelid_up_4_bbone_in_R', 'eyelid_up_vert_def_3_bbone_out_R', 'eyelid_in_vert_def_bbone_out_R', 'eyelid_low_2_bezier_in_mstr_R', 'eyelid_low_2_bezier_in_R', 'eyelid_low_2_bbone_in_R', 'eyelid_low_2_bbone_out_R', 'eyelid_low_1_L_bezier_in_R', 'eyelid_low_1_L_bbone_in_R', 'eyelid_low_1_bbone_out_R', 'eyelid_up_2_bezier_in_mstr_R', 'eyelid_up_2_bezier_in_R', 'eyelid_up_2_bbone_in_R', 'eyelid_up_2_bbone_out_R', 'eyelid_up_1_L_bezier_in_R', 'eyelid_up_1_L_bbone_in_R', 'eyelid_up_1_bbone_out_R', 'eyelid_out_vert_def_bbone_out_R', 'eyelid_low_3_bezier_out_mstr_R', 'eyelid_low_3_bezier_out_R', 'eyelid_low_3_bbone_out_R', 'eyelid_up_3_bezier_out_mstr_R', 'eyelid_up_3_bezier_out_R', 'eyelid_up_3_bbone_out_R']
        if b.name in TOON_L_bones:
            b.bone_group_index = TOON_L_index[0]
        if b.name in TOON_R_bones:
            b.bone_group_index = TOON_R_index[0]
        if b.name in BBONE_MECH_bones:
            b.bone_group_index = BBONE_MECH_index[0]

#### Bone Shapes #### 

def biped_update_1005_bone_shapes(self, context):

    arm = bpy.context.active_object
    pbones = arm.pose.bones

    for b in pbones:
        if b.name == 'lattice_eye_L':
            b.custom_shape = bpy.data.objects['cs_toon_eye_low_L']
            try:
                b.custom_shape_scale = 5
            except:
                b.custom_shape_scale_xyz = 5
        if b.name == 'lattice_eye_R':
            b.custom_shape = bpy.data.objects['cs_toon_eye_low_R'] 
            try:
                b.custom_shape_scale = 5
            except:
                b.custom_shape_scale_xyz = 5
        if b.name == 'head_toon':
            try:
                b.custom_shape_scale = b.custom_shape_scale + 0.1
            except:
                b.custom_shape_scale_xyz = b.custom_shape_scale_xyz + 0.1

#### New Bones for Lattice_eye #### 

def biped_update_1005_new_bones(self, context):
    arm = bpy.context.active_object
    arm_data = arm.data
    # Generic bone creation function
    def add_bones (b_name, b_head, b_tail, b_bbone_in, b_bbone_out, b_bbone_segments, b_bbone_x, b_bbone_z, b_envelope_distance, b_envelope_weight, b_head_radius, b_parent, b_roll, b_tail_radius, b_use_connect, b_use_cyclic_offset, b_use_deform, b_use_envelope_multiply, b_use_inherit_rotation, b_use_inherit_scale, b_use_local_location, b_use_relative_parent, b_layers, b_align_prop, b_head_prop, b_tail_prop, b_roll_prop, b_roll_angle_prop):
        bone = arm_data.edit_bones.new(b_name) 
        bone.head = b_head  
        bone.tail = b_tail
        bone.bbone_in = b_bbone_in 
        bone.bbone_out = b_bbone_out
        bone.bbone_segments = b_bbone_segments 
        bone.bbone_x = b_bbone_x
        bone.bbone_z = b_bbone_z
        bone.envelope_distance = b_envelope_distance
        bone.envelope_weight = b_envelope_weight 
        bone.head_radius = b_head_radius 
        bone.parent = b_parent
        bone.roll = b_roll 
        bone.tail_radius = b_tail_radius
        bone.use_connect = b_use_connect
        bone.use_cyclic_offset = b_use_cyclic_offset
        bone.use_deform = b_use_deform
        bone.use_envelope_multiply = b_use_envelope_multiply
        bone.use_inherit_rotation = b_use_inherit_rotation
        bone.use_inherit_scale = b_use_inherit_scale 
        bone.use_local_location = b_use_local_location      
        bone.use_relative_parent = b_use_relative_parent 
        bone.layers[:] = b_layers
        bone['b_align'] = b_align_prop
        bone['b_head'] = b_head_prop
        bone['b_tail'] = b_tail_prop
        bone['b_roll'] = b_roll_prop
        bone['b_roll_angle'] = b_roll_angle_prop    

    # Add new bones
    bpy.ops.object.mode_set(mode='EDIT') 

    for b in arm_data.edit_bones:
        if b.name == 'eye_mstr_str_L':
            bone_head = b.head
            bone_tail = b.tail
            bone_roll = b.roll
            add_bones ('lattice_eye_mstr_L', bone_head, bone_tail, 1.0, 1.0, 1, 0.0001083384922822006, 0.0001083384922822006, 0.008668862283229828, 1.0, 0.008668862283229828, arm_data.edit_bones["eye_mstr_str_L"], bone_roll, 0.003488908987492323, False, True, True, False, True, True, True, True, (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False), [''], ['eye_mstr_str_L', 'head'], ['eye_mstr_str_L', 'tail'], ['GLOBAL_POS_Z', ''], ['0.0'])    

    for b in arm_data.edit_bones:
        if b.name == 'eye_mstr_str_R':
            bone_head = b.head
            bone_tail = b.tail
            bone_roll = b.roll
            add_bones ('lattice_eye_mstr_R', bone_head, bone_tail, 1.0, 1.0, 1, 0.0001083384922822006, 0.0001083384922822006, 0.008668862283229828, 1.0, 0.008668862283229828, arm_data.edit_bones["eye_mstr_str_R"], bone_roll, 0.003488908987492323, False, True, True, False, True, True, True, True, (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False), [''], ['eye_mstr_str_R', 'head'], ['eye_mstr_str_R', 'tail'], ['GLOBAL_POS_Z', ''], ['-0.0'])

    bpy.ops.object.mode_set(mode='POSE') 

    # Add Copy Scale Constraint

    pbones = arm.pose.bones

    bone = []
    const_name = []

    # Generic constraint add function
    def add_consts(b_name, c_type, c_name, c_influence, c_mute):
        bone[:] = []
        const_name[:] = []
        cnst = pbones[b_name].constraints.new(c_type)
        cnst.name = c_name
        cnst.influence = c_influence
        cnst.mute = c_mute
        bone.append(b_name)
        const_name.append(cnst.name)

    # Generic Copy Scale parameters function
    def copy_scale(c_owner_space, c_subtarget, c_target_space, c_use_offset, c_use_x, c_use_y, c_use_z):
        for b in pbones:
            if b.name == bone[0]:
                for C in b.constraints:
                    if C.name == const_name[0]:
                        C.owner_space = c_owner_space
                        C.subtarget = c_subtarget
                        C.target = arm
                        C.target_space = c_target_space
                        C.use_offset = c_use_offset
                        C.use_x = c_use_x
                        C.use_y = c_use_y
                        C.use_z = c_use_z

    # Add constraints
    add_consts('lattice_eye_mstr_L', 'COPY_SCALE', 'Copy Scale', 1.0, False)
    copy_scale('LOCAL', 'look_L', 'LOCAL', False, True, True, True)

    add_consts('lattice_eye_mstr_R', 'COPY_SCALE', 'Copy Scale', 1.0, False)
    copy_scale('LOCAL', 'look_R', 'LOCAL', False, True, True, True)

#### Add Hooks to Lattice_eye_L and R #### 

def biped_update_1005_lattices(self, context):
    arm = bpy.context.active_object
    
    blenrig_name = []
    lattice_name = []
    vgroup_name = []

    # Save state of layers    
    active_layers = []

    def all_layers():     
        for i in range(len(bpy.context.scene.layers)):
            layers_status = bpy.context.scene.layers[i]
            if layers_status.real == 1:
                active_layers.append(i)            
        #Turn on all layers
        bpy.context.scene.layers = [(x in [x]) for x in range(20)]  

    def reset_layers():          
        bpy.context.scene.layers = [(x in active_layers) for x in range(20)]    

    # Generic function for adding a Vgroup to a lattice
    def add_vgroups(l_name, l_vg_name):
        blenrig_name.append(arm.name)
        vgroup_name[:] = []
        lattice_name[:] = []
        for ob in bpy.data.objects:
            if ob.name == l_name:
                vg = ob.vertex_groups.new(l_vg_name)
                vgroup_name.append(vg.name)
                lattice_name.append(ob.name)

    # Generic function for assigning vertex weights to the lattice   
    def add_vg_weights(l_vg_point, l_vg_weight):
        for ob in bpy.data.objects:
            if ob.name == lattice_name[0]:
                for vg in ob.vertex_groups:
                    if vg.name == vgroup_name[0]:
                        vg.add([l_vg_point],l_vg_weight, 'REPLACE')

    # Generic for adding a hook modifier to the lattice                   
    def add_mod(m_name, m_type, m_strength, m_subtarget, m_vgroup):
        for ob in bpy.data.objects:
            if ob.name == lattice_name[0]:
                mod = ob.modifiers.new(m_name, m_type)
                mod.object = bpy.data.objects[blenrig_name[0]]     
                mod.strength = m_strength             
                mod.subtarget = m_subtarget
                mod.vertex_group = m_vgroup     
                bpy.context.scene.objects.active = ob

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.lattice.select_all(action='SELECT')
                for mod in ob.modifiers:
                    if mod.type == 'HOOK':
                        bpy.ops.object.hook_reset(modifier=mod.name)
                bpy.ops.object.mode_set(mode='OBJECT')   

    # Make BlenRig armature the active object again
    def select_blenrig():
        for ob in bpy.data.objects:
            if ob.name == blenrig_name[0]:
                bpy.context.scene.objects.active = ob    

    # Apply changes
    all_layers()
    add_vgroups('LATTICE_EYE_L', 'lattice_eye_mstr_L')
    add_vg_weights(0,1.0)
    add_vg_weights(1,1.0)
    add_vg_weights(2,1.0)
    add_vg_weights(3,1.0)
    add_vg_weights(4,1.0)
    add_vg_weights(5,1.0)
    add_vg_weights(6,1.0)
    add_vg_weights(7,1.0)
    add_vg_weights(8,1.0)
    add_vg_weights(9,1.0)
    add_vg_weights(10,1.0)
    add_vg_weights(11,1.0)
    add_vg_weights(12,1.0)
    add_vg_weights(13,1.0)
    add_vg_weights(14,1.0)
    add_vg_weights(15,1.0)
    add_vg_weights(16,1.0)
    add_vg_weights(17,1.0)
    add_mod('lattice_eye_mstr_L', 'HOOK', 1.0, 'lattice_eye_mstr_L', 'lattice_eye_mstr_L')
    select_blenrig()

    add_vgroups('LATTICE_EYE_R', 'lattice_eye_mstr_R')
    add_vg_weights(0,1.0)
    add_vg_weights(1,1.0)
    add_vg_weights(2,1.0)
    add_vg_weights(3,1.0)
    add_vg_weights(4,1.0)
    add_vg_weights(5,1.0)
    add_vg_weights(6,1.0)
    add_vg_weights(7,1.0)
    add_vg_weights(8,1.0)
    add_vg_weights(9,1.0)
    add_vg_weights(10,1.0)
    add_vg_weights(11,1.0)
    add_vg_weights(12,1.0)
    add_vg_weights(13,1.0)
    add_vg_weights(14,1.0)
    add_vg_weights(15,1.0)
    add_vg_weights(16,1.0)
    add_vg_weights(17,1.0)
    add_mod('lattice_eye_mstr_R', 'HOOK', 1.0, 'lattice_eye_mstr_R', 'lattice_eye_mstr_R')
    select_blenrig()
    reset_layers()

#### Protected layers change #### 

def biped_update_1005_protected_layers(self, context):
    arm = bpy.context.active_object
    arm_data = arm.data

    arm_data.layers_protected =[(x not in [25]) for x in range(32)]    

#### Update Rig Functions local script #### 

def biped_update_1005_functions_script(self, context):

    # Updated script
    update_1005 = """import bpy

# V 1.005

#### Script used for generating the scripted functions of BlenRig when the addon is not present

####### Bones Hiding System #######

from bpy.props import FloatProperty, IntProperty, BoolProperty


def bone_auto_hide(context):  
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False    
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):   
        for b_prop in bpy.context.active_object.data.items():
            if b_prop[0] == 'bone_auto_hide' and b_prop[1] == 0:
                return False          
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):     

                arm = bpy.context.active_object.data 
                p_bones = bpy.context.active_object.pose.bones
                
                for b in p_bones:
                    if ('properties' in b.name):
                        if ('torso' in b.name):

                        # Torso FK/IK   
                            prop = int(b.ik_torso)
                            prop_inv = int(b.inv_torso)  
                        
                            for bone in arm.bones:          
                                if (bone.name in b['bones_ik']):
                                    if prop == 1 or prop_inv == 1:
                                        bone.hide = 1   
                                    else:
                                        bone.hide = 0    
                                if (bone.name in b['bones_fk']):
                                    if prop != 1 or prop_inv == 1:
                                        bone.hide = 1 
                                    else:
                                        bone.hide = 0            

                        # Torso INV   
                            for bone in arm.bones:   
                                if (bone.name in b['bones_inv']):
                                    if prop_inv == 1:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                                 
                        if ('head' in b.name):
                        # Neck FK/IK          
                            prop = int(b.ik_head)
                            for bone in arm.bones:
                                if (bone.name in b['bones_fk']):
                                    if prop == 1:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                                      
                                if (bone.name in b['bones_ik']):
                                    if prop == 0:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                                                                         

                        # Head Hinge         
                            prop_hinge = int(b.hinge_head)
                            for bone in arm.bones:       
                                if (bone.name in b['bones_fk_hinge']):
                                    if prop == 1 or prop_hinge == 0:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                              
                                if (bone.name in b['bones_ik_hinge']):
                                    if prop == 0 or prop_hinge == 1:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1     
                        #Left Properties                
                        if ('_L' in b.name): 
                            if ('arm' in b.name):

                            # Arm_L FK/IK           
                                prop = int(b.ik_arm_L)
                                prop_hinge = int(b.space_hand_L)
                                for bone in arm.bones:       
                                    if (bone.name in b['bones_fk_L']):
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                           
                                    if (bone.name in b['bones_ik_L']):
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                      

                            # HAND_L
                                    if arm['rig_type'] == "Biped":    
                                        if (bone.name in b['bones_ik_hand_L']):  
                                            if prop == 1 and prop_hinge == 0:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0  
                                        if (bone.name in b['bones_fk_hand_L']):   
                                            if prop_hinge == 1:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                              
                                        if (bone.name in b['bones_ik_palm_L']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                       
                                        if (bone.name in b['bones_fk_palm_L']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1   

                            # Fingers_L   
                                prop_ik_all = int(b.ik_fing_all_L)  
                                prop_hinge_all = int(b.hinge_fing_all_L)   

                                def fingers_hide(b_name):                                              
                                    for bone in arm.bones:
                                        ik_bones = [b_name]   
                                        if (bone.name == b_name):
                                            if prop == 1 or prop_hinge == 1 or prop_ik_all == 1 or prop_hinge_all == 1:
                                                bone.hide = 0
                                            if prop == 0 and prop_hinge == 0 and prop_ik_all == 0 and prop_hinge_all == 0:
                                                bone.hide = 1  
                                    return {"FINISHED"}      

                                prop_hinge = int(b.hinge_fing_ind_L)
                                prop = int(b.ik_fing_ind_L)                                                                                           
                                fingers_hide('fing_ind_ik_L')     
                                prop_hinge = int(b.hinge_fing_mid_L)
                                prop = int(b.ik_fing_mid_L)                                                                                           
                                fingers_hide('fing_mid_ik_L')  
                                prop_hinge = int(b.hinge_fing_ring_L)
                                prop = int(b.ik_fing_ring_L)                                                                                           
                                fingers_hide('fing_ring_ik_L')   
                                prop_hinge = int(b.hinge_fing_lit_L)
                                prop = int(b.ik_fing_lit_L)                                                                                           
                                fingers_hide('fing_lit_ik_L')   
                                prop_hinge = int(b.hinge_fing_thumb_L)
                                prop = int(b.ik_fing_thumb_L)                                                                                           
                                fingers_hide('fing_thumb_ik_L')                                                                     

                            if ('leg' in b.name):                                       
                            # Leg_L FK/IK           
                                prop = int(b.ik_leg_L)
                                for bone in arm.bones:     
                                    if (bone.name in b['bones_fk_L']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                               
                                    if (bone.name in b['bones_ik_L']):   
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1   

                            # Toes_L FK/IK          
                                prop = int(b.ik_toes_all_L)
                                prop_hinge = int(b.hinge_toes_all_L)                                
                                for bone in arm.bones:           
                                    if (bone.name in b['bones_fk_foot_L']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  
                                    if (bone.name in b['bones_ik_foot_L']):  
                                        if prop == 0 or prop_hinge == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  

                        #Right Properties                
                        if ('_R' in b.name): 
                            if ('arm' in b.name):

                            # Arm_R FK/IK           
                                prop = int(b.ik_arm_R)
                                prop_hinge = int(b.space_hand_R)
                                for bone in arm.bones:       
                                    if (bone.name in b['bones_fk_R']):
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                           
                                    if (bone.name in b['bones_ik_R']):
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                      

                            # HAND_R
                                    if arm['rig_type'] == "Biped":    
                                        if (bone.name in b['bones_ik_hand_R']):  
                                            if prop == 1 and prop_hinge == 0:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0  
                                        if (bone.name in b['bones_fk_hand_R']):   
                                            if prop_hinge == 1:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                              
                                        if (bone.name in b['bones_ik_palm_R']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                       
                                        if (bone.name in b['bones_fk_palm_R']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1   

                            # Fingers_R   
                                prop_ik_all = int(b.ik_fing_all_R)  
                                prop_hinge_all = int(b.hinge_fing_all_R)   

                                def fingers_hide(b_name):                                              
                                    for bone in arm.bones:
                                        ik_bones = [b_name]   
                                        if (bone.name == b_name):
                                            if prop == 1 or prop_hinge == 1 or prop_ik_all == 1 or prop_hinge_all == 1:
                                                bone.hide = 0
                                            if prop == 0 and prop_hinge == 0 and prop_ik_all == 0 and prop_hinge_all == 0:
                                                bone.hide = 1  
                                    return {"FINISHED"}      

                                prop_hinge = int(b.hinge_fing_ind_R)
                                prop = int(b.ik_fing_ind_R)                                                                                           
                                fingers_hide('fing_ind_ik_R')     
                                prop_hinge = int(b.hinge_fing_mid_R)
                                prop = int(b.ik_fing_mid_R)                                                                                           
                                fingers_hide('fing_mid_ik_R')  
                                prop_hinge = int(b.hinge_fing_ring_R)
                                prop = int(b.ik_fing_ring_R)                                                                                           
                                fingers_hide('fing_ring_ik_R')   
                                prop_hinge = int(b.hinge_fing_lit_R)
                                prop = int(b.ik_fing_lit_R)                                                                                           
                                fingers_hide('fing_lit_ik_R')   
                                prop_hinge = int(b.hinge_fing_thumb_R)
                                prop = int(b.ik_fing_thumb_R)                                                                                           
                                fingers_hide('fing_thumb_ik_R')                                                                     

                            if ('leg' in b.name):                                       
                            # Leg_R FK/IK           
                                prop = int(b.ik_leg_R)
                                for bone in arm.bones:     
                                    if (bone.name in b['bones_fk_R']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                               
                                    if (bone.name in b['bones_ik_R']):   
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1   

                            # Toes_R FK/IK          
                                prop = int(b.ik_toes_all_R)
                                prop_hinge = int(b.hinge_toes_all_R)
                                for bone in arm.bones:           
                                    if (bone.name in b['bones_fk_foot_R']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  
                                    if (bone.name in b['bones_ik_foot_R']):  
                                        if prop == 0 or prop_hinge == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  
                                
####### Reproportion Toggle #######
listaDeEstados = []
def reproportion_toggle(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False    
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):   
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):  
                prop = bool(bpy.context.active_object.data.reproportion)        
                p_bones = bpy.context.active_object.pose.bones
                if prop:
                    contador = 0
                    for layer in bpy.context.active_object.data.layers:
                        listaDeEstados.insert(contador, layer)
                        contador += 1
                    
                    contador = 0
                    for layer in bpy.context.active_object.data.layers:
                        if layer:
                            bpy.context.active_object.data.layers[contador] = not bpy.context.active_object.data.layers[contador]
                        
                        contador += 1
                        bpy.context.active_object.data.layers[31] = True


                    for b in p_bones:      
                        for C in b.constraints:
                            if ('REPROP' in C.name):
                                C.mute = False 
                            if ('NOREP' in C.name):
                                C.mute = True   

                else:
                    contador = 0 
                    try :
                        for layer in bpy.context.active_object.data.layers:
                            bpy.context.active_object.data.layers[contador] = listaDeEstados[contador]
                            contador += 1
                    
                        for b in p_bones:
                            for C in b.constraints:
                                if ('REPROP' in C.name):
                                    C.mute = True
                                if ('NOREP' in C.name):
                                    C.mute = False
                        rig_toggles(context)
                    except:
                        pass


####### Rig Toggles #######

def rig_toggles(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False    
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):   
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):                
                p_bones = bpy.context.active_object.pose.bones
                arm = bpy.context.active_object.data 

                for b in p_bones:
                    if ('properties' in b.name):
                        # Left Properties
                        #Fingers_L 
                        if ('L' in b.name):
                            if ('arm'in b.name):
                                prop_fing = int(b.toggle_fingers_L)
                                for bone in arm.bones:  
                                    if (bone.name in b['bones_fingers_def_1_L']):   
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0 
                                    if (bone.name in b['bones_fingers_def_2_L']):   
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1                                                
                                        else:
                                            bone.layers[27] = 0  
                                            bone.layers[31] = 0                                                
                                    if (bone.name in b['bones_fingers_str_L']):   
                                        if prop_fing == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0                     
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:                                                                                                               
                                            if (bone.name in b['bones_fingers_ctrl_1_L']):  
                                                if prop_fing == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0                                                                                                   
                                            if (bone.name in b['bones_fingers_ctrl_2_L']):  
                                                if prop_fing == 1:
                                                    bone.layers[2] = 1     
                                                else:
                                                    bone.layers[2] = 0                                                                                                 
                                    if (bone.name in b['bones_fingers_ctrl_2_L']):  
                                        if prop_fing == 1:                                         
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False                                                                          
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                    
                        #Toes_L
                        if ('L' in b.name):
                            if ('leg'in b.name):
                                prop_toes = int(b.toggle_toes_L)
                                for bone in arm.bones:         
                                    if (bone.name in b['bones_toes_def_1_L']): 
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0 
                                    if (bone.name in b['bones_toes_def_2_L']): 
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1                                                
                                        else:
                                            bone.layers[27] = 0    
                                            bone.layers[31] = 0                                                                                       
                                    if (bone.name in b['bones_no_toes_def_L']): 
                                        if prop_toes == 1:
                                            bone.layers[27] = 0
                                        else:
                                            bone.layers[27] = 1   
                                    if (bone.name in b['bones_toes_str_L']):   
                                        if prop_toes == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0         
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:                                                                                                                                
                                            if (bone.name in b['bones_toes_ctrl_1_L']): 
                                                if prop_toes == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0     
                                            if (bone.name in b['bones_no_toes_ctrl_L']): 
                                                if prop_toes == 1:
                                                    bone.layers[0] = 0
                                                else:
                                                    bone.layers[0] = 1    
                                            if (bone.name in b['bones_toes_ctrl_2_L']): 
                                                if prop_toes == 1:
                                                    bone.layers[2] = 1    
                                                else:
                                                    bone.layers[2] = 0                                                                                                                                                                 
                                    if (bone.name in b['bones_toes_ctrl_2_L']): 
                                        if prop_toes == 1:                                          
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False           
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                    

                        # Right Properties
                        #Fingers_R 
                        if ('R' in b.name):
                            if ('arm'in b.name):
                                prop_fing = int(b.toggle_fingers_R)
                                for bone in arm.bones:         
                                    if (bone.name in b['bones_fingers_def_1_R']):   
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0
                                    if (bone.name in b['bones_fingers_def_2_R']):   
                                        if prop_fing == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1                                                
                                        else:
                                            bone.layers[27] = 0
                                            bone.layers[31] = 0                                                
                                    if (bone.name in b['bones_fingers_str_R']):   
                                        if prop_fing == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0     
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:                                                                                                                                     
                                            if (bone.name in b['bones_fingers_ctrl_1_R']):  
                                                if prop_fing == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0                                                
                                            if (bone.name in b['bones_fingers_ctrl_2_R']):  
                                                if prop_fing == 1:
                                                    bone.layers[2] = 1     
                                                else:
                                                    bone.layers[2] = 0                                              
                                    if (bone.name in b['bones_fingers_ctrl_2_R']):  
                                        if prop_fing == 1:                                        
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False                                                                      
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                     
                        #Toes_R
                        if ('R' in b.name):
                            if ('leg'in b.name):
                                prop_toes = int(b.toggle_toes_R)
                                for bone in arm.bones:         
                                    if (bone.name in b['bones_toes_def_1_R']): 
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                        else:
                                            bone.layers[27] = 0
                                    if (bone.name in b['bones_toes_def_2_R']): 
                                        if prop_toes == 1:
                                            bone.layers[27] = 1
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[27] = 0
                                            bone.layers[31] = 0                                          
                                    if (bone.name in b['bones_no_toes_def_R']): 
                                        if prop_toes == 1:
                                            bone.layers[27] = 0
                                        else:
                                            bone.layers[27] = 1      
                                    if (bone.name in b['bones_toes_str_R']):   
                                        if prop_toes == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0     
                                    for b_prop in bpy.context.active_object.data.items():
                                        if b_prop[0] == 'custom_layers' and b_prop[1] == 0:                                                                                                                                
                                            if (bone.name in b['bones_toes_ctrl_1_R']): 
                                                if prop_toes == 1:
                                                    bone.layers[0] = 1
                                                else:
                                                    bone.layers[0] = 0     
                                            if (bone.name in b['bones_no_toes_ctrl_R']): 
                                                if prop_toes == 1:
                                                    bone.layers[0] = 0
                                                else:
                                                    bone.layers[0] = 1                                                                                       
                                            if (bone.name in b['bones_toes_ctrl_2_R']): 
                                                if prop_toes == 1:
                                                    bone.layers[2] = 1
                                                else:
                                                    bone.layers[2] = 0                                                    
                                    if (bone.name in b['bones_toes_ctrl_2_R']): 
                                        if prop_toes == 1:                                           
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False                                                                    
                                        else:
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                    

####### Rig Optimizations #######

####### Toggle Face Drivers #######

def toggle_face_drivers(context):
    if not bpy.context.screen:
        return False 
    if bpy.context.screen.is_animation_playing == True:
        return False       
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False    
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):                
            prop = bool(bpy.context.active_object.data.toggle_face_drivers)
            armobj = bpy.context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["mouth_corner_R"]["BACK_LIMIT_R"]',                                              
            'pose.bones["mouth_corner_R"]["DOWN_LIMIT_R"]',               
            'pose.bones["mouth_corner_R"]["FORW_LIMIT_R"]',
            'pose.bones["mouth_corner_R"]["IN_LIMIT_R"]', 
            'pose.bones["mouth_corner_R"]["OUT_LIMIT_R"]',
            'pose.bones["mouth_corner_R"]["UP_LIMIT_R"]',
            'pose.bones["mouth_corner_L"]["UP_LIMIT_L"]',
            'pose.bones["mouth_corner_L"]["OUT_LIMIT_L"]',
            'pose.bones["mouth_corner_L"]["IN_LIMIT_L"]',
            'pose.bones["mouth_corner_L"]["FORW_LIMIT_L"]',
            'pose.bones["mouth_corner_L"]["DOWN_LIMIT_L"]',
            'pose.bones["mouth_corner_L"]["BACK_LIMIT_L"]',
            'pose.bones["mouth_ctrl"]["OUT_LIMIT"]',
            'pose.bones["mouth_ctrl"]["IN_LIMIT"]',
            'pose.bones["mouth_ctrl"]["SMILE_LIMIT"]',
            'pose.bones["mouth_ctrl"]["JAW_ROTATION"]',
            'pose.bones["maxi"]["JAW_UP_LIMIT"]',
            'pose.bones["maxi"]["JAW_DOWN_LIMIT"]',
            'pose.bones["cheek_ctrl_R"]["CHEEK_DOWN_LIMIT_R"]',
            'pose.bones["cheek_ctrl_L"]["CHEEK_DOWN_LIMIT_L"]',
            'pose.bones["cheek_ctrl_R"]["CHEEK_UP_LIMIT_R"]',
            'pose.bones["cheek_ctrl_L"]["CHEEK_UP_LIMIT_L"]',
            'pose.bones["cheek_ctrl_R"]["AUTO_SMILE_R"]',
            'pose.bones["cheek_ctrl_L"]["AUTO_SMILE_L"]',
            'pose.bones["eyelid_low_ctrl_L"]["AUTO_CHEEK_L"]',
            'pose.bones["eyelid_low_ctrl_R"]["AUTO_CHEEK_R"]',
            'pose.bones["eyelid_low_ctrl_R"]["EYELID_DOWN_LIMIT_R"]',
            'pose.bones["eyelid_low_ctrl_L"]["EYELID_DOWN_LIMIT_L"]',
            'pose.bones["eyelid_low_ctrl_R"]["EYELID_UP_LIMIT_R"]',
            'pose.bones["eyelid_low_ctrl_L"]["EYELID_UP_LIMIT_L"]',
            'pose.bones["eyelid_up_ctrl_R"]["EYELID_DOWN_LIMIT_R"]',
            'pose.bones["eyelid_up_ctrl_L"]["EYELID_DOWN_LIMIT_L"]',
            'pose.bones["eyelid_up_ctrl_R"]["EYELID_UP_LIMIT_R"]',
            'pose.bones["eyelid_up_ctrl_L"]["EYELID_UP_LIMIT_L"]',
            'pose.bones["mouth_frown_ctrl_R"]["DOWN_LIMIT_R"]',
            'pose.bones["mouth_frown_ctrl_L"]["DOWN_LIMIT_L"]',
            'pose.bones["nose_frown_ctrl_R"]["UP_LIMIT_R"]',
            'pose.bones["nose_frown_ctrl_L"]["UP_LIMIT_L"]',
            'pose.bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"]',
            'pose.bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"]',
            'pose.bones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"]',
            'pose.bones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"]',
            'pose.bones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"]',
            'pose.bones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"]',
            'pose.bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"]',
            'pose.bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"]',
            'pose.bones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"]',
            'pose.bones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"]',
            'pose.bones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"]',
            'pose.bones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"]',
            'pose.bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"]',
            'pose.bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"]',
            'pose.bones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"]',
            'pose.bones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"]',
            'pose.bones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"]',
            'pose.bones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"]',
            'pose.bones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_X_R"]',
            'pose.bones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_Y_R"]',
            'pose.bones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_Z_R"]',
            'pose.bones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_X_R"]',
            'pose.bones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_Y_R"]',
            'pose.bones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_Z_R"]',
            'pose.bones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_X_R"]',
            'pose.bones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_Y_R"]',
            'pose.bones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_Z_R"]',
            'pose.bones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_X_R"]',
            'pose.bones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_Y_R"]',
            'pose.bones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_Z_R"]',
            'pose.bones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_X_R"]',
            'pose.bones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_Y_R"]',
            'pose.bones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_Z_R"]',
            'pose.bones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_X_R"]',
            'pose.bones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_Y_R"]',
            'pose.bones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_Z_R"]',
            'pose.bones["mouth_corner_R"]["ACTION_BACK_TOGGLE_R"]',
            'pose.bones["mouth_corner_L"]["ACTION_BACK_TOGGLE_L"]',
            'pose.bones["mouth_corner_R"]["ACTION_DOWN_TOGGLE_R"]',
            'pose.bones["mouth_corner_L"]["ACTION_DOWN_TOGGLE_L"]',
            'pose.bones["mouth_corner_R"]["ACTION_FORW_TOGGLE_R"]',
            'pose.bones["mouth_corner_L"]["ACTION_FORW_TOGGLE_L"]',
            'pose.bones["mouth_corner_R"]["ACTION_IN_TOGGLE_R"]',
            'pose.bones["mouth_corner_L"]["ACTION_IN_TOGGLE_L"]',
            'pose.bones["mouth_corner_R"]["ACTION_OUT_TOGGLE_R"]',
            'pose.bones["mouth_corner_L"]["ACTION_OUT_TOGGLE_L"]',
            'pose.bones["mouth_corner_R"]["ACTION_UP_TOGGLE_R"]',
            'pose.bones["mouth_corner_L"]["ACTION_UP_TOGGLE_L"]',
            'pose.bones["maxi"]["ACTION_UP_DOWN_TOGGLE"]',
            'pose.bones["cheek_ctrl_R"]["ACTION_CHEEK_TOGGLE_R"]',
            'pose.bones["cheek_ctrl_L"]["ACTION_CHEEK_TOGGLE_L"]',
            'pose.bones["mouth_corner_L"]["AUTO_BACK_L"]',
            'pose.bones["mouth_corner_R"]["AUTO_BACK_R"]']        

            for C in drivers:
                for vars in C.driver.variables:
                        for T in vars.targets:        
                            for D in data_path_list:
                                if D in T.data_path:
                                    if prop == 1:
                                        C.mute = False
                                    else:
                                        C.mute = True    

####### Toggle Flex Drivers #######

def toggle_flex_drivers(context):
    if not bpy.context.screen:
        return False 
    if bpy.context.screen.is_animation_playing == True:
        return False       
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False    
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):                
            prop = bool(bpy.context.active_object.data.toggle_flex_drivers)
            armobj = bpy.context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["properties_head"]["flex_head_scale"]',
            'pose.bones["properties_head"]["flex_neck_length"]',
            'pose.bones["properties_head"]["flex_neck_width"]',
            'pose.bones["properties_arm_R"]["flex_arm_length_R"]',
            'pose.bones["properties_arm_R"]["flex_arm_uniform_scale_R"]',
            'pose.bones["properties_arm_R"]["flex_arm_width_R"]',
            'pose.bones["properties_arm_R"]["flex_forearm_length_R"]',
            'pose.bones["properties_arm_R"]["flex_forearm_width_R"]',
            'pose.bones["properties_arm_R"]["flex_hand_scale_R"]',
            'pose.bones["properties_torso"]["flex_torso_height"]',
            'pose.bones["properties_torso"]["flex_torso_scale"]',
            'pose.bones["properties_torso"]["flex_chest_width"]',
            'pose.bones["properties_torso"]["flex_ribs_width"]',
            'pose.bones["properties_torso"]["flex_waist_width"]',
            'pose.bones["properties_torso"]["flex_pelvis_width"]',
            'pose.bones["properties_arm_L"]["flex_arm_length_L"]',
            'pose.bones["properties_arm_L"]["flex_arm_uniform_scale_L"]',
            'pose.bones["properties_arm_L"]["flex_arm_width_L"]',
            'pose.bones["properties_arm_L"]["flex_forearm_length_L"]',
            'pose.bones["properties_arm_L"]["flex_forearm_width_L"]',
            'pose.bones["properties_arm_L"]["flex_hand_scale_L"]',
            'pose.bones["properties_leg_R"]["flex_leg_uniform_scale_R"]',
            'pose.bones["properties_leg_R"]["flex_thigh_length_R"]',
            'pose.bones["properties_leg_R"]["flex_thigh_width_R"]',
            'pose.bones["properties_leg_R"]["flex_shin_length_R"]',
            'pose.bones["properties_leg_R"]["flex_shin_width_R"]',
            'pose.bones["properties_leg_R"]["flex_foot_scale_R"]',
            'pose.bones["properties_leg_R"]["flex_foot_loc_R"]',
            'pose.bones["properties_leg_L"]["flex_leg_uniform_scale_L"]',
            'pose.bones["properties_leg_L"]["flex_thigh_length_L"]',
            'pose.bones["properties_leg_L"]["flex_thigh_width_L"]',
            'pose.bones["properties_leg_L"]["flex_shin_length_L"]',
            'pose.bones["properties_leg_L"]["flex_shin_width_L"]',
            'pose.bones["properties_leg_L"]["flex_foot_scale_L"]',
            'pose.bones["properties_leg_L"]["flex_foot_loc_L"]']       

            for C in drivers:
                for vars in C.driver.variables:
                        for T in vars.targets:        
                            for D in data_path_list:
                                if D in T.data_path:
                                    if prop == 1:
                                        C.mute = False
                                    else:
                                        C.mute = True    

####### Toggle Body Drivers #######

def toggle_body_drivers(context):
    if not bpy.context.screen:
        return False 
    if bpy.context.screen.is_animation_playing == True:
        return False       
    if not bpy.context.active_object:
        return False
    if not context.armature:
        return False    
    for prop in bpy.context.active_object.data.items():
        if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):                
            prop = bool(bpy.context.active_object.data.toggle_body_drivers)
            armobj = bpy.context.active_object
            drivers = armobj.animation_data.drivers
            data_path_list = ['pose.bones["forearm_ik_R"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
            'pose.bones["forearm_ik_L"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
            'pose.bones["shin_ik_R"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
            'pose.bones["shin_ik_L"].constraints["Ik_Initial_Rotation"].to_min_x_rot',
            'pose.bones["properties_arm_R"]["realistic_joints_wrist_R"]',
            'pose.bones["properties_arm_L"]["realistic_joints_hand_L"]',
            'pose.bones["properties_arm_R"]["realistic_joints_hand_R"]',
            'pose.bones["properties_arm_L"]["realistic_joints_wrist_L"]',
            'pose.bones["properties_arm_R"]["realistic_joints_elbow_R"]',
            'pose.bones["properties_arm_L"]["realistic_joints_elbow_L"]',
            'pose.bones["properties_leg_R"]["realistic_joints_knee_R"]',
            'pose.bones["properties_leg_L"]["realistic_joints_knee_L"]',
            'pose.bones["properties_leg_R"]["realistic_joints_ankle_R"]',
            'pose.bones["properties_leg_L"]["realistic_joints_foot_L"]',
            'pose.bones["properties_leg_R"]["realistic_joints_foot_R"]',
            'pose.bones["properties_leg_L"]["realistic_joints_ankle_L"]',
            'pose.bones["foot_roll_ctrl_R"]["FOOT_ROLL_AMPLITUD_R"]',
            'pose.bones["foot_roll_ctrl_L"]["FOOT_ROLL_AMPLITUD_L"]',
            'pose.bones["foot_roll_ctrl_R"]["TOE_1_ROLL_START_R"]',
            'pose.bones["foot_roll_ctrl_L"]["TOE_1_ROLL_START_L"]',
            'pose.bones["foot_roll_ctrl_R"]["TOE_2_ROLL_START_R"]',
            'pose.bones["foot_roll_ctrl_L"]["TOE_2_ROLL_START_L"]',
            'pose.bones["neck_1_fk"]["fk_follow_main"]',
            'pose.bones["neck_2_fk"]["fk_follow_main"]',
            'pose.bones["neck_3_fk"]["fk_follow_main"]',
            'pose.bones["spine_1_fk"]["fk_follow_main"]',
            'pose.bones["spine_2_fk"]["fk_follow_main"]',
            'pose.bones["spine_3_fk"]["fk_follow_main"]',
            'pose.bones["spine_2_inv"]["fk_follow_main"]',
            'pose.bones["spine_1_inv"]["fk_follow_main"]',
            'pose.bones["pelvis_inv"]["fk_follow_main"]']     

            for C in drivers:
                for vars in C.driver.variables:
                        for T in vars.targets:        
                            for D in data_path_list:
                                if D in T.data_path:
                                    if prop == 1:
                                        C.mute = False
                                    else:
                                        C.mute = True         

######### Update Function for Properties ##########

def prop_update(self, context):
    bone_auto_hide(context)

def reprop_update(self, context):
    reproportion_toggle(context) 

def rig_toggles_update(self, context):
    rig_toggles(context)

def optimize_face(self, context):
    toggle_face_drivers(context) 

def optimize_flex(self, context):
    toggle_flex_drivers(context) 
            
def optimize_body(self, context):
    toggle_body_drivers(context)   

######### Hanlder for update on load and frame change #########

from bpy.app.handlers import persistent

@persistent
def load_handler(context):  
    bone_auto_hide(context)      
    reproportion_toggle(context)
    rig_toggles(context)      

bpy.app.handlers.load_post.append(load_handler)
bpy.app.handlers.frame_change_post.append(bone_auto_hide)


######### Properties Creation ############

#FK/IK

bpy.types.PoseBone.ik_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_head"
)

bpy.types.PoseBone.ik_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_torso"
)
bpy.types.PoseBone.inv_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Invert Torso Hierarchy",
    update=prop_update,
    name="inv_torso"
)
bpy.types.PoseBone.ik_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_arm_L"
)
bpy.types.PoseBone.ik_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_arm_R"
)
bpy.types.PoseBone.ik_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_leg_L"
)
bpy.types.PoseBone.ik_toes_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_toes_all_L"
)
bpy.types.PoseBone.ik_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_leg_R"
)
bpy.types.PoseBone.ik_toes_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_toes_all_R"
)
bpy.types.PoseBone.ik_fing_ind_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_ind_L"
)
bpy.types.PoseBone.ik_fing_mid_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_L"
)
bpy.types.PoseBone.ik_fing_ring_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_L"
)
bpy.types.PoseBone.ik_fing_lit_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_lit_L"
)
bpy.types.PoseBone.ik_fing_thumb_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_thumb_L"
)
bpy.types.PoseBone.ik_fing_ind_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_ind_R"
)
bpy.types.PoseBone.ik_fing_mid_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_R"
)
bpy.types.PoseBone.ik_fing_ring_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_R"
)
bpy.types.PoseBone.ik_fing_lit_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_lit_R"
)
bpy.types.PoseBone.ik_fing_thumb_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_thumb_R"
)
bpy.types.PoseBone.ik_fing_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_all_R"
)
bpy.types.PoseBone.ik_fing_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_all_L"
)

# HINGE

bpy.types.PoseBone.hinge_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_head"
)
bpy.types.PoseBone.hinge_neck = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_neck"
)
bpy.types.PoseBone.hinge_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_arm_L"
)
bpy.types.PoseBone.hinge_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_arm_R"
)
bpy.types.PoseBone.space_hand_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="space_hand_L"
)
bpy.types.PoseBone.space_hand_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="space_hand_R"
)
bpy.types.PoseBone.hinge_fing_ind_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_ind_L"
)
bpy.types.PoseBone.hinge_fing_mid_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_L"
)
bpy.types.PoseBone.hinge_fing_ring_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_L"
)
bpy.types.PoseBone.hinge_fing_lit_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_lit_L"
)
bpy.types.PoseBone.hinge_fing_thumb_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_thumb_L"
)
bpy.types.PoseBone.hinge_fing_ind_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_ind_R"
)
bpy.types.PoseBone.hinge_fing_mid_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_R"
)
bpy.types.PoseBone.hinge_fing_ring_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_R"
)
bpy.types.PoseBone.hinge_fing_lit_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_lit_R"
)
bpy.types.PoseBone.hinge_fing_thumb_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_thumb_R"
)
bpy.types.PoseBone.hinge_fing_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_all_R"
)
bpy.types.PoseBone.hinge_fing_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_all_L"
)
bpy.types.PoseBone.hinge_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_leg_L"
)
bpy.types.PoseBone.hinge_toes_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_toes_all_L"
)
bpy.types.PoseBone.hinge_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_leg_R"
)           
bpy.types.PoseBone.hinge_toes_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_toes_all_R"
)

#Stretchy IK

bpy.types.PoseBone.toon_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_head"
)   

bpy.types.PoseBone.toon_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_torso"
) 

bpy.types.PoseBone.toon_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_arm_L"
) 

bpy.types.PoseBone.toon_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_arm_R"
) 

bpy.types.PoseBone.toon_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_leg_L"
) 

bpy.types.PoseBone.toon_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_leg_R"
) 

# LOOK SWITCH
bpy.types.PoseBone.look_switch = FloatProperty(
    default=3.000,
    min=0.000,
    max=3.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Target of Eyes",
    update=prop_update,
    name="look_switch"
) 

# REPROPORTION
bpy.types.Armature.reproportion = BoolProperty(
    default=0,
    description="Toggle Reproportion Mode",
    update=reprop_update,
    name="reproportion"
) 
# TOGGLE_FACE_DRIVERS
bpy.types.Armature.toggle_face_drivers = BoolProperty(
    default=1,
    description="Toggle Face Riggin Drivers",
    update=optimize_face,
    name="toggle_face_drivers"
) 
# TOGGLE_FLEX_DRIVERS
bpy.types.Armature.toggle_flex_drivers = BoolProperty(
    default=1,
    description="Toggle Flex Scaling",
    update=optimize_flex,
    name="toggle_flex_drivers"
) 
# TOGGLE_BODY_DRIVERS
bpy.types.Armature.toggle_body_drivers = BoolProperty(
    default=1,
    description="Toggle Body Rigging Drivers",
    update=optimize_body,
    name="toggle_body_drivers"
) 
# TOGGLES
bpy.types.PoseBone.toggle_fingers_L = BoolProperty(
    default=0,
    description="Toggle fingers in rig",
    update=rig_toggles_update,
    name="toggle_fingers_L"
) 

bpy.types.PoseBone.toggle_toes_L = BoolProperty(
    default=0,
    description="Toggle toes in rig",
    update=rig_toggles_update,
    name="toggle_toes_L"
) 

bpy.types.PoseBone.toggle_fingers_R = BoolProperty(
    default=0,
    description="Toggle fingers in rig",
    update=rig_toggles_update,
    name="toggle_fingers_R"
) 

bpy.types.PoseBone.toggle_toes_R = BoolProperty(
    default=0,
    description="Toggle toes in rig",
    update=rig_toggles_update,
    name="toggle_toes_R"
)
    """

    for T in bpy.data.texts:
        if ('generate_customprops' in T.name):
            T.clear()
            T.current_line_index = 0
            T.write(update_1005)    
            T.current_line_index = 0     

#### Set Condensed Scheme #### 

def biped_update_1005_layer_scheme(self, context): 

    ## Run Condensed Scheme ##
    bpy.ops.blenrig.layers_scheme_compact()

#### Update Rig version #### 

def biped_update_1005_update_version(self, context): 
    arm_data = bpy.context.active_object.data
    
    arm_data['rig_version'] = 1.005          

    self.report({'INFO'}, 'BlenRig Armature updated to 1.005')
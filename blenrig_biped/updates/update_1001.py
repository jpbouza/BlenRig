import bpy

########### Biped Update 1.001 ###########

def biped_update_1001(self, context):
    # Fixes bug in IK torso
    arm = bpy.context.active_object
    arm_data = arm.data
    pbones = arm.pose.bones

    if arm_data['rig_version'] == 1.0:
        for b in pbones:
            if b.name == 'spine_2_ik_ctrl':
                for C in b.constraints:
                    if C.name == 'Transformation_torso_ik_ctrl':
                        b.constraints.remove(C)
                        
            if b.name == 'spine_2_ik':
                for C in b.constraints:
                    b.constraints.remove(C)    
                cnst = pbones['spine_2_ik'].constraints.new('COPY_ROTATION')
                cnst.name = 'Copy Rotation' 
                cnst.influence = 1.0 
                cnst.mute = False
                cnst.invert_x = False 
                cnst.invert_y = False 
                cnst.invert_z = False 
                cnst.owner_space = 'WORLD' 
                cnst.subtarget = 'spine_2_ik_ctrl' 
                cnst.target = bpy.context.active_object 
                cnst.target_space = 'WORLD' 
                cnst.use_offset = False 
                cnst.use_x = True 
                cnst.use_y = True 
                cnst.use_z = True
                cnst = pbones['spine_2_ik'].constraints.new('TRANSFORM')
                cnst.name = 'Transformation_torso_ik_ctrl' 
                cnst.influence = 1.0 
                cnst.mute = False
                cnst.from_max_x = 0.0 
                cnst.from_max_x_rot = 0.0 
                cnst.from_max_x_scale = 0.0 
                cnst.from_max_y = 0.0 
                cnst.from_max_y_rot = 0.01745329238474369 
                cnst.from_max_y_scale = 0.0 
                cnst.from_max_z = 0.0 
                cnst.from_max_z_rot = 0.0 
                cnst.from_max_z_scale = 0.0                                                                                                                                                        
                cnst.from_min_x = 0.0                                                                                                                                                              
                cnst.from_min_x_rot = 0.0                                                                                                                                                          
                cnst.from_min_x_scale = 0.0                                                                                                                                                        
                cnst.from_min_y = 0.0                                                                                                                                                              
                cnst.from_min_y_rot = 0.0                                                                                                                                                          
                cnst.from_min_y_scale = 0.0                                                                                                                                                        
                cnst.from_min_z = 0.0                                                                                                                                                              
                cnst.from_min_z_rot = 0.0 
                cnst.from_min_z_scale = 0.0 
                cnst.map_to = 'ROTATION' 
                cnst.map_to_x_from = 'X' 
                cnst.name = 'Transformation_torso_ik_ctrl' 
                cnst.map_to_y_from = 'Y' 
                cnst.map_to_z_from = 'Z' 
                cnst.map_from = 'ROTATION' 
                cnst.owner_space = 'LOCAL' 
                cnst.subtarget = 'torso_ik_ctrl' 
                cnst.target = bpy.context.active_object 
                cnst.target_space = 'LOCAL' 
                cnst.to_max_x = 0.0 
                cnst.to_max_x_rot = 0.0 
                cnst.to_max_x_scale = 0.0 
                cnst.to_max_y = 0.0 
                cnst.to_max_y_rot = 0.008726646192371845 
                cnst.to_max_y_scale = 0.0 
                cnst.to_max_z = 0.0 
                cnst.to_max_z_rot = 0.0 
                cnst.to_max_z_scale = 0.0 
                cnst.to_min_x = 0.0 
                cnst.to_min_x_rot = 0.0 
                cnst.to_min_x_scale = 0.0 
                cnst.to_min_y = 0.0 
                cnst.to_min_y_rot = 0.0 
                cnst.to_min_y_scale = 0.0 
                cnst.to_min_z = 0.0 
                cnst.to_min_z_rot = 0.0 
                cnst.to_min_z_scale = 0.0 
                cnst.use_motion_extrapolate = True
                cnst = pbones['spine_2_ik'].constraints.new('COPY_SCALE')
                cnst.name = 'Copy Scale' 
                cnst.influence = 1.0 
                cnst.mute = False
                cnst.owner_space = 'POSE' 
                cnst.subtarget = 'master_torso_pivot' 
                cnst.target = bpy.context.active_object 
                cnst.target_space = 'POSE' 
                cnst.use_offset = True 
                cnst.use_x = True 
                cnst.use_y = True 
                cnst.use_z = True
                cnst = pbones['spine_2_ik'].constraints.new('DAMPED_TRACK')
                cnst.name = 'Damped Track' 
                cnst.influence = 1.0 
                cnst.mute = False
                cnst.owner_space = 'WORLD' 
                cnst.subtarget = 'spine_3_inv_ik' 
                cnst.target = bpy.context.active_object 
                cnst.target_space = 'WORLD' 
                cnst.head_tail = 1.0 
                cnst.track_axis = 'TRACK_Y'
                cnst = pbones['spine_2_ik'].constraints.new('STRETCH_TO')
                cnst.name = 'Stretch To_REPROP' 
                cnst.influence = 1.0 
                cnst.mute = True
                cnst.owner_space = 'WORLD' 
                cnst.subtarget = 'spine_3_ik_ctrl' 
                cnst.target = bpy.context.active_object 
                cnst.target_space = 'WORLD' 
                cnst.head_tail = 0.0 
                cnst.keep_axis = 'PLANE_X' 
                cnst.rest_length = 0.1161453053355217 
                cnst.volume = 'NO_VOLUME' 
                cnst.bulge = 1.0 
                cnst.bulge_max = 1.0 
                cnst.bulge_min = 1.0 
                cnst.bulge_smooth = 0.0 
                cnst.use_bulge_max = False 
                cnst.use_bulge_min = False
        arm_data['rig_version'] = 1.001           
        self.report({'INFO'}, 'BlenRig Armature updated to 1.001')  
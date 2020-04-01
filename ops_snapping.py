import bpy

################################# IK/FK SNAPPING OPERATORS ##########################################################

#Selected and Active Bones Transforms Copy Function

def sel_act_bones(b1, b2, copy_op): #args will be replaced by the actual bone names

    arm = bpy.context.active_object
    arm_data = arm.data
    p_bones = arm.pose.bones

    Bone1 = p_bones[b1]
    Bone2 = p_bones[b2]
    #set Bone2 as active
    arm.data.bones.active = Bone2.bone
    Bone1.bone.select = 1
    copy_operator = ['rot', 'loc', 'scale', 'loc_rot', 'loc_rot_scale']
    if copy_operator[0] == copy_op:
        bpy.ops.pose.copy_pose_vis_rot()
    elif copy_operator[1] == copy_op:
        bpy.ops.pose.copy_pose_vis_loc() 
    elif copy_operator[2] == copy_op:
        bpy.ops.pose.copy_pose_vis_sca()   
    elif copy_operator[3] == copy_op:
        bpy.ops.pose.copy_pose_vis_loc()   
        bpy.ops.pose.copy_pose_vis_rot()   
    elif copy_operator[4] == copy_op:
        bpy.ops.pose.copy_pose_vis_loc()   
        bpy.ops.pose.copy_pose_vis_rot()                           
        bpy.ops.pose.copy_pose_vis_sca()                                 
    Bone1.bone.select = 0
    Bone2.bone.select = 0

##### TORSO #####

class Operator_Torso_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "torso_snap.ik_fk"   
    bl_label = "BlenRig Torso Snap IK FK"   
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_torso' == b.name):
#                prop = int(b.ik_torso)
#                prop_inv = int(b.inv_torso)
#                if prop != 0 or prop_inv != 0:
#                    self.report({'ERROR'}, 'Only works in IK mode')  
#                    return {"CANCELLED"}                  

        check_bones = ['spine_1_fk', 'spine_1_ik', 'spine_2_fk', 'spine_2_ik', 'spine_3_fk', 'spine_3_ik', 'torso_fk_ctrl']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 

        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False            

        arm_data.layers[30] = True           
        sel_act_bones('spine_1_fk', 'spine_1_ik', 'loc_rot')         
        sel_act_bones('spine_2_fk', 'spine_2_ik', 'loc_rot')      
        sel_act_bones('spine_3_fk', 'spine_3_ik', 'loc_rot')                  
        p_bones['torso_fk_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()               

        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['spine_1_fk', 'spine_2_fk', 'spine_3_fk', 'torso_fk_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            

        return {"FINISHED"}                

class Operator_Torso_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "torso_snap.fk_ik"   
    bl_label = "BlenRig Torso Snap FK IK"     
    bl_description = "Prepare seamless switch to IK"     
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_torso' == b.name):
#                prop = int(b.ik_torso)
#                prop_inv = int(b.inv_torso)
#                if prop != 1 or prop_inv != 0:
#                    self.report({'ERROR'}, 'Only works in FK mode')  
#                    return {"CANCELLED"}   

        check_bones = ['torso_ik_ctrl', 'snap_torso_fk_ctrl', 'spine_4_ik_ctrl', 'neck_1_fk', 'spine_3_ik_ctrl', 'spine_3_fk', 'spine_2_ik_ctrl', 'spine_2_fk', 'spine_1_ik_ctrl', 'spine_1_fk']

        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 

        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False       

        arm_data.layers[30] = True    
        sel_act_bones('torso_ik_ctrl', 'snap_torso_fk_ctrl', 'loc_rot')         
        sel_act_bones('spine_4_ik_ctrl', 'neck_1_fk', 'loc')      
        sel_act_bones('spine_3_ik_ctrl', 'spine_3_fk', 'loc')  
        sel_act_bones('spine_2_ik_ctrl', 'spine_2_fk', 'loc_rot')           
        sel_act_bones('spine_1_ik_ctrl', 'spine_1_fk', 'rot')   
        p_bones['spine_4_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()    
        p_bones['spine_3_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                            

        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['spine_1_ik_ctrl', 'spine_2_ik_ctrl', 'spine_3_ik_ctrl', 'spine_4_ik_ctrl', 'torso_ik_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            

        return {"FINISHED"}        

class Operator_Torso_Snap_INV_UP(bpy.types.Operator):   
    
    bl_idname = "torso_snap.inv_up"  
    bl_label = "BlenRig Torso Snap INV UP"    
    bl_description = "Prepare seamless switch to Invert torso"     
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_torso' == b.name):
#                prop_inv = int(b.inv_torso)
#                if prop_inv != 1:
#                    self.report({'ERROR'}, 'Only works in FK/IK mode')  
#                    return {"CANCELLED"}   

        check_bones = ['pelvis_ctrl', 'snap_pelvis_ctrl_inv', 'spine_1_fk', 'snap_spine_1_fk_inv', 'spine_2_fk', 'snap_spine_2_fk_inv', 'spine_3_fk', 'spine_3_inv', 'spine_2_ik_ctrl', 'spine_3_ik_ctrl', 'spine_4_ik_ctrl', 'torso_ik_ctrl', 'torso_fk_ctrl', 'neck_1_fk']

        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 

        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False          

        arm_data.layers[30] = True    
        sel_act_bones('pelvis_ctrl', 'snap_pelvis_ctrl_inv', 'loc_rot')         
        sel_act_bones('spine_1_fk', 'snap_spine_1_fk_inv', 'loc_rot')      
        sel_act_bones('spine_2_fk', 'snap_spine_2_fk_inv', 'loc_rot')  
        sel_act_bones('spine_3_fk', 'spine_3_inv', 'loc_rot')
        sel_act_bones('torso_ik_ctrl', 'snap_torso_fk_ctrl', 'loc_rot')         
        sel_act_bones('spine_4_ik_ctrl', 'neck_1_fk', 'loc')      
        sel_act_bones('spine_3_ik_ctrl', 'spine_3_fk', 'loc')  
        sel_act_bones('spine_2_ik_ctrl', 'spine_2_fk', 'loc_rot')           
        sel_act_bones('spine_1_ik_ctrl', 'spine_1_fk', 'rot')   
        p_bones['spine_4_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()    
        p_bones['spine_3_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()         
        p_bones['torso_fk_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                              

        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['pelvis_ctrl', 'spine_1_fk', 'spine_2_fk', 'spine_3_fk','spine_2_ik_ctrl', 'spine_3_ik_ctrl', 'spine_4_ik_ctrl', 'torso_ik_ctrl', 'torso_fk_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            

        return {"FINISHED"}        


class Operator_Torso_Snap_UP_INV(bpy.types.Operator):   
    
    bl_idname = "torso_snap.up_inv"  
    bl_label = "BlenRig Torso Snap UP INV"    
    bl_description = "Prepare seamless switch to FK or IK Torso"      
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_torso' == b.name):
#                prop = int(b.ik_torso)
#                prop_inv = int(b.inv_torso)
#                if prop_inv != 0:
#                    self.report({'ERROR'}, 'Only works in invert mode')  
#                    return {"CANCELLED"}   

        check_bones = ['spine_3_inv_ctrl', 'snap_torso_ctrl_inv_loc', 'spine_3_inv', 'spine_3_fk', 'spine_2_inv', 'snap_spine_2_inv_fk', 'spine_1_inv', 'snap_spine_1_inv_fk', 'pelvis_inv', 'pelvis', 'torso_inv_ctrl']

        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 

        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False       

        arm_data.layers[30] = True    
        sel_act_bones('spine_3_inv_ctrl', 'snap_torso_ctrl_inv_loc', 'loc_rot')         
        sel_act_bones('spine_3_inv', 'spine_3_fk', 'loc_rot')      
        sel_act_bones('spine_2_inv', 'snap_spine_2_inv_fk', 'loc_rot')  
        sel_act_bones('spine_1_inv', 'snap_spine_1_inv_fk', 'loc_rot')           
        sel_act_bones('pelvis_inv', 'pelvis', 'loc_rot')   
        p_bones['torso_inv_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                            

        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['pelvis_inv', 'spine_1_inv', 'spine_2_inv', 'spine_3_inv', 'torso_inv_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            

        return {"FINISHED"}    

##### HEAD #####
    

class Operator_Head_Snap_IK_FK(bpy.types.Operator): 

    bl_idname = "head_snap.ik_fk"    
    bl_label = "BlenRig Head Snap IK FK"     
    bl_description = "Prepare seamless switch to FK"     
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_head' == b.name):
#                prop = int(b.ik_head)
#                if prop != 0:
#                    self.report({'ERROR'}, 'Only works in IK mode')  
#                    return {"CANCELLED"}                  

        check_bones = ['neck_1_fk', 'neck_1_ik', 'neck_2_fk', 'neck_2_ik', 'neck_3_fk', 'neck_3_ik', 'neck_fk_ctrl']

        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 

        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False            

        arm_data.layers[30] = True           
        sel_act_bones('neck_1_fk', 'neck_1_ik', 'loc_rot')         
        sel_act_bones('neck_2_fk', 'neck_2_ik', 'loc_rot')      
        sel_act_bones('neck_3_fk', 'neck_3_ik', 'loc_rot')                  
        p_bones['neck_fk_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()               

        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['neck_1_fk', 'neck_2_fk', 'neck_3_fk', 'neck_fk_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            

        return {"FINISHED"}       

class Operator_Head_Snap_FK_IK(bpy.types.Operator): 
    
    bl_idname = "head_snap.fk_ik"    
    bl_label = "BlenRig Head Snap FK IK"      
    bl_description = "Prepare seamless switch to IK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_head' == b.name):
#                prop = int(b.ik_head)
#                if prop != 1:
#                    self.report({'ERROR'}, 'Only works in FK mode')  
#                    return {"CANCELLED"}   

        check_bones = ['neck_ik_ctrl', 'snap_neck_fk_pivot', 'head_ik_ctrl', 'head_fk', 'neck_3_ik_ctrl', 'neck_3_fk', 'neck_2_ik_ctrl', 'neck_2_fk']

        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 

        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False       

        arm_data.layers[30] = True    
        sel_act_bones('neck_ik_ctrl', 'snap_neck_fk_pivot', 'loc_rot')         
        sel_act_bones('head_ik_ctrl', 'head_fk', 'loc')              
        sel_act_bones('neck_3_ik_ctrl', 'neck_3_fk', 'loc_rot')    
        sel_act_bones('neck_2_ik_ctrl', 'neck_2_fk', 'loc')          
        p_bones['neck_2_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                                             

        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['neck_ik_ctrl', 'neck_3_ik_ctrl', 'neck_2_ik_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            

        return {"FINISHED"}        

##### ARM L #####


class Operator_Arm_L_Snap_IK_FK(bpy.types.Operator):    

    bl_idname = "arm_l_snap.ik_fk"   
    bl_label = "BlenRig Arm_L Snap IK FK"    
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_arm_L' == b.name):
#                prop = int(b.ik_arm_L)
#                if prop != 0:
#                    self.report({'ERROR'}, 'Only works in IK mode')  
#                    return {"CANCELLED"}                  

        # Biped
        if arm_data['rig_type'] == 'Biped':

            check_bones = ['arm_fk_L', 'arm_ik_L', 'forearm_fk_L', 'forearm_ik_L', 'hand_fk_L', 'hand_ik_ctrl_L']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_L', 'arm_ik_L', 'rot')         
            sel_act_bones('forearm_fk_L', 'forearm_ik_L', 'rot')  
            for b in p_bones:
                if ('properties_arm_L' in b.name):
                    prop = int(b.space_hand_L)
                    if prop == 1:            
                        sel_act_bones('hand_fk_L', 'hand_ik_ctrl_L', 'rot')                                

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_L', 'forearm_fk_L', 'hand_fk_L', 'hand_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False       

        #Quadruped    
        if arm_data['rig_type'] == 'Quadruped':     

            check_bones = ['arm_fk_L', 'arm_ik_L', 'forearm_fk_L', 'forearm_ik_L', 'hand_fk_L', 'hand_ik_ctrl_L', 'carpal_fk_L', 'carpal_ik_L', 'fing_1_fk_L', 'fing_1_ik_L', 'fing_2_fk_L', 'fing_2_ik_L']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_L', 'arm_ik_L', 'rot')         
            sel_act_bones('forearm_fk_L', 'forearm_ik_L', 'rot')  
            sel_act_bones('carpal_fk_L', 'carpal_ik_L', 'rot')               
            sel_act_bones('hand_fk_L', 'hand_ik_ctrl_L', 'rot') 
            sel_act_bones('fing_1_fk_L', 'fing_1_ik_L', 'rot')  
            sel_act_bones('fing_2_fk_L', 'fing_2_ik_L', 'rot')                  

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_L', 'forearm_fk_L', 'hand_fk_L', 'hand_ik_ctrl_L', 'carpal_fk_L', 'fing_1_fk_L', 'fing_2_fk_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                  

        return {"FINISHED"}    

class Operator_Arm_L_Snap_FK_IK(bpy.types.Operator):    

    bl_idname = "arm_l_snap.fk_ik"   
    bl_label = "BlenRig Arm_L Snap FK IK"    
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_arm_L' == b.name):
#                prop = int(b.ik_arm_L)
#                if prop != 1:
#                    self.report({'ERROR'}, 'Only works in FK mode')  
#                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':

            check_bones = ['hand_ik_ctrl_L', 'hand_fk_L', 'elbow_pole_L', 'snap_elbow_pole_fk_L', 'hand_fk_L', 'hand_ik_ctrl_L', 'hand_ik_pivot_point_L']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['hand_ik_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_ik_pivot_point_L'].bone.select = 0                 
            sel_act_bones('hand_ik_ctrl_L', 'hand_fk_L', 'loc')         
            for b in p_bones:
                if ('properties_arm_L' in b.name):
                    prop = int(b.space_hand_L)
                    if prop == 0:            
                        sel_act_bones('hand_ik_ctrl_L', 'hand_fk_L', 'rot')                                                              
            sel_act_bones('elbow_pole_L', 'snap_elbow_pole_fk_L', 'loc')  

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_ik_ctrl_L', 'elbow_pole_L', 'hand_ik_pivot_point_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False            

        #Quadruped   
        if arm_data['rig_type'] == 'Quadruped':        

            check_bones = ['hand_sole_ctrl_L', 'snap_hand_sole_ctrl_fk_L', 'hand_ik_ctrl_L', 'hand_fk_L', 'fings_ik_ctrl_L', 'snap_fings_ctrl_fk_L', 'fings_ik_ctrl_mid_L', 'snap_fing_ctrl_mid_fk_L', 'elbow_pole_L', 'snap_elbow_pole_fk_L', 'hand_sole_pivot_point_L', 'hand_roll_ctrl_L', 'fing_roll_1_L', 'fing_roll_2_L']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['hand_sole_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_sole_pivot_point_L'].bone.select = 0  
            p_bones['hand_roll_ctrl_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_roll_ctrl_L'].bone.select = 0     
            p_bones['fing_roll_1_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_1_L'].bone.select = 0     
            p_bones['fing_roll_2_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_2_L'].bone.select = 0                                                                                                  
            sel_act_bones('hand_sole_ctrl_L', 'snap_hand_sole_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('hand_ik_ctrl_L', 'hand_fk_L', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_L', 'snap_fings_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_mid_L', 'snap_fing_ctrl_mid_fk_L', 'loc_rot')       
            sel_act_bones('elbow_pole_L', 'snap_elbow_pole_fk_L', 'loc')                               

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_sole_ctrl_L', 'elbow_pole_L', 'fings_ik_ctrl_L', 'fings_ik_ctrl_mid_L', 'hand_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                  

        return {"FINISHED"}  

##### ARM R #####


class Operator_Arm_R_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "arm_r_snap.ik_fk"   
    bl_label = "BlenRig Arm_R Snap IK FK"    
    bl_description = "Prepare seamless switch to FK"       
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_arm_R' == b.name):
#                prop = int(b.ik_arm_R)
#                if prop != 0:
#                    self.report({'ERROR'}, 'Only works in IK mode')  
#                    return {"CANCELLED"}                  

        # Biped
        if arm_data['rig_type'] == 'Biped':

            check_bones = ['arm_fk_R', 'arm_ik_R', 'forearm_fk_R', 'forearm_ik_R', 'hand_fk_R', 'hand_ik_ctrl_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_R', 'arm_ik_R', 'rot')         
            sel_act_bones('forearm_fk_R', 'forearm_ik_R', 'rot')  
            for b in p_bones:
                if ('properties_arm_R' in b.name):
                    prop = int(b.space_hand_R)
                    if prop == 1:            
                        sel_act_bones('hand_fk_R', 'hand_ik_ctrl_R', 'rot')                                

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_R', 'forearm_fk_R', 'hand_fk_R', 'hand_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False       
        
        #Quadruped    
        if arm_data['rig_type'] == 'Quadruped':     

            check_bones = ['arm_fk_R', 'arm_ik_R', 'forearm_fk_R', 'forearm_ik_R', 'hand_fk_R', 'hand_ik_ctrl_R', 'carpal_fk_R', 'carpal_ik_R', 'fing_1_fk_R', 'fing_1_ik_R', 'fing_2_fk_R', 'fing_2_ik_R']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_R', 'arm_ik_R', 'rot')         
            sel_act_bones('forearm_fk_R', 'forearm_ik_R', 'rot')  
            sel_act_bones('carpal_fk_R', 'carpal_ik_R', 'rot')               
            sel_act_bones('hand_fk_R', 'hand_ik_ctrl_R', 'rot') 
            sel_act_bones('fing_1_fk_R', 'fing_1_ik_R', 'rot')  
            sel_act_bones('fing_2_fk_R', 'fing_2_ik_R', 'rot')                  

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_R', 'forearm_fk_R', 'hand_fk_R', 'hand_ik_ctrl_R', 'carpal_fk_R', 'fing_1_fk_R', 'fing_2_fk_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                  

        return {"FINISHED"}    

class Operator_Arm_R_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "arm_r_snap.fk_ik"   
    bl_label = "BlenRig Arm_R Snap FK IK"    
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_arm_R' == b.name):
#                prop = int(b.ik_arm_R)
#                if prop != 1:
#                    self.report({'ERROR'}, 'Only works in FK mode')  
#                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':

            check_bones = ['hand_ik_ctrl_R', 'hand_fk_R', 'elbow_pole_R', 'snap_elbow_pole_fk_R', 'hand_fk_R', 'hand_ik_ctrl_R', 'hand_ik_pivot_point_R']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['hand_ik_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_ik_pivot_point_R'].bone.select = 0                 
            sel_act_bones('hand_ik_ctrl_R', 'hand_fk_R', 'loc')         
            for b in p_bones:
                if ('properties_arm_R' in b.name):
                    prop = int(b.space_hand_R)
                    if prop == 0:            
                        sel_act_bones('hand_ik_ctrl_R', 'hand_fk_R', 'rot')                                                              
            sel_act_bones('elbow_pole_R', 'snap_elbow_pole_fk_R', 'loc')  

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_ik_ctrl_R', 'elbow_pole_R', 'hand_ik_pivot_point_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False            

        #Quadruped   
        if arm_data['rig_type'] == 'Quadruped':        

            check_bones = ['hand_sole_ctrl_R', 'snap_hand_sole_ctrl_fk_R', 'hand_ik_ctrl_R', 'hand_fk_R', 'fings_ik_ctrl_R', 'snap_fings_ctrl_fk_R', 'fings_ik_ctrl_mid_R', 'snap_fing_ctrl_mid_fk_R', 'elbow_pole_R', 'snap_elbow_pole_fk_R', 'hand_sole_pivot_point_R', 'hand_roll_ctrl_R', 'fing_roll_1_R', 'fing_roll_2_R']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['hand_sole_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_sole_pivot_point_R'].bone.select = 0  
            p_bones['hand_roll_ctrl_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_roll_ctrl_R'].bone.select = 0     
            p_bones['fing_roll_1_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_1_R'].bone.select = 0     
            p_bones['fing_roll_2_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_2_R'].bone.select = 0                                                                                                  
            sel_act_bones('hand_sole_ctrl_R', 'snap_hand_sole_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('hand_ik_ctrl_R', 'hand_fk_R', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_R', 'snap_fings_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_mid_R', 'snap_fing_ctrl_mid_fk_R', 'loc_rot')       
            sel_act_bones('elbow_pole_R', 'snap_elbow_pole_fk_R', 'loc')                               

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_sole_ctrl_R', 'elbow_pole_R', 'fings_ik_ctrl_R', 'fings_ik_ctrl_mid_R', 'hand_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False              

        return {"FINISHED"}  

##### LEG L #####


class Operator_Leg_L_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "leg_l_snap.ik_fk"   
    bl_label = "BlenRig Leg_L Snap IK FK"     
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_leg_L' == b.name):
#                prop = int(b.ik_leg_L)
#                if prop != 0:
#                    self.report({'ERROR'}, 'Only works in IK mode')  
#                    return {"CANCELLED"}   

        #Biped
        if arm_data['rig_type'] == 'Biped':                               

            check_bones = ['thigh_fk_L', 'thigh_ik_L', 'shin_fk_L', 'shin_ik_L', 'foot_fk_L', 'foot_ik_L', 'toe_1_fk_L', 'toe_1_ik_L', 'toe_2_fk_L', 'toe_2_ik_L' ]

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_L', 'thigh_ik_L', 'rot')         
            sel_act_bones('shin_fk_L', 'shin_ik_L', 'rot')  
            sel_act_bones('foot_fk_L', 'foot_ik_L', 'rot')    
            sel_act_bones('toe_1_fk_L', 'toe_1_ik_L', 'rot')  
            sel_act_bones('toe_2_fk_L', 'toe_2_ik_L', 'rot')                                           

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_L', 'shin_fk_L', 'foot_fk_L', 'toe_1_fk_L', 'toe_2_fk_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False 

        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':                               

            check_bones = ['thigh_fk_L', 'thigh_ik_L', 'shin_fk_L', 'shin_ik_L', 'tarsal_fk_L', 'tarsal_ik_L', 'foot_fk_L', 'foot_ik_L', 'toe_1_fk_L', 'toe_1_ik_L', 'toe_2_fk_L', 'toe_2_ik_L' ]

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_L', 'thigh_ik_L', 'rot')         
            sel_act_bones('shin_fk_L', 'shin_ik_L', 'rot')  
            sel_act_bones('tarsal_fk_L', 'tarsal_ik_L', 'rot')              
            sel_act_bones('foot_fk_L', 'foot_ik_L', 'rot')    
            sel_act_bones('toe_1_fk_L', 'toe_1_ik_L', 'rot')  
            sel_act_bones('toe_2_fk_L', 'toe_2_ik_L', 'rot')                                           

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_L', 'shin_fk_L', 'tarsal_fk_L', 'foot_fk_L', 'toe_1_fk_L', 'toe_2_fk_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                                 

        return {"FINISHED"}        

class Operator_Leg_L_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "leg_l_snap.fk_ik"   
    bl_label = "BlenRig Leg_L Snap FK IK"  
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_leg_L' == b.name):
#                prop = int(b.ik_leg_L)
#                if prop != 1:
#                    self.report({'ERROR'}, 'Only works in FK mode')  
#                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':  

            check_bones = ['sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'foot_ik_ctrl_L', 'foot_fk_L', 'toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'knee_pole_L', 'snap_knee_fk_L', 'sole_pivot_point_L', 'foot_roll_ctrl_L', 'toe_roll_1_L', 'toe_roll_2_L']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_L'].bone.select = 0  
            p_bones['foot_roll_ctrl_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_L'].bone.select = 0     
            p_bones['toe_roll_1_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_L'].bone.select = 0     
            p_bones['toe_roll_2_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_L'].bone.select = 0                                                                                                  
            sel_act_bones('sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_L', 'foot_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'loc_rot')       
            sel_act_bones('knee_pole_L', 'snap_knee_fk_L', 'loc')                               

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_L', 'knee_pole_L', 'toes_ik_ctrl_L', 'toes_ik_ctrl_mid_L', 'foot_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False         

        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':      

            check_bones = ['sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'foot_ik_ctrl_L', 'foot_fk_L', 'toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'thigh_fk_L', 'thigh_ik_L', 'knee_pole_L', 'snap_knee_fk_L', 'sole_pivot_point_L', 'foot_roll_ctrl_L', 'toe_roll_1_L', 'toe_roll_2_L']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_L'].bone.select = 0  
            p_bones['foot_roll_ctrl_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_L'].bone.select = 0     
            p_bones['toe_roll_1_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_L'].bone.select = 0     
            p_bones['toe_roll_2_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_L'].bone.select = 0         
            sel_act_bones('thigh_ik_L', 'thigh_fk_L', 'rot')                                                                                           
            sel_act_bones('sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_L', 'foot_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'loc_rot')       
            sel_act_bones('knee_pole_L', 'snap_knee_fk_L', 'loc')                               

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_L', 'knee_pole_L', 'toes_ik_ctrl_L', 'toes_ik_ctrl_mid_L', 'foot_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                                       

        return {"FINISHED"}      

##### LEG R #####


class Operator_Leg_R_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "leg_r_snap.ik_fk"   
    bl_label = "BlenRig Leg_R Snap IK FK"     
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_Leg_R' == b.name):
#                prop = int(b.ik_leg_R)
#                if prop != 0:
#                    self.report({'ERROR'}, 'Only works in IK mode')  
#                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':                               

            check_bones = ['thigh_fk_R', 'thigh_ik_R', 'shin_fk_R', 'shin_ik_R', 'foot_fk_R', 'foot_ik_R', 'toe_1_fk_R', 'toe_1_ik_R', 'toe_2_fk_R', 'toe_2_ik_R' ]

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_R', 'thigh_ik_R', 'rot')         
            sel_act_bones('shin_fk_R', 'shin_ik_R', 'rot')  
            sel_act_bones('foot_fk_R', 'foot_ik_R', 'rot')    
            sel_act_bones('toe_1_fk_R', 'toe_1_ik_R', 'rot')  
            sel_act_bones('toe_2_fk_R', 'toe_2_ik_R', 'rot')                                           

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_R', 'shin_fk_R', 'foot_fk_R', 'toe_1_fk_R', 'toe_2_fk_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False 

        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':                               

            check_bones = ['thigh_fk_R', 'thigh_ik_R', 'shin_fk_R', 'shin_ik_R', 'tarsal_fk_R', 'tarsal_ik_R', 'foot_fk_R', 'foot_ik_R', 'toe_1_fk_R', 'toe_1_ik_R', 'toe_2_fk_R', 'toe_2_ik_R' ]

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_R', 'thigh_ik_R', 'rot')         
            sel_act_bones('shin_fk_R', 'shin_ik_R', 'rot')  
            sel_act_bones('tarsal_fk_R', 'tarsal_ik_R', 'rot')              
            sel_act_bones('foot_fk_R', 'foot_ik_R', 'rot')    
            sel_act_bones('toe_1_fk_R', 'toe_1_ik_R', 'rot')  
            sel_act_bones('toe_2_fk_R', 'toe_2_ik_R', 'rot')                                           

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_R', 'shin_fk_R', 'tarsal_fk_R', 'foot_fk_R', 'toe_1_fk_R', 'toe_2_fk_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False           

        return {"FINISHED"}        

class Operator_Leg_R_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "leg_r_snap.fk_ik"   
    bl_label = "BlenRig Leg_R Snap FK IK"  
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

#        for b in p_bones:
#            if ('properties_leg_R' == b.name):
#                prop = int(b.ik_leg_R)
#                if prop != 1:
#                    self.report({'ERROR'}, 'Only works in FK mode')  
#                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':  

            check_bones = ['sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'foot_ik_ctrl_R', 'foot_fk_R', 'toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'knee_pole_R', 'snap_knee_fk_R', 'sole_pivot_point_R', 'foot_roll_ctrl_R', 'toe_roll_1_R', 'toe_roll_2_R']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_R'].bone.select = 0  
            p_bones['foot_roll_ctrl_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_R'].bone.select = 0     
            p_bones['toe_roll_1_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_R'].bone.select = 0     
            p_bones['toe_roll_2_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_R'].bone.select = 0                                                                                                  
            sel_act_bones('sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_R', 'foot_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'loc_rot')       
            sel_act_bones('knee_pole_R', 'snap_knee_fk_R', 'loc')                               

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_R', 'knee_pole_R', 'toes_ik_ctrl_R', 'toes_ik_ctrl_mid_R', 'foot_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False         

        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':      

            check_bones = ['sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'foot_ik_ctrl_R', 'foot_fk_R', 'toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'thigh_fk_R', 'thigh_ik_R', 'knee_pole_R', 'snap_knee_fk_R', 'sole_pivot_point_R', 'foot_roll_ctrl_R', 'toe_roll_1_R', 'toe_roll_2_R']

            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 

            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            

            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_R'].bone.select = 0  
            p_bones['foot_roll_ctrl_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_R'].bone.select = 0     
            p_bones['toe_roll_1_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_R'].bone.select = 0     
            p_bones['toe_roll_2_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_R'].bone.select = 0         
            sel_act_bones('thigh_ik_R', 'thigh_fk_R', 'rot')                                                                                           
            sel_act_bones('sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_R', 'foot_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'loc_rot')       
            sel_act_bones('knee_pole_R', 'snap_knee_fk_R', 'loc')                               

            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_R', 'knee_pole_R', 'toes_ik_ctrl_R', 'toes_ik_ctrl_mid_R', 'foot_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False               

        return {"FINISHED"}
import bpy
from math import radians

#################################### BLENRIG SET CONSTRAINTS VALUES OPERATORS ####################################################

################### SET FUNCTIONS ##################################

#Function for setting values on Action Constraints

def Set_Movement_Ranges_Actions(self, context, b_name, prop_name, C_name, min_factor, max_factor):

        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        p_bones = bpy.context.active_object.pose.bones
        constraint_value = []

        for b in p_bones:
            if b.name == b_name:
                for cust_prop in b.items():
                    if cust_prop[0] == prop_name:
                        constraint_value = []
                        constraint_value.append(cust_prop[1])
                        for b in p_bones:
                            for C in b.constraints:
                                if C.type == 'ACTION':
                                    if C.name == C_name:
                                        C.min = constraint_value[0] * min_factor
                                        C.max = constraint_value[0] * max_factor

#Functions for setting values on Realistic Joints Transform Constraints

def Set_RJ_Transforms_Limbs(self, context, b_name, prop_name, C_name, x_loc_factor, z_loc_factor, x_rot_factor, z_rot_factor):

        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        p_bones = bpy.context.active_object.pose.bones
        constraint_value = []

        for b in p_bones:
            if b.name == b_name:
                for cust_prop in b.items():
                    if cust_prop[0] == prop_name:
                        constraint_value = []
                        constraint_value.append(cust_prop[1])
                        for b in p_bones:
                            for C in b.constraints:
                                if C.type == 'TRANSFORM':
                                    if C.name == C_name:
                                        C.to_max_x = constraint_value[0] * x_loc_factor
                                        C.to_max_z = constraint_value[0] * z_loc_factor
                                        C.to_max_x_rot = radians(constraint_value[0] * x_rot_factor)
                                        C.to_max_z_rot = radians(constraint_value[0] * z_rot_factor)

def Set_RJ_Transforms_Fing_Toes(self, context, b_name, prop_name, C_name, z_loc_factor, x_rot_factor, Loc_Array_n, Rot_Array_n):

        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        p_bones = bpy.context.active_object.pose.bones
        constraint_value = []

        for b in p_bones:
            if b.name == b_name:
                for cust_prop in b.items():
                    if cust_prop[0] == prop_name:
                        constraint_value = []
                        constraint_value.append(cust_prop[1][0])
                        constraint_value.append(cust_prop[1][1])
                        constraint_value.append(cust_prop[1][2])
                        for b in p_bones:
                            for C in b.constraints:
                                if C.type == 'TRANSFORM':
                                    if C.name == C_name:
                                        C.to_max_z = constraint_value[Loc_Array_n] * z_loc_factor
                                        C.to_max_x_rot = radians(constraint_value[Rot_Array_n] * x_rot_factor)

#Function for setting values on Volume Variation Constraints

def Set_Volume_Variation_Stretch_To(self, context, b_name, prop_name, C_name):

        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        p_bones = bpy.context.active_object.pose.bones
        constraint_value = []

        for b in p_bones:
            if b.name == b_name:
                for cust_prop in b.items():
                    if cust_prop[0] == prop_name:
                        constraint_value = []
                        constraint_value.append(cust_prop[1])
                        for b in p_bones:
                            for C in b.constraints:
                                if C.type == 'STRETCH_TO':
                                    if C.name == C_name:
                                        C.bulge = constraint_value[0]


######## SET OPERATORS ###########################################

### FACIAL CONSTRAINTS ####

#EYELIDS

class Operator_Set_Eyelids(bpy.types.Operator):
    bl_idname = "operator.set_eyelids"
    bl_label = "BlenRig Set values for Facial Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Eyelid Up L
        Set_Movement_Ranges_Actions(self, context, 'eyelid_up_ctrl_L', 'EYELID_UP_LIMIT_L', 'Eyelid_Upper_Up_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'eyelid_up_ctrl_L', 'EYELID_DOWN_LIMIT_L', 'Eyelid_Upper_Down_L_NOREP', 0, -1)
        #Eyelid Up R
        Set_Movement_Ranges_Actions(self, context, 'eyelid_up_ctrl_R', 'EYELID_UP_LIMIT_R', 'Eyelid_Upper_Up_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'eyelid_up_ctrl_R', 'EYELID_DOWN_LIMIT_R', 'Eyelid_Upper_Down_R_NOREP', 0, -1)
        #Eyelid Low L
        Set_Movement_Ranges_Actions(self, context, 'eyelid_low_ctrl_L', 'EYELID_UP_LIMIT_L', 'Eyelid_Lower_Up_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'eyelid_low_ctrl_L', 'EYELID_DOWN_LIMIT_L', 'Eyelid_Lower_Down_L_NOREP', 0, -1)
        #Eyelid Low R
        Set_Movement_Ranges_Actions(self, context, 'eyelid_low_ctrl_R', 'EYELID_UP_LIMIT_R', 'Eyelid_Lower_Up_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'eyelid_low_ctrl_R', 'EYELID_DOWN_LIMIT_R', 'Eyelid_Lower_Down_R_NOREP', 0, -1)
        return {"FINISHED"}

#CHEEKS

class Operator_Set_Cheeks(bpy.types.Operator):
    bl_idname = "operator.set_cheeks"
    bl_label = "BlenRig Set values for Facial Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Cheeks L
        Set_Movement_Ranges_Actions(self, context, 'cheek_ctrl_L', 'CHEEK_UP_LIMIT_L', 'Cheek_Up_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'cheek_ctrl_L', 'CHEEK_DOWN_LIMIT_L', 'Cheek_Down_L_NOREP', 0, -1)
        #Cheeks R
        Set_Movement_Ranges_Actions(self, context, 'cheek_ctrl_R', 'CHEEK_UP_LIMIT_R', 'Cheek_Up_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'cheek_ctrl_R', 'CHEEK_DOWN_LIMIT_R', 'Cheek_Down_R_NOREP', 0, -1)
        return {"FINISHED"}

#FROWNS

class Operator_Set_Frowns(bpy.types.Operator):
    bl_idname = "operator.set_frowns"
    bl_label = "BlenRig Set values for Facial Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Nose Frown L
        Set_Movement_Ranges_Actions(self, context, 'nose_frown_ctrl_L', 'FROWN_LIMIT_L', 'Nose_Frown_L_NOREP', -1, 1)
        #Mouth Frown L
        Set_Movement_Ranges_Actions(self, context, 'mouth_frown_ctrl_L', 'FROWN_LIMIT_L', 'Mouth_Frown_L_NOREP', 0, -1)
        #Nose Frown R
        Set_Movement_Ranges_Actions(self, context, 'nose_frown_ctrl_R', 'FROWN_LIMIT_R', 'Nose_Frown_R_NOREP', -1, 1)
        #Mouth Frown R
        Set_Movement_Ranges_Actions(self, context, 'mouth_frown_ctrl_R', 'FROWN_LIMIT_R', 'Mouth_Frown_R_NOREP', 0, -1)
        #Chin Frown
        Set_Movement_Ranges_Actions(self, context, 'chin_frown_ctrl', 'FROWN_LIMIT', 'Chin_Frown_NOREP', -1, 1)
        return {"FINISHED"}

#MOUTH CORNERS

class Operator_Set_Mouth_Corners(bpy.types.Operator):
    bl_idname = "operator.set_mouth_corners"
    bl_label = "BlenRig Set values for Facial Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Mouth Corner L
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'IN_LIMIT_L', 'Mouth_Corner_In_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'IN_LIMIT_L', 'U_Up_Narrow_Corrective_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'OUT_LIMIT_L', 'Mouth_Corner_Out_L_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'UP_LIMIT_L', 'Mouth_Corner_Up_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'UP_LIMIT_L', 'Mouth_Corner_Up_Out_Corrective_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'DOWN_LIMIT_L', 'Mouth_Corner_Down_L_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'DOWN_LIMIT_L', 'Mouth_Corner_Down_Out_Corrective_L_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'FORW_LIMIT_L', 'Mouth_Corner_Forw_L_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_L', 'BACK_LIMIT_L', 'Mouth_Corner_Back_L_NOREP', 0, -1)
        #Mouth Corner R
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'IN_LIMIT_R', 'Mouth_Corner_In_R_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'IN_LIMIT_R', 'U_Up_Narrow_Corrective_R_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'OUT_LIMIT_R', 'Mouth_Corner_Out_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'OUT_LIMIT_R', 'Mouth_Corner_Up_Out_Corrective_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'UP_LIMIT_R', 'Mouth_Corner_Up_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'UP_LIMIT_R', 'Mouth_Corner_Up_Out_Corrective_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'DOWN_LIMIT_R', 'Mouth_Corner_Down_R_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'DOWN_LIMIT_R', 'Mouth_Corner_Down_Out_Corrective_R_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'FORW_LIMIT_R', 'Mouth_Corner_Forw_R_NOREP', 0, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_corner_R', 'BACK_LIMIT_R', 'Mouth_Corner_Back_R_NOREP', 0, -1)
        return {"FINISHED"}

#MOUTH CTRL

class Operator_Set_Mouth_Ctrl(bpy.types.Operator):
    bl_idname = "operator.set_mouth_ctrl"
    bl_label = "BlenRig Set values for Facial Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Mouth Ctrl
        # Set_Movement_Ranges_Actions(self, context, 'mouth_ctrl', 'IN_LIMIT', 'Mouth_Corner_In_L_NOREP', 0, 1)
        # Set_Movement_Ranges_Actions(self, context, 'mouth_ctrl', 'OUT_LIMIT', 'Mouth_Corner_Out_L_NOREP', 0, -1)
        # Set_Movement_Ranges_Actions(self, context, 'mouth_ctrl', 'SMILE_LIMIT', 'Mouth_Corner_Up_L_NOREP', 0, 1)
        # Set_Movement_Ranges_Actions(self, context, 'mouth_ctrl', 'JAW_ROTATION', 'Mouth_Corner_Down_L_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_ctrl', 'U_M_CTRL_LIMIT', 'U_O_M_Up_NOREP', -1, 1)
        Set_Movement_Ranges_Actions(self, context, 'mouth_ctrl', 'U_M_CTRL_LIMIT', 'U_O_M_Low_NOREP', -1, 1)
        #Jaw
        Set_Movement_Ranges_Actions(self, context, 'maxi', 'JAW_DOWN_LIMIT', 'Maxi_Down_NOREP', 0, -1)
        Set_Movement_Ranges_Actions(self, context, 'maxi', 'JAW_UP_LIMIT', 'Maxi_Up_NOREP', 0, 1)
        return {"FINISHED"}
        pose.bones["mouth_ctrl"]["U_M_CTRL_LIMIT"]

### REALISTIC JOINTS CONSTRAINTS ####

class Operator_Set_RJ_Transforms(bpy.types.Operator):
    bl_idname = "operator.set_rj_transforms"
    bl_label = "BlenRig Set values for Realistic Joints Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Arms L
        Set_RJ_Transforms_Limbs(self, context, 'properties_arm_L', 'realistic_joints_elbow_loc_L', 'Elbow_RJ_Loc_L_NOREP', 0, 1, 0, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_arm_L', 'realistic_joints_elbow_rot_L', 'Elbow_RJ_Rot_L_NOREP', 0, 0, -1, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_arm_L', 'realistic_joints_wrist_rot_L', 'Wrist_RJ_Rot_L_NOREP', 0, 0, -1, 1)
        #Arms R
        Set_RJ_Transforms_Limbs(self, context, 'properties_arm_R', 'realistic_joints_elbow_loc_R', 'Elbow_RJ_Loc_R_NOREP', 0, 1, 0, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_arm_R', 'realistic_joints_elbow_rot_R', 'Elbow_RJ_Rot_R_NOREP', 0, 0, -1, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_arm_R', 'realistic_joints_wrist_rot_R', 'Wrist_RJ_Rot_R_NOREP', 0, 0, 1, -1)
        #Legs L
        Set_RJ_Transforms_Limbs(self, context, 'properties_leg_L', 'realistic_joints_knee_loc_L', 'Knee_RJ_Loc_L_NOREP', 0, 1, 0, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_leg_L', 'realistic_joints_knee_rot_L', 'Knee_RJ_Rot_L_NOREP', 0, 0, -1, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_leg_L', 'realistic_joints_ankle_rot_L', 'Ankle_RJ_Rot_L_NOREP', 0, 0, -1, -1)
        #Legs R
        Set_RJ_Transforms_Limbs(self, context, 'properties_leg_R', 'realistic_joints_knee_loc_R', 'Knee_RJ_Loc_R_NOREP', 0, 1, 0, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_leg_R', 'realistic_joints_knee_rot_R', 'Knee_RJ_Rot_R_NOREP', 0, 0, -1, 0)
        Set_RJ_Transforms_Limbs(self, context, 'properties_leg_R', 'realistic_joints_ankle_rot_R', 'Ankle_RJ_Rot_R_NOREP', 0, 0, -1, -1)
        #Fingers L
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_L', 'realistic_joints_fingers_rot_L', 'Fing_1_RJ_Rot_L_NOREP', 0, -1, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_L', 'realistic_joints_fingers_rot_L', 'Fing_2_RJ_Rot_L_NOREP', 0, -1, 0, 1)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_L', 'realistic_joints_fingers_rot_L', 'Fing_3_RJ_Rot_L_NOREP', 0, -1, 0, 2)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_L', 'realistic_joints_fingers_loc_L', 'Fing_2_RJ_Loc_L_NOREP', 1, 0, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_L', 'realistic_joints_fingers_loc_L', 'Fing_3_RJ_Loc_L_NOREP', 1, 0, 1, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_L', 'realistic_joints_fingers_loc_L', 'Fing_4_RJ_Loc_L_NOREP', 1, 0, 2, 0)
        #Fingers R
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_R', 'realistic_joints_fingers_rot_R', 'Fing_1_RJ_Rot_R_NOREP', 0, -1, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_R', 'realistic_joints_fingers_rot_R', 'Fing_2_RJ_Rot_R_NOREP', 0, -1, 0, 1)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_R', 'realistic_joints_fingers_rot_R', 'Fing_3_RJ_Rot_R_NOREP', 0, -1, 0, 2)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_R', 'realistic_joints_fingers_loc_R', 'Fing_2_RJ_Loc_R_NOREP', 1, 0, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_R', 'realistic_joints_fingers_loc_R', 'Fing_3_RJ_Loc_R_NOREP', 1, 0, 1, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_arm_R', 'realistic_joints_fingers_loc_R', 'Fing_4_RJ_Loc_R_NOREP', 1, 0, 2, 0)
        #Toes L
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_L', 'realistic_joints_toes_rot_L', 'Toes_1_RJ_Rot_L_NOREP', 0, -1, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_L', 'realistic_joints_toes_rot_L', 'Toes_2_RJ_Rot_L_NOREP', 0, -1, 0, 1)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_L', 'realistic_joints_toes_rot_L', 'Toes_3_RJ_Rot_L_NOREP', 0, -1, 0, 2)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_L', 'realistic_joints_toes_loc_L', 'Toes_2_RJ_Loc_L_NOREP', 1, 0, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_L', 'realistic_joints_toes_loc_L', 'Toes_3_RJ_Loc_L_NOREP', 1, 0, 1, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_L', 'realistic_joints_toes_loc_L', 'Toes_4_RJ_Loc_L_NOREP', 1, 0, 2, 0)
        #Toes R
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_R', 'realistic_joints_toes_rot_R', 'Toes_1_RJ_Rot_R_NOREP', 0, -1, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_R', 'realistic_joints_toes_rot_R', 'Toes_2_RJ_Rot_R_NOREP', 0, -1, 0, 1)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_R', 'realistic_joints_toes_rot_R', 'Toes_3_RJ_Rot_R_NOREP', 0, -1, 0, 2)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_R', 'realistic_joints_toes_loc_R', 'Toes_2_RJ_Loc_R_NOREP', 1, 0, 0, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_R', 'realistic_joints_toes_loc_R', 'Toes_3_RJ_Loc_R_NOREP', 1, 0, 1, 0)
        Set_RJ_Transforms_Fing_Toes(self, context, 'properties_leg_R', 'realistic_joints_toes_loc_R', 'Toes_4_RJ_Loc_R_NOREP', 1, 0, 2, 0)
        return {"FINISHED"}

### REALISTIC JOINTS CONSTRAINTS ####

class Operator_Set_Volume_Variation(bpy.types.Operator):
    bl_idname = "operator.set_volume_variation"
    bl_label = "BlenRig Set values for Volume Variation Constraints"
    bl_description = "Set Defined Ranges to Related Constraints"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def execute(self, context):
        #Arms L
        Set_Volume_Variation_Stretch_To(self, context, 'properties_arm_L', 'volume_variation_arm_L', 'Vol_Var_Arm_L_Stretch_To')
        Set_Volume_Variation_Stretch_To(self, context, 'properties_arm_L', 'volume_variation_fingers_L', 'Vol_Var_Hand_L_Stretch_To')
        #Arms R
        Set_Volume_Variation_Stretch_To(self, context, 'properties_arm_R', 'volume_variation_arm_R', 'Vol_Var_Arm_R_Stretch_To')
        Set_Volume_Variation_Stretch_To(self, context, 'properties_arm_R', 'volume_variation_fingers_R', 'Vol_Var_Hand_R_Stretch_To')
        #Legs L
        Set_Volume_Variation_Stretch_To(self, context, 'properties_leg_L', 'volume_variation_leg_L', 'Vol_Var_Leg_L_Stretch_To')
        Set_Volume_Variation_Stretch_To(self, context, 'properties_leg_L', 'volume_variation_toes_L', 'Vol_Var_Foot_L_Stretch_To')
        #Legs R
        Set_Volume_Variation_Stretch_To(self, context, 'properties_leg_R', 'volume_variation_leg_R', 'Vol_Var_Leg_R_Stretch_To')
        Set_Volume_Variation_Stretch_To(self, context, 'properties_leg_R', 'volume_variation_toes_R', 'Vol_Var_Foot_R_Stretch_To')
        #Torso
        Set_Volume_Variation_Stretch_To(self, context, 'properties_torso', 'volume_variation_torso', 'Vol_Var_Torso_Stretch_To')
        #Neck
        Set_Volume_Variation_Stretch_To(self, context, 'properties_head', 'volume_variation_neck', 'Vol_Var_Neck_Stretch_To')
        #Head
        Set_Volume_Variation_Stretch_To(self, context, 'properties_head', 'volume_variation_head', 'Vol_Var_Head_Stretch_To')
        return {"FINISHED"}
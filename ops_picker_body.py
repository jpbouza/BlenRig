import bpy

#################################### BLENRIG BODY PICKER OPERATORS ####################################################

################### VIEW OPERATOR ##################################



class Operator_Zoom_Selected(bpy.types.Operator):
    bl_idname = "operator.zoom"
    bl_label = "BlenRig Zoom to Selected"
    bl_description = "Zoom to selected / View All"

    def invoke(self, context, event):
        #Context Override
        areas  = [area for area in bpy.context.screen.areas if area.type == 'VIEW_3D']

        if areas:
            regions = [region for region in areas[0].regions if region.type == 'WINDOW']

            if regions:
                override = {'area': areas[0],
                            'region': regions[0]}

        if event.ctrl == False and event.shift == False:
            bpy.ops.view3d.view_selected(override, use_all_regions=False)
        else:
            bpy.ops.view3d.view_all(override, center=False)
        return {"FINISHED"}

################### SELECTION OPERATORS ##################################

#Generic Selection Operator Structure

def select_op(self, context, event, b_name): #b_name will be replaced by the actual bone name
    armobj = bpy.context.active_object
    arm = bpy.context.active_object.data
    if (b_name in armobj.pose.bones):        # this line is replaced with actual bone name
        #Target Bone
        Bone = armobj.pose.bones[b_name]    # this line is replaced with actual bone name
        #Check if CTRL or SHIFT are pressed
        if event.ctrl == True or event.shift == True:
            #Get previously selected bones
            selected = [b.name for b in bpy.context.selected_pose_bones]
            #Set target bone as active
            for b in armobj.pose.bones:
                b.bone.select = 0
            arm.bones.active = Bone.bone
            #Reselect previously selected bones
            for b in armobj.pose.bones:
                if (b.name in selected):
                    b.bone.select = 1
        else:
            for b in armobj.pose.bones:
                b.bone.select = 0
            arm.bones.active = Bone.bone

######## BODY PICKER OPERATORS ###########################################

#Insert Keyframes to main properties

class Operator_Keyframe_Main_Props(bpy.types.Operator):

    bl_idname = "keyframe.main_props"
    bl_label = "BlenRig Insert Keyframes To Main Animation Properties"
    bl_description = "Insert Keyframes to main animation properties"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):
        pbones = bpy.context.active_object.pose.bones
        #Head
        pbones["properties_head"].keyframe_insert(data_path='look_switch')
        pbones["properties_head"].keyframe_insert(data_path='space_head')
        pbones["properties_head"].keyframe_insert(data_path='space_neck')
        #Arm_L
        pbones["properties_arm_L"].keyframe_insert(data_path='ik_arm_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_arm_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='toon_arm_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='toggle_arm_ik_pole_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_arm_ik_pole_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='pin_elbow_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_hand_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_thumb_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_ind_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_mid_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_ring_L')
        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_lit_L')
        #Arm_R
        pbones["properties_arm_R"].keyframe_insert(data_path='ik_arm_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_arm_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='toon_arm_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='toggle_arm_ik_pole_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_arm_ik_pole_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='pin_elbow_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_hand_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_thumb_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_ind_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_mid_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_ring_R')
        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_lit_R')
        #Leg_L
        pbones["properties_leg_L"].keyframe_insert(data_path='ik_leg_L')
        pbones["properties_leg_L"].keyframe_insert(data_path='space_leg_L')
        pbones["properties_leg_L"].keyframe_insert(data_path='toon_leg_L')
        pbones["properties_leg_L"].keyframe_insert(data_path='toggle_leg_ik_pole_L')
        pbones["properties_leg_L"].keyframe_insert(data_path='space_leg_ik_pole_L')
        pbones["properties_leg_L"].keyframe_insert(data_path='pin_knee_L')
        pbones["properties_leg_L"].keyframe_insert(data_path='ik_toes_all_L')
        #Leg_R
        pbones["properties_leg_R"].keyframe_insert(data_path='ik_leg_R')
        pbones["properties_leg_R"].keyframe_insert(data_path='space_leg_R')
        pbones["properties_leg_R"].keyframe_insert(data_path='toon_leg_R')
        pbones["properties_leg_R"].keyframe_insert(data_path='toggle_leg_ik_pole_R')
        pbones["properties_leg_R"].keyframe_insert(data_path='space_leg_ik_pole_R')
        pbones["properties_leg_R"].keyframe_insert(data_path='pin_knee_R')
        pbones["properties_leg_R"].keyframe_insert(data_path='ik_toes_all_R')
        #Extra Properties
        #Props
        pbones["properties_head"].keyframe_insert(data_path='["hat_free"]')
        pbones["properties_head"].keyframe_insert(data_path='["glasses_free"]')
        pbones["properties_arm_L"].keyframe_insert(data_path='["hand_accessory_L"]')
        pbones["properties_arm_R"].keyframe_insert(data_path='["hand_accessory_R"]')
        #Curve
        pbones["properties_arm_L"].keyframe_insert(data_path='["curved_arm_L"]')
        pbones["properties_arm_L"].keyframe_insert(data_path='["curved_arm_tweak_L"]')
        pbones["properties_leg_L"].keyframe_insert(data_path='["curved_leg_L"]')
        pbones["properties_leg_L"].keyframe_insert(data_path='["curved_leg_tweak_L"]')
        pbones["properties_arm_R"].keyframe_insert(data_path='["curved_arm_R"]')
        pbones["properties_arm_R"].keyframe_insert(data_path='["curved_arm_tweak_R"]')
        pbones["properties_leg_R"].keyframe_insert(data_path='["curved_leg_R"]')
        pbones["properties_leg_R"].keyframe_insert(data_path='["curved_leg_tweak_R"]')
        #Face
        pbones["properties_head"].keyframe_insert(data_path='["toon_teeth_up"]')
        pbones["properties_head"].keyframe_insert(data_path='["toon_teeth_low"]')
        pbones["properties_head"].keyframe_insert(data_path='["teeth_up_follow_mouth"]')
        pbones["properties_head"].keyframe_insert(data_path='["teeth_low_follow_mouth"]')
        pbones["properties_head"].keyframe_insert(data_path='["tongue_follow_mouth"]')

        return {"FINISHED"}

#HEAD

class Operator_Head_Stretch(bpy.types.Operator):
    bl_idname = "operator.head_stretch"
    bl_label = "BlenRig Select head_stretch"
    bl_description = "head_stretch"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_stretch")
        return {"FINISHED"}

class Operator_Head_Toon(bpy.types.Operator):
    bl_idname = "operator.head_toon"
    bl_label = "BlenRig Select head_toon"
    bl_description = "head_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_toon")
        return {"FINISHED"}

class Operator_Head_Top_Ctrl(bpy.types.Operator):
    bl_idname = "operator.head_top_ctrl"
    bl_label = "BlenRig Select head_top_ctrl"
    bl_description = "head_top_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_top_ctrl")
        return {"FINISHED"}

class Operator_Head_Mid_Ctrl(bpy.types.Operator):
    bl_idname = "operator.head_mid_ctrl"
    bl_label = "BlenRigSelect head_mid_ctrl"
    bl_description = "head_mid_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_mid_ctrl")
        return {"FINISHED"}

class Operator_Head_Mid_Curve(bpy.types.Operator):
    bl_idname = "operator.head_mid_curve"
    bl_label = "BlenRig Select head_mid_curve"
    bl_description = "head_mid_curve"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_mid_curve")
        return {"FINISHED"}

class Operator_Mouth_Str_Ctrl(bpy.types.Operator):
    bl_idname = "operator.mouth_str_ctrl"
    bl_label = "BlenRig Select mouth_str_ctrl"
    bl_description = "mouth_str_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_str_ctrl")
        return {"FINISHED"}

class Operator_Look_L(bpy.types.Operator):
    bl_idname = "operator.look_l"
    bl_label = "BlenRIg Select look_L"
    bl_description = "look_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "look_L")
        return {"FINISHED"}

class Operator_Look_R(bpy.types.Operator):
    bl_idname = "operator.look_r"
    bl_label = "BlenRIg Select look_R"
    bl_description = "look_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "look_R")
        return {"FINISHED"}

class Operator_Look(bpy.types.Operator):
    bl_idname = "operator.look"
    bl_label = "BlenRIg Select look"
    bl_description = "look"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "look")
        return {"FINISHED"}

class Operator_Head_FK(bpy.types.Operator):
    bl_idname = "operator.head_fk"
    bl_label = "BlenRIg Select head_fk"
    bl_description = "head_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_fk")
        return {"FINISHED"}

class Operator_Head_IK(bpy.types.Operator):
    bl_idname = "operator.head_ik_ctrl"
    bl_label = "BlenRIg Select head_ik_ctrl"
    bl_description = "head_ik_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)
        prop_hinge = int(bpy.context.active_object.pose.bones['properties_head'].hinge_head)
        if ('head_fk' and 'head_ik_ctrl' in armobj.pose.bones):
            #Target Bone
            if prop == 0 or prop_hinge == 1:
                Bone = armobj.pose.bones["head_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["head_fk"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Neck_4_Toon(bpy.types.Operator):
    bl_idname = "operator.neck_4_toon"
    bl_label = "BlenRig Select neck_4_toon"
    bl_description = "neck_4_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_4_toon")
        return {"FINISHED"}

class Operator_Face_Toon_Up(bpy.types.Operator):
    bl_idname = "operator.face_toon_up"
    bl_label = "BlenRig Select face_toon_up"
    bl_description = "face_toon_up"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "face_toon_up")
        return {"FINISHED"}

class Operator_Face_Toon_Mid(bpy.types.Operator):
    bl_idname = "operator.face_toon_mid"
    bl_label = "BlenRig Select face_toon_mid"
    bl_description = "face_toon_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "face_toon_mid")
        return {"FINISHED"}

class Operator_Face_Toon_Low(bpy.types.Operator):
    bl_idname = "operator.face_toon_low"
    bl_label = "BlenRig Select face_toon_low"
    bl_description = "face_toon_low"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "face_toon_low")
        return {"FINISHED"}

#NECK

class Operator_Neck_3_Legacy(bpy.types.Operator):
    bl_idname = "operator.neck_3_legacy"
    bl_label = "BlenRig Select neck_3"
    bl_description = "neck_3_ik_ctrl / neck_3_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)
        if ('neck_3_ik_ctrl' and 'neck_3_fk' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["neck_3_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["neck_3_fk"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Neck_2_Legacy(bpy.types.Operator):
    bl_idname = "operator.neck_2_legacy"
    bl_label = "BlenRig Select neck_2"
    bl_description = "neck_2_ik_ctrl / neck_2_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)
        if ('neck_2_ik_ctrl' and 'neck_2_fk' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["neck_2_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["neck_2_fk"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Neck_1(bpy.types.Operator):
    bl_idname = "operator.neck_1"
    bl_label = "BlenRig Select neck_1"
    bl_description = "neck_1_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_1_fk")
        return {"FINISHED"}

class Operator_Neck_2(bpy.types.Operator):
    bl_idname = "operator.neck_2"
    bl_label = "BlenRig Select neck_2"
    bl_description = "neck_2_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_2_fk")
        return {"FINISHED"}

class Operator_Neck_3(bpy.types.Operator):
    bl_idname = "operator.neck_3"
    bl_label = "BlenRig Select neck_3"
    bl_description = "neck_3_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_3_fk")
        return {"FINISHED"}

class Operator_Neck_Ctrl(bpy.types.Operator):
    bl_idname = "operator.neck_ctrl"
    bl_label = "BlenRig Select neck_fk_ctrl"
    bl_description = "neck_fk_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_fk_ctrl")
        return {"FINISHED"}

class Operator_Neck_3_Toon(bpy.types.Operator):
    bl_idname = "operator.neck_3_toon"
    bl_label = "BlenRig Select neck_3_toon"
    bl_description = "neck_3_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_3_toon")
        return {"FINISHED"}

class Operator_Neck_2_Toon(bpy.types.Operator):
    bl_idname = "operator.neck_2_toon"
    bl_label = "BlenRig Select neck_2_toon"
    bl_description = "neck_2_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "neck_2_toon")
        return {"FINISHED"}

class Operator_Neck_Ctrl_Legacy(bpy.types.Operator):
    bl_idname = "operator.neck_ctrl_legacy"
    bl_label = "BlenRig Select neck_ctrl"
    bl_description = "neck_ik_ctrl / neck_fk_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)
        if ('neck_ik_ctrl' and 'neck_fk_ctrl' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["neck_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["neck_fk_ctrl"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

#SHOULDERS

class Operator_Clavi_Toon_R(bpy.types.Operator):
    bl_idname = "operator.clavi_toon_r"
    bl_label = "BlenRig Select clavi_toon_R"
    bl_description = "clavi_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "clavi_toon_R")
        return {"FINISHED"}

class Operator_Shoulder_Rot_R(bpy.types.Operator):
    bl_idname = "operator.shoulder_rot_r"
    bl_label = "BlenRig Select shoulder_rot_R"
    bl_description = "shoulder_rot_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_rot_R")
        return {"FINISHED"}

class Operator_Shoulder_R(bpy.types.Operator):
    bl_idname = "operator.shoulder_r"
    bl_label = "BlenRig Select shoulder_R"
    bl_description = "shoulder_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_R")
        return {"FINISHED"}

class Operator_Head_Scale(bpy.types.Operator):
    bl_idname = "operator.head_scale"
    bl_label = "BlenRig Select head_scale"
    bl_description = "head_scale"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_scale")
        return {"FINISHED"}

class Operator_Shoulder_L(bpy.types.Operator):
    bl_idname = "operator.shoulder_l"
    bl_label = "BlenRig Select shoulder_L"
    bl_description = "shoulder_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_L")
        return {"FINISHED"}

class Operator_Shoulder_Rot_L(bpy.types.Operator):
    bl_idname = "operator.shoulder_rot_l"
    bl_label = "BlenRig Select shoulder_rot_L"
    bl_description = "shoulder_rot_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_rot_L")
        return {"FINISHED"}

class Operator_Clavi_Toon_L(bpy.types.Operator):
    bl_idname = "operator.clavi_toon_l"
    bl_label = "BlenRig Select clavi_toon_L"
    bl_description = "clavi_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "clavi_toon_L")
        return {"FINISHED"}

#ARM_R

class Operator_Arm_Toon_R(bpy.types.Operator):
    bl_idname = "operator.arm_toon_r"
    bl_label = "BlenRig Select arm_toon_R"
    bl_description = "arm_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_toon_R")
        return {"FINISHED"}

class Operator_Elbow_Pole_R(bpy.types.Operator):
    bl_idname = "operator.elbow_pole_r"
    bl_label = "BlenRig Select elbow_pole_R"
    bl_description = "elbow_pole_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "elbow_pole_R")
        return {"FINISHED"}

class Operator_Forearm_Toon_R(bpy.types.Operator):
    bl_idname = "operator.forearm_toon_r"
    bl_label = "BlenRig Select forearm_toon_R"
    bl_description = "forearm_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "forearm_toon_R")
        return {"FINISHED"}

class Operator_Arm_Scale_R(bpy.types.Operator):
    bl_idname = "operator.arm_scale_r"
    bl_label = "BlenRig Select arm_scale_R"
    bl_description = "arm_scale_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_scale_R")
        return {"FINISHED"}

class Operator_Arm_FK_R(bpy.types.Operator):
    bl_idname = "operator.arm_fk_r"
    bl_label = "BlenRig Select arm_fk_R"
    bl_description = "arm_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_fk_R")
        return {"FINISHED"}

class Operator_Arm_FK_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.arm_fk_ctrl_r"
    bl_label = "BlenRig Select arm_fk_R"
    bl_description = "arm_fk_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_fk_ctrl_R")
        return {"FINISHED"}

class Operator_Arm_IK_R(bpy.types.Operator):
    bl_idname = "operator.arm_ik_r"
    bl_label = "BlenRig Select arm_ik_R"
    bl_description = "arm_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_ik_R")
        return {"FINISHED"}

class Operator_Elbow_Toon_R(bpy.types.Operator):
    bl_idname = "operator.elbow_toon_r"
    bl_label = "BlenRig Select elbow_toon_R"
    bl_description = "elbow_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "elbow_toon_R")
        return {"FINISHED"}

class Operator_Forearm_FK_R(bpy.types.Operator):
    bl_idname = "operator.forearm_fk_r"
    bl_label = "BlenRig Select forearm_fk_R"
    bl_description = "forearm_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "forearm_fk_R")
        return {"FINISHED"}

class Operator_Forearm_IK_R(bpy.types.Operator):
    bl_idname = "operator.forearm_ik_r"
    bl_label = "BlenRig Select forearm_ik_R"
    bl_description = "forearm_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "forearm_ik_R")
        return {"FINISHED"}

class Operator_Hand_Toon_R(bpy.types.Operator):
    bl_idname = "operator.hand_toon_r"
    bl_label = "BlenRig Select hand_toon_R"
    bl_description = "hand_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_toon_R")
        return {"FINISHED"}

#ARM_L

class Operator_Arm_Toon_L(bpy.types.Operator):
    bl_idname = "operator.arm_toon_l"
    bl_label = "BlenRig Select arm_toon_L"
    bl_description = "arm_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_toon_L")
        return {"FINISHED"}

class Operator_Elbow_Pole_L(bpy.types.Operator):
    bl_idname = "operator.elbow_pole_l"
    bl_label = "BlenRig Select elbow_pole_L"
    bl_description = "elbow_pole_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "elbow_pole_L")
        return {"FINISHED"}

class Operator_Forearm_Toon_L(bpy.types.Operator):
    bl_idname = "operator.forearm_toon_l"
    bl_label = "BlenRig Select forearm_toon_L"
    bl_description = "forearm_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "forearm_toon_L")
        return {"FINISHED"}

class Operator_Arm_Scale_L(bpy.types.Operator):
    bl_idname = "operator.arm_scale_l"
    bl_label = "BlenRig Select arm_scale_L"
    bl_description = "arm_scale_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_scale_L")
        return {"FINISHED"}

class Operator_Arm_FK_L(bpy.types.Operator):
    bl_idname = "operator.arm_fk_l"
    bl_label = "BlenRig Select arm_fk_L"
    bl_description = "arm_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_fk_L")
        return {"FINISHED"}

class Operator_Arm_FK_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.arm_fk_ctrl_l"
    bl_label = "BlenRig Select arm_fk_L"
    bl_description = "arm_fk_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_fk_ctrl_L")
        return {"FINISHED"}

class Operator_Arm_IK_L(bpy.types.Operator):
    bl_idname = "operator.arm_ik_l"
    bl_label = "BlenRig Select arm_ik_L"
    bl_description = "arm_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "arm_ik_L")
        return {"FINISHED"}

class Operator_Elbow_Toon_L(bpy.types.Operator):
    bl_idname = "operator.elbow_toon_l"
    bl_label = "BlenRig Select elbow_toon_L"
    bl_description = "elbow_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "elbow_toon_L")
        return {"FINISHED"}

class Operator_Forearm_FK_L(bpy.types.Operator):
    bl_idname = "operator.forearm_fk_l"
    bl_label = "BlenRig Select forearm_fk_L"
    bl_description = "forearm_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "forearm_fk_L")
        return {"FINISHED"}

class Operator_Forearm_IK_L(bpy.types.Operator):
    bl_idname = "operator.forearm_ik_l"
    bl_label = "BlenRig Select forearm_ik_L"
    bl_description = "forearm_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "forearm_ik_L")
        return {"FINISHED"}

class Operator_Hand_Toon_L(bpy.types.Operator):
    bl_idname = "operator.hand_toon_l"
    bl_label = "BlenRig Select hand_toon_L"
    bl_description = "hand_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_toon_L")
        return {"FINISHED"}

#SPINE

class Operator_Torso_Ctrl_Legacy(bpy.types.Operator):
    bl_idname = "operator.torso_ctrl_legacy"
    bl_label = "BlenRig Select torso_ctrl"
    bl_description = "torso_ik_ctrl / torso_fk_ctrl / torso_inv_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)
        if ('torso_ik_ctrl' and 'torso_fk_ctrl' and 'torso_inv_ctrl' in armobj.pose.bones):
            #Target Bone
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["torso_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["torso_fk_ctrl"]
            else:
                Bone = armobj.pose.bones["torso_inv_ctrl"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Spine_3_Legacy(bpy.types.Operator):
    bl_idname = "operator.spine_3_legacy"
    bl_label = "BlenRig Select spine_3"
    bl_description = "spine_3_ik_ctrl / spine_3_fk / spine_3_inv"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)
        if ('spine_4_ik_ctrl' and 'spine_3_fk' and 'spine_3_inv' in armobj.pose.bones):
            #Target Bone
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_3_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_3_fk"]
            else:
                Bone = armobj.pose.bones["spine_3_inv"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Spine_2_Legacy(bpy.types.Operator):
    bl_idname = "operator.spine_2_legacy"
    bl_label = "BlenRig Select spine_2"
    bl_description = "spine_2_ik_ctrl / spine_2_fk / spine_2_inv"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)
        if ('spine_3_ik_ctrl' and 'spine_2_fk' and 'spine_2_inv' in armobj.pose.bones):
            #Target Bone
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_2_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_2_fk"]
            else:
                Bone = armobj.pose.bones["spine_2_inv"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Spine_1_Legacy(bpy.types.Operator):
    bl_idname = "operator.spine_1_legacy"
    bl_label = "BlenRig Select spine_1"
    bl_description = "spine_1_ik_ctrl / spine_1_fk / spine_1_inv"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)
        if ('spine_2_ik_ctrl' and 'spine_1_fk' and 'spine_1_inv' in armobj.pose.bones):
            #Target Bone
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_1_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_1_fk"]
            else:
                Bone = armobj.pose.bones["spine_1_inv"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Spine_1(bpy.types.Operator):
    bl_idname = "operator.spine_1"
    bl_label = "BlenRig Select spine_1"
    bl_description = "spine_1_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_1_fk")
        return {"FINISHED"}

class Operator_Spine_2(bpy.types.Operator):
    bl_idname = "operator.spine_2"
    bl_label = "BlenRig Select spine_2"
    bl_description = "spine_2_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_2_fk")
        return {"FINISHED"}

class Operator_Spine_3(bpy.types.Operator):
    bl_idname = "operator.spine_3"
    bl_label = "BlenRig Select spine_3"
    bl_description = "spine_3_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_3_fk")
        return {"FINISHED"}

class Operator_Torso_Ctrl(bpy.types.Operator):
    bl_idname = "operator.torso_ctrl"
    bl_label = "BlenRig Select torso_fk_ctrl"
    bl_description = "torso_fk_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "torso_fk_ctrl")
        return {"FINISHED"}

class Operator_Spine_2_FK_Inv(bpy.types.Operator):
    bl_idname = "operator.spine_2_fk_inv"
    bl_label = "BlenRig Select spine_2_fk_inv"
    bl_description = "spine_2_fk_inv"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_2_fk_inv")
        return {"FINISHED"}

class Operator_Spine_3_FK_Inv(bpy.types.Operator):
    bl_idname = "operator.spine_3_fk_inv"
    bl_label = "BlenRig Select spine_3_fk_inv"
    bl_description = "spine_3_fk_inv"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_3_fk_inv")
        return {"FINISHED"}

class Operator_Torso_FK_Ctrl_Inv(bpy.types.Operator):
    bl_idname = "operator.torso_fk_ctrl_inv"
    bl_label = "BlenRig Select torso_fk_ctrl_inv"
    bl_description = "torso_fk_ctrl_inv"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "torso_fk_ctrl_inv")
        return {"FINISHED"}

class Operator_Spine_4_Toon(bpy.types.Operator):
    bl_idname = "operator.spine_4_toon"
    bl_label = "BlenRig Select spine_4_toon"
    bl_description = "spine_4_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_4_toon")
        return {"FINISHED"}

class Operator_Spine_3_Toon(bpy.types.Operator):
    bl_idname = "operator.spine_3_toon"
    bl_label = "BlenRig Select spine_3_toon"
    bl_description = "spine_3_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_3_toon")
        return {"FINISHED"}

class Operator_Spine_2_Toon(bpy.types.Operator):
    bl_idname = "operator.spine_2_toon"
    bl_label = "BlenRig Select spine_2_toon"
    bl_description = "spine_2_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_2_toon")
        return {"FINISHED"}

class Operator_Spine_1_Toon(bpy.types.Operator):
    bl_idname = "operator.spine_1_toon"
    bl_label = "BlenRig Select spine_1_toon"
    bl_description = "spine_1_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_1_toon")
        return {"FINISHED"}

class Operator_Spine_3_Inv_Ctrl(bpy.types.Operator):
    bl_idname = "operator.spine_3_inv_ctrl"
    bl_label = "BlenRig Select spine_3_inv_ctrl"
    bl_description = "spine_3_inv_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "spine_3_inv_ctrl")
        return {"FINISHED"}

class Operator_Pelvis_Toon(bpy.types.Operator):
    bl_idname = "operator.pelvis_toon"
    bl_label = "BlenRig Select pelvis_toon"
    bl_description = "pelvis_toon"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_toon")
        return {"FINISHED"}

class Operator_Pelvis_Ctrl(bpy.types.Operator):
    bl_idname = "operator.pelvis_ctrl"
    bl_label = "BlenRig Select pelvis_ctrl"
    bl_description = "pelvis_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_ctrl")
        return {"FINISHED"}

class Operator_Pelvis_Ctrl_Legacy(bpy.types.Operator):
    bl_idname = "operator.pelvis_ctrl_legacy"
    bl_label = "BlenRig Select pelvis_ctrl"
    bl_description = "pelvis_ctrl / pelvis_inv"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)
        if ('pelvis_ctrl' and 'pelvis_inv' in armobj.pose.bones):
            #Target Bone
            if prop_inv == 0:
                Bone = armobj.pose.bones["pelvis_ctrl"]
            else:
                Bone = armobj.pose.bones["pelvis_inv"]

            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Master_Torso_Pivot_Point(bpy.types.Operator):
    bl_idname = "operator.master_torso_pivot_point"
    bl_label = "BlenRig Select master_torso_pivot_point"
    bl_description = "master_torso_pivot_point"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "master_torso_pivot_point")
        return {"FINISHED"}

class Operator_Master_Torso(bpy.types.Operator):
    bl_idname = "operator.master_torso"
    bl_label = "BlenRig Select master_torso"
    bl_description = "master_torso"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "master_torso")
        return {"FINISHED"}

#HAND_R

class Operator_Hand_Roll_R(bpy.types.Operator):
    bl_idname = "operator.hand_roll_r"
    bl_label = "BlenRig Select hand_roll_R"
    bl_description = "palm_bend_ik_ctrl_R / palm_bend_fk_ctrl_R"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_R'].ik_arm_R)
        prop_hinge = int(bpy.context.active_object.pose.bones['properties_arm_R'].hinge_hand_R)
        if ('palm_bend_ik_ctrl_R' and 'palm_bend_fk_ctrl_R' in armobj.pose.bones):
            #Target Bone
            if prop == 1 or prop_hinge == 0:
                Bone = armobj.pose.bones["palm_bend_fk_ctrl_R"]
            else:
                Bone = armobj.pose.bones["palm_bend_ik_ctrl_R"]

            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Hand_IK_Pivot_Point_R(bpy.types.Operator):
    bl_idname = "operator.hand_ik_pivot_point_r"
    bl_label = "BlenRig Select hand_ik_pivot_point_R"
    bl_description = "hand_ik_pivot_point_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_pivot_point_R")
        return {"FINISHED"}

class Operator_Hand_IK_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.hand_ik_ctrl_r"
    bl_label = "BlenRig Select hand_ik_ctrl_R"
    bl_description = "hand_ik_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_ctrl_R")
        return {"FINISHED"}

class Operator_Hand_FK_R(bpy.types.Operator):
    bl_idname = "operator.hand_fk_r"
    bl_label = "BlenRig Select hand_fk_R"
    bl_description = "hand_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_fk_R")
        return {"FINISHED"}

class Operator_Fing_Spread_R(bpy.types.Operator):
    bl_idname = "operator.fing_spread_r"
    bl_label = "BlenRig Select fing_spread_R"
    bl_description = "fing_spread_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_spread_R")
        return {"FINISHED"}

class Operator_Fing_Lit_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.fing_lit_ctrl_r"
    bl_label = "BlenRig Select fing_lit_ctrl_R"
    bl_description = "fing_lit_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ctrl_R")
        return {"FINISHED"}

class Operator_Fing_Lit_2_R(bpy.types.Operator):
    bl_idname = "operator.fing_lit_2_r"
    bl_label = "BlenRig Select fing_lit_2_R"
    bl_description = "fing_lit_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_2_R")
        return {"FINISHED"}

class Operator_Fing_Lit_3_R(bpy.types.Operator):
    bl_idname = "operator.fing_lit_3_r"
    bl_label = "BlenRig Select fing_lit_3_R"
    bl_description = "fing_lit_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_3_R")
        return {"FINISHED"}

class Operator_Fing_Lit_4_R(bpy.types.Operator):
    bl_idname = "operator.fing_lit_4_r"
    bl_label = "BlenRig Select fing_lit_4_R"
    bl_description = "fing_lit_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_4_R")
        return {"FINISHED"}

class Operator_Fing_Ring_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.fing_ring_ctrl_r"
    bl_label = "BlenRig Select fing_ring_ctrl_R"
    bl_description = "fing_ring_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ctrl_R")
        return {"FINISHED"}

class Operator_Fing_Ring_2_R(bpy.types.Operator):
    bl_idname = "operator.fing_ring_2_r"
    bl_label = "BlenRig Select fing_ring_2_R"
    bl_description = "fing_ring_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_2_R")
        return {"FINISHED"}

class Operator_Fing_Ring_3_R(bpy.types.Operator):
    bl_idname = "operator.fing_ring_3_r"
    bl_label = "BlenRig Select fing_ring_3_R"
    bl_description = "fing_ring_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_3_R")
        return {"FINISHED"}

class Operator_Fing_Ring_4_R(bpy.types.Operator):
    bl_idname = "operator.fing_ring_4_r"
    bl_label = "BlenRig Select fing_ring_4_R"
    bl_description = "fing_ring_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_4_R")
        return {"FINISHED"}

class Operator_Fing_Mid_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.fing_mid_ctrl_r"
    bl_label = "BlenRig Select fing_mid_ctrl_R"
    bl_description = "fing_mid_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ctrl_R")
        return {"FINISHED"}

class Operator_Fing_Mid_2_R(bpy.types.Operator):
    bl_idname = "operator.fing_mid_2_r"
    bl_label = "BlenRig Select fing_mid_2_R"
    bl_description = "fing_mid_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_2_R")
        return {"FINISHED"}

class Operator_Fing_Mid_3_R(bpy.types.Operator):
    bl_idname = "operator.fing_mid_3_r"
    bl_label = "BlenRig Select fing_mid_3_R"
    bl_description = "fing_mid_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_3_R")
        return {"FINISHED"}

class Operator_Fing_Mid_4_R(bpy.types.Operator):
    bl_idname = "operator.fing_mid_4_r"
    bl_label = "BlenRig Select fing_mid_4_R"
    bl_description = "fing_mid_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_4_R")
        return {"FINISHED"}

class Operator_Fing_Ind_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.fing_ind_ctrl_r"
    bl_label = "BlenRig Select fing_ind_ctrl_R"
    bl_description = "fing_ind_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ctrl_R")
        return {"FINISHED"}

class Operator_Fing_Ind_2_R(bpy.types.Operator):
    bl_idname = "operator.fing_ind_2_r"
    bl_label = "BlenRig Select fing_ind_2_R"
    bl_description = "fing_ind_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_2_R")
        return {"FINISHED"}

class Operator_Fing_Ind_3_R(bpy.types.Operator):
    bl_idname = "operator.fing_ind_3_r"
    bl_label = "BlenRig Select fing_ind_3_R"
    bl_description = "fing_ind_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_3_R")
        return {"FINISHED"}

class Operator_Fing_Ind_4_R(bpy.types.Operator):
    bl_idname = "operator.fing_ind_4_r"
    bl_label = "BlenRig Select fing_ind_4_R"
    bl_description = "fing_ind_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_4_R")
        return {"FINISHED"}

class Operator_Fing_Thumb_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_ctrl_r"
    bl_label = "BlenRig Select fing_thumb_ctrl_R"
    bl_description = "fing_thumb_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ctrl_R")
        return {"FINISHED"}

class Operator_Fing_Thumb_1_R(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_1_r"
    bl_label = "BlenRig Select fing_thumb_1_R"
    bl_description = "fing_thumb_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_1_R")
        return {"FINISHED"}

class Operator_Fing_Thumb_2_R(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_2_r"
    bl_label = "BlenRig Select fing_thumb_2_R"
    bl_description = "fing_thumb_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_2_R")
        return {"FINISHED"}

class Operator_Fing_Thumb_3_R(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_3_r"
    bl_label = "BlenRig Select fing_thumb_3_R"
    bl_description = "fing_thumb_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_3_R")
        return {"FINISHED"}

class Operator_Fing_Lit_IK_R(bpy.types.Operator):
    bl_idname = "operator.fing_lit_ik_r"
    bl_label = "BlenRig Select fing_lit_ik_R"
    bl_description = "fing_lit_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ik_R")
        return {"FINISHED"}

class Operator_Fing_Ring_IK_R(bpy.types.Operator):
    bl_idname = "operator.fing_ring_ik_r"
    bl_label = "BlenRig Select fing_ring_ik_R"
    bl_description = "fing_ring_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ik_R")
        return {"FINISHED"}

class Operator_Fing_Mid_IK_R(bpy.types.Operator):
    bl_idname = "operator.fing_mid_ik_r"
    bl_label = "BlenRig Select fing_mid_ik_R"
    bl_description = "fing_mid_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ik_R")
        return {"FINISHED"}

class Operator_Fing_Ind_IK_R(bpy.types.Operator):
    bl_idname = "operator.fing_ind_ik_r"
    bl_label = "BlenRig Select fing_ind_ik_R"
    bl_description = "fing_ind_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ik_R")
        return {"FINISHED"}

class Operator_Fing_Thumb_IK_R(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_ik_r"
    bl_label = "BlenRig Select fing_thumb_ik_R"
    bl_description = "fing_thumb_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ik_R")
        return {"FINISHED"}

class Operator_Hand_Close_R(bpy.types.Operator):
    bl_idname = "operator.hand_close_r"
    bl_label = "BlenRig Select hand_close_R"
    bl_description = "hand_close_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_close_R")
        return {"FINISHED"}

#HAND_L

class Operator_Hand_Roll_L(bpy.types.Operator):
    bl_idname = "operator.hand_roll_l"
    bl_label = "BlenRig Select hand_roll_L"
    bl_description = "palm_bend_ik_ctrl_L / palm_bend_fk_ctrl_L"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_L'].ik_arm_L)
        prop_hinge = int(bpy.context.active_object.pose.bones['properties_arm_L'].hinge_hand_L)
        if ('palm_bend_ik_ctrl_L' and 'palm_bend_fk_ctrl_L' in armobj.pose.bones):
            #Target Bone
            if prop == 1 or prop_hinge == 0:
                Bone = armobj.pose.bones["palm_bend_fk_ctrl_L"]
            else:
                Bone = armobj.pose.bones["palm_bend_ik_ctrl_L"]

            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Hand_IK_Pivot_Point_L(bpy.types.Operator):
    bl_idname = "operator.hand_ik_pivot_point_l"
    bl_label = "BlenRig Select hand_ik_pivot_point_L"
    bl_description = "hand_ik_pivot_point_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_pivot_point_L")
        return {"FINISHED"}

class Operator_Hand_IK_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.hand_ik_ctrl_l"
    bl_label = "BlenRig Select hand_ik_ctrl_L"
    bl_description = "hand_ik_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_ctrl_L")
        return {"FINISHED"}

class Operator_Hand_FK_L(bpy.types.Operator):
    bl_idname = "operator.hand_fk_l"
    bl_label = "BlenRig Select hand_fk_L"
    bl_description = "hand_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_fk_L")
        return {"FINISHED"}

class Operator_Fing_Spread_L(bpy.types.Operator):
    bl_idname = "operator.fing_spread_l"
    bl_label = "BlenRig Select fing_spread_L"
    bl_description = "fing_spread_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_spread_L")
        return {"FINISHED"}

class Operator_Fing_Lit_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.fing_lit_ctrl_l"
    bl_label = "BlenRig Select fing_lit_ctrl_L"
    bl_description = "fing_lit_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ctrl_L")
        return {"FINISHED"}

class Operator_Fing_Lit_2_L(bpy.types.Operator):
    bl_idname = "operator.fing_lit_2_l"
    bl_label = "BlenRig Select fing_lit_2_L"
    bl_description = "fing_lit_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_2_L")
        return {"FINISHED"}

class Operator_Fing_Lit_3_L(bpy.types.Operator):
    bl_idname = "operator.fing_lit_3_l"
    bl_label = "BlenRig Select fing_lit_3_L"
    bl_description = "fing_lit_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_3_L")
        return {"FINISHED"}

class Operator_Fing_Lit_4_L(bpy.types.Operator):
    bl_idname = "operator.fing_lit_4_l"
    bl_label = "BlenRig Select fing_lit_4_L"
    bl_description = "fing_lit_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_4_L")
        return {"FINISHED"}

class Operator_Fing_Ring_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.fing_ring_ctrl_l"
    bl_label = "BlenRig Select fing_ring_ctrl_L"
    bl_description = "fing_ring_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ctrl_L")
        return {"FINISHED"}

class Operator_Fing_Ring_2_L(bpy.types.Operator):
    bl_idname = "operator.fing_ring_2_l"
    bl_label = "BlenRig Select fing_ring_2_L"
    bl_description = "fing_ring_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_2_L")
        return {"FINISHED"}

class Operator_Fing_Ring_3_L(bpy.types.Operator):
    bl_idname = "operator.fing_ring_3_l"
    bl_label = "BlenRig Select fing_ring_3_L"
    bl_description = "fing_ring_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_3_L")
        return {"FINISHED"}

class Operator_Fing_Ring_4_L(bpy.types.Operator):
    bl_idname = "operator.fing_ring_4_l"
    bl_label = "BlenRig Select fing_ring_4_L"
    bl_description = "fing_ring_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_4_L")
        return {"FINISHED"}

class Operator_Fing_Mid_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.fing_mid_ctrl_l"
    bl_label = "BlenRig Select fing_mid_ctrl_L"
    bl_description = "fing_mid_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ctrl_L")
        return {"FINISHED"}

class Operator_Fing_Mid_2_L(bpy.types.Operator):
    bl_idname = "operator.fing_mid_2_l"
    bl_label = "BlenRig Select fing_mid_2_L"
    bl_description = "fing_mid_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_2_L")
        return {"FINISHED"}

class Operator_Fing_Mid_3_L(bpy.types.Operator):
    bl_idname = "operator.fing_mid_3_l"
    bl_label = "BlenRig Select fing_mid_3_L"
    bl_description = "fing_mid_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_3_L")
        return {"FINISHED"}

class Operator_Fing_Mid_4_L(bpy.types.Operator):
    bl_idname = "operator.fing_mid_4_l"
    bl_label = "BlenRig Select fing_mid_4_L"
    bl_description = "fing_mid_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_4_L")
        return {"FINISHED"}

class Operator_Fing_Ind_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.fing_ind_ctrl_l"
    bl_label = "BlenRig Select fing_ind_ctrl_L"
    bl_description = "fing_ind_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ctrl_L")
        return {"FINISHED"}

class Operator_Fing_Ind_2_L(bpy.types.Operator):
    bl_idname = "operator.fing_ind_2_l"
    bl_label = "BlenRig Select fing_ind_2_L"
    bl_description = "fing_ind_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_2_L")
        return {"FINISHED"}

class Operator_Fing_Ind_3_L(bpy.types.Operator):
    bl_idname = "operator.fing_ind_3_l"
    bl_label = "BlenRig Select fing_ind_3_L"
    bl_description = "fing_ind_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_3_L")
        return {"FINISHED"}

class Operator_Fing_Ind_4_L(bpy.types.Operator):
    bl_idname = "operator.fing_ind_4_l"
    bl_label = "BlenRig Select fing_ind_4_L"
    bl_description = "fing_ind_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_4_L")
        return {"FINISHED"}

class Operator_Fing_Thumb_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_ctrl_l"
    bl_label = "BlenRig Select fing_thumb_ctrl_L"
    bl_description = "fing_thumb_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ctrl_L")
        return {"FINISHED"}

class Operator_Fing_Thumb_1_L(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_1_l"
    bl_label = "BlenRig Select fing_thumb_1_L"
    bl_description = "fing_thumb_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_1_L")
        return {"FINISHED"}

class Operator_Fing_Thumb_2_L(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_2_l"
    bl_label = "BlenRig Select fing_thumb_2_L"
    bl_description = "fing_thumb_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_2_L")
        return {"FINISHED"}

class Operator_Fing_Thumb_3_L(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_3_l"
    bl_label = "BlenRig Select fing_thumb_3_L"
    bl_description = "fing_thumb_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_3_L")
        return {"FINISHED"}

class Operator_Fing_Lit_IK_L(bpy.types.Operator):
    bl_idname = "operator.fing_lit_ik_l"
    bl_label = "BlenRig Select fing_lit_ik_L"
    bl_description = "fing_lit_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ik_L")
        return {"FINISHED"}

class Operator_Fing_Ring_IK_L(bpy.types.Operator):
    bl_idname = "operator.fing_ring_ik_l"
    bl_label = "BlenRig Select fing_ring_ik_L"
    bl_description = "fing_ring_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ik_L")
        return {"FINISHED"}

class Operator_Fing_Mid_IK_L(bpy.types.Operator):
    bl_idname = "operator.fing_mid_ik_l"
    bl_label = "BlenRig Select fing_mid_ik_L"
    bl_description = "fing_mid_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ik_L")
        return {"FINISHED"}

class Operator_Fing_Ind_IK_L(bpy.types.Operator):
    bl_idname = "operator.fing_ind_ik_l"
    bl_label = "BlenRig Select fing_ind_ik_L"
    bl_description = "fing_ind_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ik_L")
        return {"FINISHED"}

class Operator_Fing_Thumb_IK_L(bpy.types.Operator):
    bl_idname = "operator.fing_thumb_ik_l"
    bl_label = "BlenRig Select fing_thumb_ik_L"
    bl_description = "fing_thumb_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ik_L")
        return {"FINISHED"}

class Operator_Hand_Close_L(bpy.types.Operator):
    bl_idname = "operator.hand_close_l"
    bl_label = "BlenRig Select hand_close_L"
    bl_description = "hand_close_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_close_L")
        return {"FINISHED"}

#LEG_R

class Operator_Thigh_Toon_R(bpy.types.Operator):
    bl_idname = "operator.thigh_toon_r"
    bl_label = "BlenRig Select thigh_toon_R"
    bl_description = "thigh_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_toon_R")
        return {"FINISHED"}

class Operator_Knee_Pole_R(bpy.types.Operator):
    bl_idname = "operator.knee_pole_r"
    bl_label = "BlenRig Select knee_pole_R"
    bl_description = "knee_pole_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "knee_pole_R")
        return {"FINISHED"}

class Operator_Shin_Toon_R(bpy.types.Operator):
    bl_idname = "operator.shin_toon_r"
    bl_label = "BlenRig Select shin_toon_R"
    bl_description = "shin_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shin_toon_R")
        return {"FINISHED"}

class Operator_Pelvis_Toon_R(bpy.types.Operator):
    bl_idname = "operator.pelvis_toon_r"
    bl_label = "BlenRig Select pelvis_toon_R"
    bl_description = "pelvis_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_toon_R")
        return {"FINISHED"}

class Operator_Leg_Scale_R(bpy.types.Operator):
    bl_idname = "operator.leg_scale_r"
    bl_label = "BlenRig Select leg_scale_R"
    bl_description = "leg_scale_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "leg_scale_R")
        return {"FINISHED"}

class Operator_Thigh_FK_R(bpy.types.Operator):
    bl_idname = "operator.thigh_fk_r"
    bl_label = "BlenRig Select thigh_fk_R"
    bl_description = "thigh_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_fk_R")
        return {"FINISHED"}

class Operator_Thigh_FK_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.thigh_fk_ctrl_r"
    bl_label = "BlenRig Select thigh_fk_ctrl_R"
    bl_description = "thigh_fk_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_fk_ctrl_R")
        return {"FINISHED"}

class Operator_Thigh_IK_R(bpy.types.Operator):
    bl_idname = "operator.thigh_ik_r"
    bl_label = "BlenRig Select thigh_ik_R"
    bl_description = "thigh_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_ik_R")
        return {"FINISHED"}

class Operator_Knee_Toon_R(bpy.types.Operator):
    bl_idname = "operator.knee_toon_r"
    bl_label = "BlenRig Select knee_toon_R"
    bl_description = "knee_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "knee_toon_R")
        return {"FINISHED"}

class Operator_Shin_FK_R(bpy.types.Operator):
    bl_idname = "operator.shin_fk_r"
    bl_label = "BlenRig Select shin_fk_R"
    bl_description = "shin_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shin_fk_R")
        return {"FINISHED"}

class Operator_Shin_IK_R(bpy.types.Operator):
    bl_idname = "operator.shin_ik_r"
    bl_label = "BlenRig Select shin_ik_R"
    bl_description = "shin_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shin_ik_R")
        return {"FINISHED"}

class Operator_Foot_Toon_R(bpy.types.Operator):
    bl_idname = "operator.foot_toon_r"
    bl_label = "BlenRig Select foot_toon_R"
    bl_description = "foot_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "foot_toon_R")
        return {"FINISHED"}

#LEG_L

class Operator_Thigh_Toon_L(bpy.types.Operator):
    bl_idname = "operator.thigh_toon_l"
    bl_label = "BlenRig Select thigh_toon_L"
    bl_description = "thigh_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_toon_L")
        return {"FINISHED"}

class Operator_Knee_Pole_L(bpy.types.Operator):
    bl_idname = "operator.knee_pole_l"
    bl_label = "BlenRig Select knee_pole_L"
    bl_description = "knee_pole_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "knee_pole_L")
        return {"FINISHED"}

class Operator_Shin_Toon_L(bpy.types.Operator):
    bl_idname = "operator.shin_toon_l"
    bl_label = "BlenRig Select shin_toon_L"
    bl_description = "shin_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shin_toon_L")
        return {"FINISHED"}

class Operator_Pelvis_Toon_L(bpy.types.Operator):
    bl_idname = "operator.pelvis_toon_l"
    bl_label = "BlenRig Select pelvis_toon_L"
    bl_description = "pelvis_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_toon_L")
        return {"FINISHED"}

class Operator_Leg_Scale_L(bpy.types.Operator):
    bl_idname = "operator.leg_scale_l"
    bl_label = "BlenRig Select leg_scale_L"
    bl_description = "leg_scale_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "leg_scale_L")
        return {"FINISHED"}

class Operator_Thigh_FK_L(bpy.types.Operator):
    bl_idname = "operator.thigh_fk_l"
    bl_label = "BlenRig Select thigh_fk_L"
    bl_description = "thigh_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_fk_L")
        return {"FINISHED"}

class Operator_Thigh_FK_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.thigh_fk_ctrl_l"
    bl_label = "BlenRig Select thigh_fk_ctrl_L"
    bl_description = "thigh_fk_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_fk_ctrl_L")
        return {"FINISHED"}

class Operator_Thigh_IK_L(bpy.types.Operator):
    bl_idname = "operator.thigh_ik_l"
    bl_label = "BlenRig Select thigh_ik_L"
    bl_description = "thigh_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "thigh_ik_L")
        return {"FINISHED"}

class Operator_Knee_Toon_L(bpy.types.Operator):
    bl_idname = "operator.knee_toon_l"
    bl_label = "BlenRig Select knee_toon_L"
    bl_description = "knee_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "knee_toon_L")
        return {"FINISHED"}

class Operator_Shin_FK_L(bpy.types.Operator):
    bl_idname = "operator.shin_fk_l"
    bl_label = "BlenRig Select shin_fk_L"
    bl_description = "shin_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shin_fk_L")
        return {"FINISHED"}

class Operator_Shin_IK_L(bpy.types.Operator):
    bl_idname = "operator.shin_ik_l"
    bl_label = "BlenRig Select shin_ik_L"
    bl_description = "shin_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "shin_ik_L")
        return {"FINISHED"}

class Operator_Foot_Toon_L(bpy.types.Operator):
    bl_idname = "operator.foot_toon_l"
    bl_label = "BlenRig Select foot_toon_L"
    bl_description = "foot_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "foot_toon_L")
        return {"FINISHED"}

#FOOT_R

class Operator_Toe_2_FK_R(bpy.types.Operator):
    bl_idname = "operator.toe_2_fk_r"
    bl_label = "BlenRig Select toe_2_fk_R"
    bl_description = "toe_2_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_2_fk_R")
        return {"FINISHED"}

class Operator_Toes_IK_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.toes_ik_ctrl_r"
    bl_label = "BlenRig Select toes_ik_ctrl_R"
    bl_description = "toes_ik_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toes_ik_ctrl_R")
        return {"FINISHED"}

class Operator_Toe_Roll_2_R(bpy.types.Operator):
    bl_idname = "operator.toe_roll_2_r"
    bl_label = "BlenRig Select toe_roll_2_R"
    bl_description = "toe_roll_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_2_R")
        return {"FINISHED"}

class Operator_Toe_1_FK_R(bpy.types.Operator):
    bl_idname = "operator.toe_1_fk_r"
    bl_label = "BlenRig Select toe_1_fk_R"
    bl_description = "toe_1_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_1_fk_R")
        return {"FINISHED"}

class Operator_Toes_IK_Ctrl_Mid_R(bpy.types.Operator):
    bl_idname = "operator.toes_ik_ctrl_mid_r"
    bl_label = "BlenRig Select toes_ik_ctrl_mid_R"
    bl_description = "toes_ik_ctrl_mid_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toes_ik_ctrl_mid_R")
        return {"FINISHED"}

class Operator_Toe_Roll_1_R(bpy.types.Operator):
    bl_idname = "operator.toe_roll_1_r"
    bl_label = "BlenRig Select toe_roll_1_R"
    bl_description = "toe_roll_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_1_R")
        return {"FINISHED"}

class Operator_Foot_R(bpy.types.Operator):
    bl_idname = "operator.foot_r"
    bl_label = "BlenRig Select foot_R"
    bl_description = "foot_ik_ctrl_R / foot_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_leg_R'].ik_leg_R)
        if ('foot_ik_ctrl_R' and 'foot_fk_R' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["foot_ik_ctrl_R"]
            else:
                Bone = armobj.pose.bones["foot_fk_R"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Foot_Roll_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.foot_roll_ctrl_r"
    bl_label = "BlenRig Select foot_roll_ctrl_R"
    bl_description = "foot_roll_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "foot_roll_ctrl_R")
        return {"FINISHED"}

class Operator_Toes_Spread_R(bpy.types.Operator):
    bl_idname = "operator.toes_spread_r"
    bl_label = "BlenRig Select toes_spread_R"
    bl_description = "toes_spread_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toes_spread_R")
        return {"FINISHED"}

class Operator_Toe_Lit_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.toe_lit_ctrl_r"
    bl_label = "BlenRig Select toe_lit_ctrl_R"
    bl_description = "toe_lit_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_ctrl_R")
        return {"FINISHED"}

class Operator_Toe_Lit_2_R(bpy.types.Operator):
    bl_idname = "operator.toe_lit_2_r"
    bl_label = "BlenRig Select toe_lit_2_R"
    bl_description = "toe_lit_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_2_R")
        return {"FINISHED"}

class Operator_Toe_Lit_3_R(bpy.types.Operator):
    bl_idname = "operator.toe_lit_3_r"
    bl_label = "BlenRig Select toe_lit_3_R"
    bl_description = "toe_lit_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_3_R")
        return {"FINISHED"}

class Operator_Toe_Lit_IK_R(bpy.types.Operator):
    bl_idname = "operator.toe_lit_ik_r"
    bl_label = "BlenRig Select toe_lit_ik_R"
    bl_description = "toe_lit_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_ik_R")
        return {"FINISHED"}

class Operator_Toe_Fourth_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_ctrl_r"
    bl_label = "BlenRig Select toe_fourth_ctrl_R"
    bl_description = "toe_fourth_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_ctrl_R")
        return {"FINISHED"}

class Operator_Toe_Fourth_2_R(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_2_r"
    bl_label = "BlenRig Select toe_fourth_2_R"
    bl_description = "toe_fourth_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_2_R")
        return {"FINISHED"}

class Operator_Toe_Fourth_3_R(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_3_r"
    bl_label = "BlenRig Select toe_fourth_3_R"
    bl_description = "toe_fourth_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_3_R")
        return {"FINISHED"}

class Operator_Toe_Fourth_4_R(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_4_r"
    bl_label = "BlenRig Select toe_fourth_4_R"
    bl_description = "toe_fourth_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_4_R")
        return {"FINISHED"}

class Operator_Toe_Fourth_IK_R(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_ik_r"
    bl_label = "BlenRig Select toe_fourth_ik_R"
    bl_description = "toe_fourth_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_ik_R")
        return {"FINISHED"}

class Operator_Toe_Mid_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.toe_mid_ctrl_r"
    bl_label = "BlenRig Select toe_mid_ctrl_R"
    bl_description = "toe_mid_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_ctrl_R")
        return {"FINISHED"}

class Operator_Toe_Mid_2_R(bpy.types.Operator):
    bl_idname = "operator.toe_mid_2_r"
    bl_label = "BlenRig Select toe_mid_2_R"
    bl_description = "toe_mid_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_2_R")
        return {"FINISHED"}

class Operator_Toe_Mid_3_R(bpy.types.Operator):
    bl_idname = "operator.toe_mid_3_r"
    bl_label = "BlenRig Select toe_mid_3_R"
    bl_description = "toe_mid_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_3_R")
        return {"FINISHED"}

class Operator_Toe_Mid_4_R(bpy.types.Operator):
    bl_idname = "operator.toe_mid_4_r"
    bl_label = "BlenRig Select toe_mid_4_R"
    bl_description = "toe_mid_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_4_R")
        return {"FINISHED"}

class Operator_Toe_Mid_IK_R(bpy.types.Operator):
    bl_idname = "operator.toe_mid_ik_r"
    bl_label = "BlenRig Select toe_mid_ik_R"
    bl_description = "toe_mid_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_ik_R")
        return {"FINISHED"}

class Operator_Toe_Ind_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.toe_ind_ctrl_r"
    bl_label = "BlenRig Select toe_ind_ctrl_R"
    bl_description = "toe_ind_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_ctrl_R")
        return {"FINISHED"}

class Operator_Toe_Ind_2_R(bpy.types.Operator):
    bl_idname = "operator.toe_ind_2_r"
    bl_label = "BlenRig Select toe_ind_2_R"
    bl_description = "toe_ind_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_2_R")
        return {"FINISHED"}

class Operator_Toe_Ind_3_R(bpy.types.Operator):
    bl_idname = "operator.toe_ind_3_r"
    bl_label = "BlenRig Select toe_ind_3_R"
    bl_description = "toe_ind_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_3_R")
        return {"FINISHED"}

class Operator_Toe_Ind_4_R(bpy.types.Operator):
    bl_idname = "operator.toe_ind_4_r"
    bl_label = "BlenRig Select toe_ind_4_R"
    bl_description = "toe_ind_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_4_R")
        return {"FINISHED"}

class Operator_Toe_Ind_IK_R(bpy.types.Operator):
    bl_idname = "operator.toe_ind_ik_r"
    bl_label = "BlenRig Select toe_ind_ik_R"
    bl_description = "toe_ind_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_ik_R")
        return {"FINISHED"}

class Operator_Toe_Big_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.toe_big_ctrl_r"
    bl_label = "BlenRig Select toe_big_ctrl_R"
    bl_description = "toe_big_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_ctrl_R")
        return {"FINISHED"}

class Operator_Toe_Big_2_R(bpy.types.Operator):
    bl_idname = "operator.toe_big_2_r"
    bl_label = "BlenRig Select toe_big_2_R"
    bl_description = "toe_big_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_2_R")
        return {"FINISHED"}

class Operator_Toe_Big_3_R(bpy.types.Operator):
    bl_idname = "operator.toe_big_3_r"
    bl_label = "BlenRig Select toe_big_3_R"
    bl_description = "toe_big_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_3_R")
        return {"FINISHED"}

class Operator_Toe_Big_IK_R(bpy.types.Operator):
    bl_idname = "operator.toe_big_ik_r"
    bl_label = "BlenRig Select toe_big_ik_R"
    bl_description = "toe_big_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_ik_R")
        return {"FINISHED"}

class Operator_Sole_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.sole_ctrl_r"
    bl_label = "BlenRig Select sole_ctrl_R"
    bl_description = "sole_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "sole_ctrl_R")
        return {"FINISHED"}

class Operator_Sole_Pivot_Point_R(bpy.types.Operator):
    bl_idname = "operator.sole_pivot_point_r"
    bl_label = "BlenRig Select sole_pivot_point_R"
    bl_description = "sole_pivot_point_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "sole_pivot_point_R")
        return {"FINISHED"}

#FOOT_L

class Operator_Toe_2_FK_L(bpy.types.Operator):
    bl_idname = "operator.toe_2_fk_l"
    bl_label = "BlenRig Select toe_2_fk_L"
    bl_description = "toe_2_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_2_fk_L")
        return {"FINISHED"}

class Operator_Toes_IK_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.toes_ik_ctrl_l"
    bl_label = "BlenRig Select toes_ik_ctrl_L"
    bl_description = "toes_ik_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toes_ik_ctrl_L")
        return {"FINISHED"}

class Operator_Toe_Roll_2_L(bpy.types.Operator):
    bl_idname = "operator.toe_roll_2_l"
    bl_label = "BlenRig Select toe_roll_2_L"
    bl_description = "toe_roll_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_2_L")
        return {"FINISHED"}

class Operator_Toe_1_FK_L(bpy.types.Operator):
    bl_idname = "operator.toe_1_fk_l"
    bl_label = "BlenRig Select toe_1_fk_L"
    bl_description = "toe_1_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_1_fk_L")
        return {"FINISHED"}

class Operator_Toes_IK_Ctrl_Mid_L(bpy.types.Operator):
    bl_idname = "operator.toes_ik_ctrl_mid_l"
    bl_label = "BlenRig Select toes_ik_ctrl_mid_L"
    bl_description = "toes_ik_ctrl_mid_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toes_ik_ctrl_mid_L")
        return {"FINISHED"}

class Operator_Toe_Roll_1_L(bpy.types.Operator):
    bl_idname = "operator.toe_roll_1_l"
    bl_label = "BlenRig Select toe_roll_1_L"
    bl_description = "toe_roll_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_1_L")
        return {"FINISHED"}

class Operator_Foot_L(bpy.types.Operator):
    bl_idname = "operator.foot_l"
    bl_label = "BlenRig Select foot_L"
    bl_description = "foot_ik_ctrl_L / foot_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_leg_L'].ik_leg_L)
        if ('foot_ik_ctrl_L' and 'foot_fk_L' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["foot_ik_ctrl_L"]
            else:
                Bone = armobj.pose.bones["foot_fk_L"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Foot_Roll_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.foot_roll_ctrl_l"
    bl_label = "BlenRig Select foot_roll_ctrl_L"
    bl_description = "foot_roll_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "foot_roll_ctrl_L")
        return {"FINISHED"}

class Operator_Toes_Spread_L(bpy.types.Operator):
    bl_idname = "operator.toes_spread_l"
    bl_label = "BlenRig Select toes_spread_L"
    bl_description = "toes_spread_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toes_spread_L")
        return {"FINISHED"}

class Operator_Toe_Lit_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.toe_lit_ctrl_l"
    bl_label = "BlenRig Select toe_lit_ctrl_L"
    bl_description = "toe_lit_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_ctrl_L")
        return {"FINISHED"}

class Operator_Toe_Lit_2_L(bpy.types.Operator):
    bl_idname = "operator.toe_lit_2_l"
    bl_label = "BlenRig Select toe_lit_2_L"
    bl_description = "toe_lit_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_2_L")
        return {"FINISHED"}

class Operator_Toe_Lit_3_L(bpy.types.Operator):
    bl_idname = "operator.toe_lit_3_l"
    bl_label = "BlenRig Select toe_lit_3_L"
    bl_description = "toe_lit_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_3_L")
        return {"FINISHED"}

class Operator_Toe_Lit_IK_L(bpy.types.Operator):
    bl_idname = "operator.toe_lit_ik_l"
    bl_label = "BlenRig Select toe_lit_ik_L"
    bl_description = "toe_lit_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_lit_ik_L")
        return {"FINISHED"}

class Operator_Toe_Fourth_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_ctrl_l"
    bl_label = "BlenRig Select toe_fourth_ctrl_L"
    bl_description = "toe_fourth_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_ctrl_L")
        return {"FINISHED"}

class Operator_Toe_Fourth_2_L(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_2_l"
    bl_label = "BlenRig Select toe_fourth_2_L"
    bl_description = "toe_fourth_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_2_L")
        return {"FINISHED"}

class Operator_Toe_Fourth_3_L(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_3_l"
    bl_label = "BlenRig Select toe_fourth_3_L"
    bl_description = "toe_fourth_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_3_L")
        return {"FINISHED"}

class Operator_Toe_Fourth_4_L(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_4_l"
    bl_label = "BlenRig Select toe_fourth_4_L"
    bl_description = "toe_fourth_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_4_L")
        return {"FINISHED"}

class Operator_Toe_Fourth_IK_L(bpy.types.Operator):
    bl_idname = "operator.toe_fourth_ik_l"
    bl_label = "BlenRig Select toe_fourth_ik_L"
    bl_description = "toe_fourth_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_fourth_ik_L")
        return {"FINISHED"}

class Operator_Toe_Mid_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.toe_mid_ctrl_l"
    bl_label = "BlenRig Select toe_mid_ctrl_L"
    bl_description = "toe_mid_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_ctrl_L")
        return {"FINISHED"}

class Operator_Toe_Mid_2_L(bpy.types.Operator):
    bl_idname = "operator.toe_mid_2_l"
    bl_label = "BlenRig Select toe_mid_2_L"
    bl_description = "toe_mid_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_2_L")
        return {"FINISHED"}

class Operator_Toe_Mid_3_L(bpy.types.Operator):
    bl_idname = "operator.toe_mid_3_l"
    bl_label = "BlenRig Select toe_mid_3_L"
    bl_description = "toe_mid_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_3_L")
        return {"FINISHED"}

class Operator_Toe_Mid_4_L(bpy.types.Operator):
    bl_idname = "operator.toe_mid_4_l"
    bl_label = "BlenRig Select toe_mid_4_L"
    bl_description = "toe_mid_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_4_L")
        return {"FINISHED"}

class Operator_Toe_Mid_IK_L(bpy.types.Operator):
    bl_idname = "operator.toe_mid_ik_l"
    bl_label = "BlenRig Select toe_mid_ik_L"
    bl_description = "toe_mid_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_mid_ik_L")
        return {"FINISHED"}

class Operator_Toe_Ind_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.toe_ind_ctrl_l"
    bl_label = "BlenRig Select toe_ind_ctrl_L"
    bl_description = "toe_ind_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_ctrl_L")
        return {"FINISHED"}

class Operator_Toe_Ind_2_L(bpy.types.Operator):
    bl_idname = "operator.toe_ind_2_l"
    bl_label = "BlenRig Select toe_ind_2_L"
    bl_description = "toe_ind_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_2_L")
        return {"FINISHED"}

class Operator_Toe_Ind_3_L(bpy.types.Operator):
    bl_idname = "operator.toe_ind_3_l"
    bl_label = "BlenRig Select toe_ind_3_L"
    bl_description = "toe_ind_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_3_L")
        return {"FINISHED"}

class Operator_Toe_Ind_4_L(bpy.types.Operator):
    bl_idname = "operator.toe_ind_4_l"
    bl_label = "BlenRig Select toe_ind_4_L"
    bl_description = "toe_ind_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_4_L")
        return {"FINISHED"}

class Operator_Toe_Ind_IK_L(bpy.types.Operator):
    bl_idname = "operator.toe_ind_ik_l"
    bl_label = "BlenRig Select toe_ind_ik_L"
    bl_description = "toe_ind_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_ind_ik_L")
        return {"FINISHED"}

class Operator_Toe_Big_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.toe_big_ctrl_l"
    bl_label = "BlenRig Select toe_big_ctrl_L"
    bl_description = "toe_big_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_ctrl_L")
        return {"FINISHED"}

class Operator_Toe_Big_2_L(bpy.types.Operator):
    bl_idname = "operator.toe_big_2_l"
    bl_label = "BlenRig Select toe_big_2_L"
    bl_description = "toe_big_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_2_L")
        return {"FINISHED"}

class Operator_Toe_Big_3_L(bpy.types.Operator):
    bl_idname = "operator.toe_big_3_l"
    bl_label = "BlenRig Select toe_big_3_L"
    bl_description = "toe_big_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_3_L")
        return {"FINISHED"}

class Operator_Toe_Big_IK_L(bpy.types.Operator):
    bl_idname = "operator.toe_big_ik_l"
    bl_label = "BlenRig Select toe_big_ik_L"
    bl_description = "toe_big_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toe_big_ik_L")
        return {"FINISHED"}

class Operator_Sole_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.sole_ctrl_l"
    bl_label = "BlenRig Select sole_ctrl_L"
    bl_description = "sole_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "sole_ctrl_L")
        return {"FINISHED"}

class Operator_Sole_Pivot_Point_L(bpy.types.Operator):
    bl_idname = "operator.sole_pivot_point_l"
    bl_label = "BlenRig Select sole_pivot_point_L"
    bl_description = "sole_pivot_point_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "sole_pivot_point_L")
        return {"FINISHED"}

#MASTER

class Operator_Master(bpy.types.Operator):
    bl_idname = "operator.master"
    bl_label = "BlenRig Select master"
    bl_description = "master"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "master")
        return {"FINISHED"}

class Operator_Master_Pivot_Point(bpy.types.Operator):
    bl_idname = "operator.master_pivot_point"
    bl_label = "BlenRig Select master_pivot_point"
    bl_description = "master_pivot_point"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "master_pivot_point")
        return {"FINISHED"}

#MASTER EXTRA

class Operator_Master_extra(bpy.types.Operator):
    bl_idname = "operator.master_extra"
    bl_label = "BlenRig Select master extra"
    bl_description = "master extra"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "master_extra")
        return {"FINISHED"}

######### QUADRUPED #######################################

#ARM_L

class Operator_Ankle_Toon_L(bpy.types.Operator):
    bl_idname = "operator.ankle_toon_l"
    bl_label = "BlenRig Select ankle_toon_L"
    bl_description = "ankle_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ankle_toon_L")
        return {"FINISHED"}

class Operator_Carpal_FK_L(bpy.types.Operator):
    bl_idname = "operator.carpal_fk_l"
    bl_label = "BlenRig Select carpal_fk_L"
    bl_description = "carpal_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "carpal_fk_L")
        return {"FINISHED"}

class Operator_Carpal_IK_L(bpy.types.Operator):
    bl_idname = "operator.carpal_ik_l"
    bl_label = "BlenRig Select carpal_ik_L"
    bl_description = "carpal_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "carpal_ik_L")
        return {"FINISHED"}

class Operator_Carpal_Toon_L(bpy.types.Operator):
    bl_idname = "operator.carpal_toon_l"
    bl_label = "BlenRig Select carpal_toon_L"
    bl_description = "carpal_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "carpal_toon_L")
        return {"FINISHED"}

#ARM_R

class Operator_Ankle_Toon_R(bpy.types.Operator):
    bl_idname = "operator.ankle_toon_r"
    bl_label = "BlenRig Select ankle_toon_R"
    bl_description = "ankle_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ankle_toon_R")
        return {"FINISHED"}

class Operator_Carpal_FK_R(bpy.types.Operator):
    bl_idname = "operator.carpal_fk_r"
    bl_label = "BlenRig Select carpal_fk_R"
    bl_description = "carpal_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "carpal_fk_R")
        return {"FINISHED"}

class Operator_Carpal_IK_R(bpy.types.Operator):
    bl_idname = "operator.carpal_ik_r"
    bl_label = "BlenRig Select carpal_ik_R"
    bl_description = "carpal_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "carpal_ik_R")
        return {"FINISHED"}

class Operator_Carpal_Toon_R(bpy.types.Operator):
    bl_idname = "operator.carpal_toon_r"
    bl_label = "BlenRig Select carpal_toon_R"
    bl_description = "carpal_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "carpal_toon_R")
        return {"FINISHED"}

#LEG_L

class Operator_Hock_Toon_L(bpy.types.Operator):
    bl_idname = "operator.hock_toon_l"
    bl_label = "BlenRig Select hock_toon_L"
    bl_description = "hock_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hock_toon_L")
        return {"FINISHED"}

class Operator_Tarsal_FK_L(bpy.types.Operator):
    bl_idname = "operator.tarsal_fk_l"
    bl_label = "BlenRig Select tarsal_fk_L"
    bl_description = "tarsal_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_fk_L")
        return {"FINISHED"}

class Operator_Tarsal_IK_L(bpy.types.Operator):
    bl_idname = "operator.tarsal_ik_l"
    bl_label = "BlenRig Select tarsal_ik_L"
    bl_description = "tarsal_ik_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_ik_L")
        return {"FINISHED"}

class Operator_Tarsal_Toon_L(bpy.types.Operator):
    bl_idname = "operator.tarsal_toon_l"
    bl_label = "BlenRig Select tarsal_toon_L"
    bl_description = "tarsal_toon_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_toon_L")
        return {"FINISHED"}

#LEG_R

class Operator_Hock_Toon_R(bpy.types.Operator):
    bl_idname = "operator.hock_toon_r"
    bl_label = "BlenRig Select hock_toon_R"
    bl_description = "hock_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hock_toon_R")
        return {"FINISHED"}

class Operator_Tarsal_FK_R(bpy.types.Operator):
    bl_idname = "operator.tarsal_fk_r"
    bl_label = "BlenRig Select tarsal_fk_R"
    bl_description = "tarsal_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_fk_R")
        return {"FINISHED"}

class Operator_Tarsal_IK_R(bpy.types.Operator):
    bl_idname = "operator.tarsal_ik_r"
    bl_label = "BlenRig Select tarsal_ik_R"
    bl_description = "tarsal_ik_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_ik_R")
        return {"FINISHED"}

class Operator_Tarsal_Toon_R(bpy.types.Operator):
    bl_idname = "operator.tarsal_toon_r"
    bl_label = "BlenRig Select tarsal_toon_R"
    bl_description = "tarsal_toon_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_toon_R")
        return {"FINISHED"}

#HAND_L

class Operator_Fing_2_FK_L(bpy.types.Operator):
    bl_idname = "operator.fing_2_fk_l"
    bl_label = "BlenRig Select fing_2_fk_L"
    bl_description = "fing_2_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_2_fk_L")
        return {"FINISHED"}

class Operator_Fing_Roll_2_L(bpy.types.Operator):
    bl_idname = "operator.fing_roll_2_l"
    bl_label = "BlenRig Select fing_roll_2_L"
    bl_description = "fing_roll_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_2_L")
        return {"FINISHED"}

class Operator_Fing_1_FK_L(bpy.types.Operator):
    bl_idname = "operator.fing_1_fk_l"
    bl_label = "BlenRig Select fing_1_fk_L"
    bl_description = "fing_1_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_1_fk_L")
        return {"FINISHED"}

class Operator_Fing_Roll_1_L(bpy.types.Operator):
    bl_idname = "operator.fing_roll_1_l"
    bl_label = "BlenRig Select fing_roll_1_L"
    bl_description = "fing_roll_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_1_L")
        return {"FINISHED"}

class Operator_Hand_L(bpy.types.Operator):
    bl_idname = "operator.hand_l"
    bl_label = "BlenRig Select hand_L"
    bl_description = "hand_ik_ctrl_L / hand_fk_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_L'].ik_arm_L)
        if ('hand_ik_ctrl_L' and 'hand_fk_L' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["hand_ik_ctrl_L"]
            else:
                Bone = armobj.pose.bones["hand_fk_L"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Hand_Roll_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.hand_roll_ctrl_l"
    bl_label = "BlenRig Select hand_roll_ctrl_L"
    bl_description = "hand_roll_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_roll_ctrl_L")
        return {"FINISHED"}

class Operator_Hand_Sole_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.hand_sole_ctrl_l"
    bl_label = "BlenRig Select hand_sole_ctrl_L"
    bl_description = "hand_sole_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_ctrl_L")
        return {"FINISHED"}

class Operator_Hand_Sole_Pivot_Point_L(bpy.types.Operator):
    bl_idname = "operator.hand_sole_pivot_point_l"
    bl_label = "BlenRig Select hand_sole_pivot_point_L"
    bl_description = "hand_sole_pivot_point_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_pivot_point_L")
        return {"FINISHED"}

#HAND_R

class Operator_Fing_2_FK_R(bpy.types.Operator):
    bl_idname = "operator.fing_2_fk_r"
    bl_label = "BlenRig Select fing_2_fk_R"
    bl_description = "fing_2_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_2_fk_R")
        return {"FINISHED"}

class Operator_Fing_Roll_2_R(bpy.types.Operator):
    bl_idname = "operator.fing_roll_2_r"
    bl_label = "BlenRig Select fing_roll_2_R"
    bl_description = "fing_roll_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_2_R")
        return {"FINISHED"}

class Operator_Fing_1_FK_R(bpy.types.Operator):
    bl_idname = "operator.fing_1_fk_r"
    bl_label = "BlenRig Select fing_1_fk_R"
    bl_description = "fing_1_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_1_fk_R")
        return {"FINISHED"}

class Operator_Fing_Roll_1_R(bpy.types.Operator):
    bl_idname = "operator.fing_roll_1_r"
    bl_label = "BlenRig Select fing_roll_1_R"
    bl_description = "fing_roll_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_1_R")
        return {"FINISHED"}

class Operator_Hand_R(bpy.types.Operator):
    bl_idname = "operator.hand_r"
    bl_label = "BlenRig Select hand_R"
    bl_description = "hand_ik_ctrl_R / hand_fk_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ankle_toon_L")
        return {"FINISHED"}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_R'].ik_arm_R)
        if ('hand_ik_ctrl_R' and 'hand_fk_R' in armobj.pose.bones):
            #Target Bone
            if prop == 0:
                Bone = armobj.pose.bones["hand_ik_ctrl_R"]
            else:
                Bone = armobj.pose.bones["hand_fk_R"]
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones]
                #Set target bone as active
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1
            else:
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone
        return {"FINISHED"}

class Operator_Hand_Roll_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.hand_roll_ctrl_r"
    bl_label = "BlenRig Select hand_roll_ctrl_R"
    bl_description = "hand_roll_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_roll_ctrl_R")
        return {"FINISHED"}

class Operator_Hand_Sole_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.hand_sole_ctrl_r"
    bl_label = "BlenRig Select hand_sole_ctrl_R"
    bl_description = "hand_sole_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_ctrl_R")
        return {"FINISHED"}

class Operator_Hand_Sole_Pivot_Point_R(bpy.types.Operator):
    bl_idname = "operator.hand_sole_pivot_point_r"
    bl_label = "BlenRig Select hand_sole_pivot_point_R"
    bl_description = "hand_sole_pivot_point_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_pivot_point_R")
        return {"FINISHED"}
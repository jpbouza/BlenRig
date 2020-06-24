import bpy
from mathutils import Matrix
from bpy.props import StringProperty

#Matrix Functions (Taken from Copy Attributes Menu Addon)

def getmat(bone, active, ignoreparent):
    """Helper function for visual transform copy,
       gets the active transform in bone space
    """
    obj_bone = bone.id_data
    obj_active = active.id_data
    data_bone = obj_bone.data.bones[bone.name]
    # all matrices are in armature space unless commented otherwise
    active_to_selected = obj_bone.matrix_world.inverted() @ obj_active.matrix_world
    active_matrix = active_to_selected @ active.matrix
    otherloc = active_matrix  # final 4x4 mat of target, location.
    bonemat_local = data_bone.matrix_local.copy()  # self rest matrix
    if data_bone.parent:
        parentposemat = obj_bone.pose.bones[data_bone.parent.name].matrix.copy()
        parentbonemat = data_bone.parent.matrix_local.copy()
    else:
        parentposemat = parentbonemat = Matrix()
    if parentbonemat == parentposemat or ignoreparent:
        newmat = bonemat_local.inverted() @ otherloc
    else:
        bonemat = parentbonemat.inverted() @ bonemat_local

        newmat = bonemat.inverted() @ parentposemat.inverted() @ otherloc
    return newmat

def rotcopy(item, mat):
    """Copy rotation to item from matrix mat depending on item.rotation_mode"""
    if item.rotation_mode == 'QUATERNION':
        item.rotation_quaternion = mat.to_3x3().to_quaternion()
    elif item.rotation_mode == 'AXIS_ANGLE':
        rot = mat.to_3x3().to_quaternion().to_axis_angle()    # returns (Vector((x, y, z)), w)
        axis_angle = rot[1], rot[0][0], rot[0][1], rot[0][2]  # convert to w, x, y, z
        item.rotation_axis_angle = axis_angle
    else:
        item.rotation_euler = mat.to_3x3().to_euler(item.rotation_mode)

def pVisLocExec(bone, active):
    bone.location = getmat(bone, active, False).to_translation()

def pVisRotExec(bone, active):
    obj_bone = bone.id_data
    rotcopy(bone, getmat(bone, active, not obj_bone.data.bones[bone.name].use_inherit_rotation))


def pVisScaExec(bone, active):
    obj_bone = bone.id_data
    bone.scale = getmat(bone, active, not obj_bone.data.bones[bone.name].use_inherit_scale)\
        .to_scale()

#Copy Matrix from Bone to Self after Space change
def paste_visual_matrix(bone, parent_bone, bone_world, bone_matrix, transform_type):
    """Helper function for visual transform copy,
       given a bone transform (bone_world and bone_matrix), it pastes back the visual transform after changing the space property.
       The parent_bone has changed with the Armature constraint.
    """

    armobj = bpy.context.active_object
    pbones = armobj.pose.bones
    dbones = armobj.data.bones

    #Get Matrix in previous space
    bone_previous_world = bone_world
    bone_previous_mat = bone_matrix

    #Paste Matrix in new Space
    obj_bone = pbones[bone].id_data
    data_bone = obj_bone.data.bones[bone]
    # all matrices are in armature space unless commented otherwise
    active_to_selected = obj_bone.matrix_world.inverted() @ bone_previous_world
    active_matrix = active_to_selected @ bone_previous_mat
    otherloc = active_matrix  # final 4x4 mat of target, location.
    bonemat_local = data_bone.matrix_local.copy()  # self rest matrix

    parentposemat = pbones[parent_bone].matrix.copy()
    parentbonemat = dbones[parent_bone].matrix_local.copy()

    if parentbonemat == parentposemat:
        newmat = bonemat_local.inverted() @ otherloc
    else:
        bonemat = parentbonemat.inverted() @ bonemat_local

        newmat = bonemat.inverted() @ parentposemat.inverted() @ otherloc

    if transform_type == 'Location':
        pbones[bone].location = newmat.to_translation()
        refresh_hack()
    if transform_type == 'Rotation':
        rotcopy(pbones[bone], newmat)
        refresh_hack()
    if transform_type == 'Scale':
        bone.scale = newmat.to_scale()
        refresh_hack()

#Armature Refresh Hack
def refresh_hack():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')

#Insert Bone Keyframes Function
def insert_bkeys(b_name, key_type):
    armobj = bpy.context.active_object
    pbones = armobj.pose.bones

    if pbones.get(b_name) != None:
        if key_type == 'Loc':
            pbones[b_name].keyframe_insert(data_path="location", group=b_name)

        if key_type == 'Rot':
            if pbones[b_name].rotation_mode == 'QUATERNION':
                pbones[b_name].keyframe_insert(data_path="rotation_quaternion", group=b_name)
            elif pbones[b_name].rotation_mode == 'AXIS_ANGLE':
                pbones[b_name].keyframe_insert(data_path="rotation_axis_angle", group=b_name)
            else:
                pbones[b_name].keyframe_insert(data_path="rotation_euler", group=b_name)

        if key_type == 'Scale':
            pbones[b_name].keyframe_insert(data_path="scale", group=b_name)

        if key_type == 'LocRot':
            pbones[b_name].keyframe_insert(data_path="location", group=b_name)
            if pbones[b_name].rotation_mode == 'QUATERNION':
                pbones[b_name].keyframe_insert(data_path="rotation_quaternion", group=b_name)
            elif pbones[b_name].rotation_mode == 'AXIS_ANGLE':
                pbones[b_name].keyframe_insert(data_path="rotation_axis_angle", group=b_name)
            else:
                pbones[b_name].keyframe_insert(data_path="rotation_euler", group=b_name)

        if key_type == 'LocScale':
            pbones[b_name].keyframe_insert(data_path="location", group=b_name)
            pbones[b_name].keyframe_insert(data_path="scale", group=b_name)

        if key_type == 'RotScale':
            pbones[b_name].keyframe_insert(data_path="scale", group=b_name)
            if pbones[b_name].rotation_mode == 'QUATERNION':
                pbones[b_name].keyframe_insert(data_path="rotation_quaternion", group=b_name)
            elif pbones[b_name].rotation_mode == 'AXIS_ANGLE':
                pbones[b_name].keyframe_insert(data_path="rotation_axis_angle", group=b_name)
            else:
                pbones[b_name].keyframe_insert(data_path="rotation_euler", group=b_name)

        if key_type == 'LocRotScale':
            pbones[b_name].keyframe_insert(data_path="location", group=b_name)
            pbones[b_name].keyframe_insert(data_path="scale", group=b_name)
            if pbones[b_name].rotation_mode == 'QUATERNION':
                pbones[b_name].keyframe_insert(data_path="rotation_quaternion", group=b_name)
            elif pbones[b_name].rotation_mode == 'AXIS_ANGLE':
                pbones[b_name].keyframe_insert(data_path="rotation_axis_angle", group=b_name)
            else:
                pbones[b_name].keyframe_insert(data_path="rotation_euler", group=b_name)

##### Left Ops #####

##### Arm_L IK>FK #####

class Operator_Snap_ArmIKtoFK_L(bpy.types.Operator):

    bl_idname = "snap.arm_ik_to_fk_l"
    bl_label = "BlenRig Arm_L IK to FK"
    bl_description = "Switch Arm to FK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if armobj.pose.bones["properties_arm_L"].ik_arm_L < 0.1:

            #Collect Matrix
            ArmFkMat = pbones['arm_fk_L'].matrix.copy()
            ArmFkLoc = pbones['arm_fk_L'].location.copy()
            ArmFkScale = pbones['arm_fk_L'].scale.copy()
            ForearmFkMat = pbones['forearm_fk_L'].matrix.copy()
            ForearmFkLoc = pbones['forearm_fk_L'].location.copy()
            ForearmFkScale = pbones['forearm_fk_L'].scale.copy()
            ShoulderMat = pbones['shoulder_L'].matrix.copy()
            ShoulderLoc = pbones['shoulder_L'].location.copy()
            ShoulderScale = pbones['shoulder_L'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='ik_arm_L')
                        insert_bkeys('arm_fk_L', 'LocRotScale')
                        insert_bkeys('forearm_fk_L', 'LocRotScale')
                        insert_bkeys('arm_ik_L', 'RotScale')
                        insert_bkeys('forearm_ik_L', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('shoulder_L', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('hand_fk_L', 'LocRotScale')
                        if pbones["properties_arm_L"].toggle_arm_ik_pole_L == 1.0:
                            insert_bkeys('elbow_pole_L', 'Loc')

            armobj.pose.bones["properties_arm_L"].ik_arm_L = 1.0
            refresh_hack()

            #Paste Matrix
            pVisRotExec (pbones['arm_fk_ctrl_L'], pbones['arm_ik_L'])
            pbones['arm_fk_ctrl_L'].scale[:] = (1.0, 1.0, 1.0)
            refresh_hack()
            pbones['shoulder_L'].matrix = ShoulderMat
            pbones['shoulder_L'].location = ShoulderLoc
            pbones['shoulder_L'].scale = ShoulderScale
            refresh_hack()
            pbones['arm_fk_L'].matrix = ArmFkMat
            pbones['arm_fk_L'].location = ArmFkLoc
            pbones['arm_fk_L'].scale = ArmFkScale
            refresh_hack()
            pbones['forearm_fk_L'].matrix = ForearmFkMat
            pbones['forearm_fk_L'].location = ForearmFkLoc
            pbones['forearm_fk_L'].scale = ForearmFkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        ShoulderRotEuler = pbones['shoulder_L'].rotation_euler.copy()
                        ShoulderRotQuat = pbones['shoulder_L'].rotation_quaternion.copy()
                        ShoulderLoc = pbones['shoulder_L'].location.copy()
                        ShoulderScale = pbones['shoulder_L'].scale.copy()

                        ArmCtrlRotEuler = pbones['arm_fk_ctrl_L'].rotation_euler.copy()
                        ArmCtrlRotQuat = pbones['arm_fk_ctrl_L'].rotation_quaternion.copy()
                        ArmCtrlLoc = pbones['arm_fk_ctrl_L'].location.copy()
                        ArmCtrlScale = pbones['arm_fk_ctrl_L'].scale.copy()

                        ArmFkRotEuler = pbones['arm_fk_L'].rotation_euler.copy()
                        ArmFkRotQuat = pbones['arm_fk_L'].rotation_quaternion.copy()
                        ArmFkLoc = pbones['arm_fk_L'].location.copy()
                        ArmFkScale = pbones['arm_fk_L'].scale.copy()

                        ForearmFkRotEuler = pbones['forearm_fk_L'].rotation_euler.copy()
                        ForearmFkRotQuat = pbones['forearm_fk_L'].rotation_quaternion.copy()
                        ForearmFkLoc = pbones['forearm_fk_L'].location.copy()
                        ForearmFkScale = pbones['forearm_fk_L'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_arm_L"].ik_arm_L = 1.0
                        refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='ik_arm_L')

                        #Re-Paste Transforms
                        pbones['shoulder_L'].rotation_euler = ShoulderRotEuler
                        pbones['shoulder_L'].rotation_quaternion = ShoulderRotQuat
                        pbones['shoulder_L'].location = ShoulderLoc
                        pbones['shoulder_L'].scale = ShoulderScale
                        refresh_hack()
                        pbones['arm_fk_ctrl_L'].rotation_euler = ArmCtrlRotEuler
                        pbones['arm_fk_ctrl_L'].rotation_quaternion = ArmCtrlRotQuat
                        pbones['arm_fk_ctrl_L'].location = ArmCtrlLoc
                        pbones['arm_fk_ctrl_L'].scale = ArmCtrlScale
                        refresh_hack()
                        pbones['arm_fk_L'].rotation_euler = ArmFkRotEuler
                        pbones['arm_fk_L'].rotation_quaternion = ArmFkRotQuat
                        pbones['arm_fk_L'].location = ArmFkLoc
                        pbones['arm_fk_L'].scale = ArmFkScale
                        refresh_hack()
                        pbones['forearm_fk_L'].rotation_euler = ForearmFkRotEuler
                        pbones['forearm_fk_L'].rotation_quaternion = ForearmFkRotQuat
                        pbones['forearm_fk_L'].location = ForearmFkLoc
                        pbones['forearm_fk_L'].scale = ForearmFkScale
                        refresh_hack()

                        insert_bkeys('arm_fk_L', 'LocRotScale')
                        insert_bkeys('forearm_fk_L', 'LocRotScale')
                        insert_bkeys('arm_ik_L', 'RotScale')
                        insert_bkeys('forearm_ik_L', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('shoulder_L', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('hand_fk_L', 'LocRotScale')
                        if pbones["properties_arm_L"].toggle_arm_ik_pole_L == 1.0:
                            insert_bkeys('elbow_pole_L', 'Loc')

            #Switch Hand to Arm Space
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)

            #Switch Hand to Arm Space
            bpy.ops.switch.hand_space_l(space='Arm')


        return {"FINISHED"}

##### Arm_L FK>IK #####

class Operator_Snap_ArmFKtoIK_L(bpy.types.Operator):

    bl_idname = "snap.arm_fk_to_ik_l"
    bl_label = "BlenRig Arm_L FK to IK"
    bl_description = "Switch Arm to IK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if bpy.context.active_object.pose.bones["properties_arm_L"].ik_arm_L > 0.9:
            #Collect Matrix
            ArmFkMat = pbones['arm_fk_L'].matrix.copy()
            ArmFkLoc = pbones['arm_fk_L'].location.copy()
            ArmFkScale = pbones['arm_fk_L'].scale.copy()
            ForearmFkMat = pbones['forearm_fk_L'].matrix.copy()
            ForearmFkLoc = pbones['forearm_fk_L'].location.copy()
            ForearmFkScale = pbones['forearm_fk_L'].scale.copy()
            ArmFkCtrlMat = pbones['arm_fk_ctrl_L'].matrix.copy()
            ShoulderMat = pbones['shoulder_L'].matrix.copy()
            ShoulderLoc = pbones['shoulder_L'].location.copy()
            ShoulderScale = pbones['shoulder_L'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='ik_arm_L')
                        insert_bkeys('arm_fk_L', 'LocRotScale')
                        insert_bkeys('forearm_fk_L', 'LocRotScale')
                        insert_bkeys('arm_ik_L', 'RotScale')
                        insert_bkeys('forearm_ik_L', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('shoulder_L', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('hand_fk_L', 'LocRotScale')
                        if pbones["properties_arm_L"].toggle_arm_ik_pole_L == 1.0:
                            insert_bkeys('elbow_pole_L', 'Loc')

            #Paste Matrix
            pVisLocExec(pbones['hand_ik_ctrl_L'], pbones['hand_fk_L'])
            refresh_hack()
            pVisLocExec(pbones['elbow_pole_L'], pbones['snap_elbow_pole_fk_L'])
            refresh_hack()

            bpy.context.active_object.pose.bones["properties_arm_L"].ik_arm_L = 0.0
            refresh_hack()

            pVisRotExec (pbones['arm_ik_L'], pbones['arm_fk_ctrl_L'])
            refresh_hack()
            pbones['shoulder_L'].matrix = ShoulderMat
            pbones['shoulder_L'].location = ShoulderLoc
            pbones['shoulder_L'].scale = ShoulderScale
            refresh_hack()
            pbones['arm_fk_L'].matrix = ArmFkMat
            pbones['arm_fk_L'].location = ArmFkLoc
            pbones['arm_fk_L'].scale = ArmFkScale
            refresh_hack()
            pbones['forearm_fk_L'].matrix = ForearmFkMat
            pbones['forearm_fk_L'].location = ForearmFkLoc
            pbones['forearm_fk_L'].scale = ForearmFkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        HandIkCtrlRotEuler = pbones['hand_ik_ctrl_L'].rotation_euler.copy()
                        HandIkCtrlRotQuat = pbones['hand_ik_ctrl_L'].rotation_quaternion.copy()
                        HandIkCtrlLoc = pbones['hand_ik_ctrl_L'].location.copy()
                        HandIkCtrlScale = pbones['hand_ik_ctrl_L'].scale.copy()

                        ArmIkRotEuler = pbones['arm_ik_L'].rotation_euler.copy()
                        ArmIkRotQuat = pbones['arm_ik_L'].rotation_quaternion.copy()
                        ArmIkLoc = pbones['arm_ik_L'].location.copy()
                        ArmIkScale = pbones['arm_ik_L'].scale.copy()

                        ElbowlLoc = pbones['elbow_pole_L'].location.copy()

                        ShoulderRotEuler = pbones['shoulder_L'].rotation_euler.copy()
                        ShoulderRotQuat = pbones['shoulder_L'].rotation_quaternion.copy()
                        ShoulderLoc = pbones['shoulder_L'].location.copy()
                        ShoulderScale = pbones['shoulder_L'].scale.copy()

                        ArmFkRotEuler = pbones['arm_fk_L'].rotation_euler.copy()
                        ArmFkRotQuat = pbones['arm_fk_L'].rotation_quaternion.copy()
                        ArmFkLoc = pbones['arm_fk_L'].location.copy()
                        ArmFkScale = pbones['arm_fk_L'].scale.copy()

                        ForearmFkRotEuler = pbones['forearm_fk_L'].rotation_euler.copy()
                        ForearmFkRotQuat = pbones['forearm_fk_L'].rotation_quaternion.copy()
                        ForearmFkLoc = pbones['forearm_fk_L'].location.copy()
                        ForearmFkScale = pbones['forearm_fk_L'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_arm_L"].ik_arm_L = 0.0
                        refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='ik_arm_L')

                        #Re-Paste Transforms
                        pbones['hand_ik_ctrl_L'].rotation_euler = HandIkCtrlRotEuler
                        pbones['hand_ik_ctrl_L'].rotation_quaternion = HandIkCtrlRotQuat
                        pbones['hand_ik_ctrl_L'].location = HandIkCtrlLoc
                        pbones['hand_ik_ctrl_L'].scale = HandIkCtrlScale
                        refresh_hack()
                        pbones['elbow_pole_L'].location = ElbowlLoc
                        refresh_hack()
                        pbones['arm_ik_L'].rotation_euler = ArmIkRotEuler
                        pbones['arm_ik_L'].rotation_quaternion = ArmIkRotQuat
                        pbones['arm_ik_L'].location = ArmIkLoc
                        pbones['arm_ik_L'].scale = ArmIkScale
                        refresh_hack()
                        pbones['shoulder_L'].rotation_euler = ShoulderRotEuler
                        pbones['shoulder_L'].rotation_quaternion = ShoulderRotQuat
                        pbones['shoulder_L'].location = ShoulderLoc
                        pbones['shoulder_L'].scale = ShoulderScale
                        refresh_hack()
                        pbones['arm_fk_L'].rotation_euler = ArmFkRotEuler
                        pbones['arm_fk_L'].rotation_quaternion = ArmFkRotQuat
                        pbones['arm_fk_L'].location = ArmFkLoc
                        pbones['arm_fk_L'].scale = ArmFkScale
                        refresh_hack()
                        pbones['forearm_fk_L'].rotation_euler = ForearmFkRotEuler
                        pbones['forearm_fk_L'].rotation_quaternion = ForearmFkRotQuat
                        pbones['forearm_fk_L'].location = ForearmFkLoc
                        pbones['forearm_fk_L'].scale = ForearmFkScale
                        refresh_hack()

                        insert_bkeys('arm_fk_L', 'LocRotScale')
                        insert_bkeys('forearm_fk_L', 'LocRotScale')
                        insert_bkeys('arm_ik_L', 'RotScale')
                        insert_bkeys('forearm_ik_L', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('shoulder_L', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('hand_fk_L', 'LocRotScale')
                        if pbones["properties_arm_L"].toggle_arm_ik_pole_L == 1.0:
                            insert_bkeys('elbow_pole_L', 'Loc')

            #Switch Hand to Arm Space
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)

            #Switch Hand to Free Space
            bpy.ops.switch.hand_space_l(space='Free')

        return {"FINISHED"}

##### Arm_L Space #####

class Operator_Switch_Arm_Space_L(bpy.types.Operator):

    bl_idname = "switch.arm_space_l"
    bl_label = "BlenRig Switch Arm_L Space"
    bl_description = "Switch Arm_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        HandIkMat = pbones['hand_ik_ctrl_L'].matrix.copy()
        ArmFkCtrlMat = pbones['arm_fk_ctrl_L'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_L"].keyframe_insert(data_path='space_arm_L')
                    insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                    insert_bkeys('arm_fk_ctrl_L', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 0.0
            refresh_hack()
        if self.space == 'Pelvis':
            bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 1.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 2.0
            refresh_hack()
        if self.space == 'Head':
            bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 3.0
            refresh_hack()

        #Paste Matrix
        pbones['hand_ik_ctrl_L'].matrix = HandIkMat
        pbones['arm_fk_ctrl_L'].matrix = ArmFkCtrlMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HandIkCtrlRotEuler = pbones['hand_ik_ctrl_L'].rotation_euler.copy()
                    HandIkCtrlRotQuat = pbones['hand_ik_ctrl_L'].rotation_quaternion.copy()
                    HandIkCtrlLoc = pbones['hand_ik_ctrl_L'].location.copy()
                    HandIkCtrlScale = pbones['hand_ik_ctrl_L'].scale.copy()

                    ArmCtrlRotEuler = pbones['arm_fk_ctrl_L'].rotation_euler.copy()
                    ArmCtrlRotQuat = pbones['arm_fk_ctrl_L'].rotation_quaternion.copy()
                    ArmCtrlLoc = pbones['arm_fk_ctrl_L'].location.copy()
                    ArmCtrlScale = pbones['arm_fk_ctrl_L'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 0.0
                        refresh_hack()
                    if self.space == 'Pelvis':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 1.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 2.0
                        refresh_hack()
                    if self.space == 'Head':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_L = 3.0
                        refresh_hack()
                    pbones["properties_arm_L"].keyframe_insert(data_path='space_arm_L')

                    #Re-Paste Transforms
                    pbones['hand_ik_ctrl_L'].rotation_euler = HandIkCtrlRotEuler
                    pbones['hand_ik_ctrl_L'].rotation_quaternion = HandIkCtrlRotQuat
                    pbones['hand_ik_ctrl_L'].location = HandIkCtrlLoc
                    pbones['hand_ik_ctrl_L'].scale = HandIkCtrlScale
                    refresh_hack()
                    pbones['arm_fk_ctrl_L'].rotation_euler = ArmCtrlRotEuler
                    pbones['arm_fk_ctrl_L'].rotation_quaternion = ArmCtrlRotQuat
                    pbones['arm_fk_ctrl_L'].location = ArmCtrlLoc
                    pbones['arm_fk_ctrl_L'].scale = ArmCtrlScale
                    refresh_hack()

                    insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                    insert_bkeys('arm_fk_ctrl_L', 'LocRotScale')


        return {"FINISHED"}

#Create Space PopUp
def Arm_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.arm_space_l", text = "Free").space = 'Free'
    col.operator("switch.arm_space_l", text = "Pelvis").space = 'Pelvis'
    col.operator("switch.arm_space_l", text = "Torso").space = 'Torso'
    col.operator("switch.arm_space_l", text = "Head").space = 'Head'

class Operator_Show_Arm_Space_List_L(bpy.types.Operator):
    bl_idname = "show.arm_list_l"
    bl_label = "Arm_L Space Switch List"
    bl_description = "Switch Arm_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Arm_Space_List_L, title='Switch Arm_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Hand_L Space #####

class Operator_Switch_Hand_Space_L(bpy.types.Operator):

    bl_idname = "switch.hand_space_l"
    bl_label = "BlenRig Switch Hand_L Space"
    bl_description = "Switch Hand_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_L"].keyframe_insert(data_path='space_hand_L')
                    insert_bkeys('hand_ik_ctrl_L', 'RotScale')
                    insert_bkeys('hand_fk_L', 'RotScale')

        if self.space == 'Arm':
            #Collect Matrix
            HandFkMat = pbones['hand_fk_L'].matrix.copy()
            HandFkLoc = pbones['hand_fk_L'].location.copy()
            HandFkScale = pbones['hand_fk_L'].scale.copy()

            bpy.context.active_object.pose.bones["properties_arm_L"].space_hand_L = 1.0

            #Paste Matrix
            pbones['hand_fk_L'].matrix = HandFkMat
            pbones['hand_fk_L'].location = HandFkLoc
            pbones['hand_fk_L'].scale = HandFkScale
            refresh_hack()

        if self.space == 'Free':
            #Paste Matrix
            pVisRotExec (pbones['hand_ik_ctrl_L'], pbones['hand_fk_L'])
            refresh_hack()

            bpy.context.active_object.pose.bones["properties_arm_L"].space_hand_L = 0.0
            refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HandIkCtrlRotEuler = pbones['hand_ik_ctrl_L'].rotation_euler.copy()
                    HandIkCtrlRotQuat = pbones['hand_ik_ctrl_L'].rotation_quaternion.copy()
                    HandIkCtrlScale = pbones['hand_ik_ctrl_L'].scale.copy()

                    HandFkCtrlRotEuler = pbones['hand_fk_L'].rotation_euler.copy()
                    HandFkCtrlRotQuat = pbones['hand_fk_L'].rotation_quaternion.copy()
                    HandFkCtrlScale = pbones['hand_fk_L'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Arm':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_hand_L = 1.0
                        refresh_hack()
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_hand_L = 0.0
                        refresh_hack()
                    pbones["properties_arm_L"].keyframe_insert(data_path='space_hand_L')

                    #Re-Paste Transforms
                    pbones['hand_ik_ctrl_L'].rotation_euler = HandIkCtrlRotEuler
                    pbones['hand_ik_ctrl_L'].rotation_quaternion = HandIkCtrlRotQuat
                    pbones['hand_ik_ctrl_L'].scale = HandIkCtrlScale
                    refresh_hack()
                    pbones['hand_fk_L'].rotation_euler = HandFkCtrlRotEuler
                    pbones['hand_fk_L'].rotation_quaternion = HandFkCtrlRotQuat
                    pbones['hand_fk_L'].scale = HandFkCtrlScale
                    refresh_hack()

                    insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                    insert_bkeys('hand_fk_L', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Hand_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.hand_space_l", text = "Arm").space = 'Arm'
    col.operator("switch.hand_space_l", text = "Free").space = 'Free'

class Operator_Show_Hand_Space_List_L(bpy.types.Operator):
    bl_idname = "show.hand_list_l"
    bl_label = "Hand_L Space Switch List"
    bl_description = "Switch Hand_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Hand_Space_List_L, title='Switch Hand_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Arm_Pole_L Space #####

class Operator_Switch_Arm_Pole_Space_L(bpy.types.Operator):

    bl_idname = "switch.arm_pole_space_l"
    bl_label = "BlenRig Switch Arm_L Pole Space"
    bl_description = "Switch Arm_L Pole Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_L"].keyframe_insert(data_path='space_arm_ik_pole_L')
                    insert_bkeys('elbow_pole_L', 'Loc')

        #Collect Matrix
        PoleMat = pbones['elbow_pole_L'].matrix.copy()

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_ik_pole_L = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_ik_pole_L = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['elbow_pole_L'].matrix = PoleMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    PoleLoc = pbones['elbow_pole_L'].location.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_ik_pole_L = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_arm_L"].space_arm_ik_pole_L = 1.0
                        refresh_hack()
                    pbones["properties_arm_L"].keyframe_insert(data_path='space_arm_ik_pole_L')

                    #Re-Paste Transforms
                    pbones['elbow_pole_L'].location = PoleLoc
                    refresh_hack()

                    insert_bkeys('elbow_pole_L', 'Loc')

        return {"FINISHED"}

#Create Space PopUp
def Arm_Pole_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.arm_pole_space_l", text = "Free").space = 'Free'
    col.operator("switch.arm_pole_space_l", text = "Torso").space = 'Torso'

class Operator_Show_Arm_Pole_Space_List_L(bpy.types.Operator):
    bl_idname = "show.arm_pole_list_l"
    bl_label = "Arm_L Pole Space Switch List"
    bl_description = "Switch Arm_L Pole Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Arm_Pole_Space_List_L, title='Switch Arm_L Pole Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### All Fingers_L Space #####

class Operator_Switch_Fing_All_Space_L(bpy.types.Operator):

    bl_idname = "switch.fing_all_space_l"
    bl_label = "BlenRig Switch All Fingers_L Space"
    bl_description = "Switch All Fingers_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data

        if self.space == 'Free':
            bpy.ops.switch.fing_thumb_space_l(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ind_space_l(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_mid_space_l(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ring_space_l(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_lit_space_l(space='Free')

            #Change Space
            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_all_L = 0.0

        if self.space == 'Hand':
            bpy.ops.switch.fing_thumb_space_l(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ind_space_l(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_mid_space_l(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ring_space_l(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_lit_space_l(space='Hand')

            #Change Space
            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_all_L = 1.0

        return {"FINISHED"}

#Create Space PopUp
def Fing_All_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.fing_all_space_l", text = "Free").space = 'Free'
    col.operator("switch.fing_all_space_l", text = "Hand").space = 'Hand'

class Operator_Show_Fing_All_Space_List_L(bpy.types.Operator):
    bl_idname = "show.fing_all_list_l"
    bl_label = "All Fingers_L Space Switch List"
    bl_description = "Switch All Fingers_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_All_Space_List_L, title='Switch All Fingers_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Thumb Finger_L Space #####

class Operator_Switch_Fing_Thumb_Space_L(bpy.types.Operator):

    bl_idname = "switch.fing_thumb_space_l"
    bl_label = "BlenRig Switch Thumb Finger_L Space"
    bl_description = "Switch Thumb Finger_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_thumb_L')
                        insert_bkeys('fing_thumb_ik_L', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Thumb_world_mat = pbones['fing_thumb_ik_L'].id_data.matrix_world.copy()
                Thumb_mat = pbones['fing_thumb_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_thumb_L = 0.0

                paste_visual_matrix('fing_thumb_ik_L', 'master_pivot', Thumb_world_mat, Thumb_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Thumb_world_mat = pbones['fing_thumb_ik_L'].id_data.matrix_world.copy()
                Thumb_mat = pbones['fing_thumb_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_thumb_L = 1.0

                paste_visual_matrix('fing_thumb_ik_L', 'fing_thumb_ctrl_track_L', Thumb_world_mat, Thumb_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        ThumbLoc = pbones['fing_thumb_ik_L'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_thumb_L = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_thumb_L = 1.0
                            refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_thumb_L')

                        #Re-Paste Transforms
                        pbones['fing_thumb_ik_L'].location = ThumbLoc
                        refresh_hack()

                        insert_bkeys('fing_thumb_ik_L', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Thumb_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.fing_thumb_space_l", text = "Free").space = 'Free'
    col.operator("switch.fing_thumb_space_l", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Thumb_Space_List_L(bpy.types.Operator):
    bl_idname = "show.fing_thumb_list_l"
    bl_label = "Thumb Finger_L Space Switch List"
    bl_description = "Switch Thumb Finger_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Thumb_Space_List_L, title='Switch Thumb Finger_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Ind Finger_L Space #####

class Operator_Switch_Fing_Ind_Space_L(bpy.types.Operator):

    bl_idname = "switch.fing_ind_space_l"
    bl_label = "BlenRig Switch Index Finger_L Space"
    bl_description = "Switch Index Finger_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_ind_L')
                        insert_bkeys('fing_ind_ik_L', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Ind_world_mat = pbones['fing_ind_ik_L'].id_data.matrix_world.copy()
                Ind_mat = pbones['fing_ind_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ind_L = 0.0

                paste_visual_matrix('fing_ind_ik_L', 'master_pivot', Ind_world_mat, Ind_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Ind_world_mat = pbones['fing_ind_ik_L'].id_data.matrix_world.copy()
                Ind_mat = pbones['fing_ind_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ind_L = 1.0

                paste_visual_matrix('fing_ind_ik_L', 'fing_ind_ctrl_track_L', Ind_world_mat, Ind_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        IndLoc = pbones['fing_ind_ik_L'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ind_L = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ind_L = 1.0
                            refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_ind_L')

                        #Re-Paste Transforms
                        pbones['fing_ind_ik_L'].location = IndLoc
                        refresh_hack()

                        insert_bkeys('fing_ind_ik_L', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Ind_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.fing_ind_space_l", text = "Free").space = 'Free'
    col.operator("switch.fing_ind_space_l", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Ind_Space_List_L(bpy.types.Operator):
    bl_idname = "show.fing_ind_list_l"
    bl_label = "Index Finger_L Space Switch List"
    bl_description = "Switch Index Finger_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Ind_Space_List_L, title='Switch Index Finger_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Mid Finger_L Space #####

class Operator_Switch_Fing_Mid_Space_L(bpy.types.Operator):

    bl_idname = "switch.fing_mid_space_l"
    bl_label = "BlenRig Switch Middle Finger_L Space"
    bl_description = "Switch Middle Finger_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_mid_L')
                        insert_bkeys('fing_mid_ik_L', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Mid_world_mat = pbones['fing_mid_ik_L'].id_data.matrix_world.copy()
                Mid_mat = pbones['fing_mid_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_mid_L = 0.0

                paste_visual_matrix('fing_mid_ik_L', 'master_pivot', Mid_world_mat, Mid_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Mid_world_mat = pbones['fing_mid_ik_L'].id_data.matrix_world.copy()
                Mid_mat = pbones['fing_mid_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_mid_L = 1.0

                paste_visual_matrix('fing_mid_ik_L', 'fing_mid_ctrl_track_L', Mid_world_mat, Mid_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        MidLoc = pbones['fing_mid_ik_L'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_mid_L = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_mid_L = 1.0
                            refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_mid_L')

                        #Re-Paste Transforms
                        pbones['fing_mid_ik_L'].location = MidLoc
                        refresh_hack()

                        insert_bkeys('fing_mid_ik_L', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Mid_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.fing_mid_space_l", text = "Free").space = 'Free'
    col.operator("switch.fing_mid_space_l", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Mid_Space_List_L(bpy.types.Operator):
    bl_idname = "show.fing_mid_list_l"
    bl_label = "Middle Finger_L Space Switch List"
    bl_description = "Switch Middle Finger_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Mid_Space_List_L, title='Switch Middle Finger_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Ring Finger_L Space #####

class Operator_Switch_Fing_Ring_Space_L(bpy.types.Operator):

    bl_idname = "switch.fing_ring_space_l"
    bl_label = "BlenRig Switch Ring Finger_L Space"
    bl_description = "Switch Ring Finger_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_ring_L')
                        insert_bkeys('fing_ring_ik_L', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Ring_world_mat = pbones['fing_ring_ik_L'].id_data.matrix_world.copy()
                Ring_mat = pbones['fing_ring_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ring_L = 0.0

                paste_visual_matrix('fing_ring_ik_L', 'master_pivot', Ring_world_mat, Ring_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Ring_world_mat = pbones['fing_ring_ik_L'].id_data.matrix_world.copy()
                Ring_mat = pbones['fing_ring_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ring_L = 1.0

                paste_visual_matrix('fing_ring_ik_L', 'fing_ring_ctrl_track_L', Ring_world_mat, Ring_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        RingLoc = pbones['fing_ring_ik_L'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ring_L = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_ring_L = 1.0
                            refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_ring_L')

                        #Re-Paste Transforms
                        pbones['fing_ring_ik_L'].location = RingLoc
                        refresh_hack()

                        insert_bkeys('fing_ring_ik_L', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Ring_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.fing_ring_space_l", text = "Free").space = 'Free'
    col.operator("switch.fing_ring_space_l", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Ring_Space_List_L(bpy.types.Operator):
    bl_idname = "show.fing_ring_list_l"
    bl_label = "Ring Finger_L Space Switch List"
    bl_description = "Switch Ring Finger_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Ring_Space_List_L, title='Switch Ring Finger_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Lit Finger_L Space #####

class Operator_Switch_Fing_Lit_Space_L(bpy.types.Operator):

    bl_idname = "switch.fing_lit_space_l"
    bl_label = "BlenRig Switch Little Finger_L Space"
    bl_description = "Switch Little Finger_L Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_lit_L')
                        insert_bkeys('fing_lit_ik_L', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Lit_world_mat = pbones['fing_lit_ik_L'].id_data.matrix_world.copy()
                Lit_mat = pbones['fing_lit_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_lit_L = 0.0

                paste_visual_matrix('fing_lit_ik_L', 'master_pivot', Lit_world_mat, Lit_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Lit_world_mat = pbones['fing_lit_ik_L'].id_data.matrix_world.copy()
                Lit_mat = pbones['fing_lit_ik_L'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_lit_L = 1.0

                paste_visual_matrix('fing_lit_ik_L', 'fing_lit_ctrl_track_L', Lit_world_mat, Lit_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        LitLoc = pbones['fing_lit_ik_L'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_lit_L = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_L"].space_fing_lit_L = 1.0
                            refresh_hack()
                        pbones["properties_arm_L"].keyframe_insert(data_path='space_fing_lit_L')

                        #Re-Paste Transforms
                        pbones['fing_lit_ik_L'].location = LitLoc
                        refresh_hack()

                        insert_bkeys('fing_lit_ik_L', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Lit_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.fing_lit_space_l", text = "Free").space = 'Free'
    col.operator("switch.fing_lit_space_l", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Lit_Space_List_L(bpy.types.Operator):
    bl_idname = "show.fing_lit_list_l"
    bl_label = "Little Finger_L Space Switch List"
    bl_description = "Switch Little Finger_L Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Lit_Space_List_L, title='Switch Little Finger_L Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Leg_L IK>FK #####

class Operator_Snap_LegIKtoFK_L(bpy.types.Operator):

    bl_idname = "snap.leg_ik_to_fk_l"
    bl_label = "BlenRig Leg_L IK to FK"
    bl_description = "Switch Leg to FK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if bpy.context.active_object.pose.bones["properties_leg_L"].ik_leg_L < 0.1:

            #Collect Matrix
            ThighFkMat = pbones['thigh_fk_L'].matrix.copy()
            ThighFkLoc = pbones['thigh_fk_L'].location.copy()
            ThighFkScale = pbones['thigh_fk_L'].scale.copy()
            ShinFkMat = pbones['shin_fk_L'].matrix.copy()
            ShinFkLoc = pbones['shin_fk_L'].location.copy()
            ShinFkScale = pbones['shin_fk_L'].scale.copy()
            FootFkMat = pbones['foot_fk_L'].matrix.copy()
            FootFkLoc = pbones['foot_fk_L'].location.copy()
            FootFkScale = pbones['foot_fk_L'].scale.copy()
            FootToe1FkMat = pbones['foot_toe_1_fk_L'].matrix.copy()
            FootToe1FkLoc = pbones['foot_toe_1_fk_L'].location.copy()
            FootToe1FkScale = pbones['foot_toe_1_fk_L'].scale.copy()
            FootToe2FkMat = pbones['foot_toe_2_fk_L'].matrix.copy()
            FootToe2FkLoc = pbones['foot_toe_2_fk_L'].location.copy()
            FootToe2FkScale = pbones['foot_toe_2_fk_L'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_leg_L"].keyframe_insert(data_path='ik_leg_L')
                        insert_bkeys('thigh_fk_L', 'LocRotScale')
                        insert_bkeys('shin_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_ik_L', 'RotScale')
                        insert_bkeys('shin_ik_L', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_L', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_L', 'Rot')
                        insert_bkeys('toe_roll_1_L', 'Rot')
                        insert_bkeys('toe_roll_2_L', 'Rot')
                        insert_bkeys('sole_ctrl_L', 'Rot')
                        if pbones["properties_leg_L"].toggle_leg_ik_pole_L == 1.0:
                            insert_bkeys('knee_pole_L', 'Loc')

            bpy.context.active_object.pose.bones["properties_leg_L"].ik_leg_L = 1.0
            refresh_hack()

            #Paste Matrix
            pVisRotExec (pbones['thigh_fk_ctrl_L'], pbones['thigh_ik_L'])
            pbones['thigh_fk_ctrl_L'].scale[:] = (1.0, 1.0, 1.0)
            refresh_hack()
            pbones['thigh_fk_L'].matrix = ThighFkMat
            pbones['thigh_fk_L'].location = ThighFkLoc
            pbones['thigh_fk_L'].scale = ThighFkScale
            refresh_hack()
            pbones['shin_fk_L'].matrix = ShinFkMat
            pbones['shin_fk_L'].location = ShinFkLoc
            pbones['shin_fk_L'].scale = ShinFkScale
            refresh_hack()
            pbones['foot_fk_L'].matrix = FootFkMat
            pbones['foot_fk_L'].location = FootFkLoc
            pbones['foot_fk_L'].scale = FootFkScale
            refresh_hack()
            pbones['foot_toe_1_fk_L'].matrix = FootToe1FkMat
            pbones['foot_toe_1_fk_L'].location = FootToe1FkLoc
            pbones['foot_toe_1_fk_L'].scale = FootToe1FkScale
            refresh_hack()
            pbones['foot_toe_2_fk_L'].matrix = FootToe2FkMat
            pbones['foot_toe_2_fk_L'].location = FootToe2FkLoc
            pbones['foot_toe_2_fk_L'].scale = FootToe2FkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms

                        ThighCtrlRotEuler = pbones['thigh_fk_ctrl_L'].rotation_euler.copy()
                        ThighCtrlRotQuat = pbones['thigh_fk_ctrl_L'].rotation_quaternion.copy()
                        ThighCtrlLoc = pbones['thigh_fk_ctrl_L'].location.copy()
                        ThighCtrlScale = pbones['thigh_fk_ctrl_L'].scale.copy()

                        ThighFkRotEuler = pbones['thigh_fk_L'].rotation_euler.copy()
                        ThighFkRotQuat = pbones['thigh_fk_L'].rotation_quaternion.copy()
                        ThighFkLoc = pbones['thigh_fk_L'].location.copy()
                        ThighFkScale = pbones['thigh_fk_L'].scale.copy()

                        ShinFkRotEuler = pbones['shin_fk_L'].rotation_euler.copy()
                        ShinFkRotQuat = pbones['shin_fk_L'].rotation_quaternion.copy()
                        ShinFkLoc = pbones['shin_fk_L'].location.copy()
                        ShinFkScale = pbones['shin_fk_L'].scale.copy()

                        FootFkRotEuler = pbones['foot_fk_L'].rotation_euler.copy()
                        FootFkRotQuat = pbones['foot_fk_L'].rotation_quaternion.copy()
                        FootFkLoc = pbones['foot_fk_L'].location.copy()
                        FootFkScale = pbones['foot_fk_L'].scale.copy()

                        FootToe1FkRotEuler = pbones['foot_toe_1_fk_L'].rotation_euler.copy()
                        FootToe1FkRotQuat = pbones['foot_toe_1_fk_L'].rotation_quaternion.copy()
                        FootToe1FkLoc = pbones['foot_toe_1_fk_L'].location.copy()
                        FootToe1FkScale = pbones['foot_toe_1_fk_L'].scale.copy()

                        FootToe2FkRotEuler = pbones['foot_toe_2_fk_L'].rotation_euler.copy()
                        FootToe2FkRotQuat = pbones['foot_toe_2_fk_L'].rotation_quaternion.copy()
                        FootToe2FkLoc = pbones['foot_toe_2_fk_L'].location.copy()
                        FootToe2FkScale = pbones['foot_toe_2_fk_L'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_leg_L"].ik_leg_L = 1.0
                        refresh_hack()
                        pbones["properties_leg_L"].keyframe_insert(data_path='ik_leg_L')

                        #Re-Paste Transforms
                        pbones['thigh_fk_ctrl_L'].rotation_euler = ThighCtrlRotEuler
                        pbones['thigh_fk_ctrl_L'].rotation_quaternion = ThighCtrlRotQuat
                        pbones['thigh_fk_ctrl_L'].location = ThighCtrlLoc
                        pbones['thigh_fk_ctrl_L'].scale = ThighCtrlScale
                        refresh_hack()
                        pbones['thigh_fk_L'].rotation_euler = ThighFkRotEuler
                        pbones['thigh_fk_L'].rotation_quaternion = ThighFkRotQuat
                        pbones['thigh_fk_L'].location = ThighFkLoc
                        pbones['thigh_fk_L'].scale = ThighFkScale
                        refresh_hack()
                        pbones['shin_fk_L'].rotation_euler = ShinFkRotEuler
                        pbones['shin_fk_L'].rotation_quaternion = ShinFkRotQuat
                        pbones['shin_fk_L'].location = ShinFkLoc
                        pbones['shin_fk_L'].scale = ShinFkScale
                        refresh_hack()
                        pbones['foot_fk_L'].rotation_euler = FootFkRotEuler
                        pbones['foot_fk_L'].rotation_quaternion = FootFkRotQuat
                        pbones['foot_fk_L'].location = FootFkLoc
                        pbones['foot_fk_L'].scale = FootFkScale
                        refresh_hack()
                        pbones['foot_toe_1_fk_L'].rotation_euler = FootToe1FkRotEuler
                        pbones['foot_toe_1_fk_L'].rotation_quaternion = FootToe1FkRotQuat
                        pbones['foot_toe_1_fk_L'].location = FootToe1FkLoc
                        pbones['foot_toe_1_fk_L'].scale = FootToe1FkScale
                        refresh_hack()
                        pbones['foot_toe_2_fk_L'].rotation_euler = FootToe2FkRotEuler
                        pbones['foot_toe_2_fk_L'].rotation_quaternion = FootToe2FkRotQuat
                        pbones['foot_toe_2_fk_L'].location = FootToe2FkLoc
                        pbones['foot_toe_2_fk_L'].scale = FootToe2FkScale
                        refresh_hack()

                        insert_bkeys('thigh_fk_L', 'LocRotScale')
                        insert_bkeys('shin_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_ik_L', 'RotScale')
                        insert_bkeys('shin_ik_L', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_L', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_L', 'Rot')
                        insert_bkeys('toe_roll_1_L', 'Rot')
                        insert_bkeys('toe_roll_2_L', 'Rot')
                        insert_bkeys('sole_ctrl_L', 'Rot')
                        if pbones["properties_leg_L"].toggle_leg_ik_pole_L == 1.0:
                            insert_bkeys('knee_pole_L', 'Loc')

        return {"FINISHED"}

##### Leg_L FK>IK #####

class Operator_Snap_LegFKtoIK_L(bpy.types.Operator):

    bl_idname = "snap.leg_fk_to_ik_l"
    bl_label = "BlenRig Leg_L IK to FK"
    bl_description = "Switch Leg to IK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if bpy.context.active_object.pose.bones["properties_leg_L"].ik_leg_L > 0.9:

            #Collect Matrix
            ThighFkMat = pbones['thigh_fk_L'].matrix.copy()
            ThighFkLoc = pbones['thigh_fk_L'].location.copy()
            ThighFkScale = pbones['thigh_fk_L'].scale.copy()
            ShinFkMat = pbones['shin_fk_L'].matrix.copy()
            ShinFkLoc = pbones['shin_fk_L'].location.copy()
            ShinFkScale = pbones['shin_fk_L'].scale.copy()
            FootToe1FkMat = pbones['foot_toe_1_fk_L'].matrix.copy()
            FootToe1FkLoc = pbones['foot_toe_1_fk_L'].location.copy()
            FootToe1FkScale = pbones['foot_toe_1_fk_L'].scale.copy()
            FootToe2FkMat = pbones['foot_toe_2_fk_L'].matrix.copy()
            FootToe2FkLoc = pbones['foot_toe_2_fk_L'].location.copy()
            FootToe2FkScale = pbones['foot_toe_2_fk_L'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_leg_L"].keyframe_insert(data_path='ik_leg_L')
                        insert_bkeys('thigh_fk_L', 'LocRotScale')
                        insert_bkeys('shin_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_ik_L', 'RotScale')
                        insert_bkeys('shin_ik_L', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_L', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_L', 'Rot')
                        insert_bkeys('toe_roll_1_L', 'Rot')
                        insert_bkeys('toe_roll_2_L', 'Rot')
                        insert_bkeys('sole_ctrl_L', 'Rot')
                        if pbones["properties_leg_L"].toggle_leg_ik_pole_L == 1.0:
                            insert_bkeys('knee_pole_L', 'Loc')

            #Paste Matrix
            pVisLocExec(pbones['sole_ctrl_L'], pbones['snap_sole_ctrl_fk_L'])
            pVisRotExec(pbones['sole_ctrl_L'], pbones['snap_sole_ctrl_fk_L'])
            refresh_hack()
            pbones['foot_roll_ctrl_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['foot_ik_ctrl_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['foot_ik_ctrl_L'].location[:] = (0.0, 0.0, 0.0)
            pbones['toe_roll_1_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['toe_roll_2_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['foot_toe_ik_ctrl_mid_L'].location[:] = (0.0, 0.0, 0.0)
            pbones['foot_toe_ik_ctrl_mid_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['toes_ik_ctrl_L'].location[:] = (0.0, 0.0, 0.0)
            pbones['toes_ik_ctrl_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pVisLocExec(pbones['knee_pole_L'], pbones['snap_knee_fk_L'])
            refresh_hack()

            bpy.context.active_object.pose.bones["properties_leg_L"].ik_leg_L = 0.0
            refresh_hack()

            pVisRotExec (pbones['thigh_ik_L'], pbones['thigh_fk_ctrl_L'])
            refresh_hack()
            pbones['thigh_fk_L'].matrix = ThighFkMat
            pbones['thigh_fk_L'].location = ThighFkLoc
            pbones['thigh_fk_L'].scale = ThighFkScale
            refresh_hack()
            pbones['shin_fk_L'].matrix = ShinFkMat
            pbones['shin_fk_L'].location = ShinFkLoc
            pbones['shin_fk_L'].scale = ShinFkScale
            refresh_hack()
            pbones['foot_toe_1_fk_L'].matrix = FootToe1FkMat
            pbones['foot_toe_1_fk_L'].location = FootToe1FkLoc
            pbones['foot_toe_1_fk_L'].scale = FootToe1FkScale
            refresh_hack()
            pbones['foot_toe_2_fk_L'].matrix = FootToe2FkMat
            pbones['foot_toe_2_fk_L'].location = FootToe2FkLoc
            pbones['foot_toe_2_fk_L'].scale = FootToe2FkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms

                        SoleCtrlRotEuler = pbones['sole_ctrl_L'].rotation_euler.copy()
                        SoleCtrlRotQuat = pbones['sole_ctrl_L'].rotation_quaternion.copy()
                        SoleCtrlLoc = pbones['sole_ctrl_L'].location.copy()
                        SoleCtrlScale = pbones['sole_ctrl_L'].scale.copy()

                        KneePoleRotEuler = pbones['knee_pole_L'].rotation_euler.copy()
                        KneePoleRotQuat = pbones['knee_pole_L'].rotation_quaternion.copy()
                        KneePoleLoc = pbones['knee_pole_L'].location.copy()
                        KneePoleScale = pbones['knee_pole_L'].scale.copy()

                        ThighIkRotEuler = pbones['thigh_ik_L'].rotation_euler.copy()
                        ThighIkRotQuat = pbones['thigh_ik_L'].rotation_quaternion.copy()
                        ThighIkLoc = pbones['thigh_ik_L'].location.copy()
                        ThighIkScale = pbones['thigh_ik_L'].scale.copy()

                        ThighFkRotEuler = pbones['thigh_fk_L'].rotation_euler.copy()
                        ThighFkRotQuat = pbones['thigh_fk_L'].rotation_quaternion.copy()
                        ThighFkLoc = pbones['thigh_fk_L'].location.copy()
                        ThighFkScale = pbones['thigh_fk_L'].scale.copy()

                        ShinFkRotEuler = pbones['shin_fk_L'].rotation_euler.copy()
                        ShinFkRotQuat = pbones['shin_fk_L'].rotation_quaternion.copy()
                        ShinFkLoc = pbones['shin_fk_L'].location.copy()
                        ShinFkScale = pbones['shin_fk_L'].scale.copy()

                        FootToe1FkRotEuler = pbones['foot_toe_1_fk_L'].rotation_euler.copy()
                        FootToe1FkRotQuat = pbones['foot_toe_1_fk_L'].rotation_quaternion.copy()
                        FootToe1FkLoc = pbones['foot_toe_1_fk_L'].location.copy()
                        FootToe1FkScale = pbones['foot_toe_1_fk_L'].scale.copy()

                        FootToe2FkRotEuler = pbones['foot_toe_2_fk_L'].rotation_euler.copy()
                        FootToe2FkRotQuat = pbones['foot_toe_2_fk_L'].rotation_quaternion.copy()
                        FootToe2FkLoc = pbones['foot_toe_2_fk_L'].location.copy()
                        FootToe2FkScale = pbones['foot_toe_2_fk_L'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_leg_L"].ik_leg_L = 0.0
                        refresh_hack()
                        pbones["properties_leg_L"].keyframe_insert(data_path='ik_leg_L')

                        #Re-Paste Transforms
                        pbones['sole_ctrl_L'].rotation_euler = SoleCtrlRotEuler
                        pbones['sole_ctrl_L'].rotation_quaternion = SoleCtrlRotQuat
                        pbones['sole_ctrl_L'].location = SoleCtrlLoc
                        pbones['sole_ctrl_L'].scale = SoleCtrlScale
                        refresh_hack()
                        pbones['knee_pole_L'].rotation_euler = KneePoleRotEuler
                        pbones['knee_pole_L'].rotation_quaternion = KneePoleRotQuat
                        pbones['knee_pole_L'].location = KneePoleLoc
                        pbones['knee_pole_L'].scale = KneePoleScale
                        refresh_hack()
                        pbones['thigh_ik_L'].rotation_euler = ThighIkRotEuler
                        pbones['thigh_ik_L'].rotation_quaternion = ThighIkRotQuat
                        pbones['thigh_ik_L'].location = ThighIkLoc
                        pbones['thigh_ik_L'].scale = ThighIkScale
                        refresh_hack()
                        pbones['thigh_fk_L'].rotation_euler = ThighFkRotEuler
                        pbones['thigh_fk_L'].rotation_quaternion = ThighFkRotQuat
                        pbones['thigh_fk_L'].location = ThighFkLoc
                        pbones['thigh_fk_L'].scale = ThighFkScale
                        refresh_hack()
                        pbones['shin_fk_L'].rotation_euler = ShinFkRotEuler
                        pbones['shin_fk_L'].rotation_quaternion = ShinFkRotQuat
                        pbones['shin_fk_L'].location = ShinFkLoc
                        pbones['shin_fk_L'].scale = ShinFkScale
                        refresh_hack()
                        pbones['foot_toe_1_fk_L'].rotation_euler = FootToe1FkRotEuler
                        pbones['foot_toe_1_fk_L'].rotation_quaternion = FootToe1FkRotQuat
                        pbones['foot_toe_1_fk_L'].location = FootToe1FkLoc
                        pbones['foot_toe_1_fk_L'].scale = FootToe1FkScale
                        refresh_hack()
                        pbones['foot_toe_2_fk_L'].rotation_euler = FootToe2FkRotEuler
                        pbones['foot_toe_2_fk_L'].rotation_quaternion = FootToe2FkRotQuat
                        pbones['foot_toe_2_fk_L'].location = FootToe2FkLoc
                        pbones['foot_toe_2_fk_L'].scale = FootToe2FkScale
                        refresh_hack()
                        pbones['foot_roll_ctrl_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['foot_ik_ctrl_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['foot_ik_ctrl_L'].location[:] = (0.0, 0.0, 0.0)
                        pbones['toe_roll_1_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['toe_roll_2_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['foot_toe_ik_ctrl_mid_L'].location[:] = (0.0, 0.0, 0.0)
                        pbones['foot_toe_ik_ctrl_mid_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['toes_ik_ctrl_L'].location[:] = (0.0, 0.0, 0.0)
                        pbones['toes_ik_ctrl_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        refresh_hack()

                        insert_bkeys('thigh_fk_L', 'LocRotScale')
                        insert_bkeys('shin_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_L', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_L', 'LocRotScale')
                        insert_bkeys('thigh_ik_L', 'RotScale')
                        insert_bkeys('shin_ik_L', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_L', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_L', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_L', 'Rot')
                        insert_bkeys('toe_roll_1_L', 'Rot')
                        insert_bkeys('toe_roll_2_L', 'Rot')
                        insert_bkeys('sole_ctrl_L', 'Rot')
                        if pbones["properties_leg_L"].toggle_leg_ik_pole_L == 1.0:
                            insert_bkeys('knee_pole_L', 'Loc')

        return {"FINISHED"}

##### Leg_L Space #####

class Operator_Switch_Leg_Space_L(bpy.types.Operator):

    bl_idname = "switch.leg_space_l"
    bl_label = "BlenRig Switch Leg_L FK Space"
    bl_description = "Switch Leg_L FK Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        ThighFkCtrlMat = pbones['thigh_fk_ctrl_L'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_leg_L"].keyframe_insert(data_path='space_leg_L')
                    insert_bkeys('thigh_fk_ctrl_L', 'RotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_L = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_L = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['thigh_fk_ctrl_L'].matrix = ThighFkCtrlMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    ThighFkCtrlRotEuler = pbones['thigh_fk_ctrl_L'].rotation_euler.copy()
                    ThighFkCtrlRotQuat = pbones['thigh_fk_ctrl_L'].rotation_quaternion.copy()
                    ThighFkCtrlScale = pbones['thigh_fk_ctrl_L'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_L = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_L = 1.0
                        refresh_hack()
                    pbones["properties_leg_L"].keyframe_insert(data_path='space_leg_L')

                    #Re-Paste Transforms
                    pbones['thigh_fk_ctrl_L'].rotation_euler = ThighFkCtrlRotEuler
                    pbones['thigh_fk_ctrl_L'].rotation_quaternion = ThighFkCtrlRotQuat
                    pbones['thigh_fk_ctrl_L'].scale = ThighFkCtrlScale
                    refresh_hack()

                    insert_bkeys('thigh_fk_ctrl_L', 'RotScale')

        return {"FINISHED"}

#Create Space PopUp
def Leg_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.leg_space_l", text = "Free").space = 'Free'
    col.operator("switch.leg_space_l", text = "Torso").space = 'Torso'

class Operator_Show_Leg_Space_List_L(bpy.types.Operator):
    bl_idname = "show.leg_list_l"
    bl_label = "Leg_L FK Space Switch List"
    bl_description = "Switch Leg_L FK Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Leg_Space_List_L, title='Switch Leg_L FK Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Leg_Pole_L Space #####

class Operator_Switch_Leg_Pole_Space_L(bpy.types.Operator):

    bl_idname = "switch.leg_pole_space_l"
    bl_label = "BlenRig Switch Leg_L Pole Space"
    bl_description = "Switch Leg_L Pole Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_leg_L"].keyframe_insert(data_path='space_leg_ik_pole_L')
                    insert_bkeys('knee_pole_L', 'Loc')

        #Collect Matrix
        PoleMat = pbones['knee_pole_L'].matrix.copy()

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_ik_pole_L = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_ik_pole_L = 1.0
            refresh_hack()
        if self.space == 'Foot':
            bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_ik_pole_L = 2.0
            refresh_hack()

        #Paste Matrix
        pbones['knee_pole_L'].matrix = PoleMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    KneePoleLoc = pbones['knee_pole_L'].location.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_ik_pole_L = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_ik_pole_L = 1.0
                        refresh_hack()
                    if self.space == 'Foot':
                        bpy.context.active_object.pose.bones["properties_leg_L"].space_leg_ik_pole_L = 2.0
                        refresh_hack()
                    pbones["properties_leg_L"].keyframe_insert(data_path='space_leg_ik_pole_L')

                    #Re-Paste Transforms
                    pbones['knee_pole_L'].location = KneePoleLoc
                    refresh_hack()

                    insert_bkeys('knee_pole_L', 'Loc')

        return {"FINISHED"}

#Create Space PopUp
def Leg_Pole_Space_List_L(self, context):
    col = self.layout.column()
    col.operator("switch.leg_pole_space_l", text = "Free").space = 'Free'
    col.operator("switch.leg_pole_space_l", text = "Torso").space = 'Torso'
    col.operator("switch.leg_pole_space_l", text = "Foot").space = 'Foot'

class Operator_Show_Leg_Pole_Space_List_L(bpy.types.Operator):
    bl_idname = "show.leg_pole_list_l"
    bl_label = "Leg_L Pole Space Switch List"
    bl_description = "Switch Leg_L Pole Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Leg_Pole_Space_List_L, title='Switch Leg_L Pole Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Right Ops #####

##### Arm_R IK>FK #####

class Operator_Snap_ArmIKtoFK_R(bpy.types.Operator):

    bl_idname = "snap.arm_ik_to_fk_r"
    bl_label = "BlenRig Arm_R IK to FK"
    bl_description = "Switch Arm to FK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if armobj.pose.bones["properties_arm_R"].ik_arm_R < 0.1:

            #Collect Matrix
            ArmFkMat = pbones['arm_fk_R'].matrix.copy()
            ArmFkLoc = pbones['arm_fk_R'].location.copy()
            ArmFkScale = pbones['arm_fk_R'].scale.copy()
            ForearmFkMat = pbones['forearm_fk_R'].matrix.copy()
            ForearmFkLoc = pbones['forearm_fk_R'].location.copy()
            ForearmFkScale = pbones['forearm_fk_R'].scale.copy()
            ShoulderMat = pbones['shoulder_R'].matrix.copy()
            ShoulderLoc = pbones['shoulder_R'].location.copy()
            ShoulderScale = pbones['shoulder_R'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='ik_arm_R')
                        insert_bkeys('arm_fk_R', 'LocRotScale')
                        insert_bkeys('forearm_fk_R', 'LocRotScale')
                        insert_bkeys('arm_ik_R', 'RotScale')
                        insert_bkeys('forearm_ik_R', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('shoulder_R', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('hand_fk_R', 'LocRotScale')
                        if pbones["properties_arm_R"].toggle_arm_ik_pole_R == 1.0:
                            insert_bkeys('elbow_pole_R', 'Loc')

            armobj.pose.bones["properties_arm_R"].ik_arm_R = 1.0
            refresh_hack()

            #Paste Matrix
            pVisRotExec (pbones['arm_fk_ctrl_R'], pbones['arm_ik_R'])
            pbones['arm_fk_ctrl_R'].scale[:] = (1.0, 1.0, 1.0)
            refresh_hack()
            pbones['shoulder_R'].matrix = ShoulderMat
            pbones['shoulder_R'].location = ShoulderLoc
            pbones['shoulder_R'].scale = ShoulderScale
            refresh_hack()
            pbones['arm_fk_R'].matrix = ArmFkMat
            pbones['arm_fk_R'].location = ArmFkLoc
            pbones['arm_fk_R'].scale = ArmFkScale
            refresh_hack()
            pbones['forearm_fk_R'].matrix = ForearmFkMat
            pbones['forearm_fk_R'].location = ForearmFkLoc
            pbones['forearm_fk_R'].scale = ForearmFkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        ShoulderRotEuler = pbones['shoulder_R'].rotation_euler.copy()
                        ShoulderRotQuat = pbones['shoulder_R'].rotation_quaternion.copy()
                        ShoulderLoc = pbones['shoulder_R'].location.copy()
                        ShoulderScale = pbones['shoulder_R'].scale.copy()

                        ArmCtrlRotEuler = pbones['arm_fk_ctrl_R'].rotation_euler.copy()
                        ArmCtrlRotQuat = pbones['arm_fk_ctrl_R'].rotation_quaternion.copy()
                        ArmCtrlLoc = pbones['arm_fk_ctrl_R'].location.copy()
                        ArmCtrlScale = pbones['arm_fk_ctrl_R'].scale.copy()

                        ArmFkRotEuler = pbones['arm_fk_R'].rotation_euler.copy()
                        ArmFkRotQuat = pbones['arm_fk_R'].rotation_quaternion.copy()
                        ArmFkLoc = pbones['arm_fk_R'].location.copy()
                        ArmFkScale = pbones['arm_fk_R'].scale.copy()

                        ForearmFkRotEuler = pbones['forearm_fk_R'].rotation_euler.copy()
                        ForearmFkRotQuat = pbones['forearm_fk_R'].rotation_quaternion.copy()
                        ForearmFkLoc = pbones['forearm_fk_R'].location.copy()
                        ForearmFkScale = pbones['forearm_fk_R'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_arm_R"].ik_arm_R = 1.0
                        refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='ik_arm_R')

                        #Re-Paste Transforms
                        pbones['shoulder_R'].rotation_euler = ShoulderRotEuler
                        pbones['shoulder_R'].rotation_quaternion = ShoulderRotQuat
                        pbones['shoulder_R'].location = ShoulderLoc
                        pbones['shoulder_R'].scale = ShoulderScale
                        refresh_hack()
                        pbones['arm_fk_ctrl_R'].rotation_euler = ArmCtrlRotEuler
                        pbones['arm_fk_ctrl_R'].rotation_quaternion = ArmCtrlRotQuat
                        pbones['arm_fk_ctrl_R'].location = ArmCtrlLoc
                        pbones['arm_fk_ctrl_R'].scale = ArmCtrlScale
                        refresh_hack()
                        pbones['arm_fk_R'].rotation_euler = ArmFkRotEuler
                        pbones['arm_fk_R'].rotation_quaternion = ArmFkRotQuat
                        pbones['arm_fk_R'].location = ArmFkLoc
                        pbones['arm_fk_R'].scale = ArmFkScale
                        refresh_hack()
                        pbones['forearm_fk_R'].rotation_euler = ForearmFkRotEuler
                        pbones['forearm_fk_R'].rotation_quaternion = ForearmFkRotQuat
                        pbones['forearm_fk_R'].location = ForearmFkLoc
                        pbones['forearm_fk_R'].scale = ForearmFkScale
                        refresh_hack()

                        insert_bkeys('arm_fk_R', 'LocRotScale')
                        insert_bkeys('forearm_fk_R', 'LocRotScale')
                        insert_bkeys('arm_ik_R', 'RotScale')
                        insert_bkeys('forearm_ik_R', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('shoulder_R', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('hand_fk_R', 'LocRotScale')
                        if pbones["properties_arm_R"].toggle_arm_ik_pole_R == 1.0:
                            insert_bkeys('elbow_pole_R', 'Loc')

            #Switch Hand to Arm Space
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)

            #Switch Hand to Arm Space
            bpy.ops.switch.hand_space_r(space='Arm')

        return {"FINISHED"}



##### Arm_R FK>IK #####

class Operator_Snap_ArmFKtoIK_R(bpy.types.Operator):

    bl_idname = "snap.arm_fk_to_ik_r"
    bl_label = "BlenRig Arm_R FK to IK"
    bl_description = "Switch Arm to IK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if bpy.context.active_object.pose.bones["properties_arm_R"].ik_arm_R > 0.9:
            #Collect Matrix
            ArmFkMat = pbones['arm_fk_R'].matrix.copy()
            ArmFkLoc = pbones['arm_fk_R'].location.copy()
            ArmFkScale = pbones['arm_fk_R'].scale.copy()
            ForearmFkMat = pbones['forearm_fk_R'].matrix.copy()
            ForearmFkLoc = pbones['forearm_fk_R'].location.copy()
            ForearmFkScale = pbones['forearm_fk_R'].scale.copy()
            ArmFkCtrlMat = pbones['arm_fk_ctrl_R'].matrix.copy()
            ShoulderMat = pbones['shoulder_R'].matrix.copy()
            ShoulderLoc = pbones['shoulder_R'].location.copy()
            ShoulderScale = pbones['shoulder_R'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='ik_arm_R')
                        insert_bkeys('arm_fk_R', 'LocRotScale')
                        insert_bkeys('forearm_fk_R', 'LocRotScale')
                        insert_bkeys('arm_ik_R', 'RotScale')
                        insert_bkeys('forearm_ik_R', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('shoulder_R', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('hand_fk_R', 'LocRotScale')
                        if pbones["properties_arm_R"].toggle_arm_ik_pole_R == 1.0:
                            insert_bkeys('elbow_pole_R', 'Loc')

            #Paste Matrix
            pVisLocExec(pbones['hand_ik_ctrl_R'], pbones['hand_fk_R'])
            refresh_hack()
            pVisLocExec(pbones['elbow_pole_R'], pbones['snap_elbow_pole_fk_R'])
            refresh_hack()

            bpy.context.active_object.pose.bones["properties_arm_R"].ik_arm_R = 0.0
            refresh_hack()

            pVisRotExec (pbones['arm_ik_R'], pbones['arm_fk_ctrl_R'])
            refresh_hack()
            pbones['shoulder_R'].matrix = ShoulderMat
            pbones['shoulder_R'].location = ShoulderLoc
            pbones['shoulder_R'].scale = ShoulderScale
            refresh_hack()
            pbones['arm_fk_R'].matrix = ArmFkMat
            pbones['arm_fk_R'].location = ArmFkLoc
            pbones['arm_fk_R'].scale = ArmFkScale
            refresh_hack()
            pbones['forearm_fk_R'].matrix = ForearmFkMat
            pbones['forearm_fk_R'].location = ForearmFkLoc
            pbones['forearm_fk_R'].scale = ForearmFkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        HandIkCtrlRotEuler = pbones['hand_ik_ctrl_R'].rotation_euler.copy()
                        HandIkCtrlRotQuat = pbones['hand_ik_ctrl_R'].rotation_quaternion.copy()
                        HandIkCtrlLoc = pbones['hand_ik_ctrl_R'].location.copy()
                        HandIkCtrlScale = pbones['hand_ik_ctrl_R'].scale.copy()

                        ArmIkRotEuler = pbones['arm_ik_R'].rotation_euler.copy()
                        ArmIkRotQuat = pbones['arm_ik_R'].rotation_quaternion.copy()
                        ArmIkLoc = pbones['arm_ik_R'].location.copy()
                        ArmIkScale = pbones['arm_ik_R'].scale.copy()

                        ElbowlLoc = pbones['elbow_pole_R'].location.copy()

                        ShoulderRotEuler = pbones['shoulder_R'].rotation_euler.copy()
                        ShoulderRotQuat = pbones['shoulder_R'].rotation_quaternion.copy()
                        ShoulderLoc = pbones['shoulder_R'].location.copy()
                        ShoulderScale = pbones['shoulder_R'].scale.copy()

                        ArmFkRotEuler = pbones['arm_fk_R'].rotation_euler.copy()
                        ArmFkRotQuat = pbones['arm_fk_R'].rotation_quaternion.copy()
                        ArmFkLoc = pbones['arm_fk_R'].location.copy()
                        ArmFkScale = pbones['arm_fk_R'].scale.copy()

                        ForearmFkRotEuler = pbones['forearm_fk_R'].rotation_euler.copy()
                        ForearmFkRotQuat = pbones['forearm_fk_R'].rotation_quaternion.copy()
                        ForearmFkLoc = pbones['forearm_fk_R'].location.copy()
                        ForearmFkScale = pbones['forearm_fk_R'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_arm_R"].ik_arm_R = 0.0
                        refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='ik_arm_R')

                        #Re-Paste Transforms
                        pbones['hand_ik_ctrl_R'].rotation_euler = HandIkCtrlRotEuler
                        pbones['hand_ik_ctrl_R'].rotation_quaternion = HandIkCtrlRotQuat
                        pbones['hand_ik_ctrl_R'].location = HandIkCtrlLoc
                        pbones['hand_ik_ctrl_R'].scale = HandIkCtrlScale
                        refresh_hack()
                        pbones['elbow_pole_R'].location = ElbowlLoc
                        refresh_hack()
                        pbones['arm_ik_R'].rotation_euler = ArmIkRotEuler
                        pbones['arm_ik_R'].rotation_quaternion = ArmIkRotQuat
                        pbones['arm_ik_R'].location = ArmIkLoc
                        pbones['arm_ik_R'].scale = ArmIkScale
                        refresh_hack()
                        pbones['shoulder_R'].rotation_euler = ShoulderRotEuler
                        pbones['shoulder_R'].rotation_quaternion = ShoulderRotQuat
                        pbones['shoulder_R'].location = ShoulderLoc
                        pbones['shoulder_R'].scale = ShoulderScale
                        refresh_hack()
                        pbones['arm_fk_R'].rotation_euler = ArmFkRotEuler
                        pbones['arm_fk_R'].rotation_quaternion = ArmFkRotQuat
                        pbones['arm_fk_R'].location = ArmFkLoc
                        pbones['arm_fk_R'].scale = ArmFkScale
                        refresh_hack()
                        pbones['forearm_fk_R'].rotation_euler = ForearmFkRotEuler
                        pbones['forearm_fk_R'].rotation_quaternion = ForearmFkRotQuat
                        pbones['forearm_fk_R'].location = ForearmFkLoc
                        pbones['forearm_fk_R'].scale = ForearmFkScale
                        refresh_hack()

                        insert_bkeys('arm_fk_R', 'LocRotScale')
                        insert_bkeys('forearm_fk_R', 'LocRotScale')
                        insert_bkeys('arm_ik_R', 'RotScale')
                        insert_bkeys('forearm_ik_R', 'RotScale')
                        insert_bkeys('arm_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('shoulder_R', 'LocRotScale')
                        insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('hand_fk_R', 'LocRotScale')
                        if pbones["properties_arm_R"].toggle_arm_ik_pole_R == 1.0:
                            insert_bkeys('elbow_pole_R', 'Loc')

            #Switch Hand to Arm Space
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)

            #Switch Hand to Free Space
            bpy.ops.switch.hand_space_r(space='Free')

        return {"FINISHED"}

##### Arm_R Space #####

class Operator_Switch_Arm_Space_R(bpy.types.Operator):

    bl_idname = "switch.arm_space_r"
    bl_label = "BlenRig Switch Arm_R Space"
    bl_description = "Switch Arm_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        HandIkMat = pbones['hand_ik_ctrl_R'].matrix.copy()
        ArmFkCtrlMat = pbones['arm_fk_ctrl_R'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_R"].keyframe_insert(data_path='space_arm_R')
                    insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                    insert_bkeys('arm_fk_ctrl_R', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 0.0
            refresh_hack()
        if self.space == 'Pelvis':
            bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 1.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 2.0
            refresh_hack()
        if self.space == 'Head':
            bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 3.0
            refresh_hack()

        #Paste Matrix
        pbones['hand_ik_ctrl_R'].matrix = HandIkMat
        pbones['arm_fk_ctrl_R'].matrix = ArmFkCtrlMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HandIkCtrlRotEuler = pbones['hand_ik_ctrl_R'].rotation_euler.copy()
                    HandIkCtrlRotQuat = pbones['hand_ik_ctrl_R'].rotation_quaternion.copy()
                    HandIkCtrlLoc = pbones['hand_ik_ctrl_R'].location.copy()
                    HandIkCtrlScale = pbones['hand_ik_ctrl_R'].scale.copy()

                    ArmCtrlRotEuler = pbones['arm_fk_ctrl_R'].rotation_euler.copy()
                    ArmCtrlRotQuat = pbones['arm_fk_ctrl_R'].rotation_quaternion.copy()
                    ArmCtrlLoc = pbones['arm_fk_ctrl_R'].location.copy()
                    ArmCtrlScale = pbones['arm_fk_ctrl_R'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 0.0
                        refresh_hack()
                    if self.space == 'Pelvis':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 1.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 2.0
                        refresh_hack()
                    if self.space == 'Head':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_R = 3.0
                        refresh_hack()
                    pbones["properties_arm_R"].keyframe_insert(data_path='space_arm_R')

                    #Re-Paste Transforms
                    pbones['hand_ik_ctrl_R'].rotation_euler = HandIkCtrlRotEuler
                    pbones['hand_ik_ctrl_R'].rotation_quaternion = HandIkCtrlRotQuat
                    pbones['hand_ik_ctrl_R'].location = HandIkCtrlLoc
                    pbones['hand_ik_ctrl_R'].scale = HandIkCtrlScale
                    refresh_hack()
                    pbones['arm_fk_ctrl_R'].rotation_euler = ArmCtrlRotEuler
                    pbones['arm_fk_ctrl_R'].rotation_quaternion = ArmCtrlRotQuat
                    pbones['arm_fk_ctrl_R'].location = ArmCtrlLoc
                    pbones['arm_fk_ctrl_R'].scale = ArmCtrlScale
                    refresh_hack()

                    insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                    insert_bkeys('arm_fk_ctrl_R', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Arm_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.arm_space_r", text = "Free").space = 'Free'
    col.operator("switch.arm_space_r", text = "Pelvis").space = 'Pelvis'
    col.operator("switch.arm_space_r", text = "Torso").space = 'Torso'
    col.operator("switch.arm_space_r", text = "Head").space = 'Head'

class Operator_Show_Arm_Space_List_R(bpy.types.Operator):
    bl_idname = "show.arm_list_r"
    bl_label = "Arm_R Space Switch List"
    bl_description = "Switch Arm_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Arm_Space_List_R, title='Switch Arm_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Hand_R Space #####

class Operator_Switch_Hand_Space_R(bpy.types.Operator):

    bl_idname = "switch.hand_space_r"
    bl_label = "BlenRig Switch Hand_R Space"
    bl_description = "Switch Hand_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):
        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_R"].keyframe_insert(data_path='space_hand_R')
                    insert_bkeys('hand_ik_ctrl_R', 'RotScale')
                    insert_bkeys('hand_fk_R', 'RotScale')

        if self.space == 'Arm':
            #Collect Matrix
            HandFkMat = pbones['hand_fk_R'].matrix.copy()
            HandFkLoc = pbones['hand_fk_R'].location.copy()
            HandFkScale = pbones['hand_fk_R'].scale.copy()

            bpy.context.active_object.pose.bones["properties_arm_R"].space_hand_R = 1.0

            #Paste Matrix
            pbones['hand_fk_R'].matrix = HandFkMat
            pbones['hand_fk_R'].location = HandFkLoc
            pbones['hand_fk_R'].scale = HandFkScale
            refresh_hack()

        if self.space == 'Free':
            #Paste Matrix
            pVisRotExec (pbones['hand_ik_ctrl_R'], pbones['hand_fk_R'])
            refresh_hack()

            bpy.context.active_object.pose.bones["properties_arm_R"].space_hand_R = 0.0
            refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HandIkCtrlRotEuler = pbones['hand_ik_ctrl_R'].rotation_euler.copy()
                    HandIkCtrlRotQuat = pbones['hand_ik_ctrl_R'].rotation_quaternion.copy()
                    HandIkCtrlScale = pbones['hand_ik_ctrl_R'].scale.copy()

                    HandFkCtrlRotEuler = pbones['hand_fk_R'].rotation_euler.copy()
                    HandFkCtrlRotQuat = pbones['hand_fk_R'].rotation_quaternion.copy()
                    HandFkCtrlScale = pbones['hand_fk_R'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Arm':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_hand_R = 1.0
                        refresh_hack()
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_hand_R = 0.0
                        refresh_hack()
                    pbones["properties_arm_R"].keyframe_insert(data_path='space_hand_R')

                    #Re-Paste Transforms
                    pbones['hand_ik_ctrl_R'].rotation_euler = HandIkCtrlRotEuler
                    pbones['hand_ik_ctrl_R'].rotation_quaternion = HandIkCtrlRotQuat
                    pbones['hand_ik_ctrl_R'].scale = HandIkCtrlScale
                    refresh_hack()
                    pbones['hand_fk_R'].rotation_euler = HandFkCtrlRotEuler
                    pbones['hand_fk_R'].rotation_quaternion = HandFkCtrlRotQuat
                    pbones['hand_fk_R'].scale = HandFkCtrlScale
                    refresh_hack()

                    insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                    insert_bkeys('hand_fk_R', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Hand_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.hand_space_r", text = "Arm").space = 'Arm'
    col.operator("switch.hand_space_r", text = "Free").space = 'Free'

class Operator_Show_Hand_Space_List_R(bpy.types.Operator):
    bl_idname = "show.hand_list_r"
    bl_label = "Hand_R Space Switch List"
    bl_description = "Switch Hand_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Hand_Space_List_R, title='Switch Hand_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Arm_Pole_R Space #####

class Operator_Switch_Arm_Pole_Space_R(bpy.types.Operator):

    bl_idname = "switch.arm_pole_space_r"
    bl_label = "BlenRig Switch Arm_R Pole Space"
    bl_description = "Switch Arm_R Pole Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_R"].keyframe_insert(data_path='space_arm_ik_pole_R')
                    insert_bkeys('elbow_pole_R', 'Loc')

        #Collect Matrix
        PoleMat = pbones['elbow_pole_R'].matrix.copy()

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_ik_pole_R = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_ik_pole_R = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['elbow_pole_R'].matrix = PoleMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    PoleLoc = pbones['elbow_pole_R'].location.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_ik_pole_R = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_arm_R"].space_arm_ik_pole_R = 1.0
                        refresh_hack()
                    pbones["properties_arm_R"].keyframe_insert(data_path='space_arm_ik_pole_R')

                    #Re-Paste Transforms
                    pbones['elbow_pole_R'].location = PoleLoc
                    refresh_hack()

                    insert_bkeys('elbow_pole_R', 'Loc')

        return {"FINISHED"}

#Create Space PopUp
def Arm_Pole_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.arm_pole_space_r", text = "Free").space = 'Free'
    col.operator("switch.arm_pole_space_r", text = "Torso").space = 'Torso'

class Operator_Show_Arm_Pole_Space_List_R(bpy.types.Operator):
    bl_idname = "show.arm_pole_list_r"
    bl_label = "Arm_R Pole Space Switch List"
    bl_description = "Switch Arm_R Pole Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Arm_Pole_Space_List_R, title='Switch Arm_R Pole Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### All Fingers_R Space #####

class Operator_Switch_Fing_All_Space_R(bpy.types.Operator):

    bl_idname = "switch.fing_all_space_r"
    bl_label = "BlenRig Switch All Fingers_R Space"
    bl_description = "Switch All Fingers_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data

        if self.space == 'Free':
            bpy.ops.switch.fing_thumb_space_r(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ind_space_r(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_mid_space_r(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ring_space_r(space='Free')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_lit_space_r(space='Free')

            #Change Space
            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_all_R = 0.0

        if self.space == 'Hand':
            bpy.ops.switch.fing_thumb_space_r(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ind_space_r(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_mid_space_r(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_ring_space_r(space='Hand')
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Jump to previous Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current - 1)
            bpy.ops.switch.fing_lit_space_r(space='Hand')

            #Change Space
            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_all_R = 1.0

        return {"FINISHED"}

#Create Space PopUp
def Fing_All_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.fing_all_space_r", text = "Free").space = 'Free'
    col.operator("switch.fing_all_space_r", text = "Hand").space = 'Hand'

class Operator_Show_Fing_All_Space_List_R(bpy.types.Operator):
    bl_idname = "show.fing_all_list_r"
    bl_label = "All Fingers_R Space Switch List"
    bl_description = "Switch All Fingers_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_All_Space_List_R, title='Switch All Fingers_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Thumb Finger_R Space #####

class Operator_Switch_Fing_Thumb_Space_R(bpy.types.Operator):

    bl_idname = "switch.fing_thumb_space_r"
    bl_label = "BlenRig Switch Thumb Finger_R Space"
    bl_description = "Switch Thumb Finger_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_thumb_R')
                        insert_bkeys('fing_thumb_ik_R', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Thumb_world_mat = pbones['fing_thumb_ik_R'].id_data.matrix_world.copy()
                Thumb_mat = pbones['fing_thumb_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_thumb_R = 0.0

                paste_visual_matrix('fing_thumb_ik_R', 'master_pivot', Thumb_world_mat, Thumb_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Thumb_world_mat = pbones['fing_thumb_ik_R'].id_data.matrix_world.copy()
                Thumb_mat = pbones['fing_thumb_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_thumb_R = 1.0

                paste_visual_matrix('fing_thumb_ik_R', 'fing_thumb_ctrl_track_R', Thumb_world_mat, Thumb_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        ThumbLoc = pbones['fing_thumb_ik_R'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_thumb_R = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_thumb_R = 1.0
                            refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_thumb_R')

                        #Re-Paste Transforms
                        pbones['fing_thumb_ik_R'].location = ThumbLoc
                        refresh_hack()

                        insert_bkeys('fing_thumb_ik_R', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Thumb_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.fing_thumb_space_r", text = "Free").space = 'Free'
    col.operator("switch.fing_thumb_space_r", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Thumb_Space_List_R(bpy.types.Operator):
    bl_idname = "show.fing_thumb_list_r"
    bl_label = "Thumb Finger_R Space Switch List"
    bl_description = "Switch Thumb Finger_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Thumb_Space_List_R, title='Switch Thumb Finger_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Ind Finger_R Space #####

class Operator_Switch_Fing_Ind_Space_R(bpy.types.Operator):

    bl_idname = "switch.fing_ind_space_r"
    bl_label = "BlenRig Switch Index Finger_R Space"
    bl_description = "Switch Index Finger_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_ind_R')
                        insert_bkeys('fing_ind_ik_R', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Ind_world_mat = pbones['fing_ind_ik_R'].id_data.matrix_world.copy()
                Ind_mat = pbones['fing_ind_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ind_R = 0.0

                paste_visual_matrix('fing_ind_ik_R', 'master_pivot', Ind_world_mat, Ind_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Ind_world_mat = pbones['fing_ind_ik_R'].id_data.matrix_world.copy()
                Ind_mat = pbones['fing_ind_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ind_R = 1.0

                paste_visual_matrix('fing_ind_ik_R', 'fing_ind_ctrl_track_R', Ind_world_mat, Ind_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        IndLoc = pbones['fing_ind_ik_R'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ind_R = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ind_R = 1.0
                            refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_ind_R')

                        #Re-Paste Transforms
                        pbones['fing_ind_ik_R'].location = IndLoc
                        refresh_hack()

                        insert_bkeys('fing_ind_ik_R', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Ind_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.fing_ind_space_r", text = "Free").space = 'Free'
    col.operator("switch.fing_ind_space_r", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Ind_Space_List_R(bpy.types.Operator):
    bl_idname = "show.fing_ind_list_r"
    bl_label = "Index Finger_R Space Switch List"
    bl_description = "Switch Index Finger_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Ind_Space_List_R, title='Switch Index Finger_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Mid Finger_R Space #####

class Operator_Switch_Fing_Mid_Space_R(bpy.types.Operator):

    bl_idname = "switch.fing_mid_space_r"
    bl_label = "BlenRig Switch Middle Finger_R Space"
    bl_description = "Switch Middle Finger_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_mid_R')
                        insert_bkeys('fing_mid_ik_R', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Mid_world_mat = pbones['fing_mid_ik_R'].id_data.matrix_world.copy()
                Mid_mat = pbones['fing_mid_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_mid_R = 0.0

                paste_visual_matrix('fing_mid_ik_R', 'master_pivot', Mid_world_mat, Mid_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Mid_world_mat = pbones['fing_mid_ik_R'].id_data.matrix_world.copy()
                Mid_mat = pbones['fing_mid_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_mid_R = 1.0

                paste_visual_matrix('fing_mid_ik_R', 'fing_mid_ctrl_track_R', Mid_world_mat, Mid_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        MidLoc = pbones['fing_mid_ik_R'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_mid_R = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_mid_R = 1.0
                            refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_mid_R')

                        #Re-Paste Transforms
                        pbones['fing_mid_ik_R'].location = MidLoc
                        refresh_hack()

                        insert_bkeys('fing_mid_ik_R', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Mid_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.fing_mid_space_r", text = "Free").space = 'Free'
    col.operator("switch.fing_mid_space_r", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Mid_Space_List_R(bpy.types.Operator):
    bl_idname = "show.fing_mid_list_r"
    bl_label = "Middle Finger_R Space Switch List"
    bl_description = "Switch Middle Finger_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Mid_Space_List_R, title='Switch Middle Finger_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Ring Finger_R Space #####

class Operator_Switch_Fing_Ring_Space_R(bpy.types.Operator):

    bl_idname = "switch.fing_ring_space_r"
    bl_label = "BlenRig Switch Ring Finger_R Space"
    bl_description = "Switch Ring Finger_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_ring_R')
                        insert_bkeys('fing_ring_ik_R', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Ring_world_mat = pbones['fing_ring_ik_R'].id_data.matrix_world.copy()
                Ring_mat = pbones['fing_ring_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ring_R = 0.0

                paste_visual_matrix('fing_ring_ik_R', 'master_pivot', Ring_world_mat, Ring_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Ring_world_mat = pbones['fing_ring_ik_R'].id_data.matrix_world.copy()
                Ring_mat = pbones['fing_ring_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ring_R = 1.0

                paste_visual_matrix('fing_ring_ik_R', 'fing_ring_ctrl_track_R', Ring_world_mat, Ring_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        RingLoc = pbones['fing_ring_ik_R'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ring_R = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_ring_R = 1.0
                            refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_ring_R')

                        #Re-Paste Transforms
                        pbones['fing_ring_ik_R'].location = RingLoc
                        refresh_hack()

                        insert_bkeys('fing_ring_ik_R', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Ring_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.fing_ring_space_r", text = "Free").space = 'Free'
    col.operator("switch.fing_ring_space_r", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Ring_Space_List_R(bpy.types.Operator):
    bl_idname = "show.fing_ring_list_r"
    bl_label = "Ring Finger_R Space Switch List"
    bl_description = "Switch Ring Finger_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Ring_Space_List_R, title='Switch Ring Finger_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Lit Finger_R Space #####

class Operator_Switch_Fing_Lit_Space_R(bpy.types.Operator):

    bl_idname = "switch.fing_lit_space_r"
    bl_label = "BlenRig Switch Little Finger_R Space"
    bl_description = "Switch Little Finger_R Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        dbones = armobj.data.bones
        anim_data = armobj.animation_data
        try:
            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_lit_R')
                        insert_bkeys('fing_lit_ik_R', 'Loc')

            if self.space == 'Free':
                #Get Matrix in previous space
                Lit_world_mat = pbones['fing_lit_ik_R'].id_data.matrix_world.copy()
                Lit_mat = pbones['fing_lit_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_lit_R = 0.0

                paste_visual_matrix('fing_lit_ik_R', 'master_pivot', Lit_world_mat, Lit_mat, 'Location')

            if self.space == 'Hand':
                #Get Matrix in previous space
                Lit_world_mat = pbones['fing_lit_ik_R'].id_data.matrix_world.copy()
                Lit_mat = pbones['fing_lit_ik_R'].matrix.copy()

                #Change Space
                bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_lit_R = 1.0

                paste_visual_matrix('fing_lit_ik_R', 'fing_lit_ctrl_track_R', Lit_world_mat, Lit_mat, 'Location')

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms
                        LitLoc = pbones['fing_lit_ik_R'].location.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        if self.space == 'Free':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_lit_R = 0.0
                            refresh_hack()
                        if self.space == 'Hand':
                            bpy.context.active_object.pose.bones["properties_arm_R"].space_fing_lit_R = 1.0
                            refresh_hack()
                        pbones["properties_arm_R"].keyframe_insert(data_path='space_fing_lit_R')

                        #Re-Paste Transforms
                        pbones['fing_lit_ik_R'].location = LitLoc
                        refresh_hack()

                        insert_bkeys('fing_lit_ik_R', 'Loc')
        except:
            pass
        return {"FINISHED"}

#Create Space PopUp
def Fing_Lit_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.fing_lit_space_r", text = "Free").space = 'Free'
    col.operator("switch.fing_lit_space_r", text = "Hand").space = 'Hand'

class Operator_Show_Fing_Lit_Space_List_R(bpy.types.Operator):
    bl_idname = "show.fing_lit_list_r"
    bl_label = "Little Finger_R Space Switch List"
    bl_description = "Switch Little Finger_R Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Fing_Lit_Space_List_R, title='Switch Little Finger_R Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Leg_R IK>FK #####

class Operator_Snap_LegIKtoFK_R(bpy.types.Operator):

    bl_idname = "snap.leg_ik_to_fk_r"
    bl_label = "BlenRig Leg_R IK to FK"
    bl_description = "Switch Leg to FK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if bpy.context.active_object.pose.bones["properties_leg_R"].ik_leg_R < 0.1:

            #Collect Matrix
            ThighFkMat = pbones['thigh_fk_R'].matrix.copy()
            ThighFkLoc = pbones['thigh_fk_R'].location.copy()
            ThighFkScale = pbones['thigh_fk_R'].scale.copy()
            ShinFkMat = pbones['shin_fk_R'].matrix.copy()
            ShinFkLoc = pbones['shin_fk_R'].location.copy()
            ShinFkScale = pbones['shin_fk_R'].scale.copy()
            FootFkMat = pbones['foot_fk_R'].matrix.copy()
            FootFkLoc = pbones['foot_fk_R'].location.copy()
            FootFkScale = pbones['foot_fk_R'].scale.copy()
            FootToe1FkMat = pbones['foot_toe_1_fk_R'].matrix.copy()
            FootToe1FkLoc = pbones['foot_toe_1_fk_R'].location.copy()
            FootToe1FkScale = pbones['foot_toe_1_fk_R'].scale.copy()
            FootToe2FkMat = pbones['foot_toe_2_fk_R'].matrix.copy()
            FootToe2FkLoc = pbones['foot_toe_2_fk_R'].location.copy()
            FootToe2FkScale = pbones['foot_toe_2_fk_R'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_leg_R"].keyframe_insert(data_path='ik_leg_R')
                        insert_bkeys('thigh_fk_R', 'LocRotScale')
                        insert_bkeys('shin_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_ik_R', 'RotScale')
                        insert_bkeys('shin_ik_R', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_R', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_R', 'Rot')
                        insert_bkeys('toe_roll_1_R', 'Rot')
                        insert_bkeys('toe_roll_2_R', 'Rot')
                        insert_bkeys('sole_ctrl_R', 'Rot')
                        if pbones["properties_leg_R"].toggle_leg_ik_pole_R == 1.0:
                            insert_bkeys('knee_pole_R', 'Loc')

            bpy.context.active_object.pose.bones["properties_leg_R"].ik_leg_R = 1.0
            refresh_hack()

            #Paste Matrix
            pVisRotExec (pbones['thigh_fk_ctrl_R'], pbones['thigh_ik_R'])
            pbones['thigh_fk_ctrl_R'].scale[:] = (1.0, 1.0, 1.0)
            refresh_hack()
            pbones['thigh_fk_R'].matrix = ThighFkMat
            pbones['thigh_fk_R'].location = ThighFkLoc
            pbones['thigh_fk_R'].scale = ThighFkScale
            refresh_hack()
            pbones['shin_fk_R'].matrix = ShinFkMat
            pbones['shin_fk_R'].location = ShinFkLoc
            pbones['shin_fk_R'].scale = ShinFkScale
            refresh_hack()
            pbones['foot_fk_R'].matrix = FootFkMat
            pbones['foot_fk_R'].location = FootFkLoc
            pbones['foot_fk_R'].scale = FootFkScale
            refresh_hack()
            pbones['foot_toe_1_fk_R'].matrix = FootToe1FkMat
            pbones['foot_toe_1_fk_R'].location = FootToe1FkLoc
            pbones['foot_toe_1_fk_R'].scale = FootToe1FkScale
            refresh_hack()
            pbones['foot_toe_2_fk_R'].matrix = FootToe2FkMat
            pbones['foot_toe_2_fk_R'].location = FootToe2FkLoc
            pbones['foot_toe_2_fk_R'].scale = FootToe2FkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms

                        ThighCtrlRotEuler = pbones['thigh_fk_ctrl_R'].rotation_euler.copy()
                        ThighCtrlRotQuat = pbones['thigh_fk_ctrl_R'].rotation_quaternion.copy()
                        ThighCtrlLoc = pbones['thigh_fk_ctrl_R'].location.copy()
                        ThighCtrlScale = pbones['thigh_fk_ctrl_R'].scale.copy()

                        ThighFkRotEuler = pbones['thigh_fk_R'].rotation_euler.copy()
                        ThighFkRotQuat = pbones['thigh_fk_R'].rotation_quaternion.copy()
                        ThighFkLoc = pbones['thigh_fk_R'].location.copy()
                        ThighFkScale = pbones['thigh_fk_R'].scale.copy()

                        ShinFkRotEuler = pbones['shin_fk_R'].rotation_euler.copy()
                        ShinFkRotQuat = pbones['shin_fk_R'].rotation_quaternion.copy()
                        ShinFkLoc = pbones['shin_fk_R'].location.copy()
                        ShinFkScale = pbones['shin_fk_R'].scale.copy()

                        FootFkRotEuler = pbones['foot_fk_R'].rotation_euler.copy()
                        FootFkRotQuat = pbones['foot_fk_R'].rotation_quaternion.copy()
                        FootFkLoc = pbones['foot_fk_R'].location.copy()
                        FootFkScale = pbones['foot_fk_R'].scale.copy()

                        FootToe1FkRotEuler = pbones['foot_toe_1_fk_R'].rotation_euler.copy()
                        FootToe1FkRotQuat = pbones['foot_toe_1_fk_R'].rotation_quaternion.copy()
                        FootToe1FkLoc = pbones['foot_toe_1_fk_R'].location.copy()
                        FootToe1FkScale = pbones['foot_toe_1_fk_R'].scale.copy()

                        FootToe2FkRotEuler = pbones['foot_toe_2_fk_R'].rotation_euler.copy()
                        FootToe2FkRotQuat = pbones['foot_toe_2_fk_R'].rotation_quaternion.copy()
                        FootToe2FkLoc = pbones['foot_toe_2_fk_R'].location.copy()
                        FootToe2FkScale = pbones['foot_toe_2_fk_R'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_leg_R"].ik_leg_R = 1.0
                        refresh_hack()
                        pbones["properties_leg_R"].keyframe_insert(data_path='ik_leg_R')

                        #Re-Paste Transforms
                        pbones['thigh_fk_ctrl_R'].rotation_euler = ThighCtrlRotEuler
                        pbones['thigh_fk_ctrl_R'].rotation_quaternion = ThighCtrlRotQuat
                        pbones['thigh_fk_ctrl_R'].location = ThighCtrlLoc
                        pbones['thigh_fk_ctrl_R'].scale = ThighCtrlScale
                        refresh_hack()
                        pbones['thigh_fk_R'].rotation_euler = ThighFkRotEuler
                        pbones['thigh_fk_R'].rotation_quaternion = ThighFkRotQuat
                        pbones['thigh_fk_R'].location = ThighFkLoc
                        pbones['thigh_fk_R'].scale = ThighFkScale
                        refresh_hack()
                        pbones['shin_fk_R'].rotation_euler = ShinFkRotEuler
                        pbones['shin_fk_R'].rotation_quaternion = ShinFkRotQuat
                        pbones['shin_fk_R'].location = ShinFkLoc
                        pbones['shin_fk_R'].scale = ShinFkScale
                        refresh_hack()
                        pbones['foot_fk_R'].rotation_euler = FootFkRotEuler
                        pbones['foot_fk_R'].rotation_quaternion = FootFkRotQuat
                        pbones['foot_fk_R'].location = FootFkLoc
                        pbones['foot_fk_R'].scale = FootFkScale
                        refresh_hack()
                        pbones['foot_toe_1_fk_R'].rotation_euler = FootToe1FkRotEuler
                        pbones['foot_toe_1_fk_R'].rotation_quaternion = FootToe1FkRotQuat
                        pbones['foot_toe_1_fk_R'].location = FootToe1FkLoc
                        pbones['foot_toe_1_fk_R'].scale = FootToe1FkScale
                        refresh_hack()
                        pbones['foot_toe_2_fk_R'].rotation_euler = FootToe2FkRotEuler
                        pbones['foot_toe_2_fk_R'].rotation_quaternion = FootToe2FkRotQuat
                        pbones['foot_toe_2_fk_R'].location = FootToe2FkLoc
                        pbones['foot_toe_2_fk_R'].scale = FootToe2FkScale
                        refresh_hack()

                        insert_bkeys('thigh_fk_R', 'LocRotScale')
                        insert_bkeys('shin_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_ik_R', 'RotScale')
                        insert_bkeys('shin_ik_R', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_R', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_R', 'Rot')
                        insert_bkeys('toe_roll_1_R', 'Rot')
                        insert_bkeys('toe_roll_2_R', 'Rot')
                        insert_bkeys('sole_ctrl_R', 'Rot')
                        if pbones["properties_leg_R"].toggle_leg_ik_pole_R == 1.0:
                            insert_bkeys('knee_pole_R', 'Loc')

        return {"FINISHED"}

##### Leg_R FK>IK #####

class Operator_Snap_LegFKtoIK_R(bpy.types.Operator):

    bl_idname = "snap.leg_fk_to_ik_r"
    bl_label = "BlenRig Leg_R IK to FK"
    bl_description = "Switch Leg to IK preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        if bpy.context.active_object.pose.bones["properties_leg_R"].ik_leg_R > 0.9:

            #Collect Matrix
            ThighFkMat = pbones['thigh_fk_R'].matrix.copy()
            ThighFkLoc = pbones['thigh_fk_R'].location.copy()
            ThighFkScale = pbones['thigh_fk_R'].scale.copy()
            ShinFkMat = pbones['shin_fk_R'].matrix.copy()
            ShinFkLoc = pbones['shin_fk_R'].location.copy()
            ShinFkScale = pbones['shin_fk_R'].scale.copy()
            FootToe1FkMat = pbones['foot_toe_1_fk_R'].matrix.copy()
            FootToe1FkLoc = pbones['foot_toe_1_fk_R'].location.copy()
            FootToe1FkScale = pbones['foot_toe_1_fk_R'].scale.copy()
            FootToe2FkMat = pbones['foot_toe_2_fk_R'].matrix.copy()
            FootToe2FkLoc = pbones['foot_toe_2_fk_R'].location.copy()
            FootToe2FkScale = pbones['foot_toe_2_fk_R'].scale.copy()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        pbones["properties_leg_R"].keyframe_insert(data_path='ik_leg_R')
                        insert_bkeys('thigh_fk_R', 'LocRotScale')
                        insert_bkeys('shin_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_ik_R', 'RotScale')
                        insert_bkeys('shin_ik_R', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_R', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_R', 'Rot')
                        insert_bkeys('toe_roll_1_R', 'Rot')
                        insert_bkeys('toe_roll_2_R', 'Rot')
                        insert_bkeys('sole_ctrl_R', 'Rot')
                        if pbones["properties_leg_R"].toggle_leg_ik_pole_R == 1.0:
                            insert_bkeys('knee_pole_R', 'Loc')

            #Paste Matrix
            pVisLocExec(pbones['sole_ctrl_R'], pbones['snap_sole_ctrl_fk_R'])
            pVisRotExec(pbones['sole_ctrl_R'], pbones['snap_sole_ctrl_fk_R'])
            refresh_hack()
            pbones['foot_roll_ctrl_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['foot_ik_ctrl_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['foot_ik_ctrl_R'].location[:] = (0.0, 0.0, 0.0)
            pbones['toe_roll_1_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['toe_roll_2_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['foot_toe_ik_ctrl_mid_R'].location[:] = (0.0, 0.0, 0.0)
            pbones['foot_toe_ik_ctrl_mid_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pbones['toes_ik_ctrl_R'].location[:] = (0.0, 0.0, 0.0)
            pbones['toes_ik_ctrl_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
            pVisLocExec(pbones['knee_pole_R'], pbones['snap_knee_fk_R'])
            refresh_hack()

            bpy.context.active_object.pose.bones["properties_leg_R"].ik_leg_R = 0.0
            refresh_hack()

            pVisRotExec (pbones['thigh_ik_R'], pbones['thigh_fk_ctrl_R'])
            refresh_hack()
            pbones['thigh_fk_R'].matrix = ThighFkMat
            pbones['thigh_fk_R'].location = ThighFkLoc
            pbones['thigh_fk_R'].scale = ThighFkScale
            refresh_hack()
            pbones['shin_fk_R'].matrix = ShinFkMat
            pbones['shin_fk_R'].location = ShinFkLoc
            pbones['shin_fk_R'].scale = ShinFkScale
            refresh_hack()
            pbones['foot_toe_1_fk_R'].matrix = FootToe1FkMat
            pbones['foot_toe_1_fk_R'].location = FootToe1FkLoc
            pbones['foot_toe_1_fk_R'].scale = FootToe1FkScale
            refresh_hack()
            pbones['foot_toe_2_fk_R'].matrix = FootToe2FkMat
            pbones['foot_toe_2_fk_R'].location = FootToe2FkLoc
            pbones['foot_toe_2_fk_R'].scale = FootToe2FkScale
            refresh_hack()

            #Insert Keyframes if Action present
            if anim_data:
                if anim_data.action:
                    if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                        #Collect Local Transforms

                        SoleCtrlRotEuler = pbones['sole_ctrl_R'].rotation_euler.copy()
                        SoleCtrlRotQuat = pbones['sole_ctrl_R'].rotation_quaternion.copy()
                        SoleCtrlLoc = pbones['sole_ctrl_R'].location.copy()
                        SoleCtrlScale = pbones['sole_ctrl_R'].scale.copy()

                        KneePoleRotEuler = pbones['knee_pole_R'].rotation_euler.copy()
                        KneePoleRotQuat = pbones['knee_pole_R'].rotation_quaternion.copy()
                        KneePoleLoc = pbones['knee_pole_R'].location.copy()
                        KneePoleScale = pbones['knee_pole_R'].scale.copy()

                        ThighIkRotEuler = pbones['thigh_ik_R'].rotation_euler.copy()
                        ThighIkRotQuat = pbones['thigh_ik_R'].rotation_quaternion.copy()
                        ThighIkLoc = pbones['thigh_ik_R'].location.copy()
                        ThighIkScale = pbones['thigh_ik_R'].scale.copy()

                        ThighFkRotEuler = pbones['thigh_fk_R'].rotation_euler.copy()
                        ThighFkRotQuat = pbones['thigh_fk_R'].rotation_quaternion.copy()
                        ThighFkLoc = pbones['thigh_fk_R'].location.copy()
                        ThighFkScale = pbones['thigh_fk_R'].scale.copy()

                        ShinFkRotEuler = pbones['shin_fk_R'].rotation_euler.copy()
                        ShinFkRotQuat = pbones['shin_fk_R'].rotation_quaternion.copy()
                        ShinFkLoc = pbones['shin_fk_R'].location.copy()
                        ShinFkScale = pbones['shin_fk_R'].scale.copy()

                        FootToe1FkRotEuler = pbones['foot_toe_1_fk_R'].rotation_euler.copy()
                        FootToe1FkRotQuat = pbones['foot_toe_1_fk_R'].rotation_quaternion.copy()
                        FootToe1FkLoc = pbones['foot_toe_1_fk_R'].location.copy()
                        FootToe1FkScale = pbones['foot_toe_1_fk_R'].scale.copy()

                        FootToe2FkRotEuler = pbones['foot_toe_2_fk_R'].rotation_euler.copy()
                        FootToe2FkRotQuat = pbones['foot_toe_2_fk_R'].rotation_quaternion.copy()
                        FootToe2FkLoc = pbones['foot_toe_2_fk_R'].location.copy()
                        FootToe2FkScale = pbones['foot_toe_2_fk_R'].scale.copy()

                        #Jump to next Frame
                        bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                        #Key Property
                        armobj.pose.bones["properties_leg_R"].ik_leg_R = 0.0
                        refresh_hack()
                        pbones["properties_leg_R"].keyframe_insert(data_path='ik_leg_R')

                        #Re-Paste Transforms
                        pbones['sole_ctrl_R'].rotation_euler = SoleCtrlRotEuler
                        pbones['sole_ctrl_R'].rotation_quaternion = SoleCtrlRotQuat
                        pbones['sole_ctrl_R'].location = SoleCtrlLoc
                        pbones['sole_ctrl_R'].scale = SoleCtrlScale
                        refresh_hack()
                        pbones['knee_pole_R'].rotation_euler = KneePoleRotEuler
                        pbones['knee_pole_R'].rotation_quaternion = KneePoleRotQuat
                        pbones['knee_pole_R'].location = KneePoleLoc
                        pbones['knee_pole_R'].scale = KneePoleScale
                        refresh_hack()
                        pbones['thigh_ik_R'].rotation_euler = ThighIkRotEuler
                        pbones['thigh_ik_R'].rotation_quaternion = ThighIkRotQuat
                        pbones['thigh_ik_R'].location = ThighIkLoc
                        pbones['thigh_ik_R'].scale = ThighIkScale
                        refresh_hack()
                        pbones['thigh_fk_R'].rotation_euler = ThighFkRotEuler
                        pbones['thigh_fk_R'].rotation_quaternion = ThighFkRotQuat
                        pbones['thigh_fk_R'].location = ThighFkLoc
                        pbones['thigh_fk_R'].scale = ThighFkScale
                        refresh_hack()
                        pbones['shin_fk_R'].rotation_euler = ShinFkRotEuler
                        pbones['shin_fk_R'].rotation_quaternion = ShinFkRotQuat
                        pbones['shin_fk_R'].location = ShinFkLoc
                        pbones['shin_fk_R'].scale = ShinFkScale
                        refresh_hack()
                        pbones['foot_toe_1_fk_R'].rotation_euler = FootToe1FkRotEuler
                        pbones['foot_toe_1_fk_R'].rotation_quaternion = FootToe1FkRotQuat
                        pbones['foot_toe_1_fk_R'].location = FootToe1FkLoc
                        pbones['foot_toe_1_fk_R'].scale = FootToe1FkScale
                        refresh_hack()
                        pbones['foot_toe_2_fk_R'].rotation_euler = FootToe2FkRotEuler
                        pbones['foot_toe_2_fk_R'].rotation_quaternion = FootToe2FkRotQuat
                        pbones['foot_toe_2_fk_R'].location = FootToe2FkLoc
                        pbones['foot_toe_2_fk_R'].scale = FootToe2FkScale
                        refresh_hack()
                        pbones['foot_roll_ctrl_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['foot_ik_ctrl_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['foot_ik_ctrl_R'].location[:] = (0.0, 0.0, 0.0)
                        pbones['toe_roll_1_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['toe_roll_2_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['foot_toe_ik_ctrl_mid_R'].location[:] = (0.0, 0.0, 0.0)
                        pbones['foot_toe_ik_ctrl_mid_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        pbones['toes_ik_ctrl_R'].location[:] = (0.0, 0.0, 0.0)
                        pbones['toes_ik_ctrl_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                        refresh_hack()

                        insert_bkeys('thigh_fk_R', 'LocRotScale')
                        insert_bkeys('shin_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_fk_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_1_fk_R', 'LocRotScale')
                        insert_bkeys('foot_toe_2_fk_R', 'LocRotScale')
                        insert_bkeys('thigh_ik_R', 'RotScale')
                        insert_bkeys('shin_ik_R', 'RotScale')
                        insert_bkeys('foot_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_toe_ik_ctrl_mid_R', 'LocRotScale')
                        insert_bkeys('toes_ik_ctrl_R', 'LocRotScale')
                        insert_bkeys('foot_roll_ctrl_R', 'Rot')
                        insert_bkeys('toe_roll_1_R', 'Rot')
                        insert_bkeys('toe_roll_2_R', 'Rot')
                        insert_bkeys('sole_ctrl_R', 'Rot')
                        if pbones["properties_leg_R"].toggle_leg_ik_pole_R == 1.0:
                            insert_bkeys('knee_pole_R', 'Loc')

        return {"FINISHED"}

##### Leg_R Space #####

class Operator_Switch_Leg_Space_R(bpy.types.Operator):

    bl_idname = "switch.leg_space_r"
    bl_label = "BlenRig Switch Leg_R FK Space"
    bl_description = "Switch Leg_R FK Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        ThighFkCtrlMat = pbones['thigh_fk_ctrl_R'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_leg_R"].keyframe_insert(data_path='space_leg_R')
                    insert_bkeys('thigh_fk_ctrl_R', 'RotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_R = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_R = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['thigh_fk_ctrl_R'].matrix = ThighFkCtrlMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    ThighFkCtrlRotEuler = pbones['thigh_fk_ctrl_R'].rotation_euler.copy()
                    ThighFkCtrlRotQuat = pbones['thigh_fk_ctrl_R'].rotation_quaternion.copy()
                    ThighFkCtrlScale = pbones['thigh_fk_ctrl_R'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_R = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_R = 1.0
                        refresh_hack()
                    pbones["properties_leg_R"].keyframe_insert(data_path='space_leg_R')

                    #Re-Paste Transforms
                    pbones['thigh_fk_ctrl_R'].rotation_euler = ThighFkCtrlRotEuler
                    pbones['thigh_fk_ctrl_R'].rotation_quaternion = ThighFkCtrlRotQuat
                    pbones['thigh_fk_ctrl_R'].scale = ThighFkCtrlScale
                    refresh_hack()

                    insert_bkeys('thigh_fk_ctrl_R', 'RotScale')

        return {"FINISHED"}

#Create Space PopUp
def Leg_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.leg_space_r", text = "Free").space = 'Free'
    col.operator("switch.leg_space_r", text = "Torso").space = 'Torso'

class Operator_Show_Leg_Space_List_R(bpy.types.Operator):
    bl_idname = "show.leg_list_r"
    bl_label = "Leg_R FK Space Switch List"
    bl_description = "Switch Leg_R FK Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Leg_Space_List_R, title='Switch Leg_R FK Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Leg_Pole_R Space #####

class Operator_Switch_Leg_Pole_Space_R(bpy.types.Operator):

    bl_idname = "switch.leg_pole_space_r"
    bl_label = "BlenRig Switch Leg_R Pole Space"
    bl_description = "Switch Leg_R Pole Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_leg_R"].keyframe_insert(data_path='space_leg_ik_pole_R')
                    insert_bkeys('knee_pole_R', 'Loc')

        #Collect Matrix
        PoleMat = pbones['knee_pole_R'].matrix.copy()

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_ik_pole_R = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_ik_pole_R = 1.0
            refresh_hack()
        if self.space == 'Foot':
            bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_ik_pole_R = 2.0
            refresh_hack()

        #Paste Matrix
        pbones['knee_pole_R'].matrix = PoleMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    KneePoleLoc = pbones['knee_pole_R'].location.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_ik_pole_R = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_ik_pole_R = 1.0
                        refresh_hack()
                    if self.space == 'Foot':
                        bpy.context.active_object.pose.bones["properties_leg_R"].space_leg_ik_pole_R = 2.0
                        refresh_hack()
                    pbones["properties_leg_R"].keyframe_insert(data_path='space_leg_ik_pole_R')

                    #Re-Paste Transforms
                    pbones['knee_pole_R'].location = KneePoleLoc
                    refresh_hack()

                    insert_bkeys('knee_pole_R', 'Loc')

        return {"FINISHED"}

#Create Space PopUp
def Leg_Pole_Space_List_R(self, context):
    col = self.layout.column()
    col.operator("switch.leg_pole_space_r", text = "Free").space = 'Free'
    col.operator("switch.leg_pole_space_r", text = "Torso").space = 'Torso'
    col.operator("switch.leg_pole_space_r", text = "Foot").space = 'Foot'

class Operator_Show_Leg_Pole_Space_List_R(bpy.types.Operator):
    bl_idname = "show.leg_pole_list_r"
    bl_label = "Leg_R Pole Space Switch List"
    bl_description = "Switch Leg_R Pole Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Leg_Pole_Space_List_R, title='Switch Leg_R Pole Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Head Ops #####

##### Head #####

class Operator_Switch_Head_Space(bpy.types.Operator):

    bl_idname = "switch.head_space"
    bl_label = "BlenRig Switch Head Space"
    bl_description = "Switch Head Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        HeadMat = pbones['head_fk'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_head"].keyframe_insert(data_path='space_head')
                    insert_bkeys('head_fk', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_head"].space_head = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_head"].space_head = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['head_fk'].matrix = HeadMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HeadRotEuler = pbones['head_fk'].rotation_euler.copy()
                    HeadRotQuat = pbones['head_fk'].rotation_quaternion.copy()
                    HeadLoc = pbones['head_fk'].location.copy()
                    HeadScale = pbones['head_fk'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_head"].space_head = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_head"].space_head = 1.0
                        refresh_hack()
                    pbones["properties_head"].keyframe_insert(data_path='space_head')

                    #Re-Paste Transforms
                    pbones['head_fk'].rotation_euler = HeadRotEuler
                    pbones['head_fk'].rotation_quaternion = HeadRotQuat
                    pbones['head_fk'].location = HeadLoc
                    pbones['head_fk'].scale = HeadScale
                    refresh_hack()

                    insert_bkeys('head_fk', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Head_Space_List(self, context):
    col = self.layout.column()
    col.operator("switch.head_space", text = "Free").space = 'Free'
    col.operator("switch.head_space", text = "Torso").space = 'Torso'

class Operator_Show_Head_Space_List(bpy.types.Operator):
    bl_idname = "show.head_list"
    bl_label = "Head Space Switch List"
    bl_description = "Switch Head Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Head_Space_List, title='Switch Head Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Neck #####

class Operator_Switch_Neck_Space(bpy.types.Operator):

    bl_idname = "switch.neck_space"
    bl_label = "BlenRig Switch Neck Space"
    bl_description = "Switch Neck Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        NeckMat = pbones['neck_1_fk'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_head"].keyframe_insert(data_path='space_neck')
                    insert_bkeys('neck_1_fk', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_head"].space_neck = 0.0
            refresh_hack()
        if self.space == 'Torso':
            bpy.context.active_object.pose.bones["properties_head"].space_neck = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['neck_1_fk'].matrix = NeckMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    NeckRotEuler = pbones['neck_1_fk'].rotation_euler.copy()
                    NeckRotQuat = pbones['neck_1_fk'].rotation_quaternion.copy()
                    NeckLoc = pbones['neck_1_fk'].location.copy()
                    NeckScale = pbones['neck_1_fk'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_head"].space_neck = 0.0
                        refresh_hack()
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_head"].space_neck = 1.0
                        refresh_hack()
                    pbones["properties_head"].keyframe_insert(data_path='space_neck')

                    #Re-Paste Transforms
                    pbones['neck_1_fk'].rotation_euler = NeckRotEuler
                    pbones['neck_1_fk'].rotation_quaternion = NeckRotQuat
                    pbones['neck_1_fk'].location = NeckLoc
                    pbones['neck_1_fk'].scale = NeckScale
                    refresh_hack()

                    insert_bkeys('neck_1_fk', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Neck_Space_List(self, context):
    col = self.layout.column()
    col.operator("switch.neck_space", text = "Free").space = 'Free'
    col.operator("switch.neck_space", text = "Torso").space = 'Torso'

class Operator_Show_Neck_Space_List(bpy.types.Operator):
    bl_idname = "show.neck_list"
    bl_label = "Neck Space Switch List"
    bl_description = "Switch Neck Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Neck_Space_List, title='Switch Neck Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Look #####

class Operator_Switch_Look_Space(bpy.types.Operator):

    bl_idname = "switch.look_space"
    bl_label = "BlenRig Switch Look Space"
    bl_description = "Switch Look Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_head"].keyframe_insert(data_path='look_switch')
                    insert_bkeys('look', 'LocRotScale')

        if self.space == 'Free':
            #Get Matrix in previous space
            Look_world_mat = pbones['look'].id_data.matrix_world.copy()
            Look_mat = pbones['look'].matrix.copy()

            #Change Space
            bpy.context.active_object.pose.bones["properties_head"].look_switch = 0.0

            paste_visual_matrix('look', 'look_free', Look_world_mat, Look_mat, 'Location')
            paste_visual_matrix('look', 'look_free', Look_world_mat, Look_mat, 'Rotation')

        if self.space == 'Body':
            #Get Matrix in previous space
            Look_world_mat = pbones['look'].id_data.matrix_world.copy()
            Look_mat = pbones['look'].matrix.copy()

            #Change Space
            bpy.context.active_object.pose.bones["properties_head"].look_switch = 1.0

            paste_visual_matrix('look', 'master_body_pivot', Look_world_mat, Look_mat, 'Location')
            paste_visual_matrix('look', 'master_body_pivot', Look_world_mat, Look_mat, 'Rotation')

        if self.space == 'Torso':
            #Get Matrix in previous space
            Look_world_mat = pbones['look'].id_data.matrix_world.copy()
            Look_mat = pbones['look'].matrix.copy()

            #Change Space
            bpy.context.active_object.pose.bones["properties_head"].look_switch = 2.0

            paste_visual_matrix('look', 'master_torso_pivot', Look_world_mat, Look_mat, 'Location')
            paste_visual_matrix('look', 'master_torso_pivot', Look_world_mat, Look_mat, 'Rotation')

        if self.space == 'Head':
            #Get Matrix in previous space
            Look_world_mat = pbones['look'].id_data.matrix_world.copy()
            Look_mat = pbones['look'].matrix.copy()

            #Change Space
            bpy.context.active_object.pose.bones["properties_head"].look_switch = 3.0

            paste_visual_matrix('look', 'head_fk', Look_world_mat, Look_mat, 'Location')
            paste_visual_matrix('look', 'head_fk', Look_world_mat, Look_mat, 'Rotation')

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    LookRotEuler = pbones['look'].rotation_euler.copy()
                    LookRotQuat = pbones['look'].rotation_quaternion.copy()
                    LookLoc = pbones['look'].location.copy()
                    LookScale = pbones['look'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_head"].look_switch = 0.0
                    if self.space == 'Body':
                        bpy.context.active_object.pose.bones["properties_head"].look_switch = 1.0
                    if self.space == 'Torso':
                        bpy.context.active_object.pose.bones["properties_head"].look_switch = 2.0
                    if self.space == 'Head':
                        bpy.context.active_object.pose.bones["properties_head"].look_switch = 3.0
                    pbones["properties_head"].keyframe_insert(data_path='look_switch')

                    #Re-Paste Transforms
                    pbones['look'].rotation_euler = LookRotEuler
                    pbones['look'].rotation_quaternion = LookRotQuat
                    pbones['look'].location = LookLoc
                    pbones['look'].scale = LookScale
                    refresh_hack()

                    insert_bkeys('look', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Look_Space_List(self, context):
    col = self.layout.column()
    col.operator("switch.look_space", text = "Free").space = 'Free'
    col.operator("switch.look_space", text = "Body").space = 'Body'
    col.operator("switch.look_space", text = "Torso").space = 'Torso'
    col.operator("switch.look_space", text = "Head").space = 'Head'

class Operator_Show_Look_Space_List(bpy.types.Operator):
    bl_idname = "show.look_list"
    bl_label = "Look Space Switch List"
    bl_description = "Switch Look Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Look_Space_List, title='Switch Look Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Props Ops #####

##### EyeGlasses #####

class Operator_Switch_Eyeglasses_Space(bpy.types.Operator):

    bl_idname = "switch.eyeglasses_space"
    bl_label = "BlenRig Switch Eyeglasses Space"
    bl_description = "Switch Eyeglasses Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        EyeglassesMat = pbones['eyeglasses_mstr'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_head"].keyframe_insert(data_path='["glasses_free"]')
                    insert_bkeys('eyeglasses_mstr', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_head"]["glasses_free"] = 0.0
            refresh_hack()
        if self.space == 'Head':
            bpy.context.active_object.pose.bones["properties_head"]["glasses_free"] = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['eyeglasses_mstr'].matrix = EyeglassesMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    EyeGlassesRotEuler = pbones['eyeglasses_mstr'].rotation_euler.copy()
                    EyeGlassesRotQuat = pbones['eyeglasses_mstr'].rotation_quaternion.copy()
                    EyeGlassesLoc = pbones['eyeglasses_mstr'].location.copy()
                    EyeGlassesScale = pbones['eyeglasses_mstr'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_head"]["glasses_free"] = 0.0
                        refresh_hack()
                    if self.space == 'Head':
                        bpy.context.active_object.pose.bones["properties_head"]["glasses_free"] = 1.0
                        refresh_hack()
                    pbones["properties_head"].keyframe_insert(data_path='["glasses_free"]')

                    #Re-Paste Transforms
                    pbones['eyeglasses_mstr'].rotation_euler = EyeGlassesRotEuler
                    pbones['eyeglasses_mstr'].rotation_quaternion = EyeGlassesRotQuat
                    pbones['eyeglasses_mstr'].location = EyeGlassesLoc
                    pbones['eyeglasses_mstr'].scale = EyeGlassesScale
                    refresh_hack()

                    insert_bkeys('eyeglasses_mstr', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Eyeglasses_Space_List(self, context):
    col = self.layout.column()
    col.operator("switch.eyeglasses_space", text = "Free").space = 'Free'
    col.operator("switch.eyeglasses_space", text = "Head").space = 'Head'

class Operator_Show_Eyeglasses_Space_List(bpy.types.Operator):
    bl_idname = "show.eyeglasses_list"
    bl_label = "Eyeglasses Space Switch List"
    bl_description = "Switch Eyeglasses Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Eyeglasses_Space_List, title='Switch Eyeglasses Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Hat #####

class Operator_Switch_Hat_Space(bpy.types.Operator):

    bl_idname = "switch.hat_space"
    bl_label = "BlenRig Switch Hat Space"
    bl_description = "Switch Hat Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        HatMat = pbones['hat_mstr'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_head"].keyframe_insert(data_path='["hat_free"]')
                    insert_bkeys('hat_mstr', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_head"]["hat_free"] = 0.0
            refresh_hack()
        if self.space == 'Head':
            bpy.context.active_object.pose.bones["properties_head"]["hat_free"] = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['hat_mstr'].matrix = HatMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HatRotEuler = pbones['hat_mstr'].rotation_euler.copy()
                    HatRotQuat = pbones['hat_mstr'].rotation_quaternion.copy()
                    HatLoc = pbones['hat_mstr'].location.copy()
                    HatScale = pbones['hat_mstr'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_head"]["hat_free"] = 0.0
                        refresh_hack()
                    if self.space == 'Head':
                        bpy.context.active_object.pose.bones["properties_head"]["hat_free"] = 1.0
                        refresh_hack()
                    pbones["properties_head"].keyframe_insert(data_path='["hat_free"]')

                    #Re-Paste Transforms
                    pbones['hat_mstr'].rotation_euler = HatRotEuler
                    pbones['hat_mstr'].rotation_quaternion = HatRotQuat
                    pbones['hat_mstr'].location = HatLoc
                    pbones['hat_mstr'].scale = HatScale
                    refresh_hack()

                    insert_bkeys('hat_mstr', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Hat_Space_List(self, context):
    col = self.layout.column()
    col.operator("switch.hat_space", text = "Free").space = 'Free'
    col.operator("switch.hat_space", text = "Head").space = 'Head'

class Operator_Show_Hat_Space_List(bpy.types.Operator):
    bl_idname = "show.hat_list"
    bl_label = "Hat Space Switch List"
    bl_description = "Switch Hat Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Hat_Space_List, title='Switch Hat Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Hand Accessory #####

class Operator_Switch_Hand_Accessory_Space(bpy.types.Operator):

    bl_idname = "switch.hand_accessory_space"
    bl_label = "BlenRig Switch Hand Accessory Space"
    bl_description = "Switch Hand Accessory Space preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    #Create string property to parse argument to the operator
    space : bpy.props.StringProperty()

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Collect Matrix
        AccessoryMat = pbones['accessory'].matrix.copy()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    pbones["properties_arm_L"].keyframe_insert(data_path='["hand_accessory_L"]')
                    pbones["properties_arm_R"].keyframe_insert(data_path='["hand_accessory_R"]')
                    insert_bkeys('accessory', 'LocRotScale')

        if self.space == 'Free':
            bpy.context.active_object.pose.bones["properties_arm_L"]["hand_accessory_L"] = 0.0
            bpy.context.active_object.pose.bones["properties_arm_R"]["hand_accessory_R"] = 0.0
            refresh_hack()
        if self.space == 'Hand_L':
            bpy.context.active_object.pose.bones["properties_arm_L"]["hand_accessory_L"] = 1.0
            bpy.context.active_object.pose.bones["properties_arm_R"]["hand_accessory_R"] = 0.0
            refresh_hack()
        if self.space == 'Hand_R':
            bpy.context.active_object.pose.bones["properties_arm_L"]["hand_accessory_L"] = 0.0
            bpy.context.active_object.pose.bones["properties_arm_R"]["hand_accessory_R"] = 1.0
            refresh_hack()

        #Paste Matrix
        pbones['accessory'].matrix = AccessoryMat
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    AccessoryEuler = pbones['accessory'].rotation_euler.copy()
                    AccessoryRotQuat = pbones['accessory'].rotation_quaternion.copy()
                    AccessoryLoc = pbones['accessory'].location.copy()
                    AccessoryScale = pbones['accessory'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Key Property
                    if self.space == 'Free':
                        bpy.context.active_object.pose.bones["properties_arm_L"]["hand_accessory_L"] = 0.0
                        bpy.context.active_object.pose.bones["properties_arm_R"]["hand_accessory_R"] = 0.0
                        refresh_hack()
                    if self.space == 'Hand_L':
                        bpy.context.active_object.pose.bones["properties_arm_L"]["hand_accessory_L"] = 1.0
                        bpy.context.active_object.pose.bones["properties_arm_R"]["hand_accessory_R"] = 0.0
                        refresh_hack()
                    if self.space == 'Hand_R':
                        bpy.context.active_object.pose.bones["properties_arm_L"]["hand_accessory_L"] = 0.0
                        bpy.context.active_object.pose.bones["properties_arm_R"]["hand_accessory_R"] = 1.0
                        refresh_hack()
                    pbones["properties_arm_L"].keyframe_insert(data_path='["hand_accessory_L"]')
                    pbones["properties_arm_R"].keyframe_insert(data_path='["hand_accessory_R"]')

                    #Re-Paste Transforms
                    pbones['accessory'].rotation_euler = AccessoryEuler
                    pbones['accessory'].rotation_quaternion = AccessoryRotQuat
                    pbones['accessory'].location = AccessoryLoc
                    pbones['accessory'].scale = AccessoryScale
                    refresh_hack()

                    insert_bkeys('accessory', 'LocRotScale')

        return {"FINISHED"}

#Create Space PopUp
def Hand_Accessory_Space_List(self, context):
    col = self.layout.column()
    col.operator("switch.hand_accessory_space", text = "Free").space = 'Free'
    col.operator("switch.hand_accessory_space", text = "Hand_L").space = 'Hand_L'
    col.operator("switch.hand_accessory_space", text = "Hand_R").space = 'Hand_R'

class Operator_Show_Hand_Accessory_Space_List(bpy.types.Operator):
    bl_idname = "show.hand_accessory_list"
    bl_label = "Hand Accessory Space Switch List"
    bl_description = "Switch Hand Accessory Space"

    def invoke(self, context, event):
        context.window_manager.popup_menu(Hand_Accessory_Space_List, title='Switch Hand Accessory Space', icon='MOD_ARMATURE')
        return {'FINISHED'}

##### Pivots Ops #####

##### Hand_L Pivot #####

class Operator_Reset_Hand_L_Pivot(bpy.types.Operator):

    bl_idname = "reset.hand_l_pivot"
    bl_label = "BlenRig Reset Hand_L Pivot"
    bl_description = "Reset Hand_L Pivot preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                    insert_bkeys('hand_ik_pivot_point_L', 'LocRotScale')

        #Paste Matrix
        pVisLocExec (pbones['hand_ik_ctrl_L'], pbones['hand_ik_pivot_L'])
        pVisRotExec (pbones['hand_ik_ctrl_L'], pbones['hand_ik_pivot_L'])
        refresh_hack()
        pbones['hand_ik_pivot_point_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
        pbones['hand_ik_pivot_point_L'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
        pbones['hand_ik_pivot_point_L'].location[:] = (0.0, 0.0, 0.0)
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HandIkCtrlRotEuler = pbones['hand_ik_ctrl_L'].rotation_euler.copy()
                    HandIkCtrlLoc = pbones['hand_ik_ctrl_L'].location.copy()
                    HandIkCtrlScale = pbones['hand_ik_ctrl_L'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Re-Paste Transforms
                    pbones['hand_ik_ctrl_L'].rotation_euler = HandIkCtrlRotEuler
                    pbones['hand_ik_ctrl_L'].location = HandIkCtrlLoc
                    pbones['hand_ik_ctrl_L'].scale = HandIkCtrlScale
                    refresh_hack()
                    pbones['hand_ik_pivot_point_L'].rotation_euler[:] = (0.0, 0.0, 0.0)
                    pbones['hand_ik_pivot_point_L'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
                    pbones['hand_ik_pivot_point_L'].location[:] = (0.0, 0.0, 0.0)
                    refresh_hack()

                    insert_bkeys('hand_ik_ctrl_L', 'LocRotScale')
                    insert_bkeys('hand_ik_pivot_point_L', 'LocRotScale')

        return {"FINISHED"}

##### Hand_R Pivot #####

class Operator_Reset_Hand_R_Pivot(bpy.types.Operator):

    bl_idname = "reset.hand_r_pivot"
    bl_label = "BlenRig Reset Hand_R Pivot"
    bl_description = "Reset Hand_R Pivot preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                    insert_bkeys('hand_ik_pivot_point_R', 'LocRotScale')

        #Paste Matrix
        pVisLocExec (pbones['hand_ik_ctrl_R'], pbones['hand_ik_pivot_R'])
        pVisRotExec (pbones['hand_ik_ctrl_R'], pbones['hand_ik_pivot_R'])
        refresh_hack()
        pbones['hand_ik_pivot_point_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
        pbones['hand_ik_pivot_point_R'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
        pbones['hand_ik_pivot_point_R'].location[:] = (0.0, 0.0, 0.0)
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    HandIkCtrlRotEuler = pbones['hand_ik_ctrl_R'].rotation_euler.copy()
                    HandIkCtrlLoc = pbones['hand_ik_ctrl_R'].location.copy()
                    HandIkCtrlScale = pbones['hand_ik_ctrl_R'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Re-Paste Transforms
                    pbones['hand_ik_ctrl_R'].rotation_euler = HandIkCtrlRotEuler
                    pbones['hand_ik_ctrl_R'].location = HandIkCtrlLoc
                    pbones['hand_ik_ctrl_R'].scale = HandIkCtrlScale
                    refresh_hack()
                    pbones['hand_ik_pivot_point_R'].rotation_euler[:] = (0.0, 0.0, 0.0)
                    pbones['hand_ik_pivot_point_R'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
                    pbones['hand_ik_pivot_point_R'].location[:] = (0.0, 0.0, 0.0)
                    refresh_hack()

                    insert_bkeys('hand_ik_ctrl_R', 'LocRotScale')
                    insert_bkeys('hand_ik_pivot_point_R', 'LocRotScale')

        return {"FINISHED"}

##### Master_Torso Pivot #####

class Operator_Reset_Master_Torso_Pivot(bpy.types.Operator):

    bl_idname = "reset.master_torso_pivot"
    bl_label = "BlenRig Reset Master_Torso Pivot"
    bl_description = "Reset Master_Torso Pivot preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    insert_bkeys('master_torso', 'LocRotScale')
                    insert_bkeys('master_torso_pivot_point', 'LocRotScale')

        #Paste Matrix
        pVisLocExec (pbones['master_torso'], pbones['master_torso_pivot'])
        pVisRotExec (pbones['master_torso'], pbones['master_torso_pivot'])
        refresh_hack()
        pbones['master_torso_pivot_point'].rotation_euler[:] = (0.0, 0.0, 0.0)
        pbones['master_torso_pivot_point'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
        pbones['master_torso_pivot_point'].location[:] = (0.0, 0.0, 0.0)
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    MasterTorsoRotEuler = pbones['master_torso'].rotation_euler.copy()
                    MasterTorsoLoc = pbones['master_torso'].location.copy()
                    MasterTorsoScale = pbones['master_torso'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Re-Paste Transforms
                    pbones['master_torso'].rotation_euler = MasterTorsoRotEuler
                    pbones['master_torso'].location = MasterTorsoLoc
                    pbones['master_torso'].scale = MasterTorsoScale
                    refresh_hack()
                    pbones['master_torso_pivot_point'].rotation_euler[:] = (0.0, 0.0, 0.0)
                    pbones['master_torso_pivot_point'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
                    pbones['master_torso_pivot_point'].location[:] = (0.0, 0.0, 0.0)
                    refresh_hack()

                    insert_bkeys('master_torso', 'LocRotScale')
                    insert_bkeys('master_torso_pivot_point', 'LocRotScale')

        return {"FINISHED"}

##### Master_Body Pivot #####

class Operator_Reset_Master_Body_Pivot(bpy.types.Operator):

    bl_idname = "reset.master_body_pivot"
    bl_label = "BlenRig Reset Master_Body Pivot"
    bl_description = "Reset Master_Body Pivot preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    insert_bkeys('master_body', 'LocRotScale')
                    insert_bkeys('master_body_pivot_point', 'LocRotScale')

        #Paste Matrix
        pVisLocExec (pbones['master_body'], pbones['master_body_pivot'])
        pVisRotExec (pbones['master_body'], pbones['master_body_pivot'])
        refresh_hack()
        pbones['master_body_pivot_point'].rotation_euler[:] = (0.0, 0.0, 0.0)
        pbones['master_body_pivot_point'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
        pbones['master_body_pivot_point'].location[:] = (0.0, 0.0, 0.0)
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    MasterTorsoRotEuler = pbones['master_body'].rotation_euler.copy()
                    MasterTorsoLoc = pbones['master_body'].location.copy()
                    MasterTorsoScale = pbones['master_body'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Re-Paste Transforms
                    pbones['master_body'].rotation_euler = MasterTorsoRotEuler
                    pbones['master_body'].location = MasterTorsoLoc
                    pbones['master_body'].scale = MasterTorsoScale
                    refresh_hack()
                    pbones['master_body_pivot_point'].rotation_euler[:] = (0.0, 0.0, 0.0)
                    pbones['master_body_pivot_point'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
                    pbones['master_body_pivot_point'].location[:] = (0.0, 0.0, 0.0)
                    refresh_hack()

                    insert_bkeys('master_body', 'LocRotScale')
                    insert_bkeys('master_body_pivot_point', 'LocRotScale')

        return {"FINISHED"}

##### Master Pivot #####

class Operator_Reset_Master_Pivot(bpy.types.Operator):

    bl_idname = "reset.master_pivot"
    bl_label = "BlenRig Reset Master Pivot"
    bl_description = "Reset Master Pivot preserving pose"
    bl_options = {'REGISTER', 'UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True
        else:
            return False

    def execute(self, context):

        armobj = bpy.context.active_object
        pbones = armobj.pose.bones
        anim_data = armobj.animation_data

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    insert_bkeys('master', 'LocRotScale')
                    insert_bkeys('master_pivot_point', 'LocRotScale')

        #Paste Matrix
        pVisLocExec (pbones['master'], pbones['master_pivot'])
        pVisRotExec (pbones['master'], pbones['master_pivot'])
        refresh_hack()
        pbones['master_pivot_point'].rotation_euler[:] = (0.0, 0.0, 0.0)
        pbones['master_pivot_point'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
        pbones['master_pivot_point'].location[:] = (0.0, 0.0, 0.0)
        refresh_hack()

        #Insert Keyframes if Action present
        if anim_data:
            if anim_data.action:
                if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True:
                    #Collect Local Transforms
                    MasterTorsoRotEuler = pbones['master'].rotation_euler.copy()
                    MasterTorsoLoc = pbones['master'].location.copy()
                    MasterTorsoScale = pbones['master'].scale.copy()

                    #Jump to next Frame
                    bpy.context.scene.frame_set (bpy.context.scene.frame_current + 1)

                    #Re-Paste Transforms
                    pbones['master'].rotation_euler = MasterTorsoRotEuler
                    pbones['master'].location = MasterTorsoLoc
                    pbones['master'].scale = MasterTorsoScale
                    refresh_hack()
                    pbones['master_pivot_point'].rotation_euler[:] = (0.0, 0.0, 0.0)
                    pbones['master_pivot_point'].rotation_quaternion[:] = (1.0,0.0, 0.0, 0.0)
                    pbones['master_pivot_point'].location[:] = (0.0, 0.0, 0.0)
                    refresh_hack()

                    insert_bkeys('master', 'LocRotScale')
                    insert_bkeys('master_pivot_point', 'LocRotScale')

        return {"FINISHED"}

#####################################################################################################################
################################# LEGACY RIG SNAPPING ###############################################################
#####################################################################################################################

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

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
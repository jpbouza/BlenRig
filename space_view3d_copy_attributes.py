import bpy
from mathutils import Matrix
from bpy.types import (
    Operator,
    Menu,
)
from bpy.props import (
    BoolVectorProperty,
    StringProperty,
)

# First part of the operator Info message
INFO_MESSAGE = "Copy Attributes: "


def build_exec(loopfunc, func):
    """Generator function that returns exec functions for operators """

    def exec_func(self, context):
        loopfunc(self, context, func)
        return {'FINISHED'}
    return exec_func


def build_invoke(loopfunc, func):
    """Generator function that returns invoke functions for operators"""

    def invoke_func(self, context, event):
        loopfunc(self, context, func)
        return {'FINISHED'}
    return invoke_func


def build_op(idname, label, description, fpoll, fexec, finvoke):
    """Generator function that returns the basic operator"""

    class myopic(Operator):
        bl_idname = idname
        bl_label = label
        bl_description = description
        execute = fexec
        poll = fpoll
        invoke = finvoke
    return myopic


def genops(copylist, oplist, prefix, poll_func, loopfunc):
    """Generate ops from the copy list and its associated functions"""
    for op in copylist:
        exec_func = build_exec(loopfunc, op[3])
        invoke_func = build_invoke(loopfunc, op[3])
        opclass = build_op(prefix + op[0], "Copy " + op[1], op[2],
                           poll_func, exec_func, invoke_func)
        oplist.append(opclass)


def generic_copy(source, target, string=""):
    """Copy attributes from source to target that have string in them"""
    for attr in dir(source):
        if attr.find(string) > -1:
            try:
                setattr(target, attr, getattr(source, attr))
            except:
                pass
    return


def getmat(bone, active, context, ignoreparent):
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


def pLoopExec(self, context, funk):
    """Loop over selected bones and execute funk on them"""
    active = context.active_pose_bone
    selected = context.selected_pose_bones
    selected.remove(active)
    for bone in selected:
        funk(bone, active, context)


# The following functions are used to copy attributes from active to bone

def pLocLocExec(bone, active, context):
    bone.location = active.location


def pLocRotExec(bone, active, context):
    rotcopy(bone, active.matrix_basis.to_3x3())


def pLocScaExec(bone, active, context):
    bone.scale = active.scale


def pVisLocExec(bone, active, context):
    bone.location = getmat(bone, active, context, False).to_translation()


def pVisRotExec(bone, active, context):
    obj_bone = bone.id_data
    rotcopy(bone, getmat(bone, active,
                         context, not obj_bone.data.bones[bone.name].use_inherit_rotation))


def pVisScaExec(bone, active, context):
    obj_bone = bone.id_data
    bone.scale = getmat(bone, active, context,
                        not obj_bone.data.bones[bone.name].use_inherit_scale)\
        .to_scale()


def pDrwExec(bone, active, context):
    bone.custom_shape = active.custom_shape
    bone.use_custom_shape_bone_size = active.use_custom_shape_bone_size
    bone.custom_shape_scale = active.custom_shape_scale
    bone.bone.show_wire = active.bone.show_wire


def pLokExec(bone, active, context):
    for index, state in enumerate(active.lock_location):
        bone.lock_location[index] = state
    for index, state in enumerate(active.lock_rotation):
        bone.lock_rotation[index] = state
    bone.lock_rotations_4d = active.lock_rotations_4d
    bone.lock_rotation_w = active.lock_rotation_w
    for index, state in enumerate(active.lock_scale):
        bone.lock_scale[index] = state


def pConExec(bone, active, context):
    for old_constraint in active.constraints.values():
        new_constraint = bone.constraints.new(old_constraint.type)
        generic_copy(old_constraint, new_constraint)


def pIKsExec(bone, active, context):
    generic_copy(active, bone, "ik_")


def pBBonesExec(bone, active, context):
    object = active.id_data
    generic_copy(
        object.data.bones[active.name],
        object.data.bones[bone.name],
        "bbone_")


pose_copies = (
    ('pose_loc_loc', "Local Location",
     "Copy Location from Active to Selected", pLocLocExec),
    ('pose_loc_rot', "Local Rotation",
     "Copy Rotation from Active to Selected", pLocRotExec),
    ('pose_loc_sca', "Local Scale",
     "Copy Scale from Active to Selected", pLocScaExec),
    ('pose_vis_loc', "Visual Location",
     "Copy Location from Active to Selected", pVisLocExec),
    ('pose_vis_rot', "Visual Rotation",
     "Copy Rotation from Active to Selected", pVisRotExec),
    ('pose_vis_sca', "Visual Scale",
     "Copy Scale from Active to Selected", pVisScaExec),
    ('pose_drw', "Bone Shape",
     "Copy Bone Shape from Active to Selected", pDrwExec),
    ('pose_lok', "Protected Transform",
     "Copy Protected Transforms from Active to Selected", pLokExec),
    ('pose_con', "Bone Constraints",
     "Copy Object Constraints from Active to Selected", pConExec),
    ('pose_iks', "IK Limits",
     "Copy IK Limits from Active to Selected", pIKsExec),
    ('bbone_settings', "BBone Settings",
     "Copy BBone Settings from Active to Selected", pBBonesExec),
)

@classmethod
def pose_poll_func(cls, context):
    return(context.mode == 'POSE')


def pose_invoke_func(self, context, event):
    wm = context.window_manager
    wm.invoke_props_dialog(self)
    return {'RUNNING_MODAL'}


class CopySelectedPoseConstraints(Operator):
    """Copy Chosen constraints from active to selected"""
    bl_idname = "pose.copy_selected_constraints"
    bl_label = "Copy Selected Constraints"

    selection: BoolVectorProperty(
        size=32,
        options={'SKIP_SAVE'}
    )

    poll = pose_poll_func
    invoke = pose_invoke_func

    def draw(self, context):
        layout = self.layout
        for idx, const in enumerate(context.active_pose_bone.constraints):
            layout.prop(self, "selection", index=idx, text=const.name,
                        toggle=True)

    def execute(self, context):
        active = context.active_pose_bone
        selected = context.selected_pose_bones[:]
        selected.remove(active)
        for bone in selected:
            for index, flag in enumerate(self.selection):
                if flag:
                    bone.constraints.copy(active.constraints[index])
        return {'FINISHED'}


pose_ops = []  # list of pose mode copy operators
genops(pose_copies, pose_ops, "pose.copy_", pose_poll_func, pLoopExec)


class VIEW3D_MT_posecopypopup(Menu):
    bl_label = "Copy Attributes"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        for op in pose_copies:
            layout.operator("pose.copy_" + op[0])
        layout.operator("pose.copy_selected_constraints")
        layout.operator("pose.copy", text="copy pose")


def obLoopExec(self, context, funk):
    """Loop over selected objects and execute funk on them"""
    active = context.active_object
    selected = context.selected_objects[:]
    selected.remove(active)
    for obj in selected:
        msg = funk(obj, active, context)
    if msg:
        self.report({msg[0]}, INFO_MESSAGE + msg[1])


def world_to_basis(active, ob, context):
    """put world coords of active as basis coords of ob"""
    local = ob.parent.matrix_world.inverted() @ active.matrix_world
    P = ob.matrix_basis @ ob.matrix_local.inverted()
    mat = P @ local
    return(mat)


# The following functions are used to copy attributes from
# active to selected object

def obLoc(ob, active, context):
    ob.location = active.location


def obRot(ob, active, context):
    rotcopy(ob, active.matrix_local.to_3x3())


def obSca(ob, active, context):
    ob.scale = active.scale


def obVisLoc(ob, active, context):
    if ob.parent:
        mat = world_to_basis(active, ob, context)
        ob.location = mat.to_translation()
    else:
        ob.location = active.matrix_world.to_translation()
    return('INFO', "Object location copied")


def obVisRot(ob, active, context):
    if ob.parent:
        mat = world_to_basis(active, ob, context)
        rotcopy(ob, mat.to_3x3())
    else:
        rotcopy(ob, active.matrix_world.to_3x3())
    return('INFO', "Object rotation copied")


def obVisSca(ob, active, context):
    if ob.parent:
        mat = world_to_basis(active, ob, context)
        ob.scale = mat.to_scale()
    else:
        ob.scale = active.matrix_world.to_scale()
    return('INFO', "Object scale copied")


def obDrw(ob, active, context):
    ob.display_type = active.display_type
    ob.show_axis = active.show_axis
    ob.show_bounds = active.show_bounds
    ob.display_bounds_type = active.display_bounds_type
    ob.show_name = active.show_name
    ob.show_texture_space = active.show_texture_space
    ob.show_transparent = active.show_transparent
    ob.show_wire = active.show_wire
    ob.show_in_front = active.show_in_front
    ob.empty_display_type = active.empty_display_type
    ob.empty_display_size = active.empty_display_size


def obOfs(ob, active, context):
    ob.time_offset = active.time_offset
    return('INFO', "Time offset copied")


def obDup(ob, active, context):
    generic_copy(active, ob, "dupli")
    return('INFO', "Duplication method copied")


def obCol(ob, active, context):
    ob.color = active.color


def obLok(ob, active, context):
    for index, state in enumerate(active.lock_location):
        ob.lock_location[index] = state
    for index, state in enumerate(active.lock_rotation):
        ob.lock_rotation[index] = state
    ob.lock_rotations_4d = active.lock_rotations_4d
    ob.lock_rotation_w = active.lock_rotation_w
    for index, state in enumerate(active.lock_scale):
        ob.lock_scale[index] = state
    return('INFO', "Transform locks copied")


def obCon(ob, active, context):
    # for consistency with 2.49, delete old constraints first
    for removeconst in ob.constraints:
        ob.constraints.remove(removeconst)
    for old_constraint in active.constraints.values():
        new_constraint = ob.constraints.new(old_constraint.type)
        generic_copy(old_constraint, new_constraint)
    return('INFO', "Constraints copied")


def obTex(ob, active, context):
    if 'texspace_location' in dir(ob.data) and 'texspace_location' in dir(
       active.data):
        ob.data.texspace_location[:] = active.data.texspace_location[:]
    if 'texspace_size' in dir(ob.data) and 'texspace_size' in dir(active.data):
        ob.data.texspace_size[:] = active.data.texspace_size[:]
    return('INFO', "Texture space copied")


def obIdx(ob, active, context):
    ob.pass_index = active.pass_index
    return('INFO', "Pass index copied")


def obMod(ob, active, context):
    for modifier in ob.modifiers:
        # remove existing before adding new:
        ob.modifiers.remove(modifier)
    for old_modifier in active.modifiers.values():
        new_modifier = ob.modifiers.new(name=old_modifier.name,
                                        type=old_modifier.type)
        generic_copy(old_modifier, new_modifier)
    return('INFO', "Modifiers copied")


def obGrp(ob, active, context):
    for grp in bpy.data.collections:
        if active.name in grp.objects and ob.name not in grp.objects:
            grp.objects.link(ob)
    return('INFO', "Groups copied")


def obWei(ob, active, context):
    # sanity check: are source and target both mesh objects?
    if ob.type != 'MESH' or active.type != 'MESH':
        return('ERROR', "objects have to be of mesh type, doing nothing")
    me_source = active.data
    me_target = ob.data
    # sanity check: do source and target have the same amount of verts?
    if len(me_source.vertices) != len(me_target.vertices):
        return('ERROR', "objects have different vertex counts, doing nothing")
    vgroups_IndexName = {}
    for i in range(0, len(active.vertex_groups)):
        groups = active.vertex_groups[i]
        vgroups_IndexName[groups.index] = groups.name
    data = {}  # vert_indices, [(vgroup_index, weights)]
    for v in me_source.vertices:
        vg = v.groups
        vi = v.index
        if len(vg) > 0:
            vgroup_collect = []
            for i in range(0, len(vg)):
                vgroup_collect.append((vg[i].group, vg[i].weight))
            data[vi] = vgroup_collect
    # write data to target
    if ob != active:
        # add missing vertex groups
        for vgroup_name in vgroups_IndexName.values():
            # check if group already exists...
            already_present = 0
            for i in range(0, len(ob.vertex_groups)):
                if ob.vertex_groups[i].name == vgroup_name:
                    already_present = 1
            # ... if not, then add
            if already_present == 0:
                ob.vertex_groups.new(name=vgroup_name)
        # write weights
        for v in me_target.vertices:
            for vi_source, vgroupIndex_weight in data.items():
                if v.index == vi_source:

                    for i in range(0, len(vgroupIndex_weight)):
                        groupName = vgroups_IndexName[vgroupIndex_weight[i][0]]
                        groups = ob.vertex_groups
                        for vgs in range(0, len(groups)):
                            if groups[vgs].name == groupName:
                                groups[vgs].add((v.index,),
                                                vgroupIndex_weight[i][1], "REPLACE")
    return('INFO', "Weights copied")


object_copies = (
    ('obj_vis_loc', "Location",
     "Copy Location from Active to Selected", obVisLoc),
    ('obj_vis_rot', "Rotation",
     "Copy Rotation from Active to Selected", obVisRot),
    ('obj_vis_sca', "Scale",
     "Copy Scale from Active to Selected", obVisSca),
    ('obj_drw', "Draw Options",
     "Copy Draw Options from Active to Selected", obDrw),
    ('obj_ofs', "Time Offset",
     "Copy Time Offset from Active to Selected", obOfs),
    ('obj_dup', "Dupli",
     "Copy Dupli from Active to Selected", obDup),
    ('obj_col', "Object Color",
     "Copy Object Color from Active to Selected", obCol),
    ('obj_lok', "Protected Transform",
     "Copy Protected Transforms from Active to Selected", obLok),
    ('obj_con', "Object Constraints",
     "Copy Object Constraints from Active to Selected", obCon),
    ('obj_idx', "Pass Index",
     "Copy Pass Index from Active to Selected", obIdx),
    ('obj_mod', "Modifiers",
     "Copy Modifiers from Active to Selected", obMod),
    ('obj_wei', "Vertex Weights",
     "Copy vertex weights based on indices", obWei),
    ('obj_grp', "Group Links",
     "Copy selected into active object's groups", obGrp)
)


@classmethod
def object_poll_func(cls, context):
    return (len(context.selected_objects) > 1)


def object_invoke_func(self, context, event):
    wm = context.window_manager
    wm.invoke_props_dialog(self)
    return {'RUNNING_MODAL'}

object_ops = []
genops(object_copies, object_ops, "object.copy_", object_poll_func, obLoopExec)

classes = (
    CopySelectedPoseConstraints,
    VIEW3D_MT_posecopypopup,
    *object_ops,
)

# def register():
#     from bpy.utils import register_class
#     for cls in classes:
#         register_class(cls)

# def unregister():
#     from bpy.utils import unregister_class
#     for cls in classes:
#         unregister_class(cls)

# if __name__ == "__main__":
#     register()
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

# def pLocLocExec(bone, active, context):
#     bone.location = active.location


# def pLocRotExec(bone, active, context):
#     rotcopy(bone, active.matrix_basis.to_3x3())


# def pLocScaExec(bone, active, context):
#     bone.scale = active.scale


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


# def pDrwExec(bone, active, context):
#     bone.custom_shape = active.custom_shape
#     bone.use_custom_shape_bone_size = active.use_custom_shape_bone_size
#     bone.custom_shape_scale = active.custom_shape_scale
#     bone.bone.show_wire = active.bone.show_wire


# def pLokExec(bone, active, context):
#     for index, state in enumerate(active.lock_location):
#         bone.lock_location[index] = state
#     for index, state in enumerate(active.lock_rotation):
#         bone.lock_rotation[index] = state
#     bone.lock_rotations_4d = active.lock_rotations_4d
#     bone.lock_rotation_w = active.lock_rotation_w
#     for index, state in enumerate(active.lock_scale):
#         bone.lock_scale[index] = state


# def pConExec(bone, active, context):
#     for old_constraint in active.constraints.values():
#         new_constraint = bone.constraints.new(old_constraint.type)
#         generic_copy(old_constraint, new_constraint)


# def pIKsExec(bone, active, context):
#     generic_copy(active, bone, "ik_")


# def pBBonesExec(bone, active, context):
#     object = active.id_data
#     generic_copy(
#         object.data.bones[active.name],
#         object.data.bones[bone.name],
#         "bbone_")


pose_copies = (
    # ('pose_loc_loc', "Local Location",
    #  "Copy Location from Active to Selected", pLocLocExec),
    # ('pose_loc_rot', "Local Rotation",
    #  "Copy Rotation from Active to Selected", pLocRotExec),
    # ('pose_loc_sca', "Local Scale",
    #  "Copy Scale from Active to Selected", pLocScaExec),
    ('pose_vis_loc', "Visual Location",
     "Copy Location from Active to Selected", pVisLocExec),
    ('pose_vis_rot', "Visual Rotation",
     "Copy Rotation from Active to Selected", pVisRotExec),
    ('pose_vis_sca', "Visual Scale",
     "Copy Scale from Active to Selected", pVisScaExec)
    # ('pose_drw', "Bone Shape",
    #  "Copy Bone Shape from Active to Selected", pDrwExec),
    # ('pose_lok', "Protected Transform",
    #  "Copy Protected Transforms from Active to Selected", pLokExec)
)

@classmethod
def pose_poll_func(cls, context):
    return(context.mode == 'POSE')


def pose_invoke_func(self, context, event):
    wm = context.window_manager
    wm.invoke_props_dialog(self)
    return {'RUNNING_MODAL'}

pose_ops = []  # list of pose mode copy operators
genops(pose_copies, pose_ops, "pose.copy_", pose_poll_func, pLoopExec)

# def obLoopExec(self, context, funk):
#     """Loop over selected objects and execute funk on them"""
#     active = context.active_object
#     selected = context.selected_objects[:]
#     selected.remove(active)
#     for obj in selected:
#         msg = funk(obj, active, context)
#     if msg:
#         self.report({msg[0]}, INFO_MESSAGE + msg[1])


# def world_to_basis(active, ob, context):
#     """put world coords of active as basis coords of ob"""
#     local = ob.parent.matrix_world.inverted() @ active.matrix_world
#     P = ob.matrix_basis @ ob.matrix_local.inverted()
#     mat = P @ local
#     return(mat)


# The following functions are used to copy attributes from
# active to selected object

# def obLoc(ob, active, context):
#     ob.location = active.location


# def obRot(ob, active, context):
#     rotcopy(ob, active.matrix_local.to_3x3())


# def obSca(ob, active, context):
#     ob.scale = active.scale


# def obVisLoc(ob, active, context):
#     if ob.parent:
#         mat = world_to_basis(active, ob, context)
#         ob.location = mat.to_translation()
#     else:
#         ob.location = active.matrix_world.to_translation()
#     return('INFO', "Object location copied")


# def obVisRot(ob, active, context):
#     if ob.parent:
#         mat = world_to_basis(active, ob, context)
#         rotcopy(ob, mat.to_3x3())
#     else:
#         rotcopy(ob, active.matrix_world.to_3x3())
#     return('INFO', "Object rotation copied")


# def obVisSca(ob, active, context):
#     if ob.parent:
#         mat = world_to_basis(active, ob, context)
#         ob.scale = mat.to_scale()
#     else:
#         ob.scale = active.matrix_world.to_scale()
#     return('INFO', "Object scale copied")


# def obDrw(ob, active, context):
#     ob.display_type = active.display_type
#     ob.show_axis = active.show_axis
#     ob.show_bounds = active.show_bounds
#     ob.display_bounds_type = active.display_bounds_type
#     ob.show_name = active.show_name
#     ob.show_texture_space = active.show_texture_space
#     ob.show_transparent = active.show_transparent
#     ob.show_wire = active.show_wire
#     ob.show_in_front = active.show_in_front
#     ob.empty_display_type = active.empty_display_type
#     ob.empty_display_size = active.empty_display_size


# def obOfs(ob, active, context):
#     ob.time_offset = active.time_offset
#     return('INFO', "Time offset copied")


# def obLok(ob, active, context):
#     for index, state in enumerate(active.lock_location):
#         ob.lock_location[index] = state
#     for index, state in enumerate(active.lock_rotation):
#         ob.lock_rotation[index] = state
#     ob.lock_rotations_4d = active.lock_rotations_4d
#     ob.lock_rotation_w = active.lock_rotation_w
#     for index, state in enumerate(active.lock_scale):
#         ob.lock_scale[index] = state
#     return('INFO', "Transform locks copied")

# object_copies = (
#     ('obj_vis_loc', "Location",
#      "Copy Location from Active to Selected", obVisLoc),
#     ('obj_vis_rot', "Rotation",
#      "Copy Rotation from Active to Selected", obVisRot),
#     ('obj_vis_sca', "Scale",
#      "Copy Scale from Active to Selected", obVisSca),
#     ('obj_lok', "Protected Transform",
#      "Copy Protected Transforms from Active to Selected", obLok)
# )


@classmethod
def object_poll_func(cls, context):
    return (len(context.selected_objects) > 1)


def object_invoke_func(self, context, event):
    wm = context.window_manager
    wm.invoke_props_dialog(self)
    return {'RUNNING_MODAL'}

# object_ops = []
# genops(object_copies, object_ops, "object.copy_", object_poll_func, obLoopExec)

classes = (*pose_ops,)

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
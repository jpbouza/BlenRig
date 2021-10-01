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

pose_copies = (
    ('pose_vis_loc', "Visual Location",
     "Copy Location from Active to Selected", pVisLocExec),
    ('pose_vis_rot', "Visual Rotation",
     "Copy Rotation from Active to Selected", pVisRotExec),
    ('pose_vis_sca', "Visual Scale",
     "Copy Scale from Active to Selected", pVisScaExec)
)

@classmethod
def pose_poll_func(cls, context):
    return(context.mode == 'POSE')

pose_ops = []  # list of pose mode copy operators
genops(pose_copies, pose_ops, "pose.copy_", pose_poll_func, pLoopExec)

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
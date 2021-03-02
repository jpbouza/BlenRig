import bpy
from . utils import *
from . operator import *

def reproportion_on(context):
    # 0. Make sure Armature is active and in Pose Mode.
    if context.mode != 'POSE':
        set_mode('OBJECT')
        # set_active_object(context, operator.arm_obj)
        set_mode('POSE')

    # 1. Set Armature to Reproportion mode
    set_reproportion_on(context)
    unhide_all_bones(context)


def reproportion_off(context):
    # 0. Make sure Armature is active and in Pose Mode.
    if context.mode != 'POSE':
        set_mode('OBJECT')
        set_active_object(context, operator.arm_obj)
        set_mode('POSE')

    # 1. Set Armature to Reproportion mode
    set_reproportion_off(context)
    unhide_all_bones(context)

def frame_bones(context, *bone_names):
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bone_names)
    frame_selected()
    deselect_all_pose_bones(context)

#### REPROPORTION STEPS ####

def Reprop_Master_Torso(operator,context):
    reproportion_on(context)

    # 1. Side View.
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # 2. Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    # 3. hide all bones but master_torso_str.
    select_all_pose_bones(context)
    deselect_pose_bones(context, "master_torso_str")
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, 'master_torso_str')

    # 5. Se selecciona “master_torso”.
    select_pose_bone(context, 'master_torso_str')

def Reprop_Spine(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # 2. Adjust view to Bones.
    frame_bones(context, "pelvis_str", "head_str")

    # 3.
    bones = (
        "pelvis_str",
        "spine_ctrl_1_str", "spine_ctrl_2_str", "spine_ctrl_3_str", "spine_ctrl_4_str",
        "spine_1_def", "spine_2_def", "spine_3_def", "pelvis_def"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "pelvis_str", "spine_ctrl_1_str", "spine_ctrl_2_str", "spine_ctrl_3_str", "spine_ctrl_4_str")

def Reprop_Neck(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # 2. Adjust view to Bones.
    frame_bones(context, "spine_ctrl_4_str", "head_str")

    # 3.
    bones = (
        "spine_ctrl_4_str",
        "neck_ctrl_1_str", "neck_ctrl_2_str", "neck_ctrl_3_str", "neck_ctrl_4_str", "head_str",
        "neck_1_def", "neck_2_def", "neck_3_def", "head_def_mstr"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "neck_ctrl_4_str", "spine_ctrl_4_str", "neck_ctrl_2_str", "neck_ctrl_3_str", "head_str")

def Reprop_Head(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # 2. Adjust view to Bones.
    frame_bones(context, "neck_ctrl_4_str", "head_str")

    # 3.
    bones = (
        "head_mid_1_str", "head_mid_2_str",
        "head_def_1", "head_def_2", "head_def_3"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "head_mid_1_str", "head_mid_2_str")

def Reprop_Sole_Side(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # 2. Adjust view to Bones.
    frame_bones(context, "ankle_str_L", "sole_str_L")

    # 3.
    bones = (
        "sole_str_L", "sole_str_R",
        "foot_roll_ctrl_L", "foot_roll_ctrl_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "sole_str_L", "sole_str_L", "foot_roll_ctrl_L", "foot_roll_ctrl_R")

    # 5. Select Sole
    select_pose_bone(context, "sole_str_L")

def Reprop_Sole_Bot(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('BOTTOM')

    # 2. Adjust view to Bones.
    frame_bones(context, "foot_roll_ctrl_L", "foot_roll_ctrl_R", "foot_ctrl_frame_L", "foot_ctrl_frame_R")

    # 3.
    bones = (
        "sole_str_L", "sole_str_R",
        "foot_ctrl_frame_L", "foot_ctrl_frame_R",
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "sole_str_L", "sole_str_R", "foot_ctrl_frame_L", "foot_ctrl_frame_R")

    # 5. Select Sole
    select_pose_bone(context, "sole_str_L")

def Reprop_Foot_Side_Rolls(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('BOTTOM')

    # 2. Adjust view to Bones.
    frame_bones(context, "foot_roll_ctrl_L", "foot_roll_ctrl_R", "foot_ctrl_frame_L", "foot_ctrl_frame_R")

    # 3.
    bones = (
        "foot_side_roll_out_L", "foot_side_roll_out_R", "foot_side_roll_in_L", "foot_side_roll_in_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "foot_side_roll_out_L", "foot_side_roll_out_R", "foot_side_roll_in_L", "foot_side_roll_in_R")

    # 5. Select Sole
    select_pose_bone(context, "sole_str_L")

def Reprop_Leg_Front(operator, context):
    reproportion_on(context)

    # 1. Side View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # 2. Adjust view to Bones.
    frame_bones(context, "master_torso_str", "master")

    # 3.
    bones = (
        "pelvis_str_L", "pelvis_str_R", "knee_str_L", "knee_str_R", "knee_pole_str_L", "knee_pole_str_R", "knee_line_L", "knee_line_R",
        "ankle_str_L", "ankle_str_R", "foot_str_L", "foot_str_R", "toe_str_1_L", "toe_str_1_R", "toe_str_2_L", "toe_str_2_R",
        "thigh_def_L", "thigh_def_R", "thigh_twist_def_L", "thigh_twist_def_R", "shin_def_L", "shin_def_L", "shin_twist_def_L", "shin_twist_def_L",
        "foot_def_L", "foot_def_R", "foot_toe_1_def_L", "foot_toe_1_def_R", "foot_toe_2_def_L", "foot_toe_2_def_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # 4. Add OpenGL Highlight to bones
    operator.draw_bones(context, "pelvis_str_L", "pelvis_str_R", "knee_str_L", "knee_str_R",
    "ankle_str_L", "ankle_str_R", "foot_str_L", "foot_str_R", "toe_str_1_L", "toe_str_1_R", "toe_str_2_L", "toe_str_2_R"
    )

    # 5. Select Sole
    select_pose_bone(context, "sole_str_L")

def step_40(operator, context):
    # 0. Asegurarse de estar en pose mode y armature activo.
    if context.mode != 'POSE':
        set_mode('OBJECT')
        set_active_object(context, operator.arm_obj)
        set_mode('POSE')

    # 1. Se ocultan todos los huesos menos “eye_socket_mstr_str_L” y “eye_socket_mstr_str_R”.
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, "eye_socket_mstr_str_L", "eye_socket_mstr_str_R")
    hide_selected_pose_bones(context)

    # 2. Enfocar huesos de la cara.
    deselect_all_pose_bones(context)
    select_pose_bones(context, "eye_socket_mstr_str_L", "eye_socket_mstr_str_R")
    frame_selected()
    deselect_pose_bones(context, "eye_socket_mstr_str_L", "eye_socket_mstr_str_R")

    # 3. Se pone la vista en fron view (numpad 1).
    set_viewpoint('FRONT')

    # 4. Se resetean los puntos de gl.
    operator.draw_bones(context)

    # 5. Sacar de pose e ir a object para que el user vaya a seleccionar los ojos...
    set_mode('OBJECT')

def step_41(operator, context):
    # 1. Seleccionar automáticamente el armature en el que estábamos antes.
    if context.mode != 'OBJECT':
        set_mode('OBJECT')
    set_active_object(context, operator.arm_obj)
    set_mode('POSE')

    # 2. Se ocultan todos los huesos menos.
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context,
        'eye_socket_mstr_str_L',
        'eyelid_up_line_def_3_L',
        'eyelid_up_line_def_2_L',
        'eyelid_up_line_def_4_L',
        'eyelid_low_line_def_3_L',
        'eyelid_low_line_def_2_L',
        'eyelid_low_line_def_4_L',
        'eyelid_up_line_def_1_L',
        'eyelid_low_line_def_1_L',
        'eyelid_up_def_2_L',
        'eyelid_up_def_3_L',
        'eyelid_up_def_1_L',
        'eyelid_out_def_L',
        'eyelid_low_def_3_L',
        'eyelid_low_def_2_L',
        'eyelid_low_def_1_L',
        'eyelid_ctrl_in_mstr_L',
        'eyelid_ctrl_out_mstr_L',
        'eye_socket_mstr_str_R',
        'eyelid_up_def_2_bbone_out_R',
        'eyelid_up_line_def_3_R',
        'eyelid_up_def_1_bbone_out_R',
        'eyelid_up_line_def_2_R',
        'eyelid_up_def_3_bbone_out_R',
        'eyelid_up_line_def_4_R',
        'eyelid_up_line_def_4_bbone_out_R',
        'eyelid_low_def_2_bbone_out_R',
        'eyelid_low_line_def_3_R',
        'eyelid_low_def_1_bbone_out_R',
        'eyelid_low_line_def_2_R',
        'eyelid_low_def_3_bbone_out_R',
        'eyelid_low_line_def_4_R',
        'eyelid_low_line_def_4_bbone_out_R',
        'eyelid_up_line_def_1_R',
        'eyelid_up_line_def_1_bezier_in_R',
        'eyelid_low_line_def_1_R',
        'eyelid_low_line_1_bezier_in_R',
        'eyelid_up_def_2_R',
        'eyelid_up_def_3_R',
        'eyelid_up_def_1_R',
        'eyelid_in_def_R',
        'eyelid_out_def_R',
        'eyelid_low_def_3_R',
        'eyelid_low_def_2_R',
        'eyelid_low_def_1_R',
        'eyelid_ctrl_in_mstr_R',
        'eyelid_in_def_bbone_out_R',
        'eyelid_ctrl_out_mstr_R',
        'eyelid_out_def_bbone_out_R',
        'eyelid_rim_up_def_3_L',
        'eyelid_rim_up_def_2_L',
        'eyelid_rim_up_def_4_L',
        'eyelid_rim_up_def_1_L',
        'eyelid_rim_up_def_3_R',
        'eyelid_rim_up_def_2_R',
        'eyelid_rim_up_def_4_R',
        'eyelid_rim_up_def_1_R',
        'eyelid_rim_low_def_3_L',
        'eyelid_rim_low_def_2_L',
        'eyelid_rim_low_def_4_L',
        'eyelid_rim_low_def_1_L',
        'eyelid_rim_low_def_3_R',
        'eyelid_rim_low_def_2_R',
        'eyelid_rim_low_def_4_R',
        'eyelid_rim_low_def_1_R',
        'eyelid_up_ctrl_2_str_L',
        'eyelid_up_ctrl_1_str_L',
        'eyelid_up_ctrl_3_str_L',
        'eyelid_low_ctrl_2_str_L',
        'eyelid_low_ctrl_1_str_L',
        'eyelid_low_ctrl_3_str_L',
        'eyelid_up_ctrl_2_str_R',
        'eyelid_up_ctrl_1_str_R',
        'eyelid_up_ctrl_3_str_R',
        'eyelid_low_ctrl_2_str_R',
        'eyelid_low_ctrl_1_str_R',
        'eyelid_low_ctrl_3_str_R'
    )
    hide_selected_pose_bones(context)

    bones = (
        'eyelid_ctrl_in_mstr_L',
        'eyelid_ctrl_out_mstr_L',
        'eyelid_up_ctrl_2_str_L',
        'eyelid_up_ctrl_1_str_L',
        'eyelid_up_ctrl_3_str_L',
        'eyelid_low_ctrl_2_str_L',
        'eyelid_low_ctrl_1_str_L',
        'eyelid_low_ctrl_3_str_L'
    )

    # 3. “eye_socket_mstr_str_L” es posicionado en el cursor (operador Selection to cursor)
    # # 4. “eye_socket_mstr_str_R” también asume su posición correcta a través de un operador de X-Mirror de la pose de su contraparte izquierda.
    deselect_all_pose_bones(context)
    toggle_pose_x_mirror(context, True)
    select_pose_bone(context, "eye_socket_mstr_str_L")
    snap_selected_to_cursor()

    # 5. Enfocar huesos de la cara.
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bones)
    frame_selected()
    deselect_pose_bones(context, *bones)

    # 6. Se agrega un Highlight OpenGL a:
    operator.draw_bones(context, *bones)

    # 7. Se pone la vista en front view (numpad 1).
    set_viewpoint('FRONT')

def step_42(operator, context):
    # 0. Asegurarse de estar en pose mode y armature activo.
    if context.mode != 'POSE':
        set_mode('OBJECT')
        set_active_object(context, operator.arm_obj)
        set_mode('POSE')

    # 1. Se ocultan todos los huesos menos “master_torso”.
    unhide_bones(context, 'master_torso')
    select_all_pose_bones(context)
    #frame_selected()
    deselect_pose_bone(context, 'master_torso')
    hide_selected_pose_bones(context)

    # 2. Se agrega un Highlight OpenGl a “master_torso”. Puede ser un círculo opengl, una forma que se dibuje todo el tiempo sobre el hueso.
    operator.draw_bones(context, 'master_torso')

    # 3. Se pone la vista en front view (numpad 1).
    # set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # 4. Enfocar huesos de la espina.
    bones = (
        "pelvis_str",
        "spine_ctrl_1_str", "spine_ctrl_2_str", "spine_ctrl_3_str", "spine_ctrl_4_str",
        "neck_ctrl_2_str", "neck_ctrl_3_str", "head_str",
        "pelvis_def",
        "head_def_mstr",
        "neck_1_def", "neck_2_def", "neck_3_def",
        "spine_1_def", "spine_2_def", "spine_3_def"
    )
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bones)
    frame_selected()
    deselect_pose_bones(context, *bones)

    # 5. Se selecciona “master_torso”.
    select_pose_bone(context, 'master_torso')

    # 6. Empezar a mover hueso. Constraint en eje Z, orientacion de mundo.
    move_global_z()
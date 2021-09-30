import bpy
from .. utils import *

def reproportion_on(context):
    # 0. Make sure Armature is active and in Pose Mode.
    go_blenrig_pose_mode(context)

    # Set Armature to Reproportion mode
    set_reproportion_on(context)
    unhide_all_bones(context)

    #Lock Object Mode On
    bpy.context.scene.tool_settings.lock_object_mode = True

    #Lock Center Bones
    guide_props = bpy.context.scene.blenrig_guide
    guide_props.guide_lock_center_bones = True

    #Make Deform Bones not Selectable
    exclude_list = ['foot_ctrl_frame_L', 'foot_ctrl_frame_R']
    for b in guide_props.arm_obj.pose.bones:
        if b.name not in exclude_list:
            if b.lock_location[:] == (True, True, True) and b.lock_rotation[:] == (True, True, True) and b.lock_scale[:] == (True, True, True):
                b.bone.hide_select = True

    # Turn Off Lattice Modifiers
    lattice_objects = collect_lattice_objects()
    for lattice in lattice_objects:
        for ob in bpy.data.objects:
            if hasattr(ob, 'modifiers'):
                for M in ob.modifiers:
                    if M.type == 'LATTICE' and M.object == lattice:
                        M.show_viewport = False

def reproportion_off(context):
    # 0. Make sure Armature is active and in Pose Mode.
    go_blenrig_pose_mode(context)

    # Set Armature to Reproportion mode
    set_reproportion_off(context)
    unhide_all_bones(context)

def frame_bones(context, *bone_names):
    deselect_all_pose_bones(context)
    select_pose_bones(context, *bone_names)
    frame_selected()
    deselect_all_pose_bones(context)

def select_armature(context):
    # Select previously active Armature
    go_blenrig_pose_mode(context)

#### REPROPORTION STEPS ####
def Reprop_Intro(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Intro'


def Reprop_Symmetry(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Symmetry'

    reproportion_on(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

def Reprop_Master(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Master'

    reproportion_on(context)

    # Front View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'master')

    # Se selecciona “master_torso”.
    select_pose_bone(context, 'master')

def Reprop_Master_Torso(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Master_Torso'

    reproportion_on(context)

    # Set View.
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    # hide all bones but master_torso_str.
    bones = ("master_torso_str", "master_torso_str")

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'master_torso_str')

    # Se selecciona “master_torso”.
    select_pose_bone(context, 'master_torso_str')

def Reprop_Spine(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Spine'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Adjust view to Bones.
    frame_bones(context, "pelvis_str", "head_str")

    #
    bones = (
        "pelvis_str",
        "spine_ctrl_1_str", "spine_ctrl_2_str", "spine_ctrl_3_str", "spine_ctrl_4_str",
        "spine_1_def", "spine_2_def", "spine_3_def", "pelvis_def"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "pelvis_str", "spine_ctrl_1_str", "spine_ctrl_2_str", "spine_ctrl_3_str", "spine_ctrl_4_str")

def Reprop_Spine_Line(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Spine_Line'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Adjust view to Bones.
    frame_bones(context, "spine_line")

    #
    bones = (
        "spine_1_def", "spine_2_def", "spine_3_def", 'spine_line'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "spine_line")

def Reprop_Neck(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Neck'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "spine_ctrl_4_str", "head_str")

    #
    bones = (
        "neck_ctrl_1_str", "neck_ctrl_2_str", "neck_ctrl_3_str", "neck_ctrl_4_str", "head_str",
        "neck_1_def", "neck_2_def", "neck_3_def", "head_def_mstr"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "neck_ctrl_4_str", "neck_ctrl_2_str", "neck_ctrl_3_str", "head_str")

def Reprop_Head(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Head'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "neck_ctrl_4_str", "head_str")

    #
    bones = (
        "head_mid_1_str", "head_mid_2_str",
        "head_def_1", "head_def_2", "head_def_3"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "head_mid_1_str", "head_mid_2_str")

def Reprop_Head_Toon(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Head_Toon'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "neck_ctrl_4_str", "head_str")

    #
    bones = (
        "face_toon_low", "face_toon_mid", "face_toon_up"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "face_toon_low", "face_toon_mid", "face_toon_up")


def Reprop_Breasts_Pecs(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Breasts_Pecs'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(45, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, "breast_ctrl_L", "breast_ctrl_R")

    #
    bones = (
        "breast_ctrl_L", "breast_ctrl_R", "breast_tip_L", "breast_tip_R", "breast_def_L", "breast_def_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "breast_ctrl_L", "breast_ctrl_R", "breast_tip_L", "breast_tip_R")

def Reprop_Body_Lattice(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Body_Lattice'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "chest_ctrl", "belly_ctrl", "butt_ctrl")

    #
    bones = (
        "chest_ctrl", "belly_ctrl", "butt_ctrl"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "chest_ctrl", "belly_ctrl", "butt_ctrl")


def Reprop_Sole_Side(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Sole_Side'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "ankle_str_L", "sole_str_L")

    #
    bones = (
        "sole_str_L", "sole_str_R",
        "foot_roll_ctrl_L", "foot_roll_ctrl_R", "sole_pivot_point_L", "sole_pivot_point_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "sole_str_L", "sole_str_L", "foot_roll_ctrl_L", "foot_roll_ctrl_R", "sole_pivot_point_L", "sole_pivot_point_R")

    # Select Sole
    select_pose_bone(context, "sole_str_L")

    #Unlock Foot Roll Location
    context.pose_object.pose.bones['foot_roll_ctrl_L'].lock_location[1] = False
    context.pose_object.pose.bones['foot_roll_ctrl_R'].lock_location[1] = False

def Reprop_Sole_Bottom(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Sole_Bottom'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('BOTTOM')

    #Make Roll Frame Selectable
    try:
        bpy.context.scene.blenrig_guide.arm_obj.pose.bones['foot_ctrl_frame_L'].bone.hide_select = False
        bpy.context.scene.blenrig_guide.arm_obj.pose.bones['foot_ctrl_frame_R'].bone.hide_select = False
    except:
        pass

    # Adjust view to Bones.
    frame_bones(context, "foot_roll_ctrl_L", "foot_roll_ctrl_R", "foot_ctrl_frame_L", "foot_ctrl_frame_R")

    #
    bones = (
        "sole_str_L", "sole_str_R",
        "foot_ctrl_frame_L", "foot_ctrl_frame_R", "sole_pivot_point_L", "sole_pivot_point_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "sole_str_L", "sole_str_R", "foot_ctrl_frame_L", "foot_ctrl_frame_R", "sole_pivot_point_L", "sole_pivot_point_R")

    # Select Sole
    select_pose_bone(context, "sole_str_L")

    #Unlock Foot Ctrl Frame
    context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_location[0] = False
    context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_location[0] = False
    context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_location[1] = False
    context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_location[1] = False
    context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_location[2] = False
    context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_location[2] = False
    context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_scale[0] = False
    context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_scale[0] = False
    context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_scale[1] = False
    context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_scale[1] = False
    context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_scale[2] = False
    context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_scale[2] = False

def Reprop_Foot_Side_Rolls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Foot_Side_Rolls'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('BOTTOM')

    # Adjust view to Bones.
    frame_bones(context, "foot_roll_ctrl_L", "foot_roll_ctrl_R", "foot_ctrl_frame_L", "foot_ctrl_frame_R")

    #
    bones = (
        "foot_side_roll_out_L", "foot_side_roll_out_R", "foot_side_roll_in_L", "foot_side_roll_in_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "foot_side_roll_out_L", "foot_side_roll_out_R", "foot_side_roll_in_L", "foot_side_roll_in_R")

    # Select Sole
    select_pose_bone(context, "sole_str_L")

def Reprop_Legs(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Legs'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(45, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, "master_torso_str", "master")

    #
    bones = (
        "pelvis_str_L", "pelvis_str_R", "knee_str_L", "knee_str_R", "knee_pole_str_L", "knee_pole_str_R", "knee_line_L", "knee_line_R",
        "ankle_str_L", "ankle_str_R",
        "thigh_def_L", "thigh_def_R", "thigh_twist_def_L", "thigh_twist_def_R", "shin_def_L", "shin_def_R", "shin_twist_def_L", "shin_twist_def_R",
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "pelvis_str_L", "pelvis_str_R", "knee_str_L", "knee_str_R",
    "ankle_str_L", "ankle_str_R"
    )

    # Select Sole
    select_pose_bone(context, "knee_str_L")

def Reprop_Feet(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Feet'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(45, 'ORBITRIGHT')
    orbit_viewpoint(12, 'ORBITDOWN')

    # Adjust view to Bones.
    frame_bones(context, "ankle_str_L", "sole_str_L")

    #
    bones = (
        "foot_str_L", "foot_str_R", "toe_str_1_L", "toe_str_1_R", "toe_str_2_L", "toe_str_2_R",
        "foot_def_L", "foot_def_R", "foot_toe_1_def_L", "foot_toe_1_def_R", "foot_toe_2_def_L", "foot_toe_2_def_R"
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, "foot_str_L", "foot_str_R", "toe_str_1_L", "toe_str_1_R", "toe_str_2_L", "toe_str_2_R"
    )

def Reprop_Toes(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Toes'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, "ankle_str_L", "sole_str_L")

    #
    bones = (
        'toe_lit_str_1_L', 'toe_fourth_str_1_L', 'toe_mid_str_1_L', 'toe_big_str_1_L', 'toe_ind_str_1_L', 'toe_big_str_2_L', 'toe_mid_str_2_L', 'toe_fourth_str_2_L', 'toe_lit_str_2_L', 'toe_ind_str_2_L',
        'toe_big_str_3_L', 'toe_mid_str_3_L', 'toe_mid_str_4_L', 'toe_fourth_str_3_L', 'toe_fourth_str_4_L', 'toe_lit_str_3_L', 'toe_ind_str_3_L', 'toe_ind_str_4_L', 'toe_lit_str_4_L', 'toe_fourth_str_5_L', 'toe_mid_str_5_L',
        'toe_big_str_4_L', 'toe_ind_str_5_L', 'toe_lit_str_1_R', 'toe_fourth_str_1_R', 'toe_mid_str_1_R', 'toe_big_str_1_R', 'toe_ind_str_1_R', 'toe_big_str_2_R', 'toe_mid_str_2_R', 'toe_fourth_str_2_R', 'toe_lit_str_2_R', 'toe_ind_str_2_R',
        'toe_big_str_3_R', 'toe_mid_str_3_R', 'toe_mid_str_4_R', 'toe_fourth_str_3_R', 'toe_fourth_str_4_R', 'toe_lit_str_3_R', 'toe_ind_str_3_R', 'toe_ind_str_4_R', 'toe_lit_str_4_R', 'toe_big_str_4_R','toe_fourth_str_5_R', 'toe_mid_str_5_R', 'toe_ind_str_5_R',
        'toe_lit_1_def_R', 'toe_big_1_def_R', 'toe_fourth_1_def_R', 'toe_mid_1_def_R', 'toe_ind_1_def_R', 'toe_big_3_def_R', 'toe_big_2_def_R', 'toe_lit_3_def_R', 'toe_lit_2_def_R', 'toe_fourth_4_def_R',
        'toe_fourth_3_def_R', 'toe_fourth_2_def_R', 'toe_mid_4_def_R', 'toe_mid_3_def_R', 'toe_mid_2_def_R', 'toe_ind_4_def_R', 'toe_ind_3_def_R', 'toe_ind_2_def_R', 'toe_lit_1_def_L', 'toe_big_1_def_L',
        'toe_fourth_1_def_L', 'toe_mid_1_def_L', 'toe_ind_1_def_L', 'toe_lit_3_def_L', 'toe_lit_2_def_L', 'toe_big_3_def_L', 'toe_big_2_def_L', 'toe_fourth_4_def_L', 'toe_fourth_3_def_L', 'toe_fourth_2_def_L',
        'toe_mid_4_def_L', 'toe_mid_3_def_L', 'toe_mid_2_def_L', 'toe_ind_4_def_L', 'toe_ind_3_def_L', 'toe_ind_2_def_L',
        'toes_spread_L', 'toes_spread_R', 'toes_str_1_L', 'toes_str_2_L', 'toes_str_3_L', 'toes_str_1_R', 'toes_str_2_R', 'toes_str_3_R'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    # operator.draw_bones(context, 'toe_lit_str_1_L', 'toe_fourth_str_1_L', 'toe_mid_str_1_L', 'toe_big_str_1_L', 'toe_ind_str_1_L', 'toe_big_str_2_L', 'toe_mid_str_2_L', 'toe_fourth_str_2_L', 'toe_lit_str_2_L', 'toe_ind_str_2_L',
    #     'toe_big_str_3_L', 'toe_mid_str_3_L', 'toe_mid_str_4_L', 'toe_fourth_str_3_L', 'toe_fourth_str_4_L', 'toe_lit_str_3_L', 'toe_ind_str_3_L', 'toe_ind_str_4_L', 'toe_lit_str_4_L', 'toe_fourth_str_5_L', 'toe_mid_str_5_L',
    #     'toe_big_str_4_L', 'toe_ind_str_5_L', 'toe_lit_str_1_R', 'toe_fourth_str_1_R', 'toe_mid_str_1_R', 'toe_big_str_1_R', 'toe_ind_str_1_R', 'toe_big_str_2_R', 'toe_mid_str_2_R', 'toe_fourth_str_2_R', 'toe_lit_str_2_R', 'toe_ind_str_2_R',
    #     'toe_big_str_3_R', 'toe_mid_str_3_R', 'toe_mid_str_4_R', 'toe_fourth_str_3_R', 'toe_fourth_str_4_R', 'toe_lit_str_3_R', 'toe_ind_str_3_R', 'toe_ind_str_4_R', 'toe_lit_str_4_R', 'toe_big_str_4_R','toe_fourth_str_5_R', 'toe_mid_str_5_R', 'toe_ind_str_5_R',
    #     'toes_spread_L', 'toes_spread_R', 'toes_str_1_L', 'toes_str_2_L', 'toes_str_3_L', 'toes_str_1_R', 'toes_str_2_R', 'toes_str_3_R'
    # )
    operator.draw_bones(context, 'toes_spread_L', 'toes_spread_R', 'toes_str_1_L', 'toes_str_2_L', 'toes_str_3_L', 'toes_str_1_R', 'toes_str_2_R', 'toes_str_3_R'
    )

    #Unlock Toes Spread Location
    context.pose_object.pose.bones['toes_spread_L'].lock_location[0] = False
    context.pose_object.pose.bones['toes_spread_L'].lock_location[1] = False
    context.pose_object.pose.bones['toes_spread_L'].lock_location[2] = False
    context.pose_object.pose.bones['toes_spread_L'].lock_rotation[1] = False
    context.pose_object.pose.bones['toes_spread_R'].lock_location[0] = False
    context.pose_object.pose.bones['toes_spread_R'].lock_location[1] = False
    context.pose_object.pose.bones['toes_spread_R'].lock_location[2] = False
    context.pose_object.pose.bones['toes_spread_R'].lock_rotation[1] = False

def Reprop_Arms(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Arms'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(45, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, "master_torso_str", "head_str")

    #
    bones = (
        'elbow_line_R', 'clavi_def_R', 'arm_def_R', 'elbow_line_L', 'clavi_def_L', 'arm_def_L', 'wrist_str_R', 'wrist_str_L', 'elbow_str_L', 'elbow_pole_str_L',
        'elbow_str_R', 'elbow_pole_str_R', 'shoulder_str_R', 'shoulder_str_L', 'clavi_str_R', 'clavi_str_L', 'arm_twist_def_R', 'forearm_twist_def_R', 'forearm_def_R', 'arm_twist_def_L', 'forearm_twist_def_L', 'forearm_def_L',
        'fing_lit_4_def_R', 'fing_lit_3_def_R', 'fing_lit_2_def_R', 'fing_ring_4_def_R', 'fing_ring_3_def_R', 'fing_ring_2_def_R', 'fing_ind_4_def_R',
        'fing_ind_3_def_R', 'fing_ind_2_def_R', 'fing_mid_4_def_R', 'fing_mid_3_def_R', 'fing_mid_2_def_R', 'fing_ind_1_def_R', 'fing_ring_1_def_R', 'fing_lit_1_def_R', 'fing_mid_1_def_R', 'fing_thumb_3_def_R', 'fing_thumb_2_def_R',
        'fing_thumb_1_def_R', 'fing_lit_4_def_L', 'fing_lit_3_def_L', 'fing_lit_2_def_L', 'fing_ring_4_def_L', 'fing_ring_3_def_L', 'fing_ring_2_def_L', 'fing_ind_4_def_L', 'fing_ind_3_def_L', 'fing_ind_2_def_L', 'fing_mid_4_def_L',
        'fing_mid_3_def_L', 'fing_mid_2_def_L', 'fing_ind_1_def_L', 'fing_ring_1_def_L', 'fing_lit_1_def_L', 'fing_mid_1_def_L', 'fing_thumb_3_def_L', 'fing_thumb_2_def_L', 'fing_thumb_1_def_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'wrist_str_R', 'wrist_str_L', 'elbow_str_L', 'elbow_str_R', 'shoulder_str_R', 'shoulder_str_L', 'clavi_str_R', 'clavi_str_L'
    )

def Reprop_Hands(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Hands'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'wrist_str_L', 'hand_str_L')

    #
    bones = (
        'hand_str_R', 'hand_str_L', 'hand_def_R', 'hand_def_L',
        'fing_lit_4_def_R', 'fing_lit_3_def_R', 'fing_lit_2_def_R', 'fing_ring_4_def_R', 'fing_ring_3_def_R', 'fing_ring_2_def_R', 'fing_ind_4_def_R',
        'fing_ind_3_def_R', 'fing_ind_2_def_R', 'fing_mid_4_def_R', 'fing_mid_3_def_R', 'fing_mid_2_def_R', 'fing_ind_1_def_R', 'fing_ring_1_def_R', 'fing_lit_1_def_R', 'fing_mid_1_def_R',
        'fing_lit_4_def_L', 'fing_lit_3_def_L', 'fing_lit_2_def_L', 'fing_ring_4_def_L', 'fing_ring_3_def_L', 'fing_ring_2_def_L', 'fing_ind_4_def_L', 'fing_ind_3_def_L', 'fing_ind_2_def_L', 'fing_mid_4_def_L',
        'fing_mid_3_def_L', 'fing_mid_2_def_L', 'fing_ind_1_def_L', 'fing_ring_1_def_L', 'fing_lit_1_def_L', 'fing_mid_1_def_L',
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'hand_str_R', 'hand_str_L'
    )

def Reprop_Fingers(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Fingers'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(45, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'wrist_str_L', 'hand_str_L')

    #
    bones = (
        'fing_lit_str_1_R', 'fing_ring_str_1_R', 'fing_ind_str_1_R', 'fing_mid_str_1_R', 'fing_thumb_str_1_R', 'fing_thumb_str_2_R', 'fing_thumb_str_3_R', 'fing_thumb_str_4_R', 'fing_lit_str_2_R', 'fing_lit_str_3_R', 'fing_lit_str_4_R',
        'fing_lit_str_5_R', 'fing_ring_str_2_R', 'fing_ring_str_3_R', 'fing_ring_str_4_R', 'fing_ring_str_5_R', 'fing_ind_str_2_R', 'fing_ind_str_3_R', 'fing_ind_str_4_R', 'fing_ind_str_5_R', 'fing_mid_str_2_R', 'fing_mid_str_3_R',
        'fing_mid_str_4_R', 'fing_mid_str_5_R', 'fing_lit_str_1_L', 'fing_ring_str_1_L', 'fing_ind_str_1_L', 'fing_mid_str_1_L', 'fing_thumb_str_1_L', 'fing_thumb_str_2_L', 'fing_thumb_str_3_L', 'fing_thumb_str_4_L', 'fing_lit_str_2_L',
        'fing_lit_str_3_L', 'fing_lit_str_4_L', 'fing_lit_str_5_L', 'fing_ring_str_2_L', 'fing_ring_str_3_L', 'fing_ring_str_4_L', 'fing_ring_str_5_L', 'fing_ind_str_2_L', 'fing_ind_str_3_L', 'fing_ind_str_4_L', 'fing_ind_str_5_L',
        'fing_mid_str_2_L', 'fing_mid_str_3_L', 'fing_mid_str_4_L', 'fing_mid_str_5_L', 'fing_lit_4_def_R', 'fing_lit_3_def_R', 'fing_lit_2_def_R', 'fing_ring_4_def_R', 'fing_ring_3_def_R', 'fing_ring_2_def_R', 'fing_ind_4_def_R',
        'fing_ind_3_def_R', 'fing_ind_2_def_R', 'fing_mid_4_def_R', 'fing_mid_3_def_R', 'fing_mid_2_def_R', 'fing_ind_1_def_R', 'fing_ring_1_def_R', 'fing_lit_1_def_R', 'fing_mid_1_def_R', 'fing_thumb_3_def_R', 'fing_thumb_2_def_R',
        'fing_thumb_1_def_R', 'fing_lit_4_def_L', 'fing_lit_3_def_L', 'fing_lit_2_def_L', 'fing_ring_4_def_L', 'fing_ring_3_def_L', 'fing_ring_2_def_L', 'fing_ind_4_def_L', 'fing_ind_3_def_L', 'fing_ind_2_def_L', 'fing_mid_4_def_L',
        'fing_mid_3_def_L', 'fing_mid_2_def_L', 'fing_ind_1_def_L', 'fing_ring_1_def_L', 'fing_lit_1_def_L', 'fing_mid_1_def_L', 'fing_thumb_3_def_L', 'fing_thumb_2_def_L', 'fing_thumb_1_def_L', 'fing_spread_L', 'fing_spread_R',
        'hand_close_L', 'hand_close_R'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    # operator.draw_bones(context, 'fing_lit_str_1_R', 'fing_ring_str_1_R', 'fing_ind_str_1_R', 'fing_mid_str_1_R', 'fing_thumb_str_1_R', 'fing_thumb_str_2_R', 'fing_thumb_str_3_R', 'fing_thumb_str_4_R', 'fing_lit_str_2_R', 'fing_lit_str_3_R', 'fing_lit_str_4_R',
    #     'fing_lit_str_5_R', 'fing_ring_str_2_R', 'fing_ring_str_3_R', 'fing_ring_str_4_R', 'fing_ring_str_5_R', 'fing_ind_str_2_R', 'fing_ind_str_3_R', 'fing_ind_str_4_R', 'fing_ind_str_5_R', 'fing_mid_str_2_R', 'fing_mid_str_3_R',
    #     'fing_mid_str_4_R', 'fing_mid_str_5_R', 'fing_lit_str_1_L', 'fing_ring_str_1_L', 'fing_ind_str_1_L', 'fing_mid_str_1_L', 'fing_thumb_str_1_L', 'fing_thumb_str_2_L', 'fing_thumb_str_3_L', 'fing_thumb_str_4_L', 'fing_lit_str_2_L',
    #     'fing_lit_str_3_L', 'fing_lit_str_4_L', 'fing_lit_str_5_L', 'fing_ring_str_2_L', 'fing_ring_str_3_L', 'fing_ring_str_4_L', 'fing_ring_str_5_L', 'fing_ind_str_2_L', 'fing_ind_str_3_L', 'fing_ind_str_4_L', 'fing_ind_str_5_L',
    #     'fing_mid_str_2_L', 'fing_mid_str_3_L', 'fing_mid_str_4_L', 'fing_mid_str_5_L','fing_thumb_1_def_L', 'fing_spread_L', 'fing_spread_R', 'hand_close_L', 'hand_close_R'
    # )
    operator.draw_bones(context, 'fing_spread_L', 'fing_spread_R', 'hand_close_L', 'hand_close_R'
    )

    #Unlock Fingers Spread Location
    context.pose_object.pose.bones['fing_spread_L'].lock_location[0] = False
    context.pose_object.pose.bones['fing_spread_L'].lock_location[1] = False
    context.pose_object.pose.bones['fing_spread_L'].lock_location[2] = False
    context.pose_object.pose.bones['fing_spread_L'].lock_rotation[1] = False
    context.pose_object.pose.bones['fing_spread_L'].lock_scale[0] = False
    context.pose_object.pose.bones['fing_spread_L'].lock_scale[2] = False
    context.pose_object.pose.bones['fing_spread_R'].lock_location[0] = False
    context.pose_object.pose.bones['fing_spread_R'].lock_location[1] = False
    context.pose_object.pose.bones['fing_spread_R'].lock_location[2] = False
    context.pose_object.pose.bones['fing_spread_R'].lock_rotation[1] = False
    context.pose_object.pose.bones['fing_spread_R'].lock_scale[0] = False
    context.pose_object.pose.bones['fing_spread_R'].lock_scale[2] = False
    set_locks(['hand_close_L', 'hand_close_R'], False, False, False, False, False, False, False, False, False)

def Reprop_Limbs_Adjust_Shape(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Limbs_Adjust_Shape'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'master', 'head_str')

    #
    bones = (
        'arm_def_R', 'arm_def_L', 'thigh_def_L', 'thigh_def_R', 'thigh_toon_R', 'thigh_twist_def_R', 'shin_def_R', 'shin_toon_R', 'shin_twist_def_R',
        'arm_toon_R', 'arm_twist_def_R', 'forearm_toon_R', 'forearm_twist_def_R', 'forearm_def_R', 'arm_toon_L', 'arm_twist_def_L', 'forearm_toon_L',
        'forearm_twist_def_L', 'forearm_def_L', 'thigh_toon_L', 'thigh_twist_def_L', 'shin_def_L', 'shin_toon_L', 'shin_twist_def_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'arm_toon_R', 'arm_toon_L', 'forearm_toon_L', 'forearm_toon_R', 'thigh_toon_L', 'thigh_toon_R', 'shin_toon_L', 'shin_toon_R'
    )

    deselect_all_pose_bones(context)

def Reprop_Toon_Scale(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Toon_Scale'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'master', 'head_str')

    #
    bones = (
        'neck_2_toon', 'neck_3_toon', 'spine_2_toon', 'spine_3_toon', 'spine_4_toon', 'shoulder_toon_R', 'shoulder_toon_L', 'pelvis_toon', 'spine_1_toon', 'pelvis_toon_R', 'pelvis_toon_L',
        'thigh_toon_R', 'knee_toon_R', 'foot_toon_R', 'toe_3_toon_R', 'toe_2_toon_R', 'toe_1_toon_R', 'shin_toon_R', 'arm_toon_R', 'elbow_toon_R', 'hand_toon_R', 'forearm_toon_R', 'arm_toon_L',
        'elbow_toon_L', 'hand_toon_L', 'forearm_toon_L', 'thigh_toon_L', 'knee_toon_L', 'foot_toon_L', 'toe_3_toon_L', 'toe_2_toon_L', 'toe_1_toon_L', 'shin_toon_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'neck_2_toon', 'neck_3_toon', 'spine_2_toon', 'spine_3_toon', 'spine_4_toon', 'shoulder_toon_R', 'shoulder_toon_L', 'pelvis_toon', 'spine_1_toon', 'pelvis_toon_R', 'pelvis_toon_L',
        'thigh_toon_R', 'knee_toon_R', 'foot_toon_R', 'toe_3_toon_R', 'toe_2_toon_R', 'toe_1_toon_R', 'shin_toon_R', 'arm_toon_R', 'elbow_toon_R', 'hand_toon_R', 'forearm_toon_R', 'arm_toon_L',
        'elbow_toon_L', 'hand_toon_L', 'forearm_toon_L', 'thigh_toon_L', 'knee_toon_L', 'foot_toon_L', 'toe_3_toon_L', 'toe_2_toon_L', 'toe_1_toon_L', 'shin_toon_L'
    )

    deselect_all_pose_bones(context)

    # Show MdefCage
    mdef_cage_objects = collect_cage()
    collect_cage()
    blenrig_temp_link(mdef_cage_objects)
    # Unhide
    collect_cage()
    for ob in mdef_cage_objects:
        ob.hide_viewport = False

    #Set Locks
    set_locks(['neck_2_toon', 'neck_3_toon', 'spine_2_toon', 'spine_3_toon', 'spine_4_toon', 'shoulder_toon_R', 'shoulder_toon_L', 'pelvis_toon', 'spine_1_toon', 'pelvis_toon_R', 'pelvis_toon_L',
        'thigh_toon_R', 'knee_toon_R', 'foot_toon_R', 'toe_3_toon_R', 'toe_2_toon_R', 'toe_1_toon_R', 'shin_toon_R', 'arm_toon_R', 'elbow_toon_R', 'hand_toon_R', 'forearm_toon_R', 'arm_toon_L',
        'elbow_toon_L', 'hand_toon_L', 'forearm_toon_L', 'thigh_toon_L', 'knee_toon_L', 'foot_toon_L', 'toe_3_toon_L', 'toe_2_toon_L', 'toe_1_toon_L', 'shin_toon_L'], True, True, True, True, True, True, False, False, False)

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

def Reprop_Face_Mstr(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Face_Mstr'

    # Seleccionar automáticamente el armature en el que estábamos antes.
    go_blenrig_pose_mode(context)

    reproportion_on(context)

    # Set View.
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "neck_ctrl_4_str")

    bones = ("face_mstr_str", "face_mstr_str")

    # hide all bones but specific ones.
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'face_mstr_str')

    # Se selecciona “master_torso”.
    select_pose_bone(context, 'face_mstr_str')

    # Show FaceRigMesh
    face_rig_objects = collect_facemask()
    collect_facemask()
    blenrig_temp_link(face_rig_objects)

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

def Reprop_Edit_Face(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Edit_Face'

    # Set View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "neck_ctrl_4_str")

    reproportion_on(context)

    bones = ("master", "master")

    # hide all bones but specific ones.
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Se resetean los puntos de gl.
    operator.draw_bones(context)

    hide_all_bones(context)

    #Turn Layers off
    on_layers = [27]
    off_layers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15 ,16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31]
    for l in on_layers:
        context.object.data.layers[l] = True
    for l in off_layers:
        context.object.data.layers[l] = False

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    deselect_all_objects(context)

    # Show FaceRigMesh
    face_rig_objects = collect_facemask()
    collect_facemask()
    blenrig_temp_link(face_rig_objects)

    # Edit FaceRigMesh
    face_rig_objects = collect_facemask()
    collect_facemask()
    for ob in face_rig_objects:
        ob.hide_viewport = False
        context.view_layer.objects.active = ob
        set_mode('EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        ob.data.use_mirror_x = True
        ob.data.use_mirror_topology = True

    #Set Shading to Material to enable transparency
    set_viewport_shading_type('SOLID', 'MATERIAL')

def Reprop_Eye_Loop(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eye_Loop'

    # Set View.
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    reproportion_on(context)

    #Lock Object Mode Off
    bpy.context.scene.tool_settings.lock_object_mode = False

def Reprop_Set_Eyes(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Set_Eyes'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = (
        'eye_socket_mstr_str_L', 'eye_socket_mstr_str_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    deselect_all_pose_bones(context)

    select_pose_bone(context, 'eye_socket_mstr_str_L')

def Reprop_Eyebrows_Main_Ctrl(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eyebrows_Main_Ctrl'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = (
        'brow_def_5_L', 'brow_mstr_L', 'brow_mstr_R', 'brow_def_5_R',
        'frown_def', 'frown_low_def_R', 'brow_def_1_R', 'frown_up_def_R', 'brow_low_def_1_R', 'brow_def_2_R', 'brow_up_def_1_R', 'brow_low_def_2_R', 'brow_def_3_R', 'brow_up_def_2_R',
        'brow_low_def_3_R', 'brow_def_4_R', 'brow_up_def_3_R', 'brow_low_def_4_R', 'brow_up_def_4_R', 'brow_low_def_4_L', 'brow_up_def_4_L', 'frown_low_def_L', 'brow_def_1_L', 'frown_up_def_L', 'brow_low_def_1_L',
        'brow_def_2_L', 'brow_up_def_1_L', 'brow_low_def_2_L', 'brow_def_3_L', 'brow_up_def_2_L', 'brow_low_def_3_L', 'brow_def_4_L', 'brow_up_def_3_L', 'brow_low_def_5_R', 'brow_up_def_5_R', 'brow_low_def_5_L', 'brow_up_def_5_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'brow_mstr_L', 'brow_mstr_R')

    select_pose_bone(context, "brow_mstr_L")

def Reprop_Eyebrows_Curve_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eyebrows_Curve_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = (
        'brow_def_5_L', 'brow_line_L', 'brow_ctrl_in_L', 'brow_ctrl_out_L', 'brow_def_5_R', 'brow_line_R', 'brow_ctrl_in_R', 'brow_ctrl_out_R',
        'frown_ctrl_mstr', 'frown_def', 'frown_low_def_R', 'brow_def_1_R', 'frown_up_def_R', 'brow_low_def_1_R', 'brow_def_2_R', 'brow_up_def_1_R', 'brow_low_def_2_R', 'brow_def_3_R', 'brow_up_def_2_R',
        'brow_low_def_3_R', 'brow_def_4_R', 'brow_up_def_3_R', 'brow_low_def_4_R', 'brow_up_def_4_R', 'brow_low_def_4_L', 'brow_up_def_4_L', 'frown_low_def_L', 'brow_def_1_L', 'frown_up_def_L', 'brow_low_def_1_L',
        'brow_def_2_L', 'brow_up_def_1_L', 'brow_low_def_2_L', 'brow_def_3_L', 'brow_up_def_2_L', 'brow_low_def_3_L', 'brow_def_4_L', 'brow_up_def_3_L', 'brow_low_def_5_R', 'brow_up_def_5_R', 'brow_low_def_5_L', 'brow_up_def_5_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'brow_ctrl_in_L', 'brow_ctrl_out_L', 'brow_ctrl_in_R', 'brow_ctrl_out_R', 'frown_ctrl_mstr'
    )

def Reprop_Eyebrows_Curve(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eyebrows_Curve'

    guide_props = bpy.context.scene.blenrig_guide

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = (
        'brow_def_5_L', 'brow_line_L', 'brow_def_5_R', 'brow_line_R',
        'frown_def', 'frown_low_def_R', 'brow_def_1_R', 'frown_up_def_R', 'brow_low_def_1_R', 'brow_def_2_R', 'brow_up_def_1_R', 'brow_low_def_2_R', 'brow_def_3_R', 'brow_up_def_2_R',
        'brow_low_def_3_R', 'brow_def_4_R', 'brow_up_def_3_R', 'brow_low_def_4_R', 'brow_up_def_4_R', 'brow_low_def_4_L', 'brow_up_def_4_L', 'frown_low_def_L', 'brow_def_1_L', 'frown_up_def_L', 'brow_low_def_1_L',
        'brow_def_2_L', 'brow_up_def_1_L', 'brow_low_def_2_L', 'brow_def_3_L', 'brow_up_def_2_L', 'brow_low_def_3_L', 'brow_def_4_L', 'brow_up_def_3_L', 'brow_low_def_5_R', 'brow_up_def_5_R', 'brow_low_def_5_L', 'brow_up_def_5_L',
        'brow_ctrl_curve_L', 'brow_ctrl_curve_R'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    #Collect Values
    pbones = guide_props.arm_obj.pose.bones
    vert_in = pbones["brow_line_L"].bone.bbone_curveiny
    vert_out = pbones["brow_line_L"].bone.bbone_curveouty
    depth_in = pbones["brow_line_L"].bone.bbone_curveinx
    depth_out = pbones["brow_line_L"].bone.bbone_curveoutx

    #Assign BBone Values
    guide_props.guide_bbone_vertical_curve_in_brows = vert_in
    guide_props.guide_bbone_vertical_curve_out_brows = vert_out
    guide_props.guide_bbone_depth_curve_in_brows = depth_in
    guide_props.guide_bbone_depth_curve_out_brows = depth_out

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'brow_ctrl_curve_L', 'brow_ctrl_curve_R'
    )

def Reprop_Eyebrows_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eyebrows_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = (
        'frown_ctrl', 'brow_ctrl_1_R', 'brow_ctrl_3_R', 'brow_ctrl_4_R', 'brow_ctrl_5_R', 'brow_ctrl_5_L', 'brow_ctrl_1_L', 'brow_ctrl_3_L', 'brow_ctrl_4_L', 'brow_def_5_L', 'brow_def_5_R',
        'frown_def', 'frown_low_def_R', 'brow_def_1_R', 'frown_up_def_R', 'brow_low_def_1_R', 'brow_def_2_R', 'brow_up_def_1_R', 'brow_low_def_2_R', 'brow_def_3_R', 'brow_up_def_2_R', 'brow_ctrl_2_L', 'brow_ctrl_2_R',
        'brow_low_def_3_R', 'brow_def_4_R', 'brow_up_def_3_R', 'brow_low_def_4_R', 'brow_up_def_4_R', 'brow_low_def_4_L', 'brow_up_def_4_L', 'frown_low_def_L', 'brow_def_1_L', 'frown_up_def_L', 'brow_low_def_1_L',
        'brow_def_2_L', 'brow_up_def_1_L', 'brow_low_def_2_L', 'brow_def_3_L', 'brow_up_def_2_L', 'brow_low_def_3_L', 'brow_def_4_L', 'brow_up_def_3_L', 'brow_low_def_5_R', 'brow_up_def_5_R', 'brow_low_def_5_L', 'brow_up_def_5_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'frown_ctrl', 'brow_ctrl_1_R', 'brow_ctrl_3_R', 'brow_ctrl_4_R', 'brow_ctrl_5_R', 'brow_ctrl_5_L', 'brow_ctrl_1_L', 'brow_ctrl_3_L', 'brow_ctrl_4_L', 'brow_ctrl_2_L', 'brow_ctrl_2_R'
    )

def Reprop_Eyelids_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eyelids_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'eyelid_ctrl_out_mstr_L', 'eyelid_ctrl_out_mstr_R')

    #
    bones = (
        'eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_up_line_def_3_L', 'eyelid_low_line_def_1_L', 'eyelid_up_line_def_1_L', 'eyelid_up_line_def_4_L', 'eyelid_low_line_def_4_L',
        'eyelid_up_line_def_2_L', 'eyelid_low_line_def_3_L', 'eyelid_low_line_def_2_L', 'eyelid_low_ctrl_R', 'eyelid_up_ctrl_R', 'eyelid_up_line_def_3_R', 'eyelid_up_line_def_2_R',
        'eyelid_low_line_def_3_R', 'eyelid_low_line_def_2_R', 'eyelid_low_line_def_1_R', 'eyelid_up_line_def_1_R', 'eyelid_up_line_def_4_R', 'eyelid_low_line_def_4_R', 'blink_ctrl_L', 'blink_ctrl_R'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'eyelid_low_ctrl_L', 'eyelid_up_ctrl_L', 'eyelid_low_ctrl_R', 'eyelid_up_ctrl_R', 'blink_ctrl_L', 'blink_ctrl_R')

    #Define Locks
    context.pose_object.pose.bones['blink_ctrl_L'].lock_location[0] = False
    context.pose_object.pose.bones['blink_ctrl_L'].lock_location[1] = False
    context.pose_object.pose.bones['blink_ctrl_R'].lock_location[0] = False
    context.pose_object.pose.bones['blink_ctrl_R'].lock_location[1] = False
    context.pose_object.pose.bones['blink_ctrl_L'].lock_rotation[0] = False
    context.pose_object.pose.bones['blink_ctrl_L'].lock_rotation[2] = False
    context.pose_object.pose.bones['blink_ctrl_L'].lock_scale[0] = False
    context.pose_object.pose.bones['blink_ctrl_L'].lock_scale[1] = False
    context.pose_object.pose.bones['blink_ctrl_R'].lock_rotation[0] = False
    context.pose_object.pose.bones['blink_ctrl_R'].lock_rotation[2] = False
    context.pose_object.pose.bones['blink_ctrl_R'].lock_scale[0] = False
    context.pose_object.pose.bones['blink_ctrl_R'].lock_scale[1] = False

def Reprop_Eyelids_Rim_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Eyelids_Rim_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'eyelid_ctrl_out_mstr_L', 'eyelid_ctrl_out_mstr_R')

    #
    bones = (
        'eyelid_up_rim_ctrl_L', 'eyelid_rim_up_def_1_L', 'eyelid_rim_low_def_1_L', 'eyelid_low_rim_ctrl_L', 'eyelid_up_rim_ctrl_R', 'eyelid_rim_up_def_1_R', 'eyelid_rim_low_def_1_R',
        'eyelid_low_rim_ctrl_R', 'eyelid_rim_low_def_2_L', 'eyelid_rim_low_def_2_R', 'eyelid_rim_low_def_4_R', 'eyelid_rim_low_def_4_L', 'eyelid_rim_low_def_3_L', 'eyelid_rim_low_def_3_R',
        'eyelid_rim_up_def_4_L', 'eyelid_rim_up_def_4_R', 'eyelid_rim_up_def_3_L', 'eyelid_rim_up_def_3_R', 'eyelid_rim_up_def_2_R', 'eyelid_rim_up_def_2_L'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'eyelid_up_rim_ctrl_L', 'eyelid_low_rim_ctrl_L', 'eyelid_up_rim_ctrl_R', 'eyelid_low_rim_ctrl_R')

def Reprop_Face_Toon(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Face_Toon'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'eyelid_ctrl_out_mstr_L', 'eyelid_ctrl_out_mstr_R')

    #
    bones = (
        'toon_brow_L', 'toon_brow_R', 'toon_eye_up_L', 'toon_eye_out_L', 'toon_eye_in_L', 'toon_eye_low_L',
        'lattice_eye_L', 'toon_eye_up_R', 'toon_eye_out_R', 'toon_eye_in_R', 'toon_eye_low_R', 'lattice_eye_R'
    )
    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'toon_brow_L', 'toon_brow_R', 'toon_eye_up_L', 'toon_eye_out_L', 'toon_eye_in_L', 'toon_eye_low_L',
        'lattice_eye_L', 'toon_eye_up_R', 'toon_eye_out_R', 'toon_eye_in_R', 'toon_eye_low_R', 'lattice_eye_R'
    )

def Reprop_Cheek_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Cheek_Ctrls'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'eyelid_ctrl_out_mstr_L', 'eyelid_ctrl_out_mstr_R')

    #
    bones = (
        'cheek_ctrl_L', 'cheek_ctrl_R', 'nose_frown_ctrl_L', 'nose_frown_ctrl_R')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'cheek_ctrl_L', 'cheek_ctrl_R', 'nose_frown_ctrl_L', 'nose_frown_ctrl_R')

    # Unlock Nose Frown Location
    context.pose_object.pose.bones['nose_frown_ctrl_L'].lock_location[0] = False
    context.pose_object.pose.bones['nose_frown_ctrl_R'].lock_location[0] = False
    context.pose_object.pose.bones['nose_frown_ctrl_L'].lock_location[1] = False
    context.pose_object.pose.bones['nose_frown_ctrl_R'].lock_location[1] = False

def Reprop_Nose(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Nose'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = (
        'nose_low_str', 'nose_bridge_ctrl_2', 'nose_up_str', 'nose_bridge_1', 'nose_bridge_2', 'nostril_ctrl_L', 'nostril_ctrl_R', 'nose_tip_ctrl_mstr')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'nose_low_str', 'nose_bridge_ctrl_2', 'nose_up_str', 'nostril_ctrl_L', 'nostril_ctrl_R', 'nose_tip_ctrl_mstr')

def Reprop_Jaw(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Jaw'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('maxi_str_mstr', 'maxi_str_2', 'maxi_str_1')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'maxi_str_1', 'maxi_str_2')

def Reprop_Face_Low(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Face_Low'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('mouth_str_loc_1', 'mouth_str', 'mouth_str_loc_2')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'mouth_str_loc_1', 'mouth_str_loc_2')

def Reprop_Mouth_IK(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Mouth_IK'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('mouth_mstr_ik_pivot', 'mouth_mstr_str')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'mouth_mstr_ik_pivot', 'mouth_mstr_str')

    select_pose_bone(context, 'mouth_mstr_ik_pivot')

def Reprop_Lips_Centers(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Lips_Centers'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('mouth_mstr_up_str', 'mouth_mstr_low_str')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'mouth_mstr_up_str', 'mouth_mstr_low_str')

def Reprop_Mouth_Ctrl(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Mouth_Ctrl'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('mouth_ctrl_str', 'cheek_puff_mstr_R', 'cheek_puff_mstr_L')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'mouth_ctrl_str', 'cheek_puff_mstr_R', 'cheek_puff_mstr_L')

def Reprop_Mouth_Curves_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Mouth_Curves_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('lip_low_ctrl', 'lip_up_ctrl', 'mouth_corner_str_L', 'mouth_corner_str_R',
    'lip_low_def_3_R', 'lip_low_def_2_R', 'lip_low_rim_def_3_R', 'lip_low_line_def_3_R', 'lip_low_def_1_R', 'lip_low_rim_def_2_R', 'lip_low_line_def_2_R', 'lip_low_def_3_L', 'lip_low_def_2_L',
    'lip_low_rim_def_3_L', 'lip_low_line_def_3_L', 'lip_low_def_1_L', 'lip_low_rim_def_2_L', 'lip_low_line_def_2_L', 'lip_low_def_mid', 'lip_low_rim_def_1_R', 'lip_low_rim_def_1_L', 'lip_low_line_def_1_L', 'lip_low_line_def_1_R',
    'lip_low_rim_def_4_R', 'lip_up_rim_def_4_R', 'lip_low_line_def_4_R', 'lip_up_line_def_4_R', 'lip_low_rim_def_4_L', 'lip_up_rim_def_4_L', 'lip_low_line_def_4_L', 'lip_up_line_def_4_L', 'lip_up_def_mid',
    'lip_up_rim_def_1_R', 'lip_up_rim_def_1_L', 'lip_up_line_def_1_L', 'lip_up_line_def_1_R', 'lip_up_def_1_L', 'lip_up_rim_def_2_L', 'lip_up_line_def_2_L', 'lip_up_def_1_R', 'lip_up_rim_def_2_R', 'lip_up_line_def_2_R',
    'lip_up_def_2_R', 'lip_up_rim_def_3_R', 'lip_up_line_def_3_R', 'lip_up_def_2_L', 'lip_up_rim_def_3_L', 'lip_up_line_def_3_L', 'lip_up_def_3_L', 'lip_up_def_3_R',
    'lip_low_line_L', 'lip_low_line_R', 'lip_up_line_L', 'lip_up_line_R', 'lip_low_def_4_L', 'lip_low_def_4_R'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'lip_low_ctrl', 'lip_up_ctrl', 'mouth_corner_str_L', 'mouth_corner_str_R')

def Reprop_Mouth_Curves(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Mouth_Curves'
    guide_props = bpy.context.scene.blenrig_guide

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')
    orbit_viewpoint(1, 'ORBITRIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('lip_low_def_3_R', 'lip_low_def_2_R', 'lip_low_rim_def_3_R', 'lip_low_line_def_3_R', 'lip_low_def_1_R', 'lip_low_rim_def_2_R', 'lip_low_line_def_2_R', 'lip_low_def_3_L', 'lip_low_def_2_L',
    'lip_low_rim_def_3_L', 'lip_low_line_def_3_L', 'lip_low_def_1_L', 'lip_low_rim_def_2_L', 'lip_low_line_def_2_L', 'lip_low_def_mid', 'lip_low_rim_def_1_R', 'lip_low_rim_def_1_L', 'lip_low_line_def_1_L', 'lip_low_line_def_1_R',
    'lip_low_rim_def_4_R', 'lip_up_rim_def_4_R', 'lip_low_line_def_4_R', 'lip_up_line_def_4_R', 'lip_low_rim_def_4_L', 'lip_up_rim_def_4_L', 'lip_low_line_def_4_L', 'lip_up_line_def_4_L', 'lip_up_def_mid',
    'lip_up_rim_def_1_R', 'lip_up_rim_def_1_L', 'lip_up_line_def_1_L', 'lip_up_line_def_1_R', 'lip_up_def_1_L', 'lip_up_rim_def_2_L', 'lip_up_line_def_2_L', 'lip_up_def_1_R', 'lip_up_rim_def_2_R', 'lip_up_line_def_2_R',
    'lip_up_def_2_R', 'lip_up_rim_def_3_R', 'lip_up_line_def_3_R', 'lip_up_def_2_L', 'lip_up_rim_def_3_L', 'lip_up_line_def_3_L', 'lip_up_def_3_L', 'lip_up_def_3_R',
    'lip_low_line_L', 'lip_low_line_R', 'lip_up_line_L', 'lip_up_line_R', 'lip_zipper_line_L', 'lip_zipper_line_R', 'lip_low_def_4_L', 'lip_low_def_4_R',
    'lip_up_ctrl_curve_L', 'lip_up_ctrl_curve_R', 'lip_low_ctrl_curve_L', 'lip_low_ctrl_curve_R'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'lip_up_ctrl_curve_L', 'lip_up_ctrl_curve_R', 'lip_low_ctrl_curve_L', 'lip_low_ctrl_curve_R')

    #Collect Values
    pbones = guide_props.arm_obj.pose.bones
    lip_up_vert_in = pbones["lip_up_line_L"].bone.bbone_curveiny
    lip_up_vert_out = pbones["lip_up_line_L"].bone.bbone_curveouty
    lip_up_depth_in = pbones["lip_up_line_L"].bone.bbone_curveinx
    lip_up_depth_out = pbones["lip_up_line_L"].bone.bbone_curveoutx
    lip_low_vert_in = pbones["lip_low_line_L"].bone.bbone_curveiny
    lip_low_vert_out = pbones["lip_low_line_L"].bone.bbone_curveouty
    lip_low_depth_in = pbones["lip_low_line_L"].bone.bbone_curveinx
    lip_low_depth_out = pbones["lip_low_line_L"].bone.bbone_curveoutx
    lip_zipper_vert_in = pbones["lip_zipper_line_L"].bone.bbone_curveiny
    lip_zipper_vert_out = pbones["lip_zipper_line_L"].bone.bbone_curveouty
    lip_zipper_depth_in = pbones["lip_zipper_line_L"].bone.bbone_curveinx
    lip_zipper_depth_out = pbones["lip_zipper_line_L"].bone.bbone_curveoutx
    #Assign BBone Values
    guide_props.guide_bbone_vertical_curve_in_lip_up = lip_up_vert_in
    guide_props.guide_bbone_vertical_curve_out_lip_up = lip_up_vert_out
    guide_props.guide_bbone_depth_curve_in_lip_up = lip_up_depth_in
    guide_props.guide_bbone_depth_curve_out_lip_up = lip_up_depth_out
    guide_props.guide_bbone_vertical_curve_in_lip_low = lip_low_vert_in
    guide_props.guide_bbone_vertical_curve_out_lip_low = lip_low_vert_out
    guide_props.guide_bbone_depth_curve_in_lip_low = lip_low_depth_in
    guide_props.guide_bbone_depth_curve_out_lip_low = lip_low_depth_out
    guide_props.guide_bbone_vertical_curve_in_lip_zipper = lip_zipper_vert_in
    guide_props.guide_bbone_vertical_curve_out_lip_zipper = lip_zipper_vert_out
    guide_props.guide_bbone_depth_curve_in_lip_zipper = lip_zipper_depth_in
    guide_props.guide_bbone_depth_curve_out_lip_zipper = lip_zipper_depth_out

def Reprop_Mouth_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Mouth_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('lip_low_def_3_R', 'lip_low_def_2_R', 'lip_low_rim_def_3_R', 'lip_low_line_def_3_R', 'lip_low_def_1_R', 'lip_low_rim_def_2_R', 'lip_low_line_def_2_R', 'lip_low_def_3_L', 'lip_low_def_2_L',
    'lip_low_rim_def_3_L', 'lip_low_line_def_3_L', 'lip_low_def_1_L', 'lip_low_rim_def_2_L', 'lip_low_line_def_2_L', 'lip_low_def_mid', 'lip_low_rim_def_1_R', 'lip_low_rim_def_1_L', 'lip_low_line_def_1_L', 'lip_low_line_def_1_R',
    'lip_low_rim_def_4_R', 'lip_up_rim_def_4_R', 'lip_low_line_def_4_R', 'lip_up_line_def_4_R', 'lip_low_rim_def_4_L', 'lip_up_rim_def_4_L', 'lip_low_line_def_4_L', 'lip_up_line_def_4_L', 'lip_up_def_mid',
    'lip_up_rim_def_1_R', 'lip_up_rim_def_1_L', 'lip_up_line_def_1_L', 'lip_up_line_def_1_R', 'lip_up_def_1_L', 'lip_up_rim_def_2_L', 'lip_up_line_def_2_L', 'lip_up_def_1_R', 'lip_up_rim_def_2_R', 'lip_up_line_def_2_R',
    'lip_up_def_2_R', 'lip_up_rim_def_3_R', 'lip_up_line_def_3_R', 'lip_up_def_2_L', 'lip_up_rim_def_3_L', 'lip_up_line_def_3_L', 'lip_up_def_3_L', 'lip_up_def_3_R',
    'lip_low_ctrl_3_str_R', 'lip_low_ctrl_2_str_R', 'lip_low_ctrl_1_str_R', 'lip_low_ctrl_3_str_L', 'lip_low_ctrl_2_str_L',
    'lip_low_ctrl_1_str_L', 'lip_low_ctrl_str_mid', 'lip_up_ctrl_str_mid', 'lip_up_ctrl_1_str_L', 'lip_up_ctrl_1_str_R',
    'lip_up_ctrl_2_str_R', 'lip_up_ctrl_2_str_L', 'lip_up_ctrl_3_str_L', 'lip_up_ctrl_3_str_R', 'lip_low_def_4_L', 'lip_low_def_4_R', 'mouth_corner_mstr_L', 'mouth_corner_mstr_R'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'lip_low_ctrl_3_str_R', 'lip_low_ctrl_2_str_R', 'lip_low_ctrl_1_str_R', 'lip_low_ctrl_3_str_L', 'lip_low_ctrl_2_str_L',
    'lip_low_ctrl_1_str_L', 'lip_low_ctrl_str_mid', 'lip_up_ctrl_str_mid', 'lip_up_ctrl_1_str_L', 'lip_up_ctrl_1_str_R',
    'lip_up_ctrl_2_str_R', 'lip_up_ctrl_2_str_L', 'lip_up_ctrl_3_str_L', 'lip_up_ctrl_3_str_R', 'mouth_corner_mstr_L', 'mouth_corner_mstr_R'
    )

def Reprop_Mouth_Outer_Ctrls(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Mouth_Outer_Ctrls'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('lip_up_outer_line_def_1_R', 'lip_up_outer_line_def_1_L', 'lip_low_outer_line_def_2_R', 'lip_low_outer_line_def_2_L',
    'lip_low_outer_line_def_1_R', 'lip_low_outer_line_def_1_L', 'lip_low_outer_line_def_3_R', 'lip_low_outer_line_def_3_L',
    'lip_low_outer_line_def_4_R', 'lip_low_outer_line_def_4_L', 'chin_line_def_4_R', 'chin_line_def_4_L', 'chin_line_def_3_R',
    'chin_line_def_3_L', 'chin_line_def_2_R', 'chin_line_def_2_L', 'chin_line_def_1_R', 'chin_line_def_1_L', 'lip_up_outer_line_def_2_R',
    'lip_up_outer_line_def_2_L', 'lip_up_outer_line_def_4_R', 'lip_up_outer_line_def_4_L', 'lip_up_outer_line_def_5_R', 'lip_up_outer_line_def_5_L',
    'smile_line_def_3_R', 'smile_line_def_3_L', 'lip_up_outer_line_def_3_R', 'lip_up_outer_line_def_3_L', 'smile_line_def_2_R', 'smile_line_def_2_L',
    'smile_line_low_def_1_R', 'smile_line_low_def_1_L', 'nose_base_def_2_R', 'nose_base_def_1_R', 'nose_base_def_1_L', 'nose_base_def_2_L',
    'chin_ctrl_mstr', 'lip_low_outer_ctrl', 'chin_ctrl', 'lip_up_loc', 'lip_low_loc', 'lip_up_outer_ctrl', 'nose_base_ctrl'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'chin_ctrl_mstr', 'lip_low_outer_ctrl', 'chin_ctrl', 'lip_up_outer_ctrl', 'nose_base_ctrl'
    )

def Reprop_Teeth_Up(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Teeth_Up'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('teeth_up_str', 'teeth_up_ctrl_str_L', 'teeth_up_ctrl_str_R', 'teeth_up_1_def_L', 'teeth_up_2_def_L', 'teeth_up_1_def_R',
    'teeth_up_2_def_R', 'teeth_up_ctrl_mid_str', 'teeth_up_ctrl_mid_str_L', 'teeth_up_ctrl_mid_str_R'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'teeth_up_str', 'teeth_up_ctrl_str_L', 'teeth_up_ctrl_str_R', 'teeth_up_ctrl_mid_str',
    'teeth_up_ctrl_mid_str_L', 'teeth_up_ctrl_mid_str_R'
    )

    select_pose_bone(context, 'teeth_up_str')

def Reprop_Teeth_Low(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Teeth_Low'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('teeth_low_str', 'teeth_low_1_def_L', 'teeth_low_2_def_L', 'teeth_low_1_def_R', 'teeth_low_2_def_R',
    'teeth_low_ctrl_str_L', 'teeth_low_ctrl_str_R', 'teeth_low_ctrl_mid_str', 'teeth_low_ctrl_mid_str_L','teeth_low_ctrl_mid_str_R'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'teeth_low_str', 'teeth_low_ctrl_str_L', 'teeth_low_ctrl_str_R', 'teeth_low_ctrl_mid_str',
    'teeth_low_ctrl_mid_str_L', 'teeth_low_ctrl_mid_str_R'
    )

    select_pose_bone(context, 'teeth_low_str')

def Reprop_Tongue(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Tongue'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('tongue_str', 'tongue_1_def', 'tongue_2_def', 'tongue_3_def', 'tongue_1_str', 'tongue_2_str', 'tongue_3_str'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'tongue_str', 'tongue_1_str', 'tongue_2_str', 'tongue_3_str'
    )

    select_pose_bone(context, 'tongue_str')

def Reprop_Inner_Mouth(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Inner_Mouth'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('mouth_floor', 'hard_palate', 'soft_palate', 'uvula_1', 'uvula_2', 'larynx'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'mouth_floor', 'hard_palate', 'soft_palate', 'uvula_1', 'uvula_2', 'larynx'
    )

def Reprop_Ears(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Ears'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('ear_R', 'ear_up_R', 'ear_low_R', 'ear_L', 'ear_up_L', 'ear_low_L'
    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'ear_R', 'ear_up_R', 'ear_low_R', 'ear_L', 'ear_up_L', 'ear_low_L'
    )

def Reprop_Hat_Glasses(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Hat_Glasses'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('RIGHT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    #
    bones = ('hat_free', 'eyeglasses_free')

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'hat_free', 'eyeglasses_free')

def Reprop_Look(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Look'

    reproportion_on(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'neck_ctrl_4_str')

    bones = ('look_str_loc', 'look_str_loc')

    # hide all bones but master_torso_str.
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'look_str_loc')

    # Se selecciona “master_torso”.
    select_pose_bone(context, 'look_str_loc')

def Reprop_Bake(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Bake'

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    #Turn Layers on
    on_layers = [31]
    for L in on_layers:
        context.object.data.layers[L] = True
        for l in range(len(context.object.data.layers)):
            if l not in on_layers:
                context.object.data.layers[l] = False

    unhide_all_bones(context)
    deselect_all_pose_bones(context)


    #Ensure Symmetry
    unhide_all_bones(context)
    #Left Side
    for b in context.pose_object.data.bones:
        if b.name.endswith('_L'):
            b.select = True

    if bpy.context.active_object.pose.use_mirror_x == True:
        mirror_pose()
    deselect_all_pose_bones(context)

def Reprop_Custom_Alignments(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Custom_Alignments'
    guide_props = context.scene.blenrig_guide

    reproportion_on(context)

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, "head_str", "master")

    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'OCTAHEDRAL')

    #Make Deform Bones Selectable
    for b in guide_props.arm_obj.pose.bones:
        if b.lock_location[:] == (True, True, True) and b.lock_rotation[:] == (True, True, True) and b.lock_scale[:] == (True, True, True):
            b.bone.hide_select = False

    set_mode('EDIT')

    #Set pivot to Individual Origins
    context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'

    #Turn Layers on
    on_layers = [29]
    for L in on_layers:
        context.object.data.layers[L] = True
        for l in range(len(context.object.data.layers)):
            if l not in on_layers:
                context.object.data.layers[l] = False

def Reprop_IK_Check(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_IK_Check'

    reproportion_on(context)
    reproportion_off(context)
    bpy.context.scene.blenrig_guide.arm_obj.show_in_front = True

    # Set View
    set_view_perspective(context, False)
    set_viewpoint('FRONT')

    # Adjust view to Bones.
    frame_bones(context, 'head_str', 'master')

    #Turn Layers on
    on_layers = [6, 7, 9, 16, 23, 27]
    for L in on_layers:
        context.object.data.layers[L] = True
        for l in range(len(context.object.data.layers)):
            if l not in on_layers:
                context.object.data.layers[l] = False
    #
    bones = ('hand_ik_ctrl_L', 'hand_ik_ctrl_R', 'master_torso', 'sole_ctrl_L', 'sole_ctrl_R',
    'arm_def_R', 'arm_def_L', 'thigh_def_L', 'thigh_def_R', 'thigh_twist_def_R', 'shin_def_R', 'shin_twist_def_R', 'arm_twist_def_R',
    'forearm_twist_def_R', 'forearm_def_R', 'arm_twist_def_L', 'forearm_twist_def_L', 'forearm_def_L', 'thigh_twist_def_L', 'shin_def_L', 'shin_twist_def_L'

    )

    unhide_all_bones(context)
    select_all_pose_bones(context)
    deselect_pose_bones(context, *bones)
    hide_selected_pose_bones(context)

    # Set Armature to Bbone Display
    set_display_type(context, 'BBONE')

    #Add bones to list for hiding toggle
    scn = bpy.context.scene
    scn.blenrig_wp_bones.clear()
    for b in bones:
        add_item = scn.blenrig_wp_bones.add()
        add_item.bone = b

    # Add OpenGL Highlight to bones
    operator.draw_bones(context, 'hand_ik_ctrl_L', 'hand_ik_ctrl_R', 'master_torso', 'sole_ctrl_L', 'sole_ctrl_R'
    )

def Reprop_Finish(operator, context):
    #Perform end of step action and set current step name
    end_of_step_action(context)
    bpy.context.scene.blenrig_guide.guide_current_step = 'Reprop_Finish'

    reproportion_off(context)

    #Turn Layers on
    on_layers = [0, 1, 3, 4, 5, 6, 7, 9, 16, 17, 18, 20, 22, 23]
    for L in on_layers:
        context.object.data.layers[L] = True
        for l in range(len(context.object.data.layers)):
            if l not in on_layers:
                context.object.data.layers[l] = False


#### END OF STEP ACTIONS ####
def reproportion_end_generic(context):
    guide_props = context.scene.blenrig_guide

    #Select Armature
    if hasattr(context, 'active_object') and hasattr(context.active_object, 'type'):
        if context.active_object.type == 'MESH':
            deselect_all_objects(context)
            select_armature(context)

    show_armature(context)

    #Ensure Symmetry
    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Left Side
    for b in context.pose_object.data.bones:
        if b.name.endswith('_L'):
            b.select = True

    if bpy.context.active_object.pose.use_mirror_x == True:
        mirror_pose()
    deselect_all_pose_bones(context)

    reproportion_off(context)

    unhide_all_bones(context)
    deselect_all_pose_bones(context)

    #Unlock Center Bones
    guide_props.guide_lock_center_bones = False

    #Make Deform Bones Selectable
    for b in guide_props.arm_obj.pose.bones:
        if b.lock_location[:] == (True, True, True) and b.lock_rotation[:] == (True, True, True) and b.lock_scale[:] == (True, True, True):
            b.bone.hide_select = False

    #Turn Layers off
    on_layers = [0, 1, 3, 4, 5, 6, 7, 9, 16, 17, 18, 20, 22, 23]
    off_layers = [24, 25, 26, 27, 28, 29, 30, 31]
    for l in on_layers:
        context.object.data.layers[l] = True
    for l in off_layers:
        context.object.data.layers[l] = False

    # Turn On Lattice Modifiers
    lattice_objects = collect_lattice_objects()
    for lattice in lattice_objects:
        for ob in bpy.data.objects:
            if hasattr(ob, 'modifiers'):
                for M in ob.modifiers:
                    if M.type == 'LATTICE' and M.object == lattice:
                        M.show_viewport = True

    #Unlink Temp Collection
    blenrig_temp_unlink()

    #Lock Object Mode Off
    bpy.context.scene.tool_settings.lock_object_mode = False

#Property for action to be performed after steps
def end_of_step_action(context):
    reproportion_end_generic(context)
    current_step = context.scene.blenrig_guide.guide_current_step
    if current_step == 'Reprop_Sole_Side':
        context.pose_object.pose.bones['foot_roll_ctrl_L'].lock_location[1] = True
        context.pose_object.pose.bones['foot_roll_ctrl_R'].lock_location[1] = True
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Sole_Bottom':
        #Make Roll Frame Non-Selectable
        try:
            bpy.context.scene.blenrig_guide.arm_obj.pose.bones['foot_ctrl_frame_L'].bone.hide_select = True
            bpy.context.scene.blenrig_guide.arm_obj.pose.bones['foot_ctrl_frame_R'].bone.hide_select = True
        except:
            pass
    if current_step == 'Reprop_Toes':
        context.pose_object.pose.bones['toes_spread_L'].lock_location[0] = True
        context.pose_object.pose.bones['toes_spread_L'].lock_location[1] = True
        context.pose_object.pose.bones['toes_spread_L'].lock_location[2] = True
        context.pose_object.pose.bones['toes_spread_L'].lock_rotation[1] = True
        context.pose_object.pose.bones['toes_spread_R'].lock_location[0] = True
        context.pose_object.pose.bones['toes_spread_R'].lock_location[1] = True
        context.pose_object.pose.bones['toes_spread_R'].lock_location[2] = True
        context.pose_object.pose.bones['toes_spread_R'].lock_rotation[1] = True
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Fingers':
        context.pose_object.pose.bones['fing_spread_L'].lock_location[0] = True
        context.pose_object.pose.bones['fing_spread_L'].lock_location[1] = True
        context.pose_object.pose.bones['fing_spread_L'].lock_location[2] = True
        context.pose_object.pose.bones['fing_spread_L'].lock_rotation[1] = True
        context.pose_object.pose.bones['fing_spread_L'].lock_scale[0] = True
        context.pose_object.pose.bones['fing_spread_L'].lock_scale[2] = True
        context.pose_object.pose.bones['fing_spread_R'].lock_location[0] = True
        context.pose_object.pose.bones['fing_spread_R'].lock_location[1] = True
        context.pose_object.pose.bones['fing_spread_R'].lock_location[2] = True
        context.pose_object.pose.bones['fing_spread_R'].lock_rotation[1] = True
        context.pose_object.pose.bones['fing_spread_R'].lock_scale[0] = True
        context.pose_object.pose.bones['fing_spread_R'].lock_scale[2] = True
        set_locks(['hand_close_L', 'hand_close_R'], True, True, True, True, True, True, True, False, True)
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Cheek_Ctrls':
        context.pose_object.pose.bones['nose_frown_ctrl_L'].lock_location[0] = True
        context.pose_object.pose.bones['nose_frown_ctrl_R'].lock_location[0] = True
        context.pose_object.pose.bones['nose_frown_ctrl_L'].lock_location[1] = True
        context.pose_object.pose.bones['nose_frown_ctrl_R'].lock_location[1] = True
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Toon_Scale':
        #Erase Temp Collection
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Face_Mstr':
        #Erase Temp Collection
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Edit_Face':
        #Erase Temp Collection
        # try:
        #     set_mode('OBJECT')
        # except:
            # pass
        blenrig_temp_unlink()
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Sole_Bottom':
        #Lock Foot Ctrl Frame
        context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_location[0] = True
        context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_location[0] = True
        context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_location[1] = True
        context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_location[1] = True
        context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_location[2] = True
        context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_location[2] = True
        context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_scale[0] = True
        context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_scale[0] = True
        context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_scale[1] = True
        context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_scale[1] = True
        context.pose_object.pose.bones['foot_ctrl_frame_L'].lock_scale[2] = True
        context.pose_object.pose.bones['foot_ctrl_frame_R'].lock_scale[2] = True
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Toon_Scale':
        #Set Locks
        set_locks(['neck_2_toon', 'neck_3_toon', 'spine_2_toon', 'spine_3_toon', 'spine_4_toon', 'shoulder_toon_R', 'shoulder_toon_L', 'pelvis_toon', 'spine_1_toon', 'pelvis_toon_R', 'pelvis_toon_L',
            'thigh_toon_R', 'knee_toon_R', 'foot_toon_R', 'toe_3_toon_R', 'toe_2_toon_R', 'toe_1_toon_R', 'shin_toon_R', 'arm_toon_R', 'elbow_toon_R', 'hand_toon_R', 'forearm_toon_R', 'arm_toon_L',
            'elbow_toon_L', 'hand_toon_L', 'forearm_toon_L', 'thigh_toon_L', 'knee_toon_L', 'foot_toon_L', 'toe_3_toon_L', 'toe_2_toon_L', 'toe_1_toon_L', 'shin_toon_L'], False, False, False, False, False, False, False, False, False)
        context.scene.blenrig_guide.guide_current_step = ''
    if current_step == 'Reprop_Eyelids_Ctrls':
        #Define Locks
        context.pose_object.pose.bones['blink_ctrl_L'].lock_location[0] = True
        context.pose_object.pose.bones['blink_ctrl_L'].lock_location[1] = True
        context.pose_object.pose.bones['blink_ctrl_R'].lock_location[0] = True
        context.pose_object.pose.bones['blink_ctrl_R'].lock_location[1] = True
        context.pose_object.pose.bones['blink_ctrl_L'].lock_rotation[0] = True
        context.pose_object.pose.bones['blink_ctrl_L'].lock_rotation[2] = True
        context.pose_object.pose.bones['blink_ctrl_L'].lock_scale[0] = True
        context.pose_object.pose.bones['blink_ctrl_L'].lock_scale[1] = True
        context.pose_object.pose.bones['blink_ctrl_R'].lock_rotation[0] = True
        context.pose_object.pose.bones['blink_ctrl_R'].lock_rotation[2] = True
        context.pose_object.pose.bones['blink_ctrl_R'].lock_scale[0] = True
        context.pose_object.pose.bones['blink_ctrl_R'].lock_scale[1] = True
    if current_step == 'Reprop_Custom_Alignments':
        go_blenrig_pose_mode(context)
        #Set pivot to Median Point
        context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
        context.scene.blenrig_guide.guide_current_step = ''



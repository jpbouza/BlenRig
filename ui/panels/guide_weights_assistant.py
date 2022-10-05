import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_weights
from . assistant_base import BLENRIG_PT_guide_assistant
from ...guides.utils import BL_Ver

####### Weights assistant Guide

class BLENRIG_PT_weights_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Weights Assistant Guide"
    bl_idname = "BLENRIG_PT_weights_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_weights.is_instantiated(context):
            return

        guide_props = context.scene.blenrig_guide
        active = context.active_object
        active_mode = active.mode
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        exclude_list = ['WEIGHTS_Intro', 'WEIGHTS_Finish']

        steps = layout.column(align=True)
        if guide_props.guide_current_step not in exclude_list:
            box_weight = steps.box()
            box_weight.label(text='Weight Painting Options')
            if '_Cage_' in guide_props.guide_current_step:
                box_weight.operator("blenrig.toggle_weight_painting", text='Toggle Weight Painting').paint_object = 'mdef_cage'
            else:
                box_weight.operator("blenrig.toggle_weight_painting", text='Toggle Weight Painting').paint_object = 'char'
            if active_mode == 'WEIGHT_PAINT':
                box_weight.label(text='Symmetry Options')
                mirror_row = box_weight.row()
                mirror_row.prop(active, "use_mesh_mirror_x", text='Enable X Symmetry')
                mirror_row.prop(active.data, "use_mirror_vertex_groups")
                mirror_row.prop(active.data, "use_mirror_topology")
            box_weight.label(text='Pose Options')
            mirror_row = box_weight.row()
            mirror_row.prop(guide_props.arm_obj.pose, "use_mirror_x", text='X-Axis Mirror (Pose)')
            if active_mode == 'WEIGHT_PAINT':
                if '_Char_' in guide_props.guide_current_step and '_Lattice' not in guide_props.guide_current_step:
                    box_weight.operator("blenrig.select_vgroup", text='Select Mesh Deform Vgroup').vgroup = 'no_mdef'
                if '_Lattice_Head' in guide_props.guide_current_step:
                    box_weight.operator("blenrig.select_vgroup", text='Select Head Lattice Vgroup').vgroup = 'lattice_head'
                if '_Lattice_Brow' in guide_props.guide_current_step:
                    box_weight.operator("blenrig.select_vgroup", text='Select Eyebrow Lattice Vgroup').vgroup = 'lattice_brow'
                if '_Lattice_Mouth' in guide_props.guide_current_step:
                    box_weight.operator("blenrig.select_vgroup", text='Select Mouth Lattice Vgroup').vgroup = 'lattice_mouth'
                if '_Lattice_Eye' in guide_props.guide_current_step:
                    box_weight.operator("blenrig.select_vgroup", text='Select Eye Lattice Vgroup').vgroup = 'lattice_eye_L'
            if '_Lattice' not in guide_props.guide_current_step:
                if active_mode != 'WEIGHT_PAINT':
                    box_weight.operator("blenrig.edit_corrective_smooth_vgroup", text='Edit Corrective Smooth Vgroup')
                else:
                    box_weight.operator("blenrig.select_vgroup", text='Select Corrective Smooth Vgroup').vgroup = 'corrective_smooth'
            box_row = box_weight.row()
            box_row.prop(guide_props, 'guide_show_wp_bones')
            box_row.prop(guide_props.arm_obj, 'show_in_front')
            if active_mode == 'WEIGHT_PAINT':
                box_row.prop(active, 'show_wire')
            steps.separator()
        #Cage Ankle
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Ankle':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Ankle Pose')
            if guide_props.guide_joint_transforms_X6 != 0:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.prop(p_bones["properties_leg_L"], 'realistic_joints_ankle_rot_L', text='Ankle Displacement')
            if guide_props.guide_joint_transforms_X6 == 3 or guide_props.guide_joint_transforms_X6 == 4 :
                box_pose.label(text='Shin Twist Rate')
                box_pose.prop(p_bones["properties_leg_L"], '["twist_rate_shin_L"]', text='Twist Rate')
            if guide_props.guide_joint_transforms_X6 == 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Instep')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X6 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Ankle')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['ankle_fix_L'].constraints['Ankle_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['ankle_fix_L'].constraints['Ankle_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X6 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Foot Toe
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Foot_Toe':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #Foot Toe 1
            if guide_props.guide_transformation_bone == 'foot_toe_1_fk_L':
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Foot Toe 1 Pose')
                if guide_props.guide_joint_transforms_X4 == 1:
                    row_props = box_pose.row()
                    col_R = row_props.column()
                    col_L = row_props.column()
                    col_R.label(text='Volume Preservation: Toe 1 Curl Down')
                    col_L.label(text=' ')
                    try:
                        col_R.prop(p_bones['foot_toe_fix_low_1_L'].constraints['Foot_Toe_1_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['foot_toe_fix_low_1_L'].constraints['Foot_Toe_1_Low_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_joint_transforms_X4 == 2:
                    row_props = box_pose.row()
                    col_R = row_props.column()
                    col_L = row_props.column()
                    col_R.label(text='Volume Preservation: Toe 1 Curl Up')
                    col_L.label(text=' ')
                    try:
                        col_R.prop(p_bones['foot_toe_fix_up_1_L'].constraints['Foot_Toe_1_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['foot_toe_fix_up_1_L'].constraints['Foot_Toe_1_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
            #Foot Toe 2
            if guide_props.guide_transformation_bone == 'foot_toe_2_fk_L':
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Foot Toe 2 Pose')
                if guide_props.guide_joint_transforms_X4 == 1:
                    row_props = box_pose.row()
                    col_R = row_props.column()
                    col_L = row_props.column()
                    col_R.label(text='Volume Preservation: Toe 2 Curl Down')
                    col_L.label(text=' ')
                    try:
                        col_R.prop(p_bones['foot_toe_fix_low_2_L'].constraints['Foot_Toe_2_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['foot_toe_fix_low_2_L'].constraints['Foot_Toe_2_Low_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_joint_transforms_X4 == 2:
                    row_props = box_pose.row()
                    col_R = row_props.column()
                    col_L = row_props.column()
                    col_R.label(text='Volume Preservation: Toe 2 Curl Up')
                    col_L.label(text=' ')
                    try:
                        col_R.prop(p_bones['foot_toe_fix_up_2_L'].constraints['Foot_Toe_2_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['foot_toe_fix_up_2_L'].constraints['Foot_Toe_2_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Knee
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Knee':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Knee Pose')
            if guide_props.guide_joint_transforms_X4 == 1:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.prop(p_bones["properties_leg_L"], 'realistic_joints_knee_loc_L', text='Shin Displacement')
                box_pose.prop(p_bones["properties_leg_L"], 'realistic_joints_knee_rot_L', text='Thigh Displacement')
            if guide_props.guide_joint_transforms_X4 == 3 or guide_props.guide_joint_transforms_X4 == 4 :
                box_pose.label(text='Thigh Twist Rate')
                box_pose.prop(p_bones["properties_leg_L"], '["twist_rate_thigh_L"]', text='Twist Rate')
            if guide_props.guide_joint_transforms_X4 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Shin')
                col_L.label(text='Volume Preservation: Knee Volume')
                try:
                    col_R.prop(p_bones['shin_fix_L'].constraints['Shin_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['shin_fix_L'].constraints['Shin_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['knee_fix_L'].constraints['Knee_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['knee_fix_L'].constraints['Knee_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Thigh
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Thigh':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Thigh Pose')
            if guide_props.guide_joint_transforms_X4 == 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Leg')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['thigh_fix_L'].constraints['Thigh_VP_Forw_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
                    col_R.prop(p_bones['thigh_fix_L'].constraints['Thigh_VP_Forw_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['thigh_fix_L'].constraints['Thigh_VP_Forw_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Buttock')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['buttock_fix_L'].constraints['Thigh_VP_Back_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['buttock_fix_L'].constraints['Thigh_VP_Back_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 4:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Hips')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['hip_fix_L'].constraints['Thigh_VP_Out_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
                    col_R.prop(p_bones['hip_fix_L'].constraints['Thigh_VP_Out_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['hip_fix_L'].constraints['Thigh_VP_Out_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Torso
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Torso':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #Spine 1
            if guide_props.guide_transformation_bone == 'pelvis_ctrl':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Pelvis / Spine 1 Pose')
            box_pose = steps.box()
            #Spine 2
            if guide_props.guide_transformation_bone == 'spine_2_fk':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Spine 2 Pose')
            box_pose = steps.box()
            #Spine 3
            if guide_props.guide_transformation_bone == 'spine_3_fk':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Spine 3 Pose')
        #Cage Neck
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Neck':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #Neck 1
            if guide_props.guide_transformation_bone == 'neck_1_fk':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Neck 1 Pose')
            box_pose = steps.box()
            #Neck 2
            if guide_props.guide_transformation_bone == 'neck_2_fk':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Neck 2 Pose')
            box_pose = steps.box()
            #Neck 3
            if guide_props.guide_transformation_bone == 'neck_3_fk':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Neck 3 Pose')
            #Head
            if guide_props.guide_transformation_bone == 'head_fk':
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Head Pose')
        #Cage Clavicle
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Clavicle':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Collarbone Pose')
            if guide_props.guide_joint_transforms_X4 == 3:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Trapezius')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['trap_fix_L'].constraints['Trap_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['trap_fix_L'].constraints['Trap_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Shoulder
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Shoulder':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Arm Pose')
            if guide_props.guide_joint_transforms_X4 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Chest')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Forw_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Forw_L_NOREP'], 'to_max_x', text="Horizontal", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Back')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
                    col_L.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 3:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Shoulder')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['shoulder_fix_L'].constraints['Shoulder_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['shoulder_fix_L'].constraints['Shoulder_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 4:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Armpit:')
                col_L.label(text='Chest:')
                try:
                    col_R.prop(p_bones['armpit_fix_L'].constraints['Armpit_VP_Down_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['armpit_fix_L'].constraints['Armpit_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Down_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
                except:
                    pass
                col_R.label(text='Back:')
                try:
                    col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
                    col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Elbow
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Elbow':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Forearm Pose')
            if guide_props.guide_joint_transforms_X4 == 1:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_elbow_loc_L', text="Forearm Displacement", toggle=True)
                box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_elbow_rot_L', text="Arm Displacement", toggle=True)
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Forearm')
                col_L.label(text='Elbow')
                try:
                    col_R.prop(p_bones['forearm_fix_L'].constraints['Forearm_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['forearm_fix_L'].constraints['Forearm_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['elbow_fix_L'].constraints['Elbow_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['elbow_fix_L'].constraints['Elbow_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 3 or guide_props.guide_joint_transforms_X4 == 4 :
                box_pose.label(text='Arm Twist Rate')
                box_pose.prop(p_bones["properties_arm_L"], '["twist_rate_arm_L"]', text='Twist Rate')
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Cage Wrist
        if guide_props.guide_current_step == 'WEIGHTS_Cage_Wrist':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Wrist Pose')
            if guide_props.guide_joint_transforms_X6 != 0:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_wrist_rot_L', text="Wrist_L Displacement 1", toggle=True)
            if guide_props.guide_joint_transforms_X6 == 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Upper Wrist Volume:')
                col_L.label(text='Lower Wrist Volume:')
                try:
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X6 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Upper Wrist Volume:')
                col_L.label(text='Lower Wrist Volume:')
                try:
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X6 == 5 or guide_props.guide_joint_transforms_X6 == 6 :
                box_pose.label(text='Forerm Twist Rate')
                box_pose.prop(p_bones["properties_arm_L"], '["twist_rate_forearm_L"]', text='Twist Rate')
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Char Wrist
        if guide_props.guide_current_step == 'WEIGHTS_Char_Wrist':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Wrist Pose')
            if guide_props.guide_joint_transforms_X4 != 0:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_wrist_rot_L', text="Wrist_L Displacement 1", toggle=True)
            if guide_props.guide_joint_transforms_X4== 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Upper Wrist Volume:')
                col_L.label(text='Lower Wrist Volume:')
                try:
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X4 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Upper Wrist Volume:')
                col_L.label(text='Lower Wrist Volume:')
                try:
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
                try:
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
        #Char Hand VP
        if guide_props.guide_current_step == 'WEIGHTS_Char_Hand_VP':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Hand Pose')
            if guide_props.guide_joint_transforms_X2 == 1:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.label(text='Fingers:')
                row_1_L = box_pose.row()
                row_1_L.prop(p_bones['properties_arm_L'], 'realistic_joints_fingers_loc_L', toggle=True, icon_only=True)
                row_2_L = box_pose.row()
                row_2_L.prop(p_bones['properties_arm_L'], 'realistic_joints_fingers_rot_L', toggle=True, icon_only=True)
                box_pose.label(text='Volume Preservation: Fingers')
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Knuckles Volume:')
                col_L.label(text='Palm Volume:')
                try:
                    col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_knuckles_down_L', text="Outwards", toggle=True)
                    col_L.prop(p_bones['properties_arm_L'], 'volume_preservation_palm_down_L', text="Outwards", toggle=True)
                except:
                    pass
                col_R.label(text='Fingers Volume:')
                try:
                    col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_fingers_down_L', text="Outwards", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_transforms_X2 == 2:
                box_pose.label(text='Volume Preservation: Fingers')
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Knuckles Volume:')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_knuckles_up_L', text="Outwards", toggle=True)
                except:
                    pass
            box_pose.separator()
            box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
            if not guide_props.auto_mirror_vp_rj_values:
                box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Char Fingers 1
        if guide_props.guide_current_step == 'WEIGHTS_Char_Fings_1':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Fingers Pose')
            if guide_props.guide_joint_transforms_X6 == 5:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                if guide_props.guide_transformation_bone == 'fing_thumb_ctrl_L':
                    col_R.label(text='Thumb Up Knuckle Volume:')
                    try:
                        col_R.prop(p_bones['fing_thumb_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_thumb_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ind_ctrl_L':
                    col_R.label(text='Index Up Knuckle Volume:')
                    try:
                        col_R.prop(p_bones['fing_ind_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ind_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_mid_ctrl_L':
                    col_R.label(text='Middle Up Knuckle Volume:')
                    try:
                        col_R.prop(p_bones['fing_mid_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_mid_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ring_ctrl_L':
                    col_R.label(text='Ring Up Knuckle Volume:')
                    try:
                        col_R.prop(p_bones['fing_ring_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ring_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_lit_ctrl_L':
                    col_R.label(text='LIttle Up Knuckle Volume:')
                    try:
                        col_R.prop(p_bones['fing_lit_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_lit_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                    except:
                        pass
            if guide_props.guide_joint_transforms_X6 == 6:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                if guide_props.guide_transformation_bone == 'fing_thumb_ctrl_L':
                    col_R.label(text='Thumb Down Knuckle Volume:')
                    col_L.label(text='Thumb Down Palm Volume:')
                    try:
                        col_R.prop(p_bones['fing_thumb_fix_up_1_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_thumb_fix_up_1_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_thumb_fix_low_1_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_thumb_fix_low_1_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ind_ctrl_L':
                    col_R.label(text='Index Down Knuckle Volume:')
                    col_L.label(text='Index Down Palm Volume:')
                    try:
                        col_R.prop(p_bones['fing_ind_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ind_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_ind_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_ind_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_mid_ctrl_L':
                    col_R.label(text='Middle Down Knuckle Volume:')
                    col_L.label(text='Middle Down Palm Volume:')
                    try:
                        col_R.prop(p_bones['fing_mid_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_mid_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_mid_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_mid_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ring_ctrl_L':
                    col_R.label(text='Ring Down Knuckle Volume:')
                    col_L.label(text='Ring Down Palm Volume:')
                    try:
                        col_R.prop(p_bones['fing_ring_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ring_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_ring_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_ring_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_lit_ctrl_L':
                    col_R.label(text='Little Down Knuckle Volume:')
                    col_L.label(text='Little Down Palm Volume:')
                    try:
                        col_R.prop(p_bones['fing_lit_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_lit_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_lit_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_lit_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
            if guide_props.guide_joint_transforms_X6 == 5 or guide_props.guide_joint_transforms_X6 == 6:
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Char Fingers 2
        if guide_props.guide_current_step == 'WEIGHTS_Char_Fings_2':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Fingers Pose')
            if guide_props.guide_joint_transforms_X2 == 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                if guide_props.guide_transformation_bone == 'fing_thumb_3_L':
                    col_R.label(text='Thumb Upper Volume:')
                    col_L.label(text='Thumb Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_thumb_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_thumb_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_thumb_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_thumb_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ind_3_L':
                    col_R.label(text='Index Upper Volume:')
                    col_L.label(text='Index Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_ind_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ind_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_ind_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_ind_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ind_4_L':
                    col_R.label(text='Index Upper Volume:')
                    col_L.label(text='Index Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_ind_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ind_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_ind_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_ind_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_mid_3_L':
                    col_R.label(text='Middle Upper Volume:')
                    col_L.label(text='Middle Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_mid_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_mid_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_mid_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_mid_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_mid_4_L':
                    col_R.label(text='Middle Upper Volume:')
                    col_L.label(text='Middle Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_mid_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_mid_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_mid_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_mid_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ring_3_L':
                    col_R.label(text='Ring Upper Volume:')
                    col_L.label(text='Ring Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_ring_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ring_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_ring_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_ring_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_ring_4_L':
                    col_R.label(text='Ring Upper Volume:')
                    col_L.label(text='Ring Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_ring_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_ring_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_ring_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_ring_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_lit_3_L':
                    col_R.label(text='Little Upper Volume:')
                    col_L.label(text='Little Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_lit_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_lit_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_lit_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_lit_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                if guide_props.guide_transformation_bone == 'fing_lit_4_L':
                    col_R.label(text='Little Upper Volume:')
                    col_L.label(text='Little Lower Volume:')
                    try:
                        col_R.prop(p_bones['fing_lit_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_R.prop(p_bones['fing_lit_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                        col_L.prop(p_bones['fing_lit_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                        col_L.prop(p_bones['fing_lit_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                    except:
                        pass
                box_pose.separator()
                box_pose.prop(guide_props, "auto_mirror_vp_rj_values", text='Auto Mirror RJ and VP Values')
                if not guide_props.auto_mirror_vp_rj_values:
                    box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
        #Char Head
        if guide_props.guide_current_step == 'WEIGHTS_Char_Head':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Head Pose')
        #Char Head Joints
        if guide_props.guide_current_step == 'WEIGHTS_Char_Head_Joints':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Head Joints Pose')
        #Char Ears
        if guide_props.guide_current_step == 'WEIGHTS_Char_Ears':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Ear Pose')
        #Char Eyebrows
        if guide_props.guide_current_step == 'WEIGHTS_Char_Eyebrows':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Eyebrows Pose')
        #Char Eyelids
        if guide_props.guide_current_step == 'WEIGHTS_Char_Eyelids':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Eyelids Pose')
        #Char Cheeks
        if guide_props.guide_current_step == 'WEIGHTS_Char_Cheeks':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Cheeks Pose')
        #Nose
        if guide_props.guide_current_step == 'WEIGHTS_Char_Nose':
            box_pose = steps.box()
            box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            joint_row = box_pose.row()
            joint_row.alignment = 'CENTER'
            joint_row.scale_x = BL_Ver(1, 0.9)
            joint_col_1 = joint_row.column()
            joint_col_1.alignment = 'CENTER'
            joint_col_2 = joint_row.column()
            joint_col_2.alignment = 'CENTER'
            joint_col_3 = joint_row.column()
            joint_col_3.alignment = 'CENTER'
            joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Nose Pose')
        #Mouth
        if guide_props.guide_current_step == 'WEIGHTS_Char_Mouth':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Mouth Pose')
        #Inner Mouth
        if guide_props.guide_current_step == 'WEIGHTS_Char_Inner_Mouth':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Mouth Pose')
            box_pose.label(text='Masking Options')
            box_pose.prop(active.data, "use_paint_mask", text='Use Face Mask')
            box_pose.prop(bpy.context.scene.tool_settings, "use_auto_normalize", text='Use Auto Normalize')



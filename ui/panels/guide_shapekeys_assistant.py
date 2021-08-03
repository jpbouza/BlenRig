import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_shapekeys
from . assistant_base import BLENRIG_PT_guide_assistant

####### Shapekeys assistant Guide

class BLENRIG_PT_shapekeys_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Shapekeys Assistant Guide"
    bl_idname = "BLENRIG_PT_shapekeys_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"

    def draw(self, context):
        guide_props = context.scene.blenrig_guide
        active = context.active_object
        active_mode = active.mode
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        exclude_list = ['SHAPEKEYS_Cage_Add_Body_Shapes']

        if VIEW3D_OT_blenrig_guide_shapekeys.instance:
            steps = layout.column(align=True)
            if guide_props.guide_current_step not in exclude_list:
                box_weight = steps.box()
                box_pose = steps.box()
                box_weight.label(text='Shapekeys Editting Options')
                if '_Cage_' in guide_props.guide_current_step:
                    box_weight.operator("blenrig.toggle_shapekey_editting", text='Toggle Shapekey Editting').mesh_edit_object = 'mdef_cage'
                else:
                    box_weight.operator("blenrig.toggle_shapekey_editting", text='Toggle Shapekey Editting').mesh_edit_object = 'char'
                box_weight.label(text='Shapekeys Editting Options')
                mirror_row = box_weight.row()
                mirror_row.prop(guide_props.arm_obj.pose, "use_mirror_x", text='X-Axis Mirror (Pose)')
                if active_mode == 'EDIT':
                    mirror_row.prop(active.data, "use_mirror_x", text='X-Mirror')
                    mirror_row.prop(active.data, "use_mirror_topology")
                steps.separator()
            #Add Body Shapekeys
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Add_Body_Shapes':
                box_pose = steps.box()
                box_pose.label(text='Add Body Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.add_body_shapekeys", text = 'Add Body Shapekeys')
            #Cage Ankle
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Ankle':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Ankle Pose')
            #Cage Foot Toe
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Foot_Toe':
                box_pose = steps.box()
                box_pose.label(text='Select Joint Number', icon='BONE_DATA')
                joint_row = box_pose.row()
                joint_row.alignment = 'CENTER'
                joint_row.scale_x = 0.9
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
                #Foot Toe 2
                if guide_props.guide_transformation_bone == 'foot_toe_2_fk_L':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Foot Toe 2 Pose')
            #Cage Knee
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Knee':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Knee Pose')
            #Cage Thigh
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Thigh':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Thigh Pose')
            #Cage Torso
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Torso':
                box_pose = steps.box()
                box_pose.label(text='Select Joint Number', icon='BONE_DATA')
                joint_row = box_pose.row()
                joint_row.alignment = 'CENTER'
                joint_row.scale_x = 0.9
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
            # #Cage Neck
            # if guide_props.guide_current_step == 'WEIGHTS_Cage_Neck':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     #Neck 1
            #     if guide_props.guide_transformation_bone == 'neck_1_fk':
            #         box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Neck 1 Pose')
            #     box_pose = steps.box()
            #     #Neck 2
            #     if guide_props.guide_transformation_bone == 'neck_2_fk':
            #         box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Neck 2 Pose')
            #     box_pose = steps.box()
            #     #Neck 3
            #     if guide_props.guide_transformation_bone == 'neck_3_fk':
            #         box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Neck 3 Pose')
            #     #Head
            #     if guide_props.guide_transformation_bone == 'head_fk':
            #         box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Head Pose')
            # #Cage Clavicle
            # if guide_props.guide_current_step == 'WEIGHTS_Cage_Clavicle':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Collarbone Pose')
            # #Cage Shoulder
            # if guide_props.guide_current_step == 'WEIGHTS_Cage_Shoulder':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Arm Pose')
            #     if guide_props.guide_joint_transforms_X4 == 1:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Volume Preservation: Chest')
            #         col_L.label(text=' ')
            #         try:
            #             col_R.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Forw_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Forw_L_NOREP'], 'to_max_x', text="Horizontal", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X4 == 2:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Volume Preservation: Back')
            #         col_L.label(text=' ')
            #         try:
            #             col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            #             col_L.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X4 == 3:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Volume Preservation: Shoulder')
            #         col_L.label(text=' ')
            #         try:
            #             col_R.prop(p_bones['shoulder_fix_L'].constraints['Shoulder_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['shoulder_fix_L'].constraints['Shoulder_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X4 == 4:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Volume Preservation: Armpit:')
            #         col_L.label(text='Chest:')
            #         try:
            #             col_R.prop(p_bones['armpit_fix_L'].constraints['Armpit_VP_Down_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['armpit_fix_L'].constraints['Armpit_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #         try:
            #             col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #             col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Down_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            #         except:
            #             pass
            #         col_R.label(text='Back:')
            #         try:
            #             col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            #             col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X4 != 0:
            #         box_pose.separator()
            #         box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
            # #Cage Elbow
            # if guide_props.guide_current_step == 'WEIGHTS_Cage_Elbow':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Forearm Pose')
            #     if guide_props.guide_joint_transforms_X4 == 1:
            #         box_pose.label(text='Realistic Joints Parameters')
            #         box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_elbow_loc_L', text="Forearm Displacement", toggle=True)
            #         box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_elbow_rot_L', text="Arm Displacement", toggle=True)
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Volume Preservation: Forearm')
            #         col_L.label(text='Elbow')
            #         try:
            #             col_R.prop(p_bones['forearm_fix_L'].constraints['Forearm_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['forearm_fix_L'].constraints['Forearm_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #         try:
            #             col_L.prop(p_bones['elbow_fix_L'].constraints['Elbow_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['elbow_fix_L'].constraints['Elbow_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X4 == 3 or guide_props.guide_joint_transforms_X4 == 4 :
            #         box_pose.label(text='Arm Twist Rate')
            #         box_pose.prop(p_bones["properties_arm_L"], '["twist_rate_arm_L"]', text='Twist Rate')
            #     if guide_props.guide_joint_transforms_X4 != 0:
            #         box_pose.separator()
            #         box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
            # #Cage Wrist
            # if guide_props.guide_current_step == 'WEIGHTS_Cage_Wrist':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Wrist Pose')
            #     if guide_props.guide_joint_transforms_X6 != 0:
            #         box_pose.label(text='Realistic Joints Parameters')
            #         box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_wrist_rot_L', text="Wrist_L Displacement 1", toggle=True)
            #     if guide_props.guide_joint_transforms_X6 == 2:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Upper Wrist Volume:')
            #         col_L.label(text='Lower Wrist Volume:')
            #         try:
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #         try:
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X6 == 1:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Upper Wrist Volume:')
            #         col_L.label(text='Lower Wrist Volume:')
            #         try:
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #         try:
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X6 == 5 or guide_props.guide_joint_transforms_X6 == 6 :
            #         box_pose.label(text='Forerm Twist Rate')
            #         box_pose.prop(p_bones["properties_arm_L"], '["twist_rate_forearm_L"]', text='Twist Rate')
            #     if guide_props.guide_joint_transforms_X4 != 0:
            #         box_pose.separator()
            #         box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
            # #Char Wrist
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Wrist':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Wrist Pose')
            #     if guide_props.guide_joint_transforms_X4 != 0:
            #         box_pose.label(text='Realistic Joints Parameters')
            #         box_pose.prop(p_bones['properties_arm_L'], 'realistic_joints_wrist_rot_L', text="Wrist_L Displacement 1", toggle=True)
            #     if guide_props.guide_joint_transforms_X4== 2:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Upper Wrist Volume:')
            #         col_L.label(text='Lower Wrist Volume:')
            #         try:
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #         try:
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X4 == 1:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Upper Wrist Volume:')
            #         col_L.label(text='Lower Wrist Volume:')
            #         try:
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            #         try:
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
            #         except:
            #             pass
            # #Char Hand VP
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Hand_VP':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Hand Pose')
            #     if guide_props.guide_joint_transforms_X2 == 1:
            #         box_pose.label(text='Realistic Joints Parameters')
            #         box_pose.label(text='Fingers:')
            #         row_1_L = box_pose.row()
            #         row_1_L.prop(p_bones['properties_arm_L'], 'realistic_joints_fingers_loc_L', toggle=True, icon_only=True)
            #         row_2_L = box_pose.row()
            #         row_2_L.prop(p_bones['properties_arm_L'], 'realistic_joints_fingers_rot_L', toggle=True, icon_only=True)
            #         box_pose.label(text='Volume Preservation: Fingers')
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Knuckles Volume:')
            #         col_L.label(text='Palm Volume:')
            #         try:
            #             col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_knuckles_down_L', text="Outwards", toggle=True)
            #             col_L.prop(p_bones['properties_arm_L'], 'volume_preservation_palm_down_L', text="Outwards", toggle=True)
            #         except:
            #             pass
            #         col_R.label(text='Fingers Volume:')
            #         try:
            #             col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_fingers_down_L', text="Outwards", toggle=True)
            #         except:
            #             pass
            #     if guide_props.guide_joint_transforms_X2 == 2:
            #         box_pose.label(text='Volume Preservation: Fingers')
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         col_R.label(text='Knuckles Volume:')
            #         col_L.label(text=' ')
            #         try:
            #             col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_knuckles_up_L', text="Outwards", toggle=True)
            #         except:
            #             pass
            #     box_pose.separator()
            #     box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
            # #Char Fingers 1
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Fings_1':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Fingers Pose')
            #     if guide_props.guide_joint_transforms_X6 == 5:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         if guide_props.guide_transformation_bone == 'fing_thumb_ctrl_L':
            #             col_R.label(text='Thumb Up Knuckle Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_thumb_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ind_ctrl_L':
            #             col_R.label(text='Index Up Knuckle Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ind_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_mid_ctrl_L':
            #             col_R.label(text='Middle Up Knuckle Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_mid_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ring_ctrl_L':
            #             col_R.label(text='Ring Up Knuckle Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ring_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_lit_ctrl_L':
            #             col_R.label(text='LIttle Up Knuckle Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_lit_fix_up_1_L'].constraints['Fing_Knuckles_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #     if guide_props.guide_joint_transforms_X6 == 6:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         if guide_props.guide_transformation_bone == 'fing_thumb_ctrl_L':
            #             col_R.label(text='Thumb Down Knuckle Volume:')
            #             col_L.label(text='Thumb Down Palm Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_thumb_fix_up_1_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_thumb_fix_low_1_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ind_ctrl_L':
            #             col_R.label(text='Index Down Knuckle Volume:')
            #             col_L.label(text='Index Down Palm Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ind_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_ind_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_mid_ctrl_L':
            #             col_R.label(text='Middle Down Knuckle Volume:')
            #             col_L.label(text='Middle Down Palm Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_mid_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_mid_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ring_ctrl_L':
            #             col_R.label(text='Ring Down Knuckle Volume:')
            #             col_L.label(text='Ring Down Palm Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ring_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_ring_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_lit_ctrl_L':
            #             col_R.label(text='Little Down Knuckle Volume:')
            #             col_L.label(text='Little Down Palm Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_lit_fix_up_1_L'].constraints['Fing_Knuckles_VP_Down_L_NOREP'], 'to_max_z', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_lit_fix_low_1_L'].constraints['Fing_Palm_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #     if guide_props.guide_joint_transforms_X6 == 5 or guide_props.guide_joint_transforms_X6 == 6:
            #         box_pose.separator()
            #         box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
            # #Char Fingers 2
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Fings_2':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Fingers Pose')
            #     if guide_props.guide_joint_transforms_X2 == 2:
            #         row_props = box_pose.row()
            #         col_R = row_props.column()
            #         col_L = row_props.column()
            #         if guide_props.guide_transformation_bone == 'fing_thumb_3_L':
            #             col_R.label(text='Thumb Upper Volume:')
            #             col_L.label(text='Thumb Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_thumb_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_thumb_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ind_3_L':
            #             col_R.label(text='Index Upper Volume:')
            #             col_L.label(text='Index Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ind_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_ind_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ind_4_L':
            #             col_R.label(text='Index Upper Volume:')
            #             col_L.label(text='Index Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ind_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_ind_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_mid_3_L':
            #             col_R.label(text='Middle Upper Volume:')
            #             col_L.label(text='Middle Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_mid_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_mid_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_mid_4_L':
            #             col_R.label(text='Middle Upper Volume:')
            #             col_L.label(text='Middle Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_mid_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_mid_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ring_3_L':
            #             col_R.label(text='Ring Upper Volume:')
            #             col_L.label(text='Ring Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ring_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_ring_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_ring_4_L':
            #             col_R.label(text='Ring Upper Volume:')
            #             col_L.label(text='Ring Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_ring_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_ring_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_lit_3_L':
            #             col_R.label(text='Little Upper Volume:')
            #             col_L.label(text='Little Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_lit_fix_up_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_lit_fix_low_2_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         if guide_props.guide_transformation_bone == 'fing_lit_4_L':
            #             col_R.label(text='Little Upper Volume:')
            #             col_L.label(text='Little Lower Volume:')
            #             try:
            #                 col_R.prop(p_bones['fing_lit_fix_up_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #                 col_L.prop(p_bones['fing_lit_fix_low_3_L'].constraints['Fing_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            #             except:
            #                 pass
            #         box_pose.separator()
            #         box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')
            # #Char Head
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Head':
            #     box_pose = steps.box()
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Head Pose')
            # #Char Head Joints
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Head_Joints':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Head Joints Pose')
            # #Char Ears
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Ears':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Ear Pose')
            # #Char Eyebrows
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Eyebrows':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Eyebrows Pose')
            # #Char Eyelids
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Eyelids':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Eyelids Pose')
            # #Char Cheeks
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Cheeks':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Cheeks Pose')
            # #Nose
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Nose':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Nose Pose')
            # #Mouth
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Mouth':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Mouth Pose')
            # #Inner Mouth
            # if guide_props.guide_current_step == 'WEIGHTS_Char_Inner_Mouth':
            #     box_pose = steps.box()
            #     box_pose.label(text='Select Joint Number', icon='BONE_DATA')
            #     joint_row = box_pose.row()
            #     joint_row.alignment = 'CENTER'
            #     joint_row.scale_x = 0.9
            #     joint_col_1 = joint_row.column()
            #     joint_col_1.alignment = 'CENTER'
            #     joint_col_2 = joint_row.column()
            #     joint_col_2.alignment = 'CENTER'
            #     joint_col_3 = joint_row.column()
            #     joint_col_3.alignment = 'CENTER'
            #     joint_col_1.operator("blenrig.wp_joint_chain_down", icon='TRIA_LEFT', text='')
            #     joint_col_2.label(text=guide_props.guide_transformation_bone.upper())
            #     joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
            #     box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
            #     box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Mouth Pose')
            #     box_pose.label(text='Masking Options')
            #     box_pose.prop(active.data, "use_paint_mask", text='Use Face Mask')
            #     box_pose.prop(bpy.context.scene.tool_settings, "use_auto_normalize", text='Use Auto Normalize')
            if guide_props.guide_current_step not in exclude_list:
                box_pose.label(text='Active Shapekey:')
                row_shape = box_pose.row()
                row_shape.alignment = 'CENTER'
                if hasattr(guide_props.active_shp_obj, 'active_shape_key') and hasattr(guide_props.active_shp_obj.active_shape_key, 'name'):
                    row_shape.label(text=guide_props.active_shp_obj.active_shape_key.name.upper())
                box_pose.label(text='Drivers:')
                row_drivers = box_pose.row()
                row_drivers.operator("blenrig.update_shapekey_driver", text='Update Driver with Current Pose')
                if not guide_props.auto_mirror_shapekeys:
                    row_drivers.operator("blenrig.mirror_active_shapekey_driver", text='Mirror Active Shapekey Driver')
                box_pose.label(text='Mirroring:')
                box_pose.prop(guide_props, "auto_mirror_shapekeys", text='Auto Mirror Shapekeys')
                if not guide_props.auto_mirror_shapekeys:
                    if guide_props.active_shp_obj.data.use_mirror_topology == True:
                        box_pose.operator("object.blenrig_shape_key_copy", text='Mirror Active Shapekey').type='MIRROR_TOPOLOGY'
                    else:
                        box_pose.operator("object.blenrig_shape_key_copy", text='Mirror Active Shapekey').type='MIRROR'


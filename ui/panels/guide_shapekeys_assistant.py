import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_shapekeys
from . assistant_base import BLENRIG_PT_guide_assistant
from ...guides.utils import BL_Ver

####### Shapekeys assistant Guide

class BLENRIG_PT_shapekeys_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Shapekeys Assistant Guide"
    bl_idname = "BLENRIG_PT_shapekeys_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_shapekeys.is_instantiated(context):
            return

        guide_props = context.scene.blenrig_guide
        active = context.active_object
        active_mode = active.mode
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        exclude_list = ['SHAPEKEYS_Cage_Add_Body_Shapes', 'SHAPEKEYS_Char_Add_Fingers_Shapes', 'SHAPEKEYS_Char_Add_Face_Shapes', 'SHAPEKEYS_Char_Eyebrow_Weight', 'SHAPEKEYS_Char_Mouth_Weight', 'SHAPEKEYS_Intro']
        #List for Not displaying the Update Driver Button
        facial_drivers_list = ['SHAPEKEYS_Char_Eyebrow_Weight', 'SHAPEKEYS_Char_Eyelid_Up_Up', 'SHAPEKEYS_Char_Eyelid_Low_Down', 'SHAPEKEYS_Char_Cheeks', 'SHAPEKEYS_Char_Nose_Frown', 'SHAPEKEYS_Char_Nostril',
        'SHAPEKEYS_Char_Mouth_Corner_Base', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2', 'SHAPEKEYS_Char_Mouth_Weight', 'SHAPEKEYS_Char_Mouth_U', 'SHAPEKEYS_Char_Mouth_U_Thickness',
        'SHAPEKEYS_Char_Mouth_M', 'SHAPEKEYS_Char_Mouth_Open_Close', 'SHAPEKEYS_Char_Mouth_Open_Out', 'SHAPEKEYS_Char_Mouth_Open_In', 'SHAPEKEYS_Char_Mouth_Close_Out', 'SHAPEKEYS_Char_Mouth_Close_In',
        'SHAPEKEYS_Char_Mouth_Frown_Side_Out','SHAPEKEYS_Char_Mouth_Frown_Side_In']

        steps = layout.column(align=True)
        if '_BlenRigSculptShapekey' not in active.name:
            if guide_props.guide_current_step not in exclude_list:
                box_weight = steps.box()
                box_pose = steps.box()
                if '_Cage_' in guide_props.guide_current_step:
                    box_weight.operator("blenrig.toggle_shapekey_editting", text='Toggle Shapekey Editting').mesh_edit_object = 'mdef_cage'
                    if active != guide_props.mdef_cage_obj:
                        if 'BlenRigMdefCage' not in active.name:
                            if hasattr(active, 'modifiers'):
                                if active_mode != 'WEIGHT_PAINT':
                                    for mod in active.modifiers:
                                        if mod.type == 'CORRECTIVE_SMOOTH':
                                            box_weight.operator("blenrig.edit_corrective_smooth_vgroup", text='Edit Corrective Smooth Vgroup')
                            if hasattr(active, 'data') and hasattr(active.data, 'shape_keys') and hasattr(active.data.shape_keys, 'key_blocks'):
                                box_weight.label(text='Sculpt Shapekey')
                                row_sculpt = box_weight.row()
                                if active.active_shape_key.name.endswith('_L'):
                                    row_sculpt.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').X_Mirror = False
                                elif active.active_shape_key.name.endswith('_R'):
                                    row_sculpt.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').X_Mirror = False
                                else:
                                    row_sculpt.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').X_Mirror = True
                                row_sculpt.operator("blenrig.apply_sculpt_object_to_shapekey", text = 'Apply Sculpt to Shapekey')
                                row_sculpt = box_weight.row()
                                row_sculpt.prop(guide_props, "sculpt_use_smooth", text='Use Smooth Modifiers')
                                row_sculpt.operator("blenrig.reset_shapekey", text = 'Reset Active Shapekey')
                else:
                    box_weight.operator("blenrig.toggle_shapekey_editting", text='Toggle Shapekey Editting').mesh_edit_object = 'char'
                    if hasattr(active, 'modifiers'):
                        if active_mode != 'WEIGHT_PAINT':
                            for mod in active.modifiers:
                                if mod.type == 'CORRECTIVE_SMOOTH':
                                    box_weight.operator("blenrig.edit_corrective_smooth_vgroup", text='Edit Corrective Smooth Vgroup')
                    if hasattr(active, 'data') and hasattr(active.data, 'shape_keys') and hasattr(active.data.shape_keys, 'key_blocks'):
                        box_weight.label(text='Sculpt Shapekey')
                        row_sculpt = box_weight.row()
                        if active.active_shape_key.name.endswith('_L'):
                            row_sculpt.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').X_Mirror = False
                        elif active.active_shape_key.name.endswith('_R'):
                            row_sculpt.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').X_Mirror = False
                        else:
                            row_sculpt.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').X_Mirror = True
                        row_sculpt.operator("blenrig.apply_sculpt_object_to_shapekey", text = 'Apply Sculpt to Shapekey')
                        row_sculpt = box_weight.row()
                        row_sculpt.prop(guide_props, "sculpt_use_smooth", text='Use Smooth Modifiers')
                        row_sculpt.operator("blenrig.reset_shapekey", text = 'Reset Active Shapekey')

                if active_mode == 'POSE':
                    box_weight.label(text='Pose Options')
                    mirror_row = box_weight.row()
                    mirror_row.prop(guide_props.arm_obj.pose, "use_mirror_x", text='X-Axis Mirror (Pose)')
                    mirror_row.prop(guide_props, 'guide_show_wp_bones', text='Show All Bones')
                    mirror_row.prop(guide_props.arm_obj, 'show_in_front')
                if active_mode == 'EDIT' or active_mode == 'WEIGHT_PAINT':
                    box_weight.label(text='Shapekeys Editting Options')
                    mirror_row = box_weight.row()
                    mirror_row.prop(active.data, "use_mirror_x", text='X-Mirror')
                    mirror_row.prop(active.data, "use_mirror_topology")
                    if hasattr(active, 'modifiers'):
                        for mod in active.modifiers:
                            if mod.type == 'SUBSURF':
                                mirror_row.prop(mod, "show_in_editmode", text='Toggle Subsurf')
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
                if guide_props.guide_transformation_bone == 'spine_1_fk':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Pelvis / Spine 1 Pose')
                box_pose = steps.box()
                #Spine 2
                if guide_props.guide_transformation_bone == 'spine_2_fk':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Spine 2 Pose')
                box_pose = steps.box()
                #Spine 3
                if guide_props.guide_transformation_bone == 'spine_3_fk':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Spine 3 Pose')
            #Cage Neck
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Neck':
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
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Neck 1 Pose')
                box_pose = steps.box()
                #Neck 2
                if guide_props.guide_transformation_bone == 'neck_2_fk':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Neck 2 Pose')
                box_pose = steps.box()
                #Neck 3
                if guide_props.guide_transformation_bone == 'neck_3_fk':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Neck 3 Pose')
                #Head
                if guide_props.guide_transformation_bone == 'head_fk':
                    box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Head Pose')
            #Cage Clavicle
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Clavicle':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Collarbone Pose')
            #Cage Shoulder
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Shoulder':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Arm Pose')
            #Cage Elbow
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Elbow':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Forearm Pose')
            #Cage Wrist
            if guide_props.guide_current_step == 'SHAPEKEYS_Cage_Wrist':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Wrist Pose')
            #Add Fingers Shapekeys
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Add_Fingers_Shapes':
                box_pose = steps.box()
                box_pose.label(text='Add Fingers Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.add_fingers_shapekeys", text = 'Add Fingers Shapekeys')
                #Char Thumb 1
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Thumb_1':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Thumb Pose')
                #Char Little 1
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Lit_1':
                box_pose = steps.box()
            #Char Thumb Joints
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Thumb_Joints':
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
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Thumb Pose')
                #Char Index Joints
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Index_Joints':
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
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Index Pose')
                #Char Middle Joints
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Middle_Joints':
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
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Middle Pose')
                #Char Ring Joints
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Ring_Joints':
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
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Ring Pose')
                #Char Little Joints
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Little_Joints':
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
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Little Pose')
            #Add Face Shapekeys
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Add_Face_Shapes':
                box_pose = steps.box()
                box_pose.label(text='Add Face Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.add_face_shapekeys", text = 'Add Face Shapekeys')
                #Char Eyebrow Up
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Eyebrow_Up':
                box_pose = steps.box()
                box_pose.label(text='Apply Current Shape to Brow Up Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.blend_from_shape", text='Apply Shape').operation = 'brow_up_L'
                #Char Eyebrow Down
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Eyebrow_Down':
                box_pose = steps.box()
                box_pose.label(text='Apply Current Shape to Brow Down Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.blend_from_shape", text='Apply Shape').operation = 'brow_down_L'
                #Char Eyebrow Weights
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Eyebrow_Weight':
                box_pose = steps.box()
                box_pose.label(text='Select Shapekey Vertex Group', icon='BONE_DATA')
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
                joint_col_2.label(text=active.vertex_groups.active.name.upper())
                joint_col_3.operator("blenrig.wp_joint_chain_up", icon='TRIA_RIGHT', text='')
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Eyebrow Pose')
                steps.separator()
                box_weight = steps.box()
                box_weight.label(text='Weight Painting Options')
                mirror_row = box_weight.row()
                if active_mode == 'WEIGHT_PAINT':
                    mirror_row.prop(active.data, "use_mirror_x", text='X-Mirror')
                    mirror_row.prop(active.data, "use_mirror_topology")
            #Cheeks
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Cheeks':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Cheek Pose')
            #Nose
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Nostril':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Nostril Pose')
            #Mouth Corner Base
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_Corner_Base':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X6", text='Mouth Corner Pose')
            #Mouth Corner Fix 1
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_Corner_Fix_1':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Mouth Corner Pose')
            #Mouth Corner Fix 2
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_Corner_Fix_2':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X4", text='Mouth Corner Pose')
                #Char Mouth Weights
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_Weight':
                box_pose = steps.box()
                box_pose.label(text='Select Shapekey Vertex Group', icon='BONE_DATA')
                joint_row = box_pose.row()
                joint_row.alignment = 'CENTER'
                joint_row.scale_x = BL_Ver(1, 0.9)
                joint_col_1 = joint_row.column()
                joint_col_1.alignment = 'CENTER'
                joint_col_2 = joint_row.column()
                joint_col_2.alignment = 'CENTER'
                joint_col_3 = joint_row.column()
                joint_col_3.alignment = 'CENTER'
                joint_col_1.operator("blenrig.wp_vgroup_chain_down", icon='TRIA_LEFT', text='')
                joint_col_2.label(text=active.vertex_groups.active.name.upper())
                joint_col_3.operator("blenrig.wp_vgroup_chain_up", icon='TRIA_RIGHT', text='')
                steps.separator()
                box_weight = steps.box()
                box_weight.label(text='Weight Painting Options')
                mirror_row = box_weight.row()
                if active_mode == 'WEIGHT_PAINT':
                    mirror_row.prop(active.data, "use_mirror_x", text='X-Mirror')
                    mirror_row.prop(active.data, "use_mirror_topology")
                #Char Mouth U
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_U':
                box_pose = steps.box()
                box_pose.label(text='Apply Current Shape to U Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.blend_from_shape", text='Apply Shape').operation = 'U'
                #Char Mouth U Thickness
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_U_Thickness':
                box_pose = steps.box()
                box_pose.label(text='Apply Current Shape to U_Thickness Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.blend_from_shape", text='Apply Shape').operation = 'U_Thickness'
                #Char Mouth M
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_M':
                box_pose = steps.box()
                box_pose.label(text='Apply Current Shape to M Shapekeys', icon='ARMATURE_DATA')
                box_pose.operator("blenrig.blend_from_shape", text='Apply Shape').operation = 'M'
            #Mouth Open Down
            if guide_props.guide_current_step == 'SHAPEKEYS_Char_Mouth_Open_Close':
                box_pose = steps.box()
                box_pose.label(text='Set Joint Transforms', icon='ARMATURE_DATA')
                box_pose.prop(guide_props, "guide_joint_transforms_X2", text='Jaw Pose')
            #General Options
            if guide_props.guide_current_step not in exclude_list:
                box_pose.label(text='Active Shapekey:')
                row_shape = box_pose.row()
                row_shape.alignment = 'CENTER'
                if hasattr(guide_props.active_shp_obj, 'active_shape_key') and hasattr(guide_props.active_shp_obj.active_shape_key, 'name'):
                    row_shape.label(text=str(guide_props.active_shp_obj.active_shape_key.name.upper()) + " (value: " + str(round(guide_props.active_shp_obj.active_shape_key.value, 1)) + ")",
                    icon="{}".format('KEYTYPE_EXTREME_VEC' if guide_props.active_shp_obj.active_shape_key.value < 0.5
                    else ('KEYTYPE_KEYFRAME_VEC' if guide_props.active_shp_obj.active_shape_key.value >= 0.5 and guide_props.active_shp_obj.active_shape_key.value < 0.8
                    else ('KEYTYPE_JITTER_VEC'))))
                if guide_props.guide_current_step not in facial_drivers_list:
                    box_pose.label(text='Drivers:')
                    row_drivers = box_pose.row()
                    row_drivers.operator("blenrig.update_shapekey_driver", text='Update Driver with Current Pose')
                if not guide_props.auto_mirror_shapekeys:
                    row_drivers.operator("blenrig.mirror_active_shapekey_driver", text='Mirror Active Shapekey Driver')
                box_pose.label(text='Mirroring:')
                box_pose.prop(guide_props, "auto_mirror_shapekeys", text='Auto Mirror Shapekeys')
                if not guide_props.auto_mirror_shapekeys:
                    if guide_props.active_shp_obj.data.use_mirror_topology == True:
                        box_pose.operator("blenrig.mirror_active_shapekey", text='Mirror Active Shapekey').type='MIRROR_TOPOLOGY'
                    else:
                        box_pose.operator("blenrig.mirror_active_shapekey", text='Mirror Active Shapekey').type='MIRROR'
        if '_BlenRigSculptShapekey' in active.name:
            box_weight = steps.box()
            box_weight.label(text='Sculpt Shapekey')
            row_sculpt = box_weight.row()
            row_sculpt.operator("blenrig.apply_sculpt_object_to_shapekey", text = 'Apply Sculpt to Shapekey')
            row_sculpt.operator("blenrig.cancel_sculpt_object_to_shapekey", text = 'Cancel')
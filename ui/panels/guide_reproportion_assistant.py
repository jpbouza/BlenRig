import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_reproportion
from . assistant_base import BLENRIG_PT_guide_assistant

####### Repoportion assistant Guide

class BLENRIG_PT_reproportion_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Repoportion Assistant Guide"
    bl_idname = "BLENRIG_PT_reproportion_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_reproportion.is_instantiated(context):
            return
        
        if bpy.app.version < (3,0,0):
            bbone_curveiny = "bbone_curveiny"
            bbone_curveouty = "bbone_curveouty"
        else:
            bbone_curveouty = "bbone_curveoutz"
            bbone_curveiny = "bbone_curveinz"

        layout = self.layout
        arm = context.active_object
        active = context.active_object
        guide_props = bpy.context.scene.blenrig_guide
        if hasattr(arm, 'pose') and hasattr(arm.pose, 'bones'):
            pose = arm.pose
            p_bones = arm.pose.bones

            #General
            exclude = ['Reprop_Intro', 'Reprop_Bake', 'Reprop_Custom_Alignments', 'Reprop_Finish']
            if guide_props.guide_current_step not in exclude:
                steps = layout.column(align=True)
                box = steps.box()
                row_bones = box.row()
                row_bones.prop(guide_props, "guide_lock_center_bones")
                row_bones.prop(guide_props, 'guide_show_wp_bones', text='Show All Bones')
                row_display = box.row()
                row_display.prop(pose, "use_mirror_x")
                row_display.prop(arm, "show_in_front")
                box.prop(guide_props.arm_obj.data, "display_type")
            # Set Spine Curve Values Step
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Spine_Line':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Spine Curvature")
                row_props = box.row()
                col = row_props.column()
                try:
                    col.prop(p_bones['spine_line'].bone, bbone_curveoutz, text="Upper Curvature")
                    col.prop(p_bones['spine_line'].bone, bbone_curveinz,  text="Lower Curvature")
                except:
                    col.prop(p_bones['spine_line'].bone, bbone_curveouty, text="Upper Curvature")
                    col.prop(p_bones['spine_line'].bone, bbone_curveiny,  text="Lower Curvature")
                    pass
            # Fingers Toggles
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Fingers':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Fingers Toggles")
                col = box.column()
                col.label(text='General Toggle')
                row_props = col.row()
                try:
                    row_props.prop(p_bones['properties_arm_R'], "toggle_fingers_R", text="Toggle All Right Fingers")
                    row_props.prop(p_bones['properties_arm_L'], "toggle_fingers_L", text="Toggle All Left Fingers")
                except:
                    pass
                col = box.column()
                col.label(text='Individual Toggles')
                row_props = col.row()
                col_R = row_props.column()
                col_L = row_props.column()
                try:
                    col_R.prop(p_bones['properties_arm_R'], "toggle_fingers_thumb_R", text="Right Thumb")
                    col_R.prop(p_bones['properties_arm_R'], "toggle_fingers_index_R", text="Right Index")
                    col_R.prop(p_bones['properties_arm_R'], "toggle_fingers_middle_R", text="Right Middle")
                    col_R.prop(p_bones['properties_arm_R'], "toggle_fingers_ring_R", text="Right Ring")
                    col_R.prop(p_bones['properties_arm_R'], "toggle_fingers_little_R", text="Right Little")
                except:
                    pass
                try:
                    col_L.prop(p_bones['properties_arm_L'], "toggle_fingers_thumb_L", text="Left Thumb")
                    col_L.prop(p_bones['properties_arm_L'], "toggle_fingers_index_L", text="Left Index")
                    col_L.prop(p_bones['properties_arm_L'], "toggle_fingers_middle_L", text="Left Middle")
                    col_L.prop(p_bones['properties_arm_L'], "toggle_fingers_ring_L", text="Left Ring")
                    col_L.prop(p_bones['properties_arm_L'], "toggle_fingers_little_L", text="Left Little")
                except:
                    pass
            # Toes Toggles
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Toes':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Toes Toggles")
                col = box.column()
                col.label(text='General Toggle')
                row_props = col.row()
                try:
                    row_props.prop(p_bones['properties_leg_R'], "toggle_toes_R", text="Toggle All Right Toes")
                    row_props.prop(p_bones['properties_leg_L'], "toggle_toes_L", text="Toggle All Left Toes")
                except:
                    pass
                col = box.column()
                col.label(text='Individual Toggles')
                row_props = col.row()
                col_R = row_props.column()
                col_L = row_props.column()
                try:
                    col_R.prop(p_bones['properties_leg_R'], "toggle_toes_big_R", text="Right Big")
                    col_R.prop(p_bones['properties_leg_R'], "toggle_toes_index_R", text="Right Index")
                    col_R.prop(p_bones['properties_leg_R'], "toggle_toes_middle_R", text="Right Middle")
                    col_R.prop(p_bones['properties_leg_R'], "toggle_toes_fourth_R", text="Right Fourth")
                    col_R.prop(p_bones['properties_leg_R'], "toggle_toes_little_R", text="Right Little")
                except:
                    pass
                try:
                    col_L.prop(p_bones['properties_leg_L'], "toggle_toes_big_L", text="Left Big")
                    col_L.prop(p_bones['properties_leg_L'], "toggle_toes_index_L", text="Left Index")
                    col_L.prop(p_bones['properties_leg_L'], "toggle_toes_middle_L", text="Left Middle")
                    col_L.prop(p_bones['properties_leg_L'], "toggle_toes_fourth_L", text="Left Fourth")
                    col_L.prop(p_bones['properties_leg_L'], "toggle_toes_little_L", text="Left Little")
                except:
                    pass
            # Set Eye Location
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Set_Eyes':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Set Eyes Location")
                box.operator("blenrig.snap_bone_to_cursor", text="Snap Eye to Cursor")

            # Set Eyebrow Curve Values Step
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Eyebrows_Curve':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Curve Values")
                curvey = box.column()
                # Bbone Y Values
                vert = curvey.row()
                vert.alignment = 'CENTER'
                curveiny = curvey.row()
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_in_brows", text="Vertical In")
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_out_brows",  text="Vertical Out")
                # Bbone X Values
                curvex = box.column()
                depth = curvex.row()
                depth.alignment = 'CENTER'
                curveinx = curvex.row()
                curveinx.prop(guide_props, "guide_bbone_depth_curve_in_brows", text="Depth in")
                curveinx.prop(guide_props, "guide_bbone_depth_curve_out_brows",  text="Depth Out")
                # # Bbone Y Values
                # vert = curvey.row()
                # vert.alignment = 'CENTER'
                # vert.label(text="Vertical")
                # curveiny = curvey.row()
                # try:
                #     curveiny.prop(p_bones['brow_line_R'].bone, bbone_curveinz, text="Curve in Y Right")
                #     curveiny.prop(p_bones['brow_line_L'].bone, bbone_curveinz,  text="Curve in Y Left")
                # except:
                #     curveiny.prop(p_bones['brow_line_R'].bone, bbone_curveiny, text="Curve in Y Right")
                #     curveiny.prop(p_bones['brow_line_L'].bone, bbone_curveiny,  text="Curve in Y Left")
                # curveouty = curvey.row()
                # try:
                #     curveouty.prop(p_bones['brow_line_R'].bone, bbone_curveoutz, text="Curve out Y Right")
                #     curveouty.prop(p_bones['brow_line_L'].bone, bbone_curveoutz,  text="Curve out Y Left")
                # except:
                #     curveouty.prop(p_bones['brow_line_R'].bone, bbone_curveouty, text="Curve out Y Right")
                #     curveouty.prop(p_bones['brow_line_L'].bone, bbone_curveouty,  text="Curve out Y Left")
                # # Bbone X Values
                # curvex = box.column()
                # depth = curvex.row()
                # depth.alignment = 'CENTER'
                # depth.label(text="Depth")
                # curveinx = curvex.row()
                # try:
                #     curveinx.prop(p_bones['brow_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                #     curveinx.prop(p_bones['brow_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                # except:
                #     pass
                # curveoutx = curvex.row()
                # try:
                #     curveoutx.prop(p_bones['brow_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                #     curveoutx.prop(p_bones['brow_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                # except:
                #     pass

            # Set Mouth Curve Values Step
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Mouth_Curves':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Curve Values")
                curvey = box.column()
                # Bbone Y Values
                vert = curvey.row()
                vert.alignment = 'CENTER'
                # Lip Up
                lipup = curvey.row()
                lipup.alignment = 'LEFT'
                lipup.label(text="Upper Lips")
                curveiny = curvey.row()
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_in_lip_up", text="Vertical In")
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_out_lip_up",  text="Vertical Out")
                curveouty = curvey.row()
                curveouty.prop(guide_props, "guide_bbone_depth_curve_in_lip_up", text="Depth In")
                curveouty.prop(guide_props, "guide_bbone_depth_curve_out_lip_up",  text="Depth Out")
                # Lip Zipper
                lipzip = curvey.row()
                lipzip.alignment = 'LEFT'
                lipzip.label(text="Zipper")
                curveiny = curvey.row()
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_in_lip_zipper", text="Vertical In")
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_out_lip_zipper",  text="Vertical Out")
                curveouty = curvey.row()
                curveouty.prop(guide_props, "guide_bbone_depth_curve_in_lip_zipper", text="Depth In")
                curveouty.prop(guide_props, "guide_bbone_depth_curve_out_lip_zipper",  text="Depth Out")
                # Lip Low
                lipzip = curvey.row()
                lipzip.alignment = 'LEFT'
                lipzip.label(text="Lower Lips")
                curveiny = curvey.row()
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_in_lip_low", text="Vertical In")
                curveiny.prop(guide_props, "guide_bbone_vertical_curve_out_lip_low",  text="Vertical Out")
                curveouty = curvey.row()
                curveouty.prop(guide_props, "guide_bbone_depth_curve_in_lip_low", text="Depth In")
                curveouty.prop(guide_props, "guide_bbone_depth_curve_out_lip_low",  text="Depth Out")

                # # Bbone Y Values
                # vert = curvey.row()
                # vert.alignment = 'CENTER'
                # vert.label(text="Vertical")
                # # Lip Up
                # lipup = curvey.row()
                # lipup.alignment = 'LEFT'
                # lipup.label(text="Upper Lips")
                # curveiny = curvey.row()
                # try:
                #     curveiny.prop(p_bones['lip_up_line_R'].bone, "bbone_curveinz", text="Curve in Y Right")
                #     curveiny.prop(p_bones['lip_up_line_L'].bone, "bbone_curveinz",  text="Curve in Y Left")
                # except:
                #     curveiny.prop(p_bones['lip_up_line_R'].bone, "bbone_curveiny", text="Curve in Y Right")
                #     curveiny.prop(p_bones['lip_up_line_L'].bone, "bbone_curveiny",  text="Curve in Y Left")
                # curveouty = curvey.row()
                # try:
                #     curveouty.prop(p_bones['lip_up_line_R'].bone, bbone_curveoutz, text="Curve out Y Right")
                #     curveouty.prop(p_bones['lip_up_line_L'].bone, bbone_curveoutz,  text="Curve out Y Left")
                # except:
                #     curveouty.prop(p_bones['lip_up_line_R'].bone, bbone_curveouty, text="Curve out Y Right")
                #     curveouty.prop(p_bones['lip_up_line_L'].bone, bbone_curveouty,  text="Curve out Y Left")
                # # Lip Zipper
                # lipzip = curvey.row()
                # lipzip.alignment = 'LEFT'
                # lipzip.label(text="Zipper")
                # curveiny = curvey.row()
                # try:
                #     curveiny.prop(p_bones['lip_zipper_line_R'].bone, bbone_curveinz, text="Curve in Y Right")
                #     curveiny.prop(p_bones['lip_zipper_line_L'].bone, bbone_curveinz,  text="Curve in Y Left")
                # except:
                #     curveiny.prop(p_bones['lip_zipper_line_R'].bone, bbone_curveiny, text="Curve in Y Right")
                #     curveiny.prop(p_bones['lip_zipper_line_L'].bone, bbone_curveiny,  text="Curve in Y Left")
                # curveouty = curvey.row()
                # try:
                #     curveouty.prop(p_bones['lip_zipper_line_R'].bone, bbone_curveoutz, text="Curve out Y Right")
                #     curveouty.prop(p_bones['lip_zipper_line_L'].bone, bbone_curveoutz,  text="Curve out Y Left")
                # except:
                #     curveouty.prop(p_bones['lip_zipper_line_R'].bone, bbone_curveouty, text="Curve out Y Right")
                #     curveouty.prop(p_bones['lip_zipper_line_L'].bone, bbone_curveouty,  text="Curve out Y Left")
                # # Lip Low
                # lipzip = curvey.row()
                # lipzip.alignment = 'LEFT'
                # lipzip.label(text="Lower Lips")
                # curveiny = curvey.row()
                # try:
                #     curveiny.prop(p_bones['lip_low_line_R'].bone, bbone_curveinz, text="Curve in Y Right")
                #     curveiny.prop(p_bones['lip_low_line_L'].bone, bbone_curveinz,  text="Curve in Y Left")
                # except:
                #     curveiny.prop(p_bones['lip_low_line_R'].bone, bbone_curveiny, text="Curve in Y Right")
                #     curveiny.prop(p_bones['lip_low_line_L'].bone, bbone_curveiny,  text="Curve in Y Left")
                # curveouty = curvey.row()
                # try:
                #     curveouty.prop(p_bones['lip_low_line_R'].bone, bbone_curveoutz, text="Curve out Y Right")
                #     curveouty.prop(p_bones['lip_low_line_L'].bone, bbone_curveoutz,  text="Curve out Y Left")
                # except:
                #     curveouty.prop(p_bones['lip_low_line_R'].bone, bbone_curveouty, text="Curve out Y Right")
                #     curveouty.prop(p_bones['lip_low_line_L'].bone, bbone_curveouty,  text="Curve out Y Left")

                # # Bbone X Values
                # curvex = box.column()
                # depth = curvex.row()
                # depth.alignment = 'CENTER'
                # depth.label(text="Depth")
                # # Lip Up
                # lipup = curvex.row()
                # lipup.alignment = 'LEFT'
                # lipup.label(text="Upper Lips")
                # curveinx = curvex.row()
                # try:
                #     curveinx.prop(p_bones['lip_up_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                #     curveinx.prop(p_bones['lip_up_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                # except:
                #     pass
                # curveoutx = curvex.row()
                # try:
                #     curveoutx.prop(p_bones['lip_up_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                #     curveoutx.prop(p_bones['lip_up_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                # except:
                #     pass
                # # Lip Zipper
                # lipup = curvex.row()
                # lipup.alignment = 'LEFT'
                # lipup.label(text="Zipper")
                # curveinx = curvex.row()
                # try:
                #     curveinx.prop(p_bones['lip_zipper_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                #     curveinx.prop(p_bones['lip_zipper_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                # except:
                #     pass
                # curveoutx = curvex.row()
                # try:
                #     curveoutx.prop(p_bones['lip_zipper_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                #     curveoutx.prop(p_bones['lip_zipper_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                # except:
                #     pass
                # # Lip Low
                # lipup = curvex.row()
                # lipup.alignment = 'LEFT'
                # lipup.label(text="Lower Lips")
                # curveinx = curvex.row()
                # try:
                #     curveinx.prop(p_bones['lip_low_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                #     curveinx.prop(p_bones['lip_low_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                # except:
                #     pass
                # curveoutx = curvex.row()
                # try:
                #     curveoutx.prop(p_bones['lip_low_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                #     curveoutx.prop(p_bones['lip_low_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                # except:
                #     pass

            # Diplay Bake Button
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Bake':
                if context.mode in ['POSE','OBJECT']:
                    if context.active_object.data.reproportion:
                        steps = layout.column(align=True)
                        box = steps.box()
                        row = box.row()
                        row.scale_x = 0.5
                        row.scale_y = 1.8
                        row.operator("blenrig.armature_baker_all_part_1", text="Bake All")

            # Diplay Bake Button
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_Custom_Alignments':
                steps = layout.column(align=True)
                box = steps.box()
                row = box.row()
                row.scale_x = 0.5
                row.scale_y = 1.8
                row.operator("blenrig.armature_baker_all_part_2", text="Custom Alignments")
            # IK Check
            if context.scene.blenrig_guide.guide_current_step == 'Reprop_IK_Check':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="IK Rotation Override")
                row_props = box.row()
                col_R = row_props.column()
                col_L = row_props.column()
                for b in p_bones:
                    if '_R' in b.name:
                        if 'forearm' in b.name:
                            for C in b.constraints:
                                if C.name == 'IK_Initial_Rotation':
                                    col_R.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)
                for b in p_bones:
                    if '_R' in b.name:
                        if 'shin' in b.name:
                            for C in b.constraints:
                                if C.name == 'IK_Initial_Rotation':
                                    col_R.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)
                for b in p_bones:
                    if '_L' in b.name:
                        if 'forearm' in b.name:
                            for C in b.constraints:
                                if C.name == 'IK_Initial_Rotation':
                                    col_L.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)
                for b in p_bones:
                    if '_L' in b.name:
                        if 'shin' in b.name:
                            for C in b.constraints:
                                if C.name == 'IK_Initial_Rotation':
                                    col_L.prop(C, 'to_min_x_rot', text = "{}".format(b.name), toggle=True)

        # Edit Mask
        if context.scene.blenrig_guide.guide_current_step == 'Reprop_Edit_Face':
            steps = layout.column(align=True)
            box = steps.box()
            box.label(text="Mask Editing Options")
            mirror_row = box.row()
            if active.mode == 'EDIT':
                mirror_row.prop(active.data, "use_mirror_x", text='X-Mirror')
                mirror_row.prop(active.data, "use_mirror_topology")
                mirror_row.prop(active, "show_in_front")
                mirror_row.prop(guide_props, 'guide_show_wp_bones', text='Show All Bones')
                box.prop(active, "display_type")

                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Snap vertex to Face")
                box.operator("blenrig.snap_points", text="Snap")

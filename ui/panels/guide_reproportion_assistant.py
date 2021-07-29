import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_reproportion
from . assistant_base import BLENRIG_PT_guide_assistant

####### Repoportion assistant Guide

class BLENRIG_PT_reproportion_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Repoportion Assistant Guide"
    bl_idname = "BLENRIG_PT_reproportion_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"

    def draw(self, context):
        layout = self.layout
        arm = context.active_object
        arm_data = context.active_object.data
        if hasattr(arm, 'pose') and hasattr(arm.pose, 'bones'):
            pose = arm.pose
            p_bones = arm.pose.bones

            # Step 0 X-Mirror
            if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Symmetry':
                steps = layout.column(align=True)
                box = steps.box()
                box.prop(pose, "use_mirror_x")

            # Set Spine Curve Values Step
            if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Spine_Line':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Spine Curvature")
                row_props = box.row()
                col = row_props.column()
                try:
                    col.prop(p_bones['spine_line'].bone, "bbone_curveouty", text="Upper Curvature")
                    col.prop(p_bones['spine_line'].bone, "bbone_curveiny",  text="Lower Curvature")
                except:
                    pass

            # Set Eyebrow Curve Values Step
            if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Eyebrows_Curve':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Curve Values")
                curvey = box.column()
                # Bbone Y Values
                vert = curvey.row()
                vert.alignment = 'CENTER'
                vert.label(text="Vertical")
                curveiny = curvey.row()
                try:
                    curveiny.prop(p_bones['brow_line_R'].bone, "bbone_curveiny", text="Curve in Y Right")
                    curveiny.prop(p_bones['brow_line_L'].bone, "bbone_curveiny",  text="Curve in Y Left")
                except:
                    pass
                curveouty = curvey.row()
                try:
                    curveouty.prop(p_bones['brow_line_R'].bone, "bbone_curveouty", text="Curve out Y Right")
                    curveouty.prop(p_bones['brow_line_L'].bone, "bbone_curveouty",  text="Curve out Y Left")
                except:
                    pass
                # Bbone X Values
                curvex = box.column()
                depth = curvex.row()
                depth.alignment = 'CENTER'
                depth.label(text="Depth")
                curveinx = curvex.row()
                try:
                    curveinx.prop(p_bones['brow_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                    curveinx.prop(p_bones['brow_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                except:
                    pass
                curveoutx = curvex.row()
                try:
                    curveoutx.prop(p_bones['brow_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                    curveoutx.prop(p_bones['brow_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                except:
                    pass

            # Set Mouth Curve Values Step
            if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Mouth_Curves':
                steps = layout.column(align=True)
                box = steps.box()
                box.label(text="Curve Values")
                curvey = box.column()
                # Bbone Y Values
                vert = curvey.row()
                vert.alignment = 'CENTER'
                vert.label(text="Vertical")
                # Lip Up
                lipup = curvey.row()
                lipup.alignment = 'LEFT'
                lipup.label(text="Upper Lips")
                curveiny = curvey.row()
                try:
                    curveiny.prop(p_bones['lip_up_line_R'].bone, "bbone_curveiny", text="Curve in Y Right")
                    curveiny.prop(p_bones['lip_up_line_L'].bone, "bbone_curveiny",  text="Curve in Y Left")
                except:
                    pass
                curveouty = curvey.row()
                try:
                    curveouty.prop(p_bones['lip_up_line_R'].bone, "bbone_curveouty", text="Curve out Y Right")
                    curveouty.prop(p_bones['lip_up_line_L'].bone, "bbone_curveouty",  text="Curve out Y Left")
                except:
                    pass
                # Lip Zipper
                lipzip = curvey.row()
                lipzip.alignment = 'LEFT'
                lipzip.label(text="Zipper")
                curveiny = curvey.row()
                try:
                    curveiny.prop(p_bones['lip_zipper_line_R'].bone, "bbone_curveiny", text="Curve in Y Right")
                    curveiny.prop(p_bones['lip_zipper_line_L'].bone, "bbone_curveiny",  text="Curve in Y Left")
                except:
                    pass
                curveouty = curvey.row()
                try:
                    curveouty.prop(p_bones['lip_zipper_line_R'].bone, "bbone_curveouty", text="Curve out Y Right")
                    curveouty.prop(p_bones['lip_zipper_line_L'].bone, "bbone_curveouty",  text="Curve out Y Left")
                except:
                    pass
                # Lip Low
                lipzip = curvey.row()
                lipzip.alignment = 'LEFT'
                lipzip.label(text="Lower Lips")
                curveiny = curvey.row()
                try:
                    curveiny.prop(p_bones['lip_low_line_R'].bone, "bbone_curveiny", text="Curve in Y Right")
                    curveiny.prop(p_bones['lip_low_line_L'].bone, "bbone_curveiny",  text="Curve in Y Left")
                except:
                    pass
                curveouty = curvey.row()
                try:
                    curveouty.prop(p_bones['lip_low_line_R'].bone, "bbone_curveouty", text="Curve out Y Right")
                    curveouty.prop(p_bones['lip_low_line_L'].bone, "bbone_curveouty",  text="Curve out Y Left")
                except:
                    pass

                # Bbone X Values
                curvex = box.column()
                depth = curvex.row()
                depth.alignment = 'CENTER'
                depth.label(text="Depth")
                # Lip Up
                lipup = curvex.row()
                lipup.alignment = 'LEFT'
                lipup.label(text="Upper Lips")
                curveinx = curvex.row()
                try:
                    curveinx.prop(p_bones['lip_up_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                    curveinx.prop(p_bones['lip_up_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                except:
                    pass
                curveoutx = curvex.row()
                try:
                    curveoutx.prop(p_bones['lip_up_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                    curveoutx.prop(p_bones['lip_up_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                except:
                    pass
                # Lip Zipper
                lipup = curvex.row()
                lipup.alignment = 'LEFT'
                lipup.label(text="Zipper")
                curveinx = curvex.row()
                try:
                    curveinx.prop(p_bones['lip_zipper_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                    curveinx.prop(p_bones['lip_zipper_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                except:
                    pass
                curveoutx = curvex.row()
                try:
                    curveoutx.prop(p_bones['lip_zipper_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                    curveoutx.prop(p_bones['lip_zipper_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                except:
                    pass
                # Lip Low
                lipup = curvex.row()
                lipup.alignment = 'LEFT'
                lipup.label(text="Lower Lips")
                curveinx = curvex.row()
                try:
                    curveinx.prop(p_bones['lip_low_line_R'].bone, "bbone_curveinx", text="Curve in X Right")
                    curveinx.prop(p_bones['lip_low_line_L'].bone, "bbone_curveinx",  text="Curve in X Left")
                except:
                    pass
                curveoutx = curvex.row()
                try:
                    curveoutx.prop(p_bones['lip_low_line_R'].bone, "bbone_curveoutx", text="Curve out X Right")
                    curveoutx.prop(p_bones['lip_low_line_L'].bone, "bbone_curveoutx",  text="Curve out X Left")
                except:
                    pass

            # Diplay Bake Button
            if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Bake':
                if context.mode in ['POSE','OBJECT']:
                    if context.active_object.data.reproportion:
                        steps = layout.column(align=True)
                        box = steps.box()
                        row = box.row()
                        row.scale_x = 0.5
                        row.scale_y = 1.8
                        row.operator("blenrig.armature_baker_all_part_1", text="Bake All")

            # Diplay Bake Button
            if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Custom_Alignments':
                if context.mode in ['EDIT_ARMATURE']:
                    if context.active_object.data.reproportion:
                        steps = layout.column(align=True)
                        box = steps.box()
                        row = box.row()
                        row.scale_x = 0.5
                        row.scale_y = 1.8
                        row.operator("blenrig.armature_baker_all_part_2", text="Custom Alignments")

        # # Diplay Mode for Face Mask
        # if VIEW3D_OT_blenrig_guide_reproportion.instance and context.scene.blenrig_guide.guide_current_step == 'Reprop_Edit_Face':
        #     steps = layout.column(align=True)
        #     box = steps.box()
        #     box.label(text="Display As")
        #     box.prop(arm, "display_type")

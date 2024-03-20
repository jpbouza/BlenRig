import bpy

class BLENRIG_PT_Rig_Body_settings_face_bendy_bones_settings(bpy.types.Panel):
    bl_label = "Facial BBones Settings:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_face_bendy_bones_settings"
    bl_parent_id = "BLENRIG_PT_Rig_Facial_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        if bpy.app.version < (3,0,0):
            bbone_curveiny = "bbone_curveiny"
            bbone_curveouty = "bbone_curveouty"
            axis = " Y "
            
        else:
            bbone_curveouty = "bbone_curveoutz"
            bbone_curveiny = "bbone_curveinz"
            axis = " Z "

        arm = context.active_object
        arm_data = context.active_object.data
        p_bones = arm.pose.bones
        layout = self.layout

        if "gui_rig_face" in arm_data:
            props = context.window_manager.blenrig_6_props
            box = layout.column()
            col = box.column()
            row = col.row()

            #EYEBROWS
            box = col.box()
            box.label(text="Eyebrows Curve Values")
            curvey = box.column()
            # Bbone Y Values
            vert = curvey.row()
            vert.alignment = 'CENTER'
            vert.label(text="Vertical")
            curveiny = curvey.row()
            try:
                curveiny.prop(p_bones['brow_line_R'].bone, bbone_curveiny, text="Curve in" + axis + "Right")
                curveiny.prop(p_bones['brow_line_L'].bone, bbone_curveiny,  text="Curve in" + axis + "Left")
            except:
                pass
            curveouty = curvey.row()
            try:
                curveouty.prop(p_bones['brow_line_R'].bone, bbone_curveouty, text="Curve out" + axis + "Right")
                curveouty.prop(p_bones['brow_line_L'].bone, bbone_curveouty,  text="Curve out" + axis + "Left")
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
            box.separator()

            #LIPS
            box = col.box()
            box.label(text="Lips Curve Values")
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
                curveiny.prop(p_bones['lip_up_line_R'].bone, bbone_curveiny, text="Curve in" + axis + "Right")
                curveiny.prop(p_bones['lip_up_line_L'].bone, bbone_curveiny,  text="Curve in" + axis + "Left")
            except:
                pass
            curveouty = curvey.row()
            try:
                curveouty.prop(p_bones['lip_up_line_R'].bone, bbone_curveouty, text="Curve out" + axis + "Right")
                curveouty.prop(p_bones['lip_up_line_L'].bone, bbone_curveouty,  text="Curve out" + axis + "Left")
            except:
                pass
            # Lip Zipper
            lipzip = curvey.row()
            lipzip.alignment = 'LEFT'
            lipzip.label(text="Zipper")
            curveiny = curvey.row()
            try:
                curveiny.prop(p_bones['lip_zipper_line_R'].bone, bbone_curveiny, text="Curve in" + axis + "Right")
                curveiny.prop(p_bones['lip_zipper_line_L'].bone, bbone_curveiny,  text="Curve in" + axis + "Left")
            except:
                pass
            curveouty = curvey.row()
            try:
                curveouty.prop(p_bones['lip_zipper_line_R'].bone, bbone_curveouty, text="Curve out" + axis + "Right")
                curveouty.prop(p_bones['lip_zipper_line_L'].bone, bbone_curveouty,  text="Curve out" + axis + "Left")
            except:
                pass
            # Lip Low
            lipzip = curvey.row()
            lipzip.alignment = 'LEFT'
            lipzip.label(text="Lower Lips")
            curveiny = curvey.row()
            try:
                curveiny.prop(p_bones['lip_low_line_R'].bone, bbone_curveiny, text="Curve in" + axis + "Right")
                curveiny.prop(p_bones['lip_low_line_L'].bone, bbone_curveiny,  text="Curve in" + axis + "Left")
            except:
                pass
            curveouty = curvey.row()
            try:
                curveouty.prop(p_bones['lip_low_line_R'].bone, bbone_curveouty, text="Curve out" + axis + "Right")
                curveouty.prop(p_bones['lip_low_line_L'].bone, bbone_curveouty,  text="Curve out" + axis + "Left")
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
            box.separator()
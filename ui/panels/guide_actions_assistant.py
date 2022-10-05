import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_actions
from . assistant_base import BLENRIG_PT_guide_assistant

####### Actions assistant Guide

class BLENRIG_PT_actions_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Actions Assistant Guide"
    bl_idname = "BLENRIG_PT_actions_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        # Primero verificamos que la guía esté activa. Sino... un return para parar el dibujado.
        # NOTE: mejor podemos ponerlo en un poll { return VIEW3D_OT_blenrig_guide_actions.is_instantiated() }
        if not VIEW3D_OT_blenrig_guide_actions.is_instantiated(context):
            return

        arm_obj_props = context.scene.blenrig_guide
        current_step = context.scene.blenrig_guide.guide_current_step

        arm = context.active_object
        if hasattr(arm, 'pose') and hasattr(arm.pose, 'bones'):
            pose = arm.pose

            layout = self.layout

            Exclude = ['ACTIONS_Intro']

            Face_Steps = ['ACTIONS_Eyelids_Up_Up', 'ACTIONS_Eyelids_Up_Down_1', 'ACTIONS_Eyelids_Up_Down_2', 'ACTIONS_Eyelids_Low_Down', 'ACTIONS_Eyelids_Low_Up_1', 'ACTIONS_Eyelids_Low_Up_2', 'ACTIONS_Eyelids_Out', 'ACTIONS_Eyelids_In',
            'ACTIONS_Cheek_Up', 'ACTIONS_Cheek_Down', 'ACTIONS_Cheek_Frown', 'ACTIONS_Nose_Frown', 'ACTIONS_Nose_Frown_Max', 'ACTIONS_Jaw_Down', 'ACTIONS_Jaw_Up', 'ACTIONS_Mouth_Corner_Out', 'ACTIONS_Mouth_Corner_In', 'ACTIONS_Mouth_Corner_Up',
            'ACTIONS_Mouth_Corner_Down', 'ACTIONS_Mouth_Corner_Back', 'ACTIONS_Mouth_Corner_Forw', 'ACTIONS_Mouth_Corner_Up_Out_Corrective', 'ACTIONS_Mouth_Corner_Down_Out_Corrective', 'ACTIONS_U_Thicker_Lips', 'ACTIONS_U_Thinner_Lips',
            'ACTIONS_U', 'ACTIONS_O', 'ACTIONS_M', 'ACTIONS_Mouth_Frown', 'ACTIONS_Chin_Frown_Up', 'ACTIONS_Chin_Frown_Down',
            'ACTIONS_Mouth_Corner_In_Zipper', 'ACTIONS_U_Zipper', 'ACTIONS_O_Zipper', 'ACTIONS_U_Narrow_Corrective_Zipper']
            if current_step not in Exclude:
                steps = layout.column(align=True)
                box = steps.box()
                row = box.row()
                row.prop(pose, "use_mirror_x")
                row.prop(arm, "show_in_front")
                if not pose.use_mirror_x:
                    box.label(text= 'WARNING! Pose will not be mirrored to the other side. Using X-Mirror is recommended.', icon='ERROR')
                row2 = box.row()
                row2.prop(arm_obj_props, 'guide_show_def_bones')
                row2.prop(arm_obj_props, 'guide_show_wp_bones', text='Show All Bones')
                layout.row().prop(context.scene.blenrig_guide.arm_obj.data, "pose_position",text='Toggle Rest Pose', expand=True)
            # Propiedades específicas de cada STEP.
            if current_step == 'ACTIONS_Eyelids_Up_Up_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_eyelid_up_up")

            elif current_step == 'ACTIONS_Eyelids_Up_Down_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_eyelid_up_down")

            elif current_step == 'ACTIONS_Eyelids_Low_Down_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_eyelid_low_down")

            elif current_step == 'ACTIONS_Eyelids_Low_Up_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_eyelid_low_up")

            elif current_step == 'ACTIONS_Cheek_Up_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_cheek_up")

            elif current_step == 'ACTIONS_Cheek_Down_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_cheek_down")

            elif current_step == 'ACTIONS_Eyelids_Out':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_eyelid_out")

            elif current_step == 'ACTIONS_Eyelids_In':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_eyelid_in")

            elif current_step == 'ACTIONS_Nose_Frown_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_nose_frown")

            elif current_step == 'ACTIONS_Jaw_Down_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_jaw_down")

            elif current_step == 'ACTIONS_Jaw_Up_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_jaw_up")

            elif current_step == 'ACTIONS_Mouth_Corner_Out_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_corner_out")

            elif current_step == 'ACTIONS_Mouth_Corner_Up_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_corner_up")

            elif current_step == 'ACTIONS_Mouth_Corner_Down_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_corner_down")

            elif current_step == 'ACTIONS_Mouth_Corner_Back_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_corner_back")

            elif current_step == 'ACTIONS_Mouth_Corner_Forw_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_corner_forw")

            elif current_step == 'ACTIONS_Mouth_Corner_In_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_corner_in")

            elif current_step == 'ACTIONS_U_O_M_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_u_o_m")

            elif current_step == 'ACTIONS_Mouth_Frown_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_mouth_frown")

            elif current_step == 'ACTIONS_Chin_Frown_Range':
                steps = layout.column(align=True)
                box_set = steps.box()
                box_set.label(text='Define Range of Motion')
                box_set.prop(arm_obj_props, "guide_chin_frown")

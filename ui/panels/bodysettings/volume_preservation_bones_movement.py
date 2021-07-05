import bpy
from bpy.types import Panel

class BLENRIG_PT_Rig_Body_settings_vp_bones_movement(Panel):
    bl_label = "Volume Preservation Bones Movement:"
    bl_idname = "BLENRIG_PT_Rig_Body_settings_vp_bones_movement"
    bl_parent_id = "BLENRIG_PT_Rig_Body_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.column()
        col = box.column()
        box = layout.box()
        row = box.row(align=False)
        row.operator("mirror.vp_constraints", text="Mirror Values to the Right Side", icon='MOD_MIRROR')

class BlenrigVolumePreservationPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_parent_id = "BLENRIG_PT_Rig_Body_settings_vp_bones_movement"
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        arm_data = bpy.context.active_object.data
        if "gui_rig_body" in arm_data:
            return True

    def draw(self, context):
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = box.row(align=False)

    # def draw_header(self, context):
    #     scene  = context.scene
    #     layout = self.layout
    #     layout.emboss = 'NONE'
    #     row = layout.row(align=True)
    #     row = layout.row(align=True)
    #     row.prop(scene, "name", icon='BLANK1', icon_only= True)

class BLENRIG_PT_VP_forearm_upwards(BlenrigVolumePreservationPanel,Panel):
    bl_label = "Forearm Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Forearm Volume:')
        col_L.label(text='Elbow Volume:')
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

class BLENRIG_PT_VP_arm_upwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Arm Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Shoulder Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['shoulder_fix_L'].constraints['Shoulder_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['shoulder_fix_L'].constraints['Shoulder_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_arm_downwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Arm Downwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Armpit Volume:')
        col_L.label(text='Chest Volume:')
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
        col_R.label(text='Back Volume:')
        try:
            col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_arm_forwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Arm Forwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Chest Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Forw_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['chest_fix_L'].constraints['Chest_VP_Forw_L_NOREP'], 'to_max_x', text="Horizontal", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_arm_backwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Arm Backwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Back Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            col_L.prop(p_bones['back_fix_L'].constraints['Back_VP_Back_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_shoulder_upwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Shoulder Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Trap Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['trap_fix_L'].constraints['Trap_VP_Up_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['trap_fix_L'].constraints['Trap_VP_Up_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_hand_upwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Hand Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        box.label(text="Hand Up:")
        row_props = box.row()
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

class BLENRIG_PT_VP_hand_downwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Hand Downwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
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

class BLENRIG_PT_VP_fingers_backwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Fingers Backwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Knuckles Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['properties_arm_L'], 'volume_preservation_knuckles_up_L', text="Outwards", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_fingers_curl(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Fingers Curl"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Knuckles Volume:')
        col_L.label(text='Palm Volume ')
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

class BLENRIG_PT_VP_leg_forwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Leg Forwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Leg Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['thigh_fix_L'].constraints['Thigh_VP_Forw_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            col_R.prop(p_bones['thigh_fix_L'].constraints['Thigh_VP_Forw_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['thigh_fix_L'].constraints['Thigh_VP_Forw_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_leg_outwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Leg Outwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Hips Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['hip_fix_L'].constraints['Thigh_VP_Out_L_NOREP'], 'to_min_x', text="Horizontal", toggle=True)
            col_R.prop(p_bones['hip_fix_L'].constraints['Thigh_VP_Out_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['hip_fix_L'].constraints['Thigh_VP_Out_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_leg_backwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Leg Backwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Buttock Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['buttock_fix_L'].constraints['Thigh_VP_Back_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['buttock_fix_L'].constraints['Thigh_VP_Back_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_shin_upwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Shin Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Shin Volume:')
        col_L.label(text='Knee Volume:')
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

class BLENRIG_PT_VP_foot_downwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Foot Downwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Ankle Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['ankle_fix_L'].constraints['Ankle_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['ankle_fix_L'].constraints['Ankle_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_foot_upwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Foot Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Instep Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_foot_toe_curl_upwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Foot Toe Curl Upwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Toe 1 Up Volume:')
        col_L.label(text='Toe 2 Up Volume:')
        try:
            col_R.prop(p_bones['foot_toe_fix_up_1_L'].constraints['Foot_Toe_1_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['foot_toe_fix_up_2_L'].constraints['Foot_Toe_2_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_foot_toe_curl_downwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Foot Toe Curl Downwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Toe 1 Lower Volume:')
        col_L.label(text='Toe 2 Lower Volume:')
        try:
            col_R.prop(p_bones['foot_toe_fix_low_1_L'].constraints['Foot_Toe_1_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['foot_toe_fix_low_2_L'].constraints['Foot_Toe_2_Low_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_toes_backwards(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Toes Backwards"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Toe Knuckles Volume:')
        col_L.label(text=' ')
        try:
            col_R.prop(p_bones['properties_leg_L'], 'volume_preservation_toe_knuckles_up_L', text="Outwards", toggle=True)
        except:
            pass

class BLENRIG_PT_VP_toes_curl(BlenrigVolumePreservationPanel, Panel):
    bl_label = "Toes Curl"

    def draw(self, context):
        arm = bpy.context.active_object
        p_bones = arm.pose.bones
        layout = self.layout
        box = layout.column()
        col = box.column()
        row = col.row()

        box = col.box()
        row_props = box.row()
        col_R = row_props.column()
        col_L = row_props.column()
        col_R.label(text='Toe Sole Volume:')
        col_L.label(text='Toes Volume:')
        try:
            col_R.prop(p_bones['properties_leg_L'], 'volume_preservation_sole_down_L', text="Outwards", toggle=True)
        except:
            pass
        try:
            col_L.prop(p_bones['properties_leg_L'], 'volume_preservation_toes_down_L', text="Outwards", toggle=True)
        except:
            pass
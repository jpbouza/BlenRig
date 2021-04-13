import bpy
from bpy.types import Panel

class BlenrigVolumePanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_parent_id = "BLENRIG_PT_Rig_Body_settings"
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        arm_data = bpy.context.active_object.data
        if "gui_rig_body" in arm_data:
            props = bpy.context.window_manager.blenrig_6_props
        if props.gui_body_vp:
            return True

class BLENRIG_PT_forearm_upwards(BlenrigVolumePanel, Panel):
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

class BLENRIG_PT_shoulder_volume(BlenrigVolumePanel, Panel):
    bl_label = "Shoulder Volume"

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
        
class BLENRIG_PT_arm_downwards(BlenrigVolumePanel, Panel):
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
            col_R.prop(p_bones['back_fix_L'].constraints['Back_VP_Down_L_NOREP'], 'to_min_z', text="Verticañ", toggle=True)
        except:
            pass

class BLENRIG_PT_arm_forwards(BlenrigVolumePanel, Panel):
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

class BLENRIG_PT_arm_backwards(BlenrigVolumePanel, Panel):
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

class BLENRIG_PT_shoulder_up(BlenrigVolumePanel, Panel):
    bl_label = "Shoulder Up"

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

class BLENRIG_PT_hand_up(BlenrigVolumePanel, Panel):
    bl_label = "Hand Up"

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
            col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_R.prop(p_bones['wrist_fix_up_L'].constraints['Wrist_Up_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass
        try:
            col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
            col_L.prop(p_bones['wrist_fix_low_L'].constraints['Wrist_Low_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
        except:
            pass

class BLENRIG_PT_hand_down(BlenrigVolumePanel, Panel):
    bl_label = "Hand Down"

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

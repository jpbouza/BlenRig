import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_rig_settings

####### Rig Advanced Settings assistant Guide

class BLENRIG_PT_rig_settings_guide(bpy.types.Panel):
    bl_label = "Rig Advanced Settings Assistant Guide"
    bl_idname = "BLENRIG_PT_rig_settings_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER",}


    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False

        obj = context.object
        valid_types = {'POSE','ARAMTURE', 'MESH', 'LATTICE', 'CURVE', 'SURFACE', 'EDIT_ARMATURE'}

        return obj or obj.type in valid_types

    def draw(self, context):
        guide_props = context.scene.blenrig_guide
        active = context.active_object
        active_mode = active.mode
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        if VIEW3D_OT_blenrig_guide_rig_settings.instance:
            steps = layout.column(align=True)
            #Shoulder Automatic Movement
            if guide_props.guide_current_step == 'SETTINGS_Shoulder_Movement':
                box_pose = steps.box()
                box_pose.label(text='Shoulder Automatic Movement', icon='MOD_ARMATURE')
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_FORW_L"]', text="Shoulder_L Forwards", toggle=True)
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_BACK_L"]', text="Shoulder_L Backwards", toggle=True)
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_UP_L"]', text="Shoulder_L Upwards", toggle=True)
                box_pose.prop(p_bones['shoulder_L'], '["SHLDR_AUTO_DOWN_L"]', text="Shoulder_L Downwards", toggle=True)
            #Torso Rotation
            if guide_props.guide_current_step == 'SETTINGS_Torso_Rotation':
                box_pose = steps.box()
                box_pose.label(text='Torso Rotation Rate:')
                box_pose.prop(p_bones['spine_3_fk'], '["fk_follow_main"]', text="Spine 3", toggle=True)
                box_pose.prop(p_bones['spine_2_fk'], '["fk_follow_main"]', text="Spine 2", toggle=True)
                box_pose.prop(p_bones['spine_1_fk'], '["fk_follow_main"]', text="Spine 1", toggle=True)




import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide
####### Actions assistant Guide

class BLENRIG_PT_actions_guide(bpy.types.Panel):
    bl_label = "Actions Assistant Guide"
    bl_idname = "BLENRIG_PT_actions_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False
        if not context.active_object:
            return False
        
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                for prop in context.active_object.data.items():
                    if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                        return True
            else:
                return True

    def draw(self, context):
        arm = context.active_object
        arm_data = arm.data
        arm_pose = arm.pose
        p_bones = arm.pose.bones
        props = context.window_manager.blenrig_6_props
        layout = self.layout

        if VIEW3D_OT_blenrig_guide.instance and VIEW3D_OT_blenrig_guide.instance.step == 3:
            steps = layout.column(align=True)
            box = steps.box()
            box.label(text = "Opciones de los Acctions")

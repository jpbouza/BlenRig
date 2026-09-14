import bpy

####### BlenRig 6 Guides Panel

class BLENRIG_PT_blenrig_6_guides_panels(bpy.types.Panel):
    bl_label = "BlenRig 6 guides Panels"
    bl_space_type = 'VIEW_3D'
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_idname = "BLENRIG_PT_blenrig_6_guides_panels"
    bl_region_type = 'UI'
    bl_category = "BlenRig 6"

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False

        if not context.active_object:
            return False
        # if (context.active_object.type in ["ARMATURE"]):
        for prop in context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                for prop in context.active_object.data.items():
                    if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                        return True

    def draw(self, context):
        arm = context.active_object
        arm_data = context.active_object.data
        p_bones = arm.pose.bones
        layout = self.layout

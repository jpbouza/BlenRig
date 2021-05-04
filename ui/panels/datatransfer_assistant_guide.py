import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide_datatransfer

####### Data Transfer assistant Guide

class BLENRIG_PT_datatransfer_guide(bpy.types.Panel):
    bl_label = "Data Transfer Assistant Guide"
    bl_idname = "BLENRIG_PT_datatransfer_guide"
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
        arm = context.active_object
        arm_data = context.active_object.data
        pose = arm.pose
        p_bones = arm.pose.bones
        layout = self.layout

        # Step 0 X-Mirror
        if VIEW3D_OT_blenrig_guide_datatransfer.instance and VIEW3D_OT_blenrig_guide_datatransfer.instance.step == 0:
            steps = layout.column(align=True)
            box = steps.box()
            # box.prop(pose, "use_mirror_x")
            box.label(text= "Data Transfer")
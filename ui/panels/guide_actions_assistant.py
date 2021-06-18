import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide_actions

####### Actions assistant Guide

class BLENRIG_PT_actions_guide(bpy.types.Panel):
    bl_label = "Actions Assistant Guide"
    bl_idname = "BLENRIG_PT_actions_guide"
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
        arm_obj_props = bpy.context.scene.blenrig_guide
        layout = self.layout

        if VIEW3D_OT_blenrig_guide_actions.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'ACTIONS_Select_Body_Objects':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Object tha use Mesh Deform')
            box_set.prop(arm_obj_props, "guide_mouth_corner_out")
            box_set.prop(arm_obj_props, "guide_mouth_corner_in")
            box_set.prop(arm_obj_props, "guide_mouth_corner_up")
            box_set.prop(arm_obj_props, "guide_mouth_corner_down")
            box_set.prop(arm_obj_props, "guide_mouth_corner_back")
            box_set.prop(arm_obj_props, "guide_mouth_corner_forw")
            box_set.prop(arm_obj_props, "guide_jaw_up")
            box_set.prop(arm_obj_props, "guide_jaw_down")
            box_set.prop(arm_obj_props, "guide_cheek_up")
            box_set.prop(arm_obj_props, "guide_cheek_down")
            box_set.prop(arm_obj_props, "guide_nose_forwn")
            box_set.prop(arm_obj_props, "guide_mouth_forwn")
            box_set.prop(arm_obj_props, "guide_chin_forwn")
            box_set.prop(arm_obj_props, "guide_eyelid_up_up")
            box_set.prop(arm_obj_props, "guide_eyelid_up_down")
            box_set.prop(arm_obj_props, "guide_eyelid_low_down")
            box_set.prop(arm_obj_props, "guide_eyelid_low_up")
            box_set.prop(bpy.context.scene.blenrig_guide.arm_obj.data, "layers", index=27, text='Show Deformation Bones')





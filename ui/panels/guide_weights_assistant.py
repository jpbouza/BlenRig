import bpy
from ...guides.operator import VIEW3D_OT_blenrig_guide_weights

####### Weights assistant Guide

class BLENRIG_PT_weights_guide(bpy.types.Panel):
    bl_label = "Weights Assistant Guide"
    bl_idname = "BLENRIG_PT_weights_guide"
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
        guide_props = bpy.context.scene.blenrig_guide
        active = bpy.context.active_object.mode
        layout = self.layout

        if VIEW3D_OT_blenrig_guide_weights.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'WEIGHTS_Cage_Ankle':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Set Joint Angle')
            box_set.prop(guide_props.arm_obj.pose, "use_mirror_x")
            box_set.prop(guide_props, "guide_ball_joint_rotate")
            box_set.operator("blenrig.toggle_weight_painting", text='Toggle Weight Painting').paint_object = 'mdef_cage'
            if active == 'WEIGHT_PAINT':
                box_set.prop(guide_props.mdef_cage_obj.data, "use_mirror_vertex_groups")
                box_set.prop(guide_props.mdef_cage_obj.data, "use_mirror_topology")
            box_set.operator("blenrig._mirror_vp_rj_values", text='Mirror Values')







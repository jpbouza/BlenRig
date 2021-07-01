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
        p_bones = guide_props.arm_obj.pose.bones
        layout = self.layout

        if VIEW3D_OT_blenrig_guide_weights.instance:
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Weight Painting Options')
            box_set.operator("blenrig.toggle_weight_painting", text='Toggle Weight Painting').paint_object = 'mdef_cage'
            mirror_row = box_set.row()
            mirror_row.prop(guide_props.arm_obj.pose, "use_mirror_x", text='X-Axis Mirror (Pose)')
            if active == 'WEIGHT_PAINT':
                mirror_row.prop(guide_props.mdef_cage_obj.data, "use_mirror_vertex_groups")
                mirror_row.prop(guide_props.mdef_cage_obj.data, "use_mirror_topology")

        if VIEW3D_OT_blenrig_guide_weights.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'WEIGHTS_Cage_Ankle':
            box_set.label(text='Set Joint Transforms')
            box_set.prop(guide_props, "guide_joint_rotate_X6", text='Ankle Pose')
            if guide_props.guide_joint_rotate_X6 != 0:
                box_set.label(text='Realistic Joints Parameters')
                box_set.prop(p_bones["properties_leg_L"], 'realistic_joints_ankle_rot_L', text='Ankle Displacement')
            if guide_props.guide_joint_rotate_X6 == 1:
                row_props = box_set.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Instep')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_rotate_X6 != 0:
                box_set.separator()
                box_set.operator("blenrig._mirror_vp_rj_values", text='Mirror Values')







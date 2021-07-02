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
            box_weight = steps.box()
            box_weight.label(text='Weight Painting Options')
            box_weight.operator("blenrig.toggle_weight_painting", text='Toggle Weight Painting').paint_object = 'mdef_cage'
            box_weight.operator("blenrig.wp_joint_chain_up", text='>')
            box_weight.operator("blenrig.wp_joint_chain_down", text='<')
            box_weight.label(text=guide_props.guide_transformation_bone)
            mirror_row = box_weight.row()
            mirror_row.prop(guide_props.arm_obj.pose, "use_mirror_x", text='X-Axis Mirror (Pose)')
            if active == 'WEIGHT_PAINT':
                mirror_row.prop(guide_props.mdef_cage_obj.data, "use_mirror_vertex_groups")
                mirror_row.prop(guide_props.mdef_cage_obj.data, "use_mirror_topology")
            steps.separator()

        if VIEW3D_OT_blenrig_guide_weights.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'WEIGHTS_Cage_Ankle':
            box_pose = steps.box()
            box_pose.label(text='Set Joint Transforms')
            box_pose.prop(guide_props, "guide_joint_rotate_X6", text='Ankle Pose')
            if guide_props.guide_joint_rotate_X6 != 0:
                box_pose.label(text='Realistic Joints Parameters')
                box_pose.prop(p_bones["properties_leg_L"], 'realistic_joints_ankle_rot_L', text='Ankle Displacement')
            if guide_props.guide_joint_rotate_X6 == 5 or guide_props.guide_joint_rotate_X6 == 6 :
                box_pose.label(text='Shin Twist Rate')
                box_pose.prop(p_bones["properties_leg_L"], '["twist_rate_shin_L"]', text='Twist Rate')
            if guide_props.guide_joint_rotate_X6 == 2:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Instep')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['instep_fix_L'].constraints['Instep_VP_Up_L_NOREP'], 'to_min_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_rotate_X6 == 1:
                row_props = box_pose.row()
                col_R = row_props.column()
                col_L = row_props.column()
                col_R.label(text='Volume Preservation: Ankle')
                col_L.label(text=' ')
                try:
                    col_R.prop(p_bones['ankle_fix_L'].constraints['Ankle_VP_Down_L_NOREP'], 'to_max_y', text="Outwards", toggle=True)
                    col_L.prop(p_bones['ankle_fix_L'].constraints['Ankle_VP_Down_L_NOREP'], 'to_max_z', text="Vertical", toggle=True)
                except:
                    pass
            if guide_props.guide_joint_rotate_X6 != 0:
                box_pose.separator()
                box_pose.operator("blenrig.mirror_vp_rj_values", text='Mirror Values')




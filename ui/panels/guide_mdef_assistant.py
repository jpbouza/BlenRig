import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_mdef
from . assistant_base import BLENRIG_PT_guide_assistant

####### Mesh Deform assistant Guide

class BLENRIG_PT_mdef_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Mesh Deform Assistant Guide"
    bl_idname = "BLENRIG_PT_mdef_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2
    

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_mdef.is_instantiated(context):
            return

        layout = self.layout
        guide_props = bpy.context.scene.blenrig_guide
        mdef_cage = guide_props.mdef_cage_obj

        if context.scene.blenrig_guide.guide_current_step == 'MDEF_Select_Body_Objects':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Objects that use Mesh Deform')
            box_set.operator("blenrig.guide_add_body_modifiers", text = 'Set Body Objects')
        if context.scene.blenrig_guide.guide_current_step == 'MDEF_Edit_Mdef_Cage':
            props = context.window_manager.blenrig_6_props
            ob = context.active_object
            # Cage Setup
            if context.mode in ["EDIT_MESH"]:
                box = layout.column()
                box.label(text='Mdef Cage Automatic Wrapping')
                col = box.column()
                row = col.row()
                row = layout.row(align=True)
                col.operator("blenrig.snap_points", text="Adjust Cage", icon="NONE")
                row = layout.row(heading="Distance Cage")
                row.prop(props,"adjust_distance_cage",text="value")
                box = layout.column()
                box.label(text='Mdef Cage Options')
                col = box.column()
                row = col.row()
                row.prop(mdef_cage.data, "use_mirror_x", text='X-Mirror')
                row.prop(mdef_cage.data, "use_mirror_topology")
                col.prop(mdef_cage, "display_type")

        if context.scene.blenrig_guide.guide_current_step == 'MDEF_Binding_Check':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Bind Mesh Deform (Fast)')
            box_set.operator("blenrig.guide_bind_mdef_modifiers", text = 'Bind Mesh Deform (Fast)').Guide_Bind_Type = True
            box_set.operator("blenrig.guide_unbind_mdef_modifiers", text = 'Unbind Mesh Deform')
            box_rig = steps.box()
            box_rig.label(text='Deformation')
            box_rig.operator("blenrig.guide_transfer_test_rig", text = 'Test Defomation').bone = 'master_torso'
            row_mdef = box_rig.row()
            row_mdef.operator("blenrig.guide_edit_mdef_cage", text = 'Edit Mdef Cage')
            row_mdef.prop(guide_props, "guide_show_mdef_cage", text = 'Show Mdef Cage')
            if context.mode in ["EDIT_MESH"]:
                box = steps.box()
                box.label(text='Mdef Cage Options')
                col = box.column()
                row = col.row()
                row.prop(mdef_cage.data, "use_mirror_x", text='X-Mirror')
                row.prop(mdef_cage.data, "use_mirror_topology")
                col.prop(mdef_cage, "display_type")

        if context.scene.blenrig_guide.guide_current_step == 'MDEF_Final_Binding':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Bind Mesh Deform (Final)')
            box_set.operator("blenrig.guide_bind_mdef_modifiers", text = 'Bind Mesh Deform (Final)').Guide_Bind_Type = False
            box_set.operator("blenrig.guide_unbind_mdef_modifiers", text = 'Unbind Mesh Deform')
            box_rig = steps.box()
            box_rig.label(text='Deformation')
            box_rig.operator("blenrig.guide_transfer_test_rig", text = 'Test Defomation').bone = 'master_torso'




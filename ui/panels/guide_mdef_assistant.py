import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_mdef
from . assistant_base import BLENRIG_PT_guide_assistant

####### Mesh Deform assistant Guide

class BLENRIG_PT_mdef_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Mesh Deform Assistant Guide"
    bl_idname = "BLENRIG_PT_mdef_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"

    def draw(self, context):
        layout = self.layout

        if VIEW3D_OT_blenrig_guide_mdef.instance and context.scene.blenrig_guide.guide_current_step == 'MDEF_Select_Body_Objects':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Define Object tha use Mesh Deform')
            box_set.operator("blenrig.add_body_modifiers", text = 'Set Body Objects')
        if VIEW3D_OT_blenrig_guide_mdef.instance and context.scene.blenrig_guide.guide_current_step == 'MDEF_Edit_Mdef_Cage':
            props = context.window_manager.blenrig_6_props
            ob = context.active_object
            mesh = ob.data
            # Cage Setup
            if context.mode in ["EDIT_MESH"]:
                box = layout.column()
                box.label(text='Mdef Cage Automatic Wrapping')
                col = box.column()
                row = col.row()
                # row.alignment = 'CENTER'
                row = layout.row(align=True)
                comb = row.row()
                # row = layout.row(heading="Mirror")
                sub = row.row(align=True)
                sub.prop(mesh, "use_mirror_x",text= "X-Mirror")
                row.prop(mesh, "use_mirror_topology")
                col.operator("blenrig.snap_points", text="Ajust Cage", icon="NONE")
                row = layout.row(heading="Distance Cage")
                row.prop(props,"ajust_distance_cage",text="value")
        if VIEW3D_OT_blenrig_guide_mdef.instance and context.scene.blenrig_guide.guide_current_step == 'MDEF_Binding_Check':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Bind Mesh Deform (Fast)')
            box_set.operator("blenrig.guide_bind_mdef_modifiers", text = 'Bind Mesh Deform (Fast)').Guide_Bind_Type = True
            box_set.operator("blenrig.guide_unbind_mdef_modifiers", text = 'Unbind Mesh Deform')
        if VIEW3D_OT_blenrig_guide_mdef.instance and context.scene.blenrig_guide.guide_current_step == 'MDEF_Final_Binding':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Bind Mesh Deform (Final)')
            box_set.operator("blenrig.guide_bind_mdef_modifiers", text = 'Bind Mesh Deform (Final)').Guide_Bind_Type = False
            box_set.operator("blenrig.guide_unbind_mdef_modifiers", text = 'Unbind Mesh Deform')



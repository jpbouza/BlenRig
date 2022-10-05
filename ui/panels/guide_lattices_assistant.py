import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_lattices
from . assistant_base import BLENRIG_PT_guide_assistant

####### Lattices assistant Guide

class BLENRIG_PT_lattices_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Lattices Assistant Guide"
    bl_idname = "BLENRIG_PT_lattices_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_order = 2

    def draw(self, context):
        if not VIEW3D_OT_blenrig_guide_lattices.is_instantiated(context):
            return

        layout = self.layout

        STEPS = ['LATTICES_Adjust_Body', 'LATTICES_Adjust_Head', 'LATTICES_Adjust_Brow', 'LATTICES_Adjust_Mouth']

        if context.scene.blenrig_guide.guide_current_step in STEPS:
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Lattice Position')
            row = box_set.row()
            row.operator("blenrig.disable_hooks_modif", text="Edit Lattice Position")
            sub = row.row(align=False)
            sub = row.row()
            sub.scale_x = 0.6
            sub.operator("blenrig.reset_hooks", text="Apply Lattice Position")
        if context.scene.blenrig_guide.guide_current_step == 'LATTICES_Adjust_Eyes':
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Lattice Position')
            row = box_set.row()
            row.operator("blenrig.disable_hooks_modif", text="Edit Lattice Position")
            sub = row.row(align=False)
            sub = row.row()
            sub.scale_x = 0.6
            sub.operator("blenrig.reset_hooks", text="Apply Lattice Position")
            row_mirror = box_set.row()
            row_mirror.operator("blenrig.mirror_lattice_transforms", text="Mirror Lattice Transforms")

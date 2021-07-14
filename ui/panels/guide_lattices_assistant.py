import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_lattices

####### Lattices assistant Guide

class BLENRIG_PT_lattices_guide(bpy.types.Panel):
    bl_label = "Lattices Assistant Guide"
    bl_idname = "BLENRIG_PT_lattices_guide"
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
        layout = self.layout

        STEPS = ['LATTICES_Adjust_Body', 'LATTICES_Adjust_Head', 'LATTICES_Adjust_Brow', 'LATTICES_Adjust_Mouth']

        if VIEW3D_OT_blenrig_guide_lattices.instance and bpy.context.scene.blenrig_guide.guide_current_step in STEPS:
            steps = layout.column(align=True)
            box_set = steps.box()
            box_set.label(text='Lattice Position')
            row = box_set.row()
            row.operator("blenrig.disable_hooks_modif", text="Edit Lattice Position")
            sub = row.row(align=False)
            sub = row.row()
            sub.scale_x = 0.6
            sub.operator("blenrig.reset_hooks", text="Apply Lattice Position")
        if VIEW3D_OT_blenrig_guide_lattices.instance and bpy.context.scene.blenrig_guide.guide_current_step == 'LATTICES_Adjust_Eyes':
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

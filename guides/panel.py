from bpy.types import Panel
from . guide import GUIDE_STEPS


class BlendrigGuidePanel(Panel):
    bl_label = "Blendrig Guide"
    bl_idname = "BLENRIG_PT_guide_panel"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blenrig"
    bl_options = {"HIDE_HEADER",}
    bl_order = 1

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False

        obj = context.object
        valid_types = {'POSE','ARAMTURE', 'MESH', 'LATTICE', 'CURVE', 'SURFACE'}
        
        return obj or obj.type in valid_types

    def draw(self, context):
        guide = context.scene.blenrig_guide
        layout = self.layout
        from . operator import VIEW3D_OT_blenrig_guide as OPERATOR
        layout.enabled = False if OPERATOR.instance else True
        layout.prop(guide, 'language')
        layout.prop(guide, 'dpi')
        layout.prop(guide, 'image_scale')
        
        button = layout.row()
        button.scale_y = 1.5
        button.operator("view3d.blenrig_guide")

        layout.separator()
        
        steps = layout.column(align=True)
        desplegable = steps.box()
        desplegable.prop(guide, 'show_steps', icon='TRIA_DOWN' if guide.show_steps else 'TRIA_RIGHT', emboss=False)
        
        if not guide.show_steps:
            return
        
        step_list = steps.box().column(align=True)
        
        for i, step in enumerate(GUIDE_STEPS):
            step_list.operator("view3d.blenrig_guide", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

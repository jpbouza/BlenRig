from bpy.types import Panel
from .reproportion.guide_reproportion import GUIDE_STEPS_REPROPORTION
from .datatransfer.guide_datatransfer import GUIDE_STEPS_DATATRANSFER
from .mdef.guide_mdef import GUIDE_STEPS_MDEF
from .lattices.guide_lattices import GUIDE_STEPS_LATTICES
from .actions.guide_actions import GUIDE_STEPS_ACTIONS
from .weights.guide_weights import GUIDE_STEPS_WEIGHTS
from .shapekeys.guide_shapekeys import GUIDE_STEPS_SHAPEKEYS
from .rig_settings.guide_rig_settings import GUIDE_STEPS_SETTINGS

class BlenRigGuidePanel_menu:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_category = "Blenrig"

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False

        obj = context.object
        valid_types = {'POSE','ARMATURE', 'MESH', 'LATTICE', 'CURVE', 'SURFACE'}

        return obj or obj.type in valid_types

class BlenRigGuidePanel(BlenRigGuidePanel_menu,Panel):
    bl_label = "BlenRig Guide"
    bl_idname = "BLENRIG_PT_guide_panel"
    bl_space_type = 'VIEW_3D'
    bl_options = {"HIDE_HEADER",}
    bl_order = 2

    def draw(self, context):
        guide = context.scene.blenrig_guide
        layout = self.layout
        col = layout.column()
        col.scale_y = 1.5
        mainrow = col.box().row(align=True)
        col1 = mainrow.column(align=True)
        col2 = mainrow.column(align=True)
        steps = layout.column(align=True)
        col.label(text="Rigging Assistants :")

        button_1 = col1.row(align=True)
        button_2 = col1.row(align=True)
        button_3 = col1.row(align=True)
        button_4 = col1.row(align=True)
        button_5 = col1.row(align=True)
        button_6 = col1.row(align=True)
        button_7 = col1.row(align=True)
        button_8 = col1.row(align=True)
        # button_9 = col.row(align=True)

        button_1.operator("view3d.blenrig_guide_reproportion", text = '1 - Reproportion Guide')
        # button_1.prop(guide, 'show_steps_guide_reproportion',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_reproportion else 'DOWNARROW_HLT', emboss=True)

        button_2.operator("view3d.blenrig_guide_datatransfer", text = '2 - Weights Transfer Guide')
        # button_2.prop(guide, 'show_steps_guide_datatransfer',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_datatransfer else 'DOWNARROW_HLT', emboss=True)

        button_3.operator("view3d.blenrig_guide_mdef", text = '3 - Mesh Deform Guide')
        # button_3.prop(guide, 'show_steps_guide_mdef',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_mdef else 'DOWNARROW_HLT', emboss=True)

        button_4.operator("view3d.blenrig_guide_lattices", text = '4 - Lattices Guide')
        # button_4.prop(guide, 'show_steps_guide_lattices',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_lattices else 'DOWNARROW_HLT', emboss=True)

        button_5.operator("view3d.blenrig_guide_weights", text = '5 - Weight Painting Guide')
        # button_5.prop(guide, 'show_steps_guide_weights',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_weights else 'DOWNARROW_HLT', emboss=True)

        button_6.operator("view3d.blenrig_guide_actions", text = '6 - Actions Guide')
        # button_6.prop(guide, 'show_steps_guide_actions',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_actions else 'DOWNARROW_HLT', emboss=True)

        button_7.operator("view3d.blenrig_guide_rig_settings", text = '7 - Advanced Settings Guide')
        # button_7.prop(guide, 'show_steps_guide_rig_settings',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_rig_settings else 'DOWNARROW_HLT', emboss=True)

        button_8.operator("view3d.blenrig_guide_shapekeys", text = '8 - Shapekeys Guide')
        # button_8.prop(guide, 'show_steps_guide_shapekeys',text = '', icon='TRIA_DOWN' if guide.show_steps_guide_shapekeys else 'DOWNARROW_HLT', emboss=True)

        col2.prop(guide, 'show_steps_guide', text='', expand=True, toggle=True)

        layout.separator()

        step_list = steps.box().column(align=True)
        step_list.prop(guide, 'show_steps', icon='TRIA_DOWN' if guide.show_steps else 'TRIA_RIGHT', emboss=False)
        step_list.scale_y = 0.7

        if guide.show_steps:

            # if guide.show_steps_guide_reproportion:
            if guide.show_steps_guide == 'REPROPORTION':
                for i, step in enumerate(GUIDE_STEPS_REPROPORTION):
                    step_list.operator("view3d.blenrig_guide_reproportion", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_datatransfer:
            if guide.show_steps_guide == 'DATATRANFER':
                for i, step in enumerate(GUIDE_STEPS_DATATRANSFER):
                    step_list.operator("view3d.blenrig_guide_datatransfer", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_mdef:
            if guide.show_steps_guide == 'MDEF':
                for i, step in enumerate(GUIDE_STEPS_MDEF):
                    step_list.operator("view3d.blenrig_guide_mdef", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_lattices:
            if guide.show_steps_guide == 'LATTICES':
                for i, step in enumerate(GUIDE_STEPS_LATTICES):
                    step_list.operator("view3d.blenrig_guide_lattices", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_actions:
            if guide.show_steps_guide == 'ACTIONS':
                for i, step in enumerate(GUIDE_STEPS_ACTIONS):
                    step_list.operator("view3d.blenrig_guide_actions", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_weights:
            if guide.show_steps_guide == 'WHEIGHTS':
                for i, step in enumerate(GUIDE_STEPS_WEIGHTS):
                    step_list.operator("view3d.blenrig_guide_weights", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_rig_settings:
            if guide.show_steps_guide == 'RIGSETTINGS':
                for i, step in enumerate(GUIDE_STEPS_SETTINGS):
                    step_list.operator("view3d.blenrig_guide_rig_settings", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i

            # if guide.show_steps_guide_shapekeys:
            if guide.show_steps_guide == 'SHAPEKEYS':
                for i, step in enumerate(GUIDE_STEPS_SHAPEKEYS):
                    step_list.operator("view3d.blenrig_guide_shapekeys", text=str(i + 1) + "- " + str(step['titulo'][guide.language])).step=i


class BlenRigGuidePanel_options(BlenRigGuidePanel_menu,Panel):
    bl_label = "Options"
    bl_idname = "BLENRIG_PT_guide_panel_sub"
    bl_space_type = 'VIEW_3D'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    def draw(self, context):
        guide = context.scene.blenrig_guide
        layout = self.layout
        from . guide_ops import VIEW3D_OT_blenrig_guide_reproportion as OPERATOR
        layout.enabled = False if OPERATOR.instance else True
        layout.prop(guide, 'language')
        layout.prop(guide, 'dpi')
        layout.prop(guide, 'image_scale')

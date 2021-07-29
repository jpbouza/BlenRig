import bpy
from ...guides.guide_ops import VIEW3D_OT_blenrig_guide_shapekeys
from . assistant_base import BLENRIG_PT_guide_assistant

####### Shapekeys assistant Guide

class BLENRIG_PT_shapekeys_guide(BLENRIG_PT_guide_assistant):
    bl_label = "Shapekeys Assistant Guide"
    bl_idname = "BLENRIG_PT_shapekeys_guide"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"

    def draw(self, context):
        layout = self.layout

        # if VIEW3D_OT_blenrig_guide_lattices.instance and context.scene.blenrig_guide.guide_current_step == 'MDEF_Select_Body_Objects':
        #     steps = layout.column(align=True)
        #     box_set = steps.box()
        #     box_set.label(text='Define Object tha use Mesh Deform')
        #     box_set.operator("blenrig.add_body_modifiers", text = 'Set Body Objects')




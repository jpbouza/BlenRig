import bpy
from bpy.types import PropertyGroup, Object
from bpy.props import *
from . guide import languages

class BlenrigGuideData(PropertyGroup):
    language : EnumProperty(
        items=languages,
        name="Language"
    )
    dpi : IntProperty(default=72, min=72, max=300, name="Screen DPI")
    image_scale : FloatProperty(default=1, min=0.5, max=2, name="Image Scale")
    show_steps : BoolProperty(default=False, name="Show Steps")
    guide_current_step : StringProperty('')
    #BlenRig Armature
    arm_obj : PointerProperty(type=Object)
    #BlenRig Weights Transfer Mesh
    mdef_weights_transfer_obj : PointerProperty(type=Object)
    #BlenRig Mdef Cage
    mdef_cage_obj : PointerProperty(type=Object)
    #Character Objects
    character_head_obj : PointerProperty(type=Object)
    character_hands_obj : PointerProperty(type=Object)
    character_body_obj = []
    #Weight Transfer Parameters
    transfer_ray_distance : FloatProperty(default=0.05, min=0.0, max=100.0, name="Transfer Ray Distance")
    transfer_mapping : EnumProperty(
        items = (
            ('TOPOLOGY', 'Topology', '', 0),
            ('NEAREST', 'Nearest Vertex', '', 1),
            ('EDGE_NEAREST', 'Nearest Edge Vertex', '', 2),
            ('EDGEINTERP_NEAREST', 'Nearest Edge Interpolated', '', 3),
            ('POLY_NEAREST', 'Nearest Face Vertex', '', 4),
            ('POLYINTERP_NEAREST', 'Nearest Face Interpolated', '', 5),
            ('POLYINTERP_VNORPROJ', 'Projected Face Interpolated', '', 6),
            ),
            name="Mapping", default='POLYINTERP_VNORPROJ')
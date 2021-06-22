import bpy
from bpy.types import PropertyGroup, Object
from bpy.props import *
from . guide import languages
from . utils import *

class BlenRigBodyObj(bpy.types.PropertyGroup):
    character_body_obj : PointerProperty(type=Object)


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
            ('POLYINTERP_VNORPROJ', 'Projected Face Interpolated', '', 6)
            ),
            name="Mapping", default='POLYINTERP_VNORPROJ')

## Actions Properties ##

    #Mouth Corners
    guide_mouth_corner_out : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the Outwards Limit of the Character's Mouth Corners",
    update=corner_out_update,
    name="Mouth Corner Out Limit"
    )
    guide_mouth_corner_in : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the Inwards Limit of the Character's Mouth Corners",
    update=corner_in_update,
    name="Mouth Corner In Limit"
    )
    guide_mouth_corner_up : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the Upwards Limit of the Character's Mouth Corners",
    update=corner_up_update,
    name="Mouth Corner Up Limit"
    )
    guide_mouth_corner_down : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the Downwards Limit of the Character's Mouth Corners",
    update=corner_down_update,
    name="Mouth Corner Down Limit"
    )
    guide_mouth_corner_back : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the Backwards Limit of the Character's Mouth Corners",
    update=corner_back_update,
    name="Mouth Corner Back Limit"
    )
    guide_mouth_corner_forw : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the Forwards Limit of the Character's Mouth Corners",
    update=corner_forw_update,
    name="Mouth Corner Forwards Limit"
    )
    guide_auto_back : FloatProperty(default=0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define how much the Mouth Corners move Backwards when they move Outwards with Mouth_Ctrl, representing the underlying volume of the teeth",
    update=auto_back_update,
    name="Mouth Corner Auto Back"
    )
    #Jaw
    guide_jaw_up : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Define the maximum amount of Upwards rotation for the Jaw",
    update=jaw_up_update,
    name="Jaw Upwards Rotation Limit"
    )
    guide_jaw_down : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Define the maximum amount of Downwards rotation for the Jaw",
    update=jaw_down_update,
    name="Jaw Downwards Rotation Limit"
    )
    #Cheeks
    guide_cheek_up : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Upwards movement for the Cheek",
    update=cheek_up_update,
    name="Cheek Upwards Limit"
    )
    guide_cheek_down : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Downwards movement for the Cheek",
    update=cheek_down_update,
    name="Cheek Downwards Limit"
    )
    #Nose Frown
    guide_nose_frown : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Upwards movement for when Frowning the Nose",
    update=nose_frown_update,
    name="Nose Frown Limit"
    )
    #Mouth Frown
    guide_mouth_frown : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Downwards movement for when Frowning the Mouth",
    update=mouth_frown_update,
    name="Mouth Frown Limit"
    )
    #Mouth Frown
    guide_chin_frown : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Downwards movement for when Frowning the Chin",
    update=chin_frown_update,
    name="Chin Frown Limit"
    )
    #Upper Eyelids
    guide_eyelid_up_up : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Upwards movement of the Upper Eyelid",
    update=eyelid_up_up_update,
    name="Upper Eyelid Up Limit"
    )
    guide_eyelid_up_down : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Downwards movement of the Upper Eyelid",
    update=eyelid_up_down_update,
    name="Upper Eyelid Down Limit"
    )
    #Lower Eyelids
    guide_eyelid_low_down : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Downwards movement of the Lower Eyelid",
    update=eyelid_low_down_update,
    name="Lower Eyelid Down Limit"
    )
    guide_eyelid_low_up : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Upwards movement of the Lower Eyelid",
    update=eyelid_low_up_update,
    name="Lower Eyelid Up Limit"
    )
    guide_eyelid_out : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Define the maximum amount of Outwards Rotation of the Eye",
    update=eyelid_out_update,
    name="Eyelid Out Limit"
    )
    guide_eyelid_in : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Define the maximum amount of Inwards Rotation of the Eye",
    update=eyelid_in_update,
    name="Eyelid In Limit"
    )
import bpy
from bpy.types import PropertyGroup, Object
from bpy.props import *
from . traductor import languages
from . utils import *

class BlenRigBodyObj(bpy.types.PropertyGroup):
    character_body_obj : PointerProperty(type=Object)

class BlenRigJointChain(bpy.types.PropertyGroup):
    joint : StringProperty('')
    vgroup : StringProperty('')

class BlenRigWPBones(bpy.types.PropertyGroup):
    bone : StringProperty('')

class BlenrigGuideData(PropertyGroup):
    language : EnumProperty(
        items=languages,
        name="Language"
    )
    dpi : IntProperty(default=72, min=72, max=300, name="Screen DPI")
    image_scale : FloatProperty(default=1, min=0.5, max=4, name="Image Scale")
    show_steps : BoolProperty(default=False, name="Show Steps")
    guide_current_step : StringProperty('')
    #BlenRig Armature
    obj : PointerProperty(type=Object) # temporal object slot.
    arm_obj : PointerProperty(type=Object)
    #BlenRig Weights Transfer Mesh
    mdef_weights_transfer_obj : PointerProperty(type=Object)
    #BlenRig Mdef Cage
    mdef_cage_obj : PointerProperty(type=Object)
    #Character Objects
    character_head_obj : PointerProperty(type=Object)
    character_hands_obj : PointerProperty(type=Object)
    character_toes_obj : PointerProperty(type=Object)
    #Weight Paint Object
    active_wp_obj : PointerProperty(type=Object)
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
    #Mouth U_O_M
    guide_u_o_m : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of movement of the U vowel controller",
    update=u_o_m_update,
    name="U_O_M Limit"
    )
    #Mouth Frown
    guide_mouth_frown : FloatProperty(default=0.000, min=0.000, max=10.000, precision=3,
    description="Define the maximum amount of Downwards movement for when Frowning the Mouth",
    update=mouth_frown_update,
    name="Mouth Frown Limit"
    )
    #Chin Frown
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
## Weights Properties ##
    #Bone to transform
    guide_transformation_bone: StringProperty('')
    #Weight Painting Active Vgroup
    guide_active_wp_group: StringProperty('')
    #Rotation Order
    guide_axis_order: StringProperty('')
    #Joint Rotation type
    guide_transform_steps: StringProperty('')
    #Roatations for each Step
    guide_rotation_1 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Angle for Bone in Weight Painting Guide",
    name="X Rotation"
    )
    guide_rotation_2 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Angle for Bone in Weight Painting Guide",
    name="X Negative Rotation"
    )
    guide_rotation_3 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Angle for Bone in Weight Painting Guide",
    name="Y Rotation"
    )
    guide_rotation_4 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Angle for Bone in Weight Painting Guide",
    name="Y Negative Rotation"
    )
    guide_rotation_5 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Angle for Bone in Weight Painting Guide",
    name="Z Rotation"
    )
    guide_rotation_6 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Angle for Bone in Weight Painting Guide",
    name="Z Negative Rotation"
    )
    #Locations for each Step
    guide_location_1 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Location for Bone in Weight Painting Guide",
    name="X Location"
    )
    guide_location_2 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Location for Bone in Weight Painting Guide",
    name="Y Location"
    )
    guide_location_3 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Location for Bone in Weight Painting Guide",
    name="Z Location"
    )
    guide_location_4 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Location for Bone in Weight Painting Guide",
    name="X Location"
    )
    guide_location_5 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Location for Bone in Weight Painting Guide",
    name="Y Location"
    )
    guide_location_6 : FloatVectorProperty(default=(0.0, 0.0, 0.0), precision=3,
    description="Location for Bone in Weight Painting Guide",
    name="Z Location"
    )
    #Scales for each Step
    guide_scale_1 : FloatVectorProperty(default=(1.0, 1.0, 1.0), precision=3,
    description="Scale for Bone in Weight Painting Guide",
    name="X Scale"
    )
    guide_scale_2 : FloatVectorProperty(default=(1.0, 1.0, 1.0), precision=3,
    description="Scale for Bone in Weight Painting Guide",
    name="Y Scale"
    )
    guide_scale_3 : FloatVectorProperty(default=(1.0, 1.0, 1.0), precision=3,
    description="Scale for Bone in Weight Painting Guide",
    name="Z Scale"
    )
    guide_scale_4 : FloatVectorProperty(default=(1.0, 1.0, 1.0), precision=3,
    description="Scale for Bone in Weight Painting Guide",
    name="X Scale"
    )
    guide_scale_5 : FloatVectorProperty(default=(1.0, 1.0, 1.0), precision=3,
    description="Scale for Bone in Weight Painting Guide",
    name="Y Scale"
    )
    guide_scale_6 : FloatVectorProperty(default=(1.0, 1.0, 1.0), precision=3,
    description="Scale for Bone in Weight Painting Guide",
    name="Z Scale"
    )
    #Steps amount properties
    #Joint 6 Steps
    guide_joint_transforms_X6 : IntProperty(default=0, min=0, max=6,
    description="Scroll through the different rotations of the joint",
    update=joint_x6_update,
    name="6 Steps"
    )
    #Joint 4 Steps
    guide_joint_transforms_X4 : IntProperty(default=0, min=0, max=4,
    description="Scroll through the different rotations of the joint",
    update=joint_x4_update,
    name="4 Steps"
    )
    #Joint 2 Steps
    guide_joint_transforms_X2 : IntProperty(default=0, min=0, max=2,
    description="Scroll through the different rotations of the joint",
    update=joint_x2_update,
    name="2 Steps"
    )
    #Toggle All Bones
    guide_show_wp_bones : BoolProperty(default=0,
    description="Toggle Bone Visibility in BlenRig Weight Painting Guide",
    update=show_wp_bones_update,
    name="Show Bones"
    )

import bpy
from bpy.types import PropertyGroup, Object, Image
from bpy.props import *
from . traductor import languages
from . utils import *

class BlenRigBodyObj(PropertyGroup):
    character_body_obj : PointerProperty(type=Object)

class BlenRigJointChain(PropertyGroup):
    joint : StringProperty('')
    vgroup : StringProperty('')

class BlenRigWPBones(PropertyGroup):
    bone : StringProperty('')

class BlenRigShapekeysList(bpy.types.PropertyGroup):
    list_1 : StringProperty('')
    list_2 : StringProperty('')
    list_3 : StringProperty('')
    list_4 : StringProperty('')

class BlenrigGuideImages(PropertyGroup):
    image : PointerProperty(type=Image)

class BlenrigGuideData(PropertyGroup):
    # TODO: Port to PyGPU.
    def load_image(self, idx: int = 0):
        if idx < len(self.images):
            img = self.images[idx].image
            if img:
                img.gl_load()
                self.active_image = img

    def load_next_image(self):
        if self.image_index == (len(self.images)-1):
            self.image_index = 0
        else:
            self.image_index += 1
        self.load_image(self.image_index)

    def add_image(self, img: Image = None):
        if not img or not isinstance(img, Image):
            return
        if not self.active_image:
            img.gl_load()
            self.active_image = img
        container = self.images.add()
        container.image = img

    def clear_images(self):
        while self.images:
            self.images.remove(0)
        self.active_image = None
        self.image_index = 0

    language : EnumProperty(
        items=languages,
        name="Language"
    )
    dpi : IntProperty(default=72, min=72, max=300, name="Screen DPI")
    active_image : PointerProperty(type=Image)
    image_index : IntProperty(default=0)
    images : CollectionProperty(type=BlenrigGuideImages)
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
    #Shapkey Editting
    active_shp_obj : PointerProperty(type=Object)
    active_shapekey_name : StringProperty('')
    shapekeys_list_index : IntProperty(default=1, min=1, max=4, name="Shapekey List")
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

## Rig Settings Properties ##

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
    #Shoulder Automatic Movement
    guide_shoulder_auto_forw : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Shoulder Automatic Forwards Rotation on Arm movement",
    update=auto_shoulder_update,
    name="Shoulder Forwards"
    )
    guide_shoulder_auto_back : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Shoulder Automatic Backwards Rotation on Arm movement",
    update=auto_shoulder_update,
    name="Shoulder Backwards"
    )
    guide_shoulder_auto_up : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Shoulder Automatic Upwards Rotation on Arm movement",
    update=auto_shoulder_update,
    name="Shoulder Upwards"
    )
    guide_shoulder_auto_down : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Shoulder Automatic Downwards Rotation on Arm movement",
    update=auto_shoulder_update,
    name="Shoulder Downwards"
    )
    #Foot Roll
    guide_foot_roll_amp : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Foot Roll Controllers Rotation Range",
    update=foot_roll_update,
    name="Foot Roll Controller Rotation"
    )
    guide_foot_roll_toe_1 : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Angle for toe 1 to start rolling",
    update=foot_roll_update,
    name="Toe 1 Rotation Start"
    )
    guide_foot_roll_toe_2 : FloatProperty(default=0.000, min=0.000, max=180.000, precision=3,
    description="Angle for toe 2 to start rolling",
    update=foot_roll_update,
    name="Toe 2 Rotation Start"
    )
    #Volume Variation
    guide_vol_var_arms : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Stretch & Squash Volume Variation",
    update=vol_var_update,
    name="Arms Volume Variation"
    )
    guide_vol_var_fingers : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Stretch & Squash Volume Variation",
    update=vol_var_update,
    name="Fingers Volume Variation"
    )
    guide_vol_var_legs : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Stretch & Squash Volume Variation",
    update=vol_var_update,
    name="Legs Volume Variation"
    )
    guide_vol_var_toes : FloatProperty(default=0.000, min=0.000, max=100.000, precision=3,
    description="Stretch & Squash Volume Variation",
    update=vol_var_update,
    name="Toes Volume Variation"
    )
    #Floor Offset
    guide_feet_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=3,
    description="Feet Floor Offset Value",
    update=feet_floor_update,
    name="Feet Floor Offset"
    )
    guide_eyelid_1_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=5, step = 0.01,
    description="Eyelid 1 Floor Offset Value",
    update=facial_floor_update,
    name="Eyelid 1 Floor Offset"
    )
    guide_eyelid_2_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=5, step = 0.01,
    description="Eyelid 2 Floor Offset Value",
    update=facial_floor_update,
    name="Eyelid 2 Floor Offset"
    )
    guide_eyelid_3_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=5, step = 0.01,
    description="Eyelid 3 Floor Offset Value",
    update=facial_floor_update,
    name="Eyelid 3 Floor Offset"
    )
    guide_lip_1_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=5, step = 0.01,
    description="Lip 1 Floor Offset Value",
    update=facial_floor_update,
    name="Lip 1 Floor Offset"
    )
    guide_lip_2_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=5, step = 0.01,
    description="Lip 2 Floor Offset Value",
    update=facial_floor_update,
    name="Lip 2 Floor Offset"
    )
    guide_lip_3_floor : FloatProperty(default=0.000, min=-10.000, max=10.000, precision=5, step = 0.01,
    description="Lip 3 Floor Offset Value",
    update=facial_floor_update,
    name="Lip 3 Floor Offset"
    )
    #Facial Specials
    guide_mouth_corner_auto_back : FloatProperty(default=0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define how much the Mouth Corners move Backwards when they move Outwards with Mouth_Ctrl, representing the underlying volume of the teeth",
    update=corner_auto_back_update,
    name="Mouth Corner Auto Back"
    )
    guide_cheek_auto_smile : FloatProperty(default=0.000, min=-0.000, max=1.000, precision=3,
    description="Define how much the Cheek raises when the character smiles",
    update=cheek_auto_smile_update,
    name="Cheek Smile Following Rate"
    )
    guide_eyelid_up_up_follow : FloatProperty(default=0.000, min=-0.000, max=10.000, precision=3,
    description="Define how much the Upper Eyelid follows the upwards movement of the Eye",
    update=eyelids_up_follow_update,
    name="Upper Eylid Up Follow"
    )
    guide_eyelid_up_down_follow : FloatProperty(default=0.000, min=-0.000, max=10.000, precision=3,
    description="Define how much the Upper Eyelid follows the downwards movement of the Eye",
    update=eyelids_up_follow_update,
    name="Upper Eylid Down Follow"
    )
    guide_eyelid_low_up_follow : FloatProperty(default=0.000, min=-0.000, max=10.000, precision=3,
    description="Define how much the Lower Eyelid follows the upwards movement of the Eye",
    update=eyelids_low_follow_update,
    name="Lower Eylid Up Follow"
    )
    guide_eyelid_low_down_follow : FloatProperty(default=0.000, min=-0.000, max=10.000, precision=3,
    description="Define how much the Lower Eyelid follows the downwards movement of the Eye",
    update=eyelids_low_follow_update,
    name="Lower Eylid Down Follow"
    )
    guide_eyelid_auto_cheek : FloatProperty(default=0.000, min=-0.000, max=100.000, precision=3,
    description="Define how much the Lower Eyelid follows the Upwards movement of the Cheek",
    update=eyelid_auto_cheek_update,
    name="Lower Eylid Cheek Follow"
    )
    #Lip Shaping
    guide_lips_motion_curvature : FloatProperty(default=0.000, min=-5.000, max=5.000, precision=3,
    description="Define the Curvature of the lips when they move",
    update=lip_curvature_update,
    name="Lip Curvature"
    )
    guide_lip_1_rigidity : FloatProperty(default=0.000, min=0.000, max=1.000, precision=3,
    description="Define how much the joints of the lip stretch towards the mouth corner",
    update=lip_rigidity_update,
    name="Lip 1 Rigidity"
    )
    guide_lip_2_rigidity : FloatProperty(default=0.000, min=0.000, max=1.000, precision=3,
    description="Define how much the joints of the lip stretch towards the mouth corner",
    update=lip_rigidity_update,
    name="Lip 2 Rigidity"
    )
    guide_lip_3_rigidity : FloatProperty(default=0.000, min=0.000, max=1.000, precision=3,
    description="Define how much the joints of the lip stretch towards the mouth corner",
    update=lip_rigidity_update,
    name="Lip 3 Rigidity"
    )
    guide_lip_1_curvature_override : FloatVectorProperty(default=(0.0, 0.0, 0.0), min=0.000, max=100.000, precision=3,
    description="Tweak value (XYZ) to override the default curvature of the lips",
    update=lip_override_update,
    name="Lip 1 motion Override"
    )
    guide_lip_2_curvature_override : FloatVectorProperty(default=(0.0, 0.0, 0.0), min=0.000, max=100.000, precision=3,
    description="Tweak value (XYZ) to override the default curvature of the lips",
    update=lip_override_update,
    name="Lip 2 motion Override"
    )
    guide_lip_3_curvature_override : FloatVectorProperty(default=(0.0, 0.0, 0.0), min=0.000, max=100.000, precision=3,
    description="Tweak value (XYZ) to override the default curvature of the lips",
    update=lip_override_update,
    name="Lip 3 motion Override"
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
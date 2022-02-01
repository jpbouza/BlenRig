import bpy
from bpy.types import PropertyGroup, Object, Image
from bpy.props import *
from . traductor import languages
from . utils import *
from . dev import DEBUG


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

    ##########################################

    '''
    def init(self, context, gz: 'BLENRIG_GZ_guide' = None):
        print("GUIDE::init")
        if not self.enabled:
            return
        if not self.active_guide_id:
            return
        if not gz:
            from . guide_gz import BLENRIG_GZ_guide
            gz = BLENRIG_GZ_guide.get()
            if not gz:
                print("No Gizmo, it will init data once it is instanciated!")
                return
        from . guides import GuideSteps
        guide_id, step = self.active_guide_id.split('#')
        guide_steps, guide_endstep_action = GuideSteps.get(guide_id)
        gz.guide_steps = guide_steps
        gz.max_step_index = len(guide_steps) - 1
        gz.guide_name = guide_id.lower()
        gz.end_of_step_action = guide_endstep_action
        gz.load_step(context, int(step))

        #from . guide_wg import BLENRIG_WG_guide
        #BLENRIG_WG_guide.time_fun(
        #    ,
        #    time=0.5
        #)
    '''

    def update(self, context):
        if not self.enabled:
            return
        if not self.active_guide_id:
            return
        DEBUG("GuideData::update")
        from . guide_gz import BLENRIG_GZ_guide
        gz = BLENRIG_GZ_guide.get()
        if not gz:
            DEBUG("\t|- No Gizmo detected!")
            return
        gz.needs_update = True
        return
        #gz.init(context, update=True)
        from . guides import GuideSteps
        guide_id, step = self.active_guide_id.split('#')
        guide_steps, guide_endstep_action = GuideSteps.get(guide_id)
        gz.guide_steps = guide_steps
        gz.max_step_index = len(guide_steps) - 1
        gz.guide_name = guide_id.lower()
        gz.end_of_step_action = guide_endstep_action
        gz.load_step(context, int(step))
        DEBUG("GuideData::update >> end")

    enabled : BoolProperty(default=False)
    active_guide_id : StringProperty(default='', update=update)
    active_guide_name : StringProperty(default='')

    def enable(self, guide_id: 'GuideSteps' or 'BlenrigGuide_BaseOperator' or str, start_step: int = 0):
        DEBUG("GuideData::enable (%s)" % str(guide_id))
        from . guides import GuideSteps
        from . guide_ops import BlenrigGuide_BaseOperator
        if isinstance(guide_id, str):
            if hasattr(GuideSteps, guide_id.upper()):
                guide_id = guide_id.upper()
            else:
                DEBUG("GuideData::enable >> invalid string for guide idname")
                return
        elif isinstance(guide_id, GuideSteps):
            guide_id = guide_id.get_id()
        elif isinstance(guide_id, BlenrigGuide_BaseOperator):
            start_step = guide_id.step
            guide_id = guide_id.guide_name
        else:
            DEBUG("GuideData::enable >> invalid type for guide idname")
            return
        self.enabled = True
        self.active_guide_name = guide_id
        self.active_guide_id = '%s#%s' % (guide_id, start_step)

    def disable(self):
        DEBUG("GuideData::disable")
        self.enabled = False
        self.active_guide_id = ''
        self.active_guide_name = ''

    ##########################################

    # TODO: Port to PyGPU.
    def load_image(self, idx: int = 0):
        DEBUG("GuideData::load_image (%i)" % idx)
        if idx >= len(self.images) or idx < 0:
            return
        img = self.images[idx].image
        if not img:
            return
        img.gl_load()
        self.active_image = img

    def load_next_image(self):
        DEBUG("GuideData::load_next_image")
        if self.image_index == (len(self.images)-1):
            self.image_index = 0
        else:
            self.image_index += 1
        self.load_image(self.image_index)

    def add_image(self, img: Image = None):
        DEBUG("GuideData::add_image (%s)" % str(img))
        if not img or not isinstance(img, Image):
            DEBUG("\t|- Could not add image, invalid or null!")
            return
        if not self.active_image:
            img.gl_load()
            self.active_image = img
        container = self.images.add()
        container.image = img

    def clear_images(self):
        nimages = len(self.images)
        DEBUG("GuideData::clear_images (%i)" % nimages)
        while nimages > 0: # self.images:
            self.images.remove(0)
            nimages -= 1
        self.active_image = None
        self.image_index = 0

    language : EnumProperty(
        items=languages,
        name="Language"
    )

    def only_one_visible(self, context):
        print(self.name)
        targets = [
                    self.show_steps_guide_reproportion,
                    self.show_steps_guide_datatransfer,
                    self.show_steps_guide_mdef,
                    self.show_steps_guide_lattices,
                    self.show_steps_guide_actions,
                    self.show_steps_guide_weights,
                    self.show_steps_guide_rig_settings,
                    self.show_steps_guide_shapekeys
                ]
        for prop in targets:
            print('prop', prop)

    dpi : IntProperty(default=72, min=72, max=300, name="Screen DPI")
    active_image : PointerProperty(type=Image)
    image_index : IntProperty(default=0)
    images : CollectionProperty(type=BlenrigGuideImages)
    image_scale : FloatProperty(default=1, min=0.5, max=4, name="Image Scale")
    show_steps : BoolProperty(default=False, name="Steps Guide")

    # show_steps_guide_reproportion : BoolProperty(default=False, name="Show Steps Guide Reproportion", update=only_one_visible)
    # show_steps_guide_datatransfer : BoolProperty(default=False, name="Show Steps Guide Datatransfer", update=only_one_visible)
    # show_steps_guide_mdef : BoolProperty(default=False, name="Show Steps Guide Mdef")
    # show_steps_guide_lattices : BoolProperty(default=False, name="Show Steps Guide Lattices")
    # show_steps_guide_actions : BoolProperty(default=False, name="Show Steps Guide Actions")
    # show_steps_guide_weights : BoolProperty(default=False, name="Show Steps Guide Weights")
    # show_steps_guide_rig_settings : BoolProperty(default=False, name="Show Steps Rig Settings")
    # show_steps_guide_shapekeys : BoolProperty(default=False, name="Show Steps Guide Shapekeys")

    def expand_steps(self, context):
        if not context.scene.blenrig_guide.show_steps:
            context.scene.blenrig_guide.show_steps = True

    show_steps_guide: EnumProperty(
        items=(
            ("REPROPORTION", "Reproportion", "Show Steps Guide Reproportion", 'DOWNARROW_HLT', 0),
            ("DATATRANFER", "Data Transfer", "Show Steps Guide Datatransfer", 'DOWNARROW_HLT', 1),
            ("MDEF", "Mesh Deform", "Show Steps Guide Mdef", 'DOWNARROW_HLT', 2),
            ("LATTICES", "Lattices", "Show Steps Guide Lattices", 'DOWNARROW_HLT', 3),
            ("ACTIONS", "Actions", "Show Steps Guide Actions", 'DOWNARROW_HLT', 4),
            ("WHEIGHTS", "Weights", "Show Steps Guide Weight", 'DOWNARROW_HLT', 5),
            ("RIGSETTINGS", "Rig Settgins", "Show Steps Rig Settings", 'DOWNARROW_HLT', 6),
            ("SHAPEKEYS", "Shape Keys", "Show Steps Guide Shapekeys", 'DOWNARROW_HLT', 7),
        ),
        name="Steps",
        description="Show Steps Guide",
        default="REPROPORTION",
        update=expand_steps
    )

    guide_current_step : StringProperty('')
    #BlenRig Armature
    obj : PointerProperty(type=Object) # temporal object slot.
    arm_obj : PointerProperty(type=Object)
    #BlenRig Reproportion
    guide_lock_center_bones : BoolProperty(default=0,
    description="Lock the X Transform for the Center Bones of the Rig",
    update=lock_center_bones_update,
    name="Lock Center Bones"
    )
    #BlenRig Weights Transfer Meshes
    mdef_head_weights_transfer_obj : PointerProperty(type=Object)
    mdef_hands_weights_transfer_obj : PointerProperty(type=Object)
    #BlenRig Mdef Cage
    mdef_cage_obj : PointerProperty(type=Object)
    #Character Objects
    character_head_obj : PointerProperty(type=Object)
    character_hands_obj : PointerProperty(type=Object)
    character_toes_obj : PointerProperty(type=Object)
    #Weight Paint Object
    active_wp_obj : PointerProperty(type=Object)
    auto_mirror_vp_rj_values : BoolProperty(default=True, name="Auto Mirror VP and RJ values", description="Automatically Mirror Edited Realistic Joints and Volume Preservation value on Step Change")
    #Shapkey Editting
    active_shp_obj : PointerProperty(type=Object)
    active_shapekey_name : StringProperty('')
    shapekeys_list_index : IntProperty(default=1, min=1, max=4, name="Shapekey List")
    auto_mirror_shapekeys : BoolProperty(default=True, name="Auto Mirror Shapekeys", description="Automatically Mirror Edited Shapkeys on Step Change")
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
    guide_u_o_m : FloatProperty(default=0.02, min=0.0001, max=1.000, precision=3,
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
    #Blink Rate
    blink_rate : FloatProperty(default=0.000, min=0.000, max=1.000, precision=5, step = 0.01,
    description="Define the Blink Rate",
    update=blink_rate_update,
    name="Blink Rate"
    )
    #Fleshy Eyes
    fleshy_eyes_rate : FloatProperty(default=0.000, min=0.000, max=1.000, precision=3,
    description="Define the Blink Rate",
    update=fleshy_eyes_rate_update,
    name="Fleshy Eyes Rate"
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
    #BBone Curves
    #Brows
    guide_bbone_vertical_curve_in_brows : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_brows_update,
    name="Vertical Curve In"
    )
    guide_bbone_vertical_curve_out_brows : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_brows_update,
    name="Vertical Curve In"
    )
    guide_bbone_depth_curve_in_brows : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_brows_update,
    name="Depth Curve In"
    )
    guide_bbone_depth_curve_out_brows : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_brows_update,
    name="Depth Curve In"
    )
    #Lip Up
    guide_bbone_vertical_curve_in_lip_up : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_lips_update,
    name="Vertical Curve In"
    )
    guide_bbone_vertical_curve_out_lip_up : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_lips_update,
    name="Vertical Curve Out"
    )
    guide_bbone_depth_curve_in_lip_up : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_lips_update,
    name="Depth Curve In"
    )
    guide_bbone_depth_curve_out_lip_up : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_lips_update,
    name="Depth Curve Out"
    )
    #Lip Low
    guide_bbone_vertical_curve_in_lip_low : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_lips_update,
    name="Vertical Curve In"
    )
    guide_bbone_vertical_curve_out_lip_low : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_lips_update,
    name="Vertical Curve Out"
    )
    guide_bbone_depth_curve_in_lip_low : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_lips_update,
    name="Depth Curve In"
    )
    guide_bbone_depth_curve_out_lip_low : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_lips_update,
    name="Depth Curve Out"
    )
    #Lip Zipper
    guide_bbone_vertical_curve_in_lip_zipper : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_lips_update,
    name="Vertical Curve In"
    )
    guide_bbone_vertical_curve_out_lip_zipper : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Vertical Curvature",
    update=bbone_curve_lips_update,
    name="Vertical Curve Out"
    )
    guide_bbone_depth_curve_in_lip_zipper : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_lips_update,
    name="Depth Curve In"
    )
    guide_bbone_depth_curve_out_lip_zipper : FloatProperty(default=-0.000, min=-1000.000, max=1000.000, precision=3,
    description="Define BBone Depth Curvature",
    update=bbone_curve_lips_update,
    name="Depth Curve Out"
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
    description="Toggle Bone Visibility in BlenRig Guides",
    update=show_wp_bones_update,
    name="Show All Bones"
    )
    #Toggle Deformation Bones
    guide_show_def_bones : BoolProperty(default=0,
    description="Toggle Deformation Bone Visibility in BlenRig Actions Guide",
    update=show_def_bones_update,
    name="Show Deformation Bones"
    )
    #Toggle Mdef Cage
    guide_show_mdef_cage : BoolProperty(default=0,
    description="Toggle Mdef Cage Visibility in BlenRig Weights Transfer Guide",
    update=show_mdef_cage_update,
    name="Show Mdef Cage"
    )

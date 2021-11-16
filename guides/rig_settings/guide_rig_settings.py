from os.path import dirname, join
from .. rig_settings.guide_rig_settings_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_SETTINGS = (
    #Settings Intro
    {
        'imagen': 'SETTINGS_Intro.jpg',
        'titulo': {
            'EN': 'Introduction',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "In this Guide we will fine tune some of the parameters of the Rig",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Intro
    },
    #Shoulder Automatic Movement
    {
        'imagen': ('SETTINGS_Shoulder_Movement_A.jpg', 'SETTINGS_Shoulder_Movement_B.jpg', 'SETTINGS_Shoulder_Movement_C.jpg', 'SETTINGS_Shoulder_Movement_D.jpg'),
        'titulo': {
            'EN': 'Shoulder Movement',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Shoulder moves along with the Arm with the Automatic Movement Values. Move the Character's hand around to preview the result.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Shoulder_Movement
    },
    #Torso Rotation
    {
        'imagen': 'SETTINGS_Torso_Rotation.jpg',
        'titulo': {
            'EN': 'Torso Rotation Rate',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Spine Joints follow the Main Torso Controller. Rotate 'torso_fk_ctrl' to preview the result.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Torso_Rotation
    },
    #Neck Rotation
    {
        'imagen': 'SETTINGS_Neck_Rotation.jpg',
        'titulo': {
            'EN': 'Neck Rotation Rate',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Neck Joints follow the Main Neck Controller. Rotate 'neck_fk_ctrl' to preview the result.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Neck_Rotation
    },
    #Torso Inverted Rotation
    {
        'imagen': 'SETTINGS_Torso_Inv_Rotation.jpg',
        'titulo': {
            'EN': 'Inverted Torso Rotation Rate',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Spine Joints follow the Inverted Torso Controller. Rotate 'torso_fk_ctrl_inv' to preview the result.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Torso_Inv_Rotation
    },
    #Torso Stretching Curve
    {
        'imagen': ('SETTINGS_Torso_Stretching_A.jpg', 'SETTINGS_Torso_Stretching_B.jpg', 'SETTINGS_Torso_Stretching_C.jpg'),
        'titulo': {
            'EN': 'Torso Stretching Curve',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the curvature of the Joints when the Spine stretches",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Torso_Stretching
    },
    #Torso Pelvis Compensation
    {
        'imagen': ('SETTINGS_Pelvis_Compensation_A.jpg', 'SETTINGS_Pelvis_Compensation_B.jpg'),
        'titulo': {
            'EN': 'Torso Pelvis Compensation',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the torso automatically compensates the rotation of the Pelvis. Rotate the Pevlis to preview the result. This feature might be good for posing but not for animation, use it carefully or don't use it at all ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Pelvis_Compensation
    },
    #Foot Roll
    {
        'imagen': ('SETTINGS_Foot_Roll_A.jpg', 'SETTINGS_Foot_Roll_B.jpg', 'SETTINGS_Foot_Roll_C.jpg', 'SETTINGS_Foot_Roll_D.jpg'),
        'titulo': {
            'EN': 'Foot Roll',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Tweak the Foot Roll behavior. Define the 'Rasing Start Angle' values that better suit your character. Preview the result by rotating 'foot_roll_ctrl_L'.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Foot_Roll
    },
    #Volume Variation
    {
        'imagen': ('SETTINGS_Volume_Variation_A.jpg', 'SETTINGS_Volume_Variation_B.jpg', 'SETTINGS_Volume_Variation_A.jpg', 'SETTINGS_Volume_Variation_C.jpg'),
        'titulo': {
            'EN': 'Volume Variation',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use the Controllers to Squash and Stretch body parts. Define how their volume changes on this motions with the Volume Variation Values. A range between 0.0 and 4.0 is recommended",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Volume_Variation
    },
    #Foot Floor
    {
        'imagen': ('SETTINGS_Feet_Floor_A.jpg', 'SETTINGS_Feet_Floor_B.jpg'),
        'titulo': {
            'EN': 'Foot Floor',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Move the Foot Floor Controller up and check if it collides correctly with the character's foot. Tweak the Collision value if needed.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Feet_Floor
    },
    #Eyelids Floor
    {
        'imagen': ('SETTINGS_Eyelids_Floor_A.jpg', 'SETTINGS_Eyelids_Floor_B.jpg', 'SETTINGS_Eyelids_Floor_C.jpg'),
        'titulo': {
            'EN': 'Eyelids Collision',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Move the Upper Eyelid down with 'eyelid_up_ctrl_L' until it overlaps with the Lower Eyelid. Tweak the Collision Values of each joint so that the automatic Collision looks natural.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Eyelids_Floor
    },
    #Blink Rate
    {
        'imagen': 'SETTINGS_Blink.jpg',
        'titulo': {
            'EN': 'Blink Rate',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Modify the 'Blink Rate' slider value so that the eyelids touch at the middle of the Eye",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Blink
    },
    #Eye Movement Follow
    {
        'imagen': ('SETTINGS_Eyelids_Follow_A.jpg', 'SETTINGS_Eyelids_Follow_B.jpg', 'SETTINGS_Eyelids_Follow_C.jpg', 'SETTINGS_Eyelids_Follow_D.jpg', 'SETTINGS_Eyelids_Follow_E.jpg'),
        'titulo': {
            'EN': 'Eye Movement Follow',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Move the Look Controller Upwards and define how much the Eyelids follow the movement of the Eye with the Upwards Movement Values. Then, move the Look Controller Downwards and do the same with the Downwards Movement Values.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Eyelids_Follow
    },
    #Fleshy Eyes
    {
        'imagen': ('SETTINGS_Fleshy_Eyes_A.jpg', 'SETTINGS_Fleshy_Eyes_B.jpg', 'SETTINGS_Fleshy_Eyes_C.jpg'),
        'titulo': {
            'EN': 'Fleshy Eyes',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Move the Look Controller horizontally and modify the 'Fleshy Eyes' slider to define how much the Eyeball moves when looking to the side. This effect is specially interesting for Cartoony characters. ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Fleshy_Eyes
    },
    #Eyelid Cheek Movement Follow
    {
        'imagen': ('SETTINGS_Eyelids_Cheek_Follow_A.jpg', 'SETTINGS_Eyelids_Cheek_Follow_B.jpg'),
        'titulo': {
            'EN': 'Eyelid Cheek Movement Follow',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Lower Eyelid follows the movement of the Cheek. Move the Cheek controller to check if the resulting motion looks natural.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Eyelids_Cheek_Follow
    },
    #Cheek Smile Movement Follow
    {
        'imagen': ('SETTINGS_Cheek_Smile_Follow_A.jpg', 'SETTINGS_Cheek_Smile_Follow_B.jpg'),
        'titulo': {
            'EN': 'Cheek Smile Movement Follow',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Cheek follows the Smile. Move the Mouth Corner controller to check if the resulting motion looks natural.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Cheek_Smile_Follow
    },
    #Mouth Corner Auto Back
    {
        'imagen': ('SETTINGS_Coner_Auto_Back_A.jpg', 'SETTINGS_Coner_Auto_Back_B.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Auto Back',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define how much the Mouth Corners move Backwards when the Mouth Widens. This motion is intended to simulate how the Lips move around the underlying Teeth volume",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Coner_Auto_Back
    },
    #Lips Floor
    {
        'imagen': ('SETTINGS_Lips_Floor_A.jpg', 'SETTINGS_Lips_Floor_B.jpg', 'SETTINGS_Lips_Floor_C.jpg'),
        'titulo': {
            'EN': 'Lips Collision',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Put the lips together with 'mouth_ctrl' and tweak the Collision Values of each joint so that the automatic Collision looks natural.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Lips_Floor
    },
    #Lip Curvature & Rigidity
    {
        'imagen': ('SETTINGS_Lip_Curvature_A.jpg', 'SETTINGS_Lip_Curvature_B.jpg'),
        'titulo': {
            'EN': 'Lips Settings',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Basic Curvature of the Lips. If needed tweak the Rigidity values to define how much the Joints stretch towards the Mouth Corner. Finally you can override the amount in which the Joints follow the Mouth Corner in XYZ. Move the Mouth Corner around to preview the result",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Lip_Curvature
    },
    #Finish
    {
        'imagen': 'SETTINGS_Finish.jpg',
        'titulo': {
            'EN': 'Settings FInish',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Great! Finish refining Deformation with the Shapekeys Guide ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SETTINGS_Finish
    },
)





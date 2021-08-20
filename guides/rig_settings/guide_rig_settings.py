from os.path import dirname, join
from .. rig_settings.guide_rig_settings_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_SETTINGS = (
    #Shoulder Automatic Movement
    {
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
    #Eye Movement Follow
    {
        'imagen': 'DT_Finish_A.jpg',
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
    #Eyelid Cheek Movement Follow
    {
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
        'imagen': 'DT_Finish_A.jpg',
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
)





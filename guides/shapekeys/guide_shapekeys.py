from os.path import dirname, join
from .. shapekeys.guide_shapekeys_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_SHAPEKEYS = (
    #Shapekeys Intro
    {
        'imagen': 'SHAPEKEYS_Intro.jpg',
        'titulo': {
            'EN': 'Introduction',
            'ES': 'Introduccion'
            },
        'texto': {
            'EN': "Edit the Shapekeys to achieve the Final Deformation of the Character. The idea is to 'Correct what you see'. You won't need to select any Shapekey or Mirror them, just go correcting the poses on the fly.",
            'ES': 'Edita las Shapekeys para lograr la Deformación Final del Personaje. La idea es ''Corregir lo que ves''. No necesitará seleccionar ninguna Shapekey o Espejarlas, simplemente ve corrigiendo las poses sobre la marcha.'
            },
        'accion': SHAPEKEYS_Intro
    },
    #Shapekeys Intro 2
    {
        'imagen': ('SHAPEKEYS_Intro_2_A.jpg', 'SHAPEKEYS_Intro_2_B.jpg'),
        'titulo': {
            'EN': 'Workflow',
            'ES': 'Flujo de Trabajo'
            },
        'texto': {
            'EN': "To tweak the pose of the active shapekey, you can Toggle outside of Shapekeys Editting and manipulate the rig. Then press the 'Update Driver with Current Pose' Button. Don't edit the Shapekey if the color marking is Red.",
            'ES': 'Para ajustar la pose de la shapekey activa, puedes salir de la edicion Shapekeys y manipular el rig. Luego presiona el botón ''Actualizar controlador con pose actual''. No edites la Shapekey si la marca de color esta en Rojo.'
            },
        'accion': SHAPEKEYS_Intro_2
    },
    #Add Body Shapekeys
    {
        'imagen': 'SHAPEKEYS_Cage_Add_Body_Shapes.jpg',
        'titulo': {
            'EN': 'Add Body Shapekeys',
            'ES': 'Añadir Shapekeys del Cuerpo'
            },
        'texto': {
            'EN': "Select the Mesh Deform Cage and press the 'Add Body Shapekeys' Button.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Add_Body_Shapes
    },
    #Ankle
    {
        'imagen': ('SHAPEKEYS_Cage_Ankle_A.jpg', 'SHAPEKEYS_Cage_Ankle_B.jpg', 'SHAPEKEYS_Cage_Ankle_C.jpg', 'SHAPEKEYS_Cage_Ankle_D.jpg',),
        'titulo': {
            'EN': 'Ankle',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-6). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Ankle
    },
    #Foot Toe
    {
        'imagen': ('SHAPEKEYS_Cage_Foot_Toe_A.jpg', 'SHAPEKEYS_Cage_Foot_Toe_B.jpg'),
        'titulo': {
            'EN': 'Foot Toe',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Foot_Toe
    },
    #Knee
    {
        'imagen': ('SHAPEKEYS_Cage_Knee_A.jpg', 'SHAPEKEYS_Cage_Knee_B.jpg'),
        'titulo': {
            'EN': 'Knee',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Knee
    },
    #Thigh
    {
        'imagen': 'SHAPEKEYS_Cage_Thigh.jpg',
        'titulo': {
            'EN': 'Thigh',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Thigh
    },
    #Torso
    {
        'imagen': ('SHAPEKEYS_Cage_Torso_A.jpg', 'SHAPEKEYS_Cage_Torso_B.jpg', 'SHAPEKEYS_Cage_Torso_C.jpg', 'SHAPEKEYS_Cage_Torso_D.jpg', 'SHAPEKEYS_Cage_Torso_E.jpg', 'SHAPEKEYS_Cage_Torso_F.jpg'),
        'titulo': {
            'EN': 'Torso',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Torso
    },
    #Breathing
    {
        'imagen': ('SHAPEKEYS_Cage_Breathing_A.jpg', 'SHAPEKEYS_Cage_Breathing_B.jpg'),
        'titulo': {
            'EN': 'Breathing In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the 'Breathing In' Shapekey. Expand the Rib Cage and Tummy.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Breathing
    },
    #Neck
    {
        'imagen': ('SHAPEKEYS_Cage_Neck_A.jpg', 'SHAPEKEYS_Cage_Neck_B.jpg', 'SHAPEKEYS_Cage_Neck_C.jpg', 'SHAPEKEYS_Cage_Neck_D.jpg'),
        'titulo': {
            'EN': 'Neck',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Neck
    },
    #Clavicle
    {
        'imagen': ('SHAPEKEYS_Cage_Clavicle_A.jpg', 'SHAPEKEYS_Cage_Clavicle_B.jpg'),
        'titulo': {
            'EN': 'Clavicle',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Clavicle
    },
    #Shoulder
    {
        'imagen': ('SHAPEKEYS_Cage_Shoulder_A.jpg', 'SHAPEKEYS_Cage_Shoulder_B.jpg', 'SHAPEKEYS_Cage_Shoulder_C.jpg', 'SHAPEKEYS_Cage_Shoulder_D.jpg'),
        'titulo': {
            'EN': 'Arm / Shoulder',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Shoulder
    },
    #Elbow
    {
        'imagen': ('SHAPEKEYS_Cage_Elbow_A.jpg', 'SHAPEKEYS_Cage_Elbow_B.jpg'),
        'titulo': {
            'EN': 'Elbow',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Elbow
    },
    #Wrist
    {
        'imagen': ('SHAPEKEYS_Cage_Wrist_A.jpg', 'SHAPEKEYS_Cage_Wrist_B.jpg'),
        'titulo': {
            'EN': 'Wrist',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-6). On each Pose, edit the Mdef Cage to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Cage_Wrist
    },
    #Add Fingers Shapekeys
    {
        'imagen': 'SHAPEKEYS_Char_Add_Fingers_Shapes.jpg',
        'titulo': {
            'EN': 'Add Fingers Shapekeys',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select the Hands and press the 'Add Fingers Shapekeys' Button.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Add_Fingers_Shapes
    },
    #Thumb Finger Palm
    {
        'imagen': ('SHAPEKEYS_Char_Thumb_1_A.jpg', 'SHAPEKEYS_Char_Thumb_1_B.jpg', 'SHAPEKEYS_Char_Thumb_1_C.jpg'),
        'titulo': {
            'EN': 'Thumb Finger Palm',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Palm Shapekeys for when the Thumb Fnger moves around. Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Thumb_1
    },
    #Little Finger Palm
    {
        'imagen': ('SHAPEKEYS_Char_Lit_1_A.jpg', 'SHAPEKEYS_Char_Lit_1_B.jpg', 'SHAPEKEYS_Char_Lit_1_C.jpg'),
        'titulo': {
            'EN': 'Little Finger Palm',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Muscle Bulging of the Palm when the Little Finger moves In.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Lit_1
    },
    #Thumb Finger
    {
        'imagen': ('SHAPEKEYS_Char_Thumb_Joints_A.jpg', 'SHAPEKEYS_Char_Thumb_Joints_B.jpg'),
        'titulo': {
            'EN': 'Thumb Finger',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-2). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Thumb_Joints
    },
    #Index Finger
    {
        'imagen': ('SHAPEKEYS_Char_Index_Joints_A.jpg', 'SHAPEKEYS_Char_Index_Joints_B.jpg', 'SHAPEKEYS_Char_Index_Joints_C.jpg'),
        'titulo': {
            'EN': 'Index Finger',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-2). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Index_Joints
    },
    #Middle Finger
    {
        'imagen': ('SHAPEKEYS_Char_Middle_Joints_A.jpg', 'SHAPEKEYS_Char_Middle_Joints_B.jpg', 'SHAPEKEYS_Char_Middle_Joints_C.jpg'),
        'titulo': {
            'EN': 'Middle Finger',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-2). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Middle_Joints
    },
    #Ring Finger
    {
        'imagen': ('SHAPEKEYS_Char_Ring_Joints_A.jpg', 'SHAPEKEYS_Char_Ring_Joints_B.jpg', 'SHAPEKEYS_Char_Ring_Joints_C.jpg'),
        'titulo': {
            'EN': 'Ring Finger',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-2). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Ring_Joints
    },
    #Little Finger
    {
        'imagen': ('SHAPEKEYS_Char_Little_Joints_A.jpg', 'SHAPEKEYS_Char_Little_Joints_B.jpg', 'SHAPEKEYS_Char_Little_Joints_C.jpg'),
        'titulo': {
            'EN': 'Little Finger',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the key Poses with the 'Set Joint Transform' slider (0-2). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Little_Joints
    },
    #Add Face Shapekeys
    {
        'imagen': 'SHAPEKEYS_Char_Add_Face_Shapes.jpg',
        'titulo': {
            'EN': 'Add Face Shapekeys',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select the Face and press the 'Add Face Shapekeys' Button.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Add_Face_Shapes
    },
    #Eyebrow Up
    {
        'imagen': ('SHAPEKEYS_Char_Eyebrow_Up_A.jpg', 'SHAPEKEYS_Char_Eyebrow_Up_B.jpg', 'SHAPEKEYS_Char_Eyebrow_Up_C.jpg'),
        'titulo': {
            'EN': 'Eyebrow Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Eyebrow Up General Shapekey. Once satisfied, press the 'Apply Shape' Button to propagate the Shapekey to the corresponding Eyebrow Shapekeys ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyebrow_Up
    },
    #Eyebrow Down
    {
        'imagen': ('SHAPEKEYS_Char_Eyebrow_Down_A.jpg', 'SHAPEKEYS_Char_Eyebrow_Down_B.jpg', 'SHAPEKEYS_Char_Eyebrow_Down_C.jpg'),
        'titulo': {
            'EN': 'Eyebrow Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Eyebrow Down General Shapekey. Once satisfied, press the 'Apply Shape' Button to propagate the Shapekey to the corresponding Eyebrow Shapekeys ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyebrow_Down
    },
    #Eyebrow Vertex Groups
    {
        'imagen': ('SHAPEKEYS_Char_Eyebrow_Weight_A.jpg', 'SHAPEKEYS_Char_Eyebrow_Weight_B.jpg', 'SHAPEKEYS_Char_Eyebrow_Weight_C.jpg', 'SHAPEKEYS_Char_Eyebrow_Weight_D.jpg', 'SHAPEKEYS_Char_Eyebrow_Weight_E.jpg'),
        'titulo': {
            'EN': 'Eyebrow Vertex Groups',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit Eyebrow 1 to 5 Vertex Groups. This defines how the Eyebrow Shapekey is mixed among the Eyebrow Joints. Change the Active Vertex Group with 'Select Shapekey Vertex Group'. Paint the transition between the groups with a 0.5 value.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyebrow_Weight
    },
    #Frown Up
    {
        'imagen': ('SHAPEKEYS_Char_Frown_Up_A.jpg', 'SHAPEKEYS_Char_Frown_Up_B.jpg'),
        'titulo': {
            'EN': 'Frown Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Frown Up Shapekey.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Frown_Up
    },
    #Frown Down
    {
        'imagen': ('SHAPEKEYS_Char_Frown_Down_A.jpg', 'SHAPEKEYS_Char_Frown_Down_B.jpg'),
        'titulo': {
            'EN': 'Frown Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Frown Down Shapekey.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Frown_Down
    },
    #Eyebrow In
    {
        'imagen': ('SHAPEKEYS_Char_Eyebrow_In_A.jpg', 'SHAPEKEYS_Char_Eyebrow_In_B.jpg', 'SHAPEKEYS_Char_Eyebrow_In_C.jpg', 'SHAPEKEYS_Char_Eyebrow_In_D.jpg'),
        'titulo': {
            'EN': 'Eyebrow In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "This Shapekey should define the Wrinkle that appears on the Frown when the character gets Angry.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyebrow_In
    },
    #Upper Eyelid Up
    {
        'imagen': 'SHAPEKEYS_Char_Eyelid_Up_Up.jpg',
        'titulo': {
            'EN': 'Eyelid Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Upper Eyelid Upwards Shapekey.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyelid_Up_Up
    },
    #Upper Eyelid Half Way Down
    {
        'imagen': ('SHAPEKEYS_Char_Eyelid_Up_Down_1_A.jpg', 'SHAPEKEYS_Char_Eyelid_Up_Down_1_B.jpg', 'SHAPEKEYS_Char_Eyelid_Up_Down_1_C.jpg', 'SHAPEKEYS_Char_Eyelid_Up_Down_1_D.jpg'),
        'titulo': {
            'EN': 'Upper Eyelid Half Way Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Place the Upper Eyelid Border at the middle of the Eye. Then, press 'Update Driver with Current Pose' to update values. Finally Press 'Toggle Shapekey Editting' and edit the Mesh in this Half Way pose.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyelid_Up_Down_1
    },
    #Upper Eyelid Down
    {
        'imagen': ('SHAPEKEYS_Char_Eyelid_Up_Down_2_A.jpg', 'SHAPEKEYS_Char_Eyelid_Up_Down_2_B.jpg'),
        'titulo': {
            'EN': 'Upper Eyelid Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Closed Upper Eyelid Shapekey. If the Eye is clipping through the Eyelid, this is the time to fix it.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyelid_Up_Down_2
    },
    #Lower Eyelid Down
    {
        'imagen': 'SHAPEKEYS_Char_Eyelid_Low_Down.jpg',
        'titulo': {
            'EN': 'Lower Eyelid Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Lower Eyelid Downwards Shapekey",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyelid_Low_Down
    },
    #Lower Eyelid Half Way Up
    {
        'imagen': ('SHAPEKEYS_Char_Eyelid_Low_Up_1_A.jpg', 'SHAPEKEYS_Char_Eyelid_Low_Up_1_B.jpg', 'SHAPEKEYS_Char_Eyelid_Low_Up_1_C.jpg', 'SHAPEKEYS_Char_Eyelid_Low_Up_1_D.jpg'),
        'titulo': {
            'EN': 'Lower Eyelid Half Way Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Place the Lower Eyelid Border at the middle of the Eye. Then, press 'Update Driver with Current Pose' to update values. Finally Press 'Toggle Shapekey Editting' and edit the Mesh in this Half Way pose.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyelid_Low_Up_1
    },
    #Lower Eyelid Up
    {
        'imagen': ('SHAPEKEYS_Char_Eyelid_Low_Up_2_A.jpg', 'SHAPEKEYS_Char_Eyelid_Low_Up_2_B.jpg'),
        'titulo': {
            'EN': 'Lower Eyelid Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Closed Lower Eyelid Shapekey. If the Eye is clipping through the Eyelid, this is the time to fix it.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Eyelid_Low_Up_2
    },
    #Cheeks
    {
        'imagen': ('SHAPEKEYS_Char_Cheeks_A.jpg', 'SHAPEKEYS_Char_Cheeks_B.jpg'),
        'titulo': {
            'EN': 'Cheeks',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-2). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Cheeks
    },
    #Nose Frown
    {
        'imagen': ('SHAPEKEYS_Char_Nose_Frown_A.jpg', 'SHAPEKEYS_Char_Nose_Frown_B.jpg'),
        'titulo': {
            'EN': 'Nose Frown',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Nose Frown Shapekey.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Nose_Frown
    },
    #Nostril
    {
        'imagen': ('SHAPEKEYS_Char_Nostril_A.jpg', 'SHAPEKEYS_Char_Nostril_B.jpg', 'SHAPEKEYS_Char_Nostril_A.jpg', 'SHAPEKEYS_Char_Nostril_C.jpg'),
        'titulo': {
            'EN': 'Nostril',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Nostril Expand Shapekey. Afterwards, Shift to the Nostril Collapse Shapekey with the 'Set Joint Transform' slider and edit it.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Nostril
    },
    #Mouth Corner Base
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Corner_Base_A.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_B.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_C.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_D.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_E.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_F.jpg',
        'SHAPEKEYS_Char_Mouth_Corner_Base_G.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_H.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_I.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_J.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_K.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Base_L.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Base',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Scroll through the key Poses with the 'Set Joint Transform' slider (0-6). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Corner_Base
    },
    #Mouth Corner Out Combinations 1
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Corner_Fix_1_A.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1_B.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1_C.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1_D.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1_E.jpg',
        'SHAPEKEYS_Char_Mouth_Corner_Fix_1_F.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1_G.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_1_H.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Corrective 1',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the first level of Mouth Corner Combinations Shapekeys. Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Corner_Fix_1
    },
    #Mouth Corner Out Combinations 2
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Corner_Fix_2_A.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2_B.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2_C.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2_D.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2_E.jpg',
        'SHAPEKEYS_Char_Mouth_Corner_Fix_2_F.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2_G.jpg', 'SHAPEKEYS_Char_Mouth_Corner_Fix_2_H.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Corrective 2',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the second level of Mouth Corner Combinations Shapekeys. Scroll through the key Poses with the 'Set Joint Transform' slider (0-4). On each Pose, edit the Mesh to achieve the Final Deformaion of the Character.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Corner_Fix_2
    },
    #Mouth Shapekeys Vertex Groups
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Weight_A.jpg', 'SHAPEKEYS_Char_Mouth_Weight_B.jpg', 'SHAPEKEYS_Char_Mouth_Weight_C.jpg', 'SHAPEKEYS_Char_Mouth_Weight_D.jpg'),
        'titulo': {
            'EN': 'Mouth Vertex Groups',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Paint the Mouth Shapekeys Vertex Groups. Change the Active Vertex Group with 'Select Shapekey Vertex Group'. Paint the transition between the groups with a 0.5 value.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Weight
    },
    #U Vowel
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_U_A.jpg', 'SHAPEKEYS_Char_Mouth_U_B.jpg', 'SHAPEKEYS_Char_Mouth_U_C.jpg'),
        'titulo': {
            'EN': 'U Vowel',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the General 'U Vowel' Shapekey. When you're done, press the 'Apply Shape' Button to propagate the Shapekey to the corresponding 'U Vowel' Shapekeys.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_U
    },
    #U Thicken
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_U_Thickness_A.jpg', 'SHAPEKEYS_Char_Mouth_U_Thickness_B.jpg', 'SHAPEKEYS_Char_Mouth_U_Thickness_C.jpg'),
        'titulo': {
            'EN': 'U Thicken',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the General 'U Thicken Lips' Shapekey. When you're done, press the 'Apply Shape' Button to propagate the Shapekey to the corresponding 'U Thicken' Shapekeys.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_U_Thickness
    },
    #M
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_M_A.jpg', 'SHAPEKEYS_Char_Mouth_M_B.jpg', 'SHAPEKEYS_Char_Mouth_M_C.jpg'),
        'titulo': {
            'EN': 'M',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the General 'M' Shapekey. When you're done, press the 'Apply Shape' Button to propagate the Shapekey to the corresponding 'M' Shapekeys.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_M
    },
    #Mouth Open CLose
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Open_Close_A.jpg', 'SHAPEKEYS_Char_Mouth_Open_Close_B.jpg', 'SHAPEKEYS_Char_Mouth_Open_Close_C.jpg', 'SHAPEKEYS_Char_Mouth_Open_Close_D.jpg'),
        'titulo': {
            'EN': 'Mouth Open / Close',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mouth Open Shapekey. Afterwards, Shift to the Mouth Close Shapekey with the 'Set Joint Transform' slider and edit it.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Open_Close
    },
    #Mouth Open Out
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Open_Out_A.jpg', 'SHAPEKEYS_Char_Mouth_Open_Out_B.jpg'),
        'titulo': {
            'EN': 'Mouth Open Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mouth Open with Mouth Corner Out combination.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Open_Out
    },
    #Mouth Open In
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Open_In_A.jpg', 'SHAPEKEYS_Char_Mouth_Open_In_B.jpg'),
        'titulo': {
            'EN': 'Mouth Open In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mouth Open with Mouth Corner In combination.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Open_In
    },
    #Mouth Close Out
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Close_Out_A.jpg', 'SHAPEKEYS_Char_Mouth_Close_Out_B.jpg'),
        'titulo': {
            'EN': 'Mouth Close Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mouth Close with Mouth Corner Out combination.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Close_Out
    },
    #Mouth Close In
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Close_In_A.jpg', 'SHAPEKEYS_Char_Mouth_Close_In_B.jpg'),
        'titulo': {
            'EN': 'Mouth Close In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mouth Close with Mouth Corner In combination.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Close_In
    },
    #Mouth Frown to the Side
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Frown_Side_A.jpg', 'SHAPEKEYS_Char_Mouth_Frown_Side_B.jpg'),
        'titulo': {
            'EN': 'Mouth Frown to the Side',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the 'Mouth Frown to the Side' Shapekey.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Frown_Side
    },
    #Mouth Side Out
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Frown_Side_Out_A.jpg', 'SHAPEKEYS_Char_Mouth_Frown_Side_Out_B.jpg'),
        'titulo': {
            'EN': 'Mouth Side Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the 'Mouth Frown to the Side' with Mouth Corner Out combination.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Frown_Side_Out
    },
    #Mouth Side In
    {
        'imagen': ('SHAPEKEYS_Char_Mouth_Frown_Side_In_A.jpg', 'SHAPEKEYS_Char_Mouth_Frown_Side_In_B.jpg'),
        'titulo': {
            'EN': 'Mouth Side In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the 'Mouth Frown to the Side' with Mouth Corner In combination.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Char_Mouth_Frown_Side_In
    },
    #Shapekeys Finish
    {
        'imagen': ('SHAPEKEYS_Finish_A.jpg', 'SHAPEKEYS_Finish_B.jpg'),
        'titulo': {
            'EN': 'Finish',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Congratulations! Your character should be ready! Have a great time using it! If needed, you can edit the Bone Shapes with the Bone Shapes Tools in the Tools Tab.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': SHAPEKEYS_Finish
    },
)










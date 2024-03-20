from os.path import dirname, join
from .. actions.guide_actions_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_ACTIONS = (
    #Fingers Spread Up
    {
        'imagen': ('ACTIONS_Intro_A.jpg', 'ACTIONS_Intro_B.jpg', 'ACTIONS_Intro_C.jpg'),
        'titulo': {
            'EN': 'Introduction',
            'ES': 'Introduccion'
            },
        'texto': {
            'EN': "In this Guide you will customize all the predefined motions of the Rig. Just pose it as you see it in the example image. Poses will be automatically saved.",
            'ES': "En esta Guía personalizarás todos los movimientos predefinidos del Rig. Simplemente pósalo como lo ves en la imagen de ejemplo. Las poses se guardarán automáticamente."
            },
        'accion': ACTIONS_Intro
    },
    #Fingers Spread Up
    {
        'imagen': 'ACTIONS_Fingers_Spread_X_Up.jpg',
        'titulo': {
            'EN': 'Fingers Spread Up',
            'ES': 'Dedos separados hacia arriba'
            },
        'texto': {
            'EN': "Pose the Fingers into the Spread Up position.",
            'ES': "Posicione los dedos en la posición Separados hacia arriba."
            },
        'accion': ACTIONS_Fingers_Spread_X_Up
    },
    #Fingers Spread Down
    {
        'imagen': 'ACTIONS_Fingers_Spread_X_Down.jpg',
        'titulo': {
            'EN': 'Fingers Spread Down',
            'ES': 'Dedos separados'
            },
        'texto': {
            'EN': "Pose the Fingers into the Spread Down position.",
            'ES': "Posicione los dedos en la posición extendida hacia abajo."
            },
        'accion': ACTIONS_Fingers_Spread_X_Down
    },
    #Fingers Spread Out
    {
        'imagen': 'ACTIONS_Fingers_Spread_Z_Out.jpg',
        'titulo': {
            'EN': 'Fingers Spread Out',
            'ES': 'Dedos abiertos'
            },
        'texto': {
            'EN': "Pose the Fingers into the Spread Out position.",
            'ES': "Coloca los dedos en posición extendida."
            },
        'accion': ACTIONS_Fingers_Spread_Z_Out
    },
    #Fingers Spread In
    {
        'imagen': 'ACTIONS_Fingers_Spread_Z_In.jpg',
        'titulo': {
            'EN': 'Fingers Spread In',
            'ES': 'Dedos juntos'
            },
        'texto': {
            'EN': "Pose the fingers one next to the other.",
            'ES': "Coloca los dedos uno junto al otro."
            },
        'accion': ACTIONS_Fingers_Spread_Z_In
    },
    #Fingers Curl In
    {
        'imagen': 'ACTIONS_Fingers_Curl_In.jpg',
        'titulo': {
            'EN': 'Fingers Curl In',
            'ES': 'Dedos curvados hacia dentro'
            },
        'texto': {
            'EN': "Adjust the curling pose of the Fingers so that the finger tips touch the palm.",
            'ES': "Ajuste la postura curvada de los dedos para que las puntas de los dedos toquen la palma."
            },
        'accion': ACTIONS_Fingers_Curl_In
    },
    #Fingers Curl Out
    {
        'imagen': 'ACTIONS_Fingers_Curl_Out.jpg',
        'titulo': {
            'EN': 'Fingers Curl Out',
            'ES': 'Dedos curvados hacia fuera'
            },
        'texto': {
            'EN': "Adjust the outwards curling pose of the Fingers.",
            'ES': "Ajustar la postura de curvatura hacia fuera de los Dedos."
            },
        'accion': ACTIONS_Fingers_Curl_Out
    },
    #Hand Close
    {
        'imagen': 'ACTIONS_Hand_Close.jpg',
        'titulo': {
            'EN': 'Hand Close',
            'ES': 'Mano Cerrada'
            },
        'texto': {
            'EN': "Adjust the 'Closed Fist' position of the Hand. Scale the main Finger controllers to curl them. Move and Rotate the MSTR controllers to place the Fingers correctly.",
            'ES': "Ajuste la posición 'Puño cerrado' de la Mano. Escala los controladores principales de los Dedos para doblarlos. Mueve y rota los controladores MSTR para colocar los Dedos correctamente."
            },
        'accion': ACTIONS_Hand_Close
    },
    #Hand Open
    {
        'imagen': 'ACTIONS_Hand_Open.jpg',
        'titulo': {
            'EN': 'Hand Open',
            'ES': 'Mano abierta'
            },
        'texto': {
            'EN': "Adjust the 'Wide Opened' position of the Hand. Scale the main Fingers controllers to curl them. Move and Rotate the MSTR controllers to place the Fingers correctly.",
            'ES': "Ajusta la posición 'Muy abierta' de la Mano. Escala los controladores principales de los Dedos para doblarlos. Mueve y rota los controladores MSTR para colocar los Dedos correctamente."
            },
        'accion': ACTIONS_Hand_Open
    },
    #Breathe In
    {
        'imagen': ('ACTIONS_Breathing_in_A.jpg', 'ACTIONS_Breathing_in_B.jpg'),
        'titulo': {
            'EN': 'Breathe In',
            'ES': 'Inspira'
            },
        'texto': {
            'EN': "Pose the Spine and Neck into a Breathing In position. Using the 'spine_ctrl_curve' bone is recommended for this. Rib Cage Expansion, will be done with a Shapekey later. Switch between Pose and Rest Position to visualize the motion.",
            'ES': "Coloca la columna vertebral y el cuello en posición de Inspiración. Se recomienda usar el hueso 'spine_ctrl_curve' para esto. Expansión de la Caja Torácica, se hará con una Shapekey más tarde. Cambie entre Pose y Posición de Reposo para visualizar el movimiento."
            },
        'accion': ACTIONS_Breathing_in
    },
    #Breathe Out
    {
        'imagen': ('ACTIONS_Breathing_Out_A.jpg', 'ACTIONS_Breathing_Out_B.jpg'),
        'titulo': {
            'EN': 'Breathe Out',
            'ES': 'Espira'
            },
        'texto': {
            'EN': "Pose the Spine and Neck into a Breathing Out position. Using the 'spine_ctrl_curve' bone is recommended for this. Rib Cage Expansion, will be done with a Shapekey later. Switch between Pose and Rest Position to visualize the motion.",
            'ES': "Posicione la Espina Dorsal y el Cuello en una posición de Espiración. Se recomienda usar el hueso 'spine_ctrl_curve' para esto. Expansión de la Caja Torácica, se hará con una Shapekey más tarde. Cambie entre Pose y Posición de Reposo para visualizar el movimiento."
            },
        'accion': ACTIONS_Breathing_Out
    },
    #Upper Eyelids Upwards Range
    {
        'imagen': 'ACTIONS_Eyelids_Up_Up_Range.jpg',
        'titulo': {
            'EN': 'Upper Eyelid Upwards Range',
            'ES': 'Rango Párpado superior arriba'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Upper Eyelid Controller. Do this with the Range Slider.",
            'ES': "Defina el Rango Máximo de Movimiento Hacia Arriba del Controlador del Párpado Superior. Hágalo con el Deslizador de Rango."
            },
        'accion': ACTIONS_Eyelids_Up_Up_Range
    },
    #Upper Eyelids Up
    {
        'imagen': ('ACTIONS_Eyelids_Up_Up_A.jpg', 'ACTIONS_Eyelids_Up_Up_B.jpg'),
        'titulo': {
            'EN': 'Upper Eyelids Up',
            'ES': 'Párpados superiores hacia arriba'
            },
        'texto': {
            'EN': "Pose the Upper Eyelids into a fully opened position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': "Posicione los párpados superiores en una posición totalmente abierta. Primero intente rotar los controladores 'rot', si necesita mas ajustes use los controladores Cube. Usa la opción 'Show Deformation Bones' para ver que están haciendo las articulaciones."
            },
        'accion': ACTIONS_Eyelids_Up_Up
    },
    #Upper Eyelids Downwards Range
    {
        'imagen': 'ACTIONS_Eyelids_Up_Down_Range.jpg',
        'titulo': {
            'EN': 'Upper Eyelids Down Range',
            'ES': 'Rango Párpado superior abajo'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Upper Eyelid Controller. Do this with the Range Slider.",
            'ES': "Defina el Rango Máximo de Movimiento Hacia abajo del Controlador del Párpado Superior. Hágalo con el Deslizador de Rango."
            },
        'accion': ACTIONS_Eyelids_Up_Down_Range
    },
    #Upper Eyelids Down to Middle
    {
        'imagen': 'ACTIONS_Eyelids_Up_Down_1.jpg',
        'titulo': {
            'EN': 'Eyelids Down to Middle',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Upper Eyelids so that the Eye is Half Closed. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Eyelids might clip through the Eyes, this will be fixed with a Shapekey in a later Step.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Up_Down_1
    },
    #Upper Eyelids Down to Bottom
    {
        'imagen': 'ACTIONS_Eyelids_Up_Down_2.jpg',
        'titulo': {
            'EN': 'Eyelids Down to Bottom',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Upper Eyelids into a Fully Closed position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Eyelids might clip through the Eyes, this will be fixed with a Shapekey in a later Step.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Up_Down_2
    },
    #Lower Eyelids Downwards Range
    {
        'imagen': 'ACTIONS_Eyelids_Low_Down_Range.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Down Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Lower Eyelid Controller. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Low_Down_Range
    },
    #Lower Eyelids Down
    {
        'imagen': ('ACTIONS_Eyelids_Low_Down_A.jpg', 'ACTIONS_Eyelids_Low_Down_B.jpg'),
        'titulo': {
            'EN': 'Lower Eyelids Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Lower Eyelids into a fully opened position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Low_Down
    },
    #Lower Eyelids Upwards Range
    {
        'imagen': 'ACTIONS_Eyelids_Low_Up_Range.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Up Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Lower Eyelid Controller. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Low_Up_Range
    },
    #Lower Eyelids Up to Middle
    {
        'imagen': 'ACTIONS_Eyelids_Low_Up_1.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Up to Middle',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Lower Eyelids so that the Eye is Half Closed. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Eyelids might clip through the Eyes, this will be fixed with a Shapekey in a later Step.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Low_Up_1
    },
    #Lower Eyelids Up to Top
    {
        'imagen': 'ACTIONS_Eyelids_Low_Up_2.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Up to Top',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Lower Eyelids into a Fully Closed position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Eyelids might clip through the Eyes, this will be fixed with a Shapekey in a later Step.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Low_Up_2
    },
    #Eyelids Out
    {
        'imagen': ('ACTIONS_Eyelids_Out_A.jpg', 'ACTIONS_Eyelids_Out_B.jpg'),
        'titulo': {
            'EN': 'Eyelids Outwards',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Eyelids so that they react to the Eye looking Outwards.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_Out
    },
    #Eyelids In
    {
        'imagen': ('ACTIONS_Eyelids_In_A.jpg', 'ACTIONS_Eyelids_In_B.jpg'),
        'titulo': {
            'EN': 'Eyelids Inwards',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Eyelids so that they react to the Eye looking Inwards.",
            'ES': ""
            },
        'accion': ACTIONS_Eyelids_In
    },
    #Cheek Upwards Range
    {
        'imagen': 'ACTIONS_Cheek_Up_Range.jpg',
        'titulo': {
            'EN': 'Cheek Upwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Cheek Controller. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Cheek_Up_Range
    },
    #Cheek Up
    {
        'imagen': ('ACTIONS_Cheek_Up_A.jpg', 'ACTIONS_Cheek_Up_B.jpg', 'ACTIONS_Cheek_Up_C.jpg'),
        'titulo': {
            'EN': 'Cheek Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Cheek Upwards position. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Fine tuning of Deformation will be done in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Cheek_Up
    },
    #Cheek Frown
    {
        'imagen': ('ACTIONS_Cheek_Frown_A.jpg', 'ACTIONS_Cheek_Frown_B.jpg'),
        'titulo': {
            'EN': 'Cheek Frown',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Controllers as if the Character was frowning the Eye.",
            'ES': ""
            },
        'accion': ACTIONS_Cheek_Frown
    },
    #Cheek Downwards Range
    {
        'imagen': 'ACTIONS_Cheek_Down_Range.jpg',
        'titulo': {
            'EN': 'Cheek Downwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Cheek Controller. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Cheek_Down_Range
    },
    #Cheek Down
    {
        'imagen': ('ACTIONS_Cheek_Down_A.jpg', 'ACTIONS_Cheek_Down_B.jpg', 'ACTIONS_Cheek_Down_C.jpg'),
        'titulo': {
            'EN': 'Cheek Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Cheek Downwards position. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Fine tuning of Mesh Deformation will be done in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Cheek_Down
    },
    #Nose Frown Range
    {
        'imagen': 'ACTIONS_Nose_Frown_Range.jpg',
        'titulo': {
            'EN': 'Nose Frown Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Nose Frown Controller. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Nose_Frown_Range
    },
    #Nose Frown
    {
        'imagen': ('ACTIONS_Nose_Frown_A.jpg', 'ACTIONS_Nose_Frown_B.jpg', 'ACTIONS_Nose_Frown_C.jpg'),
        'titulo': {
            'EN': 'Nose Frown',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Controllers into a Nose Frowning  position. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Fine tuning of Deformation will be done in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Nose_Frown
    },
        #Nose Frown Max
    {
        'imagen': ('ACTIONS_Nose_Frown_Max_A.jpg', 'ACTIONS_Nose_Frown_Max_B.jpg'),
        'titulo': {
            'EN': 'Nose Frown Max',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Make Nose Frowning a bit more extreme, as if the character was furious. You can involve the Eyelids and Eyebrows in this Pose.",
            'ES': ""
            },
        'accion': ACTIONS_Nose_Frown_Max
    },
    #Jaw Down Range
    {
        'imagen': 'ACTIONS_Jaw_Down_Range.jpg',
        'titulo': {
            'EN': 'Jaw Downwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Downwards Rotation of the Jaw. Do this with the Range Slider",
            'ES': ""
            },
        'accion': ACTIONS_Jaw_Down_Range
    },
        #Jaw Down
    {
        'imagen': ('ACTIONS_Jaw_Down_A.jpg', 'ACTIONS_Jaw_Down_B.jpg'),
        'titulo': {
            'EN': 'Jaw Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Opened Mouth Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Jaw_Down
    },
    #Jaw Up Range
    {
        'imagen': 'ACTIONS_Jaw_Up_Range.jpg',
        'titulo': {
            'EN': 'Jaw Upwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Upwards Rotation of the Jaw. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Jaw_Up_Range
    },
        #Jaw Up
    {
        'imagen': ('ACTIONS_Jaw_Up_A.jpg', 'ACTIONS_Jaw_Up_B.jpg'),
        'titulo': {
            'EN': 'Jaw Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the 'Extreme Closed Mouth' Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Jaw_Up
    },
    #Mouth Corner Out Range
    {
        'imagen': 'ACTIONS_Mouth_Corner_Out_Range.jpg',
        'titulo': {
            'EN': 'Mouth Corner Out Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Outwards motion of the Mouth Corner. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Out_Range
    },
        #Mouth Corner Out
    {
        'imagen': ('ACTIONS_Mouth_Corner_Out_A.jpg', 'ACTIONS_Mouth_Corner_Out_B.jpg', 'ACTIONS_Mouth_Corner_Out_C.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Outwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Out
    },
    #Mouth Corner Up Range
    {
        'imagen': 'ACTIONS_Mouth_Corner_Up_Range.jpg',
        'titulo': {
            'EN': 'Mouth Corner Up Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards motion of the Mouth Corner. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Up_Range
    },
        #Mouth Corner Up
    {
        'imagen': ('ACTIONS_Mouth_Corner_Up_A.jpg', 'ACTIONS_Mouth_Corner_Up_B.jpg', 'ACTIONS_Mouth_Corner_Up_C.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Upwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Up
    },
    #Mouth Corner Down Range
    {
        'imagen': 'ACTIONS_Mouth_Corner_Down_Range.jpg',
        'titulo': {
            'EN': 'Mouth Corner Down Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards motion of the Mouth Corner. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Down_Range
    },
        #Mouth Corner Down
    {
        'imagen': ('ACTIONS_Mouth_Corner_Down_A.jpg', 'ACTIONS_Mouth_Corner_Down_B.jpg', 'ACTIONS_Mouth_Corner_Down_C.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Downwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Down
    },
    #Mouth Corner Back Range
    {
        'imagen': 'ACTIONS_Mouth_Corner_Back_Range.jpg',
        'titulo': {
            'EN': 'Mouth Corner Back Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Backwards motion of the Mouth Corner. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Back_Range
    },
        #Mouth Corner Back
    {
        'imagen': ('ACTIONS_Mouth_Corner_Back_A.jpg', 'ACTIONS_Mouth_Corner_Back_B.jpg', 'ACTIONS_Mouth_Corner_Back_C.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Back',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Backwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Back
    },
    #Mouth Corner Forwards Range
    {
        'imagen': 'ACTIONS_Mouth_Corner_Forw_Range.jpg',
        'titulo': {
            'EN': 'Mouth Corner Forwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Forwards motion of the Mouth Corner. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Forw_Range
    },
        #Mouth Corner Forwards
    {
        'imagen': ('ACTIONS_Mouth_Corner_Forw_A.jpg', 'ACTIONS_Mouth_Corner_Forw_B.jpg'),
        'titulo': {
            'EN': 'Mouth Corner Forwards',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Forwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Forw
    },
    #Mouth Corner In Range
    {
        'imagen': 'ACTIONS_Mouth_Corner_In_Range.jpg',
        'titulo': {
            'EN': 'Mouth Corner In Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Inwards motion of the Mouth Corner. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_In_Range
    },
        #Mouth Corner In
    {
        'imagen': ('ACTIONS_Mouth_Corner_In_A.jpg', 'ACTIONS_Mouth_Corner_In_B.jpg', 'ACTIONS_Mouth_Corner_In_C.jpg'),
        'titulo': {
            'EN': 'Mouth Corner In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Inwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_In
    },
        #Mouth Corner In Zipper
    {
        'imagen': ('ACTIONS_Mouth_Corner_In_Zipper_A.jpg', 'ACTIONS_Mouth_Corner_In_Zipper_B.jpg'),
        'titulo': {
            'EN': 'Mouth Corner In Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper controllers for when the mouth is narrowed inwards.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_In_Zipper
    },
    #Mouth Corner Up Out Corrective
    {
        'imagen': ('ACTIONS_Mouth_Corner_Up_Out_Corrective_A.jpg', 'ACTIONS_Mouth_Corner_Up_Out_Corrective_B.jpg', 'ACTIONS_Mouth_Corner_Up_Out_Corrective_C.jpg'),
        'titulo': {
            'EN': 'Corner Up Out Corrective',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Up and Out combination Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Up_Out_Corrective
    },
        #Mouth Corner Down Out Corrective
    {
        'imagen': ('ACTIONS_Mouth_Corner_Down_Out_Corrective_A.jpg', 'ACTIONS_Mouth_Corner_Down_Out_Corrective_B.jpg', 'ACTIONS_Mouth_Corner_Down_Out_Corrective_C.jpg'),
        'titulo': {
            'EN': 'Corner Down Out Corrective',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Up and Down combination Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_Mouth_Corner_Down_Out_Corrective
    },
    #U_O_M Range
    {
        'imagen': 'ACTIONS_U_O_M_Range.jpg',
        'titulo': {
            'EN': 'U_O_M Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of motion of the Upper and Lower Mouth Controllers. This controllers trigger the 'U Vowel' and 'M' poses. Do this with the Range Slider.",
            'ES': ""
            },
        'accion': ACTIONS_U_O_M_Range
    },
        #U
    {
        'imagen': ('ACTIONS_U_A.jpg', 'ACTIONS_U_B.jpg', 'ACTIONS_U_C.jpg', 'ACTIONS_U_D.jpg'),
        'titulo': {
            'EN': 'Subtle U Vowel',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use 'lip_up_ctrl' and 'lip_low_ctrl' to pull the lips forwards. The idea is to achieve a 'Subtle U Vowel' Pose. Use 'mouth_corner_mstr_L' to move the Mouth Corners slightly forwards.",
            'ES': ""
            },
        'accion': ACTIONS_U
    },
    #O
    {
        'imagen': ('ACTIONS_O_A.jpg', 'ACTIONS_O_B.jpg', 'ACTIONS_O_C.jpg', 'ACTIONS_O_D.jpg', 'ACTIONS_O_E.jpg'),
        'titulo': {
            'EN': 'Opened O Vowel',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use 'lip_up_ctrl' and 'lip_low_ctrl' to pull the lips forwards a bit further than in the previous step. The idea is to achieve an opened 'O Vowel' Pose. Use 'mouth_corner_mstr_L' to move the Mouth Corners forwards.",
            'ES': ""
            },
        'accion': ACTIONS_O
    },
    #U Zipper
    {
        'imagen': 'ACTIONS_U_Zipper.jpg',
        'titulo': {
            'EN': 'U Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper controllers for the 'Subtle U Vowel'.",
            'ES': ""
            },
        'accion': ACTIONS_U_Zipper
    },
    #O Zipper
    {
        'imagen': 'ACTIONS_O_Zipper.jpg',
        'titulo': {
            'EN': 'O Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper controllers for the 'O Vowel'.",
            'ES': ""
            },
        'accion': ACTIONS_O_Zipper
    },
        #U Narrow Corrective
    {
        'imagen': ('ACTIONS_U_Narrow_Corrective_A.jpg', 'ACTIONS_U_Narrow_Corrective_B.jpg', 'ACTIONS_U_Narrow_Corrective_C.jpg'),
        'titulo': {
            'EN': 'U Narrow Corrective',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the 'MSTR' controllers to conform a 'Closed U Vowel'. Use the rest of the controllers to fine tune the pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints.",
            'ES': ""
            },
        'accion': ACTIONS_U_Narrow_Corrective
    },
        #U Narrow Corrective Zipper
    {
        'imagen': 'ACTIONS_U_Narrow_Corrective_Zipper.jpg',
        'titulo': {
            'EN': 'U Narrow Corrective Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper controllers for the 'Closed U Vowel'.",
            'ES': ""
            },
        'accion': ACTIONS_U_Narrow_Corrective_Zipper
    },
    #Thicker Lips
    {
        'imagen': ('ACTIONS_U_Thicker_Lips_A.jpg', 'ACTIONS_U_Thicker_Lips_B.jpg'),
        'titulo': {
            'EN': 'Thicker Lips',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use the 'lip_line_ctrl' bones to make the lips thicker, as in a 'Whistling' Pose. Use the rest of the controllers to achieve this compressed pose on the Lips",
            'ES': ""
            },
        'accion': ACTIONS_U_Thicker_Lips
    },
        #Thinner Lips
    {
        'imagen': ('ACTIONS_U_Thinner_Lips_A.jpg', 'ACTIONS_U_Thinner_Lips_B.jpg'),
        'titulo': {
            'EN': 'Thinner Lips',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use 'lip_up_ctrl' and 'lip_low_ctrl' to open the lips. Use the 'lip_line_ctrl' bones and the rest of the controllers to make the lips thinner.",
            'ES': ""
            },
        'accion': ACTIONS_U_Thinner_Lips
    },
        #M
    {
        'imagen': ('ACTIONS_M_A.jpg', 'ACTIONS_M_B.jpg', 'ACTIONS_M_C.jpg', 'ACTIONS_M_D.jpg'),
        'titulo': {
            'EN': 'M',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Move and Rotate 'lip_up_ctrl_collision_override' and 'lip_low_ctrl_collision_override' to achieve an 'M' Pose. Use the rest of the controllers to seal and fine tune the Pose. Deformation will be enhanced in the Shapekeys Steps.",
            'ES': ""
            },
        'accion': ACTIONS_M
    },
    #Mouth Frown Range
    {
        'imagen': 'ACTIONS_Mouth_Frown_Range.jpg',
        'titulo': {
            'EN': 'Mouth Frown Range',
            'ES': 'Rango de fruncimiento de la boca'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Mouth Frown Controller. Do this with the Range Slider",
            'ES': "Defina el Rango Máximo de Movimiento Hacia Abajo del Controlador Fruncir Boca. Hágalo con el Deslizador de Rango"
            },
        'accion': ACTIONS_Mouth_Frown_Range
    },
    #Mouth Frown
    {
        'imagen': 'ACTIONS_Mouth_Frown.jpg',
        'titulo': {
            'EN': 'Mouth Frown',
            'ES': 'Fruncir la boca'
            },
        'texto': {
            'EN': "Use the controllers to achieve a 'Frowning Mouth' Pose.",
            'ES': "Utiliza los controladores para conseguir una pose de 'Boca Fruncida'."
            },
        'accion': ACTIONS_Mouth_Frown
    },
        #Chin Frown Range
    {
        'imagen': 'ACTIONS_Chin_Frown_Range.jpg',
        'titulo': {
            'EN': 'Chin Frown Range',
            'ES': 'Rango de fruncimiento de la barbilla'
            },
        'texto': {
            'EN': "Define the Maximum Range of Motion of the Chin Frown Controller. Do this with the Range Slider.",
            'ES': "Defina el Rango Máximo de Movimiento del Controlador Fruncir Mentón. Hágalo con el Deslizador de Rango."
            },
        'accion': ACTIONS_Chin_Frown_Range
    },
        #Chin Frown Up
    {
        'imagen': ('ACTIONS_Chin_Frown_Up_A.jpg', 'ACTIONS_Chin_Frown_Up_B.jpg'),
        'titulo': {
            'EN': 'Chin Frown Up',
            'ES': 'Barbilla fruncida'
            },
        'texto': {
            'EN': "Use the controllers to achieve an 'Upwards Frowning Chin' Pose. This should also compress the Lower Lips.",
            'ES': "Utiliza los controladores para conseguir una pose de 'barbilla fruncida hacia arriba'. Esto también debería comprimir los labios inferiores."
            },
        'accion': ACTIONS_Chin_Frown_Up
    },
        #Chin Frown Down
    {
        'imagen': ('ACTIONS_Chin_Frown_Down_A.jpg', 'ACTIONS_Chin_Frown_Down_B.jpg'),
        'titulo': {
            'EN': 'Chin Frown Down',
            'ES': 'Barbilla fruncida'
            },
        'texto': {
            'EN': "Use the controllers to achieve an 'Downwards Frowning Chin' Pose.",
            'ES': "Utiliza los controladores para conseguir una pose de 'barbilla fruncida hacia abajo'."
            },
        'accion': ACTIONS_Chin_Frown_Down
    },
        #Actions Finish
    {
        'imagen': 'ACTIONS_Finish.jpg',
        'titulo': {
            'EN': 'Actions Finish',
            'ES': 'Acciones Acabado'
            },
        'texto': {
            'EN': "Excellent! Move to the Advanced Settings Guide!",
            'ES': "¡Excelente! ¡Pasa a la Guía de Ajustes Avanzados!"
            },
        'accion': ACTIONS_Finish
    }
)





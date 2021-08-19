from os.path import dirname, join
from .. actions.guide_actions_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_ACTIONS = (
    #Fingers Spread Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers Spread Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the fingers into the Spread Up position.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_X_Up
    },
    #Fingers Spread Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers Spread Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the fingers into the Spread Down position",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_X_Down
    },
    #Fingers Spread Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers Spread Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the fingers into the Spread Out position.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_Z_Out
    },
    #Fingers Spread In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers Spread In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the fingers one next to the other.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_Z_In
    },
    #Fingers Curl In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers Curl In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Adjust the curling pose of the fingers so that the finger tips touch the palm",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Curl_In
    },
    #Fingers Curl Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers Curl Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Adjust the outwards curling pose of the fingers",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Curl_Out
    },
    #Hand Close
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Hand Close',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Adjust the closed fist position of the hand. Scale the main finger controllers to curl them. Move and Rotate the MSTR controllers to place the fingers correctly.",
            'ES': "Adjust the closed fist position of the hand. Scale the main finger controllers to curl them. Move and Rotate the MSTR controllers to place the fingers correctly."
            },
        'accion': ACTIONS_Hand_Close
    },
    #Hand Open
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Hand Open',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Adjust the 'wide opened' position of the hand. Scale the main fingers controllers to curl them. Move and Rotate the MSTR controllers to place the fingers correctly.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Hand_Open
    },
    #Breathe In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Breathe In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Spine and Neck into a Breathing In position. Using the 'spine_ctrl_curve' bone is recommended for this. Don't worry about rib cage Expansion, this will be done with a Shapekey in a later Step. You can Switch between Pose and Rest Position to visualize the resulting motion.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Breathing_in
    },
    #Breathe Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Breathe Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Spine and Neck into a Breathing Out position. Using the 'spine_ctrl_curve' bone is recommended for this. Don't worry about rib cage Compression, this will be done with a Shapekey in a later Step. You can Switch between Pose and Rest Position to visualize the resulting motion.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Breathing_Out
    },
    #Upper Eyelids Upwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Upper Eyelids Upwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Upper Eyelid Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Up_Range
    },
    #Upper Eyelids Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Upper Eyelids Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Upper Eyelids into a fully opened position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Up
    },
    #Upper Eyelids Downwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Upper Eyelids Downwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Upper Eyelid Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Down_Range
    },
    #Upper Eyelids Down to Middle
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Upper Eyelids Down to Middle',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Upper Eyelids so that the Eye is half closed. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Don't worry about the Eyelids clipping through the Eyes, this will be fixed with a Shapekey in a later Step. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Down_1
    },
    #Upper Eyelids Down to Bottom
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Upper Eyelids Down to Bottom',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Upper Eyelids into a fully closed position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Don't worry about the Eyelids clipping through the Eyes, this will be fixed with a Shapekey in a later Step. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Down_2
    },
    #Lower Eyelids Downwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Downwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Lower Eyelid Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Down_Range
    },
    #Lower Eyelids Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Lower Eyelids into a fully opened position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Down
    },
    #Lower Eyelids Upwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Upwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Lower Eyelid Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Up_Range
    },
    #Lower Eyelids Up to Middle
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Up to Middle',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Lower Eyelids so that the Eye is half closed. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Don't worry about the Eyelids clipping through the Eyes, this will be fixed with a Shapekey in a later Step. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Up_1
    },
    #Lower Eyelids Up to Top
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Lower Eyelids Up to Top',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Lower Eyelids into a fully closed position. First try rotating the 'rot' controllers, if you need further tweaking use the Cube controllers. Don't worry about the Eyelids clipping through the Eyes, this will be fixed with a Shapekey in a later Step. Use the 'Show Deformation Bones' option to see what the actual Joints are doing.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Up_2
    },
    #Eyelids Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Eyelids Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Eyelids so that they react to the Eye looking Out.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Out
    },
    #Eyelids In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Eyelids In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Eyelids so that they react to the Eye looking In.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_In
    },
    #Cheek Upwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Cheek Upwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Cheek Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Up_Range
    },
    #Cheek Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Cheek Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Cheek Controllers into the Cheek Upwards position. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Fine tuning of Mesh Deformation will be done in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Up
    },
    #Cheek Frown
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Cheek Frown',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Controllers as if the Character was frowning the Eye.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Frown
    },
    #Cheek Downwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Cheek Downwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Cheek Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Down_Range
    },
    #Cheek Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Cheek Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Cheek Controllers into the Cheek Downwards position. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Fine tuning of Mesh Deformation will be done in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Down
    },
    #Nose Frown Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Nose Frown Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards Motion of the Nose Frown Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Nose_Frown_Range
    },
    #Nose Frown
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Nose Frown',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the Controllers into a Nose Frowning  position. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Fine tuning of Mesh Deformation will be done in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Nose_Frown
    },
        #Nose Frown Max
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Nose Frown Max',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Make Nose Frowning a bit more extreme, as if the character was furious. You can involve the Eyelids and Eyebrows in this pose.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Nose_Frown_Max
    },
    #Jaw Down Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Jaw Down Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Downwards Rotation of the Jaw. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Jaw_Down_Range
    },
        #Jaw Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Jaw Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Opened Mouth Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Jaw_Down
    },
    #Jaw Up Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Jaw Up Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Upwards Rotation of the Jaw. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Jaw_Up_Range
    },
        #Jaw Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Jaw Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Closed Mouth Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Jaw_Up
    },
    #Mouth Corner Out Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Out Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Outwards motion of the Mouth Corner. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Out_Range
    },
        #Mouth Corner Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Out',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Outwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Out
    },
    #Mouth Corner Up Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Up Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Upwards motion of the Mouth Corner. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Up_Range
    },
        #Mouth Corner Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Upwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Up
    },
    #Mouth Corner Down Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Down Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards motion of the Mouth Corner. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Down_Range
    },
        #Mouth Corner Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Downwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Down
    },
    #Mouth Corner Back Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Back Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Backwards motion of the Mouth Corner. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Back_Range
    },
        #Mouth Corner Back
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Back',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Backwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Back
    },
    #Mouth Corner Forwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Forwards Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Forwards motion of the Mouth Corner. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Forw_Range
    },
        #Mouth Corner Forwards
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Forwards',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Forwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Forw
    },
    #Mouth Corner In Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner In Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Inwards motion of the Mouth Corner. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_In_Range
    },
        #Mouth Corner In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner In',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Inwards Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_In
    },
        #Mouth Corner In Zipper
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner In Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper Joints for when the mouth is narrowed inwards.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_In_Zipper
    },
    #Mouth Corner Up Out Corrective
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Up Out Corrective',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Up and Out combination Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Up_Out_Corrective
    },
        #Mouth Corner Down Out Corrective
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Corner Down Out Corrective',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Mouth Corner Up and Down combination Pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Corner_Down_Out_Corrective
    },
    #U_O_M Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'U_O_M Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of motion of the Upper and Lower Mouth Controllers. This motion triggers the 'U Vowel' and 'M' poses. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U_O_M_Range
    },
        #U
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'U',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use 'lip_up_ctrl' and 'lip_low_ctrl' to pull the lips out. The idea is to achieve a 'Subtle U Vowel' or 'Whistling' pose. Use 'mouth_corner_mstr_L' to move the mouth corner slightly forwards.  Use the rest of the controllers to fine tune the pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps. ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U
    },
    #O
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'O',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use 'lip_up_ctrl' and 'lip_low_ctrl' to pull the lips out a bit further. The idea is to achieve a 'O Vowel' pose. Use 'mouth_corner_mstr_L' to move the mouth corner forwards. Use the rest of the controllers to fine tune the pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps. ",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_O
    },
    #U Zipper
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'U Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper Joints for the 'Subtle U Vowel'.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U_Zipper
    },
    #O Zipper
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'O Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper Joints for the 'O Vowel'.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_O_Zipper
    },
        #U Narrow Corrective
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'U Narrow Corrective',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Pose the 'MSTR' controllers to conform a 'Strong U Vowel'. Use the rest of the controllers to fine tune the pose. Use the 'Show Deformation Bones' option and focus on the position of the Joints. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U_Narrow_Corrective
    },
        #U Narrow Corrective Zipper
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'U Narrow Corrective Zipper',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Fine tune the Lips Zipper Joints for the 'Strong U Vowel'.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U_Narrow_Corrective_Zipper
    },
    #Thicker Lips
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Thicker Lips',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use the 'lip_low_line_ctrl' bones to make the lips thicker. Use the rest of the controllers to achieve this compressed pose on the Lips",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U_Thicker_Lips
    },
        #Thinner Lips
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Thinner Lips',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use 'lip_up_ctrl' and 'lip_low_ctrl' to open the lips. Use the 'lip_low_line_ctrl' bones and the rest of the controllers to make the lips thinner.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_U_Thinner_Lips
    },
        #M
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'M',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Move and Rotate 'lip_up_ctrl_collision_override' and 'lip_low_ctrl_collision_override' to achieve an 'M' pose. Use the rest of the controllers to seal and fine tune the pose. Mesh Deformation will be enhanced in the Shapekeys Steps.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_M
    },
    #Mouth Frown Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Frown Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Downwards Motion of the Mouth Frown Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Frown_Range
    },
    #Mouth Frown
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth Frown',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use the controllers to achieve a Frowning Mouth Corner pose",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Mouth_Frown
    },
        #Chin Frown Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Chin Frown Range',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the Maximum Range of Motion of the Chin Frown Controller. Do this with the Range Slider",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Chin_Frown_Range
    },
        #Chin Frown Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Chin Frown Up',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use the controllers to achieve an Upwards Frowning Chin pose. This should also compress the Lower Lips",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Chin_Frown_Up
    },
        #Chin Frown Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Chin Frown Down',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Use the controllers to achieve an Downwards Frowning Chin pose.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Chin_Frown_Down
    },
)





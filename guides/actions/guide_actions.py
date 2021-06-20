from os.path import dirname, join
from .. actions.guide_actions_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_ACTIONS = (
    #Fingers Spread Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Corner',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Corner",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_X_Up
    },
    #Fingers Spread Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_X_Down
    },
    #Fingers Spread Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Corner',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Corner",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_Z_Out
    },
    #Fingers Spread In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Spread_Z_In
    },
    #Fingers Curl In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Corner',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Corner",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Curl_In
    },
    #Fingers Curl In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Fingers_Curl_Out
    },
    #Hand Close
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Corner',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Corner",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Hand_Close
    },
    #Hand Open
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Hand_Open
    },
    #Breathe In
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Corner',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Corner",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Breathing_in
    },
    #Breathe Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Breathing_Out
    },
    #Upper Eyelids Upwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Up_Range
    },
    #Upper Eyelids Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Up
    },
    #Upper Eyelids Downwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Down_Range
    },
    #Upper Eyelids Down to Middle
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Down_1
    },
    #Upper Eyelids Down to Bottom
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Up_Down_2
    },
    #Lower Eyelids Downwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Down_Range
    },
    #Lower Eyelids Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Down
    },
    #Lower Eyelids Upwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Up_Range
    },
    #Lower Eyelids Up to Middle
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Up_1
    },
    #Lower Eyelids Up to Top
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Low_Up_2
    },
    #Eyelids Out
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Eyelids_Out
    },
    #Cheek Upwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Up_Range
    },
    #Cheek Up
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Up
    },
    #Cheek Downwards Range
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Down_Range
    },
    #Cheek Down
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Down
    },
    #Cheek Frown
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': ACTIONS_Cheek_Frown
    },
)



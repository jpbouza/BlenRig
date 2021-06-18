from os.path import dirname, join
from .. actions.guide_actions_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_ACTIONS = (
    #Define Character Body Objects
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
    #Edit the Mesh Deform Cage
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
    }
)



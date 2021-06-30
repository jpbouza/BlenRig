from os.path import dirname, join
from .. weights.guide_weights_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_WEIGHTS = (
    #Define Character Body Objects
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Define Character Body Objects',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select all the objects that conform the character's body and press the Set Body Objects button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Ankle
    },
)



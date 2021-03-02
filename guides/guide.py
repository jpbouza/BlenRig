from os.path import dirname, join
from . guide_actions import *

images_dir = join(dirname(__file__), 'images')

languages = (
    # ID # Name # Description
    ('EN', 'English', ""),
    ('ES', 'Spanish', "")
)

diccionario = {
    'Step' : {
        'EN': 'Step',
        'ES': 'Paso'
    },
    'Next' : {
        'EN': 'Next',
        'ES': '▶'
    },
    'Prev' : {
        'EN': 'Prev',
        'ES': '◀'
    }
}

GUIDE_STEPS = (
    # 1
    {
        'imagen': 'paso_1.png',
        'titulo': {
            'EN': 'Step 1',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': 'Place “master_torso” at the height of hips.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Master_Torso
    },
    # 2
    {
        'imagen': 'paso_2.png',
        'titulo': {
            'EN': 'Step 2',
            'ES': 'Paso 2'
            },
        'texto': {
            'EN': 'Align hips, torso, neck and head.',
            'ES': 'Alinea la cadera, torso, cuello y cabeza.'
            },
        'accion': Reprop_Spine
    },
    # 3 [A-B]
    {
        'imagen': ('paso_3_A.png', 'paso_3_B.png'),
        'titulo': {
            'EN': 'Step 3',
            'ES': 'Paso 3'
            },
        'texto': {
            'EN': 'Move the 3d cursor to the center of the eyeball.',
            'ES': 'Mueva el cursor 3d al centro del globo ocular.' # 'Determinar el centro del globo ocular. Mover el cursor 3d a esa posición.'
            },
        'accion': Reprop_Neck
    },
    # 4
    {
        'imagen': 'paso_4.png',
        'titulo': {
            'EN': 'Step 4',
            'ES': 'Paso 4'
            },
        'texto': {
            'EN': 'Place the eye controls as shown in the image.',
            'ES': 'Posiciona los controles de los ojos como se muestra en la imagen.'
            },
        'accion': Reprop_Head
    },
    # 5
    {
        'imagen': 'paso_1.png',
        'titulo': {
            'EN': 'Step 5',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place “master_torso” at the height of hips.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Sole_Side
    },
    # 6
    {
        'imagen': 'paso_1.png',
        'titulo': {
            'EN': 'Step 5',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place “master_torso” at the height of hips.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Sole_Bot
    },
    # 7
    {
        'imagen': 'paso_1.png',
        'titulo': {
            'EN': 'Step 5',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place “master_torso” at the height of hips.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Foot_Side_Rolls
    },
    # 7
    {
        'imagen': 'paso_1.png',
        'titulo': {
            'EN': 'Step 5',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place “master_torso” at the height of hips.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Leg_Front
    }
)


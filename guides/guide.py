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
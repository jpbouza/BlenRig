from os.path import dirname, join
from . reproportion.guide_reproportion_actions import *

images_dir = join(dirname(__file__), 'images')

languages = (
    # ID # Name # Description
    ('EN', 'English', ""),
    ('ES', 'Spanish', "")
)

texts_dict = {
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
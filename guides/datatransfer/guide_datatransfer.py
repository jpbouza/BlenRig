from os.path import dirname, join
from .. datatransfer.guide_datatransfer_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_DATATRANSFER = (
    #Edit Weith Transfer Model Face Shape
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': ' Edit Weith Transfer Model Face Shape',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Face of the Weight Transfer Model to avoid overlapping geometry, specially in the mouth.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Weight_Mesh_Shapekey_Face
    },
    #Edit Weith Transfer Model Fingers Shape
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': 'Edit Weith Transfer Model Fingers Shape',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Check the Fingers of the Weight Transfer Model to avoid overlapping geometry.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Weight_Mesh_Shapekey_Fingers
    },
    #Select Character's Head
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': "Select Character's Head Object",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select the Head Object of the character and click Next",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Select_Face
    },
    #Edit Character's Head
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': "Edit Character's Head",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Head to get the mouth opened and match the shape of the Weight Transfer Model. Once you are done, press the Transfer Weights Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Edit_Face
    },
    #Select Character's Fingers
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': "Select Character's Fingers Object",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select the Fingers Object of the character and click Next",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Select_Fingers
    },
    #Edit Character's Fingers
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': "Edit Character's Fingers",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the FIngers to match the shape of the Weight Transfer Model. Once you are done, press the Transfer Weights Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Edit_Fingers
    },
)

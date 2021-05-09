from os.path import dirname, join
from .. datatransfer.guide_datatransfer_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_DATATRANSFER = (
    #Edit Weith Transfer Model Head Shape
    {
        'imagen': ('DT_Weight_Mesh_Shapekey_Head_A.jpg', 'DT_Weight_Mesh_Shapekey_Head_B.jpg', 'DT_Weight_Mesh_Shapekey_Head_C.jpg', 'DT_Weight_Mesh_Shapekey_Head_D.jpg'),
        'titulo': {
            'EN': ' Edit Weight Transfer Model Head Shape',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Face of the Weight Transfer Model to avoid overlapping geometry, specially in the mouth.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Weight_Mesh_Shapekey_Head
    },
    #Edit Weith Transfer Model Hands Shape
    {
        'imagen': ('DT_Weight_Mesh_Shapekey_Hands_A.jpg', 'DT_Weight_Mesh_Shapekey_Hands_B.jpg'),
        'titulo': {
            'EN': 'Edit Weith Transfer Model Hands Shape',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Check the Fingers of the Weight Transfer Model to avoid overlapping geometry.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Weight_Mesh_Shapekey_Hands
    },
    #Select Character's Head
    {
        'imagen': 'DT_Select_Head.jpg',
        'titulo': {
            'EN': "Select Character's Head Object",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select the Head Object of the character and click Next",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Select_Head
    },
    #Edit Character's Head
    {
        'imagen': ('DT_Edit_Head_A.jpg', 'DT_Edit_Head_B.jpg', 'DT_Edit_Head_C.jpg'),
        'titulo': {
            'EN': "Edit Character's Head",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Head to get the mouth opened and match the shape of the Weight Transfer Model. Once you are done, press the Transfer Weights Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Edit_Head
    },
    #Select Character's Hands
    {
        'imagen': 'DT_Select_Hands.jpg',
        'titulo': {
            'EN': "Select Character's Hands Object",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Select the Hands Object of the character and click Next",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Select_Hands
    },
    #Edit Character's Hands
    {
        'imagen': ('DT_Edit_Hands_A.jpg', 'DT_Edit_Hands_B.jpg', 'DT_Edit_Hands_C.jpg'),
        'titulo': {
            'EN': "Edit Character's Hands",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Edit the Hands to match the shape of the Weight Transfer Model. Once you are done, press the Transfer Weights Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Edit_Hands
    },
    #Weights Transfer Finish
    {
        'imagen': ('Reprop_Tongue.jpg', 'Reprop_Finish.jpg'),
        'titulo': {
            'EN': "Weights Transfer Finish",
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "The face and hands of your character should be moving now",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': DT_Finish
    },
)

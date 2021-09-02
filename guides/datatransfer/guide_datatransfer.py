from os.path import dirname, join
from .. datatransfer.guide_datatransfer_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_DATATRANSFER = (
    #Edit Weith Transfer Model Head Shape
    {
        'imagen': ('DT_Weight_Mesh_Shapekey_Head_A.jpg', 'DT_Weight_Mesh_Shapekey_Head_B.jpg', 'DT_Weight_Mesh_Shapekey_Head_C.jpg', 'DT_Weight_Mesh_Shapekey_Head_D.jpg'),
        'titulo': {
            'EN': ' Edit Weight Transfer Model Head Shape',
            'ES': 'Edita el modelo Weight Transfer del contorno de la cabeza'
            },
        'texto': {
            'EN': "Edit the Face of the Weight Transfer Model to avoid overlapping geometry, specially in the mouth.",
            'ES': "Edita la cara del modelo Weight Transfer para evitar la superposición de la geometría, especialmente en la boca."
            },
        'accion': DT_Weight_Mesh_Shapekey_Head
    },
    #Edit Weith Transfer Model Hands Shape
    {
        'imagen': ('DT_Weight_Mesh_Shapekey_Hands_A.jpg', 'DT_Weight_Mesh_Shapekey_Hands_B.jpg'),
        'titulo': {
            'EN': 'Edit Weight Transfer Model Hands Shape',
            'ES': 'Edita el modelo Weight Transfer del contorno de las Manos'
            },
        'texto': {
            'EN': "Check the Fingers of the Weight Transfer Model to avoid overlapping geometry.",
            'ES': "Compruebe los dedos del modelo Weight Transfer para evitar la superposición de la geometría."
            },
        'accion': DT_Weight_Mesh_Shapekey_Hands
    },
    #Select Character's Head
    {
        'imagen': 'DT_Select_Head.jpg',
        'titulo': {
            'EN': "Select Character's Head Object",
            'ES': 'Selecciona la cabeza de tu personaje'
            },
        'texto': {
            'EN': "Select the Head Object of the character and press the 'Define Selected as Head' Button",
            'ES': "Selecciona la cabeza del personaje y pulse el botón 'Define Selected as Head'."
            },
        'accion': DT_Select_Head
    },
    #Edit Character's Head
    {
        'imagen': ('DT_Edit_Head_A.jpg', 'DT_Edit_Head_B.jpg', 'DT_Edit_Head_C.jpg'),
        'titulo': {
            'EN': "Edit Character's Head",
            'ES': 'Edita la cabeza del personaje'
            },
        'texto': {
            'EN': "Edit the Head to get the mouth opened and match the shape of the Weight Transfer Model. Once you are done, press the Transfer Weights Button",
            'ES': "Edita la cabeza para que la boca se abra y coincida con la forma del modelo Weight Transfer. Una vez que haya terminado, pulse el botón Transfer Weights"
            },
        'accion': DT_Edit_Head
    },
    #Select Character's Hands
    {
        'imagen': 'DT_Select_Hands.jpg',
        'titulo': {
            'EN': "Select Character's Hands Object",
            'ES': 'Selecciona las manos del personaje'
            },
        'texto': {
            'EN': "Select the Hands Object of the character and and press the 'Define Selected as Hands' Button",
            'ES': "Selecciona las Manos del personaje y pulse el botón 'Define Selected as Hands'"
            },
        'accion': DT_Select_Hands
    },
    #Edit Character's Hands
    {
        'imagen': ('DT_Edit_Hands_A.jpg', 'DT_Edit_Hands_B.jpg', 'DT_Edit_Hands_C.jpg'),
        'titulo': {
            'EN': "Edit Character's Hands",
            'ES': 'Edita las manos del personaje'
            },
        'texto': {
            'EN': "Edit the Hands to match the shape of the Weight Transfer Model. Once you are done, press the Transfer Weights Button",
            'ES': "Edita las Manos para que coincidan con la forma del Modelo Weight Transfer. Una vez que haya terminado, pulse el botón 'Transfer Weights'"
            },
        'accion': DT_Edit_Hands
    },
    #Weights Transfer Finish
    {
        'imagen': ('DT_Finish_A.jpg', 'DT_Finish_B.jpg', 'DT_Finish_C.jpg', 'DT_Finish_D.jpg'),
        'titulo': {
            'EN': "Weights Transfer Finish",
            'ES': 'Weights Transfer Finalizado'
            },
        'texto': {
            'EN': "The face and hands of your character should be moving now",
            'ES': "La cara y las manos de tu personaje deberían moverse ahora"
            },
        'accion': DT_Finish
    },
)

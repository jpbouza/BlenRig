from os.path import dirname, join
from .. mdef.guide_mdef_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_MDEF = (
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
        'accion': MDEF_Select_Body_Objects
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
        'accion': MDEF_Edit_Mdef_Cage
},
    #Check Mesh Deform Binding
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Check Mesh Deform Binding',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Press the Bind Mesh Deform Button. Move the character away and check hat all of its vertices are moving along with the rig, otherwise, press the button again and Edit the cage until all the vertices move",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Binding_Check
},
    #Mesh Deform Final Binding
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mesh Deform Final Binding',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Press the Bind Mesh Deform Button. Go grab a cup of coffee because depending on how many objects you are binding, this can take long.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Final_Binding
}
)



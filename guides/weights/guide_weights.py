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
            'EN': "Press the Bind Mesh Deform Button. Move the character away and check that all of its vertices are moving along with the rig. Otherwise, press the Unbind button, Edit the cage and Bind again until all the vertices move with the rig",
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
            'EN': "If all vertices are moving along, press the Unbind button and then the Bind Mesh Deform(Final) Button. Go grab a cup of coffee because depending on how many objects you are binding, this can take long.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Final_Binding
}
)



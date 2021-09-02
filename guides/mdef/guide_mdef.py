from os.path import dirname, join
from .. mdef.guide_mdef_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_MDEF = (
    #Define Character Body Objects
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Define Character Body Objects',
            'ES': 'Define los objetos que componen el cuerpo de tu personaje'
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
            'ES': 'Edita el Mesh Deform Cage'
            },
        'texto': {
            'EN': "Edit the Mesh Deform Cage so that it wraps around the charcter's mesh. You can use the 'Adjust Cage' button to get a first approximation. Keep in mind that the closer the cage is from the character, the stiffer the deformation, the further away, the smoother the deformation. Use this strategically to get better deformation in difficult areas, such as the shoulders.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Edit_Mdef_Cage
},
    #Check Mesh Deform Binding
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Check Mesh Deform Binding',
            'ES': 'Comprueba la vinculacion de la malla de deformación'
            },
        'texto': {
            'EN': "Press the Bind Mesh Deform Button. Move the character away and check that all of its vertices are moving along with the rig. Otherwise, press the Unbind button, then Edit the cage and Bind again until all the vertices move with the rig",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Binding_Check
},
    #Mesh Deform Final Binding
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mesh Deform Final Binding',
            'ES': 'Finalización de la vinculacion del Mesh Deform'
            },
        'texto': {
            'EN': "If you managed to get all the vertices right, press the Unbind button and then the Bind Mesh Deform(Final) Button. Depending on the number of objects you are binding, this process can take long. Go take a cup of coffe.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Final_Binding
}
)



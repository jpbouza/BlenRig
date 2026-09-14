from os.path import dirname, join
from .. mdef.guide_mdef_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_MDEF = (
    #Define Character Body Objects
    {
        'imagen': 'MDEF_Intro.jpg',
        'titulo': {
            'EN': 'introduction',
            'ES': 'Mesh Deform Introduccion'
            },
        'texto': {
            'EN': "In this Guide you will setup Mesh Deform. With this method, the body of the character is deformed with a Low Resolution Mesh. Head, Hands and eventually Toes are excluded from this.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Intro
    },
    #Define Character Body Objects
    {
        'imagen': ('MDEF_Select_Body_Objects_A.jpg', 'MDEF_Select_Body_Objects_B.jpg'),
        'titulo': {
            'EN': 'Character Body Objects',
            'ES': 'Define los objetos que componen el cuerpo de tu personaje'
            },
        'texto': {
            'EN': "Select all the objects that conform the Character's Body and press the 'Set Body Objects' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Select_Body_Objects
    },
    #Edit the Mesh Deform Cage
    {
        'imagen': ('MDEF_Edit_Mdef_Cage_A.jpg', 'MDEF_Edit_Mdef_Cage_B.jpg', 'MDEF_Edit_Mdef_Cage_C.jpg'),
        'titulo': {
            'EN': 'Edit the Mesh Deform Cage',
            'ES': 'Edita el Mesh Deform Cage'
            },
        'texto': {
            'EN': "The Mesh Deform Cage should wrap the character around. The closer the cage is from the character, the stiffer the deformation, the further away, the smoother. Keep this in mind for difficult areas, such as the shoulders.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Edit_Mdef_Cage
},
    #Check Mesh Deform Binding
    {
        'imagen': ('MDEF_Binding_Check_A.jpg', 'MDEF_Binding_Check_B.jpg', 'MDEF_Binding_Check_C.jpg'),
        'titulo': {
            'EN': 'Check Mesh Deform Binding',
            'ES': 'Comprueba la vinculacion de la malla de deformación'
            },
        'texto': {
            'EN': "Press the Bind Mesh Deform Button. Move the character away. All of its vertices should move along with the rig. Otherwise, press the 'Edit Mdef Cage' Button, tweak the cage and Bind again until all the body vertices move with the rig",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Binding_Check
},
    #Mesh Deform Final Binding
    {
        'imagen': 'MDEF_Final_Binding.jpg',
        'titulo': {
            'EN': 'Mesh Deform Final Binding',
            'ES': 'Finalización de la vinculacion del Mesh Deform'
            },
        'texto': {
            'EN': "If you managed to get all the vertices right, press the Unbind button and then the Bind Mesh Deform(Final) Button. Depending on the number of objects you are binding, this process can take long. Go take a cup of coffe.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Final_Binding
},
    #Mesh Finish
    {
        'imagen': 'MDEF_Finish.jpg',
        'titulo': {
            'EN': 'Mesh Deform Finish',
            'ES': 'Finalización de la vinculacion del Mesh Deform'
            },
        'texto': {
            'EN': "Move on to the next Guide!",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': MDEF_Finish
}
)



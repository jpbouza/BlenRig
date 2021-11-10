from os.path import dirname, join
from .. lattices.guide_lattices_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_LATTICES = (
    #Introduction
    {
        'imagen': 'LATTICES_Intro.jpg',
        'titulo': {
            'EN': 'Introduction',
            'ES': 'Introducción'
            },
        'texto': {
            'EN': "In this Guide you will adjust the placement of the Lattices of the rig. Lattices will allow you to achieve extra deformations, most commonly used for toon characters.",
            'ES': "En esta Guia, tu podras ajustar el posicionamiento del Lattices del rig. El Lattices te permitira lograr una deformaciones adicionales,más comúnmente utilizadas para los personajes toon."
            },
        'accion': LATTICES_Intro
    },
    #Edit Body Lattice
    {
        'imagen': ('LATTICES_Adjust_Body_A.jpg', 'LATTICES_Adjust_Body_B.jpg', 'LATTICES_Position.jpg'),
        'titulo': {
            'EN': 'Edit Body Lattice',
            'ES': 'Edita el Lattice del cuerpo'
            },
        'texto': {
            'EN': "Adjust the Body Lattice. Press the 'Edit Lattice Position' to move the lattice, then press the 'Apply Lattice Position' button.",
            'ES': "Ajuste el Lattice del cuerpo, pulsa el botón 'Edit Lattice Position' para mover el lattice, luego pulse el botón 'Apply Lattice Position'."
            },
        'accion': LATTICES_Adjust_Body
    },
    #Edit Head Lattice
    {
        'imagen': ('LATTICES_Adjust_Head_A.jpg', 'LATTICES_Adjust_Head_B.jpg', 'LATTICES_Position.jpg'),
        'titulo': {
            'EN': 'Edit Head Lattice',
            'ES': 'Edita el Lattice de la cabeza'
            },
        'texto': {
            'EN': "Adjust the Head Lattice. Press the 'Edit Lattice Position' to move the lattice, then press the 'Apply Lattice Position' button.",
            'ES': "Ajusta el Lattice de la cabeza, pulsa el botón 'Edit Lattice Position' para mover el lattice, luego pulse el botón 'Apply Lattice Position'."
            },
        'accion': LATTICES_Adjust_Head
    },
    #Edit Brow Lattice
    {
        'imagen': ('LATTICES_Adjust_Brow_A.jpg', 'LATTICES_Adjust_Brow_B.jpg', 'LATTICES_Position.jpg'),
        'titulo': {
            'EN': 'Edit Brow Lattice',
            'ES': 'Edita el Lattice de las cejas'
            },
        'texto': {
            'EN': "Adjust the Brow Lattice. Press the 'Edit Lattice Position' to move the lattice, then press the 'Apply Lattice Position' button.",
            'ES': "Ajusta el Lattice de las cejas, pulsa el botón 'Edit Lattice Position' para mover el lattice, luego pulse el botón 'Apply Lattice Position'."
            },
        'accion': LATTICES_Adjust_Brow
    },
    #Edit Mouth Lattice
    {
        'imagen': ('LATTICES_Adjust_Mouth_A.jpg', 'LATTICES_Adjust_Mouth_B.jpg', 'LATTICES_Position.jpg'),
        'titulo': {
            'EN': 'Edit Mouth Lattice',
            'ES': 'Edita el Lattice de la boca'
            },
        'texto': {
            'EN': "Adjust the Mouth Lattice. Press the 'Edit Lattice Position' to move the lattice, then press the 'Apply Lattice Position' button.",
            'ES': "Ajusta el Lattice de la boca, pulsa el botón 'Edit Lattice Position' para mover el lattice, luego pulse el botón 'Apply Lattice Position'."
            },
        'accion': LATTICES_Adjust_Mouth
    },
    #Edit Eyes Lattice
    {
        'imagen': ('LATTICES_Adjust_Eyes_A.jpg', 'LATTICES_Adjust_Eyes_B.jpg', 'LATTICES_Adjust_Eyes_C.jpg'),
        'titulo': {
            'EN': 'Edit Eyes Lattices',
            'ES': 'Edita el Lattice de los ojos'
            },
        'texto': {
            'EN': "Adjust the Lattice of the Left Eye. Press the 'Edit Lattice Position' to move the lattice, then press the 'Apply Lattice Position' button. Finally Mirror the position to the Right Eye Lattice with the 'Mirror Lattice Transforms' button",
            'ES': "Edita el Lattice de los ojos, pulsa el botón 'Edit Lattice Position' para mover el lattice, luego pulse el botón 'Apply Lattice Position'."
            },
        'accion': LATTICES_Adjust_Eyes
    },
    #Lattices Finish
    {
        'imagen': 'LATTICES_Finish.jpg',
        'titulo': {
            'EN': 'Lattices Finish',
            'ES': 'Edita el Lattice del cuerpo'
            },
        'texto': {
            'EN': "Done! Move to the Weight Painting Guide!",
            'ES': "Hecho! Ahora puedes pasar a la guia 'Weigth Painting'."
            },
        'accion': LATTICES_Finish
    }
)




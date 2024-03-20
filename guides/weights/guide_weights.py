from os.path import dirname, join
from .. weights.guide_weights_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_WEIGHTS = (
    #Intro
    {
        'imagen': 'WEIGHTS_Intro.jpg',
        'titulo': {
            'EN': 'Introduction',
            'ES': 'Introduccion'
            },
        'texto': {
            'EN': "Adjust the Weights of the Mdef Cage and the Character if needed. Set the values of the Realistic Joints and the Volume Preservation Bones to simulate Sekeltal Structure volume.",
            'ES': 'Ajuste los Pesos del "Mdef Cage" y del Personaje si es necesario. Ajusta los valores de las Articulaciones Realistas y de los Huesos de Preservación del Volumen para simular el volumen de la Estructura ósea.'
            },
        'accion': WEIGHTS_Intro
    },
    #Ankle Poses
    {
        'imagen': ('WEIGHTS_Cage_Ankle_A.jpg', 'WEIGHTS_Cage_Ankle_B.jpg', 'WEIGHTS_Cage_Ankle_C.jpg', 'WEIGHTS_Cage_Ankle_D.jpg', 'WEIGHTS_Cage_Ankle_E.jpg'),
        'titulo': {
            'EN': 'Ankle',
            'ES': 'Tobillo'
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-6). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'. Adjust the weights with 'Toggle Weight Painting'.",
            'ES': 'Desplázate por las Poses con el control deslizante (0-6). Ajusta primero los valores de RJ y VP. Si es necesario, selecciona el Personaje para mejorar la deformación con "Edit Corrective Smooth Vgroup". Ajuste los pesos con "Toggle Weight Painting".'
            },
        'accion': WEIGHTS_Cage_Ankle
    },
    #Foot Toe Poses
    {
        'imagen': ('WEIGHTS_Cage_Foot_Toe_A.jpg', 'WEIGHTS_Cage_Foot_Toe_B.jpg', 'WEIGHTS_Cage_Foot_Toe_C.jpg', 'WEIGHTS_Cage_Foot_Toe_D.jpg', 'WEIGHTS_Cage_Foot_Toe_E.jpg', 'WEIGHTS_Cage_Foot_Toe_F.jpg'),
        'titulo': {
            'EN': 'Foot Toe',
            'ES': 'Dedos del Pie'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the Poses (0-4) and set the VP values. You can always edit Corrective Smooth on the model or edit the Mdef Cage Weights.",
            'ES': 'Cambia la articulación activa con "Seleccionar número de articulación". Desplázate por las poses (0-4) y establezca los valores de VP. Siempre puedes editar el "Corrective Smooth" en el modelo o editar los pesos del "Mdef Cage".'
            },
        'accion': WEIGHTS_Cage_Foot_Toe
    },
    #Knee Poses
    {
        'imagen': ('WEIGHTS_Cage_Knee_A.jpg', 'WEIGHTS_Cage_Knee_B.jpg'),
        'titulo': {
            'EN': 'Knee',
            'ES': 'Rodilla'
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-4). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'. Adjust the weights with 'Toggle Weight Painting'.",
            'ES': 'Desplázate por las poses con el control deslizante (0-4). Ajusta primero los valores de RJ y VP. Si es necesario, selecciona el Personaje para mejorar la deformación con "Edit Vgroup Corrective smooth". Ajusta los pesos con "Toggle Weight Painting".'
            },
        'accion': WEIGHTS_Cage_Knee
    },
    #Thigh Poses
    {
        'imagen': 'WEIGHTS_Cage_Thigh.jpg',
        'titulo': {
            'EN': 'Thigh',
            'ES': 'Muslo'
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-4). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'. Adjust the weights with 'Toggle Weight Painting'.",
            'ES': 'Desplázate por las poses con el control deslizante (0-4). Ajusta primero los valores de RJ y VP. Si es necesario, selecciona el Personaje para mejorar la deformación con "Edit Vgroup Corrective smooth". Ajusta los pesos con "Toggle Weight Painting".'
            },
        'accion': WEIGHTS_Cage_Thigh
    },
    #Torso Poses
    {
        'imagen': ('WEIGHTS_Cage_Torso_A.jpg', 'WEIGHTS_Cage_Torso_B.jpg', 'WEIGHTS_Cage_Torso_C.jpg', 'WEIGHTS_Cage_Torso_D.jpg', 'WEIGHTS_Cage_Torso_E.jpg', 'WEIGHTS_Cage_Torso_F.jpg'),
        'titulo': {
            'EN': 'Torso',
            'ES': 'Torso'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the Poses (0-6) and set the VP values. You can always edit Corrective Smooth on the model or edit the Mdef Cage Weights.",
            'ES': 'Cambia la articulación activa con "Select Joint Number". Desplázate por las Poses (0-6) y establece los valores de VP. Siempre puedes editar "Correctivo smooth" en el modelo o editar los Pesos del Mdef Cage.'
            },
        'accion': WEIGHTS_Cage_Torso
    },
    #Neck Poses
    {
        'imagen': ('WEIGHTS_Cage_Neck_A.jpg', 'WEIGHTS_Cage_Neck_B.jpg', 'WEIGHTS_Cage_Neck_C.jpg'),
        'titulo': {
            'EN': 'Neck',
            'ES': 'Cuello'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the Poses (0-6) and set the VP values. You can always edit Corrective Smooth on the model or edit the Mdef Cage Weights.",
            'ES': 'Cambia la articulación activa con "Select Joint Number". Desplaza por las Posturas (0-6) y establece los valores de VP. Siempre puedes editar el "Corrective Smooth" en el modelo o editar los Pesos del "Mdef Cage".'
            },
        'accion': WEIGHTS_Cage_Neck
    },
    #Clavicle Poses
    {
        'imagen': ('WEIGHTS_Cage_Clavicle_A.jpg', 'WEIGHTS_Cage_Clavicle_B.jpg'),
        'titulo': {
            'EN': 'Clavicle',
            'ES': 'Clavicula'
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-4). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'. Adjust the weights with 'Toggle Weight Painting'.",
            'ES': 'Desplázate por las Poses con el deslizador (0-4). Ajusta primero los valores de RJ y VP. Si es necesario, selecciona el Personaje para mejorar la deformación con "Edit Corrective Smooth Vgroup". Ajusta los pesos con "Toggle Weight Painting".'
            },
        'accion': WEIGHTS_Cage_Clavicle
    },
    #Arm Poses
    {
        'imagen': 'WEIGHTS_Cage_Shoulder.jpg',
        'titulo': {
            'EN': 'Arm / Shoulder',
            'ES': 'Brazo / Hombro '
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-4). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'. Adjust the weights with 'Toggle Weight Painting'.",
            'ES': 'Desplázate por las Poses con el deslizador (0-4). Ajusta primero los valores de RJ y VP. Si es necesario, selecciona el Personaje para mejorar la deformación con "Edit Corrective Smooth Vgroup". Ajusta los pesos con "Toggle Weight Painting".'
            },
        'accion': WEIGHTS_Cage_Shoulder
    },
    #Forearm Poses
    {
        'imagen': ('WEIGHTS_Cage_Elbow_A.jpg', 'WEIGHTS_Cage_Elbow_B.jpg'),
        'titulo': {
            'EN': 'Elbow',
            'ES': 'Codo'
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-4). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'. Adjust the weights with 'Toggle Weight Painting'.",
            'ES': 'Desplázate por las Poses con el deslizador (0-4). Ajusta primero los valores de RJ y VP. Si es necesario, selecciona el Personaje para mejorar la deformación con "Edit Corrective Smooth Vgroup". Ajusta los pesos con "Toggle Weight Painting".'
            },
        'accion': WEIGHTS_Cage_Elbow
    },
    #Wrist Poses
    {
        'imagen': 'WEIGHTS_Cage_Wrist.jpg',
        'titulo': {
            'EN': 'Wrist',
            'ES': 'Muñeca'
            },
        'texto': {
            'EN': "Scroll through the Poses with the slider (0-6). Adjust the RJ and VP values first. Adjust the weights with 'Toggle Weight Painting'. Further adjustments will be made in the next Step",
            'ES': 'Desplázate por las Poses con el deslizador (0-6). Ajuste primero los valores de RJ y VP. Ajuste los pesos con "Toggle Weight Painting". Otros ajustes se harán en el siguiente Paso'
            },
        'accion': WEIGHTS_Cage_Wrist
    },
    #Character Mesh Wrist Poses
    {
        'imagen': ('WEIGHTS_Char_Wrist_A.jpg', 'WEIGHTS_Char_Wrist_B.jpg', 'WEIGHTS_Char_Wrist_C.jpg', 'WEIGHTS_Char_Wrist_D.jpg', 'WEIGHTS_Char_Wrist_E.jpg'),
        'titulo': {
            'EN': 'Hands Mdef VGroup',
            'ES': 'Mdef Grupo de Vertices de las Manos'
            },
        'texto': {
            'EN': "Edit the 'no_mdef' Vertex Group to define the area of influence of the Mesh Deform and the Armature Modifier. Hands should have full influence of this group. Transition should happen at the Wrist area.",
            'ES': 'Edita el Grupo de Vértices "no_mdef" para definir el área de influencia del "Mesh Deform" y del Modificador de Armadura. Las manos deben tener toda la influencia de este grupo. La transición debe ocurrir en el área de la muñeca.'
            },
        'accion': WEIGHTS_Char_Wrist
    },
    #Hand Volume Preservation Poses
    {
        'imagen': ('WEIGHTS_Char_Hand_VP_A.jpg', 'WEIGHTS_Char_Hand_VP_B.jpg', 'WEIGHTS_Char_Hand_VP_C.jpg', 'WEIGHTS_Char_Hand_VP_D.jpg', 'WEIGHTS_Char_Hand_VP_E.jpg', 'WEIGHTS_Char_Hand_VP_F.jpg'),
        'titulo': {
            'EN': 'Hand VP & RJ Values',
            'ES': 'Valores VP y RJ de la mano'
            },
        'texto': {
            'EN': "Define the general values of Realistic Joints and Volume Preservation of the Fingers. Scroll through the key Poses with the 'Set Joint Transform' slider.",
            'ES': 'Define los valores generales de Articulaciones Realistas y Preservación del Volumen de los Dedos. Desplaza te a través de las posturas clave con el deslizador "Set Joint Transform".'
            },
        'accion': WEIGHTS_Char_Hand_VP
    },
    #Fingers 1 Poses
    {
        'imagen': ('WEIGHTS_Char_Fings_1_A.jpg', 'WEIGHTS_Char_Fings_1_B.jpg', 'WEIGHTS_Char_Fings_1_C.jpg', 'WEIGHTS_Char_Fings_1_D.jpg', 'WEIGHTS_Char_Fings_1_E.jpg', 'WEIGHTS_Char_Fings_1_F.jpg', 'WEIGHTS_Char_Fings_1_G.jpg', 'WEIGHTS_Char_Fings_1_H.jpg', 'WEIGHTS_Char_Fings_1_I.jpg'),
        'titulo': {
            'EN': 'Palm',
            'ES': 'Palma'
            },
        'texto': {
            'EN': "Edit the Weights of the Palm and the first Joint of the Fingers. Change the active Finger with the 'Set Joint Number' Button. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Volume Preservation values first",
            'ES': 'Edita los pesos de la palma y la primera articulación de los dedos. Cambia el Dedo activo con el Botón "Set Joint Number". Desplaza te a través de las posturas clave con el deslizador "Set Joint Transform". Ajusta primero los valores de Preservación del Volumen.'
            },
        'accion': WEIGHTS_Char_Fings_1
    },
    #Fingers 2 Poses
    {
        'imagen': ('WEIGHTS_Char_Fings_2_A.jpg', 'WEIGHTS_Char_Fings_2_B.jpg', 'WEIGHTS_Char_Fings_2_C.jpg'),
        'titulo': {
            'EN': 'Fingers',
            'ES': 'Dedos'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the Poses with the slider (0-2). Adjust the RJ and VP values first. If needed, select the Character to enhance deformation with 'Edit Corrective Smooth Vgroup'.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Fings_2
    },
    #Head Poses
    {
        'imagen': ('WEIGHTS_Char_Head_A.jpg', 'WEIGHTS_Char_Head_B.jpg', 'WEIGHTS_Char_Head_C.jpg', 'WEIGHTS_Char_Head_D.jpg', 'WEIGHTS_Char_Head_E.jpg'),
        'titulo': {
            'EN': 'Head Mdef VGroup',
            'ES': 'Mdef Grupo de Vertices de la Cabeza'
            },
        'texto': {
            'EN': "Edit the 'no_mdef' Vertex Group to define the area of influence of the Mesh Deform and the Armature Modifier. Head should have full influence of this group. Define a short transition and check deformation in the different poses.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Head
    },
    #Head Joints Poses
    {
        'imagen': ('WEIGHTS_Char_Head_Joints_A.jpg', 'WEIGHTS_Char_Head_Joints_B.jpg', 'WEIGHTS_Char_Head_Joints_C.jpg'),
        'titulo': {
            'EN': 'Head Joints',
            'ES': 'Articulaciones de la cabeza'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the Poses (0-4) and paint the joint. You can always edit Corrective Smooth on the model.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Head_Joints
    },
    #Ear Poses
    {
        'imagen': ('WEIGHTS_Char_Ears_A.jpg', 'WEIGHTS_Char_Ears_B.jpg', 'WEIGHTS_Char_Ears_C.jpg'),
        'titulo': {
            'EN': 'Ear',
            'ES': 'Oreja'
            },
        'texto': {
            'EN': "Change the active Joint with 'Select Joint Number'. Scroll through the Poses (0-2) and paint the joint. You can always edit Corrective Smooth on the model.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Ears
    },
    #Eyebrows Poses
    {
        'imagen': ('WEIGHTS_Char_Eyebrows_A.jpg', 'WEIGHTS_Char_Eyebrows_B.jpg', 'WEIGHTS_Char_Eyebrows_C.jpg'),
        'titulo': {
            'EN': 'Eyebrows',
            'ES': 'Cejas'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Eyebrows. Change the active Controller with the 'Set Joint Number' Button. You can always edit Corrective Smooth on the model.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Eyebrows
    },
    #Eye Sockets
    {
        'imagen': 'WEIGHTS_Char_Eye_Socket.jpg',
        'titulo': {
            'EN': 'Eye Socket',
            'ES': 'Caja del Ojo'
            },
        'texto': {
            'EN': "Paint the Inner part of the Eyelids with the 'Eye_Mstr_STR' bone",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Eye_Socket
    },
    #Eyelids Poses
    {
        'imagen': ('WEIGHTS_Char_Eyelids_A.jpg', 'WEIGHTS_Char_Eyelids_B.jpg', 'WEIGHTS_Char_Eyelids_C.jpg', 'WEIGHTS_Char_Eyelids_D.jpg', 'WEIGHTS_Char_Eyelids_E.jpg'),
        'titulo': {
            'EN': 'Eyelids',
            'ES': 'Pestañas'
            },
        'texto': {
            'EN': "Clean up the Weights. Change the controller with 'Set Joint Number'. Make sure that the Borders of the Eyelids are only painted with the Border bones. Do NOT Paint the Eyelids with the Corrective Smooth Vertex Group",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Eyelids
    },
    #Cheeks
    {
        'imagen': ('WEIGHTS_Char_Cheeks_A.jpg', 'WEIGHTS_Char_Cheeks_B.jpg', 'WEIGHTS_Char_Cheeks_C.jpg', 'WEIGHTS_Char_Cheeks_D.jpg'),
        'titulo': {
            'EN': 'Cheeks',
            'ES': 'Mejillas'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Cheeks. Change the active Controller with the 'Set Joint Number' Button. You can always edit Corrective Smooth on the model.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Cheeks
    },
    #Nose
    {
        'imagen': ('WEIGHTS_Char_Nose_A.jpg', 'WEIGHTS_Char_Nose_B.jpg', 'WEIGHTS_Char_Nose_C.jpg', 'WEIGHTS_Char_Nose_D.jpg', 'WEIGHTS_Char_Nose_E.jpg'),
        'titulo': {
            'EN': 'Nose',
            'ES': 'Nariz'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Nose. Change the active Controller with the 'Set Joint Number' Button. You can always edit Corrective Smooth on the model.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Nose
    },
    #Mouth
    {
        'imagen': ('WEIGHTS_Char_Mouth_A.jpg', 'WEIGHTS_Char_Mouth_B.jpg', 'WEIGHTS_Char_Mouth_C.jpg', 'WEIGHTS_Char_Mouth_D.jpg'),
        'titulo': {
            'EN': 'Mouth',
            'ES': 'Boca'
            },
        'texto': {
            'EN': "Clean up the Weights of the Mouth area. Move the controllers around to check deformation on the area. Do NOT Paint the Lips with the Corrective Smooth Vertex Group. Also paint the Inner parts of the Cheeks",
            'ES': 'Recorre rápidamente las articulaciones limpiando los pesos de la zona de la boca. Mueve los controladores alrededor para comprobar la deformación del área. NO Pinte los labios en el "Corrective Smooth Vertex Group"'
            },
        'accion': WEIGHTS_Char_Mouth
    },
    #Inner Mouth
    {
        'imagen': 'WEIGHTS_Char_Inner_Mouth.jpg',
        'titulo': {
            'EN': 'Inner Mouth',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Paint the Teeth, Gums, Uvula and Tongue. You might want to enable the Auto Normalize and Face Masks options to clean up intrecate areas. Alternatively you can activate the 'Show Bones' options to unhide all the deformation bones.",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Char_Inner_Mouth
    },
    #Lattice Head
    {
        'imagen': 'WEIGHTS_Char_Lattice_Head.jpg',
        'titulo': {
            'EN': 'Lattice Head',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Paint the Head Lattice Vertex Group",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Char_Lattice_Head
    },
    #Lattice Mouth
    {
        'imagen': 'WEIGHTS_Char_Lattice_Mouth.jpg',
        'titulo': {
            'EN': 'Lattice Mouth',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Paint the Mouth Lattice Vertex Group",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Char_Lattice_Mouth
    },
        #Lattice Eyebrow
    {
        'imagen': 'WEIGHTS_Char_Lattice_Brow.jpg',
        'titulo': {
            'EN': 'Lattice Eyebrow',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Paint the Eyebrow Lattice Vertex Group",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Char_Lattice_Brow
    },
        #Lattice Eye
    {
        'imagen': 'WEIGHTS_Char_Lattice_Eye.jpg',
        'titulo': {
            'EN': 'Lattice Eye',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Paint the Eye Lattice Vertex Group",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Char_Lattice_Eye
    },
        #Lattice Finish
    {
        'imagen': 'WEIGHTS_Finish.jpg',
        'titulo': {
            'EN': 'Lattice Eye',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Move on to the Actions Guide!",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Finish
    },
)





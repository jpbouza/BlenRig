from os.path import dirname, join
from .. weights.guide_weights_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_WEIGHTS = (
    #Intro
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Weights Guide Intro',
            'ES': 'Intro Guia de Pesos'
            },
        'texto': {
            'EN': "In this Guide you will be able to adjust the Character's and Mdef Cage Weights if needed. You will also be able to adjust the values of the Volume Preservation Bones and the Realistic Joints values to simulate Sekeltal Structure volume in the Joints. Keep in mind that this will be the initial deformation setup, if you need to fine tune it, you will be able to do it in the Shapekeys Guide",
            'ES': 'En esta Guía podrás ajustar los Pesos del Personaje y del "Mdef Cage" si es necesario. También podrás ajustar los valores de los Huesos de Preservación del Volumen y los valores de las Juntas Realistas para simular el volumen de la Estructura Sekeltal en las Juntas. Ten en cuenta que esta será la configuración inicial de la deformación, si necesitas afinarla, podrás hacerlo en la Guía de Shapekeys.'

            },
        'accion': WEIGHTS_Intro
    },
    #Ankle Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Ankle',
            'ES': 'Tobillo'
            },
        'texto': {
            'EN': "Check the Ankle deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Realistic Joints and Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Ankle
    },
    #Foot Toe Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Foot Toe',
            'ES': 'Dedos del Pie'
            },
        'texto': {
            'EN': "Check the 'Foot Toe joints' deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Change the active Joint with the 'Set Joint Number' Button. Adjust the Realistic Joints and Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Foot_Toe
    },
    #Knee Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Knee',
            'ES': 'Rodilla'
            },
        'texto': {
            'EN': "Check the Knee deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Realistic Joints and Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Knee
    },
    #Thigh Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Thigh',
            'ES': 'Muslo'
            },
        'texto': {
            'EN': "Check the Thigh deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Thigh
    },
    #Torso Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Define Character Body Objects',
            'ES': 'Definir los objetos del cuerpo del personaje'
            },
        'texto': {
            'EN': "Check the Torso deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Change the active Joint with the 'Set Joint Number' Button. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Torso
    },
    #Neck Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Neck',
            'ES': 'Cuello'
            },
        'texto': {
            'EN': "Check the Neck deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Change the active Joint with the 'Set Joint Number' Button. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Neck
    },
    #Clavicle Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Clavicle',
            'ES': 'Clavicula'
            },
        'texto': {
            'EN': "Check the Clavicle deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Clavicle
    },
    #Arm Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Arm / Shoulder',
            'ES': 'Brazo / Hombro '
            },
        'texto': {
            'EN': "Check the Shoulder deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Shoulder
    },
    #Forearm Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Elbow',
            'ES': 'Codo'
            },
        'texto': {
            'EN': "Check the Elbow deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Realistic Joints and Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Elbow
    },
    #Wrist Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Wrist',
            'ES': 'Muñeca'
            },
        'texto': {
            'EN': "Check the Wrist deformation. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Realistic Joints and Volume Preservation values first. Select the Character's Mesh and enhance deformation with the 'Edit Corrective Smooth Vgroup' Button. If you need to adjust the weights press the 'Toggle Weight Painting' button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Cage_Wrist
    },
    #Character Mesh Wrist Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Hands Mdef Vertex Group',
            'ES': 'Mdef Grupo de Vertices de las Manos'
            },
        'texto': {
            'EN': "Edit the 'no_mdef' Vertex Group to define the area of influence of the Mesh Deform and the Armature Modifier. Hands should have full influence of this group. Transition should happen at the Wrist area.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Wrist
    },
    #Hand Volume Preservation Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Hands General VP & RJ Values',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': "Define the general values of Realistic Joints and Volume Preservation for the hands. Scroll through the key Poses with the 'Set Joint Transform' slider.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Hand_VP
    },
    #Fingers 1 Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Palm',
            'ES': 'Palma'
            },
        'texto': {
            'EN': "Edit the Weights of the Palm and the first Joint of the Fingers. Change the active Finger with the 'Set Joint Number' Button. Scroll through the key Poses with the 'Set Joint Transform' slider. Adjust the Volume Preservation values first",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Fings_1
    },
    #Fingers 1 Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Fingers',
            'ES': 'Dedos'
            },
        'texto': {
            'EN': "Edit the Weights of the Fingers. Scroll through the key Poses with the 'Set Joint Transform' slider. Change the active Joint with the 'Set Joint Number' Button. Adjust the Volume Preservation values first. Enhance deformation with the 'Select Corrective Smooth Vgroup' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Fings_2
    },
    #Head Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Head Mdef Vertex Group',
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
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Head Joints',
            'ES': 'Articulaciones de la cabeza'
            },
        'texto': {
            'EN': "Edit the Weights of the Head Joints. Scroll through the key Poses with the 'Set Joint Transform' slider. Change the active Joint with the 'Set Joint Number' Button. Enhance deformation with the 'Select Corrective Smooth Vgroup' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Head_Joints
    },
    #Ear Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Ear',
            'ES': 'Oreja'
            },
        'texto': {
            'EN': "Edit the Weights of the Ear Joints. Scroll through the key Poses with the 'Set Joint Transform' slider. Change the active Joint with the 'Set Joint Number' Button. Enhance deformation with the 'Select Corrective Smooth Vgroup' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Ears
    },
    #Eyebrows Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Eyebrows',
            'ES': 'Cejas'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Eyebrows. Change the active Controller with the 'Set Joint Number' Button. Scroll through the key Poses with the 'Set Joint Transform' slider. Enhance deformation with the 'Select Corrective Smooth Vgroup' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Eyebrows
    },
    #Eye Sockets
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Eye Socket',
            'ES': 'Caja del Ojo'
            },
        'texto': {
            'EN': "Paint the inner part of the Eyelids with the Eye_Mstr_STR bone",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Eye_Socket
    },
    #Eyelids Poses
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Eyelids',
            'ES': 'Pestañas'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Eyelids. Change the active Controller with the 'Set Joint Number' Button. Scroll through the key Poses with the 'Set Joint Transform' slider. Do NOT Paint the Eyelids with the Corrective Smooth Vertex Group.",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Eyelids
    },
    #Cheeks
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Cheeks',
            'ES': 'Mejillas'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Cheeks. Change the active Controller with the 'Set Joint Number' Button. Scroll through the key Poses with the 'Set Joint Transform' slider. Enhance deformation with the 'Select Corrective Smooth Vgroup' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Cheeks
    },
    #Nose
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Nose',
            'ES': 'Nariz'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Nose. Change the active Controller with the 'Set Joint Number' Button. Scroll through the key Poses with the 'Set Joint Transform' slider. Enhance deformation with the 'Select Corrective Smooth Vgroup' Button",
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': WEIGHTS_Char_Nose
    },
    #Mouth
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Mouth',
            'ES': 'Boca'
            },
        'texto': {
            'EN': "Quickly go through the joints cleaning up the Weights of the Mouth area. Move the controllers around to check deformation on the area. Do NOT Paint the Lips with the Corrective Smooth Vertex Group",
            'ES': 'Recorre rápidamente las articulaciones limpiando los pesos de la zona de la boca. Mueve los controladores alrededor para comprobar la deformación del área. NO Pinte los labios en el "Corrective Smooth Vertex Group"'
            },
        'accion': WEIGHTS_Char_Mouth
    },
    #Inner Mouth
    {
        'imagen': 'DT_Finish_A.jpg',
        'titulo': {
            'EN': 'Inner Mouth',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': "Paint the Teeth, Gums, Uvula and Tongue. You might want to enable the Auto Normalize and Face Masks options to clean up intrecate areas. Once things look good, you might need to go back to the previous step in order to paint the inner parts of the cheeks and lips. Alternatively you can activate the 'Show Bones' options to unhide all the deformation bones.",
            'ES': 'Pinte los pesos de los dientes, las encías, la úvula y la lengua. Es posible que quiera activar las opciones de Normalización automática y Máscaras faciales para limpiar las áreas intrecatas. Una vez que las cosas se vean bien, es posible que tenga que volver al paso anterior para pintar las partes internas de las mejillas y los labios. También puedes activar las opciones "Mostrar huesos" para desocultar todos los huesos de la deformación.'
            },
        'accion': WEIGHTS_Char_Inner_Mouth
    },
)





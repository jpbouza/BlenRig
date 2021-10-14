from os.path import dirname, join
from . guide_reproportion_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_REPROPORTION = (
    # Introduction
    {
        'imagen': 'Reprop_Intro.jpg',
        'titulo': {
            'EN': 'Introduction',
            'ES': 'Introducción'
            },
        'texto': {
            'EN': 'This Guide will take you through the process of adjusting the Rig to your Character.',
            'ES': 'Esta guía te llevará a través del proceso de ajuste del Rig a su personaje.'
            },
        'accion': Reprop_Intro
    },
    # Symmetry Step
    {
        'imagen': ('Reprop_Symmetry_A.jpg', 'Reprop_Symmetry_B.jpg'),
        'titulo': {
            'EN': 'Symmetry Option',
            'ES': 'Opcion de Simetria.'
            },
        'texto': {
            'EN': 'If the character is symmetric, please enable the X-Mirror option.',
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror.'
            },
        'accion': Reprop_Symmetry
    },
    # General Scale
    {
        'imagen': ('Reprop_Master_A.jpg', 'Reprop_Master_B.jpg'),
        'titulo': {
            'EN': 'General Scale',
            'ES': 'Escala General'
            },
        'texto': {
            'EN': 'Scale the overall size of the rig so that it better fits the character.',
            'ES': 'Modifica la escala general del rig para que se ajuste más al personaje.'
            },
        'accion': Reprop_Master
    },
    # Master Torso
    {
        'imagen': 'Reprop_Master_Torso.jpg',
        'titulo': {
            'EN': 'Master Torso',
            'ES': 'Torso Principal'
            },
        'texto': {
            'EN': 'Place “master_torso” at the height of hips. It should more or less match the head of the thigh bone.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Master_Torso
    },
    # Spine Joints
    {
        'imagen': 'Reprop_Spine.jpg',
        'titulo': {
            'EN': 'Spine Joints',
            'ES': 'Articulaciones de la columna'
            },
        'texto': {
            'EN': 'Place the hips and spine joints.',
            'ES': 'Alinea la cadera, torso, cuello y cabeza.'
            },
        'accion': Reprop_Spine
    },
    # Spine Line
    {
        'imagen': ('Reprop_Spine_Line_A.jpg', 'Reprop_Spine_Line_B.jpg', 'Reprop_Spine_Line_C.jpg'),
        'titulo': {
            'EN': 'Spine Line Curvature',
            'ES': 'Curvatura de la linea de la columna'
            },
        'texto': {
            'EN': 'Adjust the curve of the Spine Line so that it best matches the shape of the spine bones.',
            'ES': 'Ajusta la curva de la línea de la columna vertebral para que se adapte mejor a la forma de los huesos de la columna.'
            },
        'accion': Reprop_Spine_Line
    },
    # 3 Neck Joints
    {
        'imagen': 'Reprop_Neck.jpg',
        'titulo': {
            'EN': 'Neck Joints',
            'ES': 'Articulacion del cuello'
            },
        'texto': {
            'EN': 'Place the neck and head joints.',
            'ES': 'Coloca las articulaciones del cuello y la cabeza.'
            },
        'accion': Reprop_Neck
    },
    # Head Joints
    {
        'imagen': 'Reprop_Head.jpg',
        'titulo': {
            'EN': 'Head Joints',
            'ES': 'Articulacion de la cabeza'
            },
        'texto': {
            'EN': 'Place the inner head joints, one at the height of the eyes and the other one the height of the base of the nose.',
            'ES': 'Coloca las articulaciones interiores de la cabeza, una a la altura de los ojos y la otra a la altura de la base de la nariz.'
            },
        'accion': Reprop_Head
    },
    # Head Toon
    {
        'imagen': 'Reprop_Head_Toon.jpg',
        'titulo': {
            'EN': 'Head Toon',
            'ES': 'Articulacion de la cabeza'
            },
        'texto': {
            'EN': 'Place the lower and middle Head Toon Controllers.',
            'ES': 'Coloca los controles "Head Toon" inferior y medio.'
            },
        'accion': Reprop_Head_Toon
    },
    # Breasts / Pecs
    {
        'imagen': 'Reprop_Breasts_Pecs.jpg',
        'titulo': {
            'EN': 'Breasts / Pecs',
            'ES': 'Pechos / Pectorales'
            },
        'texto': {
            'EN': 'Place the Breasts bones.',
            'ES': 'Coloca los huesos de los pechos.'
            },
        'accion': Reprop_Breasts_Pecs
    },
    # Body Lattice
    {
        'imagen': 'Reprop_Body_Lattice.jpg',
        'titulo': {
            'EN': 'Body Lattice',
            'ES': 'Deformador Lattice del cuerpo'
            },
        'texto': {
            'EN': 'Place the Lattice controllers for the body.',
            'ES': 'Coloca los controladores Lattice para el cuerpo.'
            },
        'accion': Reprop_Body_Lattice
    },
    # Heel Side
    {
        'imagen': 'Reprop_Sole_Side.jpg',
        'titulo': {
            'EN': 'Heel Side',
            'ES': 'Posicion del talon'
            },
        'texto': {
            'EN': 'First, place the sole bone at the heel of the character. Scale it so that its length matches the length of the foot. Then, position the Foot Roll Controller and the Front Pivot Point.',
            'ES': 'Coloca el hueso de la suela en el talon. Coloca el controlador "Foot Roll" y el "Front Pivot Point".'
            },
        'accion': Reprop_Sole_Side
    },
    # Heel Middle
    {
        'imagen': 'Reprop_Sole_Bottom.jpg',
        'titulo': {
            'EN': 'Heel Middle',
            'ES': 'Tacón medio'
            },
        'texto': {
            'EN': 'Move the sole bone horizontally to place it at the middle of the heel. Adjust the Front Pivot Point. Place foot_ctrl_frame in front of the foot.',
            'ES': 'Mueve el hueso de la suela horizontalmente para colocarlo en el centro del talón. Ajusta el punto de pivote delantero. Coloque "foot_ctrl_frame" delante del pie.'
            },
        'accion': Reprop_Sole_Bottom
    },
    # Foot Side Rolls
    {
        'imagen': 'Reprop_Foot_Side_Rolls.jpg',
        'titulo': {
            'EN': 'Foot Side Rolls',
            'ES': 'Rolls lateral del pie'
            },
        'texto': {
            'EN': 'Make the horizontal roll controllers match the shape of the foot.',
            'ES': 'Haz que los controladores de rotacion horizontal coincidan con el contorno del pie.'
            },
        'accion': Reprop_Foot_Side_Rolls
    },
    # Leg Front
    {
        'imagen': 'Reprop_Legs_Front.jpg',
        'titulo': {
            'EN': 'Leg',
            'ES': 'Pierna'
            },
        'texto': {
            'EN': 'Place the leg joints.',
            'ES': 'Coloca las articulaciones de las piernas.'
            },
        'accion': Reprop_Legs
    },
    # Feet
    {
        'imagen': 'Reprop_Feet.jpg',
        'titulo': {
            'EN': 'Feet',
            'ES': 'Pie'
            },
        'texto': {
            'EN': 'Place the foot joints.',
            'ES': 'Coloca las articulaciones de los pies.'
            },
        'accion': Reprop_Feet
    },
    # Toes
    {
        'imagen': ('Reprop_Toes_A.jpg', 'Reprop_Toes_B.jpg'),
        'titulo': {
            'EN': 'Toes',
            'ES': 'Dedos de los pies'
            },
        'texto': {
            'EN': 'Place the joints of the Toes and the toes_spread controller. You can also disable Toes completely or individually with the Toes Toggles.',
            'ES': 'Coloca las articulaciones de los dedos de los pies y el controlador "toes_spread". También puedes desactivar los dedos de los pies por completo o individualmente con los checkbox de los dedos de los pies.'
            },
        'accion': Reprop_Toes
    },
    # Arms Front
    {
        'imagen': 'Reprop_Arms_Front.jpg',
        'titulo': {
            'EN': 'Arms',
            'ES': 'Brazo hacia adelante'
            },
        'texto': {
            'EN': 'Place the arm joints. You can also scale the wrist controller to give the size of the hand a first approximation.',
            'ES': 'Coloca las articulaciones del brazo. También puedes escalar el control de la muñeca para dar una primera aproximación al tamaño de la mano.'
            },
        'accion': Reprop_Arms
    },
    # hand Joint
    {
        'imagen': 'Reprop_Hands.jpg',
        'titulo': {
            'EN': 'Hand Joint',
            'ES': 'Articulacion de la Mano'
            },
        'texto': {
            'EN': 'Place the hand joint at the root of the fingers.',
            'ES': 'Coloca la articulación de la mano en el inicio de cada uno los dedos.'
            },
        'accion': Reprop_Hands
    },
    # Fingers
    {
        'imagen': ('Reprop_Fingers_A.jpg','Reprop_Fingers_B.jpg'),
        'titulo': {
            'EN': 'Fingers',
            'ES': 'Dedos de las manos'
            },
        'texto': {
            'EN': 'Place the joints of the Fingers, the "fingers_spread" controller and the "hand_close" controller. You can also disable Fingers completely or individually with the Fingers Toggles.',
            'ES': 'Coloca las articulaciones de los dedos, el controlador "fingers_spread" y el controlador "hand_close". También puedes desactivar los dedos por completo o de forma individual con los "checkbox" de los dedos.'
            },
        'accion': Reprop_Fingers
    },
    # Toon Limbs Adjust
    {
        'imagen': ('Reprop_Limbs_Adjust_A.jpg', 'Reprop_Limbs_Adjust_B.jpg'),
        'titulo': {
            'EN': 'Toon Limbs Adjust',
            'ES': 'Escala de deformaciones Toon'
            },
        'texto': {
            'EN': 'Optionally, you can better adjust the deformation bones to the shape of the limbs of the character.',
            'ES': 'Opcionalmente, puedes ajustar mejor los huesos de deformación a la forma de las extremidades del personaje..'
            },
        'accion': Reprop_Limbs_Adjust_Shape
    },
    # Toon Scale
    {
        'imagen': ('Reprop_Toon_Scale_A.jpg', 'Reprop_Toon_Scale_B.jpg', 'Reprop_Toon_Scale_C.jpg', 'Reprop_Toon_Scale_D.jpg'),
        'titulo': {
            'EN': 'Toon Scale',
            'ES': 'Escala de deformaciones Toon'
            },
        'texto': {
            'EN': 'Optionally, you can better adjust the Mesh Deform Cage to your character by scaling the toon controllers.',
            'ES': 'Opcionalmente, puedes ajustar mejor el "Mesh Deform Cage" a la malla a tu personaje escalando los controladores del toon.'
            },
        'accion': Reprop_Toon_Scale
    },
    # Face General Placement
    {
        'imagen': ('Reprop_Face_Mstr_A.jpg', 'Reprop_Face_Mstr_B.jpg', 'Reprop_Face_Mstr_C.jpg', 'Reprop_Face_Mstr_D.jpg'),
        'titulo': {
            'EN': 'Face General Placement',
            'ES': 'Colocacion general de la cara'
            },
        'texto': {
            'EN': 'Use the Face controller to match the Face Mask to the Face of the character as best as possible.',
            'ES': 'Utiliza el controlador de la cara para hacer coincidir la máscara facial con la cara del personaje lo mejor posible.'
            },
        'accion': Reprop_Face_Mstr
    },
    # Face Mask Editting
    {
        'imagen': ('Reprop_Edit_Face_A.jpg', 'Reprop_Edit_Face_B.jpg', 'Reprop_Edit_Face_C.jpg'),
        'titulo': {
            'EN': 'Face Mask Editting',
            'ES': 'Mascara de edicion de la cara'
            },
        'texto': {
            'EN': 'Edit the Face Mask. Snap the vertices to the face of the character. You can toggle between Wire and Textured mode. Textured mode will let you see the different areas of the Face Mask.',
            'ES': 'Edita la máscara facial. Ajusta los vértices a la cara del personaje. Puedes alternar entre el modo de alambre y el de textura. El modo de textura te permitirá ver las diferentes áreas de la máscara facial.'
            },
        'accion': Reprop_Edit_Face
    },
    # Setting Eye Loop
    {
        'imagen': ('Reprop_Eye_Loop_A.jpg', 'Reprop_Eye_Loop_B.jpg'),
        'titulo': {
            'EN': 'Setting Eye Loop',
            'ES': 'Ajuste del loop del ojo'
            },
        'texto': {
            'EN': "Select the character's Left Eye object. Go into Edit Mode and select the Center Loop . Move Cursor to Selection with Shift+S.",
            'ES': 'Selecciona el objeto Ojo Izquierdo del personaje. Vaya al Modo Edición y seleccione el Bucle Central . Mueva el Cursor a la Selección con Shift+S.'
            },
        'accion': Reprop_Eye_Loop
    },
    # Eye Controls Placement Check
    {
        'imagen': ('Reprop_Set_Eyes_A.jpg', 'Reprop_Set_Eyes_B.jpg'),
        'titulo': {
            'EN': 'Eye Controls Placement Check',
            'ES': 'Comprobación de la ubicación de los controles oculares'
            },
        'texto': {
            'EN': 'With the Eye control selected, press the "Snap Eye to Cursor" Button.',
            'ES': 'Con el control del ojo seleccionado, pulse el botón "Snap Eye to Cursor".'
            },
        'accion': Reprop_Set_Eyes
    },
    # Eyebrow Main
    {
        'imagen': 'Reprop_Eyebrows_Main_Ctrl.jpg',
        'titulo': {
            'EN': 'Eyebrow Main',
            'ES': 'Ceja Principal'
            },
        'texto': {
            'EN': 'Place the main controller of the Eyebrow.',
            'ES': 'Coloca el controlador principal de las cejas'
            },
        'accion': Reprop_Eyebrows_Main_Ctrl
    },
    # Eyebrow Curve Ctrls
    {
        'imagen': ('Reprop_Eyebrows_Curve_Ctrls_A.jpg', 'Reprop_Eyebrows_Curve_Ctrls_B.jpg'),
        'titulo': {
            'EN': 'Eyebrow Curve Ctrls',
            'ES': 'Controles de la curva de la ceja'
            },
        'texto': {
            'EN': "Use the Eyebrow's inner and outer controls to place the curve along the Eyebrow arch. Finally, place the Frown controller.",
            'ES': "Utiliza los controles interior y exterior de la ceja para colocar la curva a lo largo del arco de la ceja. Por último, coloque el control de la ceja."
            },
        'accion': Reprop_Eyebrows_Curve_Ctrls
    },
    # Eyebrow Curve
    {
        'imagen': ('Reprop_Eyebrows_Curve_A.jpg', 'Reprop_Eyebrows_Curve_B.jpg', 'Reprop_Eyebrows_Curve_C.jpg'),
        'titulo': {
            'EN': 'Eyebrow Curve',
            'ES': 'Curva de las Cejas'
            },
        'texto': {
            'EN': "Modify the curve values so that the Eyebrow Curve conforms the shape of the character's Eyebrow structure. Then Place the Eyebrow Middle Controller at the center of the Eyebrow Curve.",
            'ES': 'Modifica los valores de la curva para que la Curva de la Ceja se ajuste a la forma de la estructura de la Ceja del personaje. A continuación, coloca el controlador del medio de la ceja en el centro de la curva de la ceja.'
            },
        'accion': Reprop_Eyebrows_Curve
    },
    # Eyebrow Ctrls
    {
        'imagen': 'Reprop_Eyebrows_Ctrls.jpg',
        'titulo': {
            'EN': 'Eyebrow Ctrls',
            'ES': 'Controles de las Cejas'
            },
        'texto': {
            'EN': 'Place the controllers at the center of each joint of the Eyebrow.',
            'ES': 'Coloca los controladores en el centro de cada junta de la ceja.'
            },
        'accion': Reprop_Eyebrows_Ctrls
    },
    # Eyelids Ctrls
    {
        'imagen': 'Reprop_Eyelids_Ctrls.jpg',
        'titulo': {
            'EN': 'Eyelids Ctrls',
            'ES': 'Controles de los Parpados'
            },
        'texto': {
            'EN': 'Place the controllers for the Eyelids.',
            'ES': 'Coloca los controladores para los párpados.'
            },
        'accion': Reprop_Eyelids_Ctrls
    },
    # Eyelids Rim
    {
        'imagen': 'Reprop_Eyelids_Rim_Ctrls.jpg',
        'titulo': {
            'EN': 'Eyelids Rim',
            'ES': 'Borde del párpado'
            },
        'texto': {
            'EN': 'Place the controllers for the Outer Rim of the Eyelids.',
            'ES': 'Coloca los controladores para el borde exterior de los párpados.'
            },
        'accion': Reprop_Eyelids_Rim_Ctrls
    },
    # Facial Toon Ctrls
    {
        'imagen': 'Reprop_Face_Toon.jpg',
        'titulo': {
            'EN': 'Facial Toon Ctrls',
            'ES': 'Controles Faciales Toon'
            },
        'texto': {
            'EN': 'Place the facial toon controllers.',
            'ES': 'Coloca los controladores faciales de toon.'
            },
        'accion': Reprop_Face_Toon
    },
    # Cheek Ctrls
    {
        'imagen': 'Reprop_Cheek_Ctrls.jpg',
        'titulo': {
            'EN': 'Cheek Ctrls',
            'ES': 'Control de la mejilla'
            },
        'texto': {
            'EN': 'Place the controllers for the Cheeks and the Nose Frowns.',
            'ES': 'Coloca los controladores para las mejillas y el ceño de la nariz.'
            },
        'accion': Reprop_Cheek_Ctrls
    },
    # Nose
    {
        'imagen': ('Reprop_Nose_A.jpg', 'Reprop_Nose_B.jpg'),
        'titulo': {
            'EN': 'Nose',
            'ES': 'Nariz'
            },
        'texto': {
            'EN': 'Use the controllers to fit the nose bones to the nose structure of the model. Place the Nostrils controls.',
            'ES': 'Utiliza los controles para ajustar los huesos de la nariz a la estructura de la nariz del modelo. Coloca los controles de las fosas nasales.'
            },
        'accion': Reprop_Nose
    },
    # Jaw
    {
        'imagen': 'Reprop_Jaw.jpg',
        'titulo': {
            'EN': 'Jaw',
            'ES': 'Mandibula'
            },
        'texto': {
            'EN': 'Position the jaw from its joint point to the chin.',
            'ES': 'Coloca la mandíbula desde su punto de unión hasta el mentón.'
            },
        'accion': Reprop_Jaw
    },
    # Lower Face Joint
    {
        'imagen': 'Reprop_Face_Low.jpg',
        'titulo': {
            'EN': 'Lower Face Joint',
            'ES': 'Articulacion inferior de la cara'
            },
        'texto': {
            'EN': 'Place the lower face joint from the base of the nose to the chin. This bone usually goes through the mouth corners, defining an orientation plane for the mouth.',
            'ES': 'Coloca la articulación inferior de la cara desde la base de la nariz hasta el mentón. Este hueso suele pasar por las comisuras de la boca, definiendo un lugar de orientación para la misma.'
            },
        'accion': Reprop_Face_Low
    },
    # Mouth Center & Arch
    {
        'imagen': 'Reprop_Mouth_IK.jpg',
        'titulo': {
            'EN': 'Mouth Center & Arch',
            'ES': 'Centro de la Boca y Arco'
            },
        'texto': {
            'EN': 'Place "mouth_mstr_str" at the center of the mouth. Move "mouth_mstr_ik_pivot" inside of the mouth cavity to define the pivoting point of the arch that makes the lips slide over the teeth.',
            'ES': 'Coloca "mouth_mstr_str" en el centro de la boca. Mueve "mouth_mstr_ik_pivot" dentro de la cavidad bucal para definir el punto de pivote del arco que hace que los labios se deslicen sobre los dientes.'
            },
        'accion': Reprop_Mouth_IK
    },
    # Upper & Lower Lips Centers
    {
        'imagen': 'Reprop_Lips_Centers.jpg',
        'titulo': {
            'EN': 'Upper & Lower Lips Centers',
            'ES': 'Superior e Inferior del centro del labio'
            },
        'texto': {
            'EN': 'Place the upper and lower lips centers.',
            'ES': 'Coloca los centros de los labios superior e inferior.'
            },
        'accion': Reprop_Lips_Centers
    },
    # Mouth Ctrl
    {
        'imagen': 'Reprop_Mouth_Ctrl.jpg',
        'titulo': {
            'EN': 'Mouth Ctrl',
            'ES': 'Controles de la Boca'
            },
        'texto': {
            'EN': 'Place the controller of the mouth where it best fits the character visually. Place the cheek puff controllers.',
            'ES': 'Coloca el controlador de la boca donde mejor se adapte visualmente al personaje. Coloca los controladores de las mejillas.'
            },
        'accion': Reprop_Mouth_Ctrl
    },
    # Lips Curves Ctrls
    {
        'imagen': ('Reprop_Mouth_Curves_Ctrls_A.jpg', 'Reprop_Mouth_Curves_Ctrls_B.jpg'),
        'titulo': {
            'EN': 'Mouth Curves Ctrls',
            'ES': 'Curvas de control de la boca'
            },
        'texto': {
            'EN': 'Use the mouth corner controllers and the middle lips controllers to place the curves along the lips.',
            'ES': 'Utiliza los controladores de las comisuras de la boca y los controladores de los labios centrales para colocar las curvas a lo largo de los labios.'
            },
        'accion': Reprop_Mouth_Curves_Ctrls
    },
    # Lips Curves
    {
        'imagen': ('Reprop_Mouth_Curves_A.jpg', 'Reprop_Mouth_Curves_B.jpg', 'Reprop_Mouth_Curves_C.jpg'),
        'titulo': {
            'EN': 'Lips Curves',
            'ES': 'Curva del labio'
            },
        'texto': {
            'EN': 'Use the curves values to make the upper, middle and lower curves fit the shape of the mouth. Finally place Upper and Lower the Controllers at the Center of the Curves.',
            'ES': 'Utiliza los valores de las curvas para que las curvas superior, media e inferior se ajusten a la forma de la boca. Finalmente coloque los controladores superior e inferior en el centro de las curvas.'
            },
        'accion': Reprop_Mouth_Curves
    },
    # Lips Ctrls
    {
        'imagen': 'Reprop_Mouth_Ctrls.jpg',
        'titulo': {
            'EN': 'Lips Ctrls',
            'ES': 'Controles de labio'
            },
        'texto': {
            'EN': 'Place the lips controllers at the middle of each lip joint.',
            'ES': 'Coloca los controladores de los labios en el centro de cada junta labial.'
            },
        'accion': Reprop_Mouth_Ctrls
    },
    # Mouth Outer Ctrls
    {
        'imagen': 'Reprop_Mouth_Outer_Ctrls.jpg',
        'titulo': {
            'EN': 'Mouth Outer Ctrls',
            'ES': 'Controles Exterior de la Boca'
            },
        'texto': {
            'EN': 'Place the controllers for the first and second outer rings of the mouth.',
            'ES': 'Coloca los controladores para el primer y segundo anillo exterior de la boca.'
            },
        'accion': Reprop_Mouth_Outer_Ctrls
    },
    # Upper Teeth
    {
        'imagen': 'Reprop_Teeth_Up.jpg',
        'titulo': {
            'EN': 'Upper Teeth',
            'ES': 'Dientes Superiores'
            },
        'texto': {
            'EN': 'Move "teeth_up_str" to where the teeth object is and place the Upper Teeth controls.',
            'ES': 'Mueve "teeth_up_str" hasta donde está el objeto de los dientes y coloca los controles de los dientes superiores.'
            },
        'accion': Reprop_Teeth_Up
    },
    # Lower Teeth
    {
        'imagen': 'Reprop_Teeth_Low.jpg',
        'titulo': {
            'EN': 'Lower Teeth',
            'ES': 'Dientes inferiores'
            },
        'texto': {
            'EN': 'Move "teeth_low_str" to where the teeth object is and place the Lower Teeth controls.',
            'ES': 'Mueve "teeth_low_str" hasta donde está el objeto de los dientes y coloca los controles de los dientes inferiores.'
            },
        'accion': Reprop_Teeth_Low
    },
    # Tongue
    {
        'imagen': 'Reprop_Tongue.jpg',
        'titulo': {
            'EN': 'Tongue',
            'ES': 'Lengua'
            },
        'texto': {
            'EN': 'Move "tongue_str" to the root of the tongue object and place the controllers along the tongue.',
            'ES': 'Mueve "tongue_str" al comienzo del objeto lengua y coloca los controladores a lo largo de la lengua.'
            },
        'accion': Reprop_Tongue
    },
    # Inner Mouth
    {
        'imagen': 'Reprop_Inner_Mouth.jpg',
        'titulo': {
            'EN': 'Inner Mouth',
            'ES': 'Interior de la Boca'
            },
        'texto': {
            'EN': 'Place the inner mouth area controllers.',
            'ES': 'Coloca los controladores de la zona interior de la boca.'
            },
        'accion': Reprop_Inner_Mouth
    },
    # Ears
    {
        'imagen': 'Reprop_Ears.jpg',
        'titulo': {
            'EN': 'Ears',
            'ES': 'Orejas'
            },
        'texto': {
            'EN': 'Place the Ears controllers.',
            'ES': 'Coloca los controladores de las orejas.'
            },
        'accion': Reprop_Ears
    },
    # Hat & Glasses
    {
        'imagen': 'Reprop_Hat_Glasses.jpg',
        'titulo': {
            'EN': 'Hat & Glasses',
            'ES': 'Sombrero y Gafas'
            },
        'texto': {
            'EN': 'Place the Hat and Glasses pivot controllers.',
            'ES': 'Coloca los controladores de pivote del sombrero y las gafas.'
            },
        'accion': Reprop_Hat_Glasses
    },
    # Look
    {
        'imagen': ('Reprop_Look_A.jpg', 'Reprop_Look_B.jpg'),
        'titulo': {
            'EN': 'Look',
            'ES': 'Control de la mirada'
            },
        'texto': {
            'EN': 'Place the Look controller. Scale it to fit the width of the eyes.',
            'ES': 'Coloca el controlador de la mirada. Escálalo para que se ajuste a la anchura de los ojos.'
            },
        'accion': Reprop_Look
    },
    # Bake
    {
        'imagen': 'Reprop_Bake.jpg',
        'titulo': {
            'EN': 'Bake Rig',
            'ES': 'Bake Rig'
            },
        'texto': {
            'EN': 'Press the Bake button to bake the current state of the rig and the deformation objects.',
            'ES': 'Pulse el botón Bake para bakear el estado actual del rig y los objetos de deformación.'
            },
        'accion': Reprop_Bake
    },
    # Custom Alignments
    {
        'imagen': 'Reprop_Custom_Alignments.jpg',
        'titulo': {
            'EN': 'Custom Alignments',
            'ES': 'Alineaciones personalizadas'
            },
        'texto': {
            'EN': 'Check the bone roll orientations and press the Custom Alignments Button.',
            'ES': 'Comprueba las orientaciones de los "bone roll" y pulse el botón "Custom Alignments".'
            },
        'accion': Reprop_Custom_Alignments
    },
    # Ik Check
    {
        'imagen': 'Reprop_Custom_Alignments.jpg',
        'titulo': {
            'EN': 'IK Check',
            'ES': 'Alineaciones personalizadas'
            },
        'texto': {
            'EN': "Move the controllers and check that the limbs bend correcly. In case the arms or legs don't bend, Use the 'IK Rotation Override' Sliders to make them bend.",
            'ES': 'Mueve los controladores y comprueba que las extremidades se doblan correctamente. En caso de que los brazos o las piernas no se doblen, utiliza los deslizadores de "IK Rotation Override" para que se doblen.'
            },
        'accion': Reprop_IK_Check
    },
    # Reproportion Finish
    {
        'imagen': 'Reprop_Finish.jpg',
        'titulo': {
            'EN': 'Reproportion Finish',
            'ES': 'Reproporcion Finalizada'
            },
        'texto': {
            'EN': "You're done with Reproportion. Now start the 'Weights Transfer Guide'.",
            'ES': 'Has terminado con la Reproporción. Ahora comienza la "Guía de Transferencia de Pesos".'
            },
        'accion': Reprop_Finish
    }
)



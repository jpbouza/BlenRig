from os.path import dirname, join
from . guide_reproportion_actions import *

images_dir = join(dirname(__file__), 'images')

GUIDE_STEPS_REPROPORTION = (
    # Symmetry Step
    {
        'imagen': ('Reprop_Symmetry_A.jpg', 'Reprop_Symmetry_B.jpg'),
        'titulo': {
            'EN': 'Symmetry Option',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': 'If the character is symmetric, please enable the X-Mirror option.',
            'ES': 'Si el personaje es simétrico, activa la opción X-Mirror'
            },
        'accion': Reprop_Symmetry
    },
    # General Scale
    {
        'imagen': ('Reprop_Master_A.jpg', 'Reprop_Master_B.jpg'),
        'titulo': {
            'EN': 'General Scale',
            'ES': 'Paso 1'
            },
        'texto': {
            'EN': 'Scale the overall size of the rig so that it better fits the character.',
            'ES': 'Modifica la escala general del rig para que se ajuste más al personaje'
            },
        'accion': Reprop_Master
    },
    # Master Torso
    {
        'imagen': 'Reprop_Master_Torso.jpg',
        'titulo': {
            'EN': 'Master Torso',
            'ES': 'Paso 1'
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
            'ES': 'Paso 2'
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
            'ES': 'Paso 2'
            },
        'texto': {
            'EN': 'Adjust the curve of the Spine Line so that it best matches the shape of the spine bones.',
            'ES': 'Alinea la cadera, torso, cuello y cabeza.'
            },
        'accion': Reprop_Spine_Line
    },
    # 3 Neck Joints
    {
        'imagen': 'Reprop_Neck.jpg',
        'titulo': {
            'EN': 'Neck Joints',
            'ES': 'Paso 3'
            },
        'texto': {
            'EN': 'Place the neck and head joints.',
            'ES': 'Mueva el cursor 3d al centro del globo ocular.' # 'Determinar el centro del globo ocular. Mover el cursor 3d a esa posición.'
            },
        'accion': Reprop_Neck
    },
    # Head Joints
    {
        'imagen': 'Reprop_Head.jpg',
        'titulo': {
            'EN': 'Head Joints',
            'ES': 'Paso 4'
            },
        'texto': {
            'EN': 'Place the inner head joints, one at the height of the eyes and the other one the height of the base of the nose.',
            'ES': 'Posiciona los controles de los ojos como se muestra en la imagen.'
            },
        'accion': Reprop_Head
    },
    # Breasts / Pecs
    {
        'imagen': 'Reprop_Breasts_Pecs.jpg',
        'titulo': {
            'EN': 'Breasts / Pecs',
            'ES': 'Paso 2'
            },
        'texto': {
            'EN': 'Place the Beasts bones',
            'ES': 'Alinea la cadera, torso, cuello y cabeza.'
            },
        'accion': Reprop_Breasts_Pecs
    },
    # Body Lattice
    {
        'imagen': 'Reprop_Body_Lattice.jpg',
        'titulo': {
            'EN': 'Body Lattice',
            'ES': 'Paso 2'
            },
        'texto': {
            'EN': 'Place the Lattice controllers for the body',
            'ES': 'Alinea la cadera, torso, cuello y cabeza.'
            },
        'accion': Reprop_Body_Lattice
    },
    # Heel Side
    {
        'imagen': 'Reprop_Sole_Side.jpg',
        'titulo': {
            'EN': 'Heel Side',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the sole bone at the heel. Position the Foot Roll Controller and the Front Pivot Point.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Sole_Side
    },
    # Heel Middle
    {
        'imagen': 'Reprop_Sole_Bottom.jpg',
        'titulo': {
            'EN': 'Heel Middle',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Move the sole bone horizontaly to place it at the middle of the heel. Adjust the Front Pivot Point. Place foot_ctrl_frame in front of the foot.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Sole_Bottom
    },
    # Foot Side Rolls
    {
        'imagen': 'Reprop_Foot_Side_Rolls.jpg',
        'titulo': {
            'EN': 'Foot Side Rolls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Make the horizontal roll controllers match the shape of the foot.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Foot_Side_Rolls
    },
    # Leg Front
    {
        'imagen': 'Reprop_Legs_Front.jpg',
        'titulo': {
            'EN': 'Leg Front',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the leg joints, front view.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Legs_Front
    },
    # Leg Side
    {
        'imagen': 'Reprop_Legs_Side.jpg',
        'titulo': {
            'EN': 'Leg Side',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the leg joints, side view.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Legs_Side
    },
    # Feet
    {
        'imagen': 'Reprop_Feet.jpg',
        'titulo': {
            'EN': 'Feet',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the foot joints.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Feet
    },
    # Toes
    {
        'imagen': 'Reprop_Toes.jpg',
        'titulo': {
            'EN': 'Toes',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'If your character has toes, place the toes joints, otherwise, toggle toes off.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Toes
    },
    # Arms Front
    {
        'imagen': 'Reprop_Arms_Front.jpg',
        'titulo': {
            'EN': 'Arms Front',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the arm joints, front view.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Arms_Front
    },
    # Arms Side
    {
        'imagen': 'Reprop_Arms_Side.jpg',
        'titulo': {
            'EN': 'Arms Side',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the arm joints, side view.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Arms_Side
    },
    # hand Joint
    {
        'imagen': 'Reprop_Hands.jpg',
        'titulo': {
            'EN': 'Hand Joint',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the hand joint at the root of the fingers.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Hands
    },
    # Fingers
    {
        'imagen': 'Reprop_Fingers.jpg',
        'titulo': {
            'EN': 'Fingers',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'If your character has fingers, place the finger joints, otherwise, toggle fingers off.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Fingers
    },
    # Toon Scale
    {
        'imagen': ('Reprop_Toon_Scale_A.jpg', 'Reprop_Toon_Scale_B.jpg', 'Reprop_Toon_Scale_C.jpg', 'Reprop_Toon_Scale_D.jpg'),
        'titulo': {
            'EN': 'Toon Scale',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Optionally, you can better adjust the Mesh Deform Cage to your character by scaling the toon controllers.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Toon_Scale
    },
    # Face General Placement
    {
        'imagen': ('Reprop_Face_Mstr_A.jpg', 'Reprop_Face_Mstr_B.jpg', 'Reprop_Face_Mstr_C.jpg', 'Reprop_Face_Mstr_D.jpg'),
        'titulo': {
            'EN': 'Face General Placement',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Use the Face controller to match the Face Mask to the Face of the character as best as possible.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Face_Mstr
    },
    # Face Mask Editting
    {
        'imagen': ('Reprop_Edit_Face_A.jpg', 'Reprop_Edit_Face_B.jpg', 'Reprop_Edit_Face_C.jpg'),
        'titulo': {
            'EN': 'Face Mask Editting',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Edit the Face Mask. Snap the vertices to the face of the character. Toggle Between Wire and Solid mode to see the area of the face.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Edit_Face
    },
    # Setting Eye Loop
    {
        'imagen': ('Reprop_Eye_Loop_A.jpg', 'Reprop_Eye_Loop_B.jpg'),
        'titulo': {
            'EN': 'Setting Eye Loop',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': "Pick the character's left eye object and in Edit mode select the Center Loop. Move Cursor to Selection with Shift+S.",
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eye_Loop
    },
    # Eye Controls Placement Check
    {
        'imagen': 'Reprop_Set_Eyes.jpg',
        'titulo': {
            'EN': 'Eye Controls Placement Check',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Eye controls should now match the center of the eyes. Move to the next step.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Set_Eyes
    },
    # Eyebrow Main
    {
        'imagen': 'Reprop_Eyebrows_Main_Ctrl.jpg',
        'titulo': {
            'EN': 'Eyebrow Main',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the main controller of the Eyebrow.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eyebrows_Main_Ctrl
    },
    # Eyebrow Curve Ctrls
    {
        'imagen': ('Reprop_Eyebrows_Curve_Ctrls_A.jpg', 'Reprop_Eyebrows_Curve_Ctrls_B.jpg'),
        'titulo': {
            'EN': 'Eyebrow Curve Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': "Use the Eyebrow's inner and outer controls to place the curve along the Eyebrow arch. Finally, place the middle controller.",
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eyebrows_Curve_Ctrls
    },
    # Eyebrow Curve
    {
        'imagen': ('Reprop_Eyebrows_Curve_A.jpg', 'Reprop_Eyebrows_Curve_B.jpg', 'Reprop_Eyebrows_Curve_C.jpg'),
        'titulo': {
            'EN': 'Eyebrow Curve',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': "Modify the curve values so that the Curve conforms the shape of the character's Eyebrow structure.",
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eyebrows_Curve
    },
    # Eyebrow Ctrls
    {
        'imagen': 'Reprop_Eyebrows_Ctrls.jpg',
        'titulo': {
            'EN': 'Eyebrow Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the controllers at the center of each joint of the Eyebrow.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eyebrows_Ctrls
    },
    # Eyelids Ctrls
    {
        'imagen': 'Reprop_Eyelids_Ctrls.jpg',
        'titulo': {
            'EN': 'Eyelids Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the controllers for the Eyelids.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eyelids_Ctrls
    },
    # Eyelids Rim
    {
        'imagen': 'Reprop_Eyelids_Rim_Ctrls.jpg',
        'titulo': {
            'EN': 'Eyelids Rim',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the controllers for the Outer Rim of the Eyelids.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Eyelids_Rim_Ctrls
    },
    # Facial Toon Ctrls
    {
        'imagen': 'Reprop_Face_Toon.jpg',
        'titulo': {
            'EN': 'Facial Toon Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the facial toon controllers.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Face_Toon
    },
    # Cheek Ctrls
    {
        'imagen': 'Reprop_Cheek_Ctrls.jpg',
        'titulo': {
            'EN': 'Cheek Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the controllers for the Cheeks and the Nose Frowns',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Cheek_Ctrls
    },
    # Nose
    {
        'imagen': ('Reprop_Nose_A.jpg', 'Reprop_Nose_B.jpg'),
        'titulo': {
            'EN': 'Nose',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Use the controllers to fit the nose bones to the nose structure of the model. Place the Nostrils controls.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Nose
    },
    # Jaw
    {
        'imagen': 'Reprop_Jaw.jpg',
        'titulo': {
            'EN': 'Jaw',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Position the jaw from its joint point to the chin.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Jaw
    },
    # Lower Face Joint
    {
        'imagen': 'Reprop_Face_Low.jpg',
        'titulo': {
            'EN': 'Lower Face Joint',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the lower face joint from the base of the nose to the chin. This bone usually goes through the mouth corners, defining an orientation place for the mouth.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Face_Low
    },
    # Mouth Center & Arch
    {
        'imagen': 'Reprop_Mouth_IK.jpg',
        'titulo': {
            'EN': 'Mouth Center & Arch',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place "mouth_mstr_str" at the center of the mouth. Move "mouth_mstr_ik_pivot" inside of the mouth cavity to define the pivoting point of the arch that makes the lips slide over the teeth.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Mouth_IK
    },
    # Upper & Lower Lips Centers
    {
        'imagen': 'Reprop_Lips_Centers.jpg',
        'titulo': {
            'EN': 'Upper & Lower Lips Centers',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the upper and lower lips centers',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Lips_Centers
    },
    # Mouth Ctrl
    {
        'imagen': 'Reprop_Mouth_Ctrl.jpg',
        'titulo': {
            'EN': 'Mouth Ctrl',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the controller of the mouth where it best visually fits the character. Place the cheek puff controllers.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Mouth_Ctrl
    },
    # Lips Curves Ctrls
    {
        'imagen': ('Reprop_Mouth_Curves_Ctrls_A.jpg', 'Reprop_Mouth_Curves_Ctrls_B.jpg'),
        'titulo': {
            'EN': 'Mouth Curves Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Use the mouth corner controllers and the middle lips controllers to place the curves along the lips.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Mouth_Curves_Ctrls
    },
    # Lips Curves
    {
        'imagen': ('Reprop_Mouth_Curves_A.jpg', 'Reprop_Mouth_Curves_B.jpg'),
        'titulo': {
            'EN': 'Lips Curves',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Use the curves values to make the upper, middle and lower curves fit the shape of the mouth.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Mouth_Curves
    },
    # Lips Ctrls
    {
        'imagen': 'Reprop_Mouth_Ctrls.jpg',
        'titulo': {
            'EN': 'Lips Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the lips controllers at the middle of each lip joint.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Mouth_Ctrls
    },
    # Mouth Outer Ctrls
    {
        'imagen': 'Reprop_Mouth_Outer_Ctrls.jpg',
        'titulo': {
            'EN': 'Mouth Outer Ctrls',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the controllers for the first and second outer rings of the mouth.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Mouth_Outer_Ctrls
    },
    # Upper Teeth
    {
        'imagen': 'Reprop_Teeth_Up.jpg',
        'titulo': {
            'EN': 'Upper Teeth',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Move "teeth_up_str" to where the teeth object is and place the Upper Teeth controls.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Teeth_Up
    },
    # Lower Teeth
    {
        'imagen': 'Reprop_Teeth_Low.jpg',
        'titulo': {
            'EN': 'Lower Teeth',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Move "teeth_low_str" to where the teeth object is and place the Lower Teeth controls.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Teeth_Low
    },
    # Tongue
    {
        'imagen': 'Reprop_Tongue.jpg',
        'titulo': {
            'EN': 'Tongue',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Move "tongue_str" to the root of the tongue object and place the controllers along the tongue',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Tongue
    },
    # Inner Mouth
    {
        'imagen': 'Reprop_Inner_Mouth.jpg',
        'titulo': {
            'EN': 'Inner Mouth',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the inner mouth area controllers',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Inner_Mouth
    },
    # Ears
    {
        'imagen': 'Reprop_Ears.jpg',
        'titulo': {
            'EN': 'Ears',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the Ears controllers.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Ears
    },
    # Hat & Glasses
    {
        'imagen': 'Reprop_Hat_Glasses.jpg',
        'titulo': {
            'EN': 'Hat & Glasses',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the Hat and Glasses pivot controllers.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Hat_Glasses
    },
    # Look
    {
        'imagen': ('Reprop_Look_A.jpg', 'Reprop_Look_B.jpg'),
        'titulo': {
            'EN': 'Look',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Place the Look controller. Scale it to fit the width of the eyes.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Look
    },
    # Bake
    {
        'imagen': 'Reprop_Bake.jpg',
        'titulo': {
            'EN': 'Bake Rig',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Press the Bake button to bake the current state of the rig and the deformation objects.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Bake
    },
    # Custom Alignments
    {
        'imagen': 'Reprop_Custom_Alignments.jpg',
        'titulo': {
            'EN': 'Custom Alignments',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'Check the bone roll orientations and press the Custom Alignments Button.',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Custom_Alignments
    },
    # Reproportion Finish
    {
        'imagen': 'Reprop_Finish.jpg',
        'titulo': {
            'EN': 'Reproportion Finish',
            'ES': 'Paso 5'
            },
        'texto': {
            'EN': 'End of Reproportion process. You can now start the deformation setup process',
            'ES': 'Coloca “master_torso” a la altura de las caderas.'
            },
        'accion': Reprop_Finish
    }
)

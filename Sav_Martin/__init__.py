
import bpy, os

bl_info = {
    "name": "Martin",
    "author": "Sav Martin, Jorge Hernandez Melendez",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Martin",
    }

from bpy.props import (BoolProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)

########################## FACIAL ##################################
g_FACIAL = ['FACIAL_MAIN_MID',
            'STR_FACE',
            'FACIAL_MAIN_R',
            'FACIAL_MAIN_L',
            'FACIAL_MID',
            'FACIAL_MID',
            'FACIAL_R',
            'FACIAL_L']

g_FACIAL_EXTRAS = ('chin_ctrl_mid',
                   'lip_low_outer_ctrl_mid',
                   'nose_bridge_ctrl_2',
                   'nose_root_ctrl_mid',
                   'frown_ctrl'
                   )

####################### LIPS ####################################

g_LIPS = ['STR_LIPS']
g_LIPS_EXTRAS = ('lip_low_rim_ctrl_mid',
                 'lip_low_line_ctrl_mid',
                 'lip_up_rim_ctrl_mid',
                 'lip_up_line_ctrl_mid',
                 
                 'lip_low_rim_ctrl_1_L',
                 'lip_low_rim_ctrl_2_L',
                 'lip_low_rim_ctrl_3_L',
                 'lip_low_rim_ctrl_1_R',
                 'lip_low_rim_ctrl_2_R',
                 'lip_low_rim_ctrl_3_R',

                 'lip_up_rim_ctrl_1_L',
                 'lip_up_rim_ctrl_2_L',
                 'lip_up_rim_ctrl_3_L',
                 'lip_up_rim_ctrl_4_L',
                 'lip_up_rim_ctrl_1_R',
                 'lip_up_rim_ctrl_2_R',
                 'lip_up_rim_ctrl_3_R',
                 'lip_up_rim_ctrl_4_R',
                 
                 'lip_low_line_ctrl_1_L',
                 'lip_low_line_ctrl_2_L',
                 'lip_low_line_ctrl_3_L',
                 'lip_low_line_ctrl_1_R',
                 'lip_low_line_ctrl_2_R',
                 'lip_low_line_ctrl_3_R',

                 'lip_up_line_ctrl_1_L',
                 'lip_up_line_ctrl_2_L',
                 'lip_up_line_ctrl_3_L',
                 'lip_up_line_ctrl_4_L',
                 'lip_up_line_ctrl_1_R',
                 'lip_up_line_ctrl_2_R',
                 'lip_up_line_ctrl_3_R',
                 'lip_up_line_ctrl_4_R',
)

############################## FACE CONTROLS ############################

g_FACE_CONTROLS = ('mouth_corner_L',
                   'mouth_corner_R',
                   'mouth_frown_ctrl_L',
                   'mouth_frown_ctrl_R',
                   'cheek_ctrl_L',
                   'cheek_ctrl_R',
                   'nose_frown_ctrl_L',
                   'nose_frown_ctrl_R',
                   'eyelid_up_ctrl_L',
                   'eyelid_up_ctrl_R',
                   'eyelid_low_ctrl_L',
                   'eyelid_low_ctrl_R',
                   'cheek_puff_mstr_L',
                   'cheek_puff_mstr_R',
                   'cheek_puff_ctrl_L',
                   'cheek_puff_ctrl_R',
                   'eyelid_up_rim_ctrl_L',
                   'eyelid_up_rim_ctrl_R',
                   'old_eyelid_up_ctrl_L',
                   'old_eyelid_up_ctrl_R',
                   'old_eyelid_low_rim_ctrl_L',
                   'old_eyelid_low_rim_ctrl_R',
                   'old_eyelid_low_ctrl_L',
                   'old_eyelid_low_ctrl_R'
                   )

############################## EYES #####################################

g_EYES = ('STR_EYES')

############################## EYEBROWS ############################

g_EYEBROWS = ('STR_EYEBROWS')

############################## FACE MECH ############################

g_STR_FACE_MECH = ('STR_FACE_MECH')
g_FACE_MECH_EXTRA = ('lip_low_ctrl_collision',
                     'lip_up_ctrl_collision'
                    )
############################## INNER MOUTH ############################

g_STR_INNER_MOUTH = ('STR_INNER_MOUTH')

############################## HANDS ############################

g_STR_HANDS = ('STR_HANDS')

############################## REST ############################

g_STR = ('STR','GEN','IK_L','IK_R','PIVOT_POINTS')

ex_huesos= ('brow_ctrl_3_L',
            'brow_ctrl_2_L',
            'brow_ctrl_1_L',
            'brow_ctrl_4_L',
            'brow_ctrl_5_L',
            'brow_ctrl_3_R',
            'brow_ctrl_2_R',
            'brow_ctrl_1_R',
            'brow_ctrl_4_R',
            'brow_ctrl_5_R')


############################## BODY ############################

g_BODY = ('neck_1_def',
        'neck_2_def',
        'neck_3_def',
        'head_def_mstr',
        'head_def_2',
        'head_def_3',
        'head_def_1',
        'thigh_twist_def_L',
        'foot_def_L',
        'shin_def_L',
        'shin_twist_def_L',
        'thigh_twist_def_R',
        'foot_def_R',
        'shin_def_R',
        'shin_twist_def_R',
        'arm_twist_def_L',
        'hand_def_L',
        'forearm_twist_def_L',
        'forearm_def_L',
        'arm_twist_def_R',
        'hand_def_R',
        'forearm_twist_def_R',
        'forearm_def_R',
        'knee_line_L',
        'knee_line_R',
        'pelvis_def',
        'pelvis_def_L',
        'thigh_def_L',
        'pelvis_def_R',
        'thigh_def_R',
        'spine_1_def',
        'spine_2_def',
        'elbow_line_R',
        'clavi_def_R',
        'arm_def_R',
        'elbow_line_L',
        'clavi_def_L',
        'arm_def_L',
        'spine_3_def',
        'mouth_mstr_ik_copy_loc',
        'foot_toe_2_def_L',
        'foot_toe_1_def_L',
        'foot_toe_2_def_R',
        'foot_toe_1_def_R',
        'neck_1_def.001',
        'neck_2_def.001',
        'neck_3_def.001'
        )

############################## FUNCIONS ############################

def get_bones_from_group(target):
    arm_name =bpy.context.active_object.name
    armature = bpy.data.objects[arm_name]
    grupo_target = armature.pose.bone_groups[target]
    bones = []
    for b in armature.pose.bones:
        if b.bone_group == grupo_target:
            bones.append(b)
    return bones

def show_eyes(self, context):
    
    if bpy.context.scene.ccb.eyes:
        huesos = get_bones_from_group(g_EYES)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_EYES)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True

def show_face(self, context):
    if bpy.context.scene.ccb.face:
        for g in g_FACIAL:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False
        for h in g_FACIAL_EXTRAS:
                bpy.context.object.data.bones[h].hide = False
    else:
        for g in g_FACIAL:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True
        for h in g_FACIAL_EXTRAS:
                bpy.context.object.data.bones[h].hide = True

def show_lips(self, context):
    if bpy.context.scene.ccb.lips:
        for h in g_LIPS_EXTRAS:
            bpy.context.object.data.bones[h].hide = False
        
        for g in g_LIPS:
            huesos = get_bones_from_group(g)
            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False
    else:
        for g in g_LIPS:
            huesos = get_bones_from_group(g)
            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True
            
        for h in g_LIPS_EXTRAS:
            bpy.context.object.data.bones[h].hide = True

def show_eyebrows(self, context):
    if bpy.context.scene.ccb.eyebrows:
        huesos = get_bones_from_group(g_EYEBROWS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
        for h in ex_huesos:
            bpy.context.object.data.bones[h].hide = False
    else:        
        huesos = get_bones_from_group(g_EYEBROWS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True
        for h in ex_huesos:
            bpy.context.object.data.bones[h].hide = True

def show_face_mech(self, context):
    if bpy.context.scene.ccb.face_mech:
        huesos = get_bones_from_group(g_STR_FACE_MECH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
        for h in g_FACE_MECH_EXTRA :
            bpy.context.object.data.bones[h].hide = False

    else:
        huesos = get_bones_from_group(g_STR_FACE_MECH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True
        for h in g_FACE_MECH_EXTRA :
            bpy.context.object.data.bones[h].hide = True

def show_inner_mouth(self, context):
    if bpy.context.scene.ccb.inner_mouth:
        huesos = get_bones_from_group(g_STR_INNER_MOUTH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_INNER_MOUTH)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True

def show_hands(self, context):
    if bpy.context.scene.ccb.hands:
        huesos = get_bones_from_group(g_STR_HANDS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = False
    else:
        huesos = get_bones_from_group(g_STR_HANDS)
        for h in huesos:
            bpy.context.object.data.bones[h.name].hide = True

def show_body(self, context):
    if bpy.context.scene.ccb.body:
        for g in g_STR:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = False 

        for h in g_BODY:
            bpy.context.object.data.bones[h].hide = False
    else:
        for g in g_STR:
            huesos = get_bones_from_group(g)

            for h in huesos:
                bpy.context.object.data.bones[h.name].hide = True 
        
        for h in g_BODY:
            bpy.context.object.data.bones[h].hide = True

def show_face_controls(self, context):
    if bpy.context.scene.ccb.face_controls:
        for h in g_FACE_CONTROLS :
            bpy.context.object.data.bones[h].hide = False
    else:
        for h in g_FACE_CONTROLS :
            bpy.context.object.data.bones[h].hide = True

r_side= []
def show_right_side (self, context):     
    if bpy.context.scene.ccb.right_side:                   
        for bone in bpy.context.visible_pose_bones:
            if bone.name.endswith("_R"):
                r_side.append(bone.name)

        for bones_r in r_side:
            bpy.context.object.data.bones[bones_r].hide = True
        for bone in bpy.context.visible_pose_bones:
            if bone.name.endswith("_R"):
                r_side.remove(bone.name)

    else: 
        for bones_r in r_side:
            bpy.context.object.data.bones[bones_r].hide = False
        for bone in bpy.context.visible_pose_bones:
            if bone.name.endswith("_R"):
                r_side.remove(bone.name)

l_side= []
def show_left_side (self, context):
    if bpy.context.scene.ccb.left_side:                   
        for bone in bpy.context.visible_pose_bones:
            if bone.name.endswith("_L"):
                l_side.append(bone.name)

        for bones_l in l_side:
            bpy.context.object.data.bones[bones_l].hide = True
        for bone in bpy.context.visible_pose_bones:
            if bone.name.endswith("_L"):
                l_side.remove(bone.name)

    else: 
        for bones_l in l_side:
            bpy.context.object.data.bones[bones_l].hide = False
        for bone in bpy.context.visible_pose_bones:
            if bone.name.endswith("_L"):
                l_side.remove(bone.name)

############################## PROPERTIES ############################

class myProperties(PropertyGroup):
    eyes : BoolProperty(
        name="eyes", 
        default=True, 
        update=show_eyes
        )

    face : BoolProperty(
        name="face", 
        default=True, 
        update=show_face
        )

    eyebrows : BoolProperty(
            name="eyebrows", 
            default=True, 
            update=show_eyebrows
            )

    face_mech : BoolProperty(
            name="face_mech", 
            default=True, 
            update=show_face_mech
            )

    inner_mouth : BoolProperty(
            name="inner_mouth", 
            default=True, 
            update=show_inner_mouth
            )

    hands : BoolProperty(
            name="hands", 
            default=True, 
            update=show_hands
            )
    body : BoolProperty(
            name="body", 
            default=True, 
            update=show_body
            )

    left_side : BoolProperty(
            name="left_side", 
            default=False, 
            update=show_left_side
            )

    right_side : BoolProperty(
            name="right_side", 
            default=False, 
            update=show_right_side
            )
    lips : BoolProperty(
            name="lips", 
            default=True, 
            update=show_lips
            )
    face_controls : BoolProperty(
            name="face_controls", 
            default=True, 
            update=show_face_controls
            )

############################## PANEL ############################

class CYCLES_PT_color_bleeding(Panel):
    bl_label = "Reproportion visual helper"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            for prop in bpy.context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in bpy.context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ccb = scene.ccb

        row = layout.row(align=True)
        box = layout.column()
        col = box.column()
        box = col.box()
        row = box.row()

        row.prop(ccb, "right_side", text="R_Side")
        row.prop(ccb, "left_side", text="L_Side")        
        

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.eyes else 'HIDE_OFF'
        row.prop(ccb, "eyes", icon= icon , text="", toggle=True)
        row.label(text = "EYES")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.face else 'HIDE_OFF'
        row.prop(ccb, "face", icon=icon , text="", toggle=True)
        row.label(text = "FACE")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.face_controls else 'HIDE_OFF'
        row.prop(ccb, "face_controls", icon=icon , text="", toggle=True)
        row.label(text = "FACE CONTROLS")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.lips else 'HIDE_OFF'
        row.prop(ccb, "lips", icon=icon , text="", toggle=True)
        row.label(text = "LIPS")  

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.eyebrows else 'HIDE_OFF'
        row.prop(ccb, "eyebrows", icon=icon, text="", toggle=True)
        row.label(text = "EYEBROWS")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.face_mech else 'HIDE_OFF'
        row.prop(ccb, "face_mech", icon=icon, text="", toggle=True)
        row.label(text = "FACE MECH")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.inner_mouth else 'HIDE_OFF'
        row.prop(ccb, "inner_mouth", icon=icon, text="", toggle=True)
        row.label(text = "INNER MOUTH")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.hands else 'HIDE_OFF'
        row.prop(ccb, "hands", icon=icon, text="", toggle=True)
        row.label(text = "HANDS")

        row = layout.row(align=True)
        icon = 'HIDE_ON' if not ccb.body else 'HIDE_OFF'
        row.prop(ccb, "body", icon=icon, text="", toggle=True)
        row.label(text = "BODY")


############################## REGISTER/UNREGISTER ############################

all_classes = [
    myProperties,
    CYCLES_PT_color_bleeding,
]

def register():
    from bpy.utils import register_class
    if len(all_classes) > 1:
        for cls in all_classes:
            register_class(cls)
    else:
        register_class(all_classes[0])
    bpy.types.Scene.ccb = bpy.props.PointerProperty(type=myProperties)

def unregister():
    from bpy.utils import unregister_class
    if len(all_classes) > 1:
        for cls in reversed(all_classes):
            unregister_class(cls)
    else:
        unregister_class(all_classes[0])
    del bpy.types.Scene.ccb


if __name__ == "__main__":
    register()
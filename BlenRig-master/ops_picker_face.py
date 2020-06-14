import bpy

from .ops_picker_body import select_op

######### FACE PICKER OPERATORS ###########################################

class Operator_Ear_Up_R(bpy.types.Operator):
    bl_idname = "operator.ear_up_r"
    bl_label = "BlenRig Select ear_up_R"
    bl_description = "ear_up_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ear_up_R")
        return {"FINISHED"}

class Operator_Ear_R(bpy.types.Operator):
    bl_idname = "operator.ear_r"
    bl_label = "BlenRig Select ear_R"
    bl_description = "ear_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ear_R")
        return {"FINISHED"}

class Operator_Ear_Low_R(bpy.types.Operator):
    bl_idname = "operator.ear_low_r"
    bl_label = "BlenRig Select ear_low_R"
    bl_description = "ear_low_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ear_low_R")
        return {"FINISHED"}

class Operator_Brow_Ctrl_4_R(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_4_r"
    bl_label = "BlenRig Select brow_ctrl_4_R"
    bl_description = "brow_ctrl_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_4_R")
        return {"FINISHED"}

class Operator_Brow_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_3_r"
    bl_label = "BlenRig Select brow_ctrl_3_R"
    bl_description = "brow_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_3_R")
        return {"FINISHED"}

class Operator_Brow_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_2_r"
    bl_label = "BlenRig Select brow_ctrl_2_R"
    bl_description = "brow_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_2_R")
        return {"FINISHED"}

class Operator_Brow_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_1_r"
    bl_label = "BlenRig Select brow_ctrl_1_R"
    bl_description = "brow_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_1_R")
        return {"FINISHED"}

class Operator_Brow_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_r"
    bl_label = "BlenRig Select brow_ctrl_R"
    bl_description = "brow_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_R")
        return {"FINISHED"}

class Operator_Toon_Brow_R(bpy.types.Operator):
    bl_idname = "operator.toon_brow_r"
    bl_label = "BlenRig Select toon_brow_R"
    bl_description = "toon_brow_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_brow_R")
        return {"FINISHED"}

class Operator_Ear_Up_L(bpy.types.Operator):
    bl_idname = "operator.ear_up_l"
    bl_label = "BlenRig Select ear_up_L"
    bl_description = "ear_up_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ear_up_L")
        return {"FINISHED"}

class Operator_Ear_L(bpy.types.Operator):
    bl_idname = "operator.ear_l"
    bl_label = "BlenRig Select ear_L"
    bl_description = "ear_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ear_L")
        return {"FINISHED"}

class Operator_Ear_Low_L(bpy.types.Operator):
    bl_idname = "operator.ear_low_l"
    bl_label = "BlenRig Select ear_low_L"
    bl_description = "ear_low_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "ear_low_L")
        return {"FINISHED"}

class Operator_Brow_Ctrl_4_L(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_4_l"
    bl_label = "BlenRig Select brow_ctrl_4_L"
    bl_description = "brow_ctrl_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_4_L")
        return {"FINISHED"}

class Operator_Brow_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_3_l"
    bl_label = "BlenRig Select brow_ctrl_3_L"
    bl_description = "brow_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_3_L")
        return {"FINISHED"}

class Operator_Brow_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_2_l"
    bl_label = "BlenRig Select brow_ctrl_2_L"
    bl_description = "brow_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_2_L")
        return {"FINISHED"}

class Operator_Brow_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_1_l"
    bl_label = "BlenRig Select brow_ctrl_1_L"
    bl_description = "brow_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_1_L")
        return {"FINISHED"}

class Operator_Brow_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.brow_ctrl_l"
    bl_label = "BlenRig Select brow_ctrl_L"
    bl_description = "brow_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "brow_ctrl_L")
        return {"FINISHED"}

class Operator_Toon_Brow_L(bpy.types.Operator):
    bl_idname = "operator.toon_brow_l"
    bl_label = "BlenRig Select toon_brow_L"
    bl_description = "toon_brow_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_brow_L")
        return {"FINISHED"}

class Operator_Frown_Ctrl(bpy.types.Operator):
    bl_idname = "operator.frown_ctrl"
    bl_label = "BlenRig Select frown_ctrl"
    bl_description = "frown_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "frown_ctrl")
        return {"FINISHED"}

class Operator_Nose_Bridge_1_Ctrl(bpy.types.Operator):
    bl_idname = "operator.nose_bridge_1_ctrl"
    bl_label = "BlenRig Select nose_bridge_1_ctrl"
    bl_description = "nose_bridge_1_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nose_bridge_1_ctrl")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_r"
    bl_label = "BlenRig Select eyelid_up_ctrl_R"
    bl_description = "eyelid_up_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_R")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_3_r"
    bl_label = "BlenRig Select eyelid_up_ctrl_3_R"
    bl_description = "eyelid_up_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_3_R")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_2_r"
    bl_label = "BlenRig Select eyelid_up_ctrl_2_R"
    bl_description = "eyelid_up_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_2_R")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_1_r"
    bl_label = "BlenRig Select eyelid_up_ctrl_1_R"
    bl_description = "eyelid_up_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_1_R")
        return {"FINISHED"}

class Operator_Toon_Eye_Out_R(bpy.types.Operator):
    bl_idname = "operator.toon_eye_out_r"
    bl_label = "BlenRig Select toon_eye_out_R"
    bl_description = "toon_eye_out_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_out_R")
        return {"FINISHED"}

class Operator_Toon_Eye_Up_R(bpy.types.Operator):
    bl_idname = "operator.toon_eye_up_r"
    bl_label = "BlenRig Select toon_eye_up_R"
    bl_description = "toon_eye_up_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_up_R")
        return {"FINISHED"}

class Operator_Pupil_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.pupil_ctrl_r"
    bl_label = "BlenRig Select pupil_ctrl_R"
    bl_description = "pupil_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "pupil_ctrl_R")
        return {"FINISHED"}

class Operator_Eye_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.eye_ctrl_r"
    bl_label = "BlenRig Select eye_ctrl_R"
    bl_description = "eye_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eye_ctrl_R")
        return {"FINISHED"}

class Operator_Iris_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.iris_ctrl_r"
    bl_label = "BlenRig Select iris_ctrl_R"
    bl_description = "iris_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "iris_ctrl_R")
        return {"FINISHED"}

class Operator_Toon_Eye_In_R(bpy.types.Operator):
    bl_idname = "operator.toon_eye_in_r"
    bl_label = "BlenRig Select toon_eye_in_R"
    bl_description = "toon_eye_in_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_in_R")
        return {"FINISHED"}

class Operator_Toon_Eye_Low_R(bpy.types.Operator):
    bl_idname = "operator.toon_eye_low_r"
    bl_label = "BlenRig Select toon_eye_low_R"
    bl_description = "toon_eye_low_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_low_R")
        return {"FINISHED"}

class Operator_Eyelid_Ctrl_Out_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_ctrl_out_r"
    bl_label = "BlenRig Select eyelid_ctrl_out_R"
    bl_description = "eyelid_ctrl_out_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_ctrl_out_R")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_3_r"
    bl_label = "BlenRig Select eyelid_low_ctrl_3_R"
    bl_description = "eyelid_low_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_3_R")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_2_r"
    bl_label = "BlenRig Select eyelid_low_ctrl_2_R"
    bl_description = "eyelid_low_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_2_R")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_1_r"
    bl_label = "BlenRig Select eyelid_low_ctrl_1_R"
    bl_description = "eyelid_low_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_1_R")
        return {"FINISHED"}

class Operator_Eyelid_Ctrl_In_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_ctrl_in_r"
    bl_label = "BlenRig Select eyelid_ctrl_in_R"
    bl_description = "eyelid_ctrl_in_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_ctrl_in_R")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_r"
    bl_label = "BlenRig Select eyelid_low_ctrl_R"
    bl_description = "eyelid_low_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_R")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_l"
    bl_label = "BlenRig Select eyelid_up_ctrl_L"
    bl_description = "eyelid_up_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_L")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_3_l"
    bl_label = "BlenRig Select eyelid_up_ctrl_3_L"
    bl_description = "eyelid_up_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_3_L")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_2_l"
    bl_label = "BlenRig Select eyelid_up_ctrl_2_L"
    bl_description = "eyelid_up_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_2_L")
        return {"FINISHED"}

class Operator_Eyelid_Up_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_up_ctrl_1_l"
    bl_label = "BlenRig Select eyelid_up_ctrl_1_L"
    bl_description = "eyelid_up_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_up_ctrl_1_L")
        return {"FINISHED"}

class Operator_Toon_Eye_Out_L(bpy.types.Operator):
    bl_idname = "operator.toon_eye_out_l"
    bl_label = "BlenRig Select toon_eye_out_L"
    bl_description = "toon_eye_out_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_out_L")
        return {"FINISHED"}

class Operator_Toon_Eye_Up_L(bpy.types.Operator):
    bl_idname = "operator.toon_eye_up_l"
    bl_label = "BlenRig Select toon_eye_up_L"
    bl_description = "toon_eye_up_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_up_L")
        return {"FINISHED"}

class Operator_Pupil_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.pupil_ctrl_l"
    bl_label = "BlenRig Select pupil_ctrl_L"
    bl_description = "pupil_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "pupil_ctrl_L")
        return {"FINISHED"}

class Operator_Eye_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.eye_ctrl_l"
    bl_label = "BlenRig Select eye_ctrl_L"
    bl_description = "eye_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eye_ctrl_L")
        return {"FINISHED"}

class Operator_Iris_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.iris_ctrl_l"
    bl_label = "BlenRig Select iris_ctrl_L"
    bl_description = "iris_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "iris_ctrl_L")
        return {"FINISHED"}

class Operator_Toon_Eye_In_L(bpy.types.Operator):
    bl_idname = "operator.toon_eye_in_l"
    bl_label = "BlenRig Select toon_eye_in_L"
    bl_description = "toon_eye_in_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_in_L")
        return {"FINISHED"}

class Operator_Toon_Eye_Low_L(bpy.types.Operator):
    bl_idname = "operator.toon_eye_low_l"
    bl_label = "BlenRig Select toon_eye_low_L"
    bl_description = "toon_eye_low_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "toon_eye_low_L")
        return {"FINISHED"}

class Operator_Eyelid_Ctrl_Out_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_ctrl_out_l"
    bl_label = "BlenRig Select eyelid_ctrl_out_L"
    bl_description = "eyelid_ctrl_out_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_ctrl_out_L")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_3_l"
    bl_label = "BlenRig Select eyelid_low_ctrl_3_L"
    bl_description = "eyelid_low_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_3_L")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_2_l"
    bl_label = "BlenRig Select eyelid_low_ctrl_2_L"
    bl_description = "eyelid_low_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_2_L")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_1_l"
    bl_label = "BlenRig Select eyelid_low_ctrl_1_L"
    bl_description = "eyelid_low_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_1_L")
        return {"FINISHED"}

class Operator_Eyelid_Ctrl_In_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_ctrl_in_l"
    bl_label = "BlenRig Select eyelid_ctrl_in_L"
    bl_description = "eyelid_ctrl_in_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_ctrl_in_L")
        return {"FINISHED"}

class Operator_Eyelid_Low_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.eyelid_low_ctrl_l"
    bl_label = "BlenRig Select eyelid_low_ctrl_L"
    bl_description = "eyelid_low_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "eyelid_low_ctrl_L")
        return {"FINISHED"}

class Operator_Nose_Bridge_2_Ctrl(bpy.types.Operator):
    bl_idname = "operator.nose_bridge_2_ctrl"
    bl_label = "BlenRig Select nose_bridge_2_ctrl"
    bl_description = "nose_bridge_2_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nose_bridge_2_ctrl")
        return {"FINISHED"}

class Operator_Nose_Frown_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.nose_frown_ctrl_r"
    bl_label = "BlenRig Select nose_frown_ctrl_R"
    bl_description = "nose_frown_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nose_frown_ctrl_R")
        return {"FINISHED"}

class Operator_Nose_Frown_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.nose_frown_ctrl_l"
    bl_label = "BlenRig Select nose_frown_ctrl_L"
    bl_description = "nose_frown_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nose_frown_ctrl_L")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_r"
    bl_label = "BlenRig Select cheek_ctrl_R"
    bl_description = "cheek_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_R")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_3_r"
    bl_label = "BlenRig Select cheek_ctrl_3_R"
    bl_description = "cheek_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_3_R")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_2_r"
    bl_label = "BlenRig Select cheek_ctrl_2_R"
    bl_description = "cheek_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_2_R")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_1_r"
    bl_label = "BlenRig Select cheek_ctrl_1_R"
    bl_description = "cheek_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_1_R")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_3_r"
    bl_label = "BlenRig Select cheek2_ctrl_3_R"
    bl_description = "cheek2_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_3_R")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_2_r"
    bl_label = "BlenRig Select cheek2_ctrl_2_R"
    bl_description = "cheek2_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_2_R")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_1_r"
    bl_label = "BlenRig Select cheek2_ctrl_1_R"
    bl_description = "cheek2_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_1_R")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_3_r"
    bl_label = "BlenRig Select lip_up3_ctrl_3_R"
    bl_description = "lip_up3_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_3_R")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_2_r"
    bl_label = "BlenRig Select lip_up3_ctrl_2_R"
    bl_description = "lip_up3_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_2_R")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_1_r"
    bl_label = "BlenRig Select lip_up3_ctrl_1_R"
    bl_description = "lip_up3_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_1_R")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_3_r"
    bl_label = "BlenRig Select lip_up2_ctrl_3_R"
    bl_description = "lip_up2_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_3_R")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_2_r"
    bl_label = "BlenRig Select lip_up2_ctrl_2_R"
    bl_description = "lip_up2_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_2_R")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_1_r"
    bl_label = "BlenRig Select lip_up2_ctrl_1_R"
    bl_description = "lip_up2_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_1_R")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_l"
    bl_label = "BlenRig Select cheek_ctrl_L"
    bl_description = "cheek_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_L")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_3_l"
    bl_label = "BlenRig Select cheek_ctrl_3_L"
    bl_description = "cheek_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_3_L")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_2_l"
    bl_label = "BlenRig Select cheek_ctrl_2_L"
    bl_description = "cheek_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_2_L")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_1_l"
    bl_label = "BlenRig Select cheek_ctrl_1_L"
    bl_description = "cheek_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_1_L")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_3_l"
    bl_label = "BlenRig Select cheek2_ctrl_3_L"
    bl_description = "cheek2_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_3_L")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_2_l"
    bl_label = "BlenRig Select cheek2_ctrl_2_L"
    bl_description = "cheek2_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_2_L")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_1_l"
    bl_label = "BlenRig Select cheek2_ctrl_1_L"
    bl_description = "cheek2_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_1_L")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_3_l"
    bl_label = "BlenRig Select lip_up3_ctrl_3_L"
    bl_description = "lip_up3_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_3_L")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_2_l"
    bl_label = "BlenRig Select lip_up3_ctrl_2_L"
    bl_description = "lip_up3_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_2_L")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_1_l"
    bl_label = "BlenRig Select lip_up3_ctrl_1_L"
    bl_description = "lip_up3_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_1_L")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_3_l"
    bl_label = "BlenRig Select lip_up2_ctrl_3_L"
    bl_description = "lip_up2_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_3_L")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_2_l"
    bl_label = "BlenRig Select lip_up2_ctrl_2_L"
    bl_description = "lip_up2_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_2_L")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_1_l"
    bl_label = "BlenRig Select lip_up2_ctrl_1_L"
    bl_description = "lip_up2_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_1_L")
        return {"FINISHED"}

class Operator_Nostril_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.nostril_ctrl_r"
    bl_label = "BlenRig Select nostril_ctrl_R"
    bl_description = "nostril_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nostril_ctrl_R")
        return {"FINISHED"}

class Operator_Nose_Ctrl(bpy.types.Operator):
    bl_idname = "operator.nose_ctrl"
    bl_label = "BlenRig Select nose_ctrl"
    bl_description = "nose_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nose_ctrl")
        return {"FINISHED"}

class Operator_Nostril_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.nostril_ctrl_l"
    bl_label = "BlenRig Select nostril_ctrl_L"
    bl_description = "nostril_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "nostril_ctrl_L")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_mid"
    bl_label = "BlenRig Select lip_up3_ctrl_mid"
    bl_description = "lip_up3_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_mid")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl"
    bl_label = "BlenRig Select lip_up3_ctrl"
    bl_description = "lip_up3_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_mid"
    bl_label = "BlenRig Select lip_up2_ctrl_mid"
    bl_description = "lip_up2_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_mid")
        return {"FINISHED"}

class Operator_lip_up2_ctrl(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl"
    bl_label = "BlenRig Select lip_up2_ctrl"
    bl_description = "lip_up2_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_4_R(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_4_r"
    bl_label = "BlenRig Select cheek_ctrl_4_R"
    bl_description = "cheek_ctrl_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_4_R")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_4_R(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_4_r"
    bl_label = "BlenRig Select cheek2_ctrl_4_R"
    bl_description = "cheek2_ctrl_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_4_R")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_4_R(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_4_r"
    bl_label = "BlenRig Select lip_up3_ctrl_4_R"
    bl_description = "lip_up3_ctrl_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_4_R")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_4_R(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_4_r"
    bl_label = "BlenRig Select lip_up2_ctrl_4_R"
    bl_description = "lip_up2_ctrl_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_4_R")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_4_L(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_4_l"
    bl_label = "BlenRig Select cheek_ctrl_4_L"
    bl_description = "cheek_ctrl_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_4_L")
        return {"FINISHED"}

class Operator_Cheek2_Ctrl_4_L(bpy.types.Operator):
    bl_idname = "operator.cheek2_ctrl_4_l"
    bl_label = "BlenRig Select cheek2_ctrl_4_L"
    bl_description = "cheek2_ctrl_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek2_ctrl_4_L")
        return {"FINISHED"}

class Operator_Lip_Up3_Ctrl_4_L(bpy.types.Operator):
    bl_idname = "operator.lip_up3_ctrl_4_l"
    bl_label = "BlenRig Select lip_up3_ctrl_4_L"
    bl_description = "lip_up3_ctrl_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up3_ctrl_4_L")
        return {"FINISHED"}

class Operator_Lip_Up2_Ctrl_4_L(bpy.types.Operator):
    bl_idname = "operator.lip_up2_ctrl_4_l"
    bl_label = "BlenRig Select lip_up2_ctrl_4_L"
    bl_description = "lip_up2_ctrl_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up2_ctrl_4_L")
        return {"FINISHED"}

class Operator_Mouth_Mstr_Up(bpy.types.Operator):
    bl_idname = "operator.mouth_mstr_up"
    bl_label = "BlenRig Select mouth_mstr_up"
    bl_description = "mouth_mstr_up"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_mstr_up")
        return {"FINISHED"}

class Operator_Mouth_Corner_R(bpy.types.Operator):
    bl_idname = "operator.mouth_corner_r"
    bl_label = "BlenRig Select mouth_corner_R"
    bl_description = "mouth_corner_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_corner_R")
        return {"FINISHED"}

class Operator_Mouth_Corner_L(bpy.types.Operator):
    bl_idname = "operator.mouth_corner_l"
    bl_label = "BlenRig Select mouth_corner_L"
    bl_description = "mouth_corner_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_corner_L")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl"
    bl_label = "BlenRig Select lip_up_ctrl"
    bl_description = "lip_up_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_Collision(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_collision"
    bl_label = "BlenRig Select lip_up_ctrl_collision"
    bl_description = "lip_up_ctrl_collision"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_collision")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_3_r"
    bl_label = "BlenRig Select lip_up_ctrl_3_R"
    bl_description = "lip_up_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_3_R")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_2_r"
    bl_label = "BlenRig Select lip_up_ctrl_2_R"
    bl_description = "lip_up_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_2_R")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_1_r"
    bl_label = "BlenRig Select lip_up_ctrl_1_R"
    bl_description = "lip_up_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_1_R")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_mid"
    bl_label = "BlenRig Select lip_up_ctrl_mid"
    bl_description = "lip_up_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_mid")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_1_l"
    bl_label = "BlenRig Select lip_up_ctrl_1_L"
    bl_description = "lip_up_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_1_L")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_2_l"
    bl_label = "BlenRig Select lip_up_ctrl_2_L"
    bl_description = "lip_up_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_2_L")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_3_l"
    bl_label = "BlenRig Select lip_up_ctrl_3_L"
    bl_description = "lip_up_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_3_L")
        return {"FINISHED"}

class Operator_Mouth_Up_Ctrl(bpy.types.Operator):
    bl_idname = "operator.mouth_up_ctrl"
    bl_label = "BlenRig Select mouth_up_ctrl"
    bl_description = "mouth_up_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_up_ctrl")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_4_R(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_4_r"
    bl_label = "BlenRig Select lip_up_ctrl_4_R"
    bl_description = "lip_up_ctrl_4_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_4_R")
        return {"FINISHED"}

class Operator_Lip_Up_Ctrl_4_L(bpy.types.Operator):
    bl_idname = "operator.lip_up_ctrl_4_l"
    bl_label = "BlenRig Select lip_up_ctrl_4_L"
    bl_description = "lip_up_ctrl_4_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_up_ctrl_4_L")
        return {"FINISHED"}

class Operator_Mouth_Ctrl(bpy.types.Operator):
    bl_idname = "operator.mouth_ctrl"
    bl_label = "BlenRig Select mouth_ctrl"
    bl_description = "mouth_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_ctrl")
        return {"FINISHED"}

class Operator_Mouth_Low_Ctrl(bpy.types.Operator):
    bl_idname = "operator.mouth_low_ctrl"
    bl_label = "BlenRig Select mouth_low_ctrl"
    bl_description = "mouth_low_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_low_ctrl")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_3_r"
    bl_label = "BlenRig Select lip_low_ctrl_3_R"
    bl_description = "lip_low_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_3_R")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_2_r"
    bl_label = "BlenRig Select lip_low_ctrl_2_R"
    bl_description = "lip_low_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_2_R")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_1_r"
    bl_label = "BlenRig Select lip_low_ctrl_1_R"
    bl_description = "lip_low_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_1_R")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_mid"
    bl_label = "BlenRig Select lip_low_ctrl_mid"
    bl_description = "lip_low_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_mid")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_1_l"
    bl_label = "BlenRig Select lip_low_ctrl_1_L"
    bl_description = "lip_low_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_1_L")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_2_l"
    bl_label = "BlenRig Select lip_low_ctrl_2_L"
    bl_description = "lip_low_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_2_L")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_3_l"
    bl_label = "BlenRig Select lip_low_ctrl_3_L"
    bl_description = "lip_low_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_3_L")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl_Collision(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl_collision"
    bl_label = "BlenRig Select lip_low_ctrl_collision"
    bl_description = "lip_low_ctrl_collision"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl_collision")
        return {"FINISHED"}

class Operator_Lip_Low_Ctrl(bpy.types.Operator):
    bl_idname = "operator.lip_low_ctrl"
    bl_label = "BlenRig Select lip_low_ctrl"
    bl_description = "lip_low_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low_ctrl")
        return {"FINISHED"}

class Operator_Mouth_Mstr_Low(bpy.types.Operator):
    bl_idname = "operator.mouth_mstr_low"
    bl_label = "BlenRig Select mouth_mstr_low"
    bl_description = "mouth_mstr_low"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_mstr_low")
        return {"FINISHED"}

class Operator_Mouth_Mstr_Ctrl(bpy.types.Operator):
    bl_idname = "operator.mouth_mstr_ctrl"
    bl_label = "BlenRig Select mouth_mstr_ctrl"
    bl_description = "mouth_mstr_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_mstr_ctrl")
        return {"FINISHED"}

class Operator_Mouth_Frown_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.mouth_frown_ctrl_r"
    bl_label = "BlenRig Select mouth_frown_ctrl_R"
    bl_description = "mouth_frown_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_frown_ctrl_R")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_3_r"
    bl_label = "BlenRig Select lip_low2_ctrl_3_R"
    bl_description = "lip_low2_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_3_R")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_2_r"
    bl_label = "BlenRig Select lip_low2_ctrl_2_R"
    bl_description = "lip_low2_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_2_R")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_1_r"
    bl_label = "BlenRig Select lip_low2_ctrl_1_R"
    bl_description = "lip_low2_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_1_R")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_3_r"
    bl_label = "BlenRig Select lip_low3_ctrl_3_R"
    bl_description = "lip_low3_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_3_R")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_2_r"
    bl_label = "BlenRig Select lip_low3_ctrl_2_R"
    bl_description = "lip_low3_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_2_R")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_1_r"
    bl_label = "BlenRig Select lip_low3_ctrl_1_R"
    bl_description = "lip_low3_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_1_R")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_5_R(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_5_r"
    bl_label = "BlenRig Select cheek_ctrl_5_R"
    bl_description = "cheek_ctrl_5_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_5_R")
        return {"FINISHED"}

class Operator_Chin_Ctrl_3_R(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_3_r"
    bl_label = "BlenRig Select chin_ctrl_3_R"
    bl_description = "chin_ctrl_3_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_3_R")
        return {"FINISHED"}

class Operator_Chin_Ctrl_2_R(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_2_r"
    bl_label = "BlenRig Select chin_ctrl_2_R"
    bl_description = "chin_ctrl_2_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_2_R")
        return {"FINISHED"}

class Operator_Chin_Ctrl_1_R(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_1_r"
    bl_label = "BlenRig Select chin_ctrl_1_R"
    bl_description = "chin_ctrl_1_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_1_R")
        return {"FINISHED"}

class Operator_Mouth_Frown_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.mouth_frown_ctrl_l"
    bl_label = "BlenRig Select mouth_frown_ctrl_L"
    bl_description = "mouth_frown_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_frown_ctrl_L")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_3_l"
    bl_label = "BlenRig Select lip_low2_ctrl_3_L"
    bl_description = "lip_low2_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_3_L")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_2_l"
    bl_label = "BlenRig Select lip_low2_ctrl_2_L"
    bl_description = "lip_low2_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_2_L")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_1_l"
    bl_label = "BlenRig Select lip_low2_ctrl_1_L"
    bl_description = "lip_low2_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_1_L")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_3_l"
    bl_label = "BlenRig Select lip_low3_ctrl_3_L"
    bl_description = "lip_low3_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_3_L")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_2_l"
    bl_label = "BlenRig Select lip_low3_ctrl_2_L"
    bl_description = "lip_low3_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_2_L")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_1_l"
    bl_label = "BlenRig Select lip_low3_ctrl_1_L"
    bl_description = "lip_low3_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_1_L")
        return {"FINISHED"}

class Operator_Cheek_Ctrl_5_L(bpy.types.Operator):
    bl_idname = "operator.cheek_ctrl_5_l"
    bl_label = "BlenRig Select cheek_ctrl_5_L"
    bl_description = "cheek_ctrl_5_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "cheek_ctrl_5_L")
        return {"FINISHED"}

class Operator_Chin_Ctrl_3_L(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_3_l"
    bl_label = "BlenRig Select chin_ctrl_3_L"
    bl_description = "chin_ctrl_3_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_3_L")
        return {"FINISHED"}

class Operator_Chin_Ctrl_2_L(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_2_l"
    bl_label = "BlenRig Select chin_ctrl_2_L"
    bl_description = "chin_ctrl_2_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_2_L")
        return {"FINISHED"}

class Operator_Chin_Ctrl_1_L(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_1_l"
    bl_label = "BlenRig Select chin_ctrl_1_L"
    bl_description = "chin_ctrl_1_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_1_L")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl_mid"
    bl_label = "BlenRig Select lip_low2_ctrl_mid"
    bl_description = "lip_low2_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl_mid")
        return {"FINISHED"}

class Operator_Lip_Low2_Ctrl(bpy.types.Operator):
    bl_idname = "operator.lip_low2_ctrl"
    bl_label = "BlenRig Select lip_low2_ctrl"
    bl_description = "lip_low2_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low2_ctrl")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl_mid"
    bl_label = "BlenRig Select lip_low3_ctrl_mid"
    bl_description = "lip_low3_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl_mid")
        return {"FINISHED"}

class Operator_Lip_Low3_Ctrl(bpy.types.Operator):
    bl_idname = "operator.lip_low3_ctrl"
    bl_label = "BlenRig Select lip_low3_ctrl"
    bl_description = "lip_low3_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "lip_low3_ctrl")
        return {"FINISHED"}

class Operator_Chin_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl_mid"
    bl_label = "BlenRig Select chin_ctrl_mid"
    bl_description = "chin_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl_mid")
        return {"FINISHED"}

class Operator_Chin_Ctrl(bpy.types.Operator):
    bl_idname = "operator.chin_ctrl"
    bl_label = "BlenRig Select chin_ctrl"
    bl_description = "chin_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "chin_ctrl")
        return {"FINISHED"}

class Operator_Maxi(bpy.types.Operator):
    bl_idname = "operator.maxi"
    bl_label = "BlenRig Select maxi"
    bl_description = "maxi"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "maxi")
        return {"FINISHED"}

class Operator_Mouth_Str_Ctrl(bpy.types.Operator):
    bl_idname = "operator.mouth_str_ctrl"
    bl_label = "BlenRig Select mouth_str_ctrl"
    bl_description = "mouth_str_ctrl"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "mouth_str_ctrl")
        return {"FINISHED"}

class Operator_Head_Mid_Stretch(bpy.types.Operator):
    bl_idname = "operator.head_mid_stretch"
    bl_label = "BlenRig Select head_mid_stretch"
    bl_description = "head_mid_stretch"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_mid_stretch")
        return {"FINISHED"}

class Operator_Head_Low_Stretch(bpy.types.Operator):
    bl_idname = "operator.head_low_stretch"
    bl_label = "BlenRig Select head_low_stretch"
    bl_description = "head_low_stretch"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_low_stretch")
        return {"FINISHED"}

class Operator_Teeth_Up_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.teeth_up_ctrl_r"
    bl_label = "BlenRig Select teeth_up_ctrl_R"
    bl_description = "teeth_up_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_up_ctrl_R")
        return {"FINISHED"}

class Operator_Teeth_Up_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.teeth_up_ctrl_l"
    bl_label = "BlenRig Select teeth_up_ctrl_L"
    bl_description = "teeth_up_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_up_ctrl_L")
        return {"FINISHED"}

class Operator_Teeth_Up_Ctrl_Mid_R(bpy.types.Operator):
    bl_idname = "operator.teeth_up_ctrl_mid_r"
    bl_label = "BlenRig Select teeth_up_ctrl_mid_R"
    bl_description = "teeth_up_ctrl_mid_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_up_ctrl_mid_R")
        return {"FINISHED"}

class Operator_Teeth_Up_Ctrl_Mid_L(bpy.types.Operator):
    bl_idname = "operator.teeth_up_ctrl_mid_l"
    bl_label = "BlenRig Select teeth_up_ctrl_mid_L"
    bl_description = "teeth_up_ctrl_mid_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_up_ctrl_mid_L")
        return {"FINISHED"}

class Operator_Teeth_Up_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.teeth_up_ctrl_mid"
    bl_label = "BlenRig Select teeth_up_ctrl_mid"
    bl_description = "teeth_up_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_up_ctrl_mid")
        return {"FINISHED"}

class Operator_Teeth_Up(bpy.types.Operator):
    bl_idname = "operator.teeth_up"
    bl_label = "BlenRig Select teeth_up"
    bl_description = "teeth_up"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_up")
        return {"FINISHED"}

class Operator_Teeth_Low_Ctrl_R(bpy.types.Operator):
    bl_idname = "operator.teeth_low_ctrl_r"
    bl_label = "BlenRig Select teeth_low_ctrl_R"
    bl_description = "teeth_low_ctrl_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_low_ctrl_R")
        return {"FINISHED"}

class Operator_Teeth_Low_Ctrl_L(bpy.types.Operator):
    bl_idname = "operator.teeth_low_ctrl_l"
    bl_label = "BlenRig Select teeth_low_ctrl_L"
    bl_description = "teeth_low_ctrl_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_low_ctrl_L")
        return {"FINISHED"}

class Operator_Teeth_Low_Ctrl_Mid_R(bpy.types.Operator):
    bl_idname = "operator.teeth_low_ctrl_mid_r"
    bl_label = "BlenRig Select teeth_low_ctrl_mid_R"
    bl_description = "teeth_low_ctrl_mid_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_low_ctrl_mid_R")
        return {"FINISHED"}

class Operator_Teeth_Low_Ctrl_Mid_L(bpy.types.Operator):
    bl_idname = "operator.teeth_low_ctrl_mid_l"
    bl_label = "BlenRig Select teeth_low_ctrl_mid_L"
    bl_description = "teeth_low_ctrl_mid_L"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_low_ctrl_mid_L")
        return {"FINISHED"}

class Operator_Teeth_Low_Ctrl_Mid(bpy.types.Operator):
    bl_idname = "operator.teeth_low_ctrl_mid"
    bl_label = "BlenRig Select teeth_low_ctrl_mid"
    bl_description = "teeth_low_ctrl_mid"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_low_ctrl_mid")
        return {"FINISHED"}

class Operator_Teeth_Low(bpy.types.Operator):
    bl_idname = "operator.teeth_low"
    bl_label = "BlenRig Select teeth_low"
    bl_description = "teeth_low"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "teeth_low")
        return {"FINISHED"}

class Operator_Uvula_1(bpy.types.Operator):
    bl_idname = "operator.uvula_1"
    bl_label = "BlenRig Select uvula_1"
    bl_description = "uvula_1"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "uvula_1")
        return {"FINISHED"}

class Operator_Uvula_2(bpy.types.Operator):
    bl_idname = "operator.uvula_2"
    bl_label = "BlenRig Select uvula_2"
    bl_description = "uvula_2"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "uvula_2")
        return {"FINISHED"}

class Operator_Tongue_1_FK(bpy.types.Operator):
    bl_idname = "operator.tongue_1_fk"
    bl_label = "BlenRig Select tongue_1_fk"
    bl_description = "tongue_1_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tongue_1_fk")
        return {"FINISHED"}

class Operator_Tongue_2_FK(bpy.types.Operator):
    bl_idname = "operator.tongue_2_fk"
    bl_label = "BlenRig Select tongue_2_fk"
    bl_description = "tongue_2_fk"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tongue_2_fk")
        return {"FINISHED"}

class Operator_Tongue_1_IK(bpy.types.Operator):
    bl_idname = "operator.tongue_1_ik"
    bl_label = "BlenRig Select tongue_1_ik"
    bl_description = "tongue_1_ik"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tongue_1_ik")
        return {"FINISHED"}

class Operator_Tongue_2_IK(bpy.types.Operator):
    bl_idname = "operator.tongue_2_ik"
    bl_label = "BlenRig Select tongue_2_ik"
    bl_description = "tongue_2_ik"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tongue_2_ik")
        return {"FINISHED"}

class Operator_Tongue_3_IK(bpy.types.Operator):
    bl_idname = "operator.tongue_3_ik"
    bl_label = "BlenRig Select tongue_3_ik"
    bl_description = "tongue_3_ik"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tongue_3_ik")
        return {"FINISHED"}

class Operator_Tongue_Mstr(bpy.types.Operator):
    bl_idname = "operator.tongue_mstr"
    bl_label = "BlenRig Select tongue_mstr"
    bl_description = "tongue_mstr"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "tongue_mstr")
        return {"FINISHED"}
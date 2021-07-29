from bpy.types import Panel

class BLENRIG_PT_guide_assistant(Panel):
    bl_label = ""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER",}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'GUIDES':
            return False
        if not context.object:
            return False
        if context.object.type not in {'ARAMTURE', 'MESH', 'LATTICE', 'CURVE', 'SURFACE', 'EDIT_ARMATURE'}:
            return False
        return context.scene.blenrig_guide.arm_obj

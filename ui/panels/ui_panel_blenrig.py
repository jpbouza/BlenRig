import bpy

class BLENRIG_PT_BlenRig_5_general(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_idname = "BLENRIG_PT_BlenRig_5_general"
    bl_region_type = 'UI'
    bl_label = 'BlenRig 6 General Panel'
    bl_category = "BlenRig 6"

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        if (context.active_object.type in ["ARMATURE"]):
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':
                    for prop in context.active_object.data.items():
                        return True
                        # if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                        #     return True
        else:
            return True
            # if context.mode in ["OBJECT","EDIT_MESH","LATTICE", "CURVE"]:
            #     if (context.active_object.type in ["MESH","LATTICE", "CURVE"]):
            #         for mod in context.active_object.modifiers:
            #             if (mod.type in ["ARMATURE", "MESH_DEFORM", "HOOK"]):
            #                 return True

    def draw(self, context):
        layout = self.layout
        BlenRig_Panel_Options(layout, context)

def BlenRig_Panel_Options(layout, context):
        
        column = layout.column(align=True)

        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings

        # Display options.
        columnRow = column.row()
        columnRow.prop(BlenRigPanelOptions, 'displayContext', text=" ",expand=True)

        # PICKER Menu.
        if BlenRigPanelOptions.displayContext == 'PICKER':
            column.separator()

        # RIGTOOLS Menu.
        elif BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            column.separator()

        # BONE_SHAPES Menus.
        elif BlenRigPanelOptions.displayContext == 'BONE_SHAPES':
            column.separator()

        # TOOLS Menu.
        elif BlenRigPanelOptions.displayContext == 'TOOLS':
            if context.mode == 'POSE':
                column.separator()

            else:
                column.separator()

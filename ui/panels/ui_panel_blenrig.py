import bpy

class BLENRIG_PT_blenrig_6_general(bpy.types.Panel):
    bl_label = 'BlenRig General Panel'
    bl_space_type = 'VIEW_3D'
    bl_idname = "BLENRIG_PT_blenrig_6_general"
    bl_region_type = 'UI'
    bl_category = "BlenRig 6"


    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        if (context.active_object.type in ["ARMATURE"]):
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                    for prop in context.active_object.data.items():
                        return True
        else:
            return True

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

        # TOOLS Menu.
        elif BlenRigPanelOptions.displayContext == 'TOOLS':
            column.separator()

        # GUIDES Menu.
        elif BlenRigPanelOptions.displayContext == 'GUIDES':
            column.separator()

        else:
            column.separator()

import bpy

####### Rig Version Info

class BLENRIG_PT_Rig_version_info(bpy.types.Panel):
    bl_label = "Rig Version Info"
    bl_idname = "BLENRIG_PT_Rig_version_info"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False

        if not context.active_object:
            return False
        if (context.active_object.type in ["ARMATURE"]):
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                    for prop in context.active_object.data.items():
                        if prop[0] == 'rig_version' and str(prop[1]) >= '2.0.0':
                            return True

    def draw(self, context):
        arm_data = context.active_object.data
        layout = self.layout

        ####### Rig Version Info
        col = layout.column()
        row = col.row()
        row.label(text="Armature Ver. " + str(arm_data['rig_version']))


    def draw_header(self, context):
        scene  = context.scene
        layout = self.layout
        layout.emboss = 'NONE'
        row = layout.row(align=True)
        row.prop(scene, "name", icon='INFO', icon_only= True)
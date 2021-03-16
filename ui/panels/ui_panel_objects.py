import bpy

####### Object Baking Panel

class BLENRIG_PT_blenrig_6_mesh_panel(bpy.types.Panel):
    bl_region_type = 'WINDOW'
    bl_space_type = 'VIEW_3D'
    bl_idname = "BLENRIG_PT_blenrig_6_mesh_panel"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_region_type = 'UI'
    bl_label = 'BlenRig 6 Mesh Baking Panel'
    bl_category = "BlenRig 6"

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False

        if context.mode in ["EDIT_MESH"]:
            return False

        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            for mod in bpy.context.active_object.modifiers:
                if (mod.type in ["ARMATURE", "MESH_DEFORM", "SURFACE_DEFORM"]):
                    return True

    def draw(self, context):
        props = context.window_manager.blenrig_6_props
        layout = self.layout

        box = layout.column()
        col = box.column()
        row = col.row()
    # expanded box
        col.separator
        row = col.row()
        row.operator("blenrig.mesh_pose_baker", text="Bake Mesh")
        row.prop(props, "bake_to_shape")

####### Lattice & Curves Panel

class BLENRIG_PT_blenrig_6_lattice_panel(bpy.types.Panel):
    bl_label = "BlenRig 6 Lattice & Curves Panel"
    bl_idname = "BLENRIG_PT_blenrig_6_lattice_panel"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_region_type = 'WINDOW'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BlenRig 6"

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False

        if not context.active_object:
            return False
        if (context.active_object.type in ["LATTICE", "CURVE"]):
            for mod in context.active_object.modifiers:
                if (mod.type in ["HOOK"]):
                    return True

    def draw(self, context):
        props = context.window_manager.blenrig_6_props
        layout = self.layout

        row = layout.row(align=False)
        row.operator("blenrig.disable_hooks_modif", text="Modify Lattice Position")

        sub = layout.row(align=False)
        sub = row.row()
        sub.scale_x = 0.6
        sub.operator("blenrig.reset_hooks", text="Apply Lattice Position")
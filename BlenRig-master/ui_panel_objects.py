import bpy

####### Object Baking Panel

class BLENRIG_PT_BlenRig_5_mesh_panel(bpy.types.Panel):
    bl_label = "BlenRig 5 Mesh Baking Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            for mod in bpy.context.active_object.modifiers:
                if (mod.type in ["ARMATURE", "MESH_DEFORM"]):
                    return True

    def draw(self, context):
        props = context.window_manager.blenrig_5_props
        layout = self.layout

        box = layout.column()
        col = box.column()
        row = col.row()
    # expanded box
        col.separator
        row = col.row()
        row.operator("blenrig5.mesh_pose_baker", text="Bake Mesh")
        row.prop(props, "bake_to_shape")

####### Lattice & Curves Panel

class BLENRIG_PT_BlenRig_5_lattice_panel(bpy.types.Panel):
    bl_label = "BlenRig 5 Lattice & Curves Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["LATTICE", "CURVE"]):
            for mod in bpy.context.active_object.modifiers:
                if (mod.type in ["HOOK"]):
                    return True

    def draw(self, context):
        layout = self.layout

        box = layout.column()
        col = box.column()
        row = col.row()
    # expanded box
        col.separator
        row = col.row()
        row.operator("blenrig5.reset_hooks", text="Reset Hooks")
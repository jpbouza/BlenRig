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
        # Bake Buttons
        col_buttons = row.column()
        box_bake = col_buttons.box()
        box_bake.label(text='Baking')
        col_bake = box_bake.column()
        row_bake = col_bake.row()
        row_bake.operator("blenrig.mesh_pose_baker", text="Bake Mesh")
        row_bake.prop(props, "bake_to_shape")
        col_buttons.separator()
        #Weights Transfer Buttons
        box_transfer = col_buttons.box()
        box_transfer.label(text='Weights Transfer')
        box_transfer.operator("blenrig.transfer_vgroups", text = 'Transfer Weights')
        row_options = box_transfer.row()
        col_ray = row_options.column()
        col_ray.label(text = 'Ray Distance:')
        col_ray.prop(bpy.context.scene.blenrig_guide, "transfer_ray_distance", text = '')
        col_mapping = row_options.column()
        col_mapping.label(text = 'Mapping:')
        col_mapping.prop(bpy.context.scene.blenrig_guide, "transfer_mapping", text =  '')
        #Add Modiifers Buttons
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Add Modifiers')
        box_modifiers.operator("blenrig.add_head_modifiers", text = 'Add Head Mofiiers')
        box_modifiers.operator("blenrig.add_hands_modifiers", text = 'Add Hands Mofiiers')
        #Add Shapekeys Buttons
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Add Shapekeys')
        box_modifiers.operator("blenrig.add_body_shapekeys", text = 'Add Body Shapekeys')
        box_modifiers.operator("blenrig.add_fingers_shapekeys", text = 'Add Fingers Shapekeys')
        box_modifiers.operator("blenrig.add_toes_shapekeys", text = 'Add Toes Shapekeys')
        box_modifiers.operator("blenrig.add_face_shapekeys", text = 'Add Face Shapekeys')
        #Bind Mesh Deform
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Bind Mesh Deform')
        row_mdef = box.row()
        row_mdef.operator("blenrig.bind_mdef_modifiers", text = 'Bind Mesh Deform (Fast)').Bind_Type = True
        row_mdef.operator("blenrig.bind_mdef_modifiers", text = 'Bind Mesh Deform (Final)').Bind_Type = False
        col_mdef = box.column()
        col_mdef.operator("blenrig.unbind_mdef_modifiers", text = 'Unbind Mesh Deform')

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
        row.operator("blenrig.disable_hooks_modif", text="Edit Lattice Position")

        sub = layout.row(align=False)
        sub = row.row()
        sub.scale_x = 0.6
        sub.operator("blenrig.reset_hooks", text="Apply Lattice Position")
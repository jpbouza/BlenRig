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

        if not context.active_object:
            return False
        if (context.active_object.type in ["MESH"]):
            for mod in context.active_object.modifiers:
                if (mod.type in ["ARMATURE", "MESH_DEFORM", "SURFACE_DEFORM"]):
                    return True

    def draw(self, context):
        props = context.window_manager.blenrig_6_props
        guide_props = context.scene.blenrig_guide
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
        col_ray.prop(context.scene.blenrig_guide, "transfer_ray_distance", text = '')
        col_mapping = row_options.column()
        col_mapping.label(text = 'Mapping:')
        col_mapping.prop(context.scene.blenrig_guide, "transfer_mapping", text =  '')
        #Add Modiifers Buttons
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Add Modifiers')
        box_modifiers.operator("blenrig.add_head_modifiers", text = 'Add Head Mofiiers')
        box_modifiers.operator("blenrig.add_hands_modifiers", text = 'Add Hands Mofiiers')
        box_modifiers.operator("blenrig.add_body_modifiers", text = 'Add Body Mofiiers')
        box_modifiers.operator("blenrig.add_teeth_modifiers", text = 'Add Teeth Mofiiers')
        box_modifiers.operator("blenrig.add_eyes_modifiers", text = 'Add Left Eye Mofiiers').side = 'Left'
        box_modifiers.operator("blenrig.add_eyes_modifiers", text = 'Add Right Eye Mofiiers').side = 'Right'
        #Shapekeys
        #Add Shapekeys Buttons
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Shapekeys Tools')
        box_modifiers.label(text='Add')
        box_modifiers.operator("blenrig.add_body_shapekeys", text = 'Add Body Shapekeys')
        box_modifiers.operator("blenrig.add_fingers_shapekeys", text = 'Add Fingers Shapekeys')
        box_modifiers.operator("blenrig.add_toes_shapekeys", text = 'Add Toes Shapekeys')
        box_modifiers.operator("blenrig.add_face_shapekeys", text = 'Add Face Shapekeys')
        box_modifiers.label(text='Mirroring')
        row_modifiers = box_modifiers.row()
        row_modifiers.operator("blenrig.mirror_active_shapekey", text = 'Mirror Shapekey')
        row_modifiers.operator("blenrig.mirror_all_shapekeys", text = 'Mirror All Shapekeys')
        row_modifiers = box_modifiers.row()
        row_modifiers.operator("blenrig.mirror_active_shapekey_driver", text = 'Mirror Shapekey Driver')
        row_modifiers.operator("blenrig.mirror_shapekeys_drivers", text = 'Mirror All Shapekeys Drivers')
        box_modifiers.label(text='Sculpting')
        row_modifiers = box_modifiers.row()
        row_modifiers.operator("blenrig.create_sculpt_shapekey_object_form_pose", text = 'Generate Sculpt Object').Offset = True
        row_modifiers.operator("blenrig.apply_sculpt_object_to_shapekey", text = 'Apply Sculpt to Shapekey').Clear_Sculpt_Object = True
        row_modifiers = box_modifiers.row()
        row_modifiers.prop(guide_props, "sculpt_use_smooth", text='Use Smooth Modifiers')
        row_modifiers.operator("blenrig.cancel_sculpt_object_to_shapekey", text = 'Cancel')
        box_modifiers.operator("blenrig.reset_shapekey", text = 'Reset Active Shapekey')
        row = box_modifiers.row()
        col_1 = row.column()
        col_1.scale_x = 1.5
        col_2 = row.column()
        col_1.operator("blenrig.override_sculpt_objects", text = 'Override Sculpt Object').assign = 'Sculpt'
        try:
            col_2.label(text=context.scene.blenrig_guide.sculpt_shapekey_obj.name)
        except:
            col_2.label(text='No Objects Assigned')
        col_1.operator("blenrig.override_sculpt_objects", text = 'Override Shapekey Objet').assign = 'Shapekey'
        try:
            col_2.label(text=context.scene.blenrig_guide.shapekeys_obj.name)
        except:
            col_2.label(text='No Object Assigned')
        #Mirror Vgroups
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Mirror Vertex Groups')
        box_modifiers.operator("blenrig.mirror_vertex_groups", text = 'Mirror All Vertex Groups').All = True
        box_modifiers.operator("blenrig.mirror_vertex_groups", text = 'Mirror Active Vertex Group').All = False
        #Bind Mesh Deform
        box_modifiers = col_buttons.box()
        box_modifiers.label(text='Bind Mesh Deform')
        row_mdef = box_modifiers.row()
        row_mdef.operator("blenrig.bind_mdef_modifiers", text = 'Bind Mesh Deform (Fast)').Bind_Type = True
        row_mdef.operator("blenrig.bind_mdef_modifiers", text = 'Bind Mesh Deform (Final)').Bind_Type = False
        col_mdef = box_modifiers.column()
        col_mdef.operator("blenrig.unbind_mdef_modifiers", text = 'Unbind Mesh Deform')
        #Define Body Areas
        box_area = col_buttons.box()
        box_area.label(text='Character Objects')
        row = box_area.row()
        col_1 = row.column()
        col_1.scale_x = 1.5
        col_2 = row.column()
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Body Objects').area = 'Body'
        try:
            col_2.label(text= str([b.character_body_obj.name for b in context.scene.blenrig_character_body_obj]))
        except:
            col_2.label(text='No Objects Assigned')
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Hands Object').area = 'Hands'
        try:
            col_2.label(text=context.scene.blenrig_guide.character_hands_obj.name)
        except:
            col_2.label(text='No Object Assigned')
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Toes Object').area = 'Toes'
        try:
            col_2.label(text=context.scene.blenrig_guide.character_toes_obj.name)
        except:
            col_2.label(text='No Object Assigned')
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Head Object').area = 'Head'
        try:
            col_2.label(text=context.scene.blenrig_guide.character_head_obj.name)
        except:
            col_2.label(text='No Object Assigned')

        box_area.label(text='BlenRig Rigging Meshes')
        row = box_area.row()
        col_1 = row.column()
        col_1.scale_x = 1.5
        col_2 = row.column()
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Mdef Cage Object').area = 'Mdef_Cage'
        try:
            col_2.label(text=context.scene.blenrig_guide.mdef_cage_obj.name)
        except:
            col_2.label(text='No Object Assigned')
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Head Weights Transfer Object').area = 'Head_Weights'
        try:
            col_2.label(text=context.scene.blenrig_guide.mdef_head_weights_transfer_obj.name)
        except:
            col_2.label(text='No Object Assigned')
        col_1.operator("blenrig.define_body_area", text = 'Define selected as Hands Weights Transfer Object').area = 'Hands_Weights'
        try:
            col_2.label(text=context.scene.blenrig_guide.mdef_hands_weights_transfer_obj.name)
        except:
            col_2.label(text='No Object Assigned')

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
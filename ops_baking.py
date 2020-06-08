import bpy

################################ BAKING OPERATORS ##########################################################


# Mesh Proportions Baker operator
class ARMATURE_OT_mesh_pose_baker(bpy.types.Operator):
    bl_label = "BlenRig 5 Mesh Baker"
    bl_idname = "blenrig5.mesh_pose_baker"
    bl_description = "Bake current pose to mesh"
    bl_options = {'REGISTER', 'UNDO'}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        return (bpy.context.object.type == "MESH" and context.mode=='OBJECT')

    #Baking   
    def bake(self, context):
        props = context.window_manager.blenrig_5_props      
        if not bpy.context.object:
            return False        
        old_ob = bpy.context.active_object
        bake_meshes = [ob.name for ob in bpy.context.selected_objects if ob.type=="MESH"]

        for name in bake_meshes:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]

            bpy.context.view_layer.objects.active = ob

            # Turn off SUBSURF for baking
            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    old_state = mod.show_viewport
                    mod.show_viewport = False

            # --- get a mesh from the object ---
            depsgraph = bpy.context.evaluated_depsgraph_get()
            mesh_owner = ob.evaluated_get(depsgraph)
            mesh = mesh_owner.to_mesh()

            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    mod.show_viewport = old_state

            # If Bake to shape option is off                  
            if props.bake_to_shape == False:  
                # Check if there are shapekeys in object  
                try:        
                    if ob.data.shape_keys.key_blocks:
                        key = ob.data.shape_keys
                        shapekeys = key.key_blocks                
                        # Transfer vertex locations to Basis key
                        for vert in ob.data.vertices:
                            shapekeys['Basis'].data[vert.index].co = mesh.vertices[vert.index].co 

                        # Make baked shape active
                        for i in range(len(shapekeys)):
                            shape = shapekeys[i]
                            if shape.name == 'Basis':
                                ob.active_shape_key_index = i
                except (AttributeError):
                    # Transfer vertex locations to Mesh                
                    for vert in ob.data.vertices:
                        vert.co = mesh.vertices[vert.index].co 

            # If Bake to shape option is on  
            else:
                # Check if there are shapekeys in object
                try:
                    ob.data.shape_keys.key_blocks
                except (AttributeError):
                    Basis = ob.shape_key_add(from_mix=False)
                    Basis.name = 'Basis'

                # Create new shape for storing the bake

                baked_shape = ob.shape_key_add(from_mix=False)
                baked_shape.name = 'Baked_shape'
                baked_shape.value = 1

                # Transfer vertex locations
                for vert in ob.data.vertices:
                    baked_shape.data[vert.index].co = mesh.vertices[vert.index].co 

                # Make baked shape active
                for i in range(len(ob.data.shape_keys.key_blocks)):
                    shape = ob.data.shape_keys.key_blocks[i]
                    if shape.name == baked_shape.name:
                        ob.active_shape_key_index = i

        # Remove unused baked mesh               
        ob.to_mesh_clear()
        bpy.context.view_layer.objects.active = old_ob


    #Unbind Mdef modifier if object is bound    
    def mdef_unbind(self, context):
        if not bpy.context.object:
            return False        

        old_ob = bpy.context.active_object

        bake_meshes = [ob.name for ob in bpy.context.selected_objects if ob.type=="MESH"]
        for name in bake_meshes:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
            bpy.context.view_layer.objects.active = ob

            # unbind mdef modifiers
            for i in range(len(ob.modifiers)):
                mod = ob.modifiers[i]
                if mod.type in ['MESH_DEFORM']:
                    if mod.is_bound == True:
                        bpy.ops.object.meshdeform_bind(modifier=mod.name)      

        bpy.context.view_layer.objects.active = old_ob                           

    def execute(self, context):
        self.bake(context)     
        self.mdef_unbind(context)  
        self.report({'INFO'}, "Baking done")
        return{'FINISHED'}   

# Hook Reset operator
class ARMATURE_OT_reset_hooks(bpy.types.Operator):
    bl_label = "BlenRig 5 Reset Hooks"
    bl_idname = "blenrig5.reset_hooks"
    bl_description = "Reset Hooks on Lattices and Curves"
    bl_options = {'REGISTER', 'UNDO'}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        return (bpy.context.object.type == "LATTICE", "CURVE" and context.mode=='OBJECT')

    def reset_hooks(self,context):
        
        selected_lattices = [ob.name for ob in bpy.context.selected_objects if ob.type=="LATTICE"]

        for name in selected_lattices:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]

            bpy.context.view_layer.objects.active = ob

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.lattice.select_all(action='SELECT')
            for mod in ob.modifiers:
                if mod.type == 'HOOK':
                    bpy.ops.object.hook_reset(modifier=mod.name)
            bpy.ops.object.mode_set(mode='OBJECT')      

        selected_curves = [ob.name for ob in bpy.context.selected_objects if ob.type=="CURVE"]

        for name in selected_curves:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]

            bpy.context.view_layer.objects.active = ob

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            for mod in ob.modifiers:
                if mod.type == 'HOOK':
                    bpy.ops.object.hook_reset(modifier=mod.name)
            bpy.ops.object.mode_set(mode='OBJECT')                         

    def execute(self, context):
        self.reset_hooks(context)     
        self.report({'INFO'}, "Hooks Reseted")
        return{'FINISHED'}   

# Reset Armature related Lattices and Curves operator
class ARMATURE_OT_reset_deformers(bpy.types.Operator):
    bl_label = "BlenRig 5 Reset Deformers"
    bl_idname = "blenrig5.reset_deformers"
    bl_description = "Reset Armature related Lattices and Curves"
    bl_options = {'REGISTER', 'UNDO'}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def reset_deformers(self, context):

        # preparing scene
        bpy.ops.object.mode_set(mode='OBJECT')
        old_active = bpy.context.active_object
        old_selected = bpy.context.selected_objects
        old_visible_collections = [coll.name for coll in bpy.data.collections if coll.hide_viewport == False  ]
        for ob in old_selected:
            ob.select_set(False)

        # Armature related lattices and curves
        deformers_collection = []
        selected_deformers = []

        for ob in bpy.data.objects:
            if ob.type in 'LATTICE' or 'CURVE':
                for mod in ob.modifiers:
                    if mod.type in 'HOOK':
                        if mod.object.name == bpy.context.object.name:
                            # Toggle on active collections
                            for coll in bpy.data.collections:
                                for coll_ob in coll.objects:
                                    if ob.name == coll_ob.name:
                                        deformers_collection.append(coll.name)
                            for coll in bpy.data.collections:
                                if coll.name in deformers_collection:                                  
                                    coll.hide_viewport = False
                            ob.select_set(True)
                            selected_deformers.append(ob.name)

        for name in selected_deformers:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]

            bpy.context.view_layer.objects.active = ob

            # Reset Hooks
            bpy.ops.blenrig5.reset_hooks()                               

        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select_set(False)
        for coll in bpy.data.collections:
            coll.hide_viewport = True
        for coll in bpy.data.collections:
            if coll.name in old_visible_collections:
                coll.hide_viewport = False
        bpy.context.view_layer.objects.active = old_active
        for ob in old_selected:
            ob.select_set(True)        
        bpy.ops.object.mode_set(mode='POSE')  
        #Hack for updating objects
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)                                                   

    def execute(self, context):
        self.reset_deformers(context)
        self.report({'INFO'}, "Lattices and Curves Reset")
        return{'FINISHED'}


# Armature Baker operator
class ARMATURE_OT_armature_baker(bpy.types.Operator):
    bl_label = "BlenRig 5 Armature Baker"
    bl_idname = "blenrig5.armature_baker"
    bl_description = "Bake current pose to armature"
    bl_options = {'REGISTER', 'UNDO'}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def bake_armature(self, context):

        # preparing scene
        bpy.ops.object.mode_set(mode='OBJECT')
        old_active = bpy.context.active_object
        old_selected = bpy.context.selected_objects
        old_visible_collections = [coll.name for coll in bpy.context.view_layer.layer_collection.children if coll.hide_viewport == False  ]
        for ob in old_selected:
            ob.select_set(False)


        # unparenting external objects related to the armature
        deformers_collection = []
        parent_pairs = []
        for ob in bpy.data.objects:
            if ob.parent is not None:
                if ob.parent.name == bpy.context.object.name:           
                    # Toggle on active collections
                    for coll in bpy.context.scene.collection.children:
                        for coll_ob in coll.objects:
                            if ob.name == coll_ob.name:
                                deformers_collection.append(coll.name)
                    for coll in bpy.context.view_layer.layer_collection.children:
                        if coll.name in deformers_collection:
                            coll.hide_viewport = False
                    ob.select_set(True)
                    parent_pairs.append([ob, ob.parent, ob.parent_bone])
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select_set(False)
        bpy.context.view_layer.objects.active = old_active
        for ob in old_selected:
            ob.select_set(True)                         

        bpy.ops.object.mode_set(mode='POSE')
        posebones = bpy.context.object.pose.bones

        # Bake Armature
        bpy.ops.pose.armature_apply()

        arm = bpy.context.object.data

        # Reset Constraints
        for b in posebones:
            for con in b.constraints:
                if con.type not in ['LIMIT_DISTANCE', 'STRETCH_TO', 'CHILD_OF']:
                    continue
                if con.type == 'LIMIT_DISTANCE':
                    con.distance = 0
                elif con.type == 'STRETCH_TO':
                    con.rest_length = 0
                #elif con.type == 'CHILD_OF':
                    #bpy.ops.object.mode_set(mode='EDIT')
                    #arm.edit_bones.active = arm.edit_bones[b.name]
                    #bpy.ops.object.mode_set(mode='POSE')
                    #print ('"{}"'.format(con.name))
                    #bpy.ops.constraint.childof_clear_inverse(constraint=con.name, owner='BONE')
                    #bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
                    ## somehow it only works if you run it twice
                    #bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
                    #bpy.ops.object.mode_set(mode='EDIT')
                    #arm.edit_bones[b.name].select = False
        bpy.ops.object.mode_set(mode='OBJECT')
        for ob in bpy.context.selected_objects:
            ob.select_set(False)        

        # re-parenting external objects related to the armature
        for pp in parent_pairs:
            ob, parent, bone = pp
            ob.parent = parent
            ob.parent_type = 'BONE'
            ob.parent_bone == bone 
            #Reseting Hooks
            ob.select_set(True)  
            bpy.ops.blenrig5.reset_hooks()    

        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select_set(False)
        #Set to visible collections back    
        for coll in bpy.context.view_layer.layer_collection.children:
            coll.hide_viewport = True
        for coll in bpy.context.view_layer.layer_collection.children:
            if coll.name in old_visible_collections:
                coll.hide_viewport = False
        bpy.context.view_layer.objects.active = old_active
        for ob in old_selected:
            ob.select_set(True)                         

        bpy.ops.object.mode_set(mode='POSE')

    def execute(self, context):
        self.bake_armature(context)
        self.report({'INFO'}, "Baking done")
        return{'FINISHED'}

# Reset Constraints Operator
class ARMATURE_OT_reset_constraints(bpy.types.Operator):
    bl_label = "BlenRig 5 Reset Constraints"
    bl_idname = "blenrig5.reset_constraints"
    bl_description = "Reset all posebone constraints"

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')

    def invoke(self, context, event):
        pbones = context.active_object.pose.bones
        edit_bones = context.active_object.data.edit_bones
        if len(pbones) < 1:
            self.report({'INFO'}, "No bones found")
            return{'FINISHED'}

        amount = 0
        arm = bpy.context.object.data

        for pbone in pbones:
            for con in pbone.constraints:
                if con.type == 'LIMIT_DISTANCE':
                    amount += 1
                    con.distance = 0
                elif con.type == 'STRETCH_TO':
                    amount += 1
                    con.rest_length = 0
                #elif con.type == 'CHILD_OF':
                    #bpy.ops.object.mode_set(mode='EDIT')
                    #arm.edit_bones.active = arm.edit_bones[pbone.name]
                    #bpy.ops.object.mode_set(mode='POSE')
                    #print ('"{}"'.format(con.name))
                    #bpy.ops.constraint.childof_clear_inverse(constraint=con.name, owner='BONE')
                    #bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
                    ## somehow it only works if you run it twice
                    #bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
                    #bpy.ops.object.mode_set(mode='EDIT')
                    #arm.edit_bones[b.name].select = False     
                    #bpy.ops.object.mode_set(mode='POSE')                                 
        self.report({'INFO'}, str(amount) + " constraints reset")

        return{'FINISHED'}
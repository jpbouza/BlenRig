import bpy

##################################### Bone Alignment Operators #######################################

class Operator_BlenRig_Fix_Misaligned_Bones(bpy.types.Operator):    
    
    bl_idname = "blenrig5.fix_misaligned_bones"   
    bl_label = "BlenRig Fix Misaligned Bones"   
    bl_description = "Fixes misaligned bones after baking"    
    bl_options = {'REGISTER', 'UNDO',}     

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE') 

    # Save state of layers    
    active_layers = []

    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data          
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)


        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]  

    def match_heads_tails(self, context):
        props = context.window_manager.blenrig_5_props
        arm = bpy.context.active_object
        arm_data = arm.data      
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)                           
        bpy.ops.object.mode_set(mode='EDIT')        
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')     

        #Match heads   
        if arm_data.use_mirror_x == True:                
            for b in bones:      
                if b.name in selected_bones:    
                    if b.keys() != '[]':                    
                        if '_R' not in b.name:
                            if 'b_head' in b.keys():
                                for t in bones:
                                    if (t.name == b['b_head'][0]):
                                        if b['b_head'][1] == 'head':
                                            b.head = t.head
                                        if b['b_head'][1] == 'tail':
                                            b.head = t.tail      
                        #Match tails   
                        if '_R' not in b.name:   
                            if 'b_tail' in b.keys(): 
                                for t in bones:
                                    if (t.name == b['b_tail'][0]):
                                        if b['b_tail'][1] == 'head':
                                            b.tail = t.head
                                        if b['b_tail'][1] == 'tail':
                                            b.tail = t.tail  
                        #X-mirror                    
                        if '_L' in b.name:
                            b.select = 1
                            b.select_head = 1
                            b.select_tail = 1
                            bpy.ops.armature.symmetrize(direction='NEGATIVE_X')  
                            bpy.ops.armature.select_all(action='DESELECT')                                                      
        else:
            for b in bones:
                if b.name in selected_bones:
                    if 'b_head' in b.keys():   
                        #Match heads                      
                        if b['b_head']:
                            for t in bones:
                                if (t.name == b['b_head'][0]):
                                    if b['b_head'][1] == 'head':
                                        b.head = t.head
                                    if b['b_head'][1] == 'tail':
                                        b.head = t.tail                                                                            
                        #Match tails                 
                        if 'b_tail' in b.keys():
                            for t in bones:
                                if (t.name == b['b_tail'][0]):
                                    if b['b_tail'][1] == 'head':
                                        b.tail = t.head
                                    if b['b_tail'][1] == 'tail':
                                        b.tail = t.tail    

        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1      
                                
    def reset_layers(self, context):          
        arm = bpy.context.active_object
        arm_data = arm.data       

        arm_data.layers = [(x in self.active_layers) for x in range(32)]                                  

    def execute(self, context):
        self.all_layers(context)
        self.match_heads_tails(context)
        self.reset_layers(context)


        return {'FINISHED'}  

class Operator_BlenRig_Auto_Bone_Roll(bpy.types.Operator):    
    
    bl_idname = "blenrig5.auto_bone_roll"   
    bl_label = "BlenRig Auto Calulate Roll Angles"   
    bl_description = "Set roll angles to their predefined values"    
    bl_options = {'REGISTER', 'UNDO',}   

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')    

    active_layers = []

    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data          
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]      

    def blenrig_update_mirrored(self, context):  
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones        
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)   

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_L' in b.name:
                        b.select = 1
                        b.select_head = 1
                        b.select_tail = 1
                        bpy.ops.armature.symmetrize(direction='NEGATIVE_X') 
                        bpy.ops.armature.select_all(action='DESELECT') 

        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1                                 
        else:
            return False            

    def calc_roll(self, context, roll_type):
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)        
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')              

        if arm_data.use_mirror_x == True:  
            for b in bones:
                if b.name in selected_bones:
                    if '_R' not in b.name:                      
                        if b.keys() != '[]':    
                            if 'b_roll' in b.keys():  
                                if b['b_roll'][0] == roll_type:
                                    b.select = 1
                                    bpy.ops.armature.calculate_roll(type=roll_type, axis_flip=False, axis_only=False)
                                    b.select = 0    
        else:
            for b in bones:
                if b.name in selected_bones:
                    if b.keys() != '[]':  
                        if 'b_roll' in b.keys():       
                            if b['b_roll'][0] == roll_type:
                                b.select = 1
                                bpy.ops.armature.calculate_roll(type=roll_type, axis_flip=False, axis_only=False)
                                b.select = 0   
                            
        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1                                               

    def blenrig_bone_auto_roll(self, context):
        self.calc_roll(context, 'GLOBAL_POS_Y')
        self.calc_roll(context, 'GLOBAL_POS_Z') 
        self.calc_roll(context, 'GLOBAL_POS_X') 
        self.calc_roll(context, 'GLOBAL_NEG_Y') 
        self.calc_roll(context, 'GLOBAL_NEG_Z') 
        self.calc_roll(context, 'GLOBAL_NEG_X')
        self.calc_roll(context, 'POS_Y')
        self.calc_roll(context, 'POS_Z')
        self.calc_roll(context, 'POS_X')
        self.calc_roll(context, 'NEG_Y')
        self.calc_roll(context, 'NEG_Z')
        self.calc_roll(context, 'NEG_X')

    def blenrig_bone_custom_roll(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)          
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')    

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_R' not in b.name:    
                        if b.keys() != '[]':    
                            if 'b_roll' in b.keys():                         
                                if b['b_roll'][0] == 'ACTIVE':
                                    for t in bones:
                                        if (t.name == b['b_roll'][1]):
                                            arm.data.edit_bones.active = t
                                            b.select = 1
                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                            b.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT') 
        else:
            for b in bones:      
                if b.name in selected_bones: 
                    if b.keys() != '[]':                      
                        if 'b_roll' in b.keys():                            
                            if b['b_roll'][0] == 'ACTIVE':
                                for t in bones:
                                    if (t.name == b['b_roll'][1]):
                                        arm.data.edit_bones.active = t
                                        b.select = 1
                                        bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                        b.select = 0  
                                        bpy.ops.armature.select_all(action='DESELECT')   
                                
        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1                                                                    

    def blenrig_bone_cursor_roll(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)            
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')    
        #Enable cursor snapping context
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                c = bpy.context.copy()
                c['area'] = area
        else:
            print("No View3D, aborting.")

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_R' not in b.name:     
                        if b.keys() != '[]':    
                            if 'b_roll' in b.keys():                                                           
                                if b['b_roll'][0] == 'CURSOR':
                                    for t in bones:
                                        if (t.name == b['b_roll'][1]):
                                            arm.data.edit_bones.active = t
                                            bpy.ops.view3d.snap_cursor_to_active(c)
                                            b.select = 1
                                            bpy.ops.armature.calculate_roll(type='CURSOR', axis_flip=False, axis_only=False)   
                                            b.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT') 
        else:      
            for b in bones:
                if b.name in selected_bones:   
                    if b.keys() != '[]':    
                        if 'b_roll' in b.keys():                                               
                            if b['b_roll'][0] == 'CURSOR':
                                for t in bones:
                                        if (t.name == b['b_roll'][1]):
                                            arm.data.edit_bones.active = t
                                            bpy.ops.view3d.snap_cursor_to_active(c)
                                            b.select = 1
                                            bpy.ops.armature.calculate_roll(type='CURSOR', axis_flip=False, axis_only=False)   
                                            b.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT') 
                            
        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1 

    def blenrig_bone_align(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)           
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')        

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_R' not in b.name:   
                        if b.keys() != '[]':                                        
                            if 'b_align' in b.keys():
                                if b['b_align'][0] != "''":                             
                                    for t in bones:
                                        if (t.name == b['b_align'][0]):
                                            arm.data.edit_bones.active = t
                                            b.select = 1
                                            bpy.ops.armature.align()  
                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                            b.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT') 
                                            for t2 in bones:
                                                if t2.keys() != '[]':                                        
                                                    if 'b_align' in t2.keys():                                                
                                                        if (b.name == t2['b_head'][0]):
                                                            if t2['b_head'][1] == 'head':
                                                                t2.head = b.head
                                                            if t2['b_head'][1] == 'tail':
                                                                t2.head = b.tail    
                                                        if (b.name == t2['b_tail'][0]):
                                                            if t2['b_tail'][1] == 'head':
                                                                t2.tail = b.head
                                                            if t2['b_head'][1] == 'tail':
                                                                t2.tail = b.tail                                                                                           
                                                                arm.data.edit_bones.active = t
                                                                t2.select = 1
                                                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                                                t2.select = 0  
                                                                bpy.ops.armature.select_all(action='DESELECT')                                      
        else: 
            for b in bones:
                if b.name in selected_bones:      
                    if b.keys() != '[]':                                        
                        if 'b_align' in b.keys():   
                            if b['b_align'][0] != "''":                             
                                for t in bones:
                                    if (t.name == b['b_align'][0]):
                                        arm.data.edit_bones.active = t
                                        b.select = 1
                                        bpy.ops.armature.align()  
                                        bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                        b.select = 0  
                                        bpy.ops.armature.select_all(action='DESELECT') 
                                        for t2 in bones:
                                            if t2.keys() != '[]':                                        
                                                if 'b_align' in t2.keys():                                               
                                                    if (b.name == t2['b_head'][0]):
                                                        if t2['b_head'][1] == 'head':
                                                            t2.head = b.head
                                                        if t2['b_head'][1] == 'tail':
                                                            t2.head = b.tail    
                                                    if (b.name == t2['b_tail'][0]):
                                                        if t2['b_tail'][1] == 'head':
                                                            t2.tail = b.head
                                                        if t2['b_head'][1] == 'tail':
                                                            t2.tail = b.tail                                                                                           
                                                            arm.data.edit_bones.active = t
                                                            t2.select = 1
                                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                                            t2.select = 0  
                                                            bpy.ops.armature.select_all(action='DESELECT')                                                                                                          

        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1 

    def reset_layers(self, context):          
        arm = bpy.context.active_object
        arm_data = arm.data        
        arm_data.layers = [(x in self.active_layers) for x in range(32)]     

    def execute(self, context):
        self.all_layers(context)        
        self.blenrig_bone_auto_roll(context)
        self.blenrig_bone_custom_roll(context)
        self.blenrig_bone_cursor_roll(context)
        self.blenrig_bone_align(context)    
        self.blenrig_update_mirrored(context) 
        self.reset_layers(context)     
                                                                                                                                                                                                                                    

        return {'FINISHED'}  

class Operator_BlenRig_Custom_Bone_Roll(bpy.types.Operator):    
    
    bl_idname = "blenrig5.custom_bone_roll"   
    bl_label = "BlenRig User Defined Roll Angles"   
    bl_description = "Calulate roll angles and aligns defined by user"    
    bl_options = {'REGISTER', 'UNDO',}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')  

    active_layers = []
    
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data          
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

            
        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]  

    def blenrig_update_mirrored(self, context):  
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones        
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)   

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_L' in b.name:
                        b.select = 1
                        b.select_head = 1
                        b.select_tail = 1
                        bpy.ops.armature.symmetrize(direction='NEGATIVE_X') 
                        bpy.ops.armature.select_all(action='DESELECT')    

        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1                         

        else:
            return False     

    def blenrig_bone_custom_roll(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)          
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')    

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_R' not in b.name:    
                        if b.keys() != '[]':    
                            if 'b_roll' in b.keys():                         
                                if b['b_roll'][0] == 'ACTIVE':
                                    for t in bones:
                                        if (t.name == b['b_roll'][1]):
                                            arm.data.edit_bones.active = t
                                            b.select = 1
                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                            b.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT') 
        else:
            for b in bones:      
                if b.name in selected_bones: 
                    if b.keys() != '[]':                      
                        if 'b_roll' in b.keys():                            
                            if b['b_roll'][0] == 'ACTIVE':
                                for t in bones:
                                    if (t.name == b['b_roll'][1]):
                                        arm.data.edit_bones.active = t
                                        b.select = 1
                                        bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                        b.select = 0  
                                        bpy.ops.armature.select_all(action='DESELECT')   
                                
        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1     

    def blenrig_bone_align(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)           
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')        

        if arm_data.use_mirror_x == True:
            for b in bones:
                if b.name in selected_bones:
                    if '_R' not in b.name:   
                        if b.keys() != '[]':                                        
                            if 'b_align' in b.keys():
                                if b['b_align'][0] != "''":                             
                                    for t in bones:
                                        if (t.name == b['b_align'][0]):
                                            arm.data.edit_bones.active = t
                                            b.select = 1
                                            bpy.ops.armature.align()  
                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                            b.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT') 
                                            for t2 in bones:
                                                if t2.keys() != '[]':                                        
                                                    if 'b_align' in t2.keys():                                                
                                                        if (b.name == t2['b_head'][0]):
                                                            if t2['b_head'][1] == 'head':
                                                                t2.head = b.head
                                                            if t2['b_head'][1] == 'tail':
                                                                t2.head = b.tail    
                                                        if (b.name == t2['b_tail'][0]):
                                                            if t2['b_tail'][1] == 'head':
                                                                t2.tail = b.head
                                                            if t2['b_head'][1] == 'tail':
                                                                t2.tail = b.tail                                                                                           
                                                                arm.data.edit_bones.active = t
                                                                t2.select = 1
                                                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                                                t2.select = 0  
                                                                bpy.ops.armature.select_all(action='DESELECT')                                      
        else: 
            for b in bones:
                if b.name in selected_bones:      
                    if b.keys() != '[]':                                        
                        if 'b_align' in b.keys():   
                            if b['b_align'][0] != "''":                             
                                for t in bones:
                                    if (t.name == b['b_align'][0]):
                                        arm.data.edit_bones.active = t
                                        b.select = 1
                                        bpy.ops.armature.align()  
                                        bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                        b.select = 0  
                                        bpy.ops.armature.select_all(action='DESELECT') 
                                        for t2 in bones:
                                            if t2.keys() != '[]':                                        
                                                if 'b_align' in t2.keys():                                               
                                                    if (b.name == t2['b_head'][0]):
                                                        if t2['b_head'][1] == 'head':
                                                            t2.head = b.head
                                                        if t2['b_head'][1] == 'tail':
                                                            t2.head = b.tail    
                                                    if (b.name == t2['b_tail'][0]):
                                                        if t2['b_tail'][1] == 'head':
                                                            t2.tail = b.head
                                                        if t2['b_head'][1] == 'tail':
                                                            t2.tail = b.tail                                                                                           
                                                            arm.data.edit_bones.active = t
                                                            t2.select = 1
                                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                                            t2.select = 0  
                                                            bpy.ops.armature.select_all(action='DESELECT')                                                                                                          

        # Restore selection    
        if props.align_selected_only == 1:                                
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1 
                    b.select_tail = 1 

    def reset_layers(self, context):          
        arm = bpy.context.active_object
        arm_data = arm.data        
        arm_data.layers = [(x in self.active_layers) for x in range(32)]     

    def execute(self, context):
        self.all_layers(context)         
        self.blenrig_bone_custom_roll(context)
        self.blenrig_bone_align(context)
        self.blenrig_update_mirrored(context)                 
        self.reset_layers(context)                                                                                                                                                                                                                                     

        return {'FINISHED'}    


class Operator_BlenRig_Store_Roll_Angles(bpy.types.Operator):    
    
    bl_idname = "blenrig5.store_roll_angles"   
    bl_label = "BlenRig Store Roll Angles"   
    bl_description = "Store current roll angles for each bone"    
    bl_options = {'REGISTER', 'UNDO',}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')  

    def blenrig_store_rolls(self, context):  
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones        
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)   

        for b in bones:
            if b.name in selected_bones:
                b["b_roll_angle"] = ['x'.replace('x', str(b.roll))]

    def execute(self, context):
        self.blenrig_store_rolls(context)                                                                                                                                                                                                                                           

        return {'FINISHED'}    


class Operator_BlenRig_Restore_Roll_Angles(bpy.types.Operator):    

    bl_idname = "blenrig5.restore_roll_angles"   
    bl_label = "BlenRig restore Roll Angles"   
    bl_description = "Retore roll angles to the ones saved in each bone"    
    bl_options = {'REGISTER', 'UNDO',}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')  

    def blenrig_restore_rolls(self, context):  
        props = context.window_manager.blenrig_5_props 
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones        
        selected_bones = []           
        if props.align_selected_only == 1:
            for b in bpy.context.selected_editable_bones:
                selected_bones.append(b.name)
        else:
            for b in bones:
                selected_bones.append(b.name)   

        for b in bones:
            if b.name in selected_bones:
                b.roll = float(b["b_roll_angle"][0])

    def execute(self, context):
        self.blenrig_restore_rolls(context)                                                                                                                                                                                                                                           

        return {'FINISHED'}    

##################### Dynamic Shaping Values Reset ############################

class Operator_BlenRig_Reset_Dynamic(bpy.types.Operator):    

    bl_idname = "blenrig5.reset_dynamic_shaping"   
    bl_label = "BlenRig Reset Dynamic Shaping"   
    bl_description = "Reset Dynamic Shaping values"    
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')

    def reset_dynamic_values(self, context):

        scene = bpy.context.view_layer
        arm = bpy.context.active_object
        pbones = arm.pose.bones

        #Legacy Rig
        if arm.data['rig_type'] == 'Biped':
            if str(arm.data['rig_version']) < "1.1.0":  
                pbones["properties_head"]["flex_head_scale"] = 1.0
                pbones["properties_head"]["flex_neck_length"] = 1.0
                pbones["properties_head"]["flex_neck_width"] = 1.0
                pbones["properties_arm_R"]["flex_arm_length_R"] = 1.0
                pbones["properties_arm_R"]["flex_arm_uniform_scale_R"] = 1.0
                pbones["properties_arm_R"]["flex_arm_width_R"] = 1.0
                pbones["properties_arm_R"]["flex_forearm_length_R"] = 1.0
                pbones["properties_arm_R"]["flex_forearm_width_R"] = 1.0
                pbones["properties_arm_R"]["flex_hand_scale_R"] = 1.0
                pbones["properties_torso"]["flex_torso_height"] = 0.0
                pbones["properties_torso"]["flex_torso_scale"] = 1.0
                pbones["properties_torso"]["flex_chest_width"] = 1.0
                pbones["properties_torso"]["flex_ribs_width"] = 1.0
                pbones["properties_torso"]["flex_waist_width"] = 1.0
                pbones["properties_torso"]["flex_pelvis_width"] = 1.0
                pbones["properties_arm_L"]["flex_arm_length_L"] = 1.0
                pbones["properties_arm_L"]["flex_arm_uniform_scale_L"] = 1.0
                pbones["properties_arm_L"]["flex_arm_width_L"] = 1.0
                pbones["properties_arm_L"]["flex_forearm_length_L"] = 1.0
                pbones["properties_arm_L"]["flex_forearm_width_L"] = 1.0
                pbones["properties_arm_L"]["flex_hand_scale_L"] = 1.0
                pbones["properties_leg_R"]["flex_leg_uniform_scale_R"] = 1.0
                pbones["properties_leg_R"]["flex_thigh_length_R"] = 1.0
                pbones["properties_leg_R"]["flex_thigh_width_R"] = 1.0
                pbones["properties_leg_R"]["flex_shin_length_R"] = 1.0
                pbones["properties_leg_R"]["flex_shin_width_R"] = 1.0
                pbones["properties_leg_R"]["flex_foot_scale_R"] = 1.0
                pbones["properties_leg_R"]["flex_foot_loc_R"] = 0.0
                pbones["properties_leg_L"]["flex_leg_uniform_scale_L"] = 1.0
                pbones["properties_leg_L"]["flex_thigh_length_L"] = 1.0
                pbones["properties_leg_L"]["flex_thigh_width_L"] = 1.0
                pbones["properties_leg_L"]["flex_shin_length_L"] = 1.0
                pbones["properties_leg_L"]["flex_shin_width_L"] = 1.0
                pbones["properties_leg_L"]["flex_foot_scale_L"] = 1.0
                pbones["properties_leg_L"]["flex_foot_loc_L"] = 0.0  
                scene.update() 
        #1.1.0 Rig                
        if arm.data['rig_type'] == 'Biped':
            if str(arm.data['rig_version']) >= "1.1.0":  
                pbones["properties_head"]["dynamic_head_scale"] = 1.0
                pbones["properties_head"]["dynamic_neck_length"] = 1.0
                pbones["properties_head"]["dynamic_neck_width"] = 1.0
                pbones["properties_arm_R"]["dynamic_arm_length_R"] = 1.0
                pbones["properties_arm_R"]["dynamic_arm_uniform_scale_R"] = 1.0
                pbones["properties_arm_R"]["dynamic_arm_width_R"] = 1.0
                pbones["properties_arm_R"]["dynamic_forearm_length_R"] = 1.0
                pbones["properties_arm_R"]["dynamic_forearm_width_R"] = 1.0
                pbones["properties_arm_R"]["dynamic_hand_scale_R"] = 1.0
                pbones["properties_torso"]["dynamic_torso_height"] = 0.0
                pbones["properties_torso"]["dynamic_torso_scale"] = 1.0
                pbones["properties_torso"]["dynamic_chest_width"] = 1.0
                pbones["properties_torso"]["dynamic_ribs_width"] = 1.0
                pbones["properties_torso"]["dynamic_waist_width"] = 1.0
                pbones["properties_torso"]["dynamic_pelvis_width"] = 1.0
                pbones["properties_arm_L"]["dynamic_arm_length_L"] = 1.0
                pbones["properties_arm_L"]["dynamic_arm_uniform_scale_L"] = 1.0
                pbones["properties_arm_L"]["dynamic_arm_width_L"] = 1.0
                pbones["properties_arm_L"]["dynamic_forearm_length_L"] = 1.0
                pbones["properties_arm_L"]["dynamic_forearm_width_L"] = 1.0
                pbones["properties_arm_L"]["dynamic_hand_scale_L"] = 1.0
                pbones["properties_leg_R"]["dynamic_leg_uniform_scale_R"] = 1.0
                pbones["properties_leg_R"]["dynamic_thigh_length_R"] = 1.0
                pbones["properties_leg_R"]["dynamic_thigh_width_R"] = 1.0
                pbones["properties_leg_R"]["dynamic_shin_length_R"] = 1.0
                pbones["properties_leg_R"]["dynamic_shin_width_R"] = 1.0
                pbones["properties_leg_R"]["dynamic_foot_scale_R"] = 1.0
                pbones["properties_leg_R"]["dynamic_foot_loc_R"] = 0.0
                pbones["properties_leg_L"]["dynamic_leg_uniform_scale_L"] = 1.0
                pbones["properties_leg_L"]["dynamic_thigh_length_L"] = 1.0
                pbones["properties_leg_L"]["dynamic_thigh_width_L"] = 1.0
                pbones["properties_leg_L"]["dynamic_shin_length_L"] = 1.0
                pbones["properties_leg_L"]["dynamic_shin_width_L"] = 1.0
                pbones["properties_leg_L"]["dynamic_foot_scale_L"] = 1.0
                pbones["properties_leg_L"]["dynamic_foot_loc_L"] = 0.0  
                scene.update()                 

    def update_scene(self, context):
        current = bpy.context.scene.frame_current
        bpy.context.scene.frame_set(2, subframe=0)
        bpy.context.scene.frame_set(current, subframe=0)

    def execute(self, context):
        self.reset_dynamic_values(context)
        self.update_scene(context)

        return {'FINISHED'}
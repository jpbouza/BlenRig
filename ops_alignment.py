import bpy


##################################### Bone Alignment Operators #######################################

class Operator_BlenRig_Fix_Misaligned_Bones(bpy.types.Operator):

    bl_idname = "blenrig.fix_misaligned_bones"
    bl_label = "BlenRig Fix Misaligned Bones"
    bl_description = "Fixes misaligned bones after baking"
    bl_options = {'REGISTER', 'UNDO',}

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')

    active_layers = []

    # Save current layers then enable all
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]

    #Mirror Armature from L to R if X-Mirror is enabled
    def blenrig_update_mirrored(self, context):
        props = context.window_manager.blenrig_6_props
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


    #Match Heads and Tails
    def match_heads_tails(self, context):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        props = context.window_manager.blenrig_6_props
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

        HEADS_DICT = {}
        TAILS_DICT = {}

        # #Create Heads Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_head' in b.keys():
        #                             if b['b_head'][0] != "''":
        #                                 HEADS_DICT[b['b_head'][0]] = []

        # #Populate Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_head' in b.keys():
        #                             if b['b_head'][0] != "''":
        #                                 if b['b_head'][0] in HEADS_DICT:
        #                                     HEADS_DICT[b['b_head'][0]].append(b.name)

        #     #Align Bones to Heads
        #     for b_act in HEADS_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 bone_head_vec = b.head
        #                 bone_tail_vec = b.tail
        #         for b_listed in HEADS_DICT[b_act]:
        #             for b_sel in bones:
        #                 if b_sel.name == b_listed:
        #                     if b_sel['b_head'][1] == 'head':
        #                         b_sel.head = bone_head_vec
        #                         print (b_sel.name)
        #                     if b_sel['b_head'][1] == 'tail':
        #                         b_sel.head = bone_tail_vec
        #                         print (b_sel.name)

        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'HEADS', 'XXXXXXXXXXXXXXXXXX', '\n')

        # else:
        #Create Heads Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_head' in b.keys():
                        if b['b_head'][0] != "''":
                            HEADS_DICT[b['b_head'][0]] = []

        #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_head' in b.keys():
                        if b['b_head'][0] != "''":
                            if b['b_head'][0] in HEADS_DICT:
                                HEADS_DICT[b['b_head'][0]].append(b.name)

        #Align Bones to Heads
        for b_act in HEADS_DICT:
            for b in bones:
                if b.name == b_act:
                    bone_head_vec = b.head
                    bone_tail_vec = b.tail
            for b_listed in HEADS_DICT[b_act]:
                for b_sel in bones:
                    if b_sel.name == b_listed:
                        if b_sel['b_head'][1] == 'head':
                            b_sel.head = bone_head_vec
                            print (b_sel.name)
                        if b_sel['b_head'][1] == 'tail':
                            b_sel.head = bone_tail_vec
                            print (b_sel.name)

            print ('XXXXXXXXXXXXXXXXXX', b_act, 'HEADS', 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # #Create TAILS Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_tail' in b.keys():
        #                             if b['b_tail'][0] != "''":
        #                                 TAILS_DICT[b['b_tail'][0]] = []

        # #Populate Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_tail' in b.keys():
        #                             if b['b_tail'][0] != "''":
        #                                 if b['b_tail'][0] in TAILS_DICT:
        #                                     TAILS_DICT[b['b_tail'][0]].append(b.name)

        #     #Align Bones to Heads
        #     for b_act in TAILS_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 bone_head_vec = b.head
        #                 bone_tail_vec = b.tail
        #         for b_listed in TAILS_DICT[b_act]:
        #             for b_sel in bones:
        #                 if b_sel.name == b_listed:
        #                     if b_sel['b_tail'][1] == 'head':
        #                         b_sel.tail = bone_head_vec
        #                         print (b_sel.name)
        #                     if b_sel['b_tail'][1] == 'tail':
        #                         b_sel.tail = bone_tail_vec
        #                         print (b_sel.name)

        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'TAILS', 'XXXXXXXXXXXXXXXXXX', '\n')

        # else:
        #Create TAILS Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_tail' in b.keys():
                        if b['b_tail'][0] != "''":
                            TAILS_DICT[b['b_tail'][0]] = []

    #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_tail' in b.keys():
                        if b['b_tail'][0] != "''":
                            if b['b_tail'][0] in TAILS_DICT:
                                TAILS_DICT[b['b_tail'][0]].append(b.name)

        #Align Bones to Heads
        for b_act in TAILS_DICT:
            for b in bones:
                if b.name == b_act:
                    bone_head_vec = b.head
                    bone_tail_vec = b.tail
            for b_listed in TAILS_DICT[b_act]:
                for b_sel in bones:
                    if b_sel.name == b_listed:
                        if b_sel['b_tail'][1] == 'head':
                            b_sel.tail = bone_head_vec
                            print (b_sel.name)
                        if b_sel['b_tail'][1] == 'tail':
                            b_sel.tail = bone_tail_vec
                            print (b_sel.name)

            print ('XXXXXXXXXXXXXXXXXX', b_act, 'TAILS', 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1

        win.progress_end()

    def reset_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data

        arm_data.layers = [(x in self.active_layers) for x in range(32)]

    def execute(self, context):
        self.all_layers(context)
        self.match_heads_tails(context)
        # self.blenrig_update_mirrored(context)
        self.reset_layers(context)


        return {'FINISHED'}

class Operator_BlenRig_Auto_Bone_Roll(bpy.types.Operator):

    bl_idname = "blenrig.auto_bone_roll"
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

    # Save current layers then enable all
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]

    #Mirror Armature from L to R if X-Mirror is enabled
    def blenrig_update_mirrored(self, context):
        props = context.window_manager.blenrig_6_props
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

    #Assign Bone Rolls from Global Axes
    def global_roll(self, context, roll_type):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_6_props
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

        B_List = []

        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == roll_type:
                            B_List.append(b.name)
                            i=i+1
                            win.progress_update(i)
        
        win.progress_end()

        for B in B_List:
            for b in bones:
                if b.name == B:
                    print (b.name)
                    b.select = 1
                    i=i+1
                    win.progress_update(i)
        
        win.progress_end()

        bpy.ops.armature.calculate_roll(type= roll_type, axis_flip=False, axis_only=False)
        bpy.ops.armature.select_all(action='DESELECT')

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    i=i+1
                    win.progress_update(i)

            win.progress_end()

    def blenrig_bone_global_roll(self, context):
        print ('### Global Roll ###', '\n', '\n')
        self.global_roll(context, 'GLOBAL_POS_Y')
        print ('XXXXXXXXXXXXXXXXXX', 'GLOBAL_POS_Y', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'GLOBAL_POS_Z')
        print ('XXXXXXXXXXXXXXXXXX', 'GLOBAL_POS_Z', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'GLOBAL_POS_X')
        print ('XXXXXXXXXXXXXXXXXX', 'GLOBAL_POS_X', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'GLOBAL_NEG_Y')
        print ('XXXXXXXXXXXXXXXXXX', 'GLOBAL_NEG_Y', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'GLOBAL_NEG_Z')
        print ('XXXXXXXXXXXXXXXXXX', 'GLOBAL_NEG_Z', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'GLOBAL_NEG_X')
        print ('XXXXXXXXXXXXXXXXXX', 'GLOBAL_NEG_X', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'POS_Z')
        print ('XXXXXXXXXXXXXXXXXX', 'POS_Z', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'POS_X')
        print ('XXXXXXXXXXXXXXXXXX', 'POS_X', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'NEG_Z')
        print ('XXXXXXXXXXXXXXXXXX', 'NEG_Z', 'XXXXXXXXXXXXXXXXXX', '\n')
        self.global_roll(context, 'NEG_X')
        print ('XXXXXXXXXXXXXXXXXX', 'NEG_X', 'XXXXXXXXXXXXXXXXXX', '\n')

    #Assign Bone Roll for Bones that must have the same Roll of other Bone (Active Bone)
    def blenrig_bone_custom_roll(self, context):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_6_props
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

        print ('### Active Roll ###', '\n', '\n')

        B_DICT = {}

        # #Create Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_roll' in b.keys():
        #                             if b['b_roll'][0] == 'ACTIVE':
        #                                 B_DICT[b['b_roll'][1]] = []
        #     #Populate Dictionary
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_roll' in b.keys():
        #                             if b['b_roll'][0] == 'ACTIVE':
        #                                 if b['b_roll'][1] in B_DICT:
        #                                     B_DICT[b['b_roll'][1]].append(b.name)
        #     #Perfrom Bone Roll
        #     for b_act in B_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 arm.data.edit_bones.active = b
        #                 for b_listed in B_DICT[b_act]:
        #                     for b_sel in bones:
        #                         if b_sel.name == b_listed:
        #                             print (b_sel.name)
        #                             b_sel.select = 1

        #         bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)
        #         bpy.ops.armature.select_all(action='DESELECT')
        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')

        # else:
        #Create Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == 'ACTIVE':
                            B_DICT[b['b_roll'][1]] = []
        #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == 'ACTIVE':
                            if b['b_roll'][1] in B_DICT:
                                B_DICT[b['b_roll'][1]].append(b.name)
        #Perfrom Bone Roll
        for b_act in B_DICT:
            print (b_act)
            for b in bones:
                if b.name == b_act:
                    print (b_act)
                    arm.data.edit_bones.active = b
                    for b_listed in B_DICT[b_act]:
                        for b_sel in bones:
                            if b_sel.name == b_listed:
                                print (b_sel.name)
                                b_sel.select = 1

            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)
            arm.data.edit_bones.active = None
            bpy.ops.armature.select_all(action='DESELECT')
            print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    
        win.progress_end()

    #Assign Rolls by Cursor position
    def blenrig_bone_cursor_roll(self, context):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_6_props
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

        print ('### Cursor Roll ###', '\n', '\n')

        B_DICT = {}

        # #Create Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_roll' in b.keys():
        #                             if b['b_roll'][0] == 'CURSOR':
        #                                 B_DICT[b['b_roll'][1]] = []
        #     #Populate Dictionary
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_roll' in b.keys():
        #                             if b['b_roll'][0] == 'CURSOR':
        #                                 if b['b_roll'][1] in B_DICT:
        #                                     B_DICT[b['b_roll'][1]].append(b.name)
        #     #Perfrom Bone Roll
        #     for b_act in B_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 arm.data.edit_bones.active = b
        #                 bpy.ops.view3d.snap_cursor_to_active(c)
        #                 for b_listed in B_DICT[b_act]:
        #                     for b_sel in bones:
        #                         if b_sel.name == b_listed:
        #                             print (b_sel.name)
        #                             b_sel.select = 1

        #         bpy.ops.armature.calculate_roll(type='CURSOR', axis_flip=False, axis_only=False)
        #         bpy.ops.armature.select_all(action='DESELECT')
        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')


        # else:
        #Create Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == 'CURSOR':
                            B_DICT[b['b_roll'][1]] = []
        #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == 'CURSOR':
                            if b['b_roll'][1] in B_DICT:
                                B_DICT[b['b_roll'][1]].append(b.name)
        #Perfrom Bone Roll
        for b_act in B_DICT:
            print (b_act)
            for b in bones:
                if b.name == b_act:
                    print (b_act)
                    arm.data.edit_bones.active = b
                    bpy.ops.view3d.snap_cursor_to_active(c)
                    for b_listed in B_DICT[b_act]:
                        for b_sel in bones:
                            if b_sel.name == b_listed:
                                print (b_sel.name)
                                b_sel.select = 1

            bpy.ops.armature.calculate_roll(type='CURSOR', axis_flip=False, axis_only=False)
            arm.data.edit_bones.active = None
            bpy.ops.armature.select_all(action='DESELECT')
            print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
        
        win.progress_end()

    #Perform Bone Alignment for Bones that have to be aligned to other Bones
    def blenrig_bone_align(self, context):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_6_props
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

        print ('### Bone Align ###', '\n', '\n')

        B_DICT = {}

        # #Create Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_align' in b.keys():
        #                             if b['b_align'][0] != "''":
        #                                 B_DICT[b['b_align'][0]] = []
        #     #Populate Dictionary
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_align' in b.keys():
        #                             if b['b_align'] != "['']":
        #                                 if b['b_align'][0] in B_DICT:
        #                                     B_DICT[b['b_align'][0]].append(b.name)
        #     #Perfrom Bone Alignment
        #     for b_act in B_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 arm.data.edit_bones.active = b
        #                 for b_listed in B_DICT[b_act]:
        #                     for b_sel in bones:
        #                         if b_sel.name == b_listed:
        #                             print (b_sel.name)
        #                             b_sel.select = 1

        #         bpy.ops.armature.align()
        #         bpy.ops.armature.select_all(action='DESELECT')
        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')

        # else:
        #Create Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_align' in b.keys():
                        if b['b_align'] == ['']:
                            print ('empty')
                        else:
                            B_DICT[b['b_align'][0]] = []
        #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_align' in b.keys():
                        if b['b_align'] == ['']:
                            print ('empty')
                        else:
                            if b['b_align'][0] in B_DICT:
                                B_DICT[b['b_align'][0]].append(b.name)
        #Perfrom Bone Alignment
        for b_act in B_DICT:
            print (b_act)
            for b in bones:
                if b.name == b_act:
                    print (b_act)
                    arm.data.edit_bones.active = b
                    for b_listed in B_DICT[b_act]:
                        for b_sel in bones:
                            if b_sel.name == b_listed:
                                print (b_sel.name)
                                b_sel.select = 1

            bpy.ops.armature.align()
            arm.data.edit_bones.active = None
            bpy.ops.armature.select_all(action='DESELECT')
            print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
        
        win.progress_end()

    #Reset layers to old state
    def reset_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data
        arm_data.layers = [(x in self.active_layers) for x in range(32)]

    #Execute functions
    def execute(self, context):
        self.all_layers(context)
        self.blenrig_bone_global_roll(context)
        self.blenrig_bone_custom_roll(context)
        self.blenrig_bone_cursor_roll(context)
        self.blenrig_bone_align(context)
        # self.blenrig_update_mirrored(context)
        self.reset_layers(context)
        self.report({'INFO'}, "Calc Rolls done")
        return {'FINISHED'}

class Operator_BlenRig_Custom_Bone_Roll(bpy.types.Operator):

    bl_idname = "blenrig.custom_bone_roll"
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

    # Save current layers then enable all
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]

    #Mirror Armature from L to R if X-Mirror is enabled
    def blenrig_update_mirrored(self, context):
        props = context.window_manager.blenrig_6_props
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

    #Assign Bone Roll for Bones that must have the same Roll of other Bone (Active Bone)
    def blenrig_bone_custom_roll(self, context):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_6_props
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

        print ('### Active Roll ###', '\n', '\n')

        B_DICT = {}

        # #Create Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_roll' in b.keys():
        #                             if b['b_roll'][0] == 'ACTIVE':
        #                                 B_DICT[b['b_roll'][1]] = []
        #     #Populate Dictionary
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_roll' in b.keys():
        #                             if b['b_roll'][0] == 'ACTIVE':
        #                                 if b['b_roll'][1] in B_DICT:
        #                                     B_DICT[b['b_roll'][1]].append(b.name)
        #     #Perfrom Bone Roll
        #     for b_act in B_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 arm.data.edit_bones.active = b
        #                 for b_listed in B_DICT[b_act]:
        #                     for b_sel in bones:
        #                         if b_sel.name == b_listed:
        #                             print (b_sel.name)
        #                             b_sel.select = 1

        #         bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)
        #         bpy.ops.armature.select_all(action='DESELECT')
        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')

        # else:
        #Create Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == 'ACTIVE':
                            B_DICT[b['b_roll'][1]] = []
        #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_roll' in b.keys():
                        if b['b_roll'][0] == 'ACTIVE':
                            if b['b_roll'][1] in B_DICT:
                                B_DICT[b['b_roll'][1]].append(b.name)
        #Perfrom Bone Roll
        for b_act in B_DICT:
            print (b_act)
            for b in bones:
                if b.name == b_act:
                    print (b_act)
                    arm.data.edit_bones.active = b
                    for b_listed in B_DICT[b_act]:
                        for b_sel in bones:
                            if b_sel.name == b_listed:
                                print (b_sel.name)
                                b_sel.select = 1

            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)
            arm.data.edit_bones.active = None
            bpy.ops.armature.select_all(action='DESELECT')
            print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    i = i+1
                    win.progress_update(i)
                    
        win.progress_end()


    #Perform Bone Alignment for Bones that have to be aligned to other Bones
    def blenrig_bone_align(self, context):
        win = bpy.context.window_manager
        win.progress_begin(0, 100)
        i=0
        bpy.ops.object.mode_set(mode='EDIT')
        props = context.window_manager.blenrig_6_props
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

        print ('### Bone Align ###', '\n', '\n')

        B_DICT = {}

        # #Create Dictionary
        # if arm_data.use_mirror_x == True:
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_align' in b.keys():
        #                             if b['b_align'][0] != "''":
        #                                 B_DICT[b['b_align'][0]] = []
        #     #Populate Dictionary
        #     for b in bones:
        #         if b.name in selected_bones:
        #             if '_R' not in b.name:
        #                 if b.name in selected_bones:
        #                     if b.keys() != '[]':
        #                         if 'b_align' in b.keys():
        #                             if b['b_align'] != "['']":
        #                                 if b['b_align'][0] in B_DICT:
        #                                     B_DICT[b['b_align'][0]].append(b.name)
        #     #Perfrom Bone Alignment
        #     for b_act in B_DICT:
        #         for b in bones:
        #             if b.name == b_act:
        #                 arm.data.edit_bones.active = b
        #                 for b_listed in B_DICT[b_act]:
        #                     for b_sel in bones:
        #                         if b_sel.name == b_listed:
        #                             print (b_sel.name)
        #                             b_sel.select = 1

        #         bpy.ops.armature.align()
        #         bpy.ops.armature.select_all(action='DESELECT')
        #         print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')

        # else:
        #Create Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_align' in b.keys():
                        if b['b_align'] == ['']:
                            print ('empty')
                        else:
                            B_DICT[b['b_align'][0]] = []
        #Populate Dictionary
        for b in bones:
            if b.name in selected_bones:
                if b.keys() != '[]':
                    if 'b_align' in b.keys():
                        if b['b_align'] == ['']:
                            print ('empty')
                        else:
                            if b['b_align'][0] in B_DICT:
                                B_DICT[b['b_align'][0]].append(b.name)
        #Perfrom Bone Alignment
        for b_act in B_DICT:
            print (b_act)
            for b in bones:
                if b.name == b_act:
                    print (b_act)
                    arm.data.edit_bones.active = b
                    for b_listed in B_DICT[b_act]:
                        for b_sel in bones:
                            if b_sel.name == b_listed:
                                print (b_sel.name)
                                b_sel.select = 1

            bpy.ops.armature.align()
            arm.data.edit_bones.active = None
            bpy.ops.armature.select_all(action='DESELECT')
            print ('XXXXXXXXXXXXXXXXXX', b_act, 'XXXXXXXXXXXXXXXXXX', '\n')
            i = i+1
            win.progress_update(i)

        # Restore selection
        if props.align_selected_only == 1:
            for b in bones:
                if b.name in selected_bones:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    i = i+1
                    win.progress_update(i)
        
        win.progress_end()

    #Reset layers to old state
    def reset_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data
        arm_data.layers = [(x in self.active_layers) for x in range(32)]

    #Execute functions
    def execute(self, context):
        self.all_layers(context)
        self.blenrig_bone_custom_roll(context)
        self.blenrig_bone_align(context)
        #self.blenrig_update_mirrored(context)
        self.reset_layers(context)
        self.report({'INFO'}, "Custom Aligns done")
        return {'FINISHED'}

class Operator_BlenRig_Store_Roll_Angles(bpy.types.Operator):

    bl_idname = "blenrig.store_roll_angles"
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
        props = context.window_manager.blenrig_6_props
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
        self.report({'INFO'}, "Store Roll Angles Done")
        return {'FINISHED'}


class Operator_BlenRig_Restore_Roll_Angles(bpy.types.Operator):

    bl_idname = "blenrig.restore_roll_angles"
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
        props = context.window_manager.blenrig_6_props
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

    bl_idname = "blenrig.reset_dynamic_shaping"
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
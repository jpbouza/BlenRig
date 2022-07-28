import bpy
from math import radians

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
        win.progress_begin(0, 1000)
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
        win.progress_begin(0, 1000)
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
        win.progress_begin(0, 1000)
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
        win.progress_begin(0, 1000)
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
        win.progress_begin(0, 1000)
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
        win.progress_begin(0, 1000)
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
        win.progress_begin(0, 1000)
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

        #Armature Refresh Hack
        def refresh_hack():
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='POSE')

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
                #scene.update()
                refresh_hack()
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
                #scene.update()
                refresh_hack()

    def update_scene(self, context):
        current = bpy.context.scene.frame_current
        bpy.context.scene.frame_set(2, subframe=0)
        bpy.context.scene.frame_set(current, subframe=0)

    def execute(self, context):
        self.reset_dynamic_values(context)
        self.update_scene(context)

        return {'FINISHED'}

#### Mirror Volume Preservation Constraint Values Operator ####

class Operator_Mirror_VP_Constraints(bpy.types.Operator):

    bl_idname = "mirror.vp_constraints"
    bl_label = "BlenRig Mirror Volume Preservation Constraints L to R"
    bl_description = "Mirror Volume Preservation Constraints L to R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    def execute(self, context):
        pbones = bpy.context.active_object.pose.bones
        for br in pbones:
            if '_fix_' in br.name:
                if '_R' in br.name:
                    r_name = br.name.split("_R")
                    for bl in pbones:
                        if '_fix_' in bl.name:
                            if '_L' in bl.name:
                                l_name = bl.name.split("_L")
                                if l_name[0] == r_name[0]:
                                    #print (bl.name, br.name)
                                    for CR in br.constraints:
                                        if CR.type == 'TRANSFORM':
                                            if '_R_' in CR.name:
                                                cr_name = CR.name.split('_R_')
                                                for CL in bl.constraints:
                                                    if CL.type == 'TRANSFORM':
                                                        if '_L_' in CL.name:
                                                            cl_name = CL.name.split('_L_')
                                                            if cr_name[0] == cl_name[0]:
                                                                #print (CR.name, CL.name)
                                                                if CR.map_to_x_from and CL.map_to_x_from == 'X':
                                                                    CR.to_min_x = -(CL.to_min_x)
                                                                    CR.to_max_x = -(CL.to_max_x)
                                                                if CR.map_to_y_from and CL.map_to_y_from == 'X':
                                                                    CR.to_min_y = CL.to_min_y
                                                                    CR.to_max_y = CL.to_max_y
                                                                if CR.map_to_z_from and CL.map_to_z_from == 'X':
                                                                    CR.to_min_z = CL.to_min_z
                                                                    CR.to_max_z = CL.to_max_z
                                                                if CR.map_to_x_from and CL.map_to_x_from == 'Z':
                                                                    CR.to_min_x = -(CL.to_max_x)
                                                                    CR.to_max_x = -(CL.to_min_x)
                                                                if CR.map_to_y_from and CL.map_to_y_from == 'Z':
                                                                    CR.to_min_y = CL.to_max_y
                                                                    CR.to_max_y = CL.to_min_y
                                                                if CR.map_to_z_from and CL.map_to_z_from == 'Z':
                                                                    CR.to_min_z = CL.to_max_z
                                                                    CR.to_max_z = CL.to_min_z


        for br in pbones:
            if 'properties_' in br.name:
                if '_R' in br.name:
                    r_name = br.name.split("_R")
                    for bl in pbones:
                        if 'properties_' in bl.name:
                            if '_L' in bl.name:
                                l_name = bl.name.split("_L")
                                if l_name[0] == r_name[0]:
                                    if br.items() != '[]':
                                        for Rprop in br.items():
                                            if 'volume_preservation' in Rprop[0]:
                                                r_prop = Rprop[0].split("_R")
                                                if bl.items() != '[]':
                                                    for Lprop in bl.items():
                                                        if 'volume_preservation' in Lprop[0]:
                                                            l_prop = Lprop[0].split("_L")
                                                            if r_prop[0] == l_prop[0]:
                                                                br[Rprop[0]] = bl[Lprop[0]]



        return {"FINISHED"}

#### Mirror Realistic Joints Values Operator ####

class Operator_Mirror_RJ_Constraints(bpy.types.Operator):

    bl_idname = "mirror.rj_constraints"
    bl_label = "BlenRig Mirror Realistic Joints Constraints L to R"
    bl_description = "Mirror Realistic Joints Constraints L to R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    to_side : bpy.props.StringProperty()

    def execute(self, context):
        pbones = bpy.context.active_object.pose.bones
        for br in pbones:
            if 'properties_' in br.name:
                if '_R' in br.name:
                    r_name = br.name.split("_R")
                    for bl in pbones:
                        if 'properties_' in bl.name:
                            if '_L' in bl.name:
                                l_name = bl.name.split("_L")
                                if l_name[0] == r_name[0]:
                                    if br.items() != '[]':
                                        for Rprop in br.items():
                                            if 'realistic_joints' in Rprop[0]:
                                                r_prop = Rprop[0].split("_R")
                                                if bl.items() != '[]':
                                                    for Lprop in bl.items():
                                                        if 'realistic_joints' in Lprop[0]:
                                                            l_prop = Lprop[0].split("_L")
                                                            if r_prop[0] == l_prop[0]:
                                                                if self.to_side == 'L to R':
                                                                    br[Rprop[0]] = bl[Lprop[0]]
                                                                if self.to_side == 'R to L':
                                                                    bl[Lprop[0]] = br[Rprop[0]]

        return {"FINISHED"}

#### Calculate Pole Angles ####

class Operator_blenrig_calculate_pole_angles(bpy.types.Operator):

    bl_idname = "blenrig.calculate_pole_angles"
    bl_label = "BlenRig Calculate IK Pole Angles"
    bl_description = "Calculate IK Pole Angles"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type == 'ARMATURE')
        else:
            return False

    def calc_pole_angles(self, context):
        from .rig_functions import calculate_pole_angle
        arm_obj = bpy.context.active_object
        pbones = arm_obj.pose.bones

        try:
            pbones['forearm_ik_L'].constraints["IK_NOREP"].pole_angle = radians(calculate_pole_angle('arm_ik_L', 'forearm_ik_L', 'elbow_pole_L'))
        except:
            pass
        try:
            pbones['forearm_ik_R'].constraints["IK_NOREP"].pole_angle = radians(calculate_pole_angle('arm_ik_R', 'forearm_ik_R', 'elbow_pole_R'))
        except:
            pass
        try:
            pbones['arm_elbow_pin_L'].constraints["IK_NOREP"].pole_angle = radians(calculate_pole_angle('shoulder_mstr_L', 'arm_elbow_pin_L', 'elbow_pole_L'))
        except:
            pass
        try:
            pbones['arm_elbow_pin_R'].constraints["IK_NOREP"].pole_angle = radians(calculate_pole_angle('shoulder_mstr_R', 'arm_elbow_pin_R', 'elbow_pole_R'))
        except:
            pass
        try:
            pbones['shin_ik_L'].constraints["IK_NOREP"].pole_angle = radians(calculate_pole_angle('thigh_ik_L', 'shin_ik_L', 'knee_pole_L'))
        except:
            pass
        try:
            pbones['shin_ik_R'].constraints["IK_NOREP"].pole_angle = radians(calculate_pole_angle('thigh_ik_R', 'shin_ik_R', 'knee_pole_R'))
        except:
            pass

    def refresh_hack(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    def rest_position(self, context):
        arm_obj = bpy.context.active_object
        arm_obj.data.pose_position = 'REST'

    def pose_position(self, context):
        arm_obj = bpy.context.active_object
        arm_obj.data.pose_position = 'POSE'

    def execute(self, context):
        self.rest_position(context)
        self.refresh_hack(context)
        self.calc_pole_angles(context)
        self.refresh_hack(context)
        self.pose_position(context)

        return {"FINISHED"}

#### Calculate Floor Offsets ####

class Operator_blenrig_calculate_floor_offsets(bpy.types.Operator):

    bl_idname = "blenrig.calculate_floor_offsets"
    bl_label = "BlenRig Calculate Floor Offsets"
    bl_description = "Calculate Floor Offsets"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type == 'ARMATURE')
        else:
            return False

    def update_values(self, context):
        armobj = bpy.context.active_object

        #Bone Length Properties Update
        for b in armobj.pose.bones:
            if b.keys() != '[]':
                if 'b_length_L' in b.keys():
                    b['b_length_L'] = b.bone.length
                if 'b_length_R' in b.keys():
                    b['b_length_R'] = b.bone.length
                if 'b_length' in b.keys():
                    b['b_length'] = b.bone.length
        #Floor constraints distance calculation
        for b in armobj.pose.bones:
            for C in b.constraints:
                if C.type == 'FLOOR':
                    if 'Floor_Lips' in C.name:
                        C.offset = abs((b.head[2] - armobj.pose.bones[C.subtarget].head[2]) * 0.9)
                    if 'Floor_Foot' in C.name:
                        C.offset = abs(b.head[2] - armobj.pose.bones[b.custom_shape_transform.name].head[2])

        #Blink rate calculation
        for b in armobj.pose.bones:
            if b.name == 'blink_ctrl_L':
                try:
                    b['Blink_Rate_L'] = abs(armobj.pose.bones['eyelid_up_ctrl_L'].head[2] - armobj.pose.bones['eyelid_low_ctrl_L'].head[2])
                except:
                    pass
            if b.name == 'blink_ctrl_R':
                try:
                    b['Blink_Rate_R'] = abs(armobj.pose.bones['eyelid_up_ctrl_R'].head[2] - armobj.pose.bones['eyelid_low_ctrl_R'].head[2])
                except:
                    pass


    def refresh_hack(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    def rest_position(self, context):
        arm_obj = bpy.context.active_object
        arm_obj.data.pose_position = 'REST'

    def pose_position(self, context):
        arm_obj = bpy.context.active_object
        arm_obj.data.pose_position = 'POSE'

    def execute(self, context):
        self.rest_position(context)
        self.refresh_hack(context)
        self.update_values(context)
        self.refresh_hack(context)
        self.pose_position(context)

        return {"FINISHED"}







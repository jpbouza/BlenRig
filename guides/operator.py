import bpy
from math import radians
from mathutils import Vector
from bpy.props import StringProperty, FloatProperty, BoolProperty, EnumProperty
from . draw import draw_callback_px
from . utils import inside, get_armature_object
from bpy.props import IntProperty
from . guide import texts_dict
from . reproportion.guide_reproportion import GUIDE_STEPS_REPROPORTION
from . datatransfer.guide_datatransfer import GUIDE_STEPS_DATATRANSFER

class VIEW3D_OT_blenrig_guide_reproportion(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_reproportion"
    bl_label = "Show Reproportion Guide"
    bl_description = "Run Blenrig interactive guide and show it inside 3d viewport"

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
        else:
            return False

    instance = None
    step : IntProperty(default=0)

    def modal(self, context, event):
        if context.area != self.area or context.scene != self.scene or self.workspace != context.workspace:
            # On UNDO: queremos ver si el contexto es válido (no ha cambiado realmente) para actualizarlo.
            if context.area and context.area.type == 'VIEW_3D' and context.scene and context.workspace and get_armature_object(context):
                self.area = context.area
                self.scene = context.scene
                self.workspace = context.workspace
                # from .guide import GUIDE_STEPS
                self.load_step(context,self.step)
                return {'RUNNING_MODAL'}
            self.finish()
            print("[Blenrig Guide] Error: scene, workspace or editor was changed!")
            return {'CANCELLED'}
        elif not get_armature_object(context):
            self.area.tag_redraw()
            self.finish(context)
            print("[Blenrig Guide] Error: target armature was removed!")
            return {'CANCELLED'}
        self.region.tag_redraw()

        # ''' Escape para finalizar el operador?
        if event.type == 'ESC':
            self.finish(context)
            self.area.tag_redraw()
            return {'CANCELLED'}

        if event.type == 'TIMER':
            if self.multi_image:
                if self.image_index == self.max_image_index:
                    self.image_index = 0
                else:
                    self.image_index += 1
                self.image[self.image_index].gl_load()
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE':
            mouse = Vector((event.mouse_region_x, event.mouse_region_y))
            if event.value == 'PRESS' and inside(mouse, self.widget_pos, self.widget_size):
                if self.next_button_enabled and inside(mouse, self.next_button_pos, self.button_size):
                    if not self.load_next_step(context):
                        self.finish(context)
                        self.area.tag_redraw()
                        return {'FINISHED'}
                if self.prev_button_enabled and inside(mouse, self.prev_button_pos, self.button_size):
                    if not self.load_prev_step(context):
                        self.finish(context)
                        self.area.tag_redraw()
                        return {'FINISHED'}
                if inside(mouse, self.x_button_pos, (self.button_size[1], self.button_size[1])):
                    self.finish(context)
                    self.area.tag_redraw()
                    return {'FINISHED'}
                return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def finish(self, context=bpy.context):
        from . reproportion.guide_reproportion_actions import end_of_step_action
        end_of_step_action(context)
        VIEW3D_OT_blenrig_guide_reproportion.instance = None
        if hasattr(self, 'timer') and self.timer:
            context.window_manager.event_timer_remove(self.timer)
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        # Recover temporal changes.
        context.preferences.inputs.use_auto_perspective = self.use_auto_perspective

    def load_next_step(self, context) -> bool:
        return self.load_step(context, self.step+1)

    def load_prev_step(self, context) -> bool:
        return self.load_step(context, self.step-1)

    def load_step(self, context, step: int) -> bool:
        if step < 0 or step > self.max_step_index:
            return False
        self.step = step
        if self.step == self.max_step_index:
            self.button_text = 'Close'
        self.next_button_enabled = step != self.max_step_index
        self.prev_button_enabled = step != 0
        if hasattr(self, 'timer') and self.timer:
            context.window_manager.event_timer_remove(self.timer)
            #print("Remove Timer")
        step_data = GUIDE_STEPS_REPROPORTION[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_reproportion_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_reproportion_image(name)
                if img:
                    hide_image(img)
                    self.image.append(img)
            self.image_index = 0
            self.max_image_index = len(self.image) - 1
            if self.max_image_index != -1:
                self.image[0].gl_load()
            self.timer = context.window_manager.event_timer_add(2.0, window=context.window)
            #print("Create Timer")
        else:
            self.image = load_reproportion_image(image)
            if self.image:
                hide_image(self.image)
                self.image.gl_load()

    def draw_bones(self, context, *bone_names):
        self.bones_to_display.clear()
        if context.mode != 'POSE':
            print("WARN: You are not in pose mode!")
        bones = get_armature_object(context).pose.bones

        for name in bone_names:
            bone = bones.get(name, None)
            if bone:
                self.bones_to_display.append(bone)

    def init(self, context):
        # Activar reproportion...
        context.object.data.reproportion = True

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode='POSE')

        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
        elif context.active_object.type != 'ARMATURE':
            self.report({'WARNING'}, "Active object must be an armature, cannot run operator")
            return {'CANCELLED'}

        context.scene.blenrig_guide.arm_obj = context.pose_object
        self.obj = context.object

        self.max_step_index = len(GUIDE_STEPS_REPROPORTION) - 1

        data = context.scene.blenrig_guide
        self.dpi = data.dpi
        self.language = data.language
        self.image_scale = data.image_scale

        self.bones_to_display = []

        # Textos.
        from . text import SetSizeGetDim
        self.button_text_size = 14
        self.step_text = texts_dict['Step'][self.language]

        self.next_button_text = texts_dict['Next'][self.language]
        next_dim = SetSizeGetDim(0, self.button_text_size + 4, self.dpi, self.next_button_text)

        self.prev_button_text = texts_dict['Prev'][self.language]
        prev_dim = SetSizeGetDim(0, self.button_text_size + 4, self.dpi, self.prev_button_text)

        max_button_width = max(next_dim[0], prev_dim[0])

        if not self.load_step(context, self.step):
            self.report({'WARNING'}, "Guide could not be loaded")
            return {'CANCELLED'}

        factor_dpi = self.dpi / 72
        margin = 5 * factor_dpi
        self.widget_pos = Vector((50, 50)) * factor_dpi
        self.header_height = 30 * factor_dpi
        self.text_box_height = 60 * factor_dpi
        self.image_size = Vector((300, 300)) *self.image_scale * factor_dpi
        self.widget_size = self.image_size + Vector((0, self.header_height + self.text_box_height))
        self.button_size = Vector((max(int(max_button_width), 20), 20))

        self.x_button_pos = self.widget_pos + self.widget_size - Vector((margin + self.button_size[1], margin + self.button_size[1]))

        self.next_button_pos = self.x_button_pos - Vector((margin + self.button_size[0], 0))
        self.prev_button_pos = self.next_button_pos - Vector((margin + self.button_size[0], 0))

        self.area = context.area
        self.region = context.region
        self.scene = context.scene
        self.workspace = context.workspace

        # Some temporal changes + Back-up.
        self.use_auto_perspective = context.preferences.inputs.use_auto_perspective
        context.preferences.inputs.use_auto_perspective = False

        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        VIEW3D_OT_blenrig_guide_reproportion.instance = self
        return {'RUNNING_MODAL'}

class VIEW3D_OT_blenrig_guide_datatransfer(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_datatransfer"
    bl_label = "Show Data Transfer Guide"
    bl_description = "Run Blenrig interactive guide and show it inside 3d viewport"

    instance = None
    step : IntProperty(default=0)

    def modal(self, context, event):
        if context.area != self.area or context.scene != self.scene or self.workspace != context.workspace:
            # On UNDO: queremos ver si el contexto es válido (no ha cambiado realmente) para actualizarlo.
            if context.area and context.area.type == 'VIEW_3D' and context.scene and context.workspace and get_armature_object(context):
                self.area = context.area
                self.scene = context.scene
                self.workspace = context.workspace
                # from .guide import GUIDE_STEPS
                self.load_step(context,self.step)
                return {'RUNNING_MODAL'}
            self.finish()
            print("[Blenrig Guide] Error: scene, workspace or editor was changed!")
            return {'CANCELLED'}
        elif not get_armature_object(context):
            self.area.tag_redraw()
            self.finish(context)
            print("[Blenrig Guide] Error: target armature was removed!")
            return {'CANCELLED'}
        self.region.tag_redraw()

        # ''' Escape para finalizar el operador?
        if event.type == 'ESC':
            self.finish(context)
            self.area.tag_redraw()
            return {'CANCELLED'}

        if event.type == 'TIMER':
            if self.multi_image:
                if self.image_index == self.max_image_index:
                    self.image_index = 0
                else:
                    self.image_index += 1
                self.image[self.image_index].gl_load()
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE':
            mouse = Vector((event.mouse_region_x, event.mouse_region_y))
            if event.value == 'PRESS' and inside(mouse, self.widget_pos, self.widget_size):
                if self.next_button_enabled and inside(mouse, self.next_button_pos, self.button_size):
                    if not self.load_next_step(context):
                        self.finish(context)
                        self.area.tag_redraw()
                        return {'FINISHED'}
                if self.prev_button_enabled and inside(mouse, self.prev_button_pos, self.button_size):
                    if not self.load_prev_step(context):
                        self.finish(context)
                        self.area.tag_redraw()
                        return {'FINISHED'}
                if inside(mouse, self.x_button_pos, (self.button_size[1], self.button_size[1])):
                    self.finish(context)
                    self.area.tag_redraw()
                    return {'FINISHED'}
                return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def finish(self, context=bpy.context):
        from . datatransfer.guide_datatransfer_actions import end_of_step_action
        end_of_step_action(context)

        VIEW3D_OT_blenrig_guide_datatransfer.instance = None
        if hasattr(self, 'timer') and self.timer:
            context.window_manager.event_timer_remove(self.timer)
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        # Recover temporal changes.
        context.preferences.inputs.use_auto_perspective = self.use_auto_perspective

    def load_next_step(self, context) -> bool:
        return self.load_step(context, self.step+1)

    def load_prev_step(self, context) -> bool:
        return self.load_step(context, self.step-1)

    def load_step(self, context, step: int) -> bool:
        if step < 0 or step > self.max_step_index:
            return False
        self.step = step
        if self.step == self.max_step_index:
            self.button_text = 'Close'
        self.next_button_enabled = step != self.max_step_index
        self.prev_button_enabled = step != 0
        if hasattr(self, 'timer') and self.timer:
            context.window_manager.event_timer_remove(self.timer)
            #print("Remove Timer")
        step_data = GUIDE_STEPS_DATATRANSFER[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_datatransfer_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_datatransfer_image(name)
                if img:
                    hide_image(img)
                    self.image.append(img)
            self.image_index = 0
            self.max_image_index = len(self.image) - 1
            if self.max_image_index != -1:
                self.image[0].gl_load()
            self.timer = context.window_manager.event_timer_add(2.0, window=context.window)
            #print("Create Timer")
        else:
            self.image = load_datatransfer_image(image)
            if self.image:
                hide_image(self.image)
                self.image.gl_load()

    def draw_bones(self, context, *bone_names):
        self.bones_to_display.clear()
        if context.mode != 'POSE':
            print("WARN: You are not in pose mode!")
        bones = get_armature_object(context).pose.bones

        for name in bone_names:
            bone = bones.get(name, None)
            if bone:
                self.bones_to_display.append(bone)

    # def init(self, context):
    #     # Activar reproportion...
    #     # context.object.data.reproportion = True

    def invoke(self, context, event):
        # bpy.ops.object.mode_set(mode='POSE')

        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

        self.max_step_index = len(GUIDE_STEPS_DATATRANSFER) - 1

        data = context.scene.blenrig_guide
        self.dpi = data.dpi
        self.language = data.language
        self.image_scale = data.image_scale

        self.bones_to_display = []

        # Textos.
        from . text import SetSizeGetDim
        self.button_text_size = 14
        self.step_text = texts_dict['Step'][self.language]

        self.next_button_text = texts_dict['Next'][self.language]
        next_dim = SetSizeGetDim(0, self.button_text_size + 4, self.dpi, self.next_button_text)

        self.prev_button_text = texts_dict['Prev'][self.language]
        prev_dim = SetSizeGetDim(0, self.button_text_size + 4, self.dpi, self.prev_button_text)

        max_button_width = max(next_dim[0], prev_dim[0])

        if not self.load_step(context, self.step):
            self.report({'WARNING'}, "Guide could not be loaded")
            return {'CANCELLED'}

        factor_dpi = self.dpi / 72
        margin = 5 * factor_dpi
        self.widget_pos = Vector((50, 50)) * factor_dpi
        self.header_height = 30 * factor_dpi
        self.text_box_height = 60 * factor_dpi
        self.image_size = Vector((300, 300)) *self.image_scale * factor_dpi
        self.widget_size = self.image_size + Vector((0, self.header_height + self.text_box_height))
        self.button_size = Vector((max(int(max_button_width), 20), 20))

        self.x_button_pos = self.widget_pos + self.widget_size - Vector((margin + self.button_size[1], margin + self.button_size[1]))

        self.next_button_pos = self.x_button_pos - Vector((margin + self.button_size[0], 0))
        self.prev_button_pos = self.next_button_pos - Vector((margin + self.button_size[0], 0))

        self.area = context.area
        self.region = context.region
        self.scene = context.scene
        self.workspace = context.workspace

        # Some temporal changes + Back-up.
        self.use_auto_perspective = context.preferences.inputs.use_auto_perspective
        context.preferences.inputs.use_auto_perspective = False

        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        VIEW3D_OT_blenrig_guide_datatransfer.instance = self
        return {'RUNNING_MODAL'}

class Operator_Transfer_VGroups(bpy.types.Operator):

    bl_idname = "blenrig.transfer_vgroups"
    bl_label = "BlenRig Transfer Vgroups"
    bl_description = "Transfer Vertex Groups from selected object to active object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if len(bpy.context.selected_objects) != 2:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    def execute(self, context):
        # Define objects
        active = bpy.context.active_object
        for ob in bpy.context.selected_objects:
            if ob != active:
                selected = ob

        # add modifier on active object
        mod = active.modifiers.new("DataTransfer", 'DATA_TRANSFER')
        # set modifier properties
        mod.object = selected
        mod.use_vert_data = True
        mod.data_types_verts = {'VGROUP_WEIGHTS'}
        mod.vert_mapping = bpy.context.scene.blenrig_guide.transfer_mapping
        mod.use_max_distance = True
        mod.max_distance = bpy.context.scene.blenrig_guide.transfer_ray_distance
        bpy.ops.object.datalayout_transfer(modifier=mod.name, data_type='VGROUP_WEIGHTS', use_delete=False, layers_select_src='ALL', layers_select_dst='NAME')
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=0.01, keep_single=False)
        return {"FINISHED"}

class Operator_Guide_Transfer_VGroups(bpy.types.Operator):

    bl_idname = "blenrig.guide_transfer_vgroups"
    bl_label = "BlenRig Transfer Vgroups for Transfer Guide"
    bl_description = "Transfer Vertex Groups from selected object to active object within the guide "
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    body_area : bpy.props.StringProperty()

    def execute(self, context):

        from . utils import deselect_all_objects, set_mode

        #Set back Object Mode
        if context.mode != 'OBJECT':
            set_mode('OBJECT')

        deselect_all_objects(context)

        #Select Mdef Weight Transfer Model
        transfer_obj = bpy.context.scene.blenrig_guide.mdef_weights_transfer_obj
        transfer_obj.select_set(state=True)

        if self.body_area == 'head':
            #Select Head Object
            head_object = bpy.context.scene.blenrig_guide.character_head_obj
            head_object.select_set(state=True)
            bpy.context.view_layer.objects.active = head_object

        if self.body_area == 'hands':
            #Select Fingers Object
            fingers_object = bpy.context.scene.blenrig_guide.character_hands_obj
            fingers_object.select_set(state=True)
            bpy.context.view_layer.objects.active = fingers_object

        #Transfer Weights
        bpy.ops.blenrig.transfer_vgroups()

        #Go back to Edit Mode
        deselect_all_objects(context)

        if self.body_area == 'head':
            #Select Head Object
            head_object = bpy.context.scene.blenrig_guide.character_head_obj
            head_object.select_set(state=True)
            bpy.context.view_layer.objects.active = head_object

        if self.body_area == 'hands':
            #Select Fingers Object
            fingers_object = bpy.context.scene.blenrig_guide.character_hands_obj
            fingers_object.select_set(state=True)
            bpy.context.view_layer.objects.active = fingers_object

        #Set back Object Mode
        if context.mode != 'EDIT':
            set_mode('EDIT')
        return {"FINISHED"}

class Operator_blenrig_add_head_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.add_head_modifiers"
    bl_label = "BlenRig add Head Modifiers"
    bl_description = "Add commonly used modifiers for Head Deformation based on Mesh Deform"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    def execute(self, context):

        from . utils import check_mod_type, check_mod_type_name, add_drivers, add_vars, add_mod_generator

        #Add Deform Modifiers to Character's head
        active = bpy.context.active_object

        #Armature
        if check_mod_type('ARMATURE'):
            pass
        else:
            mod = active.modifiers.new(name= "Armature",type= 'ARMATURE')
            # set modifier properties
            mod.object = bpy.context.scene.blenrig_guide.arm_obj
            mod.use_deform_preserve_volume = True
            mod.vertex_group = 'no_mdef'
            mod.show_expanded = True
            mod.show_in_editmode = True
            mod.show_on_cage = True
        #Mesh Deform
        if check_mod_type('MESH_DEFORM'):
            pass
        else:
            mod = active.modifiers.new(name= "MeshDeform",type= 'MESH_DEFORM')
            # set modifier properties
            mod.object = bpy.context.scene.blenrig_guide.mdef_cage_obj
            mod.invert_vertex_group = True
            mod.vertex_group = 'no_mdef'
            mod.show_expanded = True
            mod.show_in_editmode = True
            mod.show_on_cage = True

        #Corrective Smooth
        if check_mod_type('CORRECTIVE_SMOOTH'):
            pass
        else:
            mod = active.modifiers.new(name= "CorrectiveSmooth",type= 'CORRECTIVE_SMOOTH')
            # set modifier properties
            mod.smooth_type = 'SIMPLE'
            mod.rest_source = 'ORCO'
            mod.vertex_group = 'corrective_smooth'
            mod.show_expanded = False

        #Cheek Puffs
        if check_mod_type_name('WARP', 'Cheek_Puff_L'):
            pass
        else:
            mod = active.modifiers.new(name= "Cheek_Puff_L",type= 'WARP')
            # set modifier properties
            mod.object_from = bpy.context.scene.blenrig_guide.arm_obj
            mod.bone_from = 'cheek_puff_mstr_L'
            mod.object_to = bpy.context.scene.blenrig_guide.arm_obj
            mod.bone_to = 'cheek_puff_ctrl_L'
            mod.vertex_group = 'no_mdef'
            mod.falloff_radius = bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_puff_ctrl_L"]["PUFF_RADIUS_L"]
            mod.show_expanded = False

        if check_mod_type_name('WARP', 'Cheek_Puff_R'):
            pass
        else:
            mod = active.modifiers.new(name= "Cheek_Puff_R",type= 'WARP')
            # set modifier properties
            mod.object_from = bpy.context.scene.blenrig_guide.arm_obj
            mod.bone_from = 'cheek_puff_mstr_R'
            mod.object_to = bpy.context.scene.blenrig_guide.arm_obj
            mod.bone_to = 'cheek_puff_ctrl_R'
            mod.vertex_group = 'no_mdef'
            mod.falloff_radius = bpy.context.scene.blenrig_guide.arm_obj.pose.bones["cheek_puff_ctrl_R"]["PUFF_RADIUS_R"]
            mod.show_expanded = False

        #Lattices
        if check_mod_type_name('LATTICE', 'LATTICE_EYE_L'):
            pass
        else:
            mod = active.modifiers.new(name= "LATTICE_EYE_L",type= 'LATTICE')
            # set modifier properties
            for ob in bpy.data.objects:
                if ob.type == 'LATTICE':
                    if 'LATTICE_EYE_L' in ob.name:
                        if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                            mod.object = ob
            mod.vertex_group = 'lattice_eye_L'
            mod.show_expanded = False

        if check_mod_type_name('LATTICE', 'LATTICE_EYE_R'):
            pass
        else:
            mod = active.modifiers.new(name= "LATTICE_EYE_R",type= 'LATTICE')
            # set modifier properties
            for ob in bpy.data.objects:
                if ob.type == 'LATTICE':
                    if 'LATTICE_EYE_R' in ob.name:
                        if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                            mod.object = ob
            mod.vertex_group = 'lattice_eye_R'
            mod.show_expanded = False

        if check_mod_type_name('LATTICE', 'LATTICE_BROW'):
            pass
        else:
            mod = active.modifiers.new(name= "LATTICE_BROW",type= 'LATTICE')
            # set modifier properties
            for ob in bpy.data.objects:
                if ob.type == 'LATTICE':
                    if 'LATTICE_BROW' in ob.name:
                        if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                            mod.object = ob
            mod.vertex_group = 'lattice_brow'
            mod.show_expanded = False

        if check_mod_type_name('LATTICE', 'LATTICE_MOUTH'):
            pass
        else:
            mod = active.modifiers.new(name= "LATTICE_MOUTH",type= 'LATTICE')
            # set modifier properties
            for ob in bpy.data.objects:
                if ob.type == 'LATTICE':
                    if 'LATTICE_MOUTH' in ob.name:
                        if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                            mod.object = ob
            mod.vertex_group = 'lattice_mouth'
            mod.show_expanded = False

        if check_mod_type_name('LATTICE', 'LATTICE_HEAD'):
            pass
        else:
            mod = active.modifiers.new(name= "LATTICE_HEAD",type= 'LATTICE')
            # set modifier properties
            for ob in bpy.data.objects:
                if ob.type == 'LATTICE':
                    if 'LATTICE_HEAD' in ob.name:
                        if ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                            mod.object = ob
            mod.vertex_group = 'lattice_head'
            mod.show_expanded = False

        #Subsurf
        subsurf_mods = [mod for mod in active.modifiers if mod.type == 'SUBSURF']
        if subsurf_mods:
            active.modifiers.remove(subsurf_mods[-1])
        mod = active.modifiers.new(name= "Subdivision",type= 'SUBSURF')
        # set modifier properties
        mod.subdivision_type = 'CATMULL_CLARK'
        mod.levels = 0
        mod.render_levels = 3
        mod.show_expanded = True

        #Add Drivers
        #Delete Drivers if present
        if hasattr(active, 'modifiers') and hasattr(active.modifiers, 'data') and hasattr(active.modifiers.data, 'animation_data') and hasattr(active.modifiers.data.animation_data, 'drivers'):
            fcurves = active.modifiers.data.animation_data.drivers
            for fc in fcurves:
                if fc.data_path == 'modifiers["Cheek_Puff_L"].falloff_radius':
                    fcurves.remove(fcurves[0])
                if fc.data_path == 'modifiers["Cheek_Puff_R"].falloff_radius':
                    fcurves.remove(fcurves[0])
        #Cheek_Puff_L
        active_driver = add_drivers(active.modifiers["Cheek_Puff_L"], 'falloff_radius', 0, 'no_array', 'CONSTANT', False, False, False, '1.000', 'MAX')
        add_vars(active_driver, 'var', 'SINGLE_PROP', bpy.context.scene.blenrig_guide.arm_obj, 'cheek_puff_ctrl_L', 'pose.bones["cheek_puff_ctrl_L"]["PUFF_RADIUS_L"]', 'WORLD_SPACE', 'LOC_X', 'AUTO')
        add_mod_generator(active_driver, 'GENERATOR', 0.0, 0.0, 0.0, 0.0, 'POLYNOMIAL', False, 1, False, False, False, 0.0, 1.0)
        #Cheek_Puff_R
        active_driver = add_drivers(active.modifiers["Cheek_Puff_R"], 'falloff_radius', 0, 'no_array', 'CONSTANT', False, False, False, '1.000', 'MAX')
        add_vars(active_driver, 'var', 'SINGLE_PROP', bpy.context.scene.blenrig_guide.arm_obj, 'cheek_puff_ctrl_R', 'pose.bones["cheek_puff_ctrl_R"]["PUFF_RADIUS_R"]', 'WORLD_SPACE', 'LOC_X', 'AUTO')
        add_mod_generator(active_driver, 'GENERATOR', 0.0, 0.0, 0.0, 0.0, 'POLYNOMIAL', False, 1, False, False, False, 0.0, 1.0)

        return {"FINISHED"}

class Operator_blenrig_add_hands_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.add_hands_modifiers"
    bl_label = "BlenRig add Hands Modifiers"
    bl_description = "Add commonly used modifiers for Hands Deformation based on Mesh Deform"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    def execute(self, context):

        from . utils import check_mod_type, check_mod_type_name, add_drivers, add_vars, add_mod_generator

        #Add Deform Modifiers to Character's hands
        bpy.context.view_layer.objects.active = bpy.context.scene.blenrig_guide.character_hands_obj
        active = bpy.context.active_object

        #Armature
        if check_mod_type('ARMATURE'):
            pass
        else:
            mod = active.modifiers.new(name= "Armature",type= 'ARMATURE')
            # set modifier properties
            mod.object = bpy.context.scene.blenrig_guide.arm_obj
            mod.use_deform_preserve_volume = True
            mod.vertex_group = 'no_mdef'
            mod.show_expanded = True
            mod.show_in_editmode = True
            mod.show_on_cage = True
        #Mesh Deform
        if check_mod_type('MESH_DEFORM'):
            pass
        else:
            mod = active.modifiers.new(name= "MeshDeform",type= 'MESH_DEFORM')
            # set modifier properties
            mod.object = bpy.context.scene.blenrig_guide.mdef_cage_obj
            mod.invert_vertex_group = True
            mod.vertex_group = 'no_mdef'
            mod.show_expanded = True
            mod.show_in_editmode = True
            mod.show_on_cage = True

        #Corrective Smooth
        if check_mod_type('CORRECTIVE_SMOOTH'):
            pass
        else:
            mod = active.modifiers.new(name= "CorrectiveSmooth",type= 'CORRECTIVE_SMOOTH')
            # set modifier properties
            mod.smooth_type = 'SIMPLE'
            mod.rest_source = 'ORCO'
            mod.vertex_group = 'corrective_smooth'
            mod.show_expanded = False

        #Subsurf
        subsurf_mods = [mod for mod in active.modifiers if mod.type == 'SUBSURF']
        if subsurf_mods:
            active.modifiers.remove(subsurf_mods[-1])
        mod = active.modifiers.new(name= "Subdivision",type= 'SUBSURF')
        # set modifier properties
        mod.subdivision_type = 'CATMULL_CLARK'
        mod.levels = 0
        mod.render_levels = 3
        mod.show_expanded = True

        return {"FINISHED"}

class Operator_blenrig_add_body_shapekeys(bpy.types.Operator):

    bl_idname = "blenrig.add_body_shapekeys"
    bl_label = "BlenRig add Body Shapkeys"
    bl_description = "Add commonly used shapekeys for the body. Typically used in the Mdef Cage"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    #Neck
    def neck(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        #Head
        add_shapekey(context, 'head_L')
        add_shapekey(context, 'head_R')
        add_shapekey(context, 'head_forw')
        add_shapekey(context, 'head_back')
        add_shapekey(context, 'head_twist_L')
        add_shapekey(context, 'head_twist_R')
        #Neck 1
        add_shapekey(context, 'neck_1_L')
        add_shapekey(context, 'neck_1_R')
        add_shapekey(context, 'neck_1_forw')
        add_shapekey(context, 'neck_1_back')
        add_shapekey(context, 'neck_1_twist_L')
        add_shapekey(context, 'neck_1_twist_R')
        #Neck 2
        add_shapekey(context, 'neck_2_L')
        add_shapekey(context, 'neck_2_R')
        add_shapekey(context, 'neck_2_forw')
        add_shapekey(context, 'neck_2_back')
        add_shapekey(context, 'neck_2_twist_L')
        add_shapekey(context, 'neck_2_twist_R')
        #Neck 3
        add_shapekey(context, 'neck_3_L')
        add_shapekey(context, 'neck_3_R')
        add_shapekey(context, 'neck_3_forw')
        add_shapekey(context, 'neck_3_back')
        add_shapekey(context, 'neck_3_twist_L')
        add_shapekey(context, 'neck_3_twist_R')


        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = bpy.context.active_object.data.shape_keys.key_blocks
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Head
            #head_L
            if check_shapekey_driver('head_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #head_R
            if check_shapekey_driver('head_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #head_forw
            if check_shapekey_driver('head_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #head_back
            if check_shapekey_driver('head_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #head_twist_L
            if check_shapekey_driver('head_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #head_twist_R
            if check_shapekey_driver('head_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Neck_1
            #neck_1_L
            if check_shapekey_driver('neck_1_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #neck_1_R
            if check_shapekey_driver('neck_1_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #neck_1_forw
            if check_shapekey_driver('neck_1_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #neck_1_back
            if check_shapekey_driver('neck_1_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #neck_1_twist_L
            if check_shapekey_driver('neck_1_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #neck_1_twist_R
            if check_shapekey_driver('neck_1_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Neck_2
            #neck_2_L
            if check_shapekey_driver('neck_2_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #neck_2_R
            if check_shapekey_driver('neck_2_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #neck_2_forw
            if check_shapekey_driver('neck_2_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #neck_2_back
            if check_shapekey_driver('neck_2_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #neck_2_twist_L
            if check_shapekey_driver('neck_2_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #neck_2_twist_R
            if check_shapekey_driver('neck_2_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Neck_3
            #neck_3_L
            if check_shapekey_driver('neck_3_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #neck_3_R
            if check_shapekey_driver('neck_3_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #neck_3_forw
            if check_shapekey_driver('neck_3_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #neck_3_back
            if check_shapekey_driver('neck_3_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #neck_3_twist_L
            if check_shapekey_driver('neck_3_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #neck_3_twist_R
            if check_shapekey_driver('neck_3_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)

    #Spine
    def spine(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        #Spine_3
        add_shapekey(context, 'spine_3_L')
        add_shapekey(context, 'spine_3_R')
        add_shapekey(context, 'spine_3_forw')
        add_shapekey(context, 'spine_3_back')
        add_shapekey(context, 'spine_3_twist_L')
        add_shapekey(context, 'spine_3_twist_R')
        #Spine_2
        add_shapekey(context, 'spine_2_L')
        add_shapekey(context, 'spine_2_R')
        add_shapekey(context, 'spine_2_forw')
        add_shapekey(context, 'spine_2_back')
        add_shapekey(context, 'spine_2_twist_L')
        add_shapekey(context, 'spine_2_twist_R')
        #Spine_1
        add_shapekey(context, 'spine_1_L')
        add_shapekey(context, 'spine_1_R')
        add_shapekey(context, 'spine_1_forw')
        add_shapekey(context, 'spine_1_back')
        add_shapekey(context, 'spine_1_twist_L')
        add_shapekey(context, 'spine_1_twist_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = bpy.context.active_object.data.shape_keys.key_blocks
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Spine_3
            #spine_3_L
            if check_shapekey_driver('spine_3_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #spine_3_R
            if check_shapekey_driver('spine_3_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #spine_3_forw
            if check_shapekey_driver('spine_3_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #spine_3_back
            if check_shapekey_driver('spine_3_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #spine_3_twist_L
            if check_shapekey_driver('spine_3_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #spine_3_twist_R
            if check_shapekey_driver('spine_3_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Spine_2
            #spine_2_L
            if check_shapekey_driver('spine_2_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #spine_2_R
            if check_shapekey_driver('spine_2_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #spine_2_forw
            if check_shapekey_driver('spine_2_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #spine_2_back
            if check_shapekey_driver('spine_2_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #spine_2_twist_L
            if check_shapekey_driver('spine_2_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #spine_2_twist_R
            if check_shapekey_driver('spine_2_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Spine_1
            #spine_1_L
            if check_shapekey_driver('spine_1_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #spine_1_R
            if check_shapekey_driver('spine_1_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #spine_1_forw
            if check_shapekey_driver('spine_1_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_forw'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #spine_1_back
            if check_shapekey_driver('spine_1_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_back'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #spine_1_twist_L
            if check_shapekey_driver('spine_1_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_twist_L'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #spine_1_twist_R
            if check_shapekey_driver('spine_1_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_twist_R'], 'value')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)

    def execute(self, context):
        self.neck(context)
        self.spine(context)























        return {"FINISHED"}

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
from . mdef.guide_mdef import GUIDE_STEPS_MDEF
from . lattices.guide_lattices import GUIDE_STEPS_LATTICES
from . actions.guide_actions import GUIDE_STEPS_ACTIONS
from . weights.guide_weights import GUIDE_STEPS_WEIGHTS
from . shapekeys.guide_shapekeys import GUIDE_STEPS_SHAPEKEYS

#Guide Operators

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

class VIEW3D_OT_blenrig_guide_mdef(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_mdef"
    bl_label = "Show Mesh Deform Guide"
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
        from . mdef.guide_mdef_actions import end_of_step_action
        end_of_step_action(context)

        VIEW3D_OT_blenrig_guide_mdef.instance = None
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
        step_data = GUIDE_STEPS_MDEF[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_mdef_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_mdef_image(name)
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
            self.image = load_mdef_image(image)
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

        self.max_step_index = len(GUIDE_STEPS_MDEF) - 1

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
        VIEW3D_OT_blenrig_guide_mdef.instance = self
        return {'RUNNING_MODAL'}

class VIEW3D_OT_blenrig_guide_lattices(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_lattices"
    bl_label = "Show Mesh Deform Guide"
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
        from . lattices.guide_lattices_actions import end_of_step_action
        end_of_step_action(context)

        VIEW3D_OT_blenrig_guide_lattices.instance = None
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
        step_data = GUIDE_STEPS_LATTICES[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_lattices_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_lattices_image(name)
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
            self.image = load_lattices_image(image)
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

        self.max_step_index = len(GUIDE_STEPS_LATTICES) - 1

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
        VIEW3D_OT_blenrig_guide_lattices.instance = self
        return {'RUNNING_MODAL'}

class VIEW3D_OT_blenrig_guide_actions(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_actions"
    bl_label = "Show Actions Guide"
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
        from . actions.guide_actions_actions import end_of_step_action
        end_of_step_action(context)

        VIEW3D_OT_blenrig_guide_actions.instance = None
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
        step_data = GUIDE_STEPS_ACTIONS[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_actions_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_actions_image(name)
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
            self.image = load_actions_image(image)
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

        self.max_step_index = len(GUIDE_STEPS_ACTIONS) - 1

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
        VIEW3D_OT_blenrig_guide_actions.instance = self
        return {'RUNNING_MODAL'}

class VIEW3D_OT_blenrig_guide_weights(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_weights"
    bl_label = "Show Weight Painting Guide"
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
        from . weights.guide_weights_actions import end_of_step_action
        end_of_step_action(context)

        VIEW3D_OT_blenrig_guide_weights.instance = None
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
        step_data = GUIDE_STEPS_WEIGHTS[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_weights_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_weights_image(name)
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
            self.image = load_weights_image(image)
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

        self.max_step_index = len(GUIDE_STEPS_WEIGHTS) - 1

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
        VIEW3D_OT_blenrig_guide_weights.instance = self
        return {'RUNNING_MODAL'}

class VIEW3D_OT_blenrig_guide_shapekeys(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide_shapekeys"
    bl_label = "Show Shapekeys Guide"
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
        from . shapekeys.guide_shapekeys_actions import end_of_step_action
        end_of_step_action(context)

        VIEW3D_OT_blenrig_guide_weights.instance = None
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
        step_data = GUIDE_STEPS_SHAPEKEYS[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_shapekeys_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_shapekeys_image(name)
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
            self.image = load_shapekeys_image(image)
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

        self.max_step_index = len(GUIDE_STEPS_SHAPEKEYS) - 1

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
        VIEW3D_OT_blenrig_guide_shapekeys.instance = self
        return {'RUNNING_MODAL'}

#Weights Transfer Operators

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

#Add Modifiers Operators

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

class Operator_blenrig_add_body_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.add_body_modifiers"
    bl_label = "BlenRig add Body Modifiers"
    bl_description = "Add Mesh Deform modifier"
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

        from . utils import check_mod_type, check_mod_type_name, add_drivers, add_vars, add_mod_generator, set_active_object, deselect_all_objects

        #Clear List
        bpy.context.scene.blenrig_character_body_obj.clear()

        #Define Body Objects
        for ob in bpy.context.selected_objects:
            add_item = bpy.context.scene.blenrig_character_body_obj.add()
            add_item.character_body_obj = ob

        #Add Deform Modifiers to defined Character's body object
        for ob in bpy.context.scene.blenrig_character_body_obj:
            body_ob = ob.character_body_obj
            deselect_all_objects(context)
            set_active_object(context, body_ob)
            active = bpy.context.active_object

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

#Mesh Deform Binding Operators

class Operator_blenrig_bind_mdef_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.bind_mdef_modifiers"
    bl_label = "BlenRig Bind Mdef Modifiers"
    bl_description = "Binds Mesh Deform modifier"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            if hasattr(bpy.context.active_object, 'modifiers'):
                for mod in bpy.context.active_object.modifiers:
                    if mod.type == 'MESH_DEFORM':
                        return True
        else:
            return False

    #Bind Modifiers
    def bind_mdef(self, context, mdef_precision):
        from .utils import set_active_object, deselect_all_objects

        for ob in bpy.context.selected_objects:
            set_active_object(context, ob)
            if hasattr(ob, 'modifiers'):
                for mod in ob.modifiers:
                    if mod.type == 'MESH_DEFORM':
                        if mod.is_bound == False:
                            mod.precision = mdef_precision
                            bpy.ops.object.meshdeform_bind(modifier=mod.name)
                            #Save file
                            bpy.ops.wm.save_mainfile()

    Bind_Type: bpy.props.BoolProperty(default=True, name='Fast Binding')

    def execute(self, context):
        if self.Bind_Type == True:
            self.bind_mdef(context, 5)
        else:
            self.bind_mdef(context, 7)
        return {"FINISHED"}

class Operator_blenrig_guide_bind_mdef_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.guide_bind_mdef_modifiers"
    bl_label = "BlenRig Guide Bind Mdef Modifiers"
    bl_description = "Binds Mesh Deform modifier"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    Guide_Bind_Type: bpy.props.BoolProperty(default=True, name = 'Fast Binding' )

    def execute(self, context):
        from .utils import set_active_object, deselect_all_objects

        if self.Guide_Bind_Type == True:
            try:
                deselect_all_objects(context)
                set_active_object(context, bpy.context.scene.blenrig_guide.character_head_obj)
                bpy.ops.blenrig.bind_mdef_modifiers(Bind_Type=True)
            except:
                pass
            try:
                deselect_all_objects(context)
                set_active_object(context, bpy.context.scene.blenrig_character_body_obj.character_hands_obj)
                bpy.ops.blenrig.bind_mdef_modifiers(Bind_Type=True)
            except:
                pass
            try:
                deselect_all_objects(context)
                for ob in bpy.context.scene.blenrig_character_body_obj:
                    body_ob = ob.character_body_obj
                    deselect_all_objects(context)
                    set_active_object(context, body_ob)
                    bpy.ops.blenrig.bind_mdef_modifiers(Bind_Type=True)
            except:
                pass
        if self.Guide_Bind_Type == False:
            try:
                deselect_all_objects(context)
                set_active_object(context, bpy.context.scene.blenrig_guide.character_head_obj)
                bpy.ops.blenrig.bind_mdef_modifiers(Bind_Type=False)
            except:
                pass
            try:
                deselect_all_objects(context)
                set_active_object(context, bpy.context.scene.blenrig_guide.character_hands_obj)
                bpy.ops.blenrig.bind_mdef_modifiers(Bind_Type=False)
            except:
                pass
            try:
                deselect_all_objects(context)
                for ob in bpy.context.scene.blenrig_character_body_obj:
                    body_ob = ob.character_body_obj
                    deselect_all_objects(context)
                    set_active_object(context, body_ob)
                    bpy.ops.blenrig.bind_mdef_modifiers(Bind_Type=False)
            except:
                pass
        return {"FINISHED"}

class Operator_blenrig_unbind_mdef_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.unbind_mdef_modifiers"
    bl_label = "BlenRig Unbind Mdef Modifiers"
    bl_description = "Unbinds Mesh Deform modifier"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            if hasattr(bpy.context.active_object, 'modifiers'):
                for mod in bpy.context.active_object.modifiers:
                    if mod.type == 'MESH_DEFORM':
                        return True
        else:
            return False


    #Unbind Modifiers
    def unbind_mdef(self, context):
        from .utils import set_active_object, deselect_all_objects

        for ob in bpy.context.selected_objects:
            set_active_object(context, ob)
            if hasattr(ob, 'modifiers'):
                for mod in ob.modifiers:
                    if mod.type == 'MESH_DEFORM':
                        if mod.is_bound == True:
                            bpy.ops.object.meshdeform_bind(modifier=mod.name)

    def execute(self, context):
        self.unbind_mdef(context)
        return {"FINISHED"}

class Operator_blenrig_guide_unbind_mdef_modifiers(bpy.types.Operator):

    bl_idname = "blenrig.guide_unbind_mdef_modifiers"
    bl_label = "BlenRig Guide Unbind Mdef Modifiers"
    bl_description = "Unbinds Mesh Deform modifier"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        from .utils import set_active_object, deselect_all_objects

        try:
            deselect_all_objects(context)
            set_active_object(context, bpy.context.scene.blenrig_guide.character_head_obj)
            bpy.ops.blenrig.unbind_mdef_modifiers()
        except:
            pass
        try:
            deselect_all_objects(context)
            set_active_object(context, bpy.context.scene.blenrig_character_body_obj.character_hands_obj)
            bpy.ops.blenrig.unbind_mdef_modifiers()
        except:
            pass
        try:
            deselect_all_objects(context)
            for ob in bpy.context.scene.blenrig_character_body_obj:
                body_ob = ob.character_body_obj
                deselect_all_objects(context)
                set_active_object(context, body_ob)
                bpy.ops.blenrig.unbind_mdef_modifiers()
        except:
            pass
        return {"FINISHED"}

#Shapekeys Operators

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

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

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
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Head
            #head_L
            if check_shapekey_driver('head_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #head_R
            if check_shapekey_driver('head_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #head_forw
            if check_shapekey_driver('head_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #head_back
            if check_shapekey_driver('head_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #head_twist_L
            if check_shapekey_driver('head_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #head_twist_R
            if check_shapekey_driver('head_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['head_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'head_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Neck_1
            #neck_1_L
            if check_shapekey_driver('neck_1_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #neck_1_R
            if check_shapekey_driver('neck_1_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #neck_1_forw
            if check_shapekey_driver('neck_1_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #neck_1_back
            if check_shapekey_driver('neck_1_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #neck_1_twist_L
            if check_shapekey_driver('neck_1_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #neck_1_twist_R
            if check_shapekey_driver('neck_1_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_1_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Neck_2
            #neck_2_L
            if check_shapekey_driver('neck_2_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #neck_2_R
            if check_shapekey_driver('neck_2_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #neck_2_forw
            if check_shapekey_driver('neck_2_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #neck_2_back
            if check_shapekey_driver('neck_2_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #neck_2_twist_L
            if check_shapekey_driver('neck_2_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #neck_2_twist_R
            if check_shapekey_driver('neck_2_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_2_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Neck_3
            #neck_3_L
            if check_shapekey_driver('neck_3_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #neck_3_R
            if check_shapekey_driver('neck_3_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #neck_3_forw
            if check_shapekey_driver('neck_3_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #neck_3_back
            if check_shapekey_driver('neck_3_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #neck_3_twist_L
            if check_shapekey_driver('neck_3_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #neck_3_twist_R
            if check_shapekey_driver('neck_3_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['neck_3_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'neck_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)

    #Spine
    def spine(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

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
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Spine_3
            #spine_3_L
            if check_shapekey_driver('spine_3_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #spine_3_R
            if check_shapekey_driver('spine_3_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #spine_3_forw
            if check_shapekey_driver('spine_3_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #spine_3_back
            if check_shapekey_driver('spine_3_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #spine_3_twist_L
            if check_shapekey_driver('spine_3_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #spine_3_twist_R
            if check_shapekey_driver('spine_3_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_3_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_3_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Spine_2
            #spine_2_L
            if check_shapekey_driver('spine_2_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #spine_2_R
            if check_shapekey_driver('spine_2_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #spine_2_forw
            if check_shapekey_driver('spine_2_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #spine_2_back
            if check_shapekey_driver('spine_2_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #spine_2_twist_L
            if check_shapekey_driver('spine_2_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #spine_2_twist_R
            if check_shapekey_driver('spine_2_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_2_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_2_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Spine_1
            #spine_1_L
            if check_shapekey_driver('spine_1_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #spine_1_R
            if check_shapekey_driver('spine_1_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #spine_1_forw
            if check_shapekey_driver('spine_1_forw'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_forw'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #spine_1_back
            if check_shapekey_driver('spine_1_back'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_back'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_xz_drv', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #spine_1_twist_L
            if check_shapekey_driver('spine_1_twist_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_twist_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #spine_1_twist_R
            if check_shapekey_driver('spine_1_twist_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['spine_1_twist_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'spine_1_y_drv', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)

    #Arm_L
    def arm_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        #Shoulder_L
        add_shapekey(context, 'shoulder_up_L')
        add_shapekey(context, 'shoulder_down_L')
        add_shapekey(context, 'shoulder_forw_L')
        add_shapekey(context, 'shoulder_back_L')
        #Arm_L
        add_shapekey(context, 'arm_up_L')
        add_shapekey(context, 'arm_down_L')
        add_shapekey(context, 'arm_forw_L')
        add_shapekey(context, 'arm_back_L')
        add_shapekey(context, 'arm_twist_in_L')
        add_shapekey(context, 'arm_twist_out_L')
        #Forearm_L
        add_shapekey(context, 'forearm_up_L')
        add_shapekey(context, 'forearm_down_L')
        add_shapekey(context, 'forearm_twist_in_L')
        add_shapekey(context, 'forearm_twist_out_L')
        #Hand_L
        add_shapekey(context, 'hand_up_L')
        add_shapekey(context, 'hand_down_L')
        add_shapekey(context, 'hand_forw_L')
        add_shapekey(context, 'hand_back_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Shoulder_L
            #shoulder_up_L
            if check_shapekey_driver('shoulder_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 35)
            #shoulder_down_L
            if check_shapekey_driver('shoulder_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -20)
            #shoulder_forw_L
            if check_shapekey_driver('shoulder_forw_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_forw_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 35)
            #shoulder_back_L
            if check_shapekey_driver('shoulder_back_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_back_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -35)
            #Arm_L
            #arm_up_L
            if check_shapekey_driver('arm_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 90)
            #arm_down_L
            if check_shapekey_driver('arm_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #arm_forw_L
            if check_shapekey_driver('arm_forw_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_forw_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #arm_back_L
            if check_shapekey_driver('arm_back_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_back_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #arm_twist_in_L
            if check_shapekey_driver('arm_twist_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_twist_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #arm_twist_out_L
            if check_shapekey_driver('arm_twist_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_twist_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Forearm_L
            #forearm_up_L
            if check_shapekey_driver('forearm_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #forearm_down_L
            if check_shapekey_driver('forearm_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -35)
            #forearm_twist_in_L
            if check_shapekey_driver('forearm_twist_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_twist_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #forearm_twist_out_L
            if check_shapekey_driver('forearm_twist_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_twist_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Hand_L
            #hand_up_L
            if check_shapekey_driver('hand_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #hand_down_L
            if check_shapekey_driver('hand_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #hand_forw_L
            if check_shapekey_driver('hand_forw_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_forw_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #hand_back_L
            if check_shapekey_driver('hand_back_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_back_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)

    #Arm_R
    def arm_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        #Shoulder_R
        add_shapekey(context, 'shoulder_up_R')
        add_shapekey(context, 'shoulder_down_R')
        add_shapekey(context, 'shoulder_forw_R')
        add_shapekey(context, 'shoulder_back_R')
        #Arm_R
        add_shapekey(context, 'arm_up_R')
        add_shapekey(context, 'arm_down_R')
        add_shapekey(context, 'arm_forw_R')
        add_shapekey(context, 'arm_back_R')
        add_shapekey(context, 'arm_twist_in_R')
        add_shapekey(context, 'arm_twist_out_R')
        #Forearm_R
        add_shapekey(context, 'forearm_up_R')
        add_shapekey(context, 'forearm_down_R')
        add_shapekey(context, 'forearm_twist_in_R')
        add_shapekey(context, 'forearm_twist_out_R')
        #Hand_R
        add_shapekey(context, 'hand_up_R')
        add_shapekey(context, 'hand_down_R')
        add_shapekey(context, 'hand_forw_R')
        add_shapekey(context, 'hand_back_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Shoulder_R
            #shoulder_up_R
            if check_shapekey_driver('shoulder_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -35)
            #shoulder_down_R
            if check_shapekey_driver('shoulder_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 20)
            #shoulder_forw_R
            if check_shapekey_driver('shoulder_forw_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_forw_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 35)
            #shoulder_back_R
            if check_shapekey_driver('shoulder_back_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shoulder_back_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'clavi_def_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -35)
            #Arm_R
            #arm_up_R
            if check_shapekey_driver('arm_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -90)
            #arm_down_R
            if check_shapekey_driver('arm_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #arm_forw_R
            if check_shapekey_driver('arm_forw_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_forw_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #arm_back_R
            if check_shapekey_driver('arm_back_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_back_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #arm_twist_in_R
            if check_shapekey_driver('arm_twist_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_twist_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #arm_twist_out_R
            if check_shapekey_driver('arm_twist_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['arm_twist_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'arm_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #Forearm_R
            #forearm_up_R
            if check_shapekey_driver('forearm_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #forearm_down_R
            if check_shapekey_driver('forearm_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -35)
            #forearm_twist_in_R
            if check_shapekey_driver('forearm_twist_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_twist_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #forearm_twist_out_R
            if check_shapekey_driver('forearm_twist_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['forearm_twist_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'forearm_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #Hand_R
            #hand_up_R
            if check_shapekey_driver('hand_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #hand_down_R
            if check_shapekey_driver('hand_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #hand_forw_R
            if check_shapekey_driver('hand_forw_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_forw_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #hand_back_R
            if check_shapekey_driver('hand_back_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['hand_back_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'hand_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)

    #Leg_L
    def leg_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        #Arm_L
        add_shapekey(context, 'thigh_out_L')
        add_shapekey(context, 'thigh_in_L')
        add_shapekey(context, 'thigh_forw_L')
        add_shapekey(context, 'thigh_back_L')
        add_shapekey(context, 'thigh_twist_in_L')
        add_shapekey(context, 'thigh_twist_out_L')
        #Shin_L
        add_shapekey(context, 'shin_up_L')
        add_shapekey(context, 'shin_down_L')
        add_shapekey(context, 'shin_twist_in_L')
        add_shapekey(context, 'shin_twist_out_L')
        #Foot_L
        add_shapekey(context, 'foot_up_L')
        add_shapekey(context, 'foot_down_L')
        add_shapekey(context, 'foot_in_L')
        add_shapekey(context, 'foot_out_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Thigh_L
            #thigh_out_L
            if check_shapekey_driver('thigh_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -90)
            #thigh_in_L
            if check_shapekey_driver('thigh_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #thigh_forw_L
            if check_shapekey_driver('thigh_forw_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_forw_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #thigh_back_L
            if check_shapekey_driver('thigh_back_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_back_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #thigh_twist_in_L
            if check_shapekey_driver('thigh_twist_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_twist_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #thigh_twist_out_L
            if check_shapekey_driver('thigh_twist_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_twist_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Shin_L
            #shin_up_L
            if check_shapekey_driver('shin_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #shin_down_L
            if check_shapekey_driver('shin_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_xz_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -35)
            #shin_twist_in_L
            if check_shapekey_driver('shin_twist_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_twist_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #shin_twist_out_L
            if check_shapekey_driver('shin_twist_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_twist_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_y_drv_L', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #Foot_L
            #foot_up_L
            if check_shapekey_driver('foot_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #foot_down_L
            if check_shapekey_driver('foot_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #foot_in_L
            if check_shapekey_driver('foot_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #foot_out_L
            if check_shapekey_driver('foot_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)

    #Leg_R
    def leg_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        #Arm_R
        add_shapekey(context, 'thigh_out_R')
        add_shapekey(context, 'thigh_in_R')
        add_shapekey(context, 'thigh_forw_R')
        add_shapekey(context, 'thigh_back_R')
        add_shapekey(context, 'thigh_twist_in_R')
        add_shapekey(context, 'thigh_twist_out_R')
        #Shin_R
        add_shapekey(context, 'shin_up_R')
        add_shapekey(context, 'shin_down_R')
        add_shapekey(context, 'shin_twist_in_R')
        add_shapekey(context, 'shin_twist_out_R')
        #Foot_R
        add_shapekey(context, 'foot_up_R')
        add_shapekey(context, 'foot_down_R')
        add_shapekey(context, 'foot_in_R')
        add_shapekey(context, 'foot_out_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #Thigh_R
            #thigh_out_R
            if check_shapekey_driver('thigh_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 90)
            #thigh_in_R
            if check_shapekey_driver('thigh_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #thigh_forw_R
            if check_shapekey_driver('thigh_forw_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_forw_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #thigh_back_R
            if check_shapekey_driver('thigh_back_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_back_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #thigh_twist_in_R
            if check_shapekey_driver('thigh_twist_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_twist_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #thigh_twist_out_R
            if check_shapekey_driver('thigh_twist_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['thigh_twist_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'thigh_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #Shin_R
            #shin_up_R
            if check_shapekey_driver('shin_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #shin_down_R
            if check_shapekey_driver('shin_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_xz_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -35)
            #shin_twist_in_R
            if check_shapekey_driver('shin_twist_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_twist_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, -90)
            #shin_twist_out_R
            if check_shapekey_driver('shin_twist_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['shin_twist_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'shin_y_drv_R', "''", 'LOCAL_SPACE', 'ROT_Y', 'SWING_TWIST_Y')
                add_mod_generator_angle(active_driver, 90)
            #Foot_R
            #foot_up_R
            if check_shapekey_driver('foot_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #foot_down_R
            if check_shapekey_driver('foot_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #foot_in_R
            if check_shapekey_driver('foot_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #foot_out_R
            if check_shapekey_driver('foot_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['foot_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'foot_twist_drv_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)

    Neck_Shapekeys: bpy.props.BoolProperty(default=True)
    Spine_Shapekeys: bpy.props.BoolProperty(default=True)
    Arms_Shapekeys: bpy.props.BoolProperty(default=True)
    Legs_Shapekeys: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        if self.Neck_Shapekeys:
            self.neck(context)
        if self.Spine_Shapekeys:
            self.spine(context)
        if self.Arms_Shapekeys:
            self.arm_L(context)
            self.arm_R(context)
        if self.Legs_Shapekeys:
            self.leg_L(context)
            self.leg_R(context)
        return {"FINISHED"}

class Operator_blenrig_add_fingers_shapekeys(bpy.types.Operator):

    bl_idname = "blenrig.add_fingers_shapekeys"
    bl_label = "BlenRig add Fingers Shapkeys"
    bl_description = "Add shapekeys for the fingers"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    #Index_L
    def index_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_ind_2_up_L')
        add_shapekey(context, 'fing_ind_2_down_L')
        add_shapekey(context, 'fing_ind_3_up_L')
        add_shapekey(context, 'fing_ind_3_down_L')
        add_shapekey(context, 'fing_ind_4_up_L')
        add_shapekey(context, 'fing_ind_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_ind_2_up_L
            if check_shapekey_driver('fing_ind_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_ind_2_down_L
            if check_shapekey_driver('fing_ind_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ind_3_up_L
            if check_shapekey_driver('fing_ind_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ind_3_down_L
            if check_shapekey_driver('fing_ind_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ind_4_up_L
            if check_shapekey_driver('fing_ind_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ind_4_down_L
            if check_shapekey_driver('fing_ind_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Mid_L
    def middle_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_mid_2_up_L')
        add_shapekey(context, 'fing_mid_2_down_L')
        add_shapekey(context, 'fing_mid_3_up_L')
        add_shapekey(context, 'fing_mid_3_down_L')
        add_shapekey(context, 'fing_mid_4_up_L')
        add_shapekey(context, 'fing_mid_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_mid_2_up_L
            if check_shapekey_driver('fing_mid_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_mid_2_down_L
            if check_shapekey_driver('fing_mid_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_mid_3_up_L
            if check_shapekey_driver('fing_mid_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_mid_3_down_L
            if check_shapekey_driver('fing_mid_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_mid_4_up_L
            if check_shapekey_driver('fing_mid_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_mid_4_down_L
            if check_shapekey_driver('fing_mid_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Ring_L
    def ring_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_ring_2_up_L')
        add_shapekey(context, 'fing_ring_2_down_L')
        add_shapekey(context, 'fing_ring_3_up_L')
        add_shapekey(context, 'fing_ring_3_down_L')
        add_shapekey(context, 'fing_ring_4_up_L')
        add_shapekey(context, 'fing_ring_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_ring_2_up_L
            if check_shapekey_driver('fing_ring_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_ring_2_down_L
            if check_shapekey_driver('fing_ring_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ring_3_up_L
            if check_shapekey_driver('fing_ring_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ring_3_down_L
            if check_shapekey_driver('fing_ring_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ring_4_up_L
            if check_shapekey_driver('fing_ring_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ring_4_down_L
            if check_shapekey_driver('fing_ring_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Little_L
    def little_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_lit_1_down_L')
        add_shapekey(context, 'fing_lit_2_up_L')
        add_shapekey(context, 'fing_lit_2_down_L')
        add_shapekey(context, 'fing_lit_3_up_L')
        add_shapekey(context, 'fing_lit_3_down_L')
        add_shapekey(context, 'fing_lit_4_up_L')
        add_shapekey(context, 'fing_lit_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_lit_1_down_L
            if check_shapekey_driver('fing_lit_1_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_1_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_1_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 30)
            #fing_lit_2_up_L
            if check_shapekey_driver('fing_lit_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_lit_2_down_L
            if check_shapekey_driver('fing_lit_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_lit_3_up_L
            if check_shapekey_driver('fing_lit_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_lit_3_down_L
            if check_shapekey_driver('fing_lit_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_lit_4_up_L
            if check_shapekey_driver('fing_lit_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_lit_4_down_L
            if check_shapekey_driver('fing_lit_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Thumb_L
    def thumb_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_thumb_1_down_L')
        add_shapekey(context, 'fing_thumb_1_up_L')
        add_shapekey(context, 'fing_thumb_1_in_L')
        add_shapekey(context, 'fing_thumb_1_out_L')
        add_shapekey(context, 'fing_thumb_2_up_L')
        add_shapekey(context, 'fing_thumb_2_down_L')
        add_shapekey(context, 'fing_thumb_3_up_L')
        add_shapekey(context, 'fing_thumb_3_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_thumb_1_down_L
            if check_shapekey_driver('fing_thumb_1_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_down_L'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #fing_thumb_1_up_L
            if check_shapekey_driver('fing_thumb_1_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_up_L'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_thumb_1_in_L
            if check_shapekey_driver('fing_thumb_1_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_in_L'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -20)
            #fing_thumb_1_out_L
            if check_shapekey_driver('fing_thumb_1_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_out_L'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_L', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 45)
            #fing_thumb_2_up_L
            if check_shapekey_driver('fing_thumb_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_thumb_2_down_L
            if check_shapekey_driver('fing_thumb_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_thumb_3_up_L
            if check_shapekey_driver('fing_thumb_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_thumb_3_down_L
            if check_shapekey_driver('fing_thumb_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Index_R
    def index_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_ind_2_up_R')
        add_shapekey(context, 'fing_ind_2_down_R')
        add_shapekey(context, 'fing_ind_3_up_R')
        add_shapekey(context, 'fing_ind_3_down_R')
        add_shapekey(context, 'fing_ind_4_up_R')
        add_shapekey(context, 'fing_ind_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_ind_2_up_R
            if check_shapekey_driver('fing_ind_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_ind_2_down_R
            if check_shapekey_driver('fing_ind_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ind_3_up_R
            if check_shapekey_driver('fing_ind_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ind_3_down_R
            if check_shapekey_driver('fing_ind_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ind_4_up_R
            if check_shapekey_driver('fing_ind_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ind_4_down_R
            if check_shapekey_driver('fing_ind_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ind_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ind_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Mid_R
    def middle_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_mid_2_up_R')
        add_shapekey(context, 'fing_mid_2_down_R')
        add_shapekey(context, 'fing_mid_3_up_R')
        add_shapekey(context, 'fing_mid_3_down_R')
        add_shapekey(context, 'fing_mid_4_up_R')
        add_shapekey(context, 'fing_mid_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_mid_2_up_R
            if check_shapekey_driver('fing_mid_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_mid_2_down_R
            if check_shapekey_driver('fing_mid_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_mid_3_up_R
            if check_shapekey_driver('fing_mid_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_mid_3_down_R
            if check_shapekey_driver('fing_mid_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_mid_4_up_R
            if check_shapekey_driver('fing_mid_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_mid_4_down_R
            if check_shapekey_driver('fing_mid_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_mid_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_mid_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Ring_R
    def ring_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_ring_2_up_R')
        add_shapekey(context, 'fing_ring_2_down_R')
        add_shapekey(context, 'fing_ring_3_up_R')
        add_shapekey(context, 'fing_ring_3_down_R')
        add_shapekey(context, 'fing_ring_4_up_R')
        add_shapekey(context, 'fing_ring_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_ring_2_up_R
            if check_shapekey_driver('fing_ring_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_ring_2_down_R
            if check_shapekey_driver('fing_ring_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ring_3_up_R
            if check_shapekey_driver('fing_ring_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ring_3_down_R
            if check_shapekey_driver('fing_ring_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_ring_4_up_R
            if check_shapekey_driver('fing_ring_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_ring_4_down_R
            if check_shapekey_driver('fing_ring_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_ring_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_ring_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Little_R
    def little_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_lit_1_down_R')
        add_shapekey(context, 'fing_lit_2_up_R')
        add_shapekey(context, 'fing_lit_2_down_R')
        add_shapekey(context, 'fing_lit_3_up_R')
        add_shapekey(context, 'fing_lit_3_down_R')
        add_shapekey(context, 'fing_lit_4_up_R')
        add_shapekey(context, 'fing_lit_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_lit_1_down_R
            if check_shapekey_driver('fing_lit_1_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_1_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_1_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 30)
            #fing_lit_2_up_R
            if check_shapekey_driver('fing_lit_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_lit_2_down_R
            if check_shapekey_driver('fing_lit_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_lit_3_up_R
            if check_shapekey_driver('fing_lit_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_lit_3_down_R
            if check_shapekey_driver('fing_lit_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_lit_4_up_R
            if check_shapekey_driver('fing_lit_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_lit_4_down_R
            if check_shapekey_driver('fing_lit_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_lit_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_lit_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Thumb_R
    def thumb_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'fing_thumb_1_down_R')
        add_shapekey(context, 'fing_thumb_1_up_R')
        add_shapekey(context, 'fing_thumb_1_in_R')
        add_shapekey(context, 'fing_thumb_1_out_R')
        add_shapekey(context, 'fing_thumb_2_up_R')
        add_shapekey(context, 'fing_thumb_2_down_R')
        add_shapekey(context, 'fing_thumb_3_up_R')
        add_shapekey(context, 'fing_thumb_3_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #fing_thumb_1_down_R
            if check_shapekey_driver('fing_thumb_1_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_down_R'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)
            #fing_thumb_1_up_R
            if check_shapekey_driver('fing_thumb_1_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_up_R'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_thumb_1_in_R
            if check_shapekey_driver('fing_thumb_1_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_in_R'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, 20)
            #fing_thumb_1_out_R
            if check_shapekey_driver('fing_thumb_1_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_1_out_R'], 'value', 'SUM', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_1_ik_R', "''", 'LOCAL_SPACE', 'ROT_Z', 'SWING_TWIST_Z')
                add_mod_generator_angle(active_driver, -45)
            #fing_thumb_2_up_R
            if check_shapekey_driver('fing_thumb_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #fing_thumb_2_down_R
            if check_shapekey_driver('fing_thumb_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #fing_thumb_3_up_R
            if check_shapekey_driver('fing_thumb_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #fing_thumb_3_down_R
            if check_shapekey_driver('fing_thumb_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['fing_thumb_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'fing_thumb_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    Index_Shapekeys: bpy.props.BoolProperty(default=True)
    Middle_Shapekeys: bpy.props.BoolProperty(default=True)
    Ring_Shapekeys: bpy.props.BoolProperty(default=True)
    Little_Shapekeys: bpy.props.BoolProperty(default=True)
    Thumb_Shapekeys: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        if self.Index_Shapekeys:
            self.index_L(context)
        if self.Middle_Shapekeys:
            self.middle_L(context)
        if self.Ring_Shapekeys:
            self.ring_L(context)
        if self.Little_Shapekeys:
            self.little_L(context)
        if self.Thumb_Shapekeys:
            self.thumb_L(context)
        if self.Index_Shapekeys:
            self.index_R(context)
        if self.Middle_Shapekeys:
            self.middle_R(context)
        if self.Ring_Shapekeys:
            self.ring_R(context)
        if self.Little_Shapekeys:
            self.little_R(context)
        if self.Thumb_Shapekeys:
            self.thumb_R(context)
        return {"FINISHED"}

class Operator_blenrig_add_toes_shapekeys(bpy.types.Operator):

    bl_idname = "blenrig.add_toes_shapekeys"
    bl_label = "BlenRig add Toes Shapkeys"
    bl_description = "Add shapekeys for the toes"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    #Toe_Index_L
    def toe_index_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_ind_2_up_L')
        add_shapekey(context, 'toe_ind_2_down_L')
        add_shapekey(context, 'toe_ind_3_up_L')
        add_shapekey(context, 'toe_ind_3_down_L')
        add_shapekey(context, 'toe_ind_4_up_L')
        add_shapekey(context, 'toe_ind_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_ind_2_up_L
            if check_shapekey_driver('toe_ind_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_ind_2_down_L
            if check_shapekey_driver('toe_ind_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_ind_3_up_L
            if check_shapekey_driver('toe_ind_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_ind_3_down_L
            if check_shapekey_driver('toe_ind_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_ind_4_up_L
            if check_shapekey_driver('toe_ind_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_ind_4_down_L
            if check_shapekey_driver('toe_ind_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Mid_L
    def toe_middle_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_mid_2_up_L')
        add_shapekey(context, 'toe_mid_2_down_L')
        add_shapekey(context, 'toe_mid_3_up_L')
        add_shapekey(context, 'toe_mid_3_down_L')
        add_shapekey(context, 'toe_mid_4_up_L')
        add_shapekey(context, 'toe_mid_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_mid_2_up_L
            if check_shapekey_driver('toe_mid_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_mid_2_down_L
            if check_shapekey_driver('toe_mid_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_mid_3_up_L
            if check_shapekey_driver('toe_mid_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_mid_3_down_L
            if check_shapekey_driver('toe_mid_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_mid_4_up_L
            if check_shapekey_driver('toe_mid_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_mid_4_down_L
            if check_shapekey_driver('toe_mid_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Fourth_L
    def toe_fourth_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_fourth_2_up_L')
        add_shapekey(context, 'toe_fourth_2_down_L')
        add_shapekey(context, 'toe_fourth_3_up_L')
        add_shapekey(context, 'toe_fourth_3_down_L')
        add_shapekey(context, 'toe_fourth_4_up_L')
        add_shapekey(context, 'toe_fourth_4_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_fourth_2_up_L
            if check_shapekey_driver('toe_fourth_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_fourth_2_down_L
            if check_shapekey_driver('toe_fourth_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_fourth_3_up_L
            if check_shapekey_driver('toe_fourth_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_fourth_3_down_L
            if check_shapekey_driver('toe_fourth_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_fourth_4_up_L
            if check_shapekey_driver('toe_fourth_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_fourth_4_down_L
            if check_shapekey_driver('toe_fourth_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_4_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Little_L
    def toe_little_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_lit_2_up_L')
        add_shapekey(context, 'toe_lit_2_down_L')
        add_shapekey(context, 'toe_lit_3_up_L')
        add_shapekey(context, 'toe_lit_3_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_lit_2_up_L
            if check_shapekey_driver('toe_lit_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_lit_2_down_L
            if check_shapekey_driver('toe_lit_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_lit_3_up_L
            if check_shapekey_driver('toe_lit_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_lit_3_down_L
            if check_shapekey_driver('toe_lit_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Big_L
    def toe_big_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_big_2_up_L')
        add_shapekey(context, 'toe_big_2_down_L')
        add_shapekey(context, 'toe_big_3_up_L')
        add_shapekey(context, 'toe_big_3_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_big_2_up_L
            if check_shapekey_driver('toe_big_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_big_2_down_L
            if check_shapekey_driver('toe_big_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_2_rot_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_big_3_up_L
            if check_shapekey_driver('toe_big_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_big_3_down_L
            if check_shapekey_driver('toe_big_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_3_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Index_R
    def toe_index_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_ind_2_up_R')
        add_shapekey(context, 'toe_ind_2_down_R')
        add_shapekey(context, 'toe_ind_3_up_R')
        add_shapekey(context, 'toe_ind_3_down_R')
        add_shapekey(context, 'toe_ind_4_up_R')
        add_shapekey(context, 'toe_ind_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_ind_2_up_R
            if check_shapekey_driver('toe_ind_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_ind_2_down_R
            if check_shapekey_driver('toe_ind_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_ind_3_up_R
            if check_shapekey_driver('toe_ind_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_ind_3_down_R
            if check_shapekey_driver('toe_ind_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_ind_4_up_R
            if check_shapekey_driver('toe_ind_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_ind_4_down_R
            if check_shapekey_driver('toe_ind_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_ind_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_ind_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Mid_R
    def toe_middle_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_mid_2_up_R')
        add_shapekey(context, 'toe_mid_2_down_R')
        add_shapekey(context, 'toe_mid_3_up_R')
        add_shapekey(context, 'toe_mid_3_down_R')
        add_shapekey(context, 'toe_mid_4_up_R')
        add_shapekey(context, 'toe_mid_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_mid_2_up_R
            if check_shapekey_driver('toe_mid_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_mid_2_down_R
            if check_shapekey_driver('toe_mid_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_mid_3_up_R
            if check_shapekey_driver('toe_mid_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_mid_3_down_R
            if check_shapekey_driver('toe_mid_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_mid_4_up_R
            if check_shapekey_driver('toe_mid_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_mid_4_down_R
            if check_shapekey_driver('toe_mid_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_mid_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_mid_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Fourth_R
    def toe_fourth_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_fourth_2_up_R')
        add_shapekey(context, 'toe_fourth_2_down_R')
        add_shapekey(context, 'toe_fourth_3_up_R')
        add_shapekey(context, 'toe_fourth_3_down_R')
        add_shapekey(context, 'toe_fourth_4_up_R')
        add_shapekey(context, 'toe_fourth_4_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_fourth_2_up_R
            if check_shapekey_driver('toe_fourth_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_fourth_2_down_R
            if check_shapekey_driver('toe_fourth_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_fourth_3_up_R
            if check_shapekey_driver('toe_fourth_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_fourth_3_down_R
            if check_shapekey_driver('toe_fourth_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_fourth_4_up_R
            if check_shapekey_driver('toe_fourth_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_fourth_4_down_R
            if check_shapekey_driver('toe_fourth_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_fourth_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_fourth_4_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Rittle_R
    def toe_little_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_lit_2_up_R')
        add_shapekey(context, 'toe_lit_2_down_R')
        add_shapekey(context, 'toe_lit_3_up_R')
        add_shapekey(context, 'toe_lit_3_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_lit_2_up_R
            if check_shapekey_driver('toe_lit_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_lit_2_down_R
            if check_shapekey_driver('toe_lit_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_lit_3_up_R
            if check_shapekey_driver('toe_lit_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_lit_3_down_R
            if check_shapekey_driver('toe_lit_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_lit_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_lit_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    #Toe_Big_R
    def toe_big_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle

        #Add Shapekeys
        add_shapekey(context, 'toe_big_2_up_R')
        add_shapekey(context, 'toe_big_2_down_R')
        add_shapekey(context, 'toe_big_3_up_R')
        add_shapekey(context, 'toe_big_3_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj

            #Skip if Driver already present
            #toe_big_2_up_R
            if check_shapekey_driver('toe_big_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -90)
            #toe_big_2_down_R
            if check_shapekey_driver('toe_big_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_2_rot_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)
            #toe_big_3_up_R
            if check_shapekey_driver('toe_big_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, -45)
            #toe_big_3_down_R
            if check_shapekey_driver('toe_big_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['toe_big_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'toe_big_3_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 90)

    Toe_Big_Shapekeys: bpy.props.BoolProperty(default=True)
    Toe_Index_Shapekeys: bpy.props.BoolProperty(default=True)
    Toe_Middle_Shapekeys: bpy.props.BoolProperty(default=True)
    Toe_Fourth_Shapekeys: bpy.props.BoolProperty(default=True)
    Toe_Little_Shapekeys: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        if self.Toe_Big_Shapekeys:
            self.toe_big_L(context)
        if self.Toe_Index_Shapekeys:
            self.toe_index_L(context)
        if self.Toe_Middle_Shapekeys:
            self.toe_middle_L(context)
        if self.Toe_Fourth_Shapekeys:
            self.toe_fourth_L(context)
        if self.Toe_Little_Shapekeys:
            self.toe_little_L(context)
        if self.Toe_Big_Shapekeys:
            self.toe_big_R(context)
        if self.Toe_Index_Shapekeys:
            self.toe_index_R(context)
        if self.Toe_Middle_Shapekeys:
            self.toe_middle_R(context)
        if self.Toe_Fourth_Shapekeys:
            self.toe_fourth_R(context)
        if self.Toe_Little_Shapekeys:
            self.toe_little_R(context)
        return {"FINISHED"}

class Operator_blenrig_add_face_shapekeys(bpy.types.Operator):

    bl_idname = "blenrig.add_face_shapekeys"
    bl_label = "BlenRig add Face Shapkeys"
    bl_description = "Add shapekeys for the Face"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            return True
        else:
            return False

    #Frown
    def frown(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location

        #Add Shapekeys
        add_shapekey(context, 'frown_up')
        add_shapekey(context, 'frown_down')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Rename Shapekeys Datablock
            ob.data.shape_keys.name = 'ShapeKeys'

            #Skip if Driver already present
            #frown_up
            if check_shapekey_driver('frown_up'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['frown_up'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'frown_ctrl', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_mid'].bone.length * 0.75)
            #frown_down
            if check_shapekey_driver('frown_down'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['frown_down'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'frown_ctrl', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['nose_def_1_mid'].bone.length * 0.75))

    #Eyebrows_L
    def eyebrows_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location

        #Add Shapekeys
        add_shapekey(context, 'brow_1_up_L')
        add_shapekey(context, 'brow_1_down_L')
        add_shapekey(context, 'brow_1_in_L')
        add_shapekey(context, 'brow_2_up_L')
        add_shapekey(context, 'brow_2_down_L')
        add_shapekey(context, 'brow_3_up_L')
        add_shapekey(context, 'brow_3_down_L')
        add_shapekey(context, 'brow_4_up_L')
        add_shapekey(context, 'brow_4_down_L')
        add_shapekey(context, 'brow_5_up_L')
        add_shapekey(context, 'brow_5_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #brow_1_up_L
            if check_shapekey_driver('brow_1_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_1_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_1_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_1_L'].bone.length * 0.75)
            #brow_1_down_L
            if check_shapekey_driver('brow_1_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_1_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_1_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['nose_side_def_1_L'].bone.length * 0.75))
            #brow_1_in_L
            if check_shapekey_driver('brow_1_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_1_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_1_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
                add_mod_generator_location(active_driver, pbones['frown_low_def_L'].bone.length * 0.75)
            #brow_2_up_L
            if check_shapekey_driver('brow_2_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_2_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_2_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_2_L'].bone.length * 0.75)
            #brow_2_down_L
            if check_shapekey_driver('brow_2_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_2_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_2_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_2_L'].bone.length * 0.75))
            #brow_3_up_L
            if check_shapekey_driver('brow_3_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_3_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_3_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_3_L'].bone.length * 0.75)
            #brow_3_down_L
            if check_shapekey_driver('brow_3_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_3_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_3_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_3_L'].bone.length * 0.75))
            #brow_4_up_L
            if check_shapekey_driver('brow_4_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_4_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_4_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_4_L'].bone.length * 0.75)
            #brow_4_down_L
            if check_shapekey_driver('brow_4_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_4_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_4_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_4_L'].bone.length * 0.75))
            #brow_5_up_L
            if check_shapekey_driver('brow_5_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_5_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_5_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_5_L'].bone.length * 0.75)
            #brow_5_down_L
            if check_shapekey_driver('brow_5_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_5_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_5_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_5_L'].bone.length * 0.75))

    #Eyebrows_R
    def eyebrows_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location

        #Add Shapekeys
        add_shapekey(context, 'brow_1_up_R')
        add_shapekey(context, 'brow_1_down_R')
        add_shapekey(context, 'brow_1_in_R')
        add_shapekey(context, 'brow_2_up_R')
        add_shapekey(context, 'brow_2_down_R')
        add_shapekey(context, 'brow_3_up_R')
        add_shapekey(context, 'brow_3_down_R')
        add_shapekey(context, 'brow_4_up_R')
        add_shapekey(context, 'brow_4_down_R')
        add_shapekey(context, 'brow_5_up_R')
        add_shapekey(context, 'brow_5_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #brow_1_up_R
            if check_shapekey_driver('brow_1_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_1_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_1_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_1_R'].bone.length * 0.75)
            #brow_1_down_R
            if check_shapekey_driver('brow_1_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_1_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_1_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['nose_side_def_1_R'].bone.length * 0.75))
            #brow_1_in_R
            if check_shapekey_driver('brow_1_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_1_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_1_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['frown_low_def_R'].bone.length * 0.75))
            #brow_2_up_R
            if check_shapekey_driver('brow_2_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_2_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_2_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_2_R'].bone.length * 0.75)
            #brow_2_down_R
            if check_shapekey_driver('brow_2_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_2_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_2_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_2_R'].bone.length * 0.75))
            #brow_3_up_R
            if check_shapekey_driver('brow_3_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_3_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_3_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_3_R'].bone.length * 0.75)
            #brow_3_down_R
            if check_shapekey_driver('brow_3_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_3_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_3_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_3_R'].bone.length * 0.75))
            #brow_4_up_R
            if check_shapekey_driver('brow_4_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_4_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_4_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_4_R'].bone.length * 0.75)
            #brow_4_down_R
            if check_shapekey_driver('brow_4_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_4_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_4_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_4_R'].bone.length * 0.75))
            #brow_5_up_R
            if check_shapekey_driver('brow_5_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_5_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_5_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones['forehead_def_5_R'].bone.length * 0.75)
            #brow_5_down_R
            if check_shapekey_driver('brow_5_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['brow_5_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'brow_drv_5_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones['brow_arch_def_5_R'].bone.length * 0.75))

    #Upper_Eyelid_L
    def eyelid_up_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'eyelid_up_up_L')
        add_shapekey(context, 'eyelid_up_down_1_L')
        add_shapekey(context, 'eyelid_up_down_2_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #eyelid_up_up_L
            if check_shapekey_driver('eyelid_up_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_up_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_up_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L)
            #eyelid_up_down_1_L
            if check_shapekey_driver('eyelid_up_down_1_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_up_down_1_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_up_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L / 2))
            #eyelid_up_down_2_L
            if check_shapekey_driver('eyelid_up_down_2_L'):
                pass
            else:
                #Get eyelid_up_down_1_L value
                eyelid_up_down_1_L_value = []
                for driver in ob.data.shape_keys.animation_data.drivers:
                    if 'eyelid_up_down_1_L' in driver.data_path:
                        for mod in driver.modifiers:
                            if mod.type == 'GENERATOR':
                                value = 1 / mod.coefficients[1]
                                eyelid_up_down_1_L_value.append(value)
                #Coefficient_1 equals the movement range between eyelid_up_down_1_L and EYELID_DOWN_LIMIT_L
                coefficient_1 = pbones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L - abs(eyelid_up_down_1_L_value[0])
                #Coefficient_0 represents the size of eyelid_up_down_1_L compared to the range of motion of eyelid_up_down_2_L(coefficient_1)
                coefficient_0 = coefficient_1 / abs(eyelid_up_down_1_L_value[0])
                active_driver = add_shapekeys_driver(shapekeys['eyelid_up_down_2_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_up_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                #Add generator taking eyelid_up_down_1_L value into account
                add_mod_generator_location_offset(active_driver, -(coefficient_0), -(coefficient_1))

    #Upper_Eyelid_R
    def eyelid_up_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'eyelid_up_up_R')
        add_shapekey(context, 'eyelid_up_down_1_R')
        add_shapekey(context, 'eyelid_up_down_2_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #eyelid_up_up_R
            if check_shapekey_driver('eyelid_up_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_up_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_up_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["eyelid_up_ctrl_R"].EYELID_UP_LIMIT_R)
            #eyelid_up_down_1_R
            if check_shapekey_driver('eyelid_up_down_1_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_up_down_1_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_up_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["eyelid_up_ctrl_R"].EYELID_DOWN_LIMIT_R / 2))
            #eyelid_up_down_2_R
            if check_shapekey_driver('eyelid_up_down_2_R'):
                pass
            else:
                #Get eyelid_up_down_1_R value
                eyelid_up_down_1_R_value = []
                for driver in ob.data.shape_keys.animation_data.drivers:
                    if 'eyelid_up_down_1_R' in driver.data_path:
                        for mod in driver.modifiers:
                            if mod.type == 'GENERATOR':
                                value = 1 / mod.coefficients[1]
                                eyelid_up_down_1_R_value.append(value)
                #Coefficient_1 equals the movement range between eyelid_up_down_1_R and EYELID_DOWN_LIMIT_R
                coefficient_1 = pbones["eyelid_up_ctrl_R"].EYELID_DOWN_LIMIT_R - abs(eyelid_up_down_1_R_value[0])
                #Coefficient_0 represents the size of eyelid_up_down_1_R compared to the range of motion of eyelid_up_down_2_R(coefficient_1)
                coefficient_0 = coefficient_1 / abs(eyelid_up_down_1_R_value[0])
                active_driver = add_shapekeys_driver(shapekeys['eyelid_up_down_2_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_up_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                #Add generator taking eyelid_up_down_1_R value into account
                add_mod_generator_location_offset(active_driver, -(coefficient_0), -(coefficient_1))

    #Lower_Eyelid_L
    def eyelid_low_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'eyelid_low_down_L')
        add_shapekey(context, 'eyelid_low_up_1_L')
        add_shapekey(context, 'eyelid_low_up_2_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #eyelid_low_down_L
            if check_shapekey_driver('eyelid_low_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_low_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_low_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["eyelid_low_ctrl_L"].EYELID_DOWN_LIMIT_L))
            #eyelid_low_up_1_L
            if check_shapekey_driver('eyelid_low_up_1_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_low_up_1_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_low_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L / 2)
            #eyelid_low_up_2_L
            if check_shapekey_driver('eyelid_low_up_2_L'):
                pass
            else:
                #Get eyelid_low_up_1_L value
                eyelid_low_up_1_L_value = []
                for driver in ob.data.shape_keys.animation_data.drivers:
                    if 'eyelid_low_up_1_L' in driver.data_path:
                        for mod in driver.modifiers:
                            if mod.type == 'GENERATOR':
                                value = 1 / mod.coefficients[1]
                                eyelid_low_up_1_L_value.append(value)
                #Coefficient_1 equals the movement range between eyelid_low_up_1_L and EYELID_UP_LIMIT_L
                coefficient_1 = pbones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L - abs(eyelid_low_up_1_L_value[0])
                #Coefficient_0 represents the size of eyelid_low_up_1_L compared to the range of motion of eyelid_low_up_2_L(coefficient_1)
                coefficient_0 = coefficient_1 / abs(eyelid_low_up_1_L_value[0])
                active_driver = add_shapekeys_driver(shapekeys['eyelid_low_up_2_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_low_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                #Add generator taking eyelid_low_up_1_L value into account
                add_mod_generator_location_offset(active_driver, -(coefficient_0), coefficient_1)

    #Lower_Eyelid_R
    def eyelid_low_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'eyelid_low_down_R')
        add_shapekey(context, 'eyelid_low_up_1_R')
        add_shapekey(context, 'eyelid_low_up_2_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #eyelid_low_down_R
            if check_shapekey_driver('eyelid_low_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_low_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_low_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["eyelid_low_ctrl_R"].EYELID_DOWN_LIMIT_R))
            #eyelid_low_up_1_R
            if check_shapekey_driver('eyelid_low_up_1_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['eyelid_low_up_1_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_low_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["eyelid_low_ctrl_R"].EYELID_UP_LIMIT_R / 2)
            #eyelid_low_up_2_R
            if check_shapekey_driver('eyelid_low_up_2_R'):
                pass
            else:
                #Get eyelid_low_up_1_R value
                eyelid_low_up_1_R_value = []
                for driver in ob.data.shape_keys.animation_data.drivers:
                    if 'eyelid_low_up_1_R' in driver.data_path:
                        for mod in driver.modifiers:
                            if mod.type == 'GENERATOR':
                                value = 1 / mod.coefficients[1]
                                eyelid_low_up_1_R_value.append(value)
                #Coefficient_1 equals the movement range between eyelid_low_up_1_R and EYELID_UP_LIMIT_R
                coefficient_1 = pbones["eyelid_low_ctrl_R"].EYELID_UP_LIMIT_R - abs(eyelid_low_up_1_R_value[0])
                #Coefficient_0 represents the size of eyelid_low_up_1_R compared to the range of motion of eyelid_low_up_2_R(coefficient_1)
                coefficient_0 = coefficient_1 / abs(eyelid_low_up_1_R_value[0])
                active_driver = add_shapekeys_driver(shapekeys['eyelid_low_up_2_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'eyelid_low_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                #Add generator taking eyelid_low_up_1_R value into account
                add_mod_generator_location_offset(active_driver, -(coefficient_0), coefficient_1)

    #Cheek_L
    def cheek_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'cheek_up_L')
        add_shapekey(context, 'cheek_down_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #cheek_up_L
            if check_shapekey_driver('cheek_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['cheek_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'cheek_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L)
            #cheek_down_L
            if check_shapekey_driver('cheek_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['cheek_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'cheek_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["cheek_ctrl_L"].CHEEK_DOWN_LIMIT_L))

    #Cheek_R
    def cheek_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'cheek_up_R')
        add_shapekey(context, 'cheek_down_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #cheek_up_R
            if check_shapekey_driver('cheek_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['cheek_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'cheek_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["cheek_ctrl_R"].CHEEK_UP_LIMIT_R)
            #cheek_down_R
            if check_shapekey_driver('cheek_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['cheek_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'cheek_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["cheek_ctrl_R"].CHEEK_DOWN_LIMIT_R))

    #Nose_L
    def nose_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'nose_frown_L')
        add_shapekey(context, 'nostril_expand_L')
        add_shapekey(context, 'nostril_collapse_L')
        add_shapekey(context, 'nostril_frown_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #nose_frown_L
            if check_shapekey_driver('nose_frown_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nose_frown_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nose_frown_ctrl_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["nose_frown_ctrl_L"].FROWN_LIMIT_L)
            #nostril_expand_L
            if check_shapekey_driver('nostril_expand_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nostril_expand_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nostril_ctrl_L', "''", 'LOCAL_SPACE', 'SCALE_X', 'AUTO')
                add_mod_generator_location_offset(active_driver, -1.0, 1.0)
            #nostril_collapse_L
            if check_shapekey_driver('nostril_collapse_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nostril_collapse_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nostril_ctrl_L', "''", 'LOCAL_SPACE', 'SCALE_X', 'AUTO')
                add_mod_generator_location_offset(active_driver, 2.0, -0.5)
            #nostril_frown_L
            if check_shapekey_driver('nostril_frown_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nostril_frown_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nostril_ctrl_L', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)

    #Nose_R
    def nose_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'nose_frown_R')
        add_shapekey(context, 'nostril_expand_R')
        add_shapekey(context, 'nostril_collapse_R')
        add_shapekey(context, 'nostril_frown_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #nose_frown_R
            if check_shapekey_driver('nose_frown_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nose_frown_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nose_frown_ctrl_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["nose_frown_ctrl_R"].FROWN_LIMIT_R)
            #nostril_expand_R
            if check_shapekey_driver('nostril_expand_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nostril_expand_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nostril_ctrl_R', "''", 'LOCAL_SPACE', 'SCALE_X', 'AUTO')
                add_mod_generator_location_offset(active_driver, -1.0, 1.0)
            #nostril_collapse_R
            if check_shapekey_driver('nostril_collapse_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nostril_collapse_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nostril_ctrl_R', "''", 'LOCAL_SPACE', 'SCALE_X', 'AUTO')
                add_mod_generator_location_offset(active_driver, 2.0, -0.5)
            #nostril_frown_R
            if check_shapekey_driver('nostril_frown_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['nostril_frown_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'nostril_ctrl_R', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_mod_generator_angle(active_driver, 45)

    #Mouth_L
    def mouth_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_corner_out_L')
        add_shapekey(context, 'mouth_corner_up_L')
        add_shapekey(context, 'mouth_corner_down_L')
        add_shapekey(context, 'mouth_corner_back_L')
        add_shapekey(context, 'mouth_corner_out_up_fix_L')
        add_shapekey(context, 'mouth_corner_out_down_fix_L')
        add_shapekey(context, 'mouth_corner_out_back_fix_L')
        add_shapekey(context, 'mouth_corner_out_back_up_fix_L')
        add_shapekey(context, 'mouth_corner_out_back_down_fix_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #mouth_corner_out_L
            if check_shapekey_driver('mouth_corner_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L))
            #mouth_corner_up_L
            if check_shapekey_driver('mouth_corner_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_up_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_corner_L"].UP_LIMIT_L)
            #mouth_corner_down_L
            if check_shapekey_driver('mouth_corner_down_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_down_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].DOWN_LIMIT_L))
            #mouth_corner_back_L
            if check_shapekey_driver('mouth_corner_back_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_back_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].BACK_LIMIT_L))

            #Corrective Shapes

            #Legacy Transforms Based Drivers
            # #mouth_corner_out_up_fix_L
            # if check_shapekey_driver('mouth_corner_out_up_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_up_fix_L'], 'value', 'SCRIPTED', '100 * var_out * var_up if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_up', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].UP_LIMIT_L * 100)
            # #mouth_corner_out_down_fix_L
            # if check_shapekey_driver('mouth_corner_out_down_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_down_fix_L'], 'value', 'SCRIPTED', '100 * var_out * var_down if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_down', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].DOWN_LIMIT_L) * 100)
            # #mouth_corner_out_back_fix_L
            # if check_shapekey_driver('mouth_corner_out_back_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_fix_L'], 'value', 'SCRIPTED', '100 * var_out * var_back if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_back', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].BACK_LIMIT_L) * 100)
            # #mouth_corner_out_back_up_fix_L
            # if check_shapekey_driver('mouth_corner_out_back_up_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_up_fix_L'], 'value', 'SCRIPTED', '1000 * var_out * var_up * var_back if var_out < 0 and var_up > 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_up', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_back', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].UP_LIMIT_L * -(pbones["mouth_corner_L"].BACK_LIMIT_L) * 1000)
            # #mouth_corner_out_back_down_fix_L
            # if check_shapekey_driver('mouth_corner_out_back_down_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_down_fix_L'], 'value', 'SCRIPTED', '1000 * var_out * var_down * var_back if var_out < 0 and var_down < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_down', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_back', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].DOWN_LIMIT_L) * -(pbones["mouth_corner_L"].BACK_LIMIT_L) * 1000)


            #mouth_corner_out_up_fix_L
            if check_shapekey_driver('mouth_corner_out_up_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_up_fix_L'], 'value', 'SCRIPTED', 'var_out * var_up')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_up', keys_name, 'mouth_corner_up_L')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_down_fix_L
            if check_shapekey_driver('mouth_corner_out_down_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_down_fix_L'], 'value', 'SCRIPTED', 'var_out * var_down')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_down', keys_name, 'mouth_corner_down_L')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_back_fix_L
            if check_shapekey_driver('mouth_corner_out_back_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_fix_L'], 'value', 'SCRIPTED', 'var_out * var_back')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_back', keys_name, 'mouth_corner_back_L')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_back_up_fix_L
            if check_shapekey_driver('mouth_corner_out_back_up_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_up_fix_L'], 'value', 'SCRIPTED', 'var_out * var_up * var_back')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_up', keys_name, 'mouth_corner_up_L')
                add_vars_shapekeys(active_driver, 'var_back', keys_name, 'mouth_corner_back_L')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_back_down_fix_L
            if check_shapekey_driver('mouth_corner_out_back_down_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_down_fix_L'], 'value', 'SCRIPTED', 'var_out * var_down * var_back')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_down', keys_name, 'mouth_corner_down_L')
                add_vars_shapekeys(active_driver, 'var_back', keys_name, 'mouth_corner_back_L')
                add_mod_generator_location(active_driver, 1)

    #Mouth_Extra_L
    def mouth_extra_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_corner_forw_L')
        add_shapekey(context, 'mouth_corner_out_forw_fix_L')
        add_shapekey(context, 'mouth_corner_out_forw_up_fix_L')
        add_shapekey(context, 'mouth_corner_out_forw_down_fix_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #Mostly used in Quadruped faces


            #mouth_corner_forw_L
            if check_shapekey_driver('mouth_corner_forw_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_forw_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_corner_L"].FORW_LIMIT_L)

            # #Legacy Transforms Based Drivers
            # #mouth_corner_out_forw_fix_L
            # if check_shapekey_driver('mouth_corner_out_forw_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_fix_L'], 'value', 'SCRIPTED', '100 * var_out * var_forw if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_forw', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].FORW_LIMIT_L * 100)
            # #mouth_corner_out_forw_up_fix_L
            # if check_shapekey_driver('mouth_corner_out_forw_up_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_up_fix_L'], 'value', 'SCRIPTED', '1000 * var_out * var_up * var_forw if var_out < 0 and var_up > 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_up', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_forw', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].UP_LIMIT_L * pbones["mouth_corner_L"].FORW_LIMIT_L * 1000)
            # #mouth_corner_out_forw_down_fix_L
            # if check_shapekey_driver('mouth_corner_out_forw_down_fix_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_down_fix_L'], 'value', 'SCRIPTED', '1000 * var_out * var_down * var_forw if var_out < 0 and var_down < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_down', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_forw', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].DOWN_LIMIT_L) * pbones["mouth_corner_L"].FORW_LIMIT_L * 1000)

            #mouth_corner_out_forw_fix_L
            if check_shapekey_driver('mouth_corner_out_forw_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_fix_L'], 'value', 'SCRIPTED', 'var_out * var_forw')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_forw', keys_name, 'mouth_corner_forw_L')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_forw_up_fix_L
            if check_shapekey_driver('mouth_corner_out_forw_up_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_up_fix_L'], 'value', 'SCRIPTED', 'var_out * var_forw * var_up')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_forw', keys_name, 'mouth_corner_forw_L')
                add_vars_shapekeys(active_driver, 'var_up', keys_name, 'mouth_corner_up_L')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_forw_down_fix_L
            if check_shapekey_driver('mouth_corner_out_forw_down_fix_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_down_fix_L'], 'value', 'SCRIPTED', 'var_out * var_forw * var_down')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_forw', keys_name, 'mouth_corner_forw_L')
                add_vars_shapekeys(active_driver, 'var_down', keys_name, 'mouth_corner_down_L')
                add_mod_generator_location(active_driver, 1)


    #Mouth_R
    def mouth_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_corner_out_R')
        add_shapekey(context, 'mouth_corner_up_R')
        add_shapekey(context, 'mouth_corner_down_R')
        add_shapekey(context, 'mouth_corner_back_R')
        add_shapekey(context, 'mouth_corner_out_up_fix_R')
        add_shapekey(context, 'mouth_corner_out_down_fix_R')
        add_shapekey(context, 'mouth_corner_out_back_fix_R')
        add_shapekey(context, 'mouth_corner_out_back_up_fix_R')
        add_shapekey(context, 'mouth_corner_out_back_down_fix_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #mouth_corner_out_R
            if check_shapekey_driver('mouth_corner_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_corner_R"].OUT_LIMIT_R)
            #mouth_corner_up_R
            if check_shapekey_driver('mouth_corner_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_up_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_corner_R"].UP_LIMIT_R)
            #mouth_corner_down_R
            if check_shapekey_driver('mouth_corner_down_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_down_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].DOWN_LIMIT_R))
            #mouth_corner_back_R
            if check_shapekey_driver('mouth_corner_back_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_back_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].BACK_LIMIT_R))

            #Corrective Shapes

            #Legacy Transforms Based Drivers
            # #mouth_corner_out_up_fix_R
            # if check_shapekey_driver('mouth_corner_out_up_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_up_fix_R'], 'value', 'SCRIPTED', '100 * var_out * var_up if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_up', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].UP_LIMIT_R * 100)
            # #mouth_corner_out_down_fix_R
            # if check_shapekey_driver('mouth_corner_out_down_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_down_fix_R'], 'value', 'SCRIPTED', '100 * var_out * var_down if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_down', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].DOWN_LIMIT_R) * 100)
            # #mouth_corner_out_back_fix_R
            # if check_shapekey_driver('mouth_corner_out_back_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_fix_R'], 'value', 'SCRIPTED', '100 * var_out * var_back if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_back', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].BACK_LIMIT_R) * 100)
            # #mouth_corner_out_back_up_fix_R
            # if check_shapekey_driver('mouth_corner_out_back_up_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_up_fix_R'], 'value', 'SCRIPTED', '1000 * var_out * var_up * var_back if var_out < 0 and var_up > 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_up', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_back', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].UP_LIMIT_R * -(pbones["mouth_corner_R"].BACK_LIMIT_R) * 1000)
            # #mouth_corner_out_back_down_fix_R
            # if check_shapekey_driver('mouth_corner_out_back_down_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_down_fix_R'], 'value', 'SCRIPTED', '1000 * var_out * var_down * var_back if var_out < 0 and var_down < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_down', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_back', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].DOWN_LIMIT_R) * -(pbones["mouth_corner_R"].BACK_LIMIT_R) * 1000)


            #mouth_corner_out_up_fix_R
            if check_shapekey_driver('mouth_corner_out_up_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_up_fix_R'], 'value', 'SCRIPTED', 'var_out * var_up')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_up', keys_name, 'mouth_corner_up_R')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_down_fix_R
            if check_shapekey_driver('mouth_corner_out_down_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_down_fix_R'], 'value', 'SCRIPTED', 'var_out * var_down')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_down', keys_name, 'mouth_corner_down_R')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_back_fix_R
            if check_shapekey_driver('mouth_corner_out_back_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_fix_R'], 'value', 'SCRIPTED', 'var_out * var_back')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_back', keys_name, 'mouth_corner_back_R')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_back_up_fix_R
            if check_shapekey_driver('mouth_corner_out_back_up_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_up_fix_R'], 'value', 'SCRIPTED', 'var_out * var_up * var_back')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_up', keys_name, 'mouth_corner_up_R')
                add_vars_shapekeys(active_driver, 'var_back', keys_name, 'mouth_corner_back_R')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_back_down_fix_R
            if check_shapekey_driver('mouth_corner_out_back_down_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_back_down_fix_R'], 'value', 'SCRIPTED', 'var_out * var_down * var_back')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_down', keys_name, 'mouth_corner_down_R')
                add_vars_shapekeys(active_driver, 'var_back', keys_name, 'mouth_corner_back_R')
                add_mod_generator_location(active_driver, 1)

    #Mouth_Extra_R
    def mouth_extra_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_corner_forw_R')
        add_shapekey(context, 'mouth_corner_out_forw_fix_R')
        add_shapekey(context, 'mouth_corner_out_forw_up_fix_R')
        add_shapekey(context, 'mouth_corner_out_forw_down_fix_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #Mostly used in Quadruped faces


            #mouth_corner_forw_R
            if check_shapekey_driver('mouth_corner_forw_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_forw_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_corner_R"].FORW_LIMIT_R)

            # #Legacy Transforms Based Drivers
            # #mouth_corner_out_forw_fix_R
            # if check_shapekey_driver('mouth_corner_out_forw_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_fix_R'], 'value', 'SCRIPTED', '100 * var_out * var_forw if var_out < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_forw', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].FORW_LIMIT_R * 100)
            # #mouth_corner_out_forw_up_fix_R
            # if check_shapekey_driver('mouth_corner_out_forw_up_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_up_fix_R'], 'value', 'SCRIPTED', '1000 * var_out * var_up * var_forw if var_out < 0 and var_up > 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_up', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_forw', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].UP_LIMIT_R * pbones["mouth_corner_R"].FORW_LIMIT_R * 1000)
            # #mouth_corner_out_forw_down_fix_R
            # if check_shapekey_driver('mouth_corner_out_forw_down_fix_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_down_fix_R'], 'value', 'SCRIPTED', '1000 * var_out * var_down * var_forw if var_out < 0 and var_down < 0 else 0')
            #     add_vars(active_driver, 'var_out', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_down', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
            #     add_vars(active_driver, 'var_forw', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].DOWN_LIMIT_R) * pbones["mouth_corner_R"].FORW_LIMIT_R * 1000)

            #mouth_corner_out_forw_fix_R
            if check_shapekey_driver('mouth_corner_out_forw_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_fix_R'], 'value', 'SCRIPTED', 'var_out * var_forw')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_forw', keys_name, 'mouth_corner_forw_R')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_forw_up_fix_R
            if check_shapekey_driver('mouth_corner_out_forw_up_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_up_fix_R'], 'value', 'SCRIPTED', 'var_out * var_forw * var_up')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_forw', keys_name, 'mouth_corner_forw_R')
                add_vars_shapekeys(active_driver, 'var_up', keys_name, 'mouth_corner_up_R')
                add_mod_generator_location(active_driver, 1)
            #mouth_corner_out_forw_down_fix_R
            if check_shapekey_driver('mouth_corner_out_forw_down_fix_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_out_forw_down_fix_R'], 'value', 'SCRIPTED', 'var_out * var_forw * var_down')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_forw', keys_name, 'mouth_corner_forw_R')
                add_vars_shapekeys(active_driver, 'var_down', keys_name, 'mouth_corner_down_R')
                add_mod_generator_location(active_driver, 1)

    #U_L
    def U_L(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_corner_in_L')
        add_shapekey(context, 'U_up_L')
        add_shapekey(context, 'U_low_L')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #mouth_corner_in_L
            if check_shapekey_driver('mouth_corner_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_in_L'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_corner_L"].IN_LIMIT_L)

            # #Legacy Transforms Based Drivers
            # #U_up_L
            # if check_shapekey_driver('U_up_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['U_up_L'], 'value', 'SCRIPTED', '100 * var_in * var_lip if var_in > 0 else 0')
            #     add_vars(active_driver, 'var_in', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_up_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, pbones["mouth_corner_L"].IN_LIMIT_L * pbones["mouth_ctrl"].U_M_CTRL_LIMIT * 100)
            # #U_low_L
            # if check_shapekey_driver('U_low_L'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['U_low_L'], 'value', 'SCRIPTED', '100 * var_in * var_lip if var_in > 0 else 0')
            #     add_vars(active_driver, 'var_in', 'TRANSFORMS', blenrig_arm, 'mouth_corner_L', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_low_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, pbones["mouth_corner_L"].IN_LIMIT_L * pbones["mouth_ctrl"].U_M_CTRL_LIMIT * 100)

            #U_up_L
            if check_shapekey_driver('U_up_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['U_up_L'], 'value', 'SCRIPTED', 'var_in * var_lip')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_L')
                add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_up_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_ctrl"].U_M_CTRL_LIMIT)
            #U_low_L
            if check_shapekey_driver('U_low_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['U_low_L'], 'value', 'SCRIPTED', 'var_in * var_lip')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_L')
                add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_low_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_ctrl"].U_M_CTRL_LIMIT)

        #Assign Vgroups
        shapekeys['U_up_L'].vertex_group = 'mouth_up_L'
        shapekeys['U_low_L'].vertex_group = 'mouth_low_L'

    #U_R
    def U_R(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_corner_in_R')
        add_shapekey(context, 'U_up_R')
        add_shapekey(context, 'U_low_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #mouth_corner_in_R
            if check_shapekey_driver('mouth_corner_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_corner_in_R'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_corner_R"].IN_LIMIT_R))

            # #Legacy Transforms Based Drivers
            # #U_up_R
            # if check_shapekey_driver('U_up_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['U_up_R'], 'value', 'SCRIPTED', '100 * var_in * var_lip if var_in > 0 else 0')
            #     add_vars(active_driver, 'var_in', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_up_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, pbones["mouth_corner_R"].IN_LIMIT_R * pbones["mouth_ctrl"].U_M_CTRL_LIMIT * 100)
            # #U_low_R
            # if check_shapekey_driver('U_low_R'):
            #     pass
            # else:
            #     active_driver = add_shapekeys_driver(shapekeys['U_low_R'], 'value', 'SCRIPTED', '100 * var_in * var_lip if var_in > 0 else 0')
            #     add_vars(active_driver, 'var_in', 'TRANSFORMS', blenrig_arm, 'mouth_corner_R', "''", 'LOCAL_SPACE', 'LOC_X', 'AUTO')
            #     add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_low_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
            #     add_mod_generator_location(active_driver, pbones["mouth_corner_R"].IN_LIMIT_R * pbones["mouth_ctrl"].U_M_CTRL_LIMIT * 100)

            #U_up_R
            if check_shapekey_driver('U_up_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['U_up_R'], 'value', 'SCRIPTED', 'var_in * var_lip')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_R')
                add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_up_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_ctrl"].U_M_CTRL_LIMIT)
            #U_low_R
            if check_shapekey_driver('U_low_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['U_low_R'], 'value', 'SCRIPTED', 'var_in * var_lip')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_R')
                add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_low_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, pbones["mouth_ctrl"].U_M_CTRL_LIMIT)

        #Assign Vgroups
        shapekeys['U_up_R'].vertex_group = 'mouth_up_R'
        shapekeys['U_low_R'].vertex_group = 'mouth_low_R'

    #U
    def U(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'U_thickness_up')
        add_shapekey(context, 'U_thickness_low')
        add_shapekey(context, 'U_thickness')
        add_shapekey(context, 'U')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #U_thickness_up
            if check_shapekey_driver('U_thickness_up'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['U_thickness_up'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_up_ctrl', "''", 'LOCAL_SPACE', 'SCALE_Z', 'AUTO')
                add_mod_generator_location_offset(active_driver, 2.0, -0.5)
            #U_thickness_low
            if check_shapekey_driver('U_thickness_low'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['U_thickness_low'], 'value', 'MAX', '')
                add_vars(active_driver, 'var', 'TRANSFORMS', blenrig_arm, 'mouth_low_ctrl', "''", 'LOCAL_SPACE', 'SCALE_Z', 'AUTO')
                add_mod_generator_location_offset(active_driver, 2.0, -0.5)
            #Turn U and Thickness Sculpting Shapes Off
            shapekeys['U'].value = 0.0
            shapekeys['U_thickness'].value = 0.0

        #Assign Vgroups
        shapekeys['U_thickness_up'].vertex_group = 'mouth_up'
        shapekeys['U_thickness_low'].vertex_group = 'mouth_low'

    #M
    def M(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'M_up')
        add_shapekey(context, 'M_low')
        add_shapekey(context, 'M')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #M_up
            if check_shapekey_driver('M_up'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['M_up'], 'value', 'MAX', '')
                add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_up_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_ctrl"].U_M_CTRL_LIMIT))
            #M_low
            if check_shapekey_driver('M_low'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['M_low'], 'value', 'MAX', '')
                add_vars(active_driver, 'var_lip', 'TRANSFORMS', blenrig_arm, 'mouth_low_ctrl', "''", 'LOCAL_SPACE', 'LOC_Y', 'AUTO')
                add_mod_generator_location(active_driver, -(pbones["mouth_ctrl"].U_M_CTRL_LIMIT))
            #Turn M Sculpting Shapes Off
            shapekeys['M'].value = 0.0

        #Assign Vgroups
        shapekeys['M_up'].vertex_group = 'mouth_up'
        shapekeys['M_low'].vertex_group = 'mouth_low'

    #Mouth Open
    def mouth_open(self, context):

        from . utils import add_shapekey, add_drivers, add_vars, add_vars_shapekeys, add_mod_generator, check_shapekey_driver, add_shapekeys_driver, add_mod_generator_angle, add_mod_generator_location, add_mod_generator_location_offset

        #Add Shapekeys
        add_shapekey(context, 'mouth_open_down')
        add_shapekey(context, 'mouth_close_up')
        add_shapekey(context, 'mouth_open_corner_out_L')
        add_shapekey(context, 'mouth_open_corner_in_L')
        add_shapekey(context, 'mouth_close_corner_out_L')
        add_shapekey(context, 'mouth_close_corner_in_L')
        add_shapekey(context, 'mouth_open_corner_out_R')
        add_shapekey(context, 'mouth_open_corner_in_R')
        add_shapekey(context, 'mouth_close_corner_out_R')
        add_shapekey(context, 'mouth_close_corner_in_R')

        #Add Drivers
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            keys_name = ob.data.shape_keys.name
            blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
            pbones = blenrig_arm.pose.bones

            #Skip if Driver already present
            #mouth_open_down
            if check_shapekey_driver('mouth_open_down'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_open_down'], 'value', 'SCRIPTED', '-(var_rot / ' + str(round(radians(-(pbones["maxi"].JAW_DOWN_LIMIT)), 4)) + ') + -(var_loc / ' + str(-(round(pbones['maxi'].bone.length * 0.33, 4))) + ')')
                add_vars(active_driver, 'var_rot', 'TRANSFORMS', blenrig_arm, 'maxi', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_vars(active_driver, 'var_loc', 'TRANSFORMS', blenrig_arm, 'maxi', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, -1)
            #mouth_close_up
            if check_shapekey_driver('mouth_close_up'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_close_up'], 'value', 'SCRIPTED', 'var_rot / ' + str(round(radians(pbones["maxi"].JAW_UP_LIMIT), 4)) + ' + var_loc / ' + str(round(pbones['maxi'].bone.length * 0.1, 4)))
                add_vars(active_driver, 'var_rot', 'TRANSFORMS', blenrig_arm, 'maxi', "''", 'LOCAL_SPACE', 'ROT_X', 'SWING_TWIST_X')
                add_vars(active_driver, 'var_loc', 'TRANSFORMS', blenrig_arm, 'maxi', "''", 'LOCAL_SPACE', 'LOC_Z', 'AUTO')
                add_mod_generator_location(active_driver, 1)
            #mouth_open_corner_out_L
            if check_shapekey_driver('mouth_open_corner_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_open_corner_out_L'], 'value', 'SCRIPTED', 'var_out * var_open')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_open', keys_name, 'mouth_open_down')
                add_mod_generator_location(active_driver, 1)
            #mouth_open_corner_in_L
            if check_shapekey_driver('mouth_open_corner_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_open_corner_in_L'], 'value', 'SCRIPTED', 'var_in * var_open')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_L')
                add_vars_shapekeys(active_driver, 'var_open', keys_name, 'mouth_open_down')
                add_mod_generator_location(active_driver, 1)
             #mouth_close_corner_out_L
            if check_shapekey_driver('mouth_close_corner_out_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_close_corner_out_L'], 'value', 'SCRIPTED', 'var_out * var_close')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_L')
                add_vars_shapekeys(active_driver, 'var_close', keys_name, 'mouth_close_up')
                add_mod_generator_location(active_driver, 1)
            #mouth_close_corner_in_L
            if check_shapekey_driver('mouth_close_corner_in_L'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_close_corner_in_L'], 'value', 'SCRIPTED', 'var_in * var_close')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_L')
                add_vars_shapekeys(active_driver, 'var_close', keys_name, 'mouth_close_up')
                add_mod_generator_location(active_driver, 1)

            #mouth_open_corner_out_R
            if check_shapekey_driver('mouth_open_corner_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_open_corner_out_R'], 'value', 'SCRIPTED', 'var_out * var_open')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_open', keys_name, 'mouth_open_down')
                add_mod_generator_location(active_driver, 1)
            #mouth_open_corner_in_R
            if check_shapekey_driver('mouth_open_corner_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_open_corner_in_R'], 'value', 'SCRIPTED', 'var_in * var_open')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_R')
                add_vars_shapekeys(active_driver, 'var_open', keys_name, 'mouth_open_down')
                add_mod_generator_location(active_driver, 1)
             #mouth_close_corner_out_R
            if check_shapekey_driver('mouth_close_corner_out_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_close_corner_out_R'], 'value', 'SCRIPTED', 'var_out * var_close')
                add_vars_shapekeys(active_driver, 'var_out', keys_name, 'mouth_corner_out_R')
                add_vars_shapekeys(active_driver, 'var_close', keys_name, 'mouth_close_up')
                add_mod_generator_location(active_driver, 1)
            #mouth_close_corner_in_R
            if check_shapekey_driver('mouth_close_corner_in_R'):
                pass
            else:
                active_driver = add_shapekeys_driver(shapekeys['mouth_close_corner_in_R'], 'value', 'SCRIPTED', 'var_in * var_close')
                add_vars_shapekeys(active_driver, 'var_in', keys_name, 'mouth_corner_in_R')
                add_vars_shapekeys(active_driver, 'var_close', keys_name, 'mouth_close_up')
                add_mod_generator_location(active_driver, 1)

    Forehead_Frown_Shapekeys: bpy.props.BoolProperty(default=True)
    Eyebrows_Shapekeys: bpy.props.BoolProperty(default=True)
    Eyelids_Shapekeys: bpy.props.BoolProperty(default=True)
    Cheeks_Shapekeys: bpy.props.BoolProperty(default=True)
    Nose_Shapekeys: bpy.props.BoolProperty(default=True)
    Mouth_Corners_Shapekeys: bpy.props.BoolProperty(default=True)
    Mouth_Corners_Quadruped_Extra_Shapekeys: bpy.props.BoolProperty(default=False)
    Mouth_U_Shapekeys: bpy.props.BoolProperty(default=True)
    Mouth_M_Shapekeys: bpy.props.BoolProperty(default=True)
    Mouth_Open_Shapekeys: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        if self.Forehead_Frown_Shapekeys:
            self.frown(context)
        if self.Eyebrows_Shapekeys:
            self.eyebrows_L(context)
            self.eyebrows_R(context)
        if self.Eyelids_Shapekeys:
            self.eyelid_up_L(context)
            self.eyelid_up_R(context)
            self.eyelid_low_L(context)
            self.eyelid_low_R(context)
        if self.Cheeks_Shapekeys:
            self.cheek_L(context)
            self.cheek_R(context)
        if self.Nose_Shapekeys:
            self.nose_L(context)
            self.nose_R(context)
        if self.Mouth_Corners_Shapekeys:
            self.mouth_L(context)
            self.mouth_R(context)
        if self.Mouth_Corners_Quadruped_Extra_Shapekeys:
            self.mouth_extra_L(context)
            self.mouth_extra_R(context)
        if self.Mouth_U_Shapekeys:
            self.U_L(context)
            self.U_R(context)
            self.U(context)
        if self.Mouth_M_Shapekeys:
            self.M(context)
        if self.Mouth_Open_Shapekeys:
            self.mouth_open(context)
        return {"FINISHED"}

class Operator_blenrig_update_shapekey_driver(bpy.types.Operator):

    bl_idname = "blenrig.update_shapekey_driver"
    bl_label = "BlenRig Update Shapkey Driver"
    bl_description = "Update Active Shapkey Driver based on the current Pose and Values of the Rig"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            ob = bpy.context.active_object
            if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
                return True
        else:
            return False

    #Get Bone transformation to update driver
    def update_trasnform(self, context):

        from . utils import bone_local_transforms

        ob = bpy.context.active_object
        active_shapekey = ob.active_shape_key.name

        driver_target = []
        driver_bone = []
        driver_transform_type = []

        #Get Active Shapekey Driver
        for driver in ob.data.shape_keys.animation_data.drivers:
            d_path = driver.data_path
            driver_target[:] = []
            driver_bone[:] = []
            driver_transform_type[:] = []
            if d_path == 'key_blocks["' + active_shapekey + '"].value':
                #For MAX type
                if driver.driver.type == 'MAX':
                    for var in driver.driver.variables:
                        if var.type == 'TRANSFORMS':
                            driver_target.append(var.targets[0].id)
                            driver_bone.append(var.targets[0].bone_target)
                            driver_transform_type.append(var.targets[0].transform_type)
                            # print (driver_target, driver_bone, driver_transform_type)
                    #Update Driver Value with current Bone Transform
                    for mod in driver.modifiers:
                        if mod.type == 'GENERATOR':
                            #X ROTATION
                            if driver_transform_type[0] == 'ROT_X':
                                if round(bone_local_transforms(driver_target[0], driver_bone[0], 'rot_x'), 1) == 0.0:
                                    self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' X Rotation is 0.0. Driver won't be updated")
                                else:
                                    mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'rot_x')
                            #Y ROTATION
                            if driver_transform_type[0] == 'ROT_Y':
                                if round(bone_local_transforms(driver_target[0], driver_bone[0], 'rot_y'), 1) == 0.0:
                                    self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Y Rotation is 0.0. Driver won't be updated")
                                else:
                                    mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'rot_y')
                            #Z ROTATION
                            if driver_transform_type[0] == 'ROT_Z':
                                if round(bone_local_transforms(driver_target[0], driver_bone[0], 'rot_z'), 1) == 0.0:
                                    self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Z Rotation is 0.0. Driver won't be updated")
                                else:
                                    mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'rot_z')
                            #X LOCATION
                            if driver_transform_type[0] == 'LOC_X':
                                if round(bone_local_transforms(driver_target[0], driver_bone[0], 'loc_x'), 3) == 0.000:
                                    self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' X Location is 0.0. Driver won't be updated")
                                else:
                                    mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'loc_x')
                            #Y LOCATION
                            if driver_transform_type[0] == 'LOC_Y':
                                if round(bone_local_transforms(driver_target[0], driver_bone[0], 'loc_y'), 3) == 0.000:
                                    self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Y Location is 0.0. Driver won't be updated")
                                else:
                                    mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'loc_y')
                            #Z LOCATION
                            if driver_transform_type[0] == 'LOC_Z':
                                if round(bone_local_transforms(driver_target[0], driver_bone[0], 'loc_z'), 3) == 0.000:
                                    self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Z Location is 0.0. Driver won't be updated")
                                else:
                                    mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'loc_z')

    #Get Bone transformation to update driver
    def update_eyelids(self, context):

        from . utils import bone_local_transforms

        ob = bpy.context.active_object
        active_shapekey = ob.active_shape_key.name
        blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
        pbones = blenrig_arm.pose.bones

        driver_target = []
        driver_bone = []
        driver_transform_type = []
        eyelid_1 = []
        eyelid_2 = []
        movement_range = []

        if active_shapekey == 'eyelid_up_down_1_L' or active_shapekey == 'eyelid_up_down_2_L':
            eyelid_1[:] = []
            eyelid_2[:] = []
            movement_range[:] = []
            eyelid_1.append('eyelid_up_down_1_L')
            eyelid_2.append('eyelid_up_down_2_L')
            movement_range.append(pbones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L)
        elif active_shapekey == 'eyelid_up_down_1_R' or active_shapekey == 'eyelid_up_down_2_R':
            eyelid_1[:] = []
            eyelid_2[:] = []
            movement_range[:] = []
            eyelid_1.append('eyelid_up_down_1_R')
            eyelid_2.append('eyelid_up_down_2_R')
            movement_range.append(pbones["eyelid_up_ctrl_R"].EYELID_DOWN_LIMIT_R)
        elif active_shapekey == 'eyelid_low_up_1_L' or active_shapekey == 'eyelid_low_up_2_L':
            eyelid_1[:] = []
            eyelid_2[:] = []
            movement_range[:] = []
            eyelid_1.append('eyelid_low_up_1_L')
            eyelid_2.append('eyelid_low_up_2_L')
            movement_range.append(pbones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L)
        elif active_shapekey == 'eyelid_low_up_1_R' or active_shapekey == 'eyelid_low_up_2_R':
            eyelid_1[:] = []
            eyelid_2[:] = []
            movement_range[:] = []
            eyelid_1.append('eyelid_low_up_1_R')
            eyelid_2.append('eyelid_low_up_2_R')
            movement_range.append(pbones["eyelid_low_ctrl_R"].EYELID_UP_LIMIT_R)

        #Get Active Shapekey Driver
        for driver in ob.data.shape_keys.animation_data.drivers:
            d_path = driver.data_path
            driver_target[:] = []
            driver_bone[:] = []
            driver_transform_type[:] = []
            #If Updating eyelid_1 movement shapekey
            if active_shapekey == eyelid_1[0]:
                if d_path == 'key_blocks["' + active_shapekey + '"].value':
                    #For MAX type
                    if driver.driver.type == 'MAX':
                        for var in driver.driver.variables:
                            if var.type == 'TRANSFORMS':
                                driver_target.append(var.targets[0].id)
                                driver_bone.append(var.targets[0].bone_target)
                                driver_transform_type.append(var.targets[0].transform_type)
                                # print (driver_target, driver_bone, driver_transform_type)
                        #Update Driver Value with current Bone Transform
                        for mod in driver.modifiers:
                            if mod.type == 'GENERATOR':
                                #Z LOCATION
                                if driver_transform_type[0] == 'LOC_Z':
                                    if round(bone_local_transforms(driver_target[0], driver_bone[0], 'loc_z'), 4) == 0.0000:
                                        self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Z Location is 0.0. Driver won't be updated")
                                    else:
                                        mod.coefficients[1] = 1 / bone_local_transforms(driver_target[0], driver_bone[0], 'loc_z')
                                        #Update eyelid_2
                                        for driver2 in ob.data.shape_keys.animation_data.drivers:
                                            if driver2.data_path == 'key_blocks["' + eyelid_2[0] + '"].value':
                                                for mod2 in driver2.modifiers:
                                                    if mod2.type == 'GENERATOR':
                                                        #Coefficient_1 equals the movement range between eyelid_up_down_1_L and EYELID_DOWN_LIMIT_L
                                                        mod2.coefficients[1] = 1 / (movement_range[0] - abs(1 / mod.coefficients[1]))
                                                        #Coefficient_0 represents the size of eyelid_up_down_1_L compared to the range of motion of eyelid_up_down_2_L(coefficient_1)
                                                        mod2.coefficients[0] = -(mod2.coefficients[1] / abs(mod.coefficients[1]))
                                                        self.report({'WARNING'}, "'" + str(eyelid_2[0]) + "' shapekey driver has also been updated")
                                                        if 'eyelid_up' in eyelid_2[0]:
                                                            mod2.coefficients[1] = -(mod2.coefficients[1])
            #If Updating eyelid_2 movement shapekey
            if active_shapekey == eyelid_2[0]:
                if driver.data_path == 'key_blocks["' + eyelid_1[0] + '"].value':
                    #Get eyelid_1 coefficient[1]
                    for mod in driver.modifiers:
                        if mod.type == 'GENERATOR':
                            eyelid_1_co_1 = mod.coefficients[1]
                            #Update eyelid_2
                            for driver2 in ob.data.shape_keys.animation_data.drivers:
                                if driver2.data_path == 'key_blocks["' + eyelid_2[0] + '"].value':
                                    for mod2 in driver2.modifiers:
                                        if mod2.type == 'GENERATOR':
                                            #Coefficient_1 equals the movement range between eyelid_up_down_1_L and EYELID_DOWN_LIMIT_L
                                            mod2.coefficients[1] = 1 / (movement_range[0] - abs(1 / eyelid_1_co_1))
                                            #Coefficient_0 represents the size of eyelid_up_down_1_L compared to the range of motion of eyelid_up_down_2_L(coefficient_1)
                                            mod2.coefficients[0] = -(mod2.coefficients[1] / abs(eyelid_1_co_1))
                                            if 'eyelid_up' in eyelid_2[0]:
                                                mod2.coefficients[1] = -(mod2.coefficients[1])

    #Get Bone transformation to update driver
    def update_mouth_open(self, context):

        from . utils import bone_local_transforms

        ob = bpy.context.active_object
        active_shapekey = ob.active_shape_key.name
        blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
        pbones = blenrig_arm.pose.bones

        driver_target = []
        driver_bone = []
        driver_transform_type = []

        #Get Active Shapekey Driver
        for driver in ob.data.shape_keys.animation_data.drivers:
            d_path = driver.data_path
            driver_target[:] = []
            driver_bone[:] = []
            driver_transform_type[:] = []
            if d_path == 'key_blocks["' + active_shapekey + '"].value':
                #For SCRIPTED type
                if driver.driver.type == 'SCRIPTED':
                    for var in driver.driver.variables:
                        if var.type == 'TRANSFORMS':
                            driver_target.append(var.targets[0].id)
                            driver_bone.append(var.targets[0].bone_target)
                            driver_transform_type.append(var.targets[0].transform_type)
                    #Mouth Open
                    if active_shapekey == 'mouth_open_down':
                        if round(bone_local_transforms(driver_target[0], driver_bone[0], 'loc_z'), 3) == 0.000:
                            self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Z Rotation is 0.0. Driver won't be updated")
                        else:
                            driver.driver.expression = '-(var_rot / ' + str(round(radians(-(pbones["maxi"].JAW_DOWN_LIMIT)), 4)) + ') + -(var_loc / ' + str(round(driver_target[0].pose.bones[driver_bone[0]].location[2], 4)) + ')'
                    #Mouth Close
                    if active_shapekey == 'mouth_close_up':
                        if round(bone_local_transforms(driver_target[0], driver_bone[0], 'loc_z'), 3) == 0.000:
                            self.report({'ERROR'}, "'" + str(driver_bone[0]) + "' Z Rotation is 0.0. Driver won't be updated")
                        else:
                            driver.driver.expression = 'var_rot / ' + str(round(radians(pbones["maxi"].JAW_UP_LIMIT), 4)) + ' + var_loc / ' + str(round(driver_target[0].pose.bones[driver_bone[0]].location[2], 4))

    #Facial Shapekeys Exception. These must be updated with the Update Facial Shapekeys Operator
    facial_shapekeys = ['eyelid_up_up_L', 'eyelid_up_up_R', 'eyelid_low_down_L', 'eyelid_low_down_R', 'cheek_up_L', 'cheek_down_L', 'cheek_up_R', 'cheek_down_R', 'nose_frown_L',
    'nostril_expand_L', 'nostril_collapse_L', 'nose_frown_R', 'nostril_expand_R', 'nostril_collapse_R',
    'mouth_corner_out_L', 'mouth_corner_up_L', 'mouth_corner_down_L', 'mouth_corner_back_L', 'mouth_corner_out_up_fix_L', 'mouth_corner_out_down_fix_L',
    'mouth_corner_out_back_fix_L', 'mouth_corner_out_back_up_fix_L', 'mouth_corner_out_back_down_fix_L', 'mouth_corner_out_R', 'mouth_corner_up_R', 'mouth_corner_down_R', 'mouth_corner_back_R',
    'mouth_corner_out_up_fix_R', 'mouth_corner_out_down_fix_R', 'mouth_corner_out_back_fix_R', 'mouth_corner_out_back_up_fix_R', 'mouth_corner_out_back_down_fix_R', 'mouth_corner_in_L', 'U_up_L', 'U_low_L',
    'mouth_corner_in_R', 'U_up_R', 'U_low_R', 'U_thickness_up', 'U_thickness_low', 'U_thickness', 'U', 'M_up', 'M_low', 'M', 'mouth_corner_forw_L', 'mouth_corner_out_forw_fix_L', 'mouth_corner_out_forw_up_fix_L',
    'mouth_corner_out_forw_down_fix_L', 'mouth_corner_forw_R', 'mouth_corner_out_forw_fix_R', 'mouth_corner_out_forw_up_fix_R', 'mouth_corner_out_forw_down_fix_R',
    'mouth_open_corner_out_L', 'mouth_open_corner_in_L', 'mouth_close_corner_out_L', 'mouth_close_corner_in_L', 'mouth_open_corner_out_R', 'mouth_open_corner_in_R', 'mouth_close_corner_out_R', 'mouth_close_corner_in_R']

    #Eyelid Shapekeys are updated separately
    eyelid_shapekeys = ['eyelid_up_down_1_L', 'eyelid_up_down_2_L', 'eyelid_up_down_1_R', 'eyelid_up_down_2_R', 'eyelid_low_up_1_L', 'eyelid_low_up_2_L', 'eyelid_low_up_1_R', 'eyelid_low_up_2_R']

    #Mouth Open Shapekeys are updated separately
    mouth_open_shapekeys = ['mouth_open_down', 'mouth_close_up']

    def execute(self, context):
        ob = bpy.context.active_object
        active_shapekey = ob.active_shape_key.name
        #Facial Shapkeys Exception
        if active_shapekey in self.facial_shapekeys:
            self.report({'ERROR'}, "'" + str(active_shapekey) + "' must be updated with the Update Facial Drivers Button")
        elif active_shapekey in self.eyelid_shapekeys:
            self.update_eyelids(context)
        elif active_shapekey in self.mouth_open_shapekeys:
            self.update_mouth_open(context)
        else:
            self.update_trasnform(context)
        return {"FINISHED"}

class Operator_blenrig_update_face_shapekeys_drivers(bpy.types.Operator):

    bl_idname = "blenrig.update_face_shapekeys_drivers"
    bl_label = "BlenRig Update Face Shapkeys Drivers"
    bl_description = "Update Facial Shapkeys Drivers based on the current Facial Movement Ranges Values"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            ob = bpy.context.active_object
            if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
                return True
        else:
            return False

    #Get Bone transformation to update driver
    def update_curve(self, context, shapekey, expression):

        ob = bpy.context.active_object
        active_shapekey = ob.active_shape_key.name

        driver_target = []
        driver_bone = []
        driver_transform_type = []

        #Update Driver with Current values of Facial Movement Ranges
        for driver in ob.data.shape_keys.animation_data.drivers:
            d_path = driver.data_path
            driver_target[:] = []
            driver_bone[:] = []
            driver_transform_type[:] = []
            if d_path == 'key_blocks["' + shapekey + '"].value':
                for mod in driver.modifiers:
                    if mod.type == 'GENERATOR':
                        mod.coefficients[1] = 1 / expression

    #Eyelid Shapekeys are updated separately
    eyelid_shapekeys = ['eyelid_up_down_1_L', 'eyelid_up_down_2_L', 'eyelid_up_down_1_R', 'eyelid_up_down_2_R', 'eyelid_low_up_1_L', 'eyelid_low_up_2_L', 'eyelid_low_up_1_R', 'eyelid_low_up_2_R']

    def execute(self, context):
        blenrig_arm = bpy.context.scene.blenrig_guide.arm_obj
        pbones = blenrig_arm.pose.bones
        #Eyelids
        self.update_curve(context, 'eyelid_up_up_L', pbones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L)
        self.update_curve(context, 'eyelid_up_up_R', pbones["eyelid_up_ctrl_R"].EYELID_UP_LIMIT_R)
        self.update_curve(context, 'eyelid_low_down_L', -(pbones["eyelid_low_ctrl_L"].EYELID_DOWN_LIMIT_L))
        self.update_curve(context, 'eyelid_low_down_R', -(pbones["eyelid_low_ctrl_R"].EYELID_DOWN_LIMIT_R))
        #Cheeks
        self.update_curve(context, 'cheek_up_L', pbones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L)
        self.update_curve(context, 'cheek_down_L', -(pbones["cheek_ctrl_L"].CHEEK_DOWN_LIMIT_L))
        self.update_curve(context, 'cheek_up_R', pbones["cheek_ctrl_R"].CHEEK_UP_LIMIT_R)
        self.update_curve(context, 'cheek_down_R', -(pbones["cheek_ctrl_R"].CHEEK_DOWN_LIMIT_R))
        #Nose Frown
        self.update_curve(context, 'nose_frown_L', pbones["nose_frown_ctrl_L"].FROWN_LIMIT_L)
        self.update_curve(context, 'nose_frown_R', pbones["nose_frown_ctrl_R"].FROWN_LIMIT_R)
        #Mouth
        self.update_curve(context, 'mouth_corner_out_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L))
        self.update_curve(context, 'mouth_corner_up_L', pbones["mouth_corner_L"].UP_LIMIT_L)
        self.update_curve(context, 'mouth_corner_down_L', -(pbones["mouth_corner_L"].DOWN_LIMIT_L))
        self.update_curve(context, 'mouth_corner_back_L', -(pbones["mouth_corner_L"].BACK_LIMIT_L))
        # self.update_curve(context, 'mouth_corner_out_up_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].UP_LIMIT_L * 100)
        # self.update_curve(context, 'mouth_corner_out_down_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].DOWN_LIMIT_L) * 100)
        # self.update_curve(context, 'mouth_corner_out_back_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].BACK_LIMIT_L) * 100)
        # self.update_curve(context, 'mouth_corner_out_back_up_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].UP_LIMIT_L * -(pbones["mouth_corner_L"].BACK_LIMIT_L) * 1000)
        # self.update_curve(context, 'mouth_corner_out_back_down_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].DOWN_LIMIT_L) * -(pbones["mouth_corner_L"].BACK_LIMIT_L) * 1000)
        self.update_curve(context, 'mouth_corner_forw_L', pbones["mouth_corner_L"].FORW_LIMIT_L)
        # self.update_curve(context, 'mouth_corner_out_forw_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].FORW_LIMIT_L * 100)
        # self.update_curve(context, 'mouth_corner_out_forw_up_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * pbones["mouth_corner_L"].UP_LIMIT_L * pbones["mouth_corner_L"].FORW_LIMIT_L * 1000)
        # self.update_curve(context, 'mouth_corner_out_forw_down_fix_L', -(pbones["mouth_corner_L"].OUT_LIMIT_L) * -(pbones["mouth_corner_L"].DOWN_LIMIT_L) * pbones["mouth_corner_L"].FORW_LIMIT_L * 1000)
        self.update_curve(context, 'mouth_corner_in_L', pbones["mouth_corner_L"].IN_LIMIT_L)
        self.update_curve(context, 'U_up_L', pbones["mouth_ctrl"].U_M_CTRL_LIMIT)
        self.update_curve(context, 'U_low_L', pbones["mouth_ctrl"].U_M_CTRL_LIMIT)
        self.update_curve(context, 'mouth_corner_out_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R))
        self.update_curve(context, 'mouth_corner_up_R', pbones["mouth_corner_R"].UP_LIMIT_R)
        self.update_curve(context, 'mouth_corner_down_R', -(pbones["mouth_corner_R"].DOWN_LIMIT_R))
        self.update_curve(context, 'mouth_corner_back_R', -(pbones["mouth_corner_R"].BACK_LIMIT_R))
        # self.update_curve(context, 'mouth_corner_out_up_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].UP_LIMIT_R * 100)
        # self.update_curve(context, 'mouth_corner_out_down_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].DOWN_LIMIT_R) * 100)
        # self.update_curve(context, 'mouth_corner_out_back_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].BACK_LIMIT_R) * 100)
        # self.update_curve(context, 'mouth_corner_out_back_up_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].UP_LIMIT_R * -(pbones["mouth_corner_R"].BACK_LIMIT_R) * 1000)
        # self.update_curve(context, 'mouth_corner_out_back_down_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].DOWN_LIMIT_R) * -(pbones["mouth_corner_R"].BACK_LIMIT_R) * 1000)
        self.update_curve(context, 'mouth_corner_forw_R', pbones["mouth_corner_R"].FORW_LIMIT_R)
        # self.update_curve(context, 'mouth_corner_out_forw_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].FORW_LIMIT_R * 100)
        # self.update_curve(context, 'mouth_corner_out_forw_up_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * pbones["mouth_corner_R"].UP_LIMIT_R * pbones["mouth_corner_R"].FORW_LIMIT_R * 1000)
        # self.update_curve(context, 'mouth_corner_out_forw_down_fix_R', -(pbones["mouth_corner_R"].OUT_LIMIT_R) * -(pbones["mouth_corner_R"].DOWN_LIMIT_R) * pbones["mouth_corner_R"].FORW_LIMIT_R * 1000)
        self.update_curve(context, 'mouth_corner_in_R', pbones["mouth_corner_R"].IN_LIMIT_R)
        self.update_curve(context, 'U_up_R', pbones["mouth_ctrl"].U_M_CTRL_LIMIT)
        self.update_curve(context, 'U_low_R', pbones["mouth_ctrl"].U_M_CTRL_LIMIT)
        self.update_curve(context, 'M_up', -(pbones["mouth_ctrl"].U_M_CTRL_LIMIT))
        self.update_curve(context, 'M_low', -(pbones["mouth_ctrl"].U_M_CTRL_LIMIT))
        return {"FINISHED"}

class Operator_blenrig_mirror_shapekeys_drivers(bpy.types.Operator):

    bl_idname = "blenrig.mirror_shapekeys_drivers"
    bl_label = "BlenRig Mirror Shapkeys Drivers"
    bl_description = "Mirror the values of all drivers"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            ob = bpy.context.active_object
            if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
                return True
        else:
            return False

    #Mirror Drivers Values
    def mirror_coefficient(self, context, transform, factor, side_1, side_2):
        ob = bpy.context.active_object
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks

            for shape_L in shapekeys:
                if shape_L.name.endswith(side_1):
                    for driver in ob.data.shape_keys.animation_data.drivers:
                        d_path = driver.data_path
                        if d_path == 'key_blocks["' + shape_L.name + '"].value':
                            for var in driver.driver.variables:
                                if var.type == 'TRANSFORMS':
                                    target = var.targets[0]
                                    #Transform
                                    if target.transform_type == transform:
                                        for mod in driver.modifiers:
                                            if mod.type == 'GENERATOR':
                                                co_1_L = mod.coefficients[1]
                                                #Look for _R
                                                for shape_R in shapekeys:
                                                    if shape_R.name.endswith(side_2):
                                                        if shape_R.name[0:-2] == shape_L.name[0:-2]:
                                                            for driver in ob.data.shape_keys.animation_data.drivers:
                                                                d_path = driver.data_path
                                                                if d_path == 'key_blocks["' + shape_R.name + '"].value':
                                                                    for mod_R in driver.modifiers:
                                                                        if mod_R.type == 'GENERATOR':
                                                                            mod_R.coefficients[1] = factor * co_1_L

    #Choose Side Property
    Side : EnumProperty(
        items = (
            ('L to R', 'Left to Right', '', 0),
            ('R to L', 'Right to Left', '', 1),
            ),
            name="Choose Side", default='L to R')

    def execute(self, context):
        if self.Side == 'L to R':
            self.mirror_coefficient(context, 'LOC_Y', 1, '_L', '_R')
            self.mirror_coefficient(context, 'LOC_Z', 1, '_L', '_R')
            self.mirror_coefficient(context, 'LOC_X', -1, '_L', '_R')
            self.mirror_coefficient(context, 'ROT_X', 1, '_L', '_R')
            self.mirror_coefficient(context, 'ROT_Z', -1, '_L', '_R')
            self.mirror_coefficient(context, 'ROT_Y', -1, '_L', '_R')
            self.mirror_coefficient(context, 'SCALE_X', 1, '_L', '_R')
            self.mirror_coefficient(context, 'SCALE_y', 1, '_L', '_R')
            self.mirror_coefficient(context, 'SCALE_Z', 1, '_L', '_R')
        else:
            self.mirror_coefficient(context, 'LOC_Y', 1, '_R', '_L')
            self.mirror_coefficient(context, 'LOC_Z', 1, '_R', '_L')
            self.mirror_coefficient(context, 'LOC_X', -1, '_R', '_L')
            self.mirror_coefficient(context, 'ROT_X', 1, '_R', '_L')
            self.mirror_coefficient(context, 'ROT_Z', -1, '_R', '_L')
            self.mirror_coefficient(context, 'ROT_Y', -1, '_R', '_L')
            self.mirror_coefficient(context, 'SCALE_X', 1, '_R', '_L')
            self.mirror_coefficient(context, 'SCALE_y', 1, '_R', '_L')
            self.mirror_coefficient(context, 'SCALE_Z', 1, '_R', '_L')
        return {"FINISHED"}

class Operator_blenrig_mirror_active_shapekey_driver(bpy.types.Operator):

    bl_idname = "blenrig.mirror_active_shapekey_driver"
    bl_label = "BlenRig Mirror Active Shapkey Driver"
    bl_description = "Mirror the driver of the active shapekey to its opposite side"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            ob = bpy.context.active_object
            if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
                return True
        else:
            return False

    #Mirror Drivers Values
    def mirror_coefficient(self, context, transform, factor):
        ob = bpy.context.active_object
        active_shapekey = ob.active_shape_key.name
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks

            for driver in ob.data.shape_keys.animation_data.drivers:
                d_path = driver.data_path
                if d_path == 'key_blocks["' + active_shapekey + '"].value':
                    for var in driver.driver.variables:
                        if var.type == 'TRANSFORMS':
                            target = var.targets[0]
                            #Transform
                            if target.transform_type == transform:
                                for mod in driver.modifiers:
                                    if mod.type == 'GENERATOR':
                                        co_1_L = mod.coefficients[1]
                                        #Look for _R
                                        for shape_R in shapekeys:
                                            if shape_R.name[0:-2] == active_shapekey[0:-2]:
                                                for driver in ob.data.shape_keys.animation_data.drivers:
                                                    d_path = driver.data_path
                                                    if d_path == 'key_blocks["' + shape_R.name + '"].value':
                                                        for mod_R in driver.modifiers:
                                                            if mod_R.type == 'GENERATOR':
                                                                mod_R.coefficients[1] = factor * co_1_L

    def execute(self, context):
        self.mirror_coefficient(context, 'LOC_Y', 1)
        self.mirror_coefficient(context, 'LOC_Z', 1)
        self.mirror_coefficient(context, 'LOC_X', -1)
        self.mirror_coefficient(context, 'ROT_X', 1)
        self.mirror_coefficient(context, 'ROT_Z', -1)
        self.mirror_coefficient(context, 'ROT_Y', -1)
        self.mirror_coefficient(context, 'SCALE_X', 1)
        self.mirror_coefficient(context, 'SCALE_y', 1)
        self.mirror_coefficient(context, 'SCALE_Z', 1)
        return {"FINISHED"}

#Mirror Lattices Transforms Operator

class Operator_blenrig_mirror_lattice_transforms(bpy.types.Operator):

    bl_idname = "blenrig.mirror_lattice_transforms"
    bl_label = "BlenRig Mirror Lattice Transforms from L to R"
    bl_description = "Mirror Mirror the LATTICE_EYE_L transforms to LATTICE_EYE_R"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["LATTICE"]):
            return True
        else:
            return False

    #Mirror Transforms Values
    def mirror_transforms(self, context):
        from . utils import deselect_all_objects, set_active_object
        try:
            eye_R = bpy.data.objects['LATTICE_EYE_R']
            eye_L = bpy.data.objects['LATTICE_EYE_L']
            eye_R.location[0] =  -(eye_L.location[0])
            eye_R.location[1] =  eye_L.location[1]
            eye_R.location[2] =  eye_L.location[2]
            eye_R.rotation_euler[0] =  eye_L.rotation_euler[0]
            eye_R.rotation_euler[1] =  -(eye_L.rotation_euler[1])
            eye_R.rotation_euler[2] =  -(eye_L.rotation_euler[2])
            eye_R.scale[0] =  eye_L.scale[0]
            eye_R.scale[1] =  eye_L.scale[1]
            eye_R.scale[2] =  eye_L.scale[2]
            deselect_all_objects(context)
            set_active_object(context, eye_R)
            bpy.ops.blenrig.disable_hooks_modif()
        except:
            pass

    def execute(self, context):
        self.mirror_transforms(context)
        return {"FINISHED"}

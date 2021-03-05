import bpy
from mathutils import Vector
from . draw import draw_callback_px
from . utils import inside, get_armature_object
from bpy.props import IntProperty
from . guide import GUIDE_STEPS

class VIEW3D_OT_blenrig_guide(bpy.types.Operator):
    bl_idname = "view3d.blenrig_guide"
    bl_label = "Show Blenrig Guide"
    bl_description = "Run Blenrig interactive guide and show it inside 3d viewport"
    
    instance = None
    step : IntProperty(default=0)

    def modal(self, context, event):
        if context.area != self.area or context.scene != self.scene or self.workspace != context.workspace and get_armature_object(context):
            # On UNDO: queremos ver si el contexto es válido (no ha cambiado realmente) para actualizarlo.
            if context.area and context.area.type == 'VIEW_3D' and context.scene and context.workspace:
                self.area = context.area
                self.scene = context.scene
                self.workspace = context.workspace
                from .guide import GUIDE_STEPS
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
        VIEW3D_OT_blenrig_guide.instance = None
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
        step_data = GUIDE_STEPS[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_step_imagen(self, context, image):
        from .utils import load_image, hide_image
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_image(name)
                if img:
                    hide_image(img)
                    self.image.append(img)
            self.image_index = 0
            self.max_image_index = len(self.image) - 1
            if self.max_image_index != -1:
                self.image[0].gl_load()
            self.timer = context.window_manager.event_timer_add(4.0, window=context.window)
            #print("Create Timer")
        else:
            self.image = load_image(image)
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

        from . guide import GUIDE_STEPS, diccionario
        self.max_step_index = len(GUIDE_STEPS) - 1

        data = context.scene.blenrig_guide
        self.dpi = data.dpi
        self.language = data.language
        self.image_scale = data.image_scale

        self.bones_to_display = []

        # Textos.
        from . text import SetSizeGetDim
        self.button_text_size = 14
        self.step_text = diccionario['Step'][self.language]

        self.next_button_text = diccionario['Next'][self.language]
        next_dim = SetSizeGetDim(0, self.button_text_size + 4, self.dpi, self.next_button_text)

        self.prev_button_text = diccionario['Prev'][self.language]
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
        VIEW3D_OT_blenrig_guide.instance = self
        return {'RUNNING_MODAL'}

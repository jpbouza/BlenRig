import functools
from time import time

import bpy
from mathutils import Vector
from bpy.app import timers
from bpy import ops as OP
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty, BoolProperty

from . text import SetSizeGetDim
from . traductor import texts_dict as dictionary
from . guides import GuideSteps
from . draw import draw_callback_px
from . utils import (
    set_mode, inside,
    inside as test,
    load_guide_image,
    get_armature_object,
    get_viewport_resolution
)
from . guide_ops import ModalReturn
from . dev import DEBUG

counter = 0


# Este Operator ejecuta la acción de la guía y step que le digas.
class BlenrigGuide_SafeCallStepAction(Operator):
    bl_label = "Call Step Action within a safe context"
    bl_idname = 'blenrig_guide.safe_call_step_action'

    guide_id : StringProperty(default='')
    step : IntProperty(default=0)

    end_action : BoolProperty(default=False)

    @classmethod
    def poll(cls, ctx):
        if ctx.active_object is None:
            return False
        return ctx.scene.blenrig_guide.enabled

    def invoke(self, context, event):
        from . guide_gz import BLENRIG_GZ_guide as Gizmo
        gz = Gizmo.get()
        if not gz:
            DEBUG("ERROR! Could not call the guide action, gizmo not found!")
            return ModalReturn.FINISH()
        guide_steps, guide_endstep_action = GuideSteps.get(self.guide_id)
        if self.end_action:
            DEBUG("* Executing '%s' end-step action *" % (self.guide_id))
            guide_endstep_action(context)
        else:
            DEBUG("* Executing '%s' ( Step-%i ) action *" % (self.guide_id, self.step))
            guide_steps[self.step]['accion'](gz, context)
        return ModalReturn.FINISH()

# Este Operator carga las imagenes de la guía y step indicados, en un contexto seguro.
class BlenrigGuide_SafeLoadStepImages(Operator):
    bl_label = "Load Step Images within a safe context"
    bl_idname = 'blenrig_guide.safe_load_step_images'

    guide_id : StringProperty(default='')
    step : IntProperty(default=0)

    @classmethod
    def poll(cls, ctx):
        if ctx.active_object is None:
            return False
        return ctx.scene.blenrig_guide.enabled

    def invoke(self, context, event):
        from . guide_gz import BLENRIG_GZ_guide as Gizmo
        gz = Gizmo.get()
        if not gz:
            DEBUG("ERROR! Could not load step images, gizmo not found!")
            return ModalReturn.FINISH()
        context.area.tag_redraw()
        guide_steps, _ = GuideSteps.get(self.guide_id)
        DEBUG("* Loading '%s' ( Step-%i ) images *" % (self.guide_id, self.step))
        gz.load_step_imagen(context, guide_steps[self.step]['imagen'])
        return ModalReturn.FINISH()


class BlenrigGuideFunctions:
    def get_armature(self, context):
        if self.arm_obj:
            return self.arm_obj
        return get_armature_object(context)

    def draw_bones(self, context, *bone_names):
        self.bones_to_display.clear()
        if context.mode != 'POSE':
            DEBUG("WARN: You are not in pose mode!")
        bones = get_armature_object(context).pose.bones
        for name in bone_names:
            bone = bones.get(name, None)
            if bone:
                self.bones_to_display.append(bone)


class BLENRIG_WG_guide(BlenrigGuideFunctions):
    def __init__(self):
        context = bpy.context
        self.needs_update = True
        self.needs_call_action_safe = False
        DEBUG("GZ::__init__")
        # Some temporal changes + Back-up.
        # self.use_auto_perspective = context.preferences.inputs.use_auto_perspective
        # context.preferences.inputs.use_auto_perspective = False

        self.arm_obj = get_armature_object(context)

        ################

        self.guide_name = ''
        self.guide_steps = []
        self.step = 0
        self.max_step_index = 0

        ################

        self.title = 'Untitled'
        self.text = "Lorem ipsum..."

        self.bones_to_display = []

        self.multi_image = False
        self.timer = None

        self.next_button_enabled = False
        self.prev_button_enabled = False


        # CONTEXTS.
        self.area = context.area
        self.region = context.region
        self.scene = context.scene
        self.workspace = context.workspace

        # DATA (Properties).
        system_scale = context.preferences.system.ui_scale
        self.scale = system_scale * context.preferences.view.ui_scale

        data = context.scene.blenrig_guide
        self.language = data.language
        self.image_scale = data.image_scale

        # TEXTOS.
        self.button_text_size = 12
        self.step_text = dictionary['Step'][self.language]

        self.next_button_text = dictionary['Next'][self.language]
        next_dim = SetSizeGetDim(0, int(self.button_text_size + 4 * self.scale), 72, self.next_button_text)

        self.prev_button_text = dictionary['Prev'][self.language]
        prev_dim = SetSizeGetDim(0, int(self.button_text_size + 4 * self.scale), 72, self.prev_button_text)

        # SIZES.
        max_button_width = max(next_dim[0], prev_dim[0])

        margin = 5 * self.scale
        self.widget_pos = Vector((72, 32)) * self.scale
        self.header_height = 30 * self.scale
        self.text_box_height = 100 * self.scale
        self.image_size = Vector((300, 300)) *self.image_scale * self.scale
        self.widget_size = self.image_size + Vector((0, self.header_height + self.text_box_height))
        self.button_size = Vector((max(int(max_button_width), 20), 20))

        self.x_button_pos = self.widget_pos + self.widget_size - Vector((margin + self.button_size[1], margin + self.button_size[1]))

        self.next_button_pos = self.x_button_pos - Vector((margin + self.button_size[0], 0))
        self.prev_button_pos = self.next_button_pos - Vector((margin + self.button_size[0], 0))

        #context.scene.blenrig_guide.init(context, self)

        DEBUG("GZ::__init__ >> end")

    def update(self, ctx):
        DEBUG("GZ::update")
        self.needs_update = False
        from . guides import GuideSteps
        guide_props = ctx.scene.blenrig_guide
        guide_id, step = guide_props.active_guide_id.split('#')
        self.guide_id = guide_id
        guide_steps, guide_endstep_action = GuideSteps.get(guide_id)
        self.guide_steps = guide_steps
        self.step = int(step)
        self.max_step_index = len(guide_steps) - 1
        self.guide_name = guide_id.lower()
        self.end_of_step_action = guide_endstep_action

        def load():
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for reg in area.regions:
                        if reg.type == 'WINDOW':
                            reg.tag_redraw()
            if not self.load_step(None, self.step):
                DEBUG("Guide could not be loaded [update]")
                guide_props.disable()
            return
        BLENRIG_WG_guide.time_fun(load, time=0.01)

        DEBUG("GZ::update >> end")

    def get_trans(self):
        return self.widget_pos, self.widget_size

    @staticmethod
    def get_cursor(evt):
        return Vector((evt.mouse_region_x, evt.mouse_region_y))

    @staticmethod
    def time_fun(fun, time=0.1, *args):
        timers.register(functools.partial(fun, *args), first_interval=time)

    def start_image_timer(self):
        DEBUG("GZ::start_image_timer")
        def image_timer():
            global counter
            counter += 1
            if counter >= 100:
                counter = 0
                self.timer = None
                return None
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
            bpy.context.scene.blenrig_guide.load_next_image()
            return 2.0

        if self.timer:
            return
        self.timer = True
        timers.register(image_timer, first_interval=2.0)

    def stop_image_timer(self):
        DEBUG("GZ::stop_image_timer")
        global counter
        counter = 100


    ''' LOAD-STEP FUNCTIONS. '''
    def load_step_imagen(self, context, step_image):
        DEBUG("GZ::load_step_imagen")
        guide_props = context.scene.blenrig_guide
        # Borramos las imagenes del contenedor de imagenes de la guía...
        guide_props.clear_images()
        # Vemos si tenemos multiples imagenes comprobando si es un tuple o no "(imagen1, imagen2, imagen3,...)"
        self.multi_image = isinstance(step_image, tuple)
        if self.multi_image:
            for name in step_image:
                guide_props.add_image(load_guide_image(self.guide_name, name, True))
            #self.timer = context.window_manager.event_timer_add(2.0, window=context.window)
            self.start_image_timer()
        else:
            guide_props.add_image(load_guide_image(self.guide_name, step_image, True))
        DEBUG("GZ::load_step_imagen >> end")

    def load_step(self, context, step: int) -> bool:
        DEBUG("GZ::load_step")
        if not self.guide_steps:
            DEBUG("\t>> error")
            return False
        if step < 0 or step > self.max_step_index:
            DEBUG("\t>> cancel")
            return False
        self.bones_to_display.clear() # Force to clear bones to display.
        self.step = step
        if self.step == self.max_step_index:
            self.button_text = 'Close'
        self.next_button_enabled = step != self.max_step_index
        self.prev_button_enabled = step != 0
        if self.timer:
            self.stop_image_timer()
        #    context.window_manager.event_timer_remove(self.timer)
        step_data = self.guide_steps[self.step]
        self.title = str(self.step + 1) + '- ' + (step_data['titulo'][self.language]).upper()
        self.text = step_data['texto'][self.language]
        if not context or not hasattr(context, 'scene') or not hasattr(context, 'space_data') or context.scene==None or context.space_data==None:
            #def call_action_safe_context():
            #    step_data['accion'](self, bpy.context)
            #BLENRIG_WG_guide.time_fun(call_action_safe_context, time=0.01)

            for window in bpy.context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'VIEW_3D':
                        override_context = {'window': window, 'screen': screen, 'area': area}
                        break
            execution_context = 'INVOKE_DEFAULT'
            undo = False
            args = (override_context, execution_context, undo)
            kwargs = {
                'guide_id' : self.guide_id,
                'step' : self.step
            }
            bpy.ops.blenrig_guide.safe_load_step_images(*args, **kwargs)
            bpy.ops.blenrig_guide.safe_call_step_action(*args, **kwargs)
        else:
            self.load_step_imagen(context, step_data['imagen'])
            step_data['accion'](self, context)
        DEBUG("GZ::load_step >> end")
        return True

    def load_next_step(self, context) -> bool:
        return self.load_step(context, self.step+1)

    def load_prev_step(self, context) -> bool:
        return self.load_step(context, self.step-1)

    def test_select(self, ctx, m):
        if self.needs_update:
            self.update(ctx)
        return 1 if test(m,*self.get_trans()) else -1

    def invoke(self, ctx, evt):
        DEBUG("EVENT! %s %s" % (evt.type, evt.value))
        # Para cazar eventos del timer para el cambio de imagen.
        #if evt.type == 'TIMER':
        #    if self.multi_image:
        #        ctx.scene.blenrig_guide.load_next_image()
        #    return ModalReturn.RUN()

        if evt.type != 'LEFTMOUSE':
            return ModalReturn.PASS()
        if evt.value != 'PRESS':
            return ModalReturn.PASS()

        mpos = self.__class__.get_cursor(evt)

        if inside(mpos, self.x_button_pos , [self.button_size.y]*2):
            DEBUG("CLOSE GUIDE!")
            self.end_of_step_action(ctx)
            self.finish(ctx)
            return ModalReturn.FINISH()

        if self.next_button_enabled and inside(mpos, self.next_button_pos , self.button_size):
            ctx.region.tag_redraw()
            if not self.load_next_step(ctx):
                self.end_of_step_action(ctx)
                return ModalReturn.FINISH()
            return ModalReturn.FINISH()

        if self.prev_button_enabled and inside(mpos, self.prev_button_pos , self.button_size):
            ctx.region.tag_redraw()
            if not self.load_prev_step(ctx):
                self.end_of_step_action(ctx)
                return ModalReturn.FINISH()
            return ModalReturn.FINISH()

        return ModalReturn.PASS()


    def finish(self, context=bpy.context):
        if self.timer:
            self.stop_image_timer()
        context.scene.blenrig_guide.disable()
        context.area.tag_redraw()


    def draw(self, context):
        draw_callback_px(self, context)

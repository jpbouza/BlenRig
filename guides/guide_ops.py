from enum import Enum

import bpy
from mathutils import Vector
from bpy.props import IntProperty

from . draw import draw_callback_px
from . utils import set_mode, inside, get_armature_object, load_guide_image, hide_image, get_armature_object
from . traductor import texts_dict
from . guides import GuideSteps


#########################
#### Operator Utils. ####


class ModalReturn(Enum):
    FINISH = 'FINISHED'
    CANCEL = 'CANCELLED'
    RUN = 'RUNNING_MODAL'
    PASS = 'PASS_THROUGH'

    def __call__(self) -> set:
        return {self.value}


########################
#### Base Operator. ####


class BlenrigGuide_BaseOperator(bpy.types.Operator):
    bl_description = "Run Blenrig interactive guide and show it inside 3d viewport"

    instance = None
    step : IntProperty(default=0)

    # PROPIEDADES A ADAPTAR EN CADA SUB-OPERATOR.
    ## Condiciones que debe cumplir para poder ejecutar este Operator.
    object_types = {'ARMATURE'} # De qué tipo debe ser el objeto activo.
    modes = {'OBJECT', 'POSE'}  # En qué modo debe de estar.
    guide_name = ''

    ''' Initialization. '''
    @classmethod
    def poll(cls, ctx):
        if ctx.active_object is None:
            return False
        if ctx.area.type != 'VIEW_3D':
            return False
        if cls.object_types and ctx.active_object.type not in cls.object_types:
            return False
        if cls.modes and ctx.mode not in cls.modes:
            return False
        return True

    # Funcion donde se inicializaran cosas especificas para cada guia.
    def init(self, context):
        pass

    def invoke(self, context, event):
        # Esta línea asegura que el rig de blenrig esté localizado y verificado.
        # para que otras partes de la guia, como las diferentes actions, puedan hacer uso de este.
        if not get_armature_object(context):
            return ModalReturn.CANCEL()

        context.scene.blenrig_guide.obj = context.active_object

        self.init(context)

        self.guide_steps, self.end_of_step_action = GuideSteps.get_steps(self)
        self.max_step_index = len(self.guide_steps) - 1

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
            return ModalReturn.CANCEL()

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
        self.__class__.instance = self
        return ModalReturn.RUN()

    ''' LOAD-STEP FUNCTIONS. '''
    def load_step_imagen(self, context, image):
        self.multi_image = isinstance(image, tuple)
        if self.multi_image:
            self.image = []
            for name in image:
                img = load_guide_image(self.guide_name, name)
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
            self.image = load_guide_image(self.guide_name, image)
            if self.image:
                hide_image(self.image)
                self.image.gl_load()

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
        step_data = self.guide_steps[self.step]
        self.title = step_data['titulo'][self.language]
        self.text = step_data['texto'][self.language]
        self.load_step_imagen(context, step_data['imagen'])
        step_data['accion'](self, context)
        return True

    def load_next_step(self, context) -> bool:
        return self.load_step(context, self.step+1)

    def load_prev_step(self, context) -> bool:
        return self.load_step(context, self.step-1)

    ''' MAIN MODAL FUNCTIONS. '''

    # Cuando el Modal inicia la vuelta... para chequear que todo es correcto...
    def check(self, context):
        if context.area != self.area or context.scene != self.scene or self.workspace != context.workspace:
            # On UNDO: queremos ver si el contexto es válido (no ha cambiado realmente) para actualizarlo.
            if context.area and context.area.type == 'VIEW_3D' and context.scene and context.workspace and get_armature_object(context):
                self.area = context.area
                self.scene = context.scene
                self.workspace = context.workspace
                self.load_step(context,self.step)
                return ModalReturn.RUN
            self.finish()
            print("[Blenrig Guide] Error: scene, workspace or editor was changed!")
            return ModalReturn.CANCEL
        elif not get_armature_object(context):
            self.area.tag_redraw()
            self.finish(context)
            print("[Blenrig Guide] Error: target armature was removed!")
            return ModalReturn.CANCEL
        self.region.tag_redraw()

    # Cuando el Modal finaliza.
    def finish(self, context=bpy.context):
        self.end_of_step_action(context)
        self.__class__.instance = None
        if hasattr(self, 'timer') and self.timer:
            context.window_manager.event_timer_remove(self.timer)
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        # Recover temporal changes.
        context.preferences.inputs.use_auto_perspective = self.use_auto_perspective

    # El Modal...
    def modal(self, context, event):
        # Condicion de salida.
        if event.type == 'ESC':
            self.finish(context)
            self.area.tag_redraw()
            return ModalReturn.CANCEL()

        # Comprobación de estado del contexto.
        res = self.check(context)
        if res:
            return res()

        # Para cazar eventos del timer para el cambio de imagen.
        if event.type == 'TIMER':
            if self.multi_image:
                if self.image_index == self.max_image_index:
                    self.image_index = 0
                else:
                    self.image_index += 1
                self.image[self.image_index].gl_load()
            return ModalReturn.RUN()

        # IGNORAR: eventos que no sean left-click.
        if event.type != 'LEFTMOUSE':
            return ModalReturn.PASS()
        if event.value not in {'PRESS', 'CLICK'}:
            return ModalReturn.PASS()

        # IGNORAR: clicks fuera del area de la guía:
        mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        if not inside(mouse, self.widget_pos, self.widget_size):
            return ModalReturn.PASS()

        # Para detectar clicks en elementos interactuables (Next/Prev)...
        ## NEXT.
        if self.next_button_enabled and inside(mouse, self.next_button_pos, self.button_size):
            if not self.load_next_step(context):
                self.finish(context)
                self.area.tag_redraw()
                return {'FINISHED'}
        # PREV.
        if self.prev_button_enabled and inside(mouse, self.prev_button_pos, self.button_size):
            if not self.load_prev_step(context):
                self.finish(context)
                self.area.tag_redraw()
                return {'FINISHED'}
        # X.
        if inside(mouse, self.x_button_pos, (self.button_size[1], self.button_size[1])):
            self.finish(context)
            self.area.tag_redraw()
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def draw_bones(self, context, *bone_names):
        self.bones_to_display.clear()
        if context.mode != 'POSE':
            print("WARN: You are not in pose mode!")
        bones = get_armature_object(context).pose.bones

        for name in bone_names:
            bone = bones.get(name, None)
            if bone:
                self.bones_to_display.append(bone)


##########################
#### Guide Operators. ####


''' REPROPORTION. '''
class VIEW3D_OT_blenrig_guide_reproportion(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_reproportion"
    bl_label = "Show Reproportion Guide"

    guide_name = 'reproportion'

    def init(self, context):
        set_mode('POSE')
        # Activar reproportion...
        context.object.data.reproportion = True


''' DATA TRANSFER. '''
class VIEW3D_OT_blenrig_guide_datatransfer(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_datatransfer"
    bl_label = "Show Data Transfer Guide"

    guide_name = 'datatransfer'

    def init(self, context):
        pass

''' MESH DEFORM. '''
class VIEW3D_OT_blenrig_guide_mdef(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_mdef"
    bl_label = "Show Mesh Deform Guide"

    guide_name = 'mdef'

    def init(self, context):
        pass


''' LATTICESS. '''
class VIEW3D_OT_blenrig_guide_lattices(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_lattices"
    bl_label = "Show Mesh Deform Guide"

    guide_name = 'lattices'

    def init(self, context):
        pass


''' ACTIONS. '''
class VIEW3D_OT_blenrig_guide_actions(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_actions"
    bl_label = "Show Actions Guide"

    guide_name = 'actions'

    def init(self, context):
        pass


''' WEIGHTS. '''
class VIEW3D_OT_blenrig_guide_weights(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_weights"
    bl_label = "Show Weight Painting Guide"

    guide_name = 'weights'

    def init(self, context):
        pass


''' SHAPE-KEYS. '''
class VIEW3D_OT_blenrig_guide_shapekeys(BlenrigGuide_BaseOperator):
    bl_idname = "view3d.blenrig_guide_shapekeys"
    bl_label = "Show Shapekeys Guide"

    guide_name = 'shapekeys'

    def init(self, context):
        pass
import re
from bpy.types import GizmoGroup as GZG

from . dev import DEBUG

class BLENRIG_GZG_guide(GZG):
    bl_idname = "BLENRIG_GZG_guide"
    bl_label = "Blenrig Guide"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SHOW_MODAL_ALL'}

    #modes = {'POSE', 'OBJECT', 'EDIT'}
    #object_types = {'ARMATURE'}

    _instance = None

    @classmethod
    def poll(cls, ctx):
        if ctx.active_object is None:
            return False
        if ctx.area.type != 'VIEW_3D':
            return False
        #if cls.object_types and ctx.active_object.type not in cls.object_types:
        #    return False
        #if cls.modes and ctx.mode not in cls.modes:
        #    return False
        #print(ctx.scene.blenrig_guide.enabled)
        return ctx.scene.blenrig_guide.enabled

    def draw_prepare(self, context):
        #DEBUG("GZG::draw_prepare")
        if self.rdim[0] != context.region.width or self.rdim[1] != context.region.height:
            self.rdim = (context.region.width, context.region.height)

    def setup(self, context):
        DEBUG("GZG::setup")
        from . guide_gz import BLENRIG_GZ_guide
        self.rdim = (context.region.width, context.region.height)
        gz = self.gizmos.new(BLENRIG_GZ_guide.bl_idname)
        gz.use_event_handle_all = True
        gz.use_draw_modal = True
        gz.scale_basis = 1
        #gz.init(context)
        self.master = gz

    #def invoke_prepare(self, context, gizmo):
    #    pass

    def refresh(self, context):
        if not self.__class__._instance or self.__class__._instance is self:
            return
        
        # Refresh code...



        # End Refresh code...

        self.__class__._instance = self

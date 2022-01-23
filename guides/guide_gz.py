from bpy.types import Gizmo as GZ
from . dev import DEBUG
from . guide_ops import ModalReturn
from . utils import get_armature_object
from . guide_wg import BLENRIG_WG_guide as WG,Vector
import bpy


class BLENRIG_GZ_guide(WG,GZ):
    bl_idname = "BLENRIG_GZ_guide"
    _instance = None

    @classmethod
    def get(cls):
        return cls._instance

    def setup(self):
        DEBUG("GZ::setup")
        BLENRIG_GZ_guide._instance = self

    def exit(self, context, cancel):
        context.area.header_text_set(None)

    def modal(self, context, event, tweak):
        return ModalReturn.FINISH()

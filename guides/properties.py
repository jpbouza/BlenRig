import bpy
from bpy.types import PropertyGroup, Object
from bpy.props import *
from . guide import languages

class BlenrigGuideData(PropertyGroup):
    language : EnumProperty(
        items=languages,
        name="Language"
    )
    dpi : IntProperty(default=72, min=72, max=300, name="Screen DPI")
    image_scale : FloatProperty(default=1, min=0.5, max=2, name="Image Scale")
    show_steps : BoolProperty(default=False, name="Show Steps")
    arm_obj : PointerProperty(type=Object)
    mdef_weights_transfer_obj : PointerProperty(type=Object)
    mdef_cage_obj : PointerProperty(type=Object)
    guide_current_step : StringProperty('')
from bpy.types import Armature
from bpy.props import BoolProperty, IntProperty
from ..rig_functions import reproportion_toggle
from ..rig_functions import toggle_face_drivers
from ..rig_functions import toggle_flex_drivers
from ..rig_functions import toggle_dynamic_drivers
from ..rig_functions import toggle_body_drivers


def reprop_update(self, context):
    reproportion_toggle(self, context)


def optimize_face(self, context):
    toggle_face_drivers(context)


def optimize_flex(self, context):
    toggle_flex_drivers(context)


def optimize_dynamic(self, context):
    toggle_dynamic_drivers(context)


def optimize_body(self, context):
    toggle_body_drivers(context)



def armature_props_register():

    # REPROPORTION
    Armature.reproportion = BoolProperty(
        default=0,
        description="Toggle Reproportion Mode",
        update=reprop_update,
        name="reproportion"
    )
    # TOGGLE_FACE_DRIVERS
    Armature.toggle_face_drivers = BoolProperty(
        default=1,
        description="Toggle Face Riggin Drivers",
        update=optimize_face,
        name="toggle_face_drivers"
    )
    # TOGGLE_DYNAMIC_DRIVERS
    Armature.toggle_flex_drivers = BoolProperty(
        default=1,
        description="Toggle Flex Drivers",
        update=optimize_flex,
        name="toggle_flex_drivers"
    )
    # TOGGLE_DYNAMIC_DRIVERS
    Armature.toggle_dynamic_drivers = BoolProperty(
        default=1,
        description="Toggle Dynamic Shaping Drivers",
        update=optimize_dynamic,
        name="toggle_dynamic_drivers"
    )
    # TOGGLE_BODY_DRIVERS
    Armature.toggle_body_drivers = BoolProperty(
        default=1,
        description="Toggle Body Rigging Drivers",
        update=optimize_body,
        name="toggle_body_drivers"
    )

    # Armature Layers para la visibilidad custom (blender ahora usa un listado en lugar de las capas viejas, y nosotros tenemos una ui similar a lo q ya teniamos en blenrig)
    Armature.layers_edit_mode = BoolProperty(default=False)
    Armature.max_items_to_show = IntProperty(name="Max Items", description="Max Items to Show", default=32, min=1)
    Armature.num_columns = IntProperty(name="Max columns", description="Max columns to Show", default=3, min=1)
    Armature.layers_edit_mode_toggle = BoolProperty(default=False)



def armature_props_unregister():
    del Armature.reproportion
    del Armature.toggle_face_drivers
    del Armature.toggle_flex_drivers
    del Armature.toggle_dynamic_drivers
    del Armature.toggle_body_drivers
    del Armature.layers_edit_mode
    del Armature.max_items_to_show
    del Armature.num_columns
    del Armature.layers_edit_mode_toggle
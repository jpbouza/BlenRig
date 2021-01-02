import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, EnumProperty
from .. import __package__ as main_package


class BoneShapesPreferences(AddonPreferences):
    bl_idname = main_package

    # widget prefix
    widget_prefix: StringProperty(
        name="Bone Shapes prefix",
        description="Choose a prefix for the widget objects",
        default="cs_",
    )

    # collection name
    boneshape_collection_name: StringProperty(
        name="Bone Shapes collection name",
        description="Choose a name for the collection the shapes will appear",
        default="BoneShapes",
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.prop(self, "widget_prefix", text="Shapes Prefix")
        col.prop(self, "boneshape_collection_name", text="Collection name")

import bpy
from .functions import (readShapess, getViewLayerCollection,)
from bpy.types import Menu


class BLENRIG_PT_posemode_panel(bpy.types.Panel):
    bl_label = "Bone Shapes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_idname = 'BLENRIG_PT_posemode_panel'
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'TOOLS':
            return False
        else:
            return True

    items = []
    for key, value in readShapess().items():
        items.append(key)

    itemsSort = []
    for key in sorted(items):
        itemsSort.append((key, key, ""))

# Panel Properties

    bpy.types.Scene.widget_list = bpy.props.EnumProperty(
        name="Shape", items=itemsSort, description="Shape")

    bpy.types.Scene.match_bone_transforms_toggle = bpy.props.BoolProperty(
        default=True, description="Automatic Match Bone Transforms")

    bpy.types.Scene.symmetrize_shape_toggle = bpy.props.BoolProperty(
        default=False, description="Automatic Symmetrize Shape")

    def draw(self, context):
        if bpy.context.mode in {"POSE","EDIT_MESH","OBJECT"}:
            layout = self.layout
            box = layout.row()
            col = box.column()
            box = col.box()
            row = box.row()
            if bpy.context.mode in {"POSE"}:
                if bpy.app.version_string.find("2.92") > -1:
                    if len(bpy.types.Scene.widget_list[1]['items']) < 6:
                        row.prop(context.scene, "widget_list", expand=True)
                    else:
                        row.prop(context.scene, "widget_list",
                            expand=False, text="Shapes Select")
                if bpy.app.version_string.find("2.93") > -1:
                    if len(bpy.types.Scene.widget_list.keywords['items']) < 6:
                        row.prop(context.scene, "widget_list", expand=True)
                    else:
                        row.prop(context.scene, "widget_list",
                            expand=False, text="Shapes Select")                

            if bpy.context.mode in {'POSE', "OBJECT"}:
                row = box.row()
                row.menu("BLENRIG_MT_bw_specials", icon='DOWNARROW_HLT', text="")
                row.operator("blenrig.create_widget", icon="OBJECT_DATAMODE")

            if bpy.context.mode in {"POSE"}:
                row.operator("blenrig.edit_widget", icon="OUTLINER_DATA_MESH")
            
            if bpy.context.mode in {"EDIT_MESH"}:
                layout.separator()
                row.scale_x = 0.9
                row.scale_y = 2.4
                row.operator("blenrig.return_to_armature",
                            icon="LOOP_BACK", text='To bone')

            if bpy.context.mode in {'POSE', "OBJECT", "EDIT_MESH"}:
                row.menu("BLENRIG_MT_bw_specials_edit",
                        icon='DOWNARROW_HLT', text="")

            if bpy.context.mode in {'POSE'}:
                layout.separator()
                layout = self.layout
                layout.operator("blenrig.symmetrize_shape",
                                icon='MOD_MIRROR', text="Symmetrize Shape")

            if bpy.context.mode in {'POSE', "OBJECT"}:
                layout = self.layout
                layout.operator("blenrig.match_bone_transforms",
                                icon='GROUP_BONE', text="Match Bone Transforms")

            if bpy.context.mode in {'POSE'}:
                layout.operator("blenrig.resync_widget_names",
                                icon='FILE_REFRESH', text="Resync Shapes Names")
            
            if bpy.context.mode in {'POSE'}:
                layout = self.layout
                row = layout.row()
                row.menu("BLENRIG_MT_shape_scale",
                                icon='DRIVER_DISTANCE', text="Shapes Size/Scale")

            if bpy.context.mode in {'POSE'}:
                layout.separator()
                layout.operator("blenrig.clear_shapes",
                                icon='X', text="Clear Bone Shapes")

            if bpy.context.mode in {'POSE'}:
                layout.operator("blenrig.delete_unused_shapes",
                                icon='TRASH', text="Delete Unused Shapess")

                # try:
                #     collection = getViewLayerCollection(context)
                # except:
                #     collection = None

                # if collection != None:
                #     if collection.hide_viewport:
                #         icon = "HIDE_ON"
                #         text = "Unhide Collection"
                #     else:
                #         icon = "HIDE_OFF"
                #         text = "Hide Collection"
                #     row = layout.row()
                #     row.separator()
                #     row = layout.row()
                #     row.operator("blenrig.toggle_collection_visibilty",
                #                  icon=icon, text=text)


class BLENRIG_MT_bw_specials(Menu):
    bl_label = "Bone Shapes Specials"

    def draw(self, context):
        layout = self.layout
        layout.operator("blenrig.add_shapes", icon="ADD",
                        text="Add Shapes to library")
        layout.operator("blenrig.remove_shapes", icon="REMOVE",
                        text="Remove Shapes from library")


class BLENRIG_MT_bw_specials_edit(Menu):
    bl_label = "Bone Shapes Specials_edit"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "symmetrize_shape_toggle",
                    text="Automatic Symmetrize Shape")
        layout.prop(context.scene, "match_bone_transforms_toggle",
                    text="Automatic Match Bone Transforms")

class BLENRIG_MT_shape_scale(Menu):
    bl_label = "Bone Shapes Size/Scale"

    def draw(self, context):
        col = self.layout.column()
        col.operator("blenrig.shape_scale", text = "Free")
        col.operator("blenrig.shape_scale", text = "Pelvis")
import bpy
from .functions import (readShapes, getViewLayerCollection,)
from bpy.types import Menu


class BLENRIG_PT_posemode_panel(bpy.types.Panel):
    bl_label = "Bone Shapes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "BLENRIG_PT_blenrig_6_general_SubPanel"
    bl_idname = 'BLENRIG_PT_posemode_panel'
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext2 == 'BONESHAPES':
            return False
        else:
            return True

    items = []
    for key, value in readShapes().items():
        items.append(key)

    itemsSort = []
    for key in sorted(items):
        itemsSort.append((key, key, ""))

# Panel Properties

    bpy.types.Scene.blenrig_widget_list = bpy.props.EnumProperty(
        items=itemsSort, name="Shape", description="Shape")

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
            
            if bpy.context.mode in {'POSE', "OBJECT"}:
                row = row.row(align=True)
                row.prop(context.scene, "blenrig_widget_list",
                        expand=False, text="Shapes Select")                
                row.menu("BLENRIG_MT_bw_specials", icon='DOWNARROW_HLT', text="")            
                

            if bpy.context.mode in {'POSE', "OBJECT"}:
                row = box.row()
                
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
                if hasattr(bpy.context.active_pose_bone,'custom_shape'):
                    if hasattr(bpy.context.active_pose_bone.custom_shape, 'users'):
                        if bpy.context.active_pose_bone.custom_shape.users > 2:
                            layout = self.layout
                            box = layout.row()
                            row = box.row()
                            row.operator("blenrig.make_unique",
                                            icon='CON_ROTLIMIT', text="Make Unique")
                
            if bpy.context.mode in {'POSE'}:
                layout = self.layout
                layout.operator("BLENRIG_OT_shape_scale",
                                icon='DRIVER_DISTANCE', text="Symmetrize Shapes Size/Scale")

            if bpy.context.mode in {'POSE'}:
                layout.separator()
                layout.operator("blenrig.clear_shapes",
                                icon='X', text="Clear Bone Shapes")

            if bpy.context.mode in {'POSE'}:
                layout.operator("blenrig.delete_unused_shapes",
                                icon='TRASH', text="Delete Unused Shapes")
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

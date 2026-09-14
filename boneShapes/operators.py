import bpy

from .functions import (
    findMatchBones,
    fromShapesFindBone,
    findMirrorObject,
    symmetrizeShapes,
    boneMatrix,
    boneScaleObject,
    createShapes,
    editShapes,
    returnToArmature,
    addRemoveShapes,
    readShapes,
    objectDataToDico,
    getCollection,
    getViewLayerCollection,
    deleteUnusedShapes,
    clearBoneShapes,
    resyncShapesNames,
    UnlinkCollection,
    LinkCollection,
    shape_scale,
    MakeUniqueShape
)
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty


class BLENRIG_OT_createShapes(bpy.types.Operator):
    """Creates a widget for selected bone"""
    bl_idname = "blenrig.create_widget"
    bl_label = "Create"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.mode == 'POSE')

    relative_size: BoolProperty(
        name="Relative size",
        default=True,
        description="Shapes size proportionnal to bone size"
    )

    global_size: FloatProperty(
        name="Global Size",
        default=1.0,
        description="Global Size"
    )

    location: FloatVectorProperty(
        name="Location",
        default = (0.0, 0.0, 0.0),
        subtype='NONE',
        unit='NONE',
        description="Location widget"
    )
    rotation: FloatVectorProperty(
        name="Rotation",
        description="Rotate the widget NOT YET WORKING",
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
        unit='ROTATION',
        precision=1,
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "relative_size")
        row = layout.row(align=True)
        row.prop(self, "global_size", expand=False)
        row = layout.row(align=True)
        row.prop(self, "location",expand=True)
        row = layout.row()
        row.prop(self, "rotation", expand=True)

    def execute(self, context):
        wgts = readShapes()
        for bone in bpy.context.selected_pose_bones:
            createShapes(bone, wgts[context.scene.blenrig_widget_list], self.relative_size, self.global_size, [
                        1, 1, 1], self.location, self.rotation, getCollection(context))
        UnlinkCollection(context)
        return {'FINISHED'}


class BLENRIG_OT_editShapes(bpy.types.Operator):
    """Edit the widget for selected bone"""
    bl_idname = "blenrig.edit_widget"
    bl_label = "Edit"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        getCollection(context)
        editShapes(context.active_pose_bone)
        return {'FINISHED'}


class BLENRIG_OT_returnToArmature(bpy.types.Operator):
    """Switch back to the armature"""
    bl_idname = "blenrig.return_to_armature"
    bl_label = "Return to armature"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH'
                and context.object.mode in ['EDIT', 'OBJECT'])

    def execute(self, context):
        if fromShapesFindBone(bpy.context.object):
            returnToArmature(bpy.context.object)
            UnlinkCollection(context)

        else:
            self.report({'INFO'}, 'Object is not a bone widget')

        return {'FINISHED'}


class BLENRIG_OT_matchBoneTransforms(bpy.types.Operator):
    """Match the widget to the bone transforms"""
    bl_idname = "blenrig.match_bone_transforms"
    bl_label = "Match bone transforms"

    def execute(self, context):
        if bpy.context.mode == "POSE":
            for bone in bpy.context.selected_pose_bones:
                if bone.custom_shape_transform and bone.custom_shape:
                    boneMatrix(bone.custom_shape, bone.custom_shape_transform)
                    boneScaleObject(bone.name,bone.custom_shape.name)
                elif bone.custom_shape:
                    boneMatrix(bone.custom_shape, bone)
                    boneScaleObject(bone.name,bone.custom_shape.name)

        else:
            for ob in bpy.context.selected_objects:
                if ob.type == 'MESH':
                    matchBone = fromShapesFindBone(ob)
                    if matchBone:
                        if matchBone.custom_shape_transform:
                            boneMatrix(ob, matchBone.custom_shape_transform)
                            boneScaleObject(matchBone.name,ob.name)
                        else:
                            boneMatrix(ob, matchBone)
                            boneScaleObject(matchBone.name,ob.name)

        return {'FINISHED'}


class BLENRIG_OT_matchSymmetrizeShape(bpy.types.Operator):
    """Symmetrize to the opposite side, if it is named with a .L or .R"""
    bl_idname = "blenrig.symmetrize_shape"
    bl_label = "Symmetrize"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        collection = getCollection(context)
        shapesAndBones = findMatchBones()[0]
        activeObject = findMatchBones()[1]
        UnlinkCollection(context)

        if not activeObject:
            self.report({"INFO"}, "No active bone or object")
            return {'FINISHED'}

        if bpy.data.objects[activeObject.custom_shape.name].users > 2:
            self.report({"INFO"}, "Custom Shape in multiples bones, symmetrize not necesary")


        for bone in shapesAndBones:
            if activeObject.name.endswith("L"):
                if bone.name.endswith("L") and shapesAndBones[bone]:
                    symmetrizeShapes(bone, collection)
            elif activeObject.name.endswith("R"):
                if bone.name.endswith("R") and shapesAndBones[bone]:
                    symmetrizeShapes(bone, collection)
        return {'FINISHED'}


class BLENRIG_OT_addShapes(bpy.types.Operator):
    """Add selected mesh object to Bone Shapes Library"""
    bl_idname = "blenrig.add_shapes"
    bl_label = "Add Shapes"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH' and context.object.mode == 'OBJECT'
                and context.active_object is not None)

    def execute(self, context):
        objects = []
        if bpy.context.mode == "POSE":
            for bone in bpy.context.selected_pose_bones:
                objects.append(bone.custom_shape)
        else:
            for ob in bpy.context.selected_objects:
                if ob.type == 'MESH':
                    objects.append(ob)

        if not objects:
            self.report({'INFO'}, 'Select Meshes or Pose_bones')

        addRemoveShapes(context, "add", bpy.types.Scene.blenrig_widget_list.keywords['items'], objects)

        return {'FINISHED'}


class BLENRIG_OT_removeShapes(bpy.types.Operator):
    """Remove selected widget object from the Bone Shapes Library"""
    bl_idname = "blenrig.remove_shapes"
    bl_label = "Remove Shapes"

    def execute(self, context):
        objects = bpy.context.scene.blenrig_widget_list
        addRemoveShapes(context, "remove", bpy.types.Scene.blenrig_widget_list.keywords['items'], objects)
        return {'FINISHED'}


class BLENRIG_OT_toggleCollectionVisibility(bpy.types.Operator):
    """HideUnhide the bone widget collection"""
    bl_idname = "blenrig.toggle_collection_visibilty"
    bl_label = "Collection Visibilty"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        collection = getViewLayerCollection(context)
        collection.hide_viewport = not collection.hide_viewport
        return {'FINISHED'}


class BLENRIG_OT_deleteUnusedShapes(bpy.types.Operator):
    """Delete unused objects in the WDGT collection"""
    bl_idname = "blenrig.delete_unused_shapes"
    bl_label = "Delete Unused Shapes"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        getCollection(context)
        deleteUnusedShapes()
        UnlinkCollection(context)
        self.report({'INFO'},"Delete Unused Shapes")
        return {'FINISHED'}


class BLENRIG_OT_clearBoneShapes(bpy.types.Operator):
    """Clear shapes from selected pose bones"""
    bl_idname = "blenrig.clear_shapes"
    bl_label = "Clear Shapes"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        clearBoneShapes()
        return {'FINISHED'}


class BLENRIG_OT_resyncShapesNames(bpy.types.Operator):
    """Clear shapes from selected pose bones"""
    bl_idname = "blenrig.resync_widget_names"
    bl_label = "Resync Shapes Names"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        resyncShapesNames()
        self.report({'INFO'},"Resync Shapes")
        return {'FINISHED'}

class BLENRIG_OT_shape_scale(bpy.types.Operator):
    """unificate shapes scale and size from L/R in selected pose bones"""
    bl_idname = "blenrig.shape_scale"
    bl_label = "Symmetrize Shapes Size/Scale"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        shape_scale()
        self.report({'INFO'},"Symmetrize Shapes Size/Scale")
        return {'FINISHED'}
    
class BLENRIG_OT_Make_Unique(bpy.types.Operator):
    """Make Unique Shape for Bone"""
    bl_idname = "blenrig.make_unique"
    bl_label = "Make Unique"

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.pose)

    def execute(self, context):
        MakeUniqueShape()
        self.report({'INFO'},"Make Unique Shape")
        return {'FINISHED'}
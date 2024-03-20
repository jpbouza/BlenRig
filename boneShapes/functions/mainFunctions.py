import bpy
import numpy
from math import pi
from mathutils import Matrix
from .jsonFunctions import objectDataToDico
from ..prefs import main_package
from ...search_functions import * 


def getCollection(context):
    bw_collection_name = context.preferences.addons[main_package].preferences.boneshape_collection_name
    LinkCollection(context)
    bw_collection_search_name = "BlenRig_temp"
    collection = context.scene.collection.children.get(bw_collection_search_name)
    if collection:  # if it already exists
        return collection

    else:  # create a new collection
        collection = bpy.data.collections.new(bw_collection_name)
        context.scene.collection.children.link(collection)
        # hide new collection
        viewlayer_collection = context.view_layer.layer_collection.children[collection.name]
        viewlayer_collection.hide_viewport = True
        bpy.data.collections[bw_collection_name].hide_viewport = False
        return collection

def LinkCollection(context):
    blenrig_temp_boneshapes(True)

def UnlinkCollection(context):
    blenrig_temp_boneshapes(False)


def getViewLayerCollection(context):
    bw_collection_name = search_boneshapes()[0].users_collection[0].name
    collection = context.view_layer.layer_collection.children[bw_collection_name]
    return collection


def boneMatrix(widget, matchBone):
    widget.matrix_local = matchBone.bone.matrix_local
    widget.matrix_world = matchBone.id_data.matrix_world @ matchBone.bone.matrix_local
    widget.data.update()

def boneScaleObject(machtBone,widget):
    try:
        b_scale =  bpy.context.object.pose.bones[machtBone].custom_shape_scale
    except:
        b_scale =  bpy.context.object.pose.bones[machtBone].custom_shape_scale_xyz

    b_size = bpy.context.object.pose.bones[machtBone].use_custom_shape_bone_size
    Length = bpy.context.object.pose.bones[machtBone].length

    if b_size:
        bpy.data.objects[widget].scale.xyz = Length * b_scale
    else:
        bpy.data.objects[widget].scale.xyz = b_scale


def fromShapesFindBone(widget):
    matchBone = None
    for ob in bpy.context.scene.objects:
        if ob.type == "ARMATURE":
            for bone in ob.pose.bones:
                if bone.custom_shape == widget:
                    matchBone = bone
    return matchBone


def createShapes(bone, widget, relative, size, scale, location, rotation, collection):
    C = bpy.context
    D = bpy.data
    bw_widget_prefix = C.preferences.addons[main_package].preferences.widget_prefix

    if bone.custom_shape_transform:
        matrixBone = bone.custom_shape_transform
    else:
        matrixBone = bone

    if bone.custom_shape:
        bone.custom_shape.name = bone.custom_shape.name+"_old"
        bone.custom_shape.data.name = bone.custom_shape.data.name+"_old"
        if C.scene.collection.objects.get(bone.custom_shape.name):
            C.scene.collection.objects.unlink(bone.custom_shape)

    # make the data name include the prefix
    newData = D.meshes.new(bw_widget_prefix + bone.name)

    if relative == True:
        boneLength = 1
    else:
        boneLength = (1/bone.bone.length)

    # add the verts
    newData.from_pydata(numpy.array(widget['vertices'])*[size*scale[0]*boneLength, size*scale[2]
                                                         * boneLength, size*scale[1]*boneLength], widget['edges'], widget['faces'])

    # Create tranform matrices (location vector and rotation)
    widget_matrix = Matrix()
    trans = Matrix.Translation((location[0],location[1],location[2]))
    rot = rotation.to_matrix().to_4x4()

    # Translate then rotate the matrix
    widget_matrix = widget_matrix @ trans
    widget_matrix = widget_matrix @ rot

    # transform the widget with this matrix
    newData.transform(widget_matrix)

    newData.update(calc_edges=True)

    newObject = D.objects.new(bw_widget_prefix + bone.name, newData)

    newObject.data = newData
    newObject.name = bw_widget_prefix + bone.name
    collection.objects.link(newObject)

    newObject.matrix_world = bpy.context.active_object.matrix_world @ matrixBone.bone.matrix_local
    #newObject.scale = [matrixBone.bone.length, matrixBone.bone.length, matrixBone.bone.length]
    layer = bpy.context.view_layer
    layer.update()

    bone.custom_shape = newObject
    bone.bone.show_wire = True


def symmetrizeShapes(bone, collection):
    C = bpy.context
    D = bpy.data
    bw_widget_prefix = C.preferences.addons[main_package].preferences.widget_prefix

    widget = bone.custom_shape

    if findMirrorObject(bone).custom_shape:
        mirrorBone = findMirrorObject(bone)

    else:
        mirrorBone = findMirrorObject(bone)

    mirrorShapes = mirrorBone.custom_shape

    if mirrorShapes:
        if not bpy.data.objects[widget.name].users > 2:
            mirrorShapes.name = mirrorShapes.name+"_old"
            mirrorShapes.data.name = mirrorShapes.data.name+"_old"
        # unlink/delete old widget        
            # if C.scene.objects.get(mirrorShapes.name):
            #     D.objects.remove(mirrorShapes)
            # else:
            #     pass

    newData = widget.data.copy()
    for vert in newData.vertices:
        vert.co = numpy.array(vert.co)*(-1, 1, 1)

    newObject = widget.copy()
    newObject.data = newData
    newData.update()
    newObject.name = bw_widget_prefix + mirrorBone.name
    collection.objects.link(newObject)
    newObject.matrix_local = mirrorBone.bone.matrix_local
    newObject.scale = [mirrorBone.bone.length, mirrorBone.bone.length, mirrorBone.bone.length]

    layer = bpy.context.view_layer
    layer.update()

    mirrorBone.custom_shape = newObject
    mirrorBone.bone.show_wire = True


def deleteUnusedShapes():
    C = bpy.context
    D = bpy.data
    bw_collection_search_name = "BlenRig_temp"
    try:
        widgetList = []

        for ob in D.objects:
            if ob.type == 'ARMATURE':
                for bone in ob.pose.bones:
                    if bone.custom_shape:
                        widgetList.append(bone.custom_shape)
        
        unwantedList = [
            ob for ob in C.scene.collection.children[bw_collection_search_name].all_objects if ob not in widgetList]
        
        # save the current context mode
        mode = C.mode
        # jump into object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # delete unwanted shapes
        bpy.ops.object.delete({"selected_objects": unwantedList})
        # jump back to current mode
        bpy.ops.object.mode_set(mode=mode)
    except:
        print("No Collection found")


def editShapes(active_bone):
    C = bpy.context
    D = bpy.data
    props = C.scene

# check if automatic Match bone transforms is on and do it automatic before edit shape
    if props.match_bone_transforms_toggle:
        bpy.ops.blenrig.match_bone_transforms()
    try:
        widget = active_bone.custom_shape

        armature = active_bone.id_data
        bpy.ops.object.mode_set(mode='OBJECT')
        C.active_object.select_set(False)

        LinkCollection(C)
        collection = "BlenRig_temp"

        if C.space_data.local_view:
            bpy.ops.view3d.localview()

        # select object and make it active
        widget.select_set(True)
        bpy.context.view_layer.objects.active = widget
        
        for ob in bpy.data.collections[collection].objects:
            if ob == widget:
                widget.hide_set(False)
            else:
                D.objects[ob.name].hide_set(True)

        bpy.ops.object.mode_set(mode='EDIT')
    except:
        UnlinkCollection(C)
        print("No Active Bone Selected")



def returnToArmature(widget):
    C = bpy.context
    D = bpy.data
    props = bpy.context.scene

    bone = fromShapesFindBone(widget)
    armature = bone.id_data

    if C.active_object.mode == 'EDIT':
        bpy.context.view_layer.objects.active.select_set(False)
        widget = None
        bpy.ops.object.mode_set(mode='OBJECT')

    UnlinkCollection(C)

    if C.space_data.local_view:
        bpy.ops.view3d.localview()
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')
    armature.data.bones[bone.name].select = True
    armature.data.bones.active = armature.data.bones[bone.name]

# check if automatic Symmetrize Shape is on and do it automatic after edit shape
    if props.symmetrize_shape_toggle:
        bpy.ops.blenrig.symmetrize_shape()

def findMirrorObject(object):
    if object.name.endswith("L"):
        suffix = 'R'
    elif object.name.endswith("R"):
        suffix = 'L'
    elif object.name.endswith("l"):
        suffix = 'r'
    elif object.name.endswith("r"):
        suffix = 'l'
    else:  # what if the widget ends in .001?
        print('Object suffix unknown, using blank')
        suffix = ''

    objectName = list(object.name)
    objectBaseName = objectName[:-1]
    mirroredObjectName = "".join(objectBaseName)+suffix

    if object.id_data.type == 'ARMATURE':
        return object.id_data.pose.bones.get(mirroredObjectName)
    else:
        return bpy.context.scene.objects.get(mirroredObjectName)


def findMatchBones():
    C = bpy.context
    D = bpy.data

    shapesAndBones = {}

    if bpy.context.object.type == 'ARMATURE':
        for bone in C.selected_pose_bones:
            if bone.name.endswith("L") or bone.name.endswith("R"):
                shapesAndBones[bone] = bone.custom_shape
                mirrorBone = findMirrorObject(bone)
                if mirrorBone:
                    shapesAndBones[mirrorBone] = mirrorBone.custom_shape

        armature = bpy.context.object
        activeObject = C.active_pose_bone
    else:
        for shape in C.selected_objects:
            bone = fromShapesFindBone(shape)
            if bone.name.endswith("L") or bone.name.endswith("R"):
                shapesAndBones[fromShapesFindBone(shape)] = shape

                mirrorShape = findMirrorObject(shape)
                if mirrorShape:
                    shapesAndBones[mirrorShape] = mirrorShape

        activeObject = fromShapesFindBone(C.object)
        armature = activeObject.id_data
    return (shapesAndBones, activeObject, armature)


def resyncShapesNames():
    C = bpy.context
    D = bpy.data

    bw_widget_prefix = C.preferences.addons[main_package].preferences.widget_prefix

    shapesAndBones = {}

    if bpy.context.object.type == 'ARMATURE':
        for bone in C.active_object.pose.bones:
            if bone.custom_shape:
                shapesAndBones[bone] = bone.custom_shape

    for k, v in shapesAndBones.items():
        if k.name != (bw_widget_prefix + k.name):
            D.objects[v.name].name = str(bw_widget_prefix + k.name)


def clearBoneShapes():
    C = bpy.context
    D = bpy.data

    if bpy.context.object.type == 'ARMATURE':
        for bone in C.selected_pose_bones:
            if bone.custom_shape:
                bone.custom_shape = None
                bone.custom_shape_transform = None
                
def shape_scale():
    C = bpy.context
    D = bpy.data
    bones = C.selected_pose_bones 

    #Find mirrored bones
    for bone in bones:
        mirrorBone = findMirrorObject(bone)
        try:
            mirrorBone.custom_shape_scale = bone.custom_shape_scale
            mirrorBone.use_custom_shape_bone_size = bone.use_custom_shape_bone_size
        except:
            mirrorBone.custom_shape_scale_xyz = bone.custom_shape_scale_xyz
            mirrorBone.use_custom_shape_bone_size = bone.use_custom_shape_bone_size

def MakeUniqueShape():
    C = bpy.context
    D = bpy.data
    bw_widget_prefix = C.preferences.addons[main_package].preferences.widget_prefix
    bones = C.selected_pose_bones   

    for bone in bones:
        widget = bone.custom_shape
        newData = widget.data.copy()
        newObject = widget.copy()
        newObject.data = newData
        newData.update()
        newObject.name = bw_widget_prefix + bone.name
        newObject = D.objects.get(newObject.name)
        bone.custom_shape = newObject

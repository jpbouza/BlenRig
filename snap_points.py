# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

import bpy
import bmesh
from math import *
import mathutils as mathu
from mathutils import Vector, Matrix
from bpy.types import Operator, PropertyGroup
from bpy.props import *

class BLENRIG_OT_SnapPoints(bpy.types.Operator):
    bl_idname = "blenrig.snap_points"
    bl_label = "Snap Points"
    bl_description = "Snap Points"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        active_obj = context.active_object

        bm = bmesh.from_edit_mesh(active_obj.data)
        bm.verts.ensure_lookup_table()
        sel_verts = [v for v in bm.verts if v.select]

        objects_array = [obj for obj in context.visible_objects if obj != active_obj and obj.type == 'MESH']

        # do snapping
        if sel_verts and objects_array:
            vert_pose_list = {}

            # get nearest positions
            for obj in objects_array:
                bvh = mathu.bvhtree.BVHTree.FromObject(obj, context.evaluated_depsgraph_get())

                for idx, vert in enumerate(sel_verts):
                    v_pos = obj.matrix_world.inverted() @ (active_obj.matrix_world @ vert.co)
                    nearest = bvh.find_nearest(v_pos)

                    if nearest and nearest[0]:
                        v_pos_near = active_obj.matrix_world.inverted() @ (obj.matrix_world @ nearest[0])

                        if vert in vert_pose_list.keys():
                            # if new near position is less
                            if (vert.co - vert_pose_list[vert]).length > (vert.co - v_pos_near).length:
                                vert_pose_list[vert] = v_pos_near
                        else:
                            vert_pose_list[vert] =  v_pos_near

            for vert in sel_verts:
                vert.co = vert_pose_list[vert]

                bm.normal_update()
                bmesh.update_edit_mesh(active_obj.data)

        return {'FINISHED'}

# Shape to bone operator class.
# class POSE_OT_shape_to_bone(Operator):
#     """
#     Align currently assigned custom bone shape on a visible scene layer to
#     active pose bone.
#     """
#     # Main variables.
#     shapeToBoneOptions = bpy.context.window_manager.shapeToBoneSettings
#     bl_idname = 'pose.shape_to_bone'
#     bl_label = 'Align to Bone'
#     bl_description = ("Align currently assigned custom bone shape on a visible "
#                       "scene layer to active pose bone.")
#     bl_options = {'REGISTER', 'UNDO'}
#     @classmethod
#     # Poll.
#     def poll(cls, context):
#         """ poll; context.active_bone and mode == 'POSE'. """
#         return context.active_bone and context.mode == 'POSE'
#     # Draw.
#     def draw(self, context):
#         """ Draw the shapeToBone settings. """
#         shapeToBoneOptions = context.window_manager.shapeToBoneSettings
#         layout = self.layout
#         column = layout.column(align=True)
#         column.prop(shapeToBoneOptions, 'showWire')
#         column.prop(shapeToBoneOptions, 'wireDrawType')
#         column.prop(shapeToBoneOptions, 'nameShape')
#         column.prop(shapeToBoneOptions, 'prefixShapeName', text="Prefix:")
#         column.prop(shapeToBoneOptions, 'prefixShapeDataName')
#         column.prop(shapeToBoneOptions, 'includeArmatureName')
#         column.prop(shapeToBoneOptions, 'separateArmatureName')
#     # Execute.
#     def execute(self, context):
#         """ Execute shapeToBone """
#         shapeToBone(self, context)
#         return {'FINISHED'}

# class shapeToBonePropertyGroup(PropertyGroup):
#     """
#     Property group; space_view3d_armature.py
#     Properties for shapeToBoneOperator class that effect how it will proceed.
#     """
#     # Show wire.
#     showWire = BoolProperty(name='Draw Wire', description="Turn on the bones dr"
#                             "aw wire option when the shape is aligned to the bo"
#                             "ne (Bone is always drawn as a wire-frame regardles"
#                             "s of the view-port draw mode.)", default=True)
#     # Wire draw type.
#     wireDrawType = BoolProperty(name='Wire Draw Type', description="Change the "
#                                 "custom shape object draw type to wire, when th"
#                                 "e shape is aligned to the bone.",
#                                 default=True)
#     # Name shape.
#     nameShape = BoolProperty(name='Auto-Name', description="Automatically name "
#                             "and prefix the custom shape based on the bone it "
#                             "is assigned to.", default=True)
#     # Prefix shape name.
#     prefixShapeName = StringProperty(name='Prefix', description="Use this prefi"
#                                     "x when naming a custom bone shape. (Leave"
#                                     " blank if you do not wish to prefix the n"
#                                     "ame.)", default='')
#     # Prefix shape data name.
#     prefixShapeDataName = BoolProperty(name='Prefix Shape Data Name',
#                                     description="Prefix the custom shape's o"
#                                     "bject data name in addition to prefixin"
#                                     "g the custom shapes name.",
#                                     default=False)
#     # Include armature name.
#     includeArmatureName = BoolProperty(name='Include Armature Name',
#                                     description="Include the armature name w"
#                                     "hen renaming the custom shape.",
#                                     default=False)
#     # Seperate armature name.
#     separateArmatureName = StringProperty(name='Separator', description="Separa"
#                                         "te the name of the armature and the "
#                                         "name of the bone with this character"
#                                         ".", default='-')

# # Shape to bone function.
# def shapeToBone(self, context):
#     """
#     Takes the custom shape assigned to the active pose bone and aligns it to the
#     pose bone's orientation.
#     """
#     # Main variables.
#     shapeToBoneOptions = context.window_manager.shapeToBoneSettings
#     activeArmature = context.active_object
#     activeBone = context.active_bone
#     activePoseBone = activeArmature.pose.bones[activeBone.name]
#     shape = activePoseBone.custom_shape
#     shapeTransform = activePoseBone.custom_shape_transform
#     # Custom shape transform.
#     if shapeTransform:
#         targetMatrix = (activeArmature.matrix_world @ shapeTransform.matrix)
#     else:
#         targetMatrix = (activeArmature.matrix_world @ activeBone.matrix_local)
#     # Location, rotation, scale.
#     shape.location = targetMatrix.to_translation()
#     shape.rotation_mode = 'XYZ'
#     shape.rotation_euler = targetMatrix.to_euler()
#     targetScale = targetMatrix.to_scale()
#     scaleAverage = ((targetScale[0] + targetScale[1] + targetScale[2]) / 3)
#     shape.scale = ((activeBone.length @ scaleAverage),
#                     (activeBone.length @ scaleAverage),
#                     (activeBone.length @ scaleAverage))
#     # Draw options.
#     if shapeToBoneOptions.showWire:
#         activeBone.show_wire = True
#     if shapeToBoneOptions.wireDrawType:
#         shape.draw_type = 'WIRE'
#     # Datablock name.
#     if shapeToBoneOptions.nameShape:
#         targetName = activeBone.name
#         if shapeToBoneOptions.includeArmatureName:
#             targetName = (activeArmature.name +
#                         shapeToBoneOptions.separateArmatureName +
#                         targetName)
#         shape.name = (shapeToBoneOptions.prefixShapeName + targetName)
#         if shapeToBoneOptions.prefixShapeDataName:
#             shape.data.name = (shapeToBoneOptions.prefixShapeName + targetName)
#         else:
#             shape.data.name = targetName


# shapeToBoneProperties = pointerProperty(type=shapeToBonePropertyGroup)
# windowManager.shapeToBoneSettings = shapeToBoneProperties
# bpy.context.window_manager.shapeToBoneSettings.name = 'Shape to Bone'

# class BLENRIG_PT_armaturePanel(bpy.types.Panel):
#     """
#     Armature panel for the add-on; space_view3d_armature.py
#     This panel is located in the 3D view's properties window, while in pose or
#     armature edit mode, decided to go with a unique design here.
#     """
#     # Main variables.
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_label = 'Armature'

#     # Poll.
#     @classmethod
#     def poll(cls, context):
#         """ poll; context.mode in {'POSE', 'EDIT_ARMATURE'}. """
#         return context.mode in {'POSE', 'EDIT_ARMATURE'}
#     # Draw.
#     def draw(self, context):
        
#         # Main variables.
#         # armaturePanelOptions = context.window_manager.armaturePanelSettings
        
#         object = context.object
#         armature = bpy.data.armatures[object.name]
#         bone = context.active_bone
#         poseBone = object.pose.bones[bone.name]
        
#         # Layout
#         layout = self.layout
#         column = layout.column(align=True)
        
#         # Display options.
#         columnRow = column.row()
#         # columnRow.prop(armaturePanelOptions, 'displayContext', text="",
#         #             expand=True)

#         # Shape to bone options.
#         if context.mode == 'POSE':
#             column.separator()
#             subColumn = column.column(align=True)
#             subColumn.active = bool(poseBone.custom_shape)
#             subColumn.scale_y = 1.5
#             subColumn.operator('pose.shape_to_bone', text="Align Custom"
#                                 " Shape")
#             column.separator()
#             # Display
#             column.label(text="Display:")
#             column.separator()
#             column.prop(poseBone, 'custom_shape', text="")
#             if poseBone.custom_shape:
#                 column.prop_search(poseBone, 'custom_shape_transform',
#                                     object.pose, 'bones', text="")
#                 columnSplit = column.split(align=True)
#                 columnSplit.prop(bone, 'hide', text="Hide", toggle=True)
#                 columnSplitRow = columnSplit.row(align=True)
#                 columnSplitRow.active = bool(poseBone.custom_shape)
#                 columnSplitRow.prop(bone, 'show_wire', text="Wireframe",
#                                     toggle=True)
#             else:
#                 column.separator()
#                 column.label(text="Must be in pose mode.")
import bpy
import bmesh
from math import *
from mathutils import bvhtree
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
        if context.object.data.use_mirror_x:
            bpy.ops.mesh.select_mirror(extend=True)

        active_obj = context.active_object
        props = context.window_manager.blenrig_6_props.adjust_distance_cage

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
                append_attribute_to_obj(active_obj, str(vert.index), vert.co)
                vert.co = vert_pose_list[vert]
                bm.normal_update()
                bmesh.update_edit_mesh(active_obj.data)

        bpy.ops.mesh.select_all(action='DESELECT')
        nombre_vertex_group = 'center_loop'
        for center in  bpy.context.active_object.vertex_groups.items():
            if center.__contains__('center_loop'):
                bpy.context.active_object.vertex_groups.active = bpy.context.active_object.vertex_groups.get(nombre_vertex_group)
                bpy.ops.object.vertex_group_select()
                bm = bmesh.from_edit_mesh(active_obj.data)
                bm.normal_update()
                sel_center_verts = [v for v in bm.verts if v.select]        
            
                for vert in sel_center_verts:
                    vert.co[0] = 0
                    vert.select = False
                    bm.normal_update()
                    bmesh.update_edit_mesh(active_obj.data)
        else:
            for vert in sel_verts:
                vert.select= True
            bmesh.update_edit_mesh(active_obj.data)
        return {'FINISHED'}

def append_attribute_to_obj(obj, attribute, value):
    v = str(value.x) + " " + str(value.y) + " " + str(value.z)
    obj[attribute] = str(v)


class BLENRIG_OT_center_loop_cage(bpy.types.Operator):
    bl_idname = "blenrig.center_loop_cage"
    bl_label = "Center loop Cage"
    bl_description = "Center loop Cage"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):    
        active_obj = bpy.context.active_object
        bpy.ops.mesh.select_all(action='DESELECT')
        nombre_vertex_group = 'center_loop'
        bpy.context.active_object.vertex_groups.active = bpy.context.active_object.vertex_groups.get(nombre_vertex_group)
        bpy.ops.object.vertex_group_select()
        bm = bmesh.from_edit_mesh(active_obj.data)
        bm.normal_update()
        sel_center_verts = [v for v in bm.verts if v.select]

        for vert in sel_center_verts:
            vert.co[0] = 0
            vert.select = False
            bm.normal_update()
            bmesh.update_edit_mesh(active_obj.data)
        return {'FINISHED'}
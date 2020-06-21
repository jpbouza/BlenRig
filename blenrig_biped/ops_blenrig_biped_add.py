import bpy
import os
from bpy.types import Operator
from ..side_visibility import side_visibility_props

class Operator_BlenRig5_Add_Biped(Operator):

    bl_idname = "blenrig5.add_biped_rig"
    bl_label = "BlenRig 5 Add Biped Rig"
    bl_description = "Generates BlenRig 5 biped rig"
    bl_options = {'REGISTER', 'UNDO',}


    @classmethod
    def poll(cls, context):                            #method called by blender to check if the operator can be run
        return context.scene != None

    def import_blenrig_biped(self, context):
        CURRENT_DIR = os.path.dirname(__file__)
        filepath =  os.path.join(CURRENT_DIR, "blenrig_biped.blend")
        scene = context.scene

        # Link the top-level collection into the file.
        with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.collections = ["BlenRig_Master_Collection"]

        # hide_collections = ['Mesh_Deform_Cage', 'Lattices', 'Proxy_Model', 'Bone_Shapes']

        # Add the collection(s) to the scene.
        for collection in data_to.collections:
            scene.collection.children.link(collection)
        # for coll in collection.children:
        #     if coll.name in hide_collections:
        #         coll.hide_viewport = True

                #Context Override
                #areas  = [area for area in context.screen.areas if area.type == 'OUTLINER']

                #if areas:
                    #regions = [region for region in areas[0].regions if region.type == 'VIEW_3D']

                    #if regions:
                        #override = {'area': areas[0],
                                    #'region': regions[0]}
                #context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[coll.name]
                #ops.outliner.show_one_level(open=False)

    def execute(self, context):
        if context.mode != 'OBJECT':
            ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        self.import_blenrig_biped(context)

        # en el .blend el biped en modo objeto tiene q estar seleccionado para que lo siguiente no falle:
        context.view_layer.objects.active = context.selected_objects[0]

        # desactivamos las siguientes colecciones:
        # disable_cols = ['Mesh_Deform_Cage', 'GameModel', 'BoneShapes', 'Lattices']
        # scenes = bpy.data.scenes
        # for scn in scenes:
        #     view_layers = scn.view_layers
        #     for vl in view_layers:
        #         for child in reversed(vl.layer_collection.children):
        #             if len(disable_cols) < 1:
        #                 break
        #             for subchild in reversed(child.children):
        #                 if len(disable_cols) < 1:
        #                     break
        #                 else:
        #                     if subchild.name in disable_cols:
        #                         subchild.exclude = True
        #                         disable_cols.remove(subchild.name)

        # Desactivando colecciones de BlenRig de forma mas eficiente:
        # IMPORTANTE Previamente en el .blend les hemos creaado el key 'BlenRig' a cada coleccion con el value de su nombre original.
        mc = context.view_layer.layer_collection.children["BlenRig_Master_Collection"]
        for lc in mc.children:
            if 'BlenRig' in lc.collection and lc.collection['BlenRig'] != 'BlenRig_Biped':
                lc.exclude = True

        return{'FINISHED'}
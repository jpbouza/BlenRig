import bpy
import os
from bpy.types import Operator
from ..visual_assistant import visual_assistant_props
from ..visual_assistant import handle_panel_events



class Operator_BlenRig5_Add_Biped(Operator):

    bl_idname = "blenrig5.add_biped_rig"
    bl_label = "BlenRig 5 Add Biped Rig"
    bl_description = "Generates BlenRig 5 biped rig"
    bl_options = {'REGISTER', 'UNDO',}

    processed = []

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

        # Add the collection(s) to the scene.
        for collection in data_to.collections:
            scene.collection.children.link(collection)
            collection['BlenRig'] = collection.name
            # Deactivating BlenRig collections (Improved):
            vlayer = bpy.context.view_layer
            for child in collection.children:
                child['BlenRig'] = child.name
                if not child.name.startswith('BlenRig_Biped'):
                    vlayer.layer_collection.children[collection.name].children[child.name].exclude = True
                    # print('Processing: ' + collection.name + ' > ' + child.name)


    def execute(self, context):
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        self.import_blenrig_biped(context)

        # in the .blend the biped in object mode has to be selected so that the following does not fail:
        context.view_layer.objects.active = context.selected_objects[0]

        handle_panel_events()

        return{'FINISHED'}
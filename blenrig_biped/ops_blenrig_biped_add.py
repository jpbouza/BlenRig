import bpy
import os
from bpy.types import Operator
from ..visual_assistant import visual_assistant_props

class Operator_BlenRig5_Add_Biped(Operator):

    bl_idname = "blenrig.add_biped_rig"
    bl_label = "BlenRig 6 Add Biped Rig"
    bl_description = "Generates BlenRig 6 biped rig"
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
            data_to.collections = ["BlenRig"]

        # Add the collection(s) to the scene.
        for collection in data_to.collections:
            scene.collection.children.link(collection)
            collection['BlenRig'] = collection.name
            # Deactivating BlenRig collections (Improved):
            vlayer = bpy.context.view_layer
            for child in collection.children:
                child['BlenRig'] = child.name
                if not child.name.startswith('Biped_BlenRig'):
                    vlayer.layer_collection.children[collection.name].children[child.name].exclude = True
                    # print('Processing: ' + collection.name + ' > ' + child.name)

    def viewport_toggle(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'OUTLINER':
                area.spaces[0].show_restrict_column_viewport = True

    def execute(self, context):
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        self.import_blenrig_biped(context)
        self.viewport_toggle(context)
        # in the .blend the biped in object mode has to be selected so that the following does not fail:
        context.view_layer.objects.active = context.selected_objects[0]
        context.scene.blenrig_guide.arm_obj = context.view_layer.objects.active
        for ob in bpy.data.objects:
            if 'BlenRigMdefCage' in ob.name:
                for mod in ob.modifiers:
                    if mod.type == 'ARMATURE':
                        if mod.object == context.view_layer.objects.active:
                            context.scene.blenrig_guide.mdef_cage_obj = ob
            if 'BlenRigMDefHeadWeightsModel' in ob.name:
                for mod in ob.modifiers:
                    if mod.type == 'ARMATURE':
                        if mod.object == context.view_layer.objects.active:
                            context.scene.blenrig_guide.mdef_head_weights_transfer_obj = ob
            if 'BlenRigMDefHandsWeightsModel' in ob.name:
                for mod in ob.modifiers:
                    if mod.type == 'ARMATURE':
                        if mod.object == context.view_layer.objects.active:
                            context.scene.blenrig_guide.mdef_hands_weights_transfer_obj = ob
        return{'FINISHED'}
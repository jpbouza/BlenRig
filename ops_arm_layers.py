import bpy
from bpy.types import Operator


class BLENRIG_OP_armature_layers_rm(Operator):
    bl_idname = "blenrig.arm_layers_rm"
    bl_label = "Remove Armature Layer"
    bl_description = "Remove Armature Layer item in collection list"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return (context.object.type=='ARMATURE' and context.mode=='POSE' or 'EDIT_ARMATURE')

    def execute(self, context):
        
        active_coll = context.object.data.collections.active
        if not active_coll:
            self.report({'ERROR'}, "Not valid active layer/collection")
            return {'CANCELLED'}
        
        if "id_layer_name" in active_coll:
            self.report({'INFO'}, "BlenRig layers should not be removed!")
            return {'CANCELLED'}
        
        # bpy.ops.armature.collection_remove()
        context.object.data.collections.remove(active_coll)
        
        return {'FINISHED'}
    

class BLENRIG_OP_old_armature_layers_converter(Operator):
    bl_idname = "blenrig.old_armature_layers_converter"
    bl_label = "Old Armature Layers Converter"
    bl_description = "Convert Old Armature Layers"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return (context.object.type == 'ARMATURE' and context.mode == 'POSE' or 'EDIT_ARMATURE')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = False

        col = layout.box().column(align=True)
        col.label(text=f"This action will adapt the old blender boxes to", icon='INFO')
        col.label(text=f"the new layer system, it is recommended")
        col.label(text=f"to save a backup file before continuing.")


    def execute(self, context):

        arm = context.object.data
        
        def remove_collections(arm, collection_names):
            prev_mode = context.object.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            for coll_name in collection_names:
                col_layer = arm.collections.get(coll_name)
                if col_layer:
                    arm.collections.remove(col_layer)
            
            if prev_mode:
                bpy.ops.object.mode_set(mode=prev_mode)

        def create_missing_layers(arm):
            for idx in range(len(arm.collections)):
                layer_name = f"Layer {idx}"
                result = arm.collections.find(layer_name)
                if result == -1 and idx != 0:
                    new_layer = arm.collections.new(layer_name)
                    arm.collections.active = new_layer
                    nlidx = arm.collections.active_index
                    arm.collections.move(nlidx, (idx - 1))
                    print(idx, layer_name, result)

        def rename_layers(arm, relations_lyrs_colls):
            for num_layer, layer_name in relations_lyrs_colls.items():
                arm.collections.active_index = num_layer
                current_layer = arm.collections[num_layer]
                current_layer.name = layer_name
                current_layer["id_col_name"] = layer_name
                print(num_layer, layer_name)

        def move_layers(arm, moves):
            for active_name, target_name in moves.items():
                arm.collections.active_name = active_name
                arm.collections.move(arm.collections.active_index, target_name)

        def set_rig_version(arm, new_version):
            arm["rig_version"] = new_version

        list_remove = [
            "GEN", "Fk_MID", "FK_INV_MID", "FK_L", "FK_R", "IK_L", "IK_R",
            "TOON_MID", "TOON_L", "TOON_R", "SCALE_L", "SCALE_R", "PIVOT_POINTS",
            "FACIAL_L", "FACIAL_R", "FACIAL_MID", "FACIAL_MAIN_L", "FACIAL_MAIN_R",
            "FACIAL_MAIN_MID", "CLOTH", "STR", "STR_EYEBROWS", "STR_EYES", "STR_FACE",
            "STR_FACE_MECH", "STR_INNER_MOUTH", "STR_HANDS", "STR_LIPS", "STR_SMILE_LINE",
            "B-BONE_MECH", "STR_LINES", "IK_MID"
        ]

        relations_lyrs_colls = {
            0: "FACIAL 1", 1: "FACIAL 2", 2: "FACIAL 3", 3: "ARM_R FK", 4: "NECK FK",
            5: "ARM_L FK", 6: "ARM_R IK", 7: "TORSO FK", 8: "EXTRAS", 9: "LEG_L IK",
            10: "TOES", 11: "PROPERTIES", 12: "TOES FK", 13: "TOON 1", 14: "TOON 2",
            15: "SCALE", 16: "ARM_L IK", 17: "FINGERS", 18: "TORSO INV", 19: "FINGERS IK",
            20: "LEG_R FK", 21: "PROPS", 22: "LEG_L FK", 23: "LEG_R IK", 24: "OPTIONALS",
            25: "PROTECTED", 26: "MECH", 27: "DEFORMATION", 28: "ACTIONS", 29: "BONE-ROLLS",
            30: "SNAPPING", 31: "REPROPORTION"
        }

        moves = {
            "ARM_L IK": 8, "FINGERS": 9, "TORSO INV": 10, "FINGERS IK": 11,
            "LEG_R FK": 12, "PROPS": 13, "LEG_L FK": 14, "LEG_R IK": 15
        }

        remove_collections(arm, list_remove)
        create_missing_layers(arm)
        rename_layers(arm, relations_lyrs_colls)
        move_layers(arm, moves)
        set_rig_version(arm, "2.2.0")
        
        return {'FINISHED'}


    
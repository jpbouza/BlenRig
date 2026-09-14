import bpy

#################################### BLENRIG UPDATE OPERATOR ####################################################

# Biped

class Operator_Biped_Updater(bpy.types.Operator):
    bl_idname = "blenrig.biped_updater"
    bl_label = "BlenRig 6 Biped Rig Updater"
    bl_description = "Update BlenRig 6 biped rig to the latest version"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        if (context.active_object.type in ["ARMATURE"]):
            for prop in context.active_object.data.items():
                if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                    for propb in context.active_object.data.items():
                        if propb[0] == 'rig_type' and propb[1] == 'Biped':
                            return True

    def execute(self, context):
        arm = context.active_object
        arm_data = arm.data
        pbones = arm.pose.bones

        # Parse rig version (stored as a string, e.g. "5.0.0")
        version = tuple(int(x) for x in arm_data.get("rig_version", "0.0.0").split("."))

        #### Update 1.0.1 ####
        if version == (1, 0, 0):
            # Load Update Functions
            from .blenrig_biped.updates.update_1001 import biped_update_1001

            # Apply
            biped_update_1001(self, context)
            print("Updated to v1.0.1")

            # Refresh version after update
            version = tuple(int(x) for x in arm_data["rig_version"].split("."))

        #### Update 1.0.5 ####
        if version < (1, 0, 5):
            # Load Update Functions
            from .blenrig_biped.updates.update_1005 import (
                biped_update_1005_drivers,
                biped_update_1005_locks,
                biped_update_1005_bone_layers,
                biped_update_1005_bone_groups,
                biped_update_1005_bone_shapes,
                biped_update_1005_new_bones,
                biped_update_1005_lattices,
                biped_update_1005_protected_layers,
                biped_update_1005_functions_script,
                biped_update_1005_layer_scheme,
                biped_update_1005_update_version,
            )

            # Apply
            biped_update_1005_drivers(self, context)
            biped_update_1005_locks(self, context)
            biped_update_1005_bone_layers(self, context)
            biped_update_1005_bone_groups(self, context)
            biped_update_1005_bone_shapes(self, context)
            biped_update_1005_new_bones(self, context)
            biped_update_1005_lattices(self, context)
            biped_update_1005_protected_layers(self, context)
            biped_update_1005_functions_script(self, context)
            biped_update_1005_layer_scheme(self, context)
            biped_update_1005_update_version(self, context)

            print("Updated to v1.0.5")

            # Refresh version after update
            version = tuple(int(x) for x in arm_data["rig_version"].split("."))

        #### Update 5.0.0 ####
        if (4, 0, 0) <= version < (5, 0, 0):
            from .blenrig_biped.updates.update_5000 import biped_update_5_000

            # Apply
            biped_update_5_000()

            print("Updated to v5.0.0")

            # Refresh version after update
            version = tuple(int(x) for x in arm_data["rig_version"].split("."))

        else:
            self.report({'INFO'}, 'Armature already up to date')
  
        return {"FINISHED"}

#Library Overrides

class Operator_Set_Lib_Override_On(bpy.types.Operator):
    bl_idname = "blenrig.set_lib_overrides_on"
    bl_label = "Set Library Overrides On for Legacy Rigs"
    bl_description = "Set Library Overrides On for Legacy Rigs"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            if bpy.app.version > (2,9,0):
                for prop in bpy.context.active_object.data.items():
                    if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):
                        return True

    def execute(self, context):
        list =[]

        for b in bpy.context.active_object.pose.bones:
            for prop in b.items():
                list.append(str("[") + str('"') + str(prop[0]) + str('"') + str("]"))

        for b in bpy.context.active_object.pose.bones:
            for l in list:
                try:
                    b.property_overridable_library_set(l, True)
                except:
                    pass
        self.report({'INFO'}, 'All Properties set to Library Overrides On')
        return {"FINISHED"}



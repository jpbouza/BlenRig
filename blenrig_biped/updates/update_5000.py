import bpy
from bpy.types import PoseBone
from bpy.props import FloatProperty, BoolProperty, IntProperty, FloatVectorProperty
import re
########### Update 5.00 ###########

##### Restore Old Rig RNA PROPS #####
def restore_rna_properties():
    #### FACIAL PROPERTIES ####

    # EYELIDS

    bpy.types.PoseBone.EYELID_DOWN_LIMIT_L = FloatProperty(
        default=0.010,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_DOWN_LIMIT_L"
    )

    bpy.types.PoseBone.EYELID_UP_LIMIT_L = FloatProperty(
        default=0.0035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_UP_LIMIT_L"
    )

    bpy.types.PoseBone.EYELID_OUT_LIMIT_L = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Outwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_OUT_LIMIT_L"
    )

    bpy.types.PoseBone.EYELID_IN_LIMIT_L = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Inwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_IN_LIMIT_L"
    )

    bpy.types.PoseBone.EYE_DOWN_FOLLOW_L = FloatProperty(
        default=0.020,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        #update=eyelids_update,
        name="EYE_DOWN_FOLLOW_L"
    )

    bpy.types.PoseBone.EYE_UP_FOLLOW_L = FloatProperty(
        default=0.008,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        #update=eyelids_update,
        name="EYE_UP_FOLLOW_L"
    )

    bpy.types.PoseBone.EYELID_DOWN_LIMIT_R = FloatProperty(
        default=0.0065,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_DOWN_LIMIT_R"
    )

    bpy.types.PoseBone.EYELID_UP_LIMIT_R = FloatProperty(
        default=0.0145,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_UP_LIMIT_R"
    )

    bpy.types.PoseBone.EYELID_OUT_LIMIT_R = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Outwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_OUT_LIMIT_R"
    )

    bpy.types.PoseBone.EYELID_IN_LIMIT_R = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Inwards Movement Limit",
        #update=eyelids_update,
        name="EYELID_IN_LIMIT_R"
    )

    bpy.types.PoseBone.EYE_DOWN_FOLLOW_R = FloatProperty(
        default=0.020,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        #update=eyelids_update,
        name="EYE_DOWN_FOLLOW_R"
    )

    bpy.types.PoseBone.EYE_UP_FOLLOW_R = FloatProperty(
        default=0.008,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        #update=eyelids_update,
        name="EYE_UP_FOLLOW_R"
    )

    #FROWNS

    bpy.types.PoseBone.FROWN_LIMIT_L = FloatProperty(
        default=0.0350,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        #update=frowns_update,
        name="FROWN_LIMIT_L"
    )

    bpy.types.PoseBone.FROWN_LIMIT_R = FloatProperty(
        default=0.0350,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        #update=frowns_update,
        name="FROWN_LIMIT_R"
    )

    bpy.types.PoseBone.FROWN_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        #update=frowns_update,
        name="FROWN_LIMIT"
    )



##### FIX RNA and ID PROPERTIES DRIVERS #####

# Your property list
props = [
"ik_head","ik_torso","inv_torso","ik_arm_L","ik_arm_R","ik_leg_L","ik_toes_all_L","ik_leg_R","ik_toes_all_R",
"ik_fing_ind_L","ik_fing_mid_L","ik_fing_ring_L","ik_fing_lit_L","ik_fing_thumb_L",
"ik_fing_ind_R","ik_fing_mid_R","ik_fing_ring_R","ik_fing_lit_R","ik_fing_thumb_R",
"ik_fing_all_R","ik_fing_all_L",

"space_head","space_neck","space_arm_L","space_arm_R","space_hand_L","space_hand_R",
"space_fing_ind_L","space_fing_mid_L","space_fing_ring_L","space_fing_lit_L","space_fing_thumb_L",
"space_fing_ind_R","space_fing_mid_R","space_fing_ring_R","space_fing_lit_R","space_fing_thumb_R",
"space_fing_all_R","space_fing_all_L","space_leg_L","space_toes_all_L","space_leg_R","space_toes_all_R",

"space_arm_ik_pole_L","space_arm_ik_pole_R","space_leg_ik_pole_L","space_leg_ik_pole_R",
"toggle_arm_ik_pole_L","toggle_arm_ik_pole_R","toggle_leg_ik_pole_L","toggle_leg_ik_pole_R",

"toon_head","toon_torso","toon_arm_L","toon_arm_R","toon_leg_L","toon_leg_R",

"toon_fing_thumb_L","toon_fing_index_L","toon_fing_middle_L","toon_fing_ring_L","toon_fing_little_L",
"toon_fing_thumb_R","toon_fing_index_R","toon_fing_middle_R","toon_fing_ring_R","toon_fing_little_R",

"pin_elbow_L","pin_elbow_R","pin_knee_L","pin_knee_R",

"look_switch",

"reproportion","toggle_face_drivers","toggle_flex_drivers","toggle_dynamic_drivers","toggle_body_drivers",

"toggle_fingers_L","toggle_fingers_index_L","toggle_fingers_middle_L","toggle_fingers_ring_L",
"toggle_fingers_little_L","toggle_fingers_thumb_L",

"toggle_toes_L","toggle_toes_index_L","toggle_toes_middle_L","toggle_toes_fourth_L",
"toggle_toes_little_L","toggle_toes_big_L",

"toggle_fingers_R","toggle_fingers_index_R","toggle_fingers_middle_R","toggle_fingers_ring_R",
"toggle_fingers_little_R","toggle_fingers_thumb_R",

"toggle_toes_R","toggle_toes_index_R","toggle_toes_middle_R","toggle_toes_fourth_R",
"toggle_toes_little_R","toggle_toes_big_R",

"EYELID_DOWN_LIMIT_L","EYELID_UP_LIMIT_L","EYELID_OUT_LIMIT_L","EYELID_IN_LIMIT_L",
"EYE_DOWN_FOLLOW_L","EYE_UP_FOLLOW_L","AUTO_CHEEK_L",

"EYELID_DOWN_LIMIT_R","EYELID_UP_LIMIT_R","EYELID_OUT_LIMIT_R","EYELID_IN_LIMIT_R",
"EYE_DOWN_FOLLOW_R","EYE_UP_FOLLOW_R","AUTO_CHEEK_R",

"FROWN_LIMIT_L","FROWN_LIMIT_R","FROWN_LIMIT",

"AUTO_SMILE_L","CHEEK_DOWN_LIMIT_L","CHEEK_UP_LIMIT_L",
"AUTO_SMILE_R","CHEEK_DOWN_LIMIT_R","CHEEK_UP_LIMIT_R",

"AUTO_BACK_L","IN_LIMIT_L","OUT_LIMIT_L","UP_LIMIT_L","DOWN_LIMIT_L","FORW_LIMIT_L","BACK_LIMIT_L",
"AUTO_BACK_R","IN_LIMIT_R","OUT_LIMIT_R","UP_LIMIT_R","DOWN_LIMIT_R","FORW_LIMIT_R","BACK_LIMIT_R",

"IN_LIMIT","OUT_LIMIT","SMILE_LIMIT","U_M_CTRL_LIMIT",
"JAW_ROTATION","JAW_DOWN_LIMIT","JAW_UP_LIMIT",

"realistic_joints_fingers_rot_L","realistic_joints_fingers_loc_L",
"realistic_joints_toes_rot_L","realistic_joints_toes_loc_L",
"realistic_joints_elbow_loc_L","realistic_joints_elbow_rot_L",
"realistic_joints_wrist_rot_L","realistic_joints_ankle_rot_L",
"realistic_joints_knee_loc_L","realistic_joints_knee_rot_L",

"realistic_joints_fingers_rot_R","realistic_joints_fingers_loc_R",
"realistic_joints_toes_rot_R","realistic_joints_toes_loc_R",
"realistic_joints_elbow_loc_R","realistic_joints_elbow_rot_R",
"realistic_joints_wrist_rot_R","realistic_joints_ankle_rot_R",
"realistic_joints_knee_loc_R","realistic_joints_knee_rot_R",

"volume_variation_arm_L","volume_variation_fingers_L","volume_variation_leg_L","volume_variation_toes_L",
"volume_variation_arm_R","volume_variation_fingers_R","volume_variation_leg_R","volume_variation_toes_R",
"volume_variation_torso","volume_variation_head","volume_variation_neck",

"volume_preservation_fingers_down_L","volume_preservation_knuckles_down_L",
"volume_preservation_knuckles_up_L","volume_preservation_palm_down_L",

"volume_preservation_fingers_down_R","volume_preservation_knuckles_down_R",
"volume_preservation_knuckles_up_R","volume_preservation_palm_down_R",

"volume_preservation_sole_down_L","volume_preservation_toe_knuckles_up_L",
"volume_preservation_toes_down_L",

"volume_preservation_sole_down_R","volume_preservation_toe_knuckles_up_R",
"volume_preservation_toes_down_R",
]

def fix_driver_paths():

    for obj in bpy.data.objects:

        if not obj.animation_data:
            continue

        if not obj.animation_data.drivers:
            continue

        for fcurve in obj.animation_data.drivers:

            driver = fcurve.driver

            for var in driver.variables:

                for target in var.targets:

                    if not target.data_path:
                        continue

                    # ==================================================
                    # FIRST PASS
                    # pose.bones["bone"].["prop"]
                    # ->
                    # pose.bones["bone"].prop
                    # ==================================================

                    path = target.data_path

                    for prop in props:

                        wrong = f'.["{prop}"]'
                        correct = f'.{prop}'

                        if wrong in path:

                            new_path = path.replace(wrong, correct)

                            print(f"\nFIRST FIX")
                            print(f"OLD: {path}")
                            print(f"NEW: {new_path}")

                            target.data_path = new_path
                            path = new_path

                    # ==================================================
                    # SECOND PASS
                    # pose.bones["bone"].["anything"]
                    # ->
                    # pose.bones["bone"]["anything"]
                    # ==================================================

                    if 'pose.bones[' in path:

                        new_path = re.sub(
                            r'\.\["([^"]+)"\]',
                            r'["\1"]',
                            path
                        )

                        if new_path != path:

                            print(f"\nSECOND FIX")
                            print(f"OLD: {path}")
                            print(f"NEW: {new_path}")

                            target.data_path = new_path

##### ADD MOCAP COMPATIBILITY CONSTRAINTS FOR LIMBS #####

def create_mocap_props():
    # Get the active armature
    obj = bpy.context.object

    # Bone name : Property name
    PROPERTIES = {
        "properties_arm_L": "mocap_arm_L",
        "properties_arm_R": "mocap_arm_R",
        "properties_leg_L": "mocap_leg_L",
        "properties_leg_R": "mocap_leg_R",
    }

    if obj and obj.type == 'ARMATURE' and obj.pose:

        for bone_name, prop_name in PROPERTIES.items():

            pb = obj.pose.bones.get(bone_name)

            if pb is None:
                print(f'Pose bone "{bone_name}" not found.')
                continue

            # Create the property
            pb[prop_name] = 1.0

            # Configure the UI
            ui = pb.id_properties_ui(prop_name)
            ui.update(
                default=1.0,
                min=0.0,
                max=1.0,
                soft_min=0.0,
                soft_max=1.0,
                precision=3,
                step=0.1,
                description="Set MOCAP mode, disable simultaneous IK FK",
            )

            # Make the property library overridable
            pb.property_overridable_library_set(f'["{prop_name}"]', True)

            print(f'Added "{prop_name}" to "{bone_name}".')

    else:
        print("Please select an armature object.")
        

def add_mocap_constraints():

    obj = bpy.context.object

    if not obj or obj.type != 'ARMATURE':
        raise Exception("Please select an armature.")

    # FK bone : IK bone
    bone_map = {
        "arm_fk_L": "arm_ik_L",
        "arm_fk_R": "arm_ik_R",
        "forearm_fk_L": "forearm_ik_L",
        "forearm_fk_R": "forearm_ik_R",
        "thigh_fk_L": "thigh_ik_L",
        "thigh_fk_R": "thigh_ik_R",
        "shin_fk_L": "shin_ik_L",
        "shin_fk_R": "shin_ik_R",
    }

    for fk_bone, ik_bone in bone_map.items():

        pb = obj.pose.bones.get(fk_bone)
        if pb is None:
            print(f'Bone "{fk_bone}" not found.')
            continue

        # Remove any existing constraint with the same name
        old = pb.constraints.get("Copy Transforms_MOCAP")
        if old:
            pb.constraints.remove(old)

        # Create the constraint
        con = pb.constraints.new('COPY_TRANSFORMS')
        con.name = "Copy Transforms_MOCAP"
        con.target = obj
        con.subtarget = ik_bone

        # Move it to the top of the stack
        idx = pb.constraints.find(con.name)
        pb.constraints.move(idx, 0)

        print(f'Added Copy Transforms_MOCAP to "{fk_bone}"')
           

def add_mocap_drivers():

    obj = bpy.context.object

    if not obj or obj.type != 'ARMATURE':
        raise Exception("Please select an armature.")

    # FK Bone : (Properties Bone, IK/FK Property, MOCAP Property)
    driver_map = {
        "arm_fk_L":      ("properties_arm_L", "ik_arm_L", "mocap_arm_L"),
        "forearm_fk_L":  ("properties_arm_L", "ik_arm_L", "mocap_arm_L"),

        "arm_fk_R":      ("properties_arm_R", "ik_arm_R", "mocap_arm_R"),
        "forearm_fk_R":  ("properties_arm_R", "ik_arm_R", "mocap_arm_R"),

        "thigh_fk_L":    ("properties_leg_L", "ik_leg_L", "mocap_leg_L"),
        "shin_fk_L":     ("properties_leg_L", "ik_leg_L", "mocap_leg_L"),

        "thigh_fk_R":    ("properties_leg_R", "ik_leg_R", "mocap_leg_R"),
        "shin_fk_R":     ("properties_leg_R", "ik_leg_R", "mocap_leg_R"),
    }

    for bone_name, (prop_bone, ik_prop, mocap_prop) in driver_map.items():

        pb = obj.pose.bones.get(bone_name)
        if pb is None:
            print(f'Bone "{bone_name}" not found.')
            continue

        con = pb.constraints.get("Copy Transforms_MOCAP")
        if con is None:
            print(f'Constraint "Copy Transforms_MOCAP" not found on "{bone_name}".')
            continue

        # Remove any existing driver
        try:
            con.driver_remove("influence")
        except RuntimeError:
            pass

        # Add new driver
        fcurve = con.driver_add("influence")
        driver = fcurve.driver

        driver.type = 'SCRIPTED'
        driver.expression = "MOCAP-var"

        # Variable: var
        var = driver.variables.new()
        var.name = "var"
        var.type = 'SINGLE_PROP'
        var.targets[0].id = obj
        var.targets[0].data_path = (
            f'pose.bones["{prop_bone}"].{ik_prop}'
        )

        # Variable: MOCAP
        mocap = driver.variables.new()
        mocap.name = "MOCAP"
        mocap.type = 'SINGLE_PROP'
        mocap.targets[0].id = obj
        mocap.targets[0].data_path = (
            f'pose.bones["{prop_bone}"]["{mocap_prop}"]'
        )

        print(f'Added driver to {bone_name}')


##### MIGRATE SPINE, NECK AND TONGUE PROPERTIES #####

def update_spine_neck_tongue_props():
    # ================================================================
    # SETTINGS
    # ================================================================

    # Each entry:
    #
    #     source bone -> (destination bone, source property, new property)
    #
    # Bone names are matched EXACTLY.
    # ================================================================

    MIGRATION_MAP = {

        # ------------------------------------------------------------
        # TORSO
        # ------------------------------------------------------------

        "spine_1_fk": (
            "properties_torso",
            "fk_follow_main",
            "spine_1_follow"
        ),

        "spine_2_fk": (
            "properties_torso",
            "fk_follow_main",
            "spine_2_follow"
        ),

        "spine_3_fk": (
            "properties_torso",
            "fk_follow_main",
            "spine_3_follow"
        ),

        "pelvis_ctrl": (
            "properties_torso",
            "fk_follow_main",
            "pelvis_follow"
        ),

        "spine_2_fk_inv": (
            "properties_torso",
            "fk_follow_main",
            "spine_inv_2_follow"
        ),

        "spine_3_fk_inv": (
            "properties_torso",
            "fk_follow_main",
            "spine_inv_3_follow"
        ),


        # ------------------------------------------------------------
        # HEAD
        # ------------------------------------------------------------

        "neck_1_fk": (
            "properties_head",
            "fk_follow_main",
            "neck_1_follow"
        ),

        "neck_2_fk": (
            "properties_head",
            "fk_follow_main",
            "neck_2_follow"
        ),

        "neck_3_fk": (
            "properties_head",
            "fk_follow_main",
            "neck_3_follow"
        ),


        # ------------------------------------------------------------
        # TONGUE
        # ------------------------------------------------------------

        "tongue_1_ik": (
            "properties_head",
            "follow_chain",
            "tongue_1_follow"
        ),

        "tongue_2_ik": (
            "properties_head",
            "follow_chain",
            "tongue_2_follow"
        ),
    }


    # ================================================================
    # ACTIVE ARMATURE
    # ================================================================

    obj = bpy.context.active_object

    if obj is None or obj.type != 'ARMATURE':
        raise RuntimeError(
            "Please select an armature."
        )


    # ================================================================
    # CHECK DESTINATION BONES
    # ================================================================

    destination_bones = set()

    for source_bone, (
        destination_bone,
        source_property,
        new_property
    ) in MIGRATION_MAP.items():

        destination_bones.add(destination_bone)


    for destination_bone in destination_bones:

        if destination_bone not in obj.pose.bones:

            raise RuntimeError(
                f"Destination bone '{destination_bone}' does not exist."
            )


    # ================================================================
    # MIGRATE ID PROPERTIES
    #
    # Source bone names are matched EXACTLY.
    #
    # Copies:
    # - Current ID property value
    # - UI metadata
    # - Library override state
    #
    # Then deletes the original property.
    # ================================================================

    migrated = []


    for source_bone, (
        destination_bone,
        source_property,
        new_property
    ) in MIGRATION_MAP.items():

        # ------------------------------------------------------------
        # Check source bone
        # ------------------------------------------------------------

        if source_bone not in obj.pose.bones:

            print(
                f"WARNING: Source bone '{source_bone}' does not exist."
            )

            continue


        src = obj.pose.bones[source_bone]
        dst = obj.pose.bones[destination_bone]


        # ------------------------------------------------------------
        # Check source property
        # ------------------------------------------------------------

        if source_property not in src:

            print(
                f"WARNING: '{source_property}' not found on "
                f"'{source_bone}'."
            )

            continue


        # ------------------------------------------------------------
        # Don't overwrite existing destination property
        # ------------------------------------------------------------

        if new_property in dst:

            print(
                f"WARNING: '{new_property}' already exists on "
                f"'{destination_bone}'. Skipping."
            )

            continue


        try:

            # --------------------------------------------------------
            # Get current ID property value
            # --------------------------------------------------------

            value = src[source_property]


            # --------------------------------------------------------
            # Copy ID property UI metadata
            # --------------------------------------------------------

            ui_data = src.id_properties_ui(
                source_property
            ).as_dict()


            # --------------------------------------------------------
            # Copy library override state
            # --------------------------------------------------------

            try:

                overridable = (
                    src.is_property_overridable_library(
                        f'["{source_property}"]'
                    )
                )

            except Exception:

                overridable = False


            # --------------------------------------------------------
            # Create destination ID property
            # --------------------------------------------------------

            dst[new_property] = value


            # --------------------------------------------------------
            # Copy UI metadata
            # --------------------------------------------------------

            try:

                dst.id_properties_ui(
                    new_property
                ).update(
                    **ui_data
                )

            except Exception as e:

                print(
                    f'WARNING: Could not copy UI data for '
                    f'{destination_bone}["{new_property}"]: {e}'
                )


            # --------------------------------------------------------
            # Copy library override state
            # --------------------------------------------------------

            try:

                dst.property_overridable_library_set(
                    f'["{new_property}"]',
                    overridable
                )

            except Exception:

                pass


            # --------------------------------------------------------
            # Delete original ID property
            # --------------------------------------------------------

            del src[source_property]


            # --------------------------------------------------------
            # Record migration
            # --------------------------------------------------------

            migrated.append(
                (
                    source_bone,
                    destination_bone,
                    source_property,
                    new_property,
                    value
                )
            )


        except Exception as e:

            print(
                f"ERROR migrating '{source_property}' from "
                f"'{source_bone}' to '{destination_bone}': {e}"
            )


    # ================================================================
    # DRIVER PATH MIGRATION
    #
    # Supports BOTH:
    #
    #     pose.bones["bone_name"].property_name
    #
    # and:
    #
    #     pose.bones["bone_name"]["property_name"]
    #
    #
    # IMPORTANT:
    # Bone names are matched EXACTLY.
    #
    # Every SINGLE_PROP variable in every driver is checked.
    # ================================================================

    driver_changes = []


    if obj.animation_data:

        # ------------------------------------------------------------
        # Matches:
        #
        # pose.bones["bone_name"].property_name
        #
        # OR:
        #
        # pose.bones["bone_name"]["property_name"]
        #
        # Group 1 = bone name
        # Group 2 = dot-style property
        # Group 3 = bracket-style property
        # ------------------------------------------------------------

        pattern = re.compile(
            r'pose\.bones\["([^"]+)"\]'
            r'(?:\.([A-Za-z_][A-Za-z0-9_]*)|\["([^"]+)"\])'
        )


        # ============================================================
        # CHECK EVERY DRIVER
        # ============================================================

        for fcurve in obj.animation_data.drivers:

            driver = fcurve.driver

            if driver is None:
                continue


            # --------------------------------------------------------
            # CHECK EVERY VARIABLE
            # --------------------------------------------------------

            for variable in driver.variables:

                # ----------------------------------------------------
                # Only SINGLE_PROP variables
                # ----------------------------------------------------

                if variable.type != 'SINGLE_PROP':
                    continue


                # ----------------------------------------------------
                # Check every target
                # ----------------------------------------------------

                for target in variable.targets:

                    if not target.data_path:
                        continue


                    old_path = target.data_path


                    # ------------------------------------------------
                    # Replacement function
                    # ------------------------------------------------

                    def replace_match(match):

                        bone_name = match.group(1)


                        # --------------------------------------------
                        # Determine property name
                        # --------------------------------------------

                        if match.group(2) is not None:

                            # Dot syntax:
                            # pose.bones["bone"].property

                            property_name = match.group(2)

                        else:

                            # ID property syntax:
                            # pose.bones["bone"]["property"]

                            property_name = match.group(3)


                        # --------------------------------------------
                        # Exact bone-name match
                        # --------------------------------------------

                        if bone_name not in MIGRATION_MAP:

                            return match.group(0)


                        # --------------------------------------------
                        # Get migration information
                        # --------------------------------------------

                        (
                            destination_bone,
                            source_property,
                            new_property
                        ) = MIGRATION_MAP[bone_name]


                        # --------------------------------------------
                        # Exact source-property match
                        # --------------------------------------------

                        if property_name != source_property:

                            return match.group(0)


                        # --------------------------------------------
                        # Destination is an ID property.
                        #
                        # Always use bracket syntax.
                        # --------------------------------------------

                        return (
                            f'pose.bones["{destination_bone}"]'
                            f'["{new_property}"]'
                        )


                    # ------------------------------------------------
                    # Replace path
                    # ------------------------------------------------

                    new_path = pattern.sub(
                        replace_match,
                        old_path
                    )


                    # ------------------------------------------------
                    # Apply changed path
                    # ------------------------------------------------

                    if new_path != old_path:

                        target.data_path = new_path

                        driver_changes.append(
                            (
                                variable.name,
                                old_path,
                                new_path
                            )
                        )


    # ================================================================
    # REPORT
    # ================================================================

    print("\n" + "=" * 80)
    print("FOLLOW PROPERTY MIGRATION")
    print("=" * 80)


    # ================================================================
    # PROPERTY MIGRATION REPORT
    # ================================================================

    print("\nMIGRATED PROPERTIES:")

    if migrated:

        for (
            source_bone,
            destination_bone,
            old_property,
            new_property,
            value
        ) in migrated:

            print(
                f'    {source_bone}["{old_property}"]'
                f' -> '
                f'{destination_bone}["{new_property}"]'
                f' = {value}'
            )

    else:

        print("    None")


    # ================================================================
    # DRIVER MIGRATION REPORT
    # ================================================================

    print("\nMIGRATED DRIVER PATHS:")

    if driver_changes:

        for (
            variable_name,
            old_path,
            new_path
        ) in driver_changes:

            print(
                f"\n    Variable: {variable_name}"
            )

            print(
                f"        OLD: {old_path}"
            )

            print(
                f"        NEW: {new_path}"
            )

    else:

        print("    None")


    # ================================================================
    # SUMMARY
    # ================================================================

    print("\n" + "-" * 80)

    print(
        f"Properties migrated: {len(migrated)}"
    )

    print(
        f"Driver paths changed: {len(driver_changes)}"
    )

    print("=" * 80)
    print("Finished.")
    print("=" * 80)

#### RENAME DUPLICATED PROPERTIES ####

def rename_duplicated_properties():
    # ================================================================
    # SETTINGS
    # ================================================================

    TARGET_PROPERTIES = {
        "EYELID_DOWN_LIMIT_L",
        "EYELID_DOWN_LIMIT_R",
        "EYELID_UP_LIMIT_L",
        "EYELID_UP_LIMIT_R",
        "EYE_DOWN_FOLLOW_L",
        "EYE_DOWN_FOLLOW_R",
        "EYE_UP_FOLLOW_L",
        "EYE_UP_FOLLOW_R",
        "FROWN_LIMIT_L",
        "FROWN_LIMIT_R",
        "FROWN_LIMIT",
    }


    # ================================================================
    # BONE NAME -> PREFIX
    # ================================================================

    def get_prefix(bone_name):

        if "eyelid_up" in bone_name:
            return "UP_"

        if "eyelid_low" in bone_name:
            return "LOW_"

        if "mouth" in bone_name:
            return "MOUTH_"

        if "nose" in bone_name:
            return "NOSE_"

        if "chin" in bone_name:
            return "CHIN_"

        return None


    # ================================================================
    # GET RNA PROPERTY
    # ================================================================

    def get_rna_property(name):

        try:
            return bpy.types.PoseBone.bl_rna.properties[name]

        except KeyError:
            return None


    # ================================================================
    # CREATE RNA PROPERTY
    # ================================================================

    def create_rna_property(new_name, source):

        prop_type = source.type

        kwargs = {
            "name": source.name,
            "description": source.description,
        }


        # ------------------------------------------------------------
        # FLOAT
        # ------------------------------------------------------------

        if prop_type == 'FLOAT':

            kwargs.update({
                "default": source.default,
                "min": source.hard_min,
                "max": source.hard_max,
                "soft_min": source.soft_min,
                "soft_max": source.soft_max,
                "step": source.step,
                "precision": source.precision,
                "subtype": source.subtype,
            })

            prop = bpy.props.FloatProperty(**kwargs)


        # ------------------------------------------------------------
        # INT
        # ------------------------------------------------------------

        elif prop_type == 'INT':

            kwargs.update({
                "default": source.default,
                "min": source.hard_min,
                "max": source.hard_max,
                "soft_min": source.soft_min,
                "soft_max": source.soft_max,
                "step": source.step,
                "subtype": source.subtype,
            })

            prop = bpy.props.IntProperty(**kwargs)


        # ------------------------------------------------------------
        # BOOLEAN
        # ------------------------------------------------------------

        elif prop_type == 'BOOLEAN':

            kwargs.update({
                "default": source.default,
            })

            prop = bpy.props.BoolProperty(**kwargs)


        # ------------------------------------------------------------
        # STRING
        # ------------------------------------------------------------

        elif prop_type == 'STRING':

            kwargs.update({
                "default": source.default,
                "subtype": source.subtype,
            })

            prop = bpy.props.StringProperty(**kwargs)


        else:

            print(
                f"WARNING: Unsupported RNA property type "
                f"'{prop_type}' for '{source.identifier}'"
            )

            return False


        # ------------------------------------------------------------
        # Register the new RNA property
        # ------------------------------------------------------------

        try:

            setattr(
                bpy.types.PoseBone,
                new_name,
                prop
            )

        except Exception as e:

            print(
                f"ERROR registering RNA property "
                f"'{new_name}': {e}"
            )

            return False


        return True


    # ================================================================
    # ACTIVE ARMATURE
    # ================================================================

    obj = bpy.context.active_object

    if obj is None or obj.type != 'ARMATURE':

        raise RuntimeError(
            "Please select an armature."
        )


    # ================================================================
    # COLLECT MIGRATIONS
    # ================================================================

    rna_renames = []
    id_renames = []


    for pb in obj.pose.bones:

        prefix = get_prefix(pb.name)

        if prefix is None:
            continue


        for old_name in TARGET_PROPERTIES:

            new_name = prefix + old_name


            # --------------------------------------------------------
            # RNA property
            # --------------------------------------------------------

            source_rna = get_rna_property(old_name)

            if source_rna is not None:

                rna_renames.append(
                    (
                        pb,
                        old_name,
                        new_name,
                        source_rna
                    )
                )


            # --------------------------------------------------------
            # ID property
            # --------------------------------------------------------

            if old_name in pb:

                id_renames.append(
                    (
                        pb,
                        old_name,
                        new_name
                    )
                )


    # ================================================================
    # CREATE NEW RNA DEFINITIONS
    # ================================================================

    created_rna = set()


    for pb, old_name, new_name, source_rna in rna_renames:

        if new_name in created_rna:
            continue


        # If it already exists, don't recreate it.

        if get_rna_property(new_name) is not None:

            print(
                f"RNA property already exists: {new_name}"
            )

            created_rna.add(new_name)

            continue


        print(
            f"Creating RNA property: "
            f"{old_name} -> {new_name}"
        )


        if create_rna_property(
            new_name,
            source_rna
        ):

            created_rna.add(new_name)


    # ================================================================
    # MIGRATE RNA PROPERTIES
    #
    # IMPORTANT:
    # We ALWAYS read the current value with getattr().
    #
    # We do NOT require property_is_set().
    #
    # This means that even if the old RNA property is currently
    # displaying its default value, that value is explicitly copied
    # to the new property.
    # ================================================================

    migrated_rna = []


    for pb, old_name, new_name, source_rna in rna_renames:

        # Make sure new property exists

        if get_rna_property(new_name) is None:
            continue


        try:

            # --------------------------------------------------------
            # READ CURRENT VALUE BEFORE MIGRATION
            # --------------------------------------------------------

            old_value = getattr(
                pb,
                old_name
            )


            # --------------------------------------------------------
            # Preserve whether the old RNA property was explicitly set
            # --------------------------------------------------------

            try:

                was_set = pb.property_is_set(
                    old_name
                )

            except Exception:

                was_set = False


            # --------------------------------------------------------
            # Write CURRENT value to new RNA property
            # --------------------------------------------------------

            setattr(
                pb,
                new_name,
                old_value
            )


            # --------------------------------------------------------
            # Clear old stored RNA value
            # --------------------------------------------------------

            try:

                pb.property_unset(
                    old_name
                )

            except Exception as e:

                print(
                    f"WARNING: Could not unset "
                    f"'{old_name}' on '{pb.name}': {e}"
                )


            migrated_rna.append(
                (
                    pb.name,
                    old_name,
                    new_name,
                    old_value,
                    was_set
                )
            )


        except Exception as e:

            print(
                f"ERROR migrating RNA property "
                f"'{old_name}' on '{pb.name}': {e}"
            )


    # ================================================================
    # MIGRATE ID PROPERTIES
    # ================================================================

    migrated_id = []


    for pb, old_name, new_name in id_renames:

        # ------------------------------------------------------------
        # Make sure old ID property still exists
        # ------------------------------------------------------------

        if old_name not in pb:
            continue


        # ------------------------------------------------------------
        # Don't overwrite existing ID property
        # ------------------------------------------------------------

        if new_name in pb:

            print(
                f"WARNING: ID property already exists: "
                f"{pb.name} -> {new_name}"
            )

            continue


        try:

            # --------------------------------------------------------
            # READ CURRENT ID VALUE
            # --------------------------------------------------------

            old_value = pb[old_name]


            # --------------------------------------------------------
            # Copy UI metadata
            # --------------------------------------------------------

            ui_data = pb.id_properties_ui(
                old_name
            ).as_dict()


            # --------------------------------------------------------
            # Copy library override state
            # --------------------------------------------------------

            try:

                overridable = (
                    pb.is_property_overridable_library(
                        f'["{old_name}"]'
                    )
                )

            except Exception:

                overridable = False


            # --------------------------------------------------------
            # Create new ID property WITH CURRENT VALUE
            # --------------------------------------------------------

            pb[new_name] = old_value


            # --------------------------------------------------------
            # Copy UI settings
            # --------------------------------------------------------

            try:

                pb.id_properties_ui(
                    new_name
                ).update(
                    **ui_data
                )

            except Exception as e:

                print(
                    f"WARNING: Could not copy UI data "
                    f"for '{new_name}': {e}"
                )


            # --------------------------------------------------------
            # Copy override state
            # --------------------------------------------------------

            try:

                pb.property_overridable_library_set(
                    f'["{new_name}"]',
                    overridable
                )

            except Exception:

                pass


            # --------------------------------------------------------
            # Delete old ID property
            # --------------------------------------------------------

            del pb[old_name]


            migrated_id.append(
                (
                    pb.name,
                    old_name,
                    new_name,
                    old_value
                )
            )


        except Exception as e:

            print(
                f"ERROR migrating ID property "
                f"'{old_name}' on '{pb.name}': {e}"
            )


    # ================================================================
    # REPORT
    # ================================================================

    print("\n" + "=" * 80)
    print("PROPERTY RENAMING / MIGRATION FINISHED")
    print("=" * 80)


    # ================================================================
    # RNA PROPERTIES CREATED
    # ================================================================

    print("\nRNA PROPERTIES CREATED:")

    if created_rna:

        for name in sorted(created_rna):

            print(
                f"    {name}"
            )

    else:

        print("    None")


    # ================================================================
    # RNA VALUES MIGRATED
    # ================================================================

    print("\nRNA VALUES MIGRATED:")

    if migrated_rna:

        for (
            bone,
            old_name,
            new_name,
            value,
            was_set
        ) in migrated_rna:

            print(
                f"    {bone}: "
                f"{old_name} -> {new_name} = {value} "
                f"(was_set={was_set})"
            )

    else:

        print("    None")


    # ================================================================
    # ID PROPERTIES MIGRATED
    # ================================================================

    print("\nID PROPERTIES MIGRATED:")

    if migrated_id:

        for (
            bone,
            old_name,
            new_name,
            value
        ) in migrated_id:

            print(
                f"    {bone}: "
                f"{old_name} -> {new_name} = {value}"
            )

    else:

        print("    None")


    print("\n" + "=" * 80)
    print("Finished.")
    print("=" * 80)


#### FIX DUPLICATED PROPERTIES DRIVERS ####

def fix_duplicated_properties_drivers():
    # ================================================================
    # SETTINGS
    # ================================================================

    TARGET_PROPERTIES = {
        "EYELID_DOWN_LIMIT_L",
        "EYELID_DOWN_LIMIT_R",
        "EYELID_UP_LIMIT_L",
        "EYELID_UP_LIMIT_R",
        "EYE_DOWN_FOLLOW_L",
        "EYE_DOWN_FOLLOW_R",
        "EYE_UP_FOLLOW_L",
        "EYE_UP_FOLLOW_R",
        "FROWN_LIMIT",
        "FROWN_LIMIT_L",
        "FROWN_LIMIT_R",
    }


    # ================================================================
    # BONE NAME -> PREFIX
    # ================================================================

    def get_prefix(bone_name):

        if "eyelid_up" in bone_name:
            return "UP_"

        if "eyelid_low" in bone_name:
            return "LOW_"

        if "mouth" in bone_name:
            return "MOUTH_"

        if "nose" in bone_name:
            return "NOSE_"

        if "chin" in bone_name:
            return "CHIN_"

        return None


    # ================================================================
    # ACTIVE ARMATURE
    # ================================================================

    obj = bpy.context.active_object

    if obj is None or obj.type != 'ARMATURE':
        raise RuntimeError(
            "Please select an armature."
        )


    # ================================================================
    # REGEX
    #
    # Matches:
    #
    # pose.bones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L
    #
    # Captures:
    #   1 = bone name
    #   2 = property name
    # ================================================================

    pattern = re.compile(
        r'pose\.bones\["([^"]+)"\]\.([A-Za-z_][A-Za-z0-9_]*)'
    )


    # ================================================================
    # PROCESS DRIVERS
    # ================================================================

    changed = []


    for fcurve in obj.animation_data.drivers if obj.animation_data else []:

        driver = fcurve.driver

        if driver is None:
            continue

        for variable in driver.variables:

            # --------------------------------------------------------
            # Only Single Property variables
            # --------------------------------------------------------

            if variable.type != 'SINGLE_PROP':
                continue

            for target in variable.targets:

                if not target.data_path:
                    continue

                old_path = target.data_path

                # ----------------------------------------------------
                # Replace matching bone/property combinations
                # ----------------------------------------------------

                def replace_match(match):

                    bone_name = match.group(1)
                    property_name = match.group(2)

                    # Is this one of the properties we want?
                    if property_name not in TARGET_PROPERTIES:
                        return match.group(0)

                    # Determine prefix from bone name
                    prefix = get_prefix(bone_name)

                    if prefix is None:
                        return match.group(0)

                    # Already renamed
                    if property_name.startswith(
                        (
                            "UP_",
                            "LOW_",
                            "MOUTH_",
                            "NOSE_",
                            "CHIN_"
                        )
                    ):
                        return match.group(0)

                    new_property_name = (
                        prefix + property_name
                    )

                    return (
                        f'pose.bones["{bone_name}"].'
                        f'{new_property_name}'
                    )

                new_path = pattern.sub(
                    replace_match,
                    old_path
                )

                # ----------------------------------------------------
                # Apply change
                # ----------------------------------------------------

                if new_path != old_path:

                    target.data_path = new_path

                    changed.append(
                        (
                            variable.name,
                            old_path,
                            new_path
                        )
                    )


    # ================================================================
    # REPORT
    # ================================================================

    print("\n" + "=" * 80)
    print("DRIVER PROPERTY PATH RENAMING")
    print("=" * 80)


    if changed:

        for variable_name, old_path, new_path in changed:

            print(
                f"\nVariable: {variable_name}"
            )

            print(
                f"    OLD: {old_path}"
            )

            print(
                f"    NEW: {new_path}"
            )

        print(
            f"\nTotal driver paths changed: {len(changed)}"
        )

    else:

        print(
            "\nNo matching driver paths were found."
        )


    print("\n" + "=" * 80)
    print("Finished.")
    print("=" * 80)

#### CREATE NEW PROPERTIES BONES ####

def create_properties_bones():

    context = bpy.context
    obj = context.object

    if not obj or obj.type != 'ARMATURE':
        raise RuntimeError("Select an armature.")

    arm = obj.data

    # -------------------------------------------------------------------
    # Source Bone : New Bone
    # (List of tuples allows repeated source bones)
    # -------------------------------------------------------------------

    bone_pairs = [
        ("flex_neck_width", "properties_eye_L"),
        ("flex_neck_width", "properties_eye_R"),
        ("flex_neck_width", "properties_mouth"),
        ("flex_neck_width", "properties_nose"),    
        ("flex_neck_width", "properties_cheek_L"),
        ("flex_neck_width", "properties_cheek_R")
        # Add more pairs here...
    ]

    previous_mode = obj.mode

    # -------------------------------------------------------------------
    # Create bones
    # -------------------------------------------------------------------

    bpy.ops.object.mode_set(mode='EDIT')

    ebones = arm.edit_bones

    for src_name, dst_name in bone_pairs:

        src = ebones.get(src_name)

        if src is None:
            print(f'Source bone "{src_name}" not found.')
            continue

        if ebones.get(dst_name):
            print(f'Bone "{dst_name}" already exists.')
            continue

        dst = ebones.new(dst_name)

        # ------------------------------------------------------------
        # Transform
        # ------------------------------------------------------------

        dst.head = src.head.copy()
        dst.tail = src.tail.copy()
        dst.roll = src.roll

        # ------------------------------------------------------------
        # Parenting
        # ------------------------------------------------------------

        if src.parent:
            parent_name = src.parent.name

            # Remap parent if it is also duplicated
            for old_name, new_name in bone_pairs:
                if parent_name == old_name:
                    parent_name = new_name
                    break

            parent = ebones.get(parent_name)

            if parent:
                dst.parent = parent

        dst.use_connect = src.use_connect

        # ------------------------------------------------------------
        # Bone behavior
        # ------------------------------------------------------------

        dst.use_inherit_rotation = src.use_inherit_rotation
        dst.inherit_scale = src.inherit_scale
        dst.use_local_location = src.use_local_location
        dst.use_relative_parent = src.use_relative_parent
        dst.use_deform = src.use_deform

        # ------------------------------------------------------------
        # B-Bone settings
        # ------------------------------------------------------------

        for prop in dir(src):

            if not prop.startswith("bbone_"):
                continue

            if prop in {
                "bbone_custom_handle_start",
                "bbone_custom_handle_end",
            }:
                continue

            try:
                setattr(dst, prop, getattr(src, prop))
            except:
                pass

        # ------------------------------------------------------------
        # B-Bone handles
        # ------------------------------------------------------------

        if src.bbone_custom_handle_start:

            handle_name = src.bbone_custom_handle_start.name

            for old_name, new_name in bone_pairs:
                if handle_name == old_name:
                    handle_name = new_name
                    break

            dst.bbone_custom_handle_start = ebones.get(handle_name)

        if src.bbone_custom_handle_end:

            handle_name = src.bbone_custom_handle_end.name

            for old_name, new_name in bone_pairs:
                if handle_name == old_name:
                    handle_name = new_name
                    break

            dst.bbone_custom_handle_end = ebones.get(handle_name)

        print(f'Created "{dst_name}"')


    # -------------------------------------------------------------------
    # Copy Bone data (Collections & Colors)
    # -------------------------------------------------------------------

    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a lookup for duplicate relationships
    pair_lookup = dict(bone_pairs)

    for src_name, dst_name in bone_pairs:

        src = arm.bones.get(src_name)
        dst = arm.bones.get(dst_name)

        if src is None or dst is None:
            continue

        # ------------------------------------------------------------
        # Bone color
        # ------------------------------------------------------------

        try:
            dst.color.palette = src.color.palette
            dst.color.custom.normal = src.color.custom.normal
            dst.color.custom.select = src.color.custom.select
            dst.color.custom.active = src.color.custom.active
        except:
            pass

        # ------------------------------------------------------------
        # Bone collections
        # ------------------------------------------------------------

        try:
            for collection in list(dst.collections):
                collection.unassign(dst)

            for collection in src.collections:
                collection.assign(dst)

        except Exception as e:
            print(f"Collection copy failed for {dst_name}: {e}")


    # -------------------------------------------------------------------
    # Restore mode
    # -------------------------------------------------------------------

    bpy.ops.object.mode_set(mode=previous_mode)

    print("\nFinished.")


#### MIGRATE PROPERTIES TO NEW PROPERTIES BONES ####

def migrate_properties():
    context = bpy.context
    obj = context.object

    if not obj or obj.type != 'ARMATURE':
        raise RuntimeError("Please select an armature.")

    # -------------------------------------------------------------------
    # Source Bone : Destination Bone
    # -------------------------------------------------------------------

    bone_pairs = {
        "foot_roll_ctrl_L": "properties_leg_L",
        "foot_roll_ctrl_R": "properties_leg_R",
        
        "shoulder_L": "properties_arm_L",
        "shoulder_R": "properties_arm_R",       
        
        "mouth_ctrl": "properties_mouth",    
        "mouth_corner_L": "properties_mouth",   
        "mouth_corner_R": "properties_mouth",
        "maxi": "properties_mouth",         
        "chin_frown_ctrl": "properties_mouth",    
        "mouth_frown_ctrl_L": "properties_mouth",   
        "mouth_frown_ctrl_R": "properties_mouth",   

        "nose_ctrl": "properties_nose",
        "nose_frown_ctrl_L": "properties_nose",
        "nose_frown_ctrl_R": "properties_nose",
        
        "cheek_ctrl_L": "properties_cheek_L",      
        "cheek_ctrl_R": "properties_cheek_R", 
        
        "blink_ctrl_L": "properties_eye_L",
        "eyelid_up_ctrl_L": "properties_eye_L",    
        "eyelid_low_ctrl_L": "properties_eye_L",
        "look_L": "properties_eye_L",    
        "blink_ctrl_R": "properties_eye_R",
        "eyelid_up_ctrl_R": "properties_eye_R",    
        "eyelid_low_ctrl_R": "properties_eye_R",   
        "look_R": "properties_eye_R",                                         
        # Add more pairs here...
    }

    for src_name, dst_name in bone_pairs.items():

        src = obj.pose.bones.get(src_name)
        dst = obj.pose.bones.get(dst_name)

        if src is None:
            print(f'Source bone "{src_name}" not found.')
            continue

        if dst is None:
            print(f'Destination bone "{dst_name}" not found.')
            continue

        print(f"\nCopying properties from '{src_name}' to '{dst_name}'")

        copied_keys = []

        # ------------------------------------------------------------
        # Pass 1: Copy ID properties and their metadata
        # ------------------------------------------------------------

        for key in src.keys():

            # Ignore Blender internal properties
            if key.startswith("_"):
                continue

            copied_keys.append(key)

            # Copy the ID property value
            dst[key] = src[key]

            # Copy UI metadata
            try:
                src_ui = src.id_properties_ui(key)
                dst_ui = dst.id_properties_ui(key)
                dst_ui.update(**src_ui.as_dict())
            except Exception as e:
                print(f"  Failed to copy UI settings for '{key}': {e}")

            # Copy library override flag
            try:
                overridable = src.is_property_overridable_library(f'["{key}"]')
                dst.property_overridable_library_set(f'["{key}"]', overridable)
            except Exception:
                pass

            print(f"  Copied ID property '{key}'")

        # ------------------------------------------------------------
        # Pass 2: Copy RNA values for properties with matching names
        # ------------------------------------------------------------

        for key in copied_keys:

            try:
                # Check that this is an RNA property
                src.bl_rna.properties[key]

                # Copy the current RNA value
                setattr(dst, key, getattr(src, key))

                print(f"  Copied RNA value '{key}'")

            except Exception:
                # Not an RNA property or read-only
                pass

        # ------------------------------------------------------------
        # Pass 3: Remove copied properties from the source bone
        # ------------------------------------------------------------

        for key in copied_keys:

            removed_id = False
            removed_rna = False

            # Remove the legacy ID property
            try:
                del src[key]
                removed_id = True
            except Exception:
                pass

            # Remove any stored RNA value
            try:
                src.property_unset(key)
                removed_rna = True
            except Exception:
                pass

            if removed_id or removed_rna:
                print(
                    f"  Cleaned '{key}' "
                    f"(ID removed={removed_id}, RNA unset={removed_rna})"
                )

    print("\nFinished.")


#### FIX MIGRATERD PROPERTIES DRIVERS####

def fix_migrated_properties_drivers():
    context = bpy.context
    obj = context.active_object

    if obj is None:
        raise RuntimeError("No active object.")

    # -------------------------------------------------------------------
    # Source Bone : Destination Bone
    # -------------------------------------------------------------------

    bone_map = {
        "foot_roll_ctrl_L": "properties_leg_L",
        "foot_roll_ctrl_R": "properties_leg_R",

        "shoulder_L": "properties_arm_L",
        "shoulder_R": "properties_arm_R",

        "mouth_ctrl": "properties_mouth",
        "mouth_corner_L": "properties_mouth",
        "mouth_corner_R": "properties_mouth",
        "maxi": "properties_mouth",
        "chin_frown_ctrl": "properties_mouth",
        "mouth_frown_ctrl_L": "properties_mouth",
        "mouth_frown_ctrl_R": "properties_mouth",

        "nose_ctrl": "properties_nose",
        "nose_frown_ctrl_L": "properties_nose",
        "nose_frown_ctrl_R": "properties_nose",

        "cheek_ctrl_L": "properties_cheek_L",
        "cheek_ctrl_R": "properties_cheek_R",

        "blink_ctrl_L": "properties_eye_L",
        "eyelid_up_ctrl_L": "properties_eye_L",
        "eyelid_low_ctrl_L": "properties_eye_L",
        "look_L": "properties_eye_L",

        "blink_ctrl_R": "properties_eye_R",
        "eyelid_up_ctrl_R": "properties_eye_R",
        "eyelid_low_ctrl_R": "properties_eye_R",
        "look_R": "properties_eye_R",
    }


    # -------------------------------------------------------------------
    # Find all drivers on the active object
    # -------------------------------------------------------------------

    if obj.animation_data is None:
        print("Active object has no animation data.")
    else:

        drivers = obj.animation_data.drivers

        print(f"Found {len(drivers)} drivers.")

        changed_drivers = 0
        changed_variables = 0

        # ----------------------------------------------------------------
        # Iterate through all drivers
        # ----------------------------------------------------------------

        for fcurve in drivers:

            driver = fcurve.driver

            if driver is None:
                continue

            # ------------------------------------------------------------
            # Iterate through all variables
            # ------------------------------------------------------------

            for variable in driver.variables:

                # Only process SINGLE_PROP variables
                if variable.type != 'SINGLE_PROP':
                    continue

                # SINGLE_PROP variables use the first target
                if not variable.targets:
                    continue

                target = variable.targets[0]

                if not target.data_path:
                    continue

                old_path = target.data_path
                new_path = old_path

                # --------------------------------------------------------
                # Look for:
                #
                # pose.bones["bone_name"]
                #
                # --------------------------------------------------------

                for source_bone, destination_bone in bone_map.items():

                    pattern = (
                        r'(pose\.bones\[")'
                        + re.escape(source_bone)
                        + r'("\])'
                    )

                    replacement = r'\1' + destination_bone + r'\2'

                    new_path = re.sub(
                        pattern,
                        replacement,
                        new_path
                    )

                # --------------------------------------------------------
                # Apply change
                # --------------------------------------------------------

                if new_path != old_path:

                    target.data_path = new_path

                    changed_variables += 1
                    changed_drivers += 1

                    print("\nDriver changed:")
                    print(f"  Variable : {variable.name}")
                    print(f"  Old path : {old_path}")
                    print(f"  New path : {new_path}")

        print("\n----------------------------------------")
        print(f"Changed drivers    : {changed_drivers}")
        print(f"Changed variables  : {changed_variables}")
        print("----------------------------------------")


#### UPDATE BLENRIG PROPERTIES TEXT FILE ####

def update_blenrig_text():

    # Replacement content
    replacement_text = """\
import bpy
from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty, FloatVectorProperty

#Check if addon is enabled
Addon = False

for mod in bpy.context.preferences.addons:
    if 'BlenRig' in mod.module:
        Addon = True
    
if Addon == False:
    ######### Update Function for Properties ##########
    def prop_update(self, context):
        try:
            bone_auto_hide(context)
        except:
            pass    
    def reprop_update(self, context):
        try:
            reproportion_toggle(context)
        except:
            pass    
    def rig_toggles_update(self, context):
        try:
            rig_toggles(context)
        except:
            pass        
    def fingers_toggles_update(self, context):
        try:
            fingers_toggles(self, context)
        except:
            pass   
    def toes_toggles_update(self, context):
        try:
            toes_toggles(self, context)   
        except:
            pass                    
    def optimize_face(self, context):
        try:
            toggle_face_drivers(context)
        except:
            pass    
    def optimize_flex(self, context):
        try:
            toggle_flex_drivers(context)
        except:
            pass    
    def optimize_dynamic(self, context):
        try:
            toggle_dynamic_drivers(context)
        except:
            pass    
    def optimize_body(self, context):
        try:
            toggle_body_drivers(context)
        except:
            pass    
    def pole_toggles_update(self, context):
        try:
            pole_toggles(context)
        except:
            pass    
    def eyelids_update(self, context):
        try:
            set_eyelids(context)
        except:
            pass    
    def frowns_update(self, context):
        try:
            set_frowns(context)
        except:
            pass    
    def cheeks_update(self, context):
        try:
            set_cheeks(context)
        except:
            pass    
    def mouth_corners_update(self, context):
        try:
            set_mouth_corners(context)
        except:
            pass    
    def mouth_ctrl_update(self, context):
        try:
            set_mouth_ctrl(context)
        except:
            pass    
    def rj_transforms_update(self, context):
        try:
            set_rj_transforms(context)
        except:
            pass    
    def vol_variation_update(self, context):
        try:
            set_vol_variation(context)
        except:
            pass    
    def vol_prservation_update(self, context):
        try:
            set_vol_preservation(context)
        except:
            pass                
    ######### Properties Creation ############

    #FK/IK

    bpy.types.PoseBone.ik_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_head"
    )

    bpy.types.PoseBone.ik_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_torso"
    )
    bpy.types.PoseBone.inv_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Invert Torso Hierarchy",
        update=prop_update,
        name="inv_torso"
    )
    bpy.types.PoseBone.ik_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_arm_L"
    )
    bpy.types.PoseBone.ik_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_arm_R"
    )
    bpy.types.PoseBone.ik_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_leg_L"
    )
    bpy.types.PoseBone.ik_toes_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_toes_all_L"
    )
    bpy.types.PoseBone.ik_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_leg_R"
    )
    bpy.types.PoseBone.ik_toes_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_toes_all_R"
    )
    bpy.types.PoseBone.ik_fing_ind_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_ind_L"
    )
    bpy.types.PoseBone.ik_fing_mid_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_L"
    )
    bpy.types.PoseBone.ik_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_L"
    )
    bpy.types.PoseBone.ik_fing_lit_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_lit_L"
    )
    bpy.types.PoseBone.ik_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_thumb_L"
    )
    bpy.types.PoseBone.ik_fing_ind_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_ind_R"
    )
    bpy.types.PoseBone.ik_fing_mid_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_R"
    )
    bpy.types.PoseBone.ik_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_mid_R"
    )
    bpy.types.PoseBone.ik_fing_lit_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_lit_R"
    )
    bpy.types.PoseBone.ik_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_thumb_R"
    )
    bpy.types.PoseBone.ik_fing_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_all_R"
    )
    bpy.types.PoseBone.ik_fing_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="IK/FK Toggle",
        update=prop_update,
        name="ik_fing_all_L"
    )

    # SPACE

    bpy.types.PoseBone.space_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_head"
    )
    bpy.types.PoseBone.space_neck = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_neck"
    )
    bpy.types.PoseBone.space_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=3.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_arm_L"
    )
    bpy.types.PoseBone.space_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=3.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_arm_R"
    )
    bpy.types.PoseBone.space_hand_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_hand_L"
    )
    bpy.types.PoseBone.space_hand_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_hand_R"
    )
    bpy.types.PoseBone.space_fing_ind_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ind_L"
    )
    bpy.types.PoseBone.space_fing_mid_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_mid_L"
    )
    bpy.types.PoseBone.space_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ring_L"
    )
    bpy.types.PoseBone.space_fing_lit_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_lit_L"
    )
    bpy.types.PoseBone.space_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_thumb_L"
    )
    bpy.types.PoseBone.space_fing_ind_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ind_R"
    )
    bpy.types.PoseBone.space_fing_mid_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_mid_R"
    )
    bpy.types.PoseBone.space_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_ring_R"
    )
    bpy.types.PoseBone.space_fing_lit_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_lit_R"
    )
    bpy.types.PoseBone.space_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_thumb_R"
    )
    bpy.types.PoseBone.space_fing_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_all_R"
    )
    bpy.types.PoseBone.space_fing_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_fing_all_L"
    )
    bpy.types.PoseBone.space_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_leg_L"
    )
    bpy.types.PoseBone.space_toes_all_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_toes_all_L"
    )
    bpy.types.PoseBone.space_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_leg_R"
    )
    bpy.types.PoseBone.space_toes_all_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Rotation Space",
        update=prop_update,
        name="space_toes_all_R"
    )

    # Poles

    bpy.types.PoseBone.space_arm_ik_pole_L = FloatProperty(
        default=1.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_arm_ik_pole_L"
    )
    bpy.types.PoseBone.space_arm_ik_pole_R = FloatProperty(
        default=1.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_arm_ik_pole_R"
    )
    bpy.types.PoseBone.space_leg_ik_pole_L = FloatProperty(
        default=1.000,
        min=0.000,
        max=2.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_leg_ik_pole_L"
    )
    bpy.types.PoseBone.space_leg_ik_pole_R = FloatProperty(
        default=1.000,
        min=0.000,
        max=2.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pole Space",
        name="space_leg_ik_pole_R"
    )
    bpy.types.PoseBone.toggle_arm_ik_pole_L = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_arm_ik_pole_L"
    )
    bpy.types.PoseBone.toggle_arm_ik_pole_R = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_arm_ik_pole_R"
    )
    bpy.types.PoseBone.toggle_leg_ik_pole_L = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_leg_ik_pole_L"
    )
    bpy.types.PoseBone.toggle_leg_ik_pole_R = BoolProperty(
        default=0,
        description="Toggle pole Target",
        override={'LIBRARY_OVERRIDABLE'},
        update=pole_toggles_update,
        name="toggle_leg_ik_pole_R"
    )

    #Stretchy IK

    bpy.types.PoseBone.toon_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_head"
    )

    bpy.types.PoseBone.toon_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_torso"
    )

    bpy.types.PoseBone.toon_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_arm_L"
    )

    bpy.types.PoseBone.toon_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_arm_R"
    )

    bpy.types.PoseBone.toon_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_leg_L"
    )

    bpy.types.PoseBone.toon_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_leg_R"
    )

    #Stretchy Fingers

    bpy.types.PoseBone.toon_fing_thumb_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_thumb_L"
    )

    bpy.types.PoseBone.toon_fing_index_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_index_L"
    )

    bpy.types.PoseBone.toon_fing_middle_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_middle_L"
    )

    bpy.types.PoseBone.toon_fing_ring_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_ring_L"
    )

    bpy.types.PoseBone.toon_fing_little_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_little_L"
    )

    bpy.types.PoseBone.toon_fing_thumb_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_thumb_R"
    )

    bpy.types.PoseBone.toon_fing_index_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_index_R"
    )

    bpy.types.PoseBone.toon_fing_middle_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_middle_R"
    )

    bpy.types.PoseBone.toon_fing_ring_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_ring_R"
    )

    bpy.types.PoseBone.toon_fing_little_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Stretchy IK Toggle",
        update=prop_update,
        name="toon_fing_little_R"
    )

    #Pin

    bpy.types.PoseBone.pin_elbow_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Elbow_L",
        update=prop_update,
        name="pin_elbow_L"
    )

    bpy.types.PoseBone.pin_elbow_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Elbow_R",
        update=prop_update,
        name="pin_elbow_R"
    )

    bpy.types.PoseBone.pin_knee_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Knee_L",
        update=prop_update,
        name="pin_knee_L"
    )

    bpy.types.PoseBone.pin_knee_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=1.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Pin Knee_R",
        update=prop_update,
        name="pin_knee_R"
    )

    # LOOK SWITCH
    bpy.types.PoseBone.look_switch = FloatProperty(
        default=3.000,
        min=0.000,
        max=3.000,
        precision=0,
        step=100,
        options={'ANIMATABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        description="Target of Eyes",
        update=prop_update,
        name="look_switch"
    )

    # REPROPORTION
    bpy.types.Armature.reproportion = BoolProperty(
        default=0,
        description="Toggle Reproportion Mode",
        update=reprop_update,
        name="reproportion"
    )
    # TOGGLE_FACE_DRIVERS
    bpy.types.Armature.toggle_face_drivers = BoolProperty(
        default=1,
        description="Toggle Face Riggin Drivers",
        update=optimize_face,
        name="toggle_face_drivers"
    )
    # TOGGLE_DYNAMIC_DRIVERS
    bpy.types.Armature.toggle_flex_drivers = BoolProperty(
        default=1,
        description="Toggle Flex Drivers",
        update=optimize_flex,
        name="toggle_flex_drivers"
    )
    # TOGGLE_DYNAMIC_DRIVERS
    bpy.types.Armature.toggle_dynamic_drivers = BoolProperty(
        default=1,
        description="Toggle Dynamic Shaping Drivers",
        update=optimize_dynamic,
        name="toggle_dynamic_drivers"
    )
    # TOGGLE_BODY_DRIVERS
    bpy.types.Armature.toggle_body_drivers = BoolProperty(
        default=1,
        description="Toggle Body Rigging Drivers",
        update=optimize_body,
        name="toggle_body_drivers"
    )
    ### TOGGLES
    #Fingers L
    bpy.types.PoseBone.toggle_fingers_L = BoolProperty(
        default=0,
        description="Toggle fingers in rig",
        update=rig_toggles_update,
        name="toggle_fingers_L"
    )
    bpy.types.PoseBone.toggle_fingers_index_L = BoolProperty(
        default=1,
        description="Toggle index finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_index_L"
    )
    bpy.types.PoseBone.toggle_fingers_middle_L = BoolProperty(
        default=1,
        description="Toggle middle finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_middle_L"
    )
    bpy.types.PoseBone.toggle_fingers_ring_L = BoolProperty(
        default=1,
        description="Toggle ring finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_ring_L"
    )
    bpy.types.PoseBone.toggle_fingers_little_L = BoolProperty(
        default=1,
        description="Toggle little finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_little_L"
    )
    bpy.types.PoseBone.toggle_fingers_thumb_L = BoolProperty(
        default=1,
        description="Toggle thumb finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_thumb_L"
    )

    #Toes L
    bpy.types.PoseBone.toggle_toes_L = BoolProperty(
        default=0,
        description="Toggle toes in rig",
        update=rig_toggles_update,
        name="toggle_toes_L"
    )
    bpy.types.PoseBone.toggle_toes_index_L = BoolProperty(
        default=1,
        description="Toggle index toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_index_L"
    )
    bpy.types.PoseBone.toggle_toes_middle_L = BoolProperty(
        default=1,
        description="Toggle middle toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_middle_L"
    )
    bpy.types.PoseBone.toggle_toes_fourth_L = BoolProperty(
        default=1,
        description="Toggle fourth toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_fourth_L"
    )
    bpy.types.PoseBone.toggle_toes_little_L = BoolProperty(
        default=1,
        description="Toggle little toe in rig",
        update=toes_toggles_update,
        name="toggle_toe_little_L"
    )
    bpy.types.PoseBone.toggle_toes_big_L = BoolProperty(
        default=1,
        description="Toggle big toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_big_L"
    )

    #Fingers R
    bpy.types.PoseBone.toggle_fingers_R = BoolProperty(
        default=0,
        description="Toggle fingers in rig",
        update=rig_toggles_update,
        name="toggle_fingers_R"
    )
    bpy.types.PoseBone.toggle_fingers_index_R = BoolProperty(
        default=1,
        description="Toggle index finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_index_R"
    )
    bpy.types.PoseBone.toggle_fingers_middle_R = BoolProperty(
        default=1,
        description="Toggle middle finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_middle_R"
    )
    bpy.types.PoseBone.toggle_fingers_ring_R = BoolProperty(
        default=1,
        description="Toggle ring finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_ring_R"
    )
    bpy.types.PoseBone.toggle_fingers_little_R = BoolProperty(
        default=1,
        description="Toggle little finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_little_R"
    )
    bpy.types.PoseBone.toggle_fingers_thumb_R = BoolProperty(
        default=1,
        description="Toggle thumb finger in rig",
        update=fingers_toggles_update,
        name="toggle_fingers_thumb_R"
    )

    #Toes R
    bpy.types.PoseBone.toggle_toes_R = BoolProperty(
        default=0,
        description="Toggle toes in rig",
        update=rig_toggles_update,
        name="toggle_toes_R"
    )
    bpy.types.PoseBone.toggle_toes_index_R = BoolProperty(
        default=1,
        description="Toggle index toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_index_R"
    )
    bpy.types.PoseBone.toggle_toes_middle_R = BoolProperty(
        default=1,
        description="Toggle middle toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_middle_R"
    )
    bpy.types.PoseBone.toggle_toes_fourth_R = BoolProperty(
        default=1,
        description="Toggle fourth toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_fourth_R"
    )
    bpy.types.PoseBone.toggle_toes_little_R = BoolProperty(
        default=1,
        description="Toggle little toe in rig",
        update=toes_toggles_update,
        name="toggle_toe_little_R"
    )
    bpy.types.PoseBone.toggle_toes_big_R = BoolProperty(
        default=1,
        description="Toggle big toe in rig",
        update=toes_toggles_update,
        name="toggle_toes_big_R"
    )

    #### FACIAL PROPERTIES ####

    # EYELIDS

    bpy.types.PoseBone.UP_EYELID_DOWN_LIMIT_L = FloatProperty(
        default=0.010,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        update=eyelids_update,
        name="UP_EYELID_DOWN_LIMIT_L"
    )

    bpy.types.PoseBone.LOW_EYELID_DOWN_LIMIT_L = FloatProperty(
        default=0.010,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        update=eyelids_update,
        name="LOW_EYELID_DOWN_LIMIT_L"
    )

    bpy.types.PoseBone.UP_EYELID_UP_LIMIT_L = FloatProperty(
        default=0.0035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        update=eyelids_update,
        name="UP_EYELID_UP_LIMIT_L"
    )

    bpy.types.PoseBone.LOW_EYELID_UP_LIMIT_L = FloatProperty(
        default=0.0035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        update=eyelids_update,
        name="LOW_EYELID_UP_LIMIT_L"
    )

    bpy.types.PoseBone.EYELID_OUT_LIMIT_L = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Outwards Movement Limit",
        update=eyelids_update,
        name="EYELID_OUT_LIMIT_L"
    )

    bpy.types.PoseBone.EYELID_IN_LIMIT_L = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Inwards Movement Limit",
        update=eyelids_update,
        name="EYELID_IN_LIMIT_L"
    )

    bpy.types.PoseBone.UP_EYE_DOWN_FOLLOW_L = FloatProperty(
        default=0.020,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        update=eyelids_update,
        name="UP_EYE_DOWN_FOLLOW_L"
    )

    bpy.types.PoseBone.LOW_EYE_DOWN_FOLLOW_L = FloatProperty(
        default=0.020,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        update=eyelids_update,
        name="LOW_EYE_DOWN_FOLLOW_L"
    )

    bpy.types.PoseBone.UP_EYE_UP_FOLLOW_L = FloatProperty(
        default=0.008,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        update=eyelids_update,
        name="UP_EYE_UP_FOLLOW_L"
    )

    bpy.types.PoseBone.LOW_EYE_UP_FOLLOW_L = FloatProperty(
        default=0.008,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        update=eyelids_update,
        name="LOW_EYE_UP_FOLLOW_L"
    )

    bpy.types.PoseBone.AUTO_CHEEK_L = IntProperty(
        default=15,
        min=0,
        max=1000,
        description="Automaic movement range for when cheek moves up",
        update=eyelids_update,
        name="AUTO_CHEEK_L"
    )

    bpy.types.PoseBone.UP_EYELID_DOWN_LIMIT_R = FloatProperty(
        default=0.0065,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        update=eyelids_update,
        name="UP_EYELID_DOWN_LIMIT_R"
    )

    bpy.types.PoseBone.LOW_EYELID_DOWN_LIMIT_R = FloatProperty(
        default=0.0065,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Downwards Movement Limit",
        update=eyelids_update,
        name="LOW_EYELID_DOWN_LIMIT_R"
    )

    bpy.types.PoseBone.UP_EYELID_UP_LIMIT_R = FloatProperty(
        default=0.0145,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        update=eyelids_update,
        name="UP_EYELID_UP_LIMIT_R"
    )

    bpy.types.PoseBone.LOW_EYELID_UP_LIMIT_R = FloatProperty(
        default=0.0145,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upper Eyelid Upwards Movement Limit",
        update=eyelids_update,
        name="LOW_EYELID_UP_LIMIT_R"
    )

    bpy.types.PoseBone.EYELID_OUT_LIMIT_R = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Outwards Movement Limit",
        update=eyelids_update,
        name="EYELID_OUT_LIMIT_R"
    )

    bpy.types.PoseBone.EYELID_IN_LIMIT_R = FloatProperty(
        default=60.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Eyelid Inwards Movement Limit",
        update=eyelids_update,
        name="EYELID_IN_LIMIT_R"
    )

    bpy.types.PoseBone.UP_EYE_DOWN_FOLLOW_R = FloatProperty(
        default=0.020,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        update=eyelids_update,
        name="UP_EYE_DOWN_FOLLOW_R"
    )

    bpy.types.PoseBone.LOW_EYE_DOWN_FOLLOW_R = FloatProperty(
        default=0.020,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks down",
        update=eyelids_update,
        name="LOW_EYE_DOWN_FOLLOW_R"
    )

    bpy.types.PoseBone.UP_EYE_UP_FOLLOW_R = FloatProperty(
        default=0.008,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        update=eyelids_update,
        name="UP_EYE_UP_FOLLOW_R"
    )

    bpy.types.PoseBone.LOW_EYE_UP_FOLLOW_R = FloatProperty(
        default=0.008,
        min=0.000,
        max=10.000,
        precision=3,
        description="Automatic movement for when eye looks up",
        update=eyelids_update,
        name="LOW_EYE_UP_FOLLOW_R"
    )

    bpy.types.PoseBone.AUTO_CHEEK_R = IntProperty(
        default=15,
        min=0,
        max=1000,
        description="Automaic movement range for when cheek moves up",
        update=eyelids_update,
        name="AUTO_CHEEK_R"
    )

    #FROWNS

    bpy.types.PoseBone.NOSE_FROWN_LIMIT_L = FloatProperty(
        default=0.0350,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="NOSE_FROWN_LIMIT_L"
    )

    bpy.types.PoseBone.MOUTH_FROWN_LIMIT_L = FloatProperty(
        default=0.0350,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="MOUTH_FROWN_LIMIT_L"
    )    

    bpy.types.PoseBone.NOSE_FROWN_LIMIT_R = FloatProperty(
        default=0.0350,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="NOSE_FROWN_LIMIT_R"
    )

    bpy.types.PoseBone.MOUTH_FROWN_LIMIT_R = FloatProperty(
        default=0.0350,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="MOUTH_FROWN_LIMIT_R"
    )

    bpy.types.PoseBone.CHIN_FROWN_LIMIT = FloatProperty(
        default=0.000,
        min=0.000,
        max=10.000,
        precision=3,
        description="Transform range for frown action",
        update=frowns_update,
        name="CHIN_FROWN_LIMIT"
    )

    #CHEEKS

    bpy.types.PoseBone.AUTO_SMILE_L = FloatProperty(
        default=0.400,
        min=0.000,
        max=1.000,
        precision=3,
        description="Automaic movement range for when mouth corner moves up",
        update=cheeks_update,
        name="AUTO_SMILE_L"
    )

    bpy.types.PoseBone.CHEEK_DOWN_LIMIT_L = FloatProperty(
        default=0.010,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=cheeks_update,
        name="CHEEK_DOWN_LIMIT_L"
    )

    bpy.types.PoseBone.CHEEK_UP_LIMIT_L = FloatProperty(
        default=0.0140,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=cheeks_update,
        name="CHEEK_UP_LIMIT_L"
    )

    bpy.types.PoseBone.AUTO_SMILE_R = FloatProperty(
        default=0.400,
        min=0.000,
        max=1.000,
        precision=3,
        description="Automaic movement range for when mouth corner moves up",
        update=cheeks_update,
        name="AUTO_SMILE_R"
    )

    bpy.types.PoseBone.CHEEK_DOWN_LIMIT_R = FloatProperty(
        default=0.010,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=cheeks_update,
        name="CHEEK_DOWN_LIMIT_R"
    )

    bpy.types.PoseBone.CHEEK_UP_LIMIT_R = FloatProperty(
        default=0.014,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=cheeks_update,
        name="CHEEK_UP_LIMIT_R"
    )

    #MOUTH CORNERS

    bpy.types.PoseBone.AUTO_BACK_L = FloatProperty(
        default=-140.0,
        min=-1000.000,
        max=1000.000,
        description="Automatic backwards movement when corner moves out",
        update=mouth_corners_update,
        name="AUTO_BACK_L"
    )

    bpy.types.PoseBone.IN_LIMIT_L = FloatProperty(
        default=0.014,
        min=0.000,
        max=10.000,
        precision=3,
        description="Inwards movement limit",
        update=mouth_corners_update,
        name="IN_LIMIT_L"
    )

    bpy.types.PoseBone.OUT_LIMIT_L = FloatProperty(
        default=0.04,
        min=0.000,
        max=10.000,
        precision=3,
        description="Outwards movement limit",
        update=mouth_corners_update,
        name="OUT_LIMIT_L"
    )

    bpy.types.PoseBone.UP_LIMIT_L = FloatProperty(
        default=0.038,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=mouth_corners_update,
        name="UP_LIMIT_L"
    )

    bpy.types.PoseBone.DOWN_LIMIT_L = FloatProperty(
        default=0.024,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=mouth_corners_update,
        name="DOWN_LIMIT_L"
    )

    bpy.types.PoseBone.FORW_LIMIT_L = FloatProperty(
        default=0.035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Forwards movement limit",
        update=mouth_corners_update,
        name="FORW_LIMIT_L"
    )

    bpy.types.PoseBone.BACK_LIMIT_L = FloatProperty(
        default=0.035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Backwards movement limit",
        update=mouth_corners_update,
        name="BACK_LIMIT_L"
    )

    bpy.types.PoseBone.AUTO_BACK_R = FloatProperty(
        default=-140.0,
        min=-1000.000,
        max=1000.000,
        description="Automatic backwards movement when corner moves out",
        update=mouth_corners_update,
        name="AUTO_BACK_R"
    )

    bpy.types.PoseBone.IN_LIMIT_R = FloatProperty(
        default=0.014,
        min=0.000,
        max=10.000,
        precision=3,
        description="Inwards movement limit",
        update=mouth_corners_update,
        name="IN_LIMIT_R"
    )

    bpy.types.PoseBone.OUT_LIMIT_R = FloatProperty(
        default=0.04,
        min=0.000,
        max=10.000,
        precision=3,
        description="Outwards movement limit",
        update=mouth_corners_update,
        name="OUT_LIMIT_R"
    )

    bpy.types.PoseBone.UP_LIMIT_R = FloatProperty(
        default=0.038,
        min=0.000,
        max=10.000,
        precision=3,
        description="Upwards movement limit",
        update=mouth_corners_update,
        name="UP_LIMIT_R"
    )

    bpy.types.PoseBone.DOWN_LIMIT_R = FloatProperty(
        default=0.024,
        min=0.000,
        max=10.000,
        precision=3,
        description="Downwards movement limit",
        update=mouth_corners_update,
        name="DOWN_LIMIT_R"
    )

    bpy.types.PoseBone.FORW_LIMIT_R = FloatProperty(
        default=0.035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Forwards movement limit",
        update=mouth_corners_update,
        name="FORW_LIMIT_R"
    )

    bpy.types.PoseBone.BACK_LIMIT_R = FloatProperty(
        default=0.035,
        min=0.000,
        max=10.000,
        precision=3,
        description="Backwards movement limit",
        update=mouth_corners_update,
        name="BACK_LIMIT_R"
    )

    #MOUTH CTRL

    bpy.types.PoseBone.IN_LIMIT = FloatProperty(
        default=0.014,
        min=0.000,
        max=10.000,
        precision=3,
        description="Inwards movement limit",
        update=mouth_ctrl_update,
        name="IN_LIMIT"
    )

    bpy.types.PoseBone.OUT_LIMIT = FloatProperty(
        default=0.04,
        min=0.000,
        max=10.000,
        precision=3,
        description="Outwards movement limit",
        update=mouth_ctrl_update,
        name="OUT_LIMIT"
    )

    bpy.types.PoseBone.SMILE_LIMIT = FloatProperty(
        default=0.038,
        min=0.000,
        max=100.000,
        precision=3,
        description="Smile rate for mouth_ctrl roatation",
        update=mouth_ctrl_update,
        name="SMILE_LIMIT"
    )

    bpy.types.PoseBone.U_M_CTRL_LIMIT = FloatProperty(
        default=0.020,
        min=0.000,
        max=1.000,
        precision=3,
        description="Transformation amount for U_M controllers",
        update=mouth_ctrl_update,
        name="U_M_CTRL_LIMIT"
    )

    bpy.types.PoseBone.JAW_ROTATION = FloatProperty(
        default=10.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Jaw rotation rate for mouth_ctrl vertical movement",
        update=mouth_ctrl_update,
        name="JAW_ROTATION"
    )

    bpy.types.PoseBone.JAW_DOWN_LIMIT = FloatProperty(
        default=20.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Jaw downwards rotation limit",
        update=mouth_ctrl_update,
        name="JAW_DOWN_LIMIT"
    )

    bpy.types.PoseBone.JAW_UP_LIMIT = FloatProperty(
        default=10.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="Jaw upwards rotation limit",
        update=mouth_ctrl_update,
        name="JAW_UP_LIMIT"
    )

    #REALISTIC JOINTS

    bpy.types.PoseBone.realistic_joints_fingers_rot_L = FloatVectorProperty(
        default=(5.0, 5.0, 5.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_rot_L",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_fingers_loc_L = FloatVectorProperty(
        default=(0.004, 0.004, 0.004),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_loc_L",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_toes_rot_L = FloatVectorProperty(
        default=(4.0, 4.0, 4.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_rot_L",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_toes_loc_L = FloatVectorProperty(
        default=(0.002, 0.002, 0.002),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_loc_L",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_elbow_loc_L = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_loc_L"
    )

    bpy.types.PoseBone.realistic_joints_elbow_rot_L = FloatProperty(
        default=0.000,
        min=-0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_rot_L"
    )

    bpy.types.PoseBone.realistic_joints_wrist_rot_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_wrist_rot_L"
    )

    bpy.types.PoseBone.realistic_joints_ankle_rot_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_ankle_rot_L"
    )

    bpy.types.PoseBone.realistic_joints_knee_loc_L = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_loc_L"
    )

    bpy.types.PoseBone.realistic_joints_knee_rot_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_rot_L"
    )

    bpy.types.PoseBone.realistic_joints_fingers_rot_R = FloatVectorProperty(
        default=(5.0, 5.0, 5.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_rot_R",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_fingers_loc_R = FloatVectorProperty(
        default=(0.004, 0.004, 0.004),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_fingers_loc_R",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_toes_rot_R = FloatVectorProperty(
        default=(4.0, 4.0, 4.0),
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_rot_R",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_toes_loc_R = FloatVectorProperty(
        default=(0.002, 0.002, 0.002),
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_toes_loc_R",
        subtype='NONE',
        size=3
    )

    bpy.types.PoseBone.realistic_joints_elbow_loc_R = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_loc_R"
    )

    bpy.types.PoseBone.realistic_joints_elbow_rot_R = FloatProperty(
        default=0.000,
        min=-0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_elbow_rot_R"
    )

    bpy.types.PoseBone.realistic_joints_wrist_rot_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_wrist_rot_R"
    )

    bpy.types.PoseBone.realistic_joints_ankle_rot_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_ankle_rot_R"
    )

    bpy.types.PoseBone.realistic_joints_knee_loc_R = FloatProperty(
        default=0.000,
        min=-10.000,
        max=10.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_loc_R"
    )

    bpy.types.PoseBone.realistic_joints_knee_rot_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=180.000,
        precision=3,
        description="joint displacement simulation",
        update=rj_transforms_update,
        name="realistic_joints_knee_rot_R"
    )

    # VOLUME VARIATION

    bpy.types.PoseBone.volume_variation_arm_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_arm_L"
    )

    bpy.types.PoseBone.volume_variation_fingers_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_fingers_L"
    )

    bpy.types.PoseBone.volume_variation_leg_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_leg_L"
    )

    bpy.types.PoseBone.volume_variation_toes_L = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_toes_L"
    )

    bpy.types.PoseBone.volume_variation_arm_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_arm_R"
    )

    bpy.types.PoseBone.volume_variation_fingers_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_fingers_R"
    )

    bpy.types.PoseBone.volume_variation_leg_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_leg_R"
    )

    bpy.types.PoseBone.volume_variation_toes_R = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_toes_R"
    )

    bpy.types.PoseBone.volume_variation_torso = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_torso"
    )

    bpy.types.PoseBone.volume_variation_head = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_head"
    )

    bpy.types.PoseBone.volume_variation_neck = FloatProperty(
        default=0.000,
        min=0.000,
        max=100.000,
        precision=3,
        description="Volume Variation for stretch and squash",
        update=vol_variation_update,
        name="volume_variation_neck"
    )

    # VOLUME PRESERVATION BONES MOVEMENT

    bpy.types.PoseBone.volume_preservation_fingers_down_L = FloatProperty(
        default=0.025,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_fingers_down_L"
    )

    bpy.types.PoseBone.volume_preservation_knuckles_down_L = FloatProperty(
        default=0.01,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_down_L"
    )

    bpy.types.PoseBone.volume_preservation_knuckles_up_L = FloatProperty(
        default=0.075,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_up_L"
    )

    bpy.types.PoseBone.volume_preservation_palm_down_L = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_palm_down_L"
    )

    bpy.types.PoseBone.volume_preservation_fingers_down_R = FloatProperty(
        default=0.025,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_fingers_down_R"
    )

    bpy.types.PoseBone.volume_preservation_knuckles_down_R = FloatProperty(
        default=0.01,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_down_R"
    )

    bpy.types.PoseBone.volume_preservation_knuckles_up_R = FloatProperty(
        default=0.075,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_knuckles_up_R"
    )

    bpy.types.PoseBone.volume_preservation_palm_down_R = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_palm_down_R"
    )

    bpy.types.PoseBone.volume_preservation_sole_down_L = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_sole_down_L"
    )

    bpy.types.PoseBone.volume_preservation_toe_knuckles_up_L = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toe_knuckles_up_L"
    )

    bpy.types.PoseBone.volume_preservation_toes_down_L = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toes_down_L"
    )

    bpy.types.PoseBone.volume_preservation_sole_down_R = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_sole_down_R"
    )

    bpy.types.PoseBone.volume_preservation_toe_knuckles_up_R = FloatProperty(
        default=0.1,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toe_knuckles_up_R"
    )

    bpy.types.PoseBone.volume_preservation_toes_down_R = FloatProperty(
        default=0.05,
        min=0.000,
        max=10.000,
        precision=3,
        description="Volume Preservation Bones Movement Rage",
        update=vol_prservation_update,
        name="volume_preservation_toes_down_R"
    )
"""


    # Find all matching text blocks
    matching_texts = [
        text
        for text in bpy.data.texts
        if "BlenRig_Properties" in text.name
    ]


    # Check if any were found
    if not matching_texts:
        raise RuntimeError(
            'No text blocks found containing "BlenRig_Properties" in their name.'
        )


    # Replace the contents of every matching text block
    for text_block in matching_texts:

        text_block.clear()
        text_block.write(replacement_text)

        print(
            f'Replaced contents of text block: "{text_block.name}"'
        )


    print(
        f"\nTotal text blocks modified: {len(matching_texts)}"
    )

##### EXEC #####

def biped_update_5_000():

    arm = bpy.context.active_object
    arm_data = arm.data
    pbones = arm.pose.bones

    version = tuple(
        int(x) for x in arm_data["rig_version"].split(".")
    )

    if (4, 0, 0) <= version < (5, 0, 0):

        wm = bpy.context.window_manager

        # --------------------------------------------------------
        # Start progress
        # --------------------------------------------------------

        wm.progress_begin(0, 100)
        bpy.context.window.cursor_modal_set("WAIT")

        try:

            wm.progress_update(5)
            restore_rna_properties()
            fix_driver_paths()

            wm.progress_update(15)
            create_mocap_props()

            wm.progress_update(25)
            add_mocap_constraints()

            wm.progress_update(35)
            add_mocap_drivers()

            wm.progress_update(45)
            update_spine_neck_tongue_props()

            wm.progress_update(55)
            rename_duplicated_properties()

            wm.progress_update(65)
            fix_duplicated_properties_drivers()

            wm.progress_update(75)
            create_properties_bones()

            wm.progress_update(85)
            migrate_properties()

            wm.progress_update(92)
            fix_migrated_properties_drivers()

            wm.progress_update(97)
            update_blenrig_text()

            wm.progress_update(100)

            arm_data["rig_version"] = "5.0.0"

        finally:

            # ----------------------------------------------------
            # Always restore cursor/progress, even if an error
            # occurs during the update
            # ----------------------------------------------------

            wm.progress_end()
            bpy.context.window.cursor_modal_restore()
import bpy

from bpy.types import (
    Operator,
    Menu,
    Panel,
    UIList,
    PropertyGroup,
)
from bpy.props import (
    StringProperty,
    IntProperty,
    EnumProperty,
    BoolProperty,
    CollectionProperty,
)

# Data Structure ##############################################################

# Note: bones are stored by name, this means that if the bone is renamed,
# there can be problems. However, bone renaming is unlikely during animation.


class SelectionEntry(PropertyGroup):
    name: StringProperty(name="Bone Name")


class SelectionSet(PropertyGroup):
    name: StringProperty(name="Set Name")
    bone_ids: CollectionProperty(type=SelectionEntry)
    is_selected: BoolProperty(name="Is Selected")

    def get_all_visible_bones_in_list(self, context):
        arm = context.object
        # el activo de la lista = arm.blenrig_active_selection_set
        bones_list = arm.blenrig_selection_sets
        all_visible_bones = []
        for item_list in bones_list:
            if item_list.visible:
                for bone in item_list.bone_ids:
                    if bone.name not in all_visible_bones:
                        all_visible_bones.append(bone.name)
        if all_visible_bones:
            return all_visible_bones

    def visible_update(self, context):
        arm = context.object
        visibility = not self.visible
        # guardo todos los que si son visibles por los grupos:
        all_vivible_bones = self.get_all_visible_bones_in_list(context)
        for bone in self.bone_ids:
            arm.data.bones[bone.name].hide = visibility
        # restauramos todos los que si era visibles
        if all_vivible_bones:
            for bone_name in all_vivible_bones:
                arm.data.bones[bone_name].hide = False

    visible: BoolProperty(default=True, update=visible_update)


# UI Panel w/ UIList ##########################################################

class BLENRIG_UL_selection_set(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        layout.prop(item, "name", text="", icon='GROUP_BONE', emboss=False)
        layout.prop(item, "visible", text="", icon='HIDE_OFF' if item.visible else 'HIDE_ON', emboss=False)

        # if self.layout_type in ('DEFAULT', 'COMPACT'):
        #     layout.prop(item, "is_selected", text="")


class BLENRIG_MT_selection_sets_context_menu(Menu):
    bl_label = "Selection Sets Specials"

    def draw(self, context):
        layout = self.layout

        layout.operator("blenrig.selection_set_delete_all", icon='X')
        layout.operator("blenrig.selection_set_remove_bones", icon='X')
        layout.operator("blenrig.selection_set_copy", icon='COPYDOWN')
        layout.operator("blenrig.selection_set_paste", icon='PASTEDOWN')


class BLENRIG_MT_selection_set_create(Menu):
    bl_label = "Choose Selection Set"

    def draw(self, context):
        layout = self.layout
        layout.operator("blenrig.selection_set_add_and_assign",
                        text="New Selection Set")


class BLENRIG_MT_selection_sets_select(Menu):
    bl_label = 'Select Selection Set'

    @classmethod
    def poll(cls, context):
        return BLENRIG_OT_selection_set_select.poll(context)

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'EXEC_DEFAULT'
        for idx, sel_set in enumerate(context.object.blenrig_selection_sets):
            props = layout.operator(BLENRIG_OT_selection_set_select.bl_idname, text=sel_set.name)
            props.selection_set_index = idx


# Operators ###################################################################

class PluginOperator(Operator):
    """Operator only available for objects of type armature in pose mode."""
    @classmethod
    def poll(cls, context):
        return (context.object and
                context.object.type == 'ARMATURE' and
                context.mode == 'POSE')


class NeedSelSetPluginOperator(PluginOperator):
    """Operator only available if the armature has a selected selection set."""
    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False
        arm = context.object
        return 0 <= arm.blenrig_active_selection_set < len(arm.blenrig_selection_sets)


class BLENRIG_OT_selection_set_delete_all(PluginOperator):
    bl_idname = "blenrig.selection_set_delete_all"
    bl_label = "Delete All Sets"
    bl_description = "Deletes All Selection Sets"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        arm.blenrig_selection_sets.clear()
        return {'FINISHED'}


class BLENRIG_OT_selection_set_remove_bones(PluginOperator):
    bl_idname = "blenrig.selection_set_remove_bones"
    bl_label = "Remove Selected Bones from All Sets"
    bl_description = "Removes the Selected Bones from All Sets"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object

        # iterate only the selected bones in current pose that are not hidden
        for bone in context.selected_pose_bones:
            for selset in arm.blenrig_selection_sets:
                if bone.name in selset.bone_ids:
                    idx = selset.bone_ids.find(bone.name)
                    selset.bone_ids.remove(idx)

        return {'FINISHED'}


class BLENRIG_OT_selection_set_move(NeedSelSetPluginOperator):
    bl_idname = "blenrig.selection_set_move"
    bl_label = "Move Selection Set in List"
    bl_description = "Move the active Selection Set up/down the list of sets"
    bl_options = {'UNDO', 'REGISTER'}

    direction: EnumProperty(
        name="Move Direction",
        description="Direction to move the active Selection Set: UP (default) or DOWN",
        items=[
            ('UP', "Up", "", -1),
            ('DOWN', "Down", "", 1),
        ],
        default='UP',
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False
        arm = context.object
        return len(arm.blenrig_selection_sets) > 1

    def execute(self, context):
        arm = context.object

        active_idx = arm.blenrig_active_selection_set
        new_idx = active_idx + (-1 if self.direction == 'UP' else 1)

        if new_idx < 0 or new_idx >= len(arm.blenrig_selection_sets):
            return {'FINISHED'}

        arm.blenrig_selection_sets.move(active_idx, new_idx)
        arm.blenrig_active_selection_set = new_idx

        return {'FINISHED'}


class BLENRIG_OT_selection_set_add(PluginOperator):
    bl_idname = "blenrig.selection_set_add"
    bl_label = "Create Selection Set"
    bl_description = "Creates a new empty Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        sel_sets = arm.blenrig_selection_sets
        new_sel_set = sel_sets.add()
        new_sel_set.name = uniqify("SelectionSet", sel_sets.keys())

        # select newly created set
        arm.blenrig_active_selection_set = len(sel_sets) - 1

        return {'FINISHED'}


class BLENRIG_OT_selection_set_remove(NeedSelSetPluginOperator):
    bl_idname = "blenrig.selection_set_remove"
    bl_label = "Delete Selection Set"
    bl_description = "Delete a Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object

        arm.blenrig_selection_sets.remove(arm.blenrig_active_selection_set)

        # change currently active selection set
        numsets = len(arm.blenrig_selection_sets)
        if (arm.blenrig_active_selection_set > (numsets - 1) and numsets > 0):
            arm.blenrig_active_selection_set = len(arm.blenrig_selection_sets) - 1

        return {'FINISHED'}


class BLENRIG_OT_selection_set_assign(PluginOperator):
    bl_idname = "blenrig.selection_set_assign"
    bl_label = "Add Bones to Selection Set"
    bl_description = "Add selected bones to Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def invoke(self, context, event):
        arm = context.object

        if not (arm.blenrig_active_selection_set < len(arm.blenrig_selection_sets)):
            bpy.ops.wm.call_menu("INVOKE_DEFAULT",
                                 name="BLENRIG_MT_selection_set_create")
        else:
            bpy.ops.blenrig.selection_set_assign('EXEC_DEFAULT')

        return {'FINISHED'}

    def execute(self, context):
        arm = context.object
        act_sel_set = arm.blenrig_selection_sets[arm.blenrig_active_selection_set]

        # iterate only the selected bones in current pose that are not hidden
        for bone in context.selected_pose_bones:
            if bone.name not in act_sel_set.bone_ids:
                bone_id = act_sel_set.bone_ids.add()
                bone_id.name = bone.name

        return {'FINISHED'}


class BLENRIG_OT_selection_set_unassign(NeedSelSetPluginOperator):
    bl_idname = "blenrig.selection_set_unassign"
    bl_label = "Remove Bones from Selection Set"
    bl_description = "Remove selected bones from Selection Set"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        act_sel_set = arm.blenrig_selection_sets[arm.blenrig_active_selection_set]

        # iterate only the selected bones in current pose that are not hidden
        for bone in context.selected_pose_bones:
            if bone.name in act_sel_set.bone_ids:
                idx = act_sel_set.bone_ids.find(bone.name)
                act_sel_set.bone_ids.remove(idx)

        return {'FINISHED'}


class BLENRIG_OT_selection_set_select(NeedSelSetPluginOperator):
    bl_idname = "blenrig.selection_set_select"
    bl_label = "Select Selection Set"
    bl_description = "Add Selection Set bones to current selection"
    bl_options = {'UNDO', 'REGISTER'}

    selection_set_index: IntProperty(
        name='Selection Set Index',
        default=-1,
        description='Which Selection Set to select; -1 uses the active Selection Set',
        options={'HIDDEN'},
    )

    def execute(self, context):
        arm = context.object

        bpy.ops.pose.reveal()
        # bpy.ops.pose.select_all(action='DESELECT')

        if self.selection_set_index == -1:
            idx = arm.blenrig_active_selection_set
        else:
            idx = self.selection_set_index

        sel_set = arm.blenrig_selection_sets[idx]

        for bone in context.visible_pose_bones:
            if bone.name in sel_set.bone_ids:
                bone.bone.select = True

        # bpy.ops.pose.hide(unselected=True)

        return {'FINISHED'}


class BLENRIG_OT_selection_set_deselect(NeedSelSetPluginOperator):
    bl_idname = "blenrig.selection_set_deselect"
    bl_label = "Deselect Selection Set"
    bl_description = "Remove Selection Set bones from current selection"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        arm = context.object
        act_sel_set = arm.blenrig_selection_sets[arm.blenrig_active_selection_set]

        for bone in context.selected_pose_bones:
            if bone.name in act_sel_set.bone_ids:
                bone.bone.select = False

        return {'FINISHED'}


class BLENRIG_OT_selection_set_add_and_assign(PluginOperator):
    bl_idname = "blenrig.selection_set_add_and_assign"
    bl_label = "Create and Add Bones to Selection Set"
    bl_description = "Creates a new Selection Set with the currently selected bones"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        bpy.ops.blenrig.selection_set_add('EXEC_DEFAULT')
        bpy.ops.blenrig.selection_set_assign('EXEC_DEFAULT')
        return {'FINISHED'}


class BLENRIG_OT_selection_set_copy(NeedSelSetPluginOperator):
    bl_idname = "blenrig.selection_set_copy"
    bl_label = "Copy Selection Set(s)"
    bl_description = "Copies the selected Selection Set(s) to the clipboard"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        context.window_manager.clipboard = to_json(context)
        self.report({'INFO'}, 'Copied Selection Set(s) to Clipboard')
        return {'FINISHED'}


class BLENRIG_OT_selection_set_paste(PluginOperator):
    bl_idname = "blenrig.selection_set_paste"
    bl_label = "Paste Selection Set(s)"
    bl_description = "Adds new Selection Set(s) from the Clipboard"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        import json

        try:
            from_json(context, context.window_manager.clipboard)
        except (json.JSONDecodeError, KeyError):
            self.report({'ERROR'}, 'The clipboard does not contain a Selection Set')
        else:
            # Select the pasted Selection Set.
            context.object.blenrig_active_selection_set = len(context.object.blenrig_selection_sets) - 1

        return {'FINISHED'}


# Helper Functions ############################################################

def menu_func_select_selection_set(self, context):
    self.layout.menu('BLENRIG_MT_selection_sets_select', text="Bone Selection Set")


def to_json(context) -> str:
    """Convert the selected Selection Sets of the current rig to JSON.

    Selected Sets are the blenrig_active_selection_set determined by the UIList
    plus any with the is_selected checkbox on."""
    import json

    arm = context.object
    active_idx = arm.blenrig_active_selection_set

    json_obj = {}
    for idx, sel_set in enumerate(context.object.blenrig_selection_sets):
        if idx == active_idx or sel_set.is_selected:
            bones = [bone_id.name for bone_id in sel_set.bone_ids]
            json_obj[sel_set.name] = bones

    return json.dumps(json_obj)


def from_json(context, as_json: str):
    """Add the selection sets (one or more) from JSON to the current rig."""
    import json

    json_obj = json.loads(as_json)
    arm_sel_sets = context.object.blenrig_selection_sets

    for name, bones in json_obj.items():
        new_sel_set = arm_sel_sets.add()
        new_sel_set.name = uniqify(name, arm_sel_sets.keys())
        for bone_name in bones:
            bone_id = new_sel_set.bone_ids.add()
            bone_id.name = bone_name


def uniqify(name: str, other_names: list) -> str:
    """Return a unique name with .xxx suffix if necessary.

    Example usage:

    >>> uniqify('hey', ['there'])
    'hey'
    >>> uniqify('hey', ['hey.001', 'hey.005'])
    'hey'
    >>> uniqify('hey', ['hey', 'hey.001', 'hey.005'])
    'hey.002'
    >>> uniqify('hey', ['hey', 'hey.005', 'hey.001'])
    'hey.002'
    >>> uniqify('hey', ['hey', 'hey.005', 'hey.001', 'hey.left'])
    'hey.002'
    >>> uniqify('hey', ['hey', 'hey.001', 'hey.002'])
    'hey.003'

    It also works with a dict_keys object:
    >>> uniqify('hey', {'hey': 1, 'hey.005': 1, 'hey.001': 1}.keys())
    'hey.002'
    """

    if name not in other_names:
        return name

    # Construct the list of numbers already in use.
    offset = len(name) + 1
    others = (n[offset:] for n in other_names
              if n.startswith(name + '.'))
    numbers = sorted(int(suffix) for suffix in others
                     if suffix.isdigit())

    # Find the first unused number.
    min_index = 1
    for num in numbers:
        if min_index < num:
            break
        min_index = num + 1
    return "{}.{:03d}".format(name, min_index)

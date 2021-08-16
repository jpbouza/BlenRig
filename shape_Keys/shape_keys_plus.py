import bpy
import bl_ui
import re


########################################################################
############################### CLASSES ################################
########################################################################

class Selection(bpy.types.PropertyGroup):
    value : bpy.props.BoolProperty()


class KeyProperties(bpy.types.PropertyGroup):
    selections : bpy.props.CollectionProperty(type=Selection)


class SceneProperties(bpy.types.PropertyGroup):
    shape_key_add_placement : \
        bpy.props.EnumProperty(
            name="Add Shape Placement",
            items=(
                ('TOP', "Top",
                 ("Place new shape keys at the top of the list."),
                 'TRIA_UP_BAR', 0),
                ('ABOVE', "Above",
                 ("Place new shape keys below the active key."),
                 'TRIA_UP', 1),
                ('BELOW', "Below",
                 ("Place new shape keys under the active key."),
                 'TRIA_DOWN', 2),
                ('BOTTOM', "Bottom",
                 ("Place new shape keys at the bottom of the list."),
                 'TRIA_DOWN_BAR', 3)
            ),
            default='BELOW')

    shape_key_parent_placement : \
        bpy.props.EnumProperty(
            name="Parenting Placement",
            items=(
                ('TOP', "Top",
                 ("Place newly parented shape keys "
                  "at the top of the list."),
                 'TRIA_UP_BAR', 0),
                ('BOTTOM', "Bottom",
                 ("Place newly parented shape keys "
                  "at the bottom of the list."),
                 'TRIA_DOWN_BAR', 1)
            ),
            default='BOTTOM')

    shape_key_unparent_placement : \
        bpy.props.EnumProperty(
            name="Unparenting Placement",
            items=(
                ('TOP', "Top",
                 ("Place unparented shape keys at "
                  "the top of the new directory."),
                 'TRIA_UP_BAR', 0),
                ('ABOVE', "Above",
                 ("Place unparented shape keys above the folder."),
                 'TRIA_UP', 1),
                ('BELOW', "Below",
                 ("Place unparented shape keys below the folder."),
                 'TRIA_DOWN', 2),
                ('BOTTOM', "Bottom",
                 ("Place unparented shape keys at the bottom of the new directory."),
                 'TRIA_DOWN_BAR', 3)
            ),
            default='ABOVE')

    shape_key_auto_parent : \
        bpy.props.BoolProperty(
            name="Auto Parent",
            description="Automatically parent new shapes to the active folder",
            default=True)

    shape_key_indent_scale : \
        bpy.props.IntProperty(
            name="Indentation",
            description="Indentation of folder contents",
            min=0,
            max=8,
            default=4)

    folder_icon_pair : \
        bpy.props.IntProperty(
            default=0)

    folder_icon_swap : \
        bpy.props.BoolProperty(
            default=False)

    driver_visible : \
        bpy.props.BoolProperty(
            name="Show Driver",
            default=True)

    show_filtered_folder_contents : \
        bpy.props.BoolProperty(
            name="Show Filtered Folder Contents",
            description="Show contents of a folder that is being filtered, even if its contents don't match the filter",
            default=True)

    shape_key_limit_to_active : \
        bpy.props.BoolProperty(
            name="Show Active Shapes Only",
            description="Only show shape keys with a value above a certain threshold",
            default=False)

    filter_active_threshold : \
        bpy.props.FloatProperty(
            name="Active Threshold",
            description="Only show shape keys above this value",
            soft_min = 0.0,
            soft_max = 1.0,
            default = 0.001,
            step=1,
            precision=3)

    filter_active_below : \
        bpy.props.BoolProperty(
            name="Flip Active Threshold",
            description="Only show values lower than the threshold instead of higher",
            default=False)


########################################################################
############################### UTILITY ################################
########################################################################


class utils:
    prefix = "SKP"
    folder = ".F"
    children = ".C"
    expand = ".E"
    icons = ".I"
    icons_swap = ".IS"

    # Value that will be given to all children as the parent count.
    folder_default = 1
    # Number of shape keys under the folder.
    children_default = 0
    # 0 = collapse, 1 = expand
    expand_default = 1
    # Block for whether or not a folder has its icon pair reversed.
    # 0 = normal, 1 = swap
    icons_swap_default = 0

    icon_pairs_standard = (
        ('DISCLOSURE_TRI_DOWN', 'DISCLOSURE_TRI_RIGHT', "Outliner", "", 0),
        ('TRIA_DOWN', 'TRIA_RIGHT', "Bold", "", 1),
        ('DOWNARROW_HLT', 'RIGHTARROW', "Wire", "", 2),
        ('SORT_ASC', 'FORWARD', "Arrow", "", 3),
        ('LAYER_ACTIVE', 'LAYER_USED', "Small", "", 4),
        ('RADIOBUT_ON', 'RADIOBUT_OFF', "Big", "", 5),
        ('DOT', 'REC', "Pulsar", "", 6),
    )

    icon_pairs_special = (
        ('KEY_DEHLT', 'KEY_HLT', "Polarity", "", 7),
        ('KEYFRAME_HLT', 'KEYFRAME', "Keyframe", "", 8),
        ('MARKER_HLT', 'MARKER', "Marker", "", 9),
        ('PMARKER_ACT', 'PMARKER_SEL', "Diamond", "", 10),
        ('SOLO_ON', 'SOLO_OFF', "Star", "", 11),
        ('CHECKBOX_HLT', 'CHECKBOX_DEHLT', "Checkbox", "", 12),
    )

    icon_pairs_misc = (
        ('PINNED', 'UNPINNED', "Pin", "", 12),
        ('PROP_ON', 'PROP_OFF', "Proportional", "", 13),
        ('ZOOM_OUT', 'ZOOM_IN', "Magnifier", "", 14),
        ('MESH_PLANE', 'SHADING_BBOX', "Continuity", "", 15),
        ('DECORATE_UNLOCKED', 'DECORATE_LOCKED', "Lock", "", 16),
        ('RESTRICT_COLOR_ON', 'RESTRICT_COLOR_OFF', "Tabs", "", 17),
        ('HIDE_OFF', 'HIDE_ON', "Eye", "", 18),
        ('RESTRICT_SELECT_OFF', 'RESTRICT_SELECT_ON', "Cursor", "", 19),
        ('RESTRICT_VIEW_OFF', 'RESTRICT_VIEW_ON', "Monitor", "", 20),
        ('RESTRICT_RENDER_OFF', 'RESTRICT_RENDER_ON', "Camera", "", 21),
        ('MODIFIER_ON', 'MODIFIER_OFF', "Modifier", "", 22),
        ('MUTE_IPO_ON', 'MUTE_IPO_OFF', "Mute", "", 23),
        ('SMOOTHCURVE', 'SPHERECURVE', "Squeeze", "", 24),
        ('SHARPCURVE', 'ROOTCURVE', "Pinch", "", 25),
        ('SNAP_ON', 'SNAP_OFF', "Magnet", "", 26),
        ('FREEZE', 'MATFLUID', "Precipitation", "", 27),
        ('ALIGN_TOP', 'ALIGN_BOTTOM', "Switch", "", 28),
        ('TEXT', 'ASSET_MANAGER', "Good Read", "", 29)
    )

    icon_pairs = \
        icon_pairs_standard[:] + \
        icon_pairs_special[:] + \
        icon_pairs_misc[:]

    cache = {
        'pointers' : [],
        'parents' : [],
        'children' : []
    }

    @classmethod
    def update_cache(cls, override=False):
        obj = bpy.context.object

        if obj:
            shape_keys = obj.data.shape_keys

            if shape_keys:
                key_blocks = shape_keys.key_blocks
                keys = [kb.as_pointer() for kb in key_blocks]

                if cls.cache['pointers'] != keys or override:
                    cls.cache['pointers'] = keys
                    cls.cache['parents'].clear()
                    cls.cache['children'].clear()

                    for kb in key_blocks:
                        parents = cls.get_key_parents(kb)
                        children = cls.get_folder_children(kb)

                        cls.cache['parents'].append(parents)
                        cls.cache['children'].append(children)

        return cls.cache

    @classmethod
    def create_folder_data(cls,
                           folder=folder_default,
                           children=children_default,
                           expand=expand_default,
                           icons=None,
                           icons_swap=icons_swap_default):

        skp = bpy.context.scene.shape_keys_plus

        if folder is None:
            folder = folder_default
        if children is None:
            children = children_default
        if expand is None:
            expand = expand_default
        if icons is None:
            icons = skp.folder_icon_pair
        if icons_swap is None:
            icons_swap = icons_swap_default

        prefix = cls.prefix
        folder = cls.folder + str(folder)
        children = cls.children + str(children)
        expand = cls.expand + str(expand)
        icons = cls.icons + str(icons)
        icons_swap = cls.icons_swap + str(icons_swap)

        return prefix + folder + children + expand + icons + icons_swap

    @classmethod
    def get_block(cls, data, block=None):
        if data.startswith(cls.prefix):
            if block is None:
                return data.split(".")
            else:
                data = data.split(".")
                block = re.sub(r"[^A-Za-z]", "", block)

                for x in data:
                    if block in x:
                        return x

        return None

    @classmethod
    def has_block(cls, data, block):
        return cls.get_block(data, block) is not None

    @classmethod
    def block_index(cls, data, block):
        data = data.split(".")
        block = re.sub(r"[^A-Za-z]", "", block)

        for i, x in enumerate(data):
            if block in x:
                return i

    @classmethod
    def block_set(cls, data, block, value):
        if cls.has_block(data, block):
            original = cls.get_block(data, block)
            key = re.sub(r"[^A-Za-z]", "", original)

            split = data.split(".")
            index = cls.block_index(data, block)

            split[index] = key + str(value)

            return ".".join(split)

        return data

    @classmethod
    def block_value(cls, data, block):
        skp = bpy.context.scene.shape_keys_plus

        if cls.has_block(data, block):
            default = None

            if block == cls.folder:
                default = cls.folder_default
            elif block == cls.children:
                default = cls.children_default
            elif block == cls.expand:
                default = cls.expand_default
            elif block == cls.icons:
                default = skp.folder_icon_pair
            elif block == cls.icons_swap:
                default = cls.icons_swap_default

            if default is not None:
                value = re.sub(r"\D", "", cls.get_block(data, block))

                if value != "":
                    return int(value)
                else:
                    return default

        return -1

    @classmethod
    def is_key_folder(cls, key):
        return cls.has_block(key.vertex_group, cls.folder)

    @classmethod
    def is_key_child_of(cls, key, folder):
        return key.name in [c.name for c in cls.get_folder_children(folder)]

    @classmethod
    def get_icon_pair(cls, id, d=0):
        return next((p for p in cls.icon_pairs if p[-1] == id), cls.icon_pairs[d])

    @classmethod
    def get_folder_capacity(cls, folder):
        capacity = 0

        context = bpy.context

        if cls.is_key_folder(folder):
            shape_keys = context.object.data.shape_keys
            folder_index = cls.get_key_index(folder)

            s = folder_index + 1
            e = s + cls.get_folder_children_value(folder)

            i = s

            while i < e:
                if len(shape_keys.key_blocks) > i:
                    key = shape_keys.key_blocks[i]

                    capacity += 1

                    if cls.is_key_folder(key):
                        e += cls.get_folder_children_value(key)

                    i += 1

        return capacity

    @classmethod
    def get_folder_children(cls, folder):
        children = []

        context = bpy.context

        if cls.is_key_folder(folder):
            shape_keys = context.object.data.shape_keys
            folder_index = shape_keys.key_blocks.find(folder.name)
            index = folder_index + 1
            capacity = cls.get_folder_capacity(folder)

            for i in range(index, index + capacity):
                if len(shape_keys.key_blocks) > i:
                    children.append(shape_keys.key_blocks[i])

        return children

    @classmethod
    def get_key_parent(cls, key):
        context = bpy.context

        if key:
            shape_keys = context.object.data.shape_keys
            index = cls.get_key_index(key)
            i = index - 1

            while i >= 0:
                key = shape_keys.key_blocks[i]
                is_folder = cls.is_key_folder(key)
                capacity = cls.get_folder_capacity(key)

                if is_folder and capacity > 0:
                    if i <= index <= i + capacity:
                        return key

                i -= 1

        return None

    @classmethod
    def get_key_parents(cls, key):
        context = bpy.context

        parents = []

        if key:
            shape_keys = context.object.data.shape_keys
            index = cls.get_key_index(key)
            i = index - 1

            while i >= 0:
                key = shape_keys.key_blocks[i]
                is_folder = cls.is_key_folder(key)
                capacity = cls.get_folder_capacity(key)

                if is_folder and capacity > 0:
                    if i <= index <= i + capacity:
                        parents.append(key)

                        if cls.get_folder_stack_value(key) < 2:
                            break

                i -= 1

        return parents

    @classmethod
    def get_key_index(cls, key):
        context = bpy.context
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if shape_keys and shape_keys.key_blocks:
            return shape_keys.key_blocks.find(key.name)

        return -1

    @classmethod
    def get_key_siblings(cls, key):
        siblings = [None, None]

        context = bpy.context
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        parents = cls.get_key_parents(key)
        parent = get(parents, 0)
        index = cls.get_key_index(key)
        capacity = cls.get_folder_capacity(key)

        previous_index = index - 1
        next_index = index + capacity + 1

        ###########################
        ######## NEIGHBORS ########
        ###########################

        # Get references to the keys in the immediate proximity.
        if previous_index >= 0:
            previous_key = key_blocks[previous_index]
        else:
            previous_key = None

        if next_index < len(key_blocks):
            next_key = key_blocks[next_index]
        else:
            next_key = None

        ###############################
        ######## OLDER SIBLING ########
        ###############################

        # Find out whether or not those keys are siblings to this key.
        if previous_key:
            previous_key_parents = cls.get_key_parents(previous_key)

            if len(previous_key_parents) > 0:
                previous_key_parent = previous_key_parents[0]
            else:
                previous_key_parent = None

            if parent:
                if previous_key_parent:
                    if previous_key_parent.name == parent.name:
                        # Two keys with the same parent are siblings.
                        siblings[0] = previous_key
                    elif previous_key.name != parent.name:
                        # If the previous key's parent is not the
                        # current key's parent, the sibling key
                        # is the parent of the previous key.
                        offset = len(previous_key_parents) - len(parents) - 1

                        siblings[0] = previous_key_parents[offset]
            else:
                if previous_key_parent:
                    # If the current key has no parent but the previous
                    # key does, this key's sibling is that key's parent.
                    siblings[0] = previous_key_parents[-1]
                else:
                    # If neither of these neighboring keys
                    # have any parents, they are siblings.
                    siblings[0] = previous_key

        #################################
        ######## YOUNGER SIBLING ########
        #################################

        if next_key:
            next_key_parents = cls.get_key_parents(next_key)

            if len(next_key_parents) > 0:
                next_key_parent = next_key_parents[0]
            else:
                next_key_parent = None

            if parent:
                if next_key_parent:
                    if next_key_parent.name == parent.name:
                        # Two keys with the same parent are siblings.
                        siblings[1] = next_key
            else:
                if next_key_parent:
                    # It's not possible for the next key to have
                    # a parent if the current key doesn't have any.
                    pass
                else:
                    siblings[1] = next_key

        return siblings

    @classmethod
    def shift_folder_children_value(cls, key, amount):
        if cls.has_block(key.vertex_group, cls.children):
            destination = cls.block_value(key.vertex_group, cls.children) + amount
            key.vertex_group = cls.block_set(key.vertex_group, cls.children, max(0, destination))

    @classmethod
    def shift_folder_stack_value(cls, key, amount):
        if cls.has_block(key.vertex_group, cls.folder):
            destination = cls.block_value(key.vertex_group, cls.folder) + amount
            key.vertex_group = cls.block_set(key.vertex_group, cls.folder, max(1, destination))

    @classmethod
    def set_folder_children_value(cls, key, val):
        if cls.has_block(key.vertex_group, cls.folder):
            key.vertex_group = cls.block_set(key.vertex_group, cls.children, val)

    @classmethod
    def set_folder_stack_value(cls, key, val):
        if cls.has_block(key.vertex_group, cls.folder):
            key.vertex_group = cls.block_set(key.vertex_group, cls.folder, val)

    @classmethod
    def get_folder_children_value(cls, key):
        return cls.block_value(key.vertex_group, cls.children)

    @classmethod
    def get_folder_stack_value(cls, key):
        return cls.block_value(key.vertex_group, cls.folder)

    @classmethod
    def toggle_folder(cls, key, expand=None):
        if cls.is_key_folder(key):
            original = cls.block_value(key.vertex_group, cls.expand)

            if expand is None:
                toggle = 1 if original == 0 else 0
            else:
                toggle = 1 if expand else 0

            key.vertex_group = cls.block_set(key.vertex_group, cls.expand, toggle)

    @classmethod
    def get_key_driver(cls, shape_keys, key):
        anim = shape_keys.animation_data
        data_path = "key_blocks[\"" + key.name + "\"].value"

        if anim and anim.drivers:
            for fcu in anim.drivers:
                if fcu.data_path == data_path:
                    return fcu.driver

        return None

    @classmethod
    def update_driver(cls, driver):
        if driver:
            driver.expression += " "
            driver.expression = driver.expression[:-1]

    @classmethod
    def reconstruct_driver_variables(cls, driver, source):
        data = []

        for var in source:
            data.append({
                'name' : var.name,
                'type' : var.type,
                'targets' : [{
                    'id' : target.id,
                    'id_type' : target.id_type,
                    'data_path' : target.data_path,
                    'bone_target' : target.bone_target,
                    'transform_type' : target.transform_type,
                    'transform_space' : target.transform_space
                } for j, target in enumerate(var.targets)]
            })

        while driver.variables:
            driver.variables.remove(driver.variables[0])

        for i in range(len(source)):
            new_var = driver.variables.new()
            new_var.name = data[i]['name']

            # The type controls the targets, so this comes first.
            new_var.type = data[i]['type']

            for j, old_target in enumerate(data[i]['targets']):
                new_target = new_var.targets[j]
                new_target.id = old_target['id']

                # Only the "Single Property" type can have its id_type changed.
                if new_var.type == 'SINGLE_PROP':
                    new_target.id_type = old_target['id_type']

                new_target.data_path = old_target['data_path']
                new_target.bone_target = old_target['bone_target']
                new_target.transform_type = old_target['transform_type']
                new_target.transform_space = old_target['transform_space']

        cls.update_driver(driver)

    @classmethod
    def shape_key_selected(cls, index):
        context = bpy.context
        obj = context.object
        shape_keys = obj.data.shape_keys

        if not shape_keys:
            return False

        return str(index) in shape_keys.shape_keys_plus.selections

    @classmethod
    def selected_shape_key_indices(cls):
        context = bpy.context
        obj = context.object
        shape_keys = obj.data.shape_keys

        indices = []

        if not shape_keys:
            return indices

        selections = shape_keys.shape_keys_plus.selections

        for i, x in enumerate(selections):
            if x.name.isdigit():
                indices.append(int(x.name))

        return sorted(indices)

    @classmethod
    def selected_shape_keys(cls):
        context = bpy.context
        obj = context.object
        shape_keys = obj.data.shape_keys

        keys = []

        if not shape_keys:
            return keys

        indices = cls.selected_shape_key_indices()

        for index in indices:
            keys.append(shape_keys.key_blocks[index])

        return keys

    @classmethod
    def shape_key_move_to(cls, origin, destination):
        context = bpy.context
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        obj.active_shape_key_index = origin

        active_key = obj.active_shape_key
        active_capacity = cls.get_folder_capacity(active_key)

        direction = 'UP' if destination < origin else 'DOWN'

        offset = origin + active_capacity + 1

        if direction == 'UP':
            move_range = range(origin, destination, -1)
        else:
            move_range = range(origin, destination)

        inc = 0

        for i in move_range:
            if direction == 'UP':
                block_range = range(origin + inc, offset + inc)
            else:
                block_range = reversed(range(origin + inc, offset + inc))

            for j in block_range:
                obj.active_shape_key_index = j
                bpy.ops.object.shape_key_move(type=direction)

            inc += -1 if direction == 'UP' else 1

        is_folder = active_capacity > 0

        if is_folder:
            # Re-selects the folder after moving its children.
            obj.active_shape_key_index = origin + inc

    @classmethod
    def apply_add_placement(cls, key, ref):
        context = bpy.context
        skp = context.scene.shape_keys_plus
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        basis_capacity = cls.get_folder_capacity(key_blocks[0])

        key_index = cls.get_key_index(key)
        ref_index = cls.get_key_index(ref)

        is_ref_folder = cls.is_key_folder(ref)

        ref_capacity = cls.get_folder_capacity(ref)
        ref_parents = cls.get_key_parents(ref)
        ref_parent = get(ref_parents, 0)

        auto_parent = skp.shape_key_auto_parent and ref_parent
        mode = skp.shape_key_add_placement

        if ref_parent:
            ref_parent_index = cls.get_key_index(ref_parent)
            ref_parent_capacity = cls.get_folder_capacity(ref_parent)

        # The reference key's highest and lowest-level parents if they exist, otherwise the reference key itself.
        ref_inner = get(ref_parents, 0, ref)
        ref_inner_index = cls.get_key_index(ref_inner)
        ref_inner_capacity = cls.get_folder_capacity(ref_inner)

        ref_outer = get(ref_parents, -1, ref)
        ref_outer_index = cls.get_key_index(ref_outer)
        ref_outer_capacity = cls.get_folder_capacity(ref_outer)

        if mode == 'TOP':
            if auto_parent:
                placement = ref_inner_index + 1
            else:
                if ref_outer_index == 0:
                    placement = 0
                else:
                    placement = basis_capacity + 1
        elif mode == 'ABOVE':
            if auto_parent:
                placement = ref_index
            else:
                placement = ref_outer_index
        elif mode == 'BELOW':
            if auto_parent:
                placement = ref_index + ref_capacity + 1
            else:
                placement = ref_outer_index + ref_outer_capacity + 1
        elif mode == 'BOTTOM':
            if auto_parent:
                placement = ref_inner_index + ref_inner_capacity
            else:
                placement = key_index

        cls.shape_key_move_to(key_index, placement)

    @classmethod
    def apply_copy_placement(cls, copy, original):
        context = bpy.context

        skp = context.scene.shape_keys_plus

        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        basis_capacity = cls.get_folder_capacity(key_blocks[0])

        copy_index = key_blocks.find(copy.name)
        original_index = key_blocks.find(original.name)

        is_original_folder = cls.is_key_folder(original)

        original_capacity = cls.get_folder_capacity(original)
        original_parents = cls.get_key_parents(original)
        original_parent = get(original_parents, 0)

        auto_parent = skp.shape_key_auto_parent and original_parent
        mode = skp.shape_key_add_placement

        if original_parent:
            original_parent_index = cls.get_key_index(original_parent)
            original_parent_capacity = cls.get_folder_capacity(original_parent)

        original_inner = get(original_parents, 0, original)
        original_inner_index = cls.get_key_index(original_inner)
        original_inner_capacity = cls.get_folder_capacity(original_inner)

        # The original key's lowest-level parent if it exists, otherwise the original key itself.
        original_outer = get(original_parents, -1, original)
        original_outer_index = cls.get_key_index(original_outer)
        original_outer_capacity = cls.get_folder_capacity(original_outer)

        if mode == 'TOP':
            if auto_parent:
                placement = original_inner_index + 1
            else:
                if original_outer_index == 0:
                    placement = 0
                else:
                    placement = basis_capacity + 1
        elif mode == 'ABOVE':
            if auto_parent:
                placement = original_index
            else:
                placement = original_outer_index
        elif mode == 'BELOW':
            if auto_parent:
                placement = original_index + original_capacity + 1
            else:
                placement = original_outer_index + original_outer_capacity + 1
        elif mode == 'BOTTOM':
            if auto_parent:
                # Add 1 because the copy is an additional child.
                placement = original_inner_index + original_inner_capacity + 1
            else:
                placement = copy_index

        cls.shape_key_move_to(copy_index, placement)

    @classmethod
    def apply_parent_placement(cls, key, parent):
        context = bpy.context
        skp = context.scene.shape_keys_plus
        obj = context.object

        key_index = cls.get_key_index(key)
        parent_index = cls.get_key_index(parent)

        key_capacity = cls.get_folder_capacity(key)

        # A replica of the parent's capacity after it is shifted.
        parent_capacity = cls.get_folder_capacity(parent) + cls.get_folder_capacity(key) + 1

        mode = skp.shape_key_parent_placement

        if mode == 'TOP':
            placement = parent_index + 1
        elif mode == 'BOTTOM':
            placement = parent_index + parent_capacity - key_capacity

        # Account for the shifting of indices after the key is moved.
        placement += (-1 - key_capacity) if placement > key_index else 0

        cls.shape_key_move_to(key_index, placement)

    @classmethod
    def apply_unparent_placement(cls, key, clear):
        context = bpy.context
        skp = context.scene.shape_keys_plus
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        key_index = cls.get_key_index(key)
        key_capacity = cls.get_folder_capacity(key)

        basis_capacity = cls.get_folder_capacity(key_blocks[0])

        parents = cls.get_key_parents(key)
        parent = parents[0]
        outer_parent = parents[-1]
        grandparent = get(parents, 1)

        parent_index = cls.get_key_index(parent)
        parent_capacity = cls.get_folder_capacity(parent)

        outer_parent_index = cls.get_key_index(outer_parent)
        outer_parent_capacity = cls.get_folder_capacity(outer_parent)

        if grandparent:
            grandparent_index = cls.get_key_index(grandparent)
            grandparent_capacity = cls.get_folder_capacity(grandparent)

        mode = skp.shape_key_unparent_placement

        if mode == 'TOP':
            if clear:
                if outer_parent_index == 0:
                    placement = 0
                else:
                    placement = basis_capacity + 1
            else:
                if grandparent:
                    placement = grandparent_index + 1
                else:
                    if parent_index == 0:
                        placement = 0
                    else:
                        placement = 1
        elif mode == 'ABOVE':
            if clear:
                placement = outer_parent_index
            else:
                placement = parent_index
        elif mode == 'BELOW':
            if clear:
                placement = outer_parent_index + outer_parent_capacity + 1
            else:
                placement = parent_index + parent_capacity + 1
        elif mode == 'BOTTOM':
            if clear:
                placement = len(key_blocks)
            else:
                if grandparent:
                    placement = grandparent_index + grandparent_capacity + 1
                else:
                    # + 1 doesn't need to be added because the length of key_blocks is already 1 extra.
                    placement = len(key_blocks)

        # Account for the shifting of indices after the key is moved.
        placement += (-1 - key_capacity) if placement > key_index else 0

        cls.shape_key_move_to(key_index, placement)


class Metadata:
    key = None
    index = 0

    parents = []
    children = []
    family = []
    is_folder = False
    stack = 0
    is_parented = False
    first_parent = None
    last_parent = None
    capacity = 0
    has_children = False
    first_child = None
    last_child = None
    first_child_index = 0
    last_child_index = 0
    is_first_child = False
    is_last_child = False
    previous_key = None
    next_key = None

    def __init__(self, key, index):
        context = bpy.context
        obj = context.object

        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        self.key = key
        self.index = index

        self.parents = utils.get_key_parents(self.key)
        self.children = utils.get_folder_children(self.key)
        self.is_folder = utils.is_key_folder(self.key)
        self.stack = len(self.parents)
        self.is_parented = self.stack > 0

        if self.is_parented:
            self.first_parent = self.parents[0]
            self.last_parent = self.parents[-1]

            self.siblings = utils.get_folder_children(self.first_parent)
        else:
            self.siblings = key_blocks

        self.capacity = len(self.children)
        self.has_children = self.capacity > 0

        if self.has_children:
            self.first_child = self.children[0]
            self.last_child = self.children[-1]

            self.first_child_index = key_blocks.find(self.first_child.name)
            self.last_child_index = key_blocks.find(self.last_child.name)

        self.is_first_child = self.key.name == self.siblings[0].name
        self.is_last_child = self.key.name == self.siblings[-1].name

        if index > 0:
            self.previous_key = key_blocks[index - 1]
        else:
            self.previous_key = None

        next_index = index + self.capacity + 1

        if len(key_blocks) > next_index:
            self.next_key = key_blocks[next_index]
        else:
            self.next_key = None

    def __eq__(self, other):
        if hasattr(self, 'key') and hasattr(other, 'key'):
            return self.key.name == other.key.name

        return False

    def __ne__(self, other):
        return not self == other

    def print_data(self):
        print("Key:", self.key.name)
        print("Index:", self.index)
        print("Parent:", self.parents[0].name if self.is_parented else "None")
        print("Is Folder:", self.is_folder)
        print("Children:", self.capacity if self.has_children else "None")

        for c in self.children:
            t = " "

            for x in utils.get_key_parents(c):
                t += " "

            print(t + c.name)

        print("\n")


class Debug:
    @classmethod
    def print_skp_data(cls):
        data = skp_data()

        for d in data:
            d.print_data()


def get(l, i, d=None):
    """Returns the value of l[i] if possible, otherwise d."""

    if type(l) in (dict, set):
        return l[i] if i in l else d

    try:
        return l[i]
    except (IndexError, KeyError, TypeError):
        return d


def evaluate():
    data = []

    context = bpy.context
    obj = context.object
    key_blocks = obj.data.shape_keys.key_blocks

    for index, key in enumerate(key_blocks):
        data.append(Metadata(key=key, index=index))

    return data


def metadata(data, key):
    m = None

    for d in data:
        if d.key.name == key.name:
            m = d
            break

    return m

def hide_modifiers(obj):
    values = []

    for modifier in obj.modifiers:
        values.append(modifier.show_viewport)
        modifier.show_viewport = False

    return obj, values

def show_modifiers(data):
    obj, values = data

    for i, modifier in enumerate(obj.modifiers):
        modifier.show_viewport = values[i]

def shape_key_parent(key, parent, sibling=None):
    if key.name == parent.name:
        return

    key_parent = utils.get_key_parent(key)

    if key_parent:
        utils.shift_folder_children_value(key_parent, -1)

    context = bpy.context
    obj = context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks

    # The folder should be open if something is being added to it.
    utils.toggle_folder(parent, True)

    if sibling:
        # The sibling is the currently active key during auto parent, if it's not a folder.
        utils.shift_folder_children_value(parent, 1)
        utils.apply_add_placement(key, sibling)
    else:
        utils.apply_parent_placement(key, parent)
        utils.shift_folder_children_value(parent, 1)

    if utils.is_key_folder(key):
        children = utils.get_folder_children(key)

        old_stack = utils.get_folder_stack_value(key)
        new_stack = utils.get_folder_stack_value(parent)

        # Add 1 because the new key will be a child of the new stack.
        stack_offset = (new_stack - old_stack) + 1

        utils.shift_folder_stack_value(key, stack_offset)

        for c in children:
            if utils.is_key_folder(c):
                utils.shift_folder_stack_value(c, stack_offset)


def shape_key_unparent(key, clear=False):
    parents = utils.get_key_parents(key)
    children = utils.get_folder_children(key)

    if not parents:
        return

    first_parent = parents[0]
    second_parent = get(parents, 1)
    last_parent = parents[-1]

    key_index = utils.get_key_index(key)
    key_capacity = utils.get_folder_capacity(key)

    is_key_folder = utils.is_key_folder(key)

    first_parent_index = utils.get_key_index(first_parent)
    last_parent_index = utils.get_key_index(last_parent)

    first_parent_capacity = utils.get_folder_capacity(first_parent)
    last_parent_capacity = utils.get_folder_capacity(last_parent)

    utils.apply_unparent_placement(key, clear)
    utils.shift_folder_children_value(first_parent, -1)

    if clear:
        if is_key_folder:
            old_stack = utils.get_folder_stack_value(key)

            utils.set_folder_stack_value(key, 1)

            for c in children:
                if not utils.is_key_folder(c):
                    continue

                stack_offset = utils.get_folder_stack_value(c) - old_stack

                utils.set_folder_stack_value(c, 1 + stack_offset)
    else:
        if second_parent:
            utils.shift_folder_children_value(second_parent, 1)

        if is_key_folder:
            utils.shift_folder_stack_value(key, -1)

            for c in children:
                if not utils.is_key_folder(c):
                    continue

                utils.shift_folder_stack_value(c, -1)


def shape_key_add(type='DEFAULT'):
    context = bpy.context
    skp = context.scene.shape_keys_plus
    obj = context.object
    active_key = obj.active_shape_key
    active_index = obj.active_shape_key_index
    active_parent = utils.get_key_parent(active_key)

    # Shape Key Creation
    if type == 'FROM_MIX':
        new_key = obj.shape_key_add(from_mix=True)
    elif type == 'FROM_MIX_SELECTED':
        selected = []

        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        for i, key in enumerate(key_blocks):
            if not utils.shape_key_selected(i):
                if not key.mute:
                    key.mute = True
                    selected.append(i)

        new_key = obj.shape_key_add(from_mix=True)

        for i in selected:
            key_blocks[i].mute = False

        shape_keys.shape_keys_plus.selections.clear()
    else:
        new_key = obj.shape_key_add(from_mix=False)

    # Shape Key Naming
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    new_index = len(key_blocks) - 1
    obj.active_shape_key_index = new_index

    if type in ('FOLDER', 'PARENT'):
        folder_count = 1

        for key in key_blocks:
            if utils.is_key_folder(key):
                folder_count += 1

        new_key.vertex_group = utils.create_folder_data()
        new_key.name = "Folder " + str(folder_count)
    else:
        if len(key_blocks) == 1:
            new_key.name = "Basis"
        else:
            new_key.name = "Key " + str(len(key_blocks) - 1)

    # Shape Key Placement
    # If there was no original active key, no special placement will be done.
    if active_key:
        is_active_folder = utils.is_key_folder(active_key)

        if is_active_folder:
            # Prioritize the selected key as the new key's
            # parent if the selected key is a folder.
            parent = active_key
        elif active_parent:
            # If the selected key isn't a folder,
            # use its parent as the new key's parent.
            parent = active_parent
        else:
            # Only consider auto-parenting if the current context
            # allows for a key to be used as the new key's parent.
            parent = None

        if type == 'PARENT':
            if active_parent:
                # This counts as manually parenting, so it works even when auto parent is turned off.
                shape_key_parent(new_key, active_parent)

            # This part ignores all placement options, and it is assumed that the
            # new folder should take the location of whatever is being parented to it.
            utils.shape_key_move_to(utils.get_key_index(new_key), active_index)
        else:
            if skp.shape_key_auto_parent and parent:
                if is_active_folder:
                    shape_key_parent(new_key, parent)
                else:
                    shape_key_parent(new_key, parent, sibling=active_key)
            else:
                utils.apply_add_placement(new_key, active_key)

    return new_key


def shape_key_remove(type='DEFAULT', index=-1):
    context = bpy.context
    skp = context.scene.shape_keys_plus
    obj = context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks

    if index == -1:
        active_index = obj.active_shape_key_index
    else:
        active_index = index

    active_key = key_blocks[active_index]
    basis_key = shape_keys.reference_key

    previous_index = active_index - 1
    previous_key = key_blocks[previous_index] if previous_index >= 0 else None

    next_index = active_index + 1
    next_key = key_blocks[next_index] if next_index < len(key_blocks) else None

    active_key_parent = utils.get_key_parent(active_key)
    previous_key_parent = utils.get_key_parent(previous_key) if previous_key else None
    next_key_parent = utils.get_key_parent(next_key) if next_key else None

    siblings = utils.get_key_siblings(active_key)

    is_active_folder = utils.is_key_folder(active_key)
    active_children = utils.get_folder_children(active_key)
    active_capacity = len(active_children)

    if type == 'CLEAR':
        bpy.ops.object.shape_key_remove(all=True)
    elif type == 'DEFAULT':
        obj.active_shape_key_index = active_index

        bpy.ops.object.shape_key_remove()

        if active_key_parent:
            utils.shift_folder_children_value(active_key_parent, -1)

        # The list of children will be empty if this key isn't a folder.
        for c in active_children:
            obj.active_shape_key_index = utils.get_key_index(c)

            bpy.ops.object.shape_key_remove()

        # Fix the active index.
        if siblings[0] and siblings[0].name != basis_key.name:
            obj.active_shape_key_index = utils.get_key_index(siblings[0])
        elif siblings[1]:
            obj.active_shape_key_index = utils.get_key_index(siblings[1])
    elif type == 'DEFAULT_SELECTED':
        selections = utils.selected_shape_keys()
        keys = []

        removing_active = False

        # Search for keys by name and remove them.
        for key in selections:
            if key != active_key:
                keys.append(key)

        # Remove the active key last so that the active index automatically corrects itself.
        if utils.shape_key_selected(active_index):
            removing_active = True
            keys.append(active_key)

        for key in keys:
            obj.active_shape_key_index = utils.get_key_index(key)

            key_parent = utils.get_key_parent(key)

            bpy.ops.object.shape_key_remove()

            if key_parent:
                utils.shift_folder_children_value(key_parent, -1)

        if not removing_active:
            obj.active_shape_key_index = utils.get_key_index(active_key)

        shape_keys.shape_keys_plus.selections.clear()


def shape_key_move(type, index=-1):
    context = bpy.context
    skp = context.scene.shape_keys_plus
    obj = context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    data = evaluate()

    modifiers = hide_modifiers(obj)

    if index == -1:
        index = obj.active_shape_key_index

    direction = 'UP' if type in ('UP', 'TOP') else 'DOWN'

    active_metadata = data[index]
    active_key = active_metadata.key

    next_key = active_metadata.previous_key if type in ('UP', 'TOP') else active_metadata.next_key
    next_metadata = metadata(data, next_key) if next_key else None
    parent_metadata = metadata(data, active_metadata.first_parent) if active_metadata.first_parent else None

    parent_key = parent_metadata.key if parent_metadata else None
    basis_key = key_blocks[0]
    basis_metadata = data[0]
    last_key = key_blocks[-1]
    last_metadata = data[-1]

    next_parent_metadata = \
        metadata(data, next_metadata.first_parent) if \
        next_metadata and next_metadata.first_parent else \
        None

    def is_active_folder():
        return active_metadata.is_folder

    def is_next_folder():
        return next_metadata and next_metadata.is_folder

    def is_active_only_child():
        if parent_metadata:
            is_only_child = utils.get_folder_children_value(parent_key) == 1
        else:
            is_only_child = len(key_blocks) == 1

        return is_only_child

    def is_active_first_child():
        if parent_metadata:
            is_first_child = active_metadata.is_first_child
        else:
            is_first_child = active_key.name == key_blocks[0].name

        return is_first_child

    def is_active_last_child():
        if active_metadata.has_children:
            if parent_metadata:
                is_last_child = active_metadata.last_child.name == parent_metadata.last_child.name
            else:
                is_last_child = active_metadata.last_child.name == last_key.name
        else:
            is_last_child = active_metadata.is_last_child

        return is_last_child

    def is_next_last_child():
        return next_metadata and next_metadata.is_last_child

    def move(index, direction):
        """Moves the shape key and all in its capacity range."""

        capacity = active_metadata.capacity
        is_folder = capacity > 0
        offset = index + capacity + 1

        if direction == 'UP':
            r = range(index, offset)
        else:
            r = reversed(range(index, offset))

        for i in r:
            obj.active_shape_key_index = i
            bpy.ops.object.shape_key_move(type=direction)

        if is_folder:
            # Re-selects the folder after moving its children.
            obj.active_shape_key_index = index - 1 if direction == 'UP' else index + 1

    def move_to_top(folder_metadata):
        if folder_metadata:
            offset = folder_metadata.first_child_index

            for i in range(index, offset, -1):
                move(i, 'UP')
        else:
            basis_capacity = basis_metadata.capacity + 1

            offset = basis_capacity if index > basis_capacity else 0

            for i in range(index, offset, -1):
                move(i, 'UP')

    def move_to_bottom(folder_metadata):
        if folder_metadata:
            offset = folder_metadata.last_child_index - active_metadata.capacity

            for i in range(index, offset):
                move(i, 'DOWN')
        else:
            offset = last_metadata.index - active_metadata.capacity

            for i in range(index, offset):
                move(i, 'DOWN')

    def skip_over_folder(next_folder_metadata):
        # The "stack" is the number of parents the key has.
        active_stack = active_metadata.stack
        folder_stack = next_folder_metadata.stack

        if folder_stack > active_stack:
            # Get the next folder's parent that matches the
            # parent of the active key, in case the next
            # folder is the last child of multiple folders.
            #
            # folder stack          = 4
            # active stack          = 2
            # common parent index   = 4 - (2 + 1) = 1
            # common parent         = parents[1]
            common_parent_index = folder_stack - (active_stack + 1)
            parent = next_folder_metadata.parents[common_parent_index]

            # Update the folder to skip over a lower-level parent.
            next_folder_metadata = metadata(data, parent)

        if direction == 'UP':
            offset = index - next_folder_metadata.capacity
            r = range(index, offset - 1, -1)
        else:
            offset = index + next_folder_metadata.capacity
            r = range(index, offset + 1)

        for i in r:
            move(i, direction)

    if is_active_only_child():
        # The key can't be moved if it's the only key in its local space.
        pass
    elif type == 'TOP':
        # Move the active key to the top of the specified folder's space, or the global space if no folder exists.
        move_to_top(parent_metadata)
    elif type == 'BOTTOM':
        # Move the active key to the bottom of the specified folder's space, or the global space if no folder exists.
        move_to_bottom(parent_metadata)
    elif is_active_first_child():
        if type == 'UP':
            # If the active key is the first child in its space,
            # moving up will cause it to loop back around to the bottom.
            move_to_bottom(parent_metadata)
        elif type == 'DOWN':
            if is_next_folder():
                skip_over_folder(next_metadata)
            else:
                move(index, 'DOWN')
    elif is_active_last_child():
        if type == 'UP':
            if is_next_last_child():
                # If moving up while the above key is the last child of another space, skip over that entire space.
                skip_over_folder(next_parent_metadata)
            else:
                move(index, 'UP')
        elif type == 'DOWN':
            # If the active key is the last child in its space,
            # moving down will cause it to loop back around to the top.
            move_to_top(parent_metadata)
    else:
        if type == 'UP':
            if is_next_last_child():
                # If moving up while the above key is the last child in another space, skip over that entire space.
                skip_over_folder(next_parent_metadata)
            else:
                move(index, 'UP')
        elif type == 'DOWN':
            if is_next_folder():
                skip_over_folder(next_metadata)
            else:
                move(index, 'DOWN')

    show_modifiers(modifiers)


def shape_key_select(i, v):
    context = bpy.context
    skp = context.scene.shape_keys_plus
    obj = context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    selections = shape_keys.shape_keys_plus.selections

    if type(i) == bpy.types.ShapeKey:
        key = i
        i = utils.get_key_index(key)
    elif type(i) == str:
        key = key_blocks[i]
        i = utils.get_key_index(key)
    elif type(i) == int:
        key = key_blocks[i]

    valid = i > 0 and not utils.is_key_folder(key)

    if not valid:
        return

    i = str(i)

    if v == True:
        get(selections, i, selections.add()).name = i
    elif v == False:
        while i in selections:
            selections.remove(selections.find(i))

#sav
def shape_key_copy(type='DEFAULT'):
    context = bpy.context
    data = bpy.data
    skp = context.scene.shape_keys_plus
    obj = context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    basis_key = shape_keys.reference_key

    active_key = obj.active_shape_key
    active_index = obj.active_shape_key_index
    active_name = active_key.name
    active_parent = utils.get_key_parent(active_key)
    active_children = utils.get_folder_children(active_key)

    is_active_folder = utils.is_key_folder(active_key)

    obj.active_shape_key_index = active_index

    def copy(original_key):
        unmuted_keys = []

        # Mute all keys other than the original key.
        for kb in key_blocks:
            applicable = kb.mute == False and kb.name != original_key.name and kb.name != basis_key.name

            if applicable:
                unmuted_keys.append(kb)
                kb.mute = True

        driver = utils.get_key_driver(shape_keys, original_key)

        # Store original values.
        old_name = original_key.name
        old_slider_min = original_key.slider_min
        old_slider_max = original_key.slider_max
        old_value = original_key.value
        old_vertex_group = original_key.vertex_group
        old_relative_key = original_key.relative_key
        old_interpolation = original_key.interpolation
        old_mute = original_key.mute

        if driver:
            old_driver_type = driver.type
            old_driver_expression = driver.expression

        # Prepare shape key for full copy.
        original_key.slider_min = 0.0
        original_key.slider_max = 1.0
        original_key.value = 1.0
        original_key.vertex_group = ""
        original_key.relative_key = basis_key
        original_key.interpolation = bpy.types.ShapeKey.bl_rna.properties['interpolation'].default
        original_key.mute = False

        if driver:
            driver.type = 'SCRIPTED'
            driver.expression = "var + " + str(original_key.value)

        new_key = obj.shape_key_add(from_mix=True)

        # Select the new key, which was sent to the bottom.
        obj.active_shape_key_index = len(key_blocks) - 1

        # to delete shape_key mirror

        def mirror_shape_key_update():
            index_new = data.shape_keys[shape_keys.name].key_blocks.find(old_name)
            if index_new !=-1:
                bpy.context.object.active_shape_key_index = index_new
                bpy.ops.object.blenrig_shape_key_remove(type='DEFAULT')

        if 'MIRROR' in type:
            use_topology = 'TOPOLOGY' in type

            bpy.ops.object.shape_key_mirror(use_topology=use_topology)

            if old_name.endswith(".L"):
                old_name = old_name[:-2] + ".R"
                mirror_shape_key_update()

            elif old_name.endswith("_L"):
                old_name = old_name[:-2] + "_R"
                mirror_shape_key_update()

            elif old_name.endswith(".R"):
                old_name = old_name[:-2] + ".L"
                mirror_shape_key_update()

            elif old_name.endswith("_R"):
                old_name = old_name[:-2] + "_L"
                mirror_shape_key_update()


        # Copy original values.
        new_key.name = old_name
        new_key.slider_min = old_slider_min
        new_key.slider_max = old_slider_max
        new_key.value = old_value
        if 'MIRROR' in type:
            if old_vertex_group.endswith("_L"):
                new_key.vertex_group = old_vertex_group[:-2] + "_R"
            elif old_vertex_group.endswith(".L"):
                new_key.vertex_group = old_vertex_group[:-2] + ".R"
            elif old_vertex_group.endswith("_R"):
                new_key.vertex_group = old_vertex_group[:-2] + "_L"
            elif old_vertex_group.endswith(".R"):
                new_key.vertex_group = old_vertex_group[:-2] + ".L"
        else:
            new_key.vertex_group = old_vertex_group
        new_key.relative_key = old_relative_key
        new_key.interpolation = old_interpolation
        new_key.mute = old_mute

        # Restore original values.
        original_key.slider_min = old_slider_min
        original_key.slider_max = old_slider_max
        original_key.value = old_value
        original_key.vertex_group = old_vertex_group
        original_key.relative_key = old_relative_key
        original_key.interpolation = old_interpolation
        original_key.mute = old_mute

        if driver:
            driver.type = old_driver_type
            driver.expression = old_driver_expression

        for key in unmuted_keys:
            key.mute = False

        return new_key

    if 'SELECTED' in type:
        selections = [key.name for key in utils.selected_shape_keys()]
        copies = []

        shape_keys.shape_keys_plus.selections.clear()

        for name in selections:
            key = key_blocks[name]
            copy_key = copy(key)

            key_parent = utils.get_key_parent(key)
            auto_parent = skp.shape_key_auto_parent and key_parent

            utils.apply_copy_placement(copy_key, key)

            if auto_parent:
                utils.shift_folder_children_value(key_parent, 1)

            copies.append(copy_key)

        for key in copies:
            shape_key_select(key, True)

        obj.active_shape_key_index = utils.get_key_index(key_blocks[active_name])
    else:
        copy_key = copy(active_key)
        copy_children = []

        for c in active_children:
            copy_children.append(copy(c))

        auto_parent = skp.shape_key_auto_parent and active_parent

        if not auto_parent:
            old_stack = utils.get_folder_stack_value(copy_key)

            utils.set_folder_stack_value(copy_key, 1)

            for c in copy_children:
                if not utils.is_key_folder(c):
                    continue

                stack_offset = utils.get_folder_stack_value(c) - old_stack

                utils.set_folder_stack_value(c, 1 + stack_offset)

        utils.apply_copy_placement(copy_key, active_key)

        if auto_parent:
            utils.shift_folder_children_value(active_parent, 1)

        bpy.ops.driver.blenrig_driver_update('INVOKE_DEFAULT')
        obj.active_shape_key_index = utils.get_key_index(active_key)
        shape_keys.shape_keys_plus.selections.clear()

########################################################################
############################## OPERATORS ###############################
########################################################################


class OBJECT_OT_blenrig_folder_icon(bpy.types.Operator):
    bl_idname = 'object.blenrig_folder_icon'
    bl_label = "Set As Folder Icon"
    bl_description = "Sets the folder icon"
    bl_options = {'REGISTER', 'UNDO'}

    icons : bpy.props.IntProperty(
        options={'HIDDEN'})

    swap : bpy.props.BoolProperty(
        name="Swap",
        default=False)

    set_as_default : bpy.props.BoolProperty(
        name="Set Default",
        default=False)

    def execute(self, context):
        skp = context.scene.shape_keys_plus
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        is_active_folder = active_key and utils.is_key_folder(active_key)

        if is_active_folder:
            active_key.vertex_group = utils.block_set(
                active_key.vertex_group,
                utils.icons,
                self.icons)

            active_key.vertex_group = utils.block_set(
                active_key.vertex_group,
                utils.icons_swap,
                1 if self.swap else 0)

        if self.set_as_default:
            skp.folder_icon_pair = self.icons
            skp.folder_icon_swap = 1 if self.swap else 0

        return {'FINISHED'}


class OBJECT_OT_blenrig_shape_key_parent(bpy.types.Operator):
    bl_idname = 'object.blenrig_shape_key_parent'
    bl_label = "Set As Parent"
    bl_description = "Sets the parent"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.EnumProperty(
        items=(
            ('PARENT', "", ""),
            ('UNPARENT', "", ""),
            ('CLEAR', "", "Unparents the active shape key completely."),
            ('NEW', "", "Creates a new parent for the active shape key."),
            ('PARENT_SELECTED', "", ""),
            ('UNPARENT_SELECTED', "", ""),
            ('CLEAR_SELECTED', "", "Unparents the selected shape keys completely."),
            ('NEW_SELECTED', "", "Creates a new parent for the selected shape keys.")
        ),
        default='PARENT',
        options={'HIDDEN'})

    child : bpy.props.StringProperty(options={'HIDDEN'})
    parent : bpy.props.StringProperty(options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return bpy.context.object.mode != 'EDIT'

    def execute(self, context):
        skp = context.scene.shape_keys_plus
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        selections = [key.name for key in utils.selected_shape_keys()]

        shape_keys.shape_keys_plus.selections.clear()

        child = key_blocks.get(self.child)
        parent = key_blocks.get(self.parent)

        if self.type == 'PARENT':
            shape_key_parent(child, parent)
        elif self.type == 'UNPARENT':
            shape_key_unparent(child)
        elif self.type == 'CLEAR':
            shape_key_unparent(child, clear=True)
        elif self.type == 'NEW':
            shape_key_parent(child, shape_key_add(type='PARENT'))
        elif self.type == 'PARENT_SELECTED':
            children = []

            for name in selections:
                child = key_blocks[name]
                child_parent = utils.get_key_parent(child)

                if child_parent:
                    utils.shift_folder_children_value(child_parent, -1)

                # Set the shape keys in the proper order.
                obj.active_shape_key_index = utils.get_key_index(child)
                bpy.ops.object.shape_key_move(type='BOTTOM')

            if skp.shape_key_parent_placement == 'TOP':
                selections = reversed(selections)

            for name in selections:
                child = key_blocks[name]
                shape_key_parent(child, parent)

                children.append(child)

            for child in children:
                shape_key_select(child, True)
        elif self.type == 'UNPARENT_SELECTED':
            children = []

            if skp.shape_key_unparent_placement in ('DOWN', 'TOP'):
                selections = reversed(selections)

            for name in selections:
                child = key_blocks[name]
                shape_key_unparent(child)

                children.append(child)

            for child in children:
                shape_key_select(child, True)
        elif self.type == 'CLEAR_SELECTED':
            children = []

            if skp.shape_key_unparent_placement in ('DOWN', 'TOP'):
                selections = reversed(selections)

            for name in selections:
                child = key_blocks[name]
                shape_key_unparent(child, clear=True)

                children.append(child)

            for child in children:
                shape_key_select(child, True)
        elif self.type == 'NEW_SELECTED':
            parent = shape_key_add(type='FOLDER')
            children = []

            for name in selections:
                child = key_blocks[name]
                shape_key_unparent(child, clear=True)

                # Set the shape keys in the proper order.
                obj.active_shape_key_index = utils.get_key_index(child)
                bpy.ops.object.shape_key_move(type='BOTTOM')

            if skp.shape_key_parent_placement == 'TOP':
                selections = reversed(selections)

            for name in selections:
                child = key_blocks[name]
                shape_key_parent(child, parent)

                children.append(child)

            for child in children:
                shape_key_select(child, True)

            obj.active_shape_key_index = utils.get_key_index(parent)

        # Force update SKP cache to ensure that the UI updates.
        utils.update_cache(override=True)

        return {'FINISHED'}


class OBJECT_OT_blenrig_shape_key_add(bpy.types.Operator):
    bl_idname = 'object.blenrig_shape_key_add'
    bl_label = "Add Shape Key"
    bl_description = "Add shape key to the object"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.EnumProperty(
        items=(
            ('DEFAULT', "", ""),
            ('FROM_MIX', "", ""),
            ('FROM_MIX_SELECTED', "", ""),
            ('FOLDER', "", "")
        ),
        default='DEFAULT',
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}

        return obj and obj.mode != 'EDIT' and obj.type in valid_types

    def execute(self, context):
        shape_key_add(self.type)
        return {'FINISHED'}


class OBJECT_OT_blenrig_shape_key_remove(bpy.types.Operator):
    bl_idname = 'object.blenrig_shape_key_remove'
    bl_label = "Remove Shape Key"
    bl_description = "Remove shape key from the object"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.EnumProperty(
        items=(
            ('DEFAULT', "", ""),
            ('CLEAR', "", ""),
            ('DEFAULT_SELECTED', "", "")
        ),
        default='DEFAULT',
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj.mode != 'EDIT' and obj.active_shape_key

    def execute(self, context):
        shape_key_remove(self.type)
        return {'FINISHED'}


class OBJECT_OT_blenrig_shape_key_copy(bpy.types.Operator):
    bl_label = "Copy Shape"
    bl_idname = 'object.blenrig_shape_key_copy'
    bl_description = "Copy existing shape key"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.EnumProperty(
        items=(
            ('DEFAULT', "", ""),
            ('MIRROR', "", ""),
            ('MIRROR_TOPOLOGY', "", ""),
            ('DEFAULT_SELECTED', "", ""),
            ('MIRROR_SELECTED', "", ""),
            ('MIRROR_TOPOLOGY_SELECTED', "", "")
        ),
        default='DEFAULT',
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key #and obj.mode != 'EDIT' #sav

    def execute(self, context):
        if context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            shape_key_copy(self.type)
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}
        shape_key_copy(self.type)
        return {'FINISHED'}


class OBJECT_OT_blenrig_shape_key_move(bpy.types.Operator):
    bl_idname = 'object.blenrig_shape_key_move'
    bl_label = "Move Shape Key"
    bl_description = "Move shape key up/down in the list"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.EnumProperty(
        name='Type',
        items=(
            ('TOP', "Top", ""),
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('BOTTOM', "Bottom", ""),
        ))

    selected : bpy.props.BoolProperty(
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        # Check if sibling shape keys exist before attempting to move.
        # A folder's children do not count as siblings to the folder.
        obj = context.object

        if not obj or obj.mode == 'EDIT':
            return False

        if obj.active_shape_key:
            # key_blocks will exist if active_shape_key exists.
            shape_keys = obj.data.shape_keys
            key_blocks = shape_keys.key_blocks
            basis_capacity = utils.get_folder_capacity(key_blocks[0])
            active_index = obj.active_shape_key_index

            return basis_capacity + 1 < len(key_blocks) or active_index > 0
        else:
            return False

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks

        if self.selected:
            original_name = obj.active_shape_key.name

            names = [key.name for key in utils.selected_shape_keys()]
            selections = [key.name for key in utils.selected_shape_keys()]

            shape_keys.shape_keys_plus.selections.clear()

            if self.type in ('DOWN', 'TOP'):
                selections = reversed(selections)

            for name in selections:
                index = utils.get_key_index(key_blocks[name])
                shape_key_move(self.type, index)

            for name in names:
                shape_key_select(name, True)

            original_index = key_blocks.find(original_name)
            obj.active_shape_key_index = original_index
        else:
            shape_key_move(self.type)

        return {'FINISHED'}


class OBJECT_OT_blenrig_shape_key_select(bpy.types.Operator):
    bl_label = "Select/Deselect Shape Key"
    bl_idname = 'object.blenrig_shape_key_select'
    bl_description = "Select this shape key"
    bl_options = {'REGISTER', 'UNDO'}

    mode : bpy.props.EnumProperty(
        items=(
            ('TOGGLE', "", ""),
            ('ALL', "", ""),
            ('NONE', "", ""),
            ('INVERSE', "", "")
        ),
        options={'HIDDEN'})

    index : bpy.props.IntProperty(options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        skp = context.scene.shape_keys_plus
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        selections = shape_keys.shape_keys_plus.selections

        if self.mode == 'TOGGLE':
            shape_key_select(self.index, str(self.index) not in selections)
        elif self.mode == 'ALL':
            for index, key in enumerate(key_blocks):
                shape_key_select(index, True)
        elif self.mode == 'NONE':
            selections.clear()
        elif self.mode == 'INVERSE':
            for index, key in enumerate(key_blocks):
                shape_key_select(index, str(index) not in selections)

        return {'FINISHED'}


class OBJECT_OT_blenrig_folder_toggle(bpy.types.Operator):
    bl_label = "Expand/Collapse"
    bl_idname = 'object.blenrig_folder_toggle'
    bl_description = "Show or hide this folder's children"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        active_key = obj.active_shape_key
        active_parents = utils.get_key_parents(active_key)
        folder = key_blocks[self.index]

        if folder in active_parents:
            # The active index shouldn't be on a hidden shape key.
            obj.active_shape_key_index = self.index

        utils.toggle_folder(folder)

        return {'FINISHED'}


class OBJECT_OT_blenrig_folder_ungroup(bpy.types.Operator):
    bl_label = "Ungroup Folder"
    bl_idname = 'object.blenrig_folder_ungroup'
    bl_description = "Ungroup this folder"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        key = shape_keys.key_blocks[self.index]
        is_folder = utils.is_key_folder(key)
        children = utils.get_folder_children(key)
        parent = utils.get_key_parent(key)

        selections = [key.name for key in utils.selected_shape_keys()]

        shape_keys.shape_keys_plus.selections.clear()

        utils.toggle_folder(key, expand=True)

        old_index = obj.active_shape_key_index

        if parent:
            utils.shift_folder_children_value(parent, utils.get_folder_children_value(key) - 1)

        for c in children:
            if utils.is_key_folder(c):
                utils.shift_folder_stack_value(c, -1)

        obj.active_shape_key_index = self.index
        bpy.ops.object.shape_key_remove()

        # Fix the active index.
        obj.active_shape_key_index = old_index - (1 if (old_index > self.index or not children) else 0)

        for name in selections:
            shape_key_select(name, True)

        return {'FINISHED'}


class DRIVER_OT_blenrig_driver_update(bpy.types.Operator):
    bl_label = "Update Driver"
    bl_idname = 'driver.blenrig_driver_update'
    bl_description = "Force update this driver"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            utils.update_driver(utils.get_key_driver(shape_keys, active_key))

        return {'FINISHED'}


class DRIVER_OT_blenrig_variable_add(bpy.types.Operator):
    bl_label = "Add Input Variable"
    bl_idname = 'driver.blenrig_variable_add'
    bl_description = "Add a new variable for this driver"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            driver = utils.get_key_driver(shape_keys, active_key)

            if driver:
                driver.variables.new()

        return {'FINISHED'}


class DRIVER_OT_blenrig_variable_remove(bpy.types.Operator):
    bl_label = "Remove Variable"
    bl_idname = 'driver.blenrig_variable_remove'
    bl_description = "Remove variable from the driver"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            driver = utils.get_key_driver(shape_keys, active_key)

            if driver and len(driver.variables) > self.index:
                driver.variables.remove(driver.variables[self.index])

        return {'FINISHED'}


class DRIVER_OT_blenrig_variable_copy(bpy.types.Operator):
    bl_label = "Copy Variable"
    bl_idname = 'driver.blenrig_variable_copy'
    bl_description = "Copy this variable"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            driver = utils.get_key_driver(shape_keys, active_key)

            if driver and len(driver.variables) > self.index:
                var = driver.variables.new()
                vars = list(driver.variables)

                vars.insert(self.index + 1, vars.pop(len(vars) - 1))

                var.name = vars[self.index].name + "_copy"
                var.type = vars[self.index].type

                for t in range(len(vars[self.index].targets)):
                    var.targets[t].bone_target = vars[self.index].targets[t].bone_target
                    var.targets[t].data_path = vars[self.index].targets[t].data_path

                    if var.type == 'SINGLE_PROP':
                        var.targets[t].id_type = vars[self.index].targets[t].id_type

                    var.targets[t].id = vars[self.index].targets[t].id
                    var.targets[t].transform_space = vars[self.index].targets[t].transform_space
                    var.targets[t].transform_type = vars[self.index].targets[t].transform_type

                utils.reconstruct_driver_variables(driver, vars)

        return {'FINISHED'}


class DRIVER_OT_blenrig_variable_move(bpy.types.Operator):
    bl_label = "Move Variable"
    bl_idname = 'driver.blenrig_variable_move'
    bl_description = "Move this variable up/down in the list"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(options={'HIDDEN'})

    type : bpy.props.EnumProperty(
        items=(
            ('TOP', "", ""),
            ('UP', "", ""),
            ('DOWN', "", ""),
            ('BOTTOM', "", "")
        ),
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            driver = utils.get_key_driver(shape_keys, active_key)

            if driver and len(driver.variables) > self.index:
                vars = list(driver.variables)

                if self.type == 'TOP':
                    vars.insert(0, vars.pop(self.index))
                elif self.type == 'UP' and self.index > 0:
                    vars.insert(self.index - 1, vars.pop(self.index))
                elif self.type == 'DOWN' and self.index < len(vars) - 1:
                    vars.insert(self.index + 1, vars.pop(self.index))
                elif self.type == 'BOTTOM':
                    vars.insert(len(vars) - 1, vars.pop(self.index))

                utils.reconstruct_driver_variables(driver, vars)

        return {'FINISHED'}


class OBJECT_OT_blenrig_debug_folder_data(bpy.types.Operator):
    bl_label = "[ DEBUG ] Folder Data"
    bl_idname = 'object.blenrig_debug_folder_data'
    bl_description = "Manually create folder data"
    bl_options = {'REGISTER', 'UNDO'}

    folder : bpy.props.IntProperty(
        name="Folder Iterations",
        default=1,
        description="Number of times to indent the folder's children (1 + [number of folder's parents])")

    children : bpy.props.IntProperty(
        name="Children",
        default=0,
        description="The amount of children the folder has, not including children of children")

    expand : bpy.props.BoolProperty(
        name="Expand",
        default=True,
        description="Expand or collapse the folder")

    icons : bpy.props.IntProperty(
        name="Icon Pair",
        default=0,
        min=0,
        max=utils.icon_pairs[-1][-1],
        description="The pair of icons used when the folder is expanded or collapsed")

    icons_swap : bpy.props.BoolProperty(
        name="Swap Icons",
        default=False,
        description="Swap the icons used for when the folder is expanded or collapsed")

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.active_shape_key

    def execute(self, context):
        obj = context.object
        active_key = obj.active_shape_key

        active_key.vertex_group = utils.create_folder_data(
            folder=self.folder,
            children=self.children,
            expand=1 if self.expand else 0,
            icons=self.icons,
            icons_swap=1 if self.icons_swap else 0)

        return {'FINISHED'}
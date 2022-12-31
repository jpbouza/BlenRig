import bpy
import bl_ui
from .shape_keys_plus import *

class BLENRIG_PT_shape_keys_plus(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_idname = "BLENRIG_PT_shape_keys_plus"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general_SubPanel"
    bl_region_type = 'UI'
    bl_label = 'Shape Keys+'
    bl_category = "BlenRig 6"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext2 == 'SHAPEKEYS':
            return False

        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}

        return obj and obj.type in valid_types

    def draw(self, context):
        layout = self.layout

        skp = context.scene.shape_keys_plus
        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key
        active_index = obj.active_shape_key_index
        selections = utils.selected_shape_keys()

        if active_key:
            is_active_folder = utils.is_key_folder(active_key)
        else:
            is_active_folder = False

        enable_edit = obj.mode != 'EDIT'
        enable_edit_value = False

        if obj.show_only_shape_key is False:
            use_edit_mode = obj.type == 'MESH' and obj.use_shape_key_edit_mode

            if enable_edit or use_edit_mode:
                enable_edit_value = True


        row = layout.row()
        col = row.column()
        box = col.box()
        box.scale_x = 5.35
        col = box.column()
        col.operator("blenrig.update_shapekey_driver", text = 'Update Driver with Current Pose')
        col.operator("blenrig.update_face_shapekeys_drivers", text = 'Update All Facial Drivers')
        row_mirror = col.row()
        row_mirror.operator("blenrig.mirror_active_shapekey_driver", text = 'Mirror Active Shapekey Driver')
        row_mirror.operator("blenrig.mirror_shapekeys_drivers", text = 'Mirror All Shapekeys Drivers')
        box2 = col.box()
        box2.scale_x = 5.35
        col = box2.column()
        col.label(text='Add Predefined Shapekeys')
        row_main = col.row()
        row_main.operator("blenrig.add_body_shapekeys", text = 'Add Body Shapekeys')
        row_main.operator("blenrig.add_face_shapekeys", text = 'Add Face Shapekeys')
        row_fingers = col.row()
        row_fingers.operator("blenrig.add_fingers_shapekeys", text = 'Add Fingers Shapekeys')
        row_fingers.operator("blenrig.add_toes_shapekeys", text = 'Add Toes Shapekeys')

        # col.separator()

        # prop_data = skp.bl_rna.properties['shape_key_add_placement']

        # col.prop_menu_enum(
        #     data=skp,
        #     property='shape_key_add_placement',
        #     text="Add / Copy",
        #     icon=prop_data.enum_items[skp.shape_key_add_placement].icon)

        # prop_data = skp.bl_rna.properties['shape_key_parent_placement']

        # col.prop_menu_enum(
        #     data=skp,
        #     property='shape_key_parent_placement',
        #     text="Parent",
        #     icon=prop_data.enum_items[skp.shape_key_parent_placement].icon)

        # prop_data = skp.bl_rna.properties['shape_key_unparent_placement']

        # col.prop_menu_enum(
        #     data=skp,
        #     property='shape_key_unparent_placement',
        #     text="Unparent",
        #     icon=prop_data.enum_items[skp.shape_key_unparent_placement].icon)

        # box = row.box()
        # col = box.column()
        # col.label(
        #     text="Hierarchy",
        #     icon='OUTLINER')
        # col.separator()

        # col.prop(
        #     data=skp,
        #     property='shape_key_auto_parent',
        #     toggle=True,
        #     icon='FILE_PARENT')

        # col.prop(
        #     data=skp,
        #     property='shape_key_indent_scale',
        #     slider=True)

        box = row.box()
        box.scale_x = 0.75
        col = box.column()

        if selections:
            col.label(text=str(len(selections)) + " Selected")
        else:
            col.label(
                text="Select...",
                icon='RESTRICT_SELECT_OFF')

        col.separator()

        op = col.operator(
            operator='object.blenrig_shape_key_select',
            text="All",
            icon='ADD')

        op.mode = 'ALL'

        op = col.operator(
            operator='object.blenrig_shape_key_select',
            text="None",
            icon='REMOVE')

        op.mode = 'NONE'

        op = col.operator(
            operator='object.blenrig_shape_key_select',
            text="Inv.",
            icon='ARROW_LEFTRIGHT')

        op.mode = 'INVERSE'

        row = layout.row()

        row.template_list(
            listtype_name='MESH_UL_BlenRig_shape_keys_plus',
            dataptr=shape_keys,
            propname='key_blocks',
            active_dataptr=obj,
            active_propname='active_shape_key_index',
            list_id='SHAPE_KEYS_PLUS',
            rows=8 if active_key else 4)

        col = row.column()

        #####################
        ######## ADD ########
        #####################

        row = col.row(align=True)
        btn = row.column()

        btn.enabled = not selections

        op = btn.operator(
            operator='object.blenrig_shape_key_add',
            icon='ADD',
            text="")

        op.type = 'DEFAULT'

        mnu = row.column()

        mnu.menu(
            menu='MESH_MT_blenrig_shape_key_add_specials',
            icon='DOWNARROW_HLT',
            text="")

        ######################
        ######## COPY ########
        ######################

        row = col.row(align=True)
        mnu = row.column()

        mnu.menu(
            menu='MESH_MT_blenrig_shape_key_copy_specials',
            icon='COLLAPSEMENU',
            text="")

        btn = row.column()

        btn.enabled = not selections

        op = btn.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEDOWN',
            text="")

        op.type = 'DEFAULT'

        ########################
        ######## REMOVE ########
        ########################

        row = col.row(align=True)
        btn = row.column()

        btn.enabled = not selections

        op = btn.operator(
            operator='object.blenrig_shape_key_remove',
            icon='REMOVE',
            text="")
        row.menu(
            menu='MESH_MT_blenrig_shape_key_other_specials',icon='DOWNARROW_HLT',
            text="")

        op.type = 'DEFAULT'

        #########################
        ######## SPECIAL ########
        #########################

        row = col.row(align=False)
        row.scale_x = 2.0

        if not active_key:
            return

        col.separator()

        sub = col.column(align=True)

        op = sub.operator(
            operator='object.blenrig_shape_key_move',
            icon='TRIA_UP_BAR',
            text="")

        op.type = 'TOP'
        op.selected = bool(selections)

        op = sub.operator(
            operator='object.blenrig_shape_key_move',
            icon='TRIA_UP',
            text="")

        op.type = 'UP'
        op.selected = bool(selections)

        op = sub.operator(
            operator='object.blenrig_shape_key_move',
            icon='TRIA_DOWN',
            text="")

        op.type = 'DOWN'
        op.selected = bool(selections)

        op = sub.operator(
            operator='object.blenrig_shape_key_move',
            icon='TRIA_DOWN_BAR',
            text="")

        op.type = 'BOTTOM'
        op.selected = bool(selections)

        split = layout.split(factor=0.4, align=False)

        row = split.row()
        row.enabled = enable_edit

        row.prop(
            data=shape_keys,
            property='use_relative')

        row = split.row()
        row.alignment = 'RIGHT'

        sub = row.row(align=True)
        sub.label()

        sub = sub.row(align=True)
        sub.active = enable_edit_value

        sub.prop(
            data=obj,
            property='show_only_shape_key',
            text="")

        sub.prop(
            data=obj,
            property='use_shape_key_edit_mode',
            text="")

        sub = row.row()

        if shape_keys.use_relative:
            sub.operator(
                operator='object.shape_key_clear',
                icon='X',
                text="")
        else:
            sub.operator(
                operator='object.shape_key_retime',
                icon='RECOVER_LAST',
                text="")

        if is_active_folder:
            return

        if shape_keys.use_relative:
            if active_index != 0:
                row = layout.row()
                row.active = enable_edit_value

                row.prop(
                    data=active_key,
                    property='value')

                split = layout.split()

                col = split.column(align=True)
                col.active = enable_edit_value

                col.label(
                    text="Range:")

                col.prop(
                    data=active_key,
                    property='slider_min',
                    text="Min")

                col.prop(
                    data=active_key,
                    property='slider_max',
                    text="Max")

                col = split.column(align=True)
                col.active = enable_edit_value

                col.label(
                    text="Blend:")

                col.prop_search(
                    data=active_key,
                    property='vertex_group',
                    search_data=obj,
                    search_property='vertex_groups',
                    text="")

                col.prop_search(
                    data=active_key,
                    property='relative_key',
                    search_data=shape_keys,
                    search_property='key_blocks',
                    text="")
        else:
            layout.prop(
                data=active_key,
                property='interpolation')

            row = layout.column()
            row.active = enable_edit_value

            row.prop(
                data=shape_keys,
                property='eval_time')

        driver = utils.get_key_driver(shape_keys, active_key)

        if not driver:
            return

        layout.separator()

        row = layout.row()
        row.prop(
            data=skp,
            property='driver_visible')

        if not skp.driver_visible:
            return

        row = layout.row()
        row.label(text="Type:")

        row = row.row()
        row.prop(
            data=driver,
            property='type',
            text="")

        row.scale_x = 2

        if driver.type == 'SCRIPTED':
            row = row.row()
            row.prop(
                data=driver,
                property='use_self')

        if driver.type == 'SCRIPTED':
            row = layout.row()
            row.label(text="Expression:")

            row = row.row()
            row.prop(
                data=driver,
                property='expression',
                text="")

            row.scale_x = 4

        row = layout.row(align=True)

        row.operator(
            operator='driver.blenrig_variable_add',
            icon='ADD')

        row.operator(
            operator='driver.blenrig_driver_update',
            icon='FILE_REFRESH')

        for i, v in enumerate(driver.variables):
            area_parent = layout.row()
            area = area_parent.column(align=True)
            box = area.box()
            box2 = area_parent.box()
            row = box.row()

            op = row.operator(
                operator='driver.blenrig_variable_remove',
                icon='X',
                text="",
                emboss=False)

            op.index = i

            row.prop(
                data=driver.variables[i],
                property='name',
                text="")

            row = row.row()

            row.prop(
                data=driver.variables[i],
                property='type',
                text="")

            row.scale_x = 2

            row2 = box2.column(align=False)

            op_copy = row2.operator(
                operator='driver.blenrig_variable_copy',
                text="",
                icon='PASTEDOWN')

            op_copy.index = i

            row3 = box2.column(align=True)

            op_move_top = row3.operator(
                operator='driver.blenrig_variable_move',
                text="",
                icon='TRIA_UP_BAR')

            op_move_top.index = i
            op_move_top.type = 'TOP'

            op_move_up = row3.operator(
                operator='driver.blenrig_variable_move',
                text="",
                icon='TRIA_UP')

            op_move_up.index = i
            op_move_up.type = 'UP'

            op_move_down = row3.operator(
                operator='driver.blenrig_variable_move',
                text="",
                icon='TRIA_DOWN')

            op_move_down.index = i
            op_move_down.type = 'DOWN'

            op_move_bottom = row3.operator(
                operator='driver.blenrig_variable_move',
                text="",
                icon='TRIA_DOWN_BAR')

            op_move_bottom.index = i
            op_move_bottom.type = 'BOTTOM'

            if driver.variables[i].type == 'SINGLE_PROP':
                row = box.row(align=True)
                row.prop(
                    data=driver.variables[i].targets[0],
                    property='id_type',
                    icon_only=True)

                row.prop(
                    data=driver.variables[i].targets[0],
                    property='id',
                    text="")

                if driver.variables[i].targets[0].id:
                    row = box.row(align=True)
                    row.prop(
                        data=driver.variables[i].targets[0],
                        property='data_path',
                        text="",
                        icon='RNA')
            elif driver.variables[i].type == 'TRANSFORMS':
                target = driver.variables[i].targets[0]

                col = box.column(align=True)
                col.prop(
                    data=target,
                    property='id',
                    text="Object",
                    expand=True)

                if target and target.id and target.id.type == 'ARMATURE':
                    col.prop_search(
                        data=target,
                        property='bone_target',
                        search_data=target.id.data,
                        search_property='bones',
                        text="Bone",
                        icon='BONE_DATA')

                row = box.row()
                col = row.column(align=True)

                col.prop(
                    data=driver.variables[i].targets[0],
                    property='transform_type',
                    text="Type")

                if driver.variables[i].targets[0].transform_type in ('ROT_X', 'ROT_Y', 'ROT_Z', 'ROT_W'):
                    col.prop(
                        data=driver.variables[i].targets[0],
                        property='rotation_mode',
                        text="Mode")

                col.prop(
                    data=driver.variables[i].targets[0],
                    property='transform_space',
                    text="Space")
            elif driver.variables[i].type == 'ROTATION_DIFF':
                for i, target in enumerate(driver.variables[i].targets):
                    col = box.column(align=True)

                    col.prop(
                        data=target,
                        property='id',
                        text="Object " + str(i + 1),
                        expand=True)

                    if target.id and target.id.type == 'ARMATURE':
                        col.prop_search(
                            data=target,
                            property='bone_target',
                            search_data=target.id.data,
                            search_property='bones',
                            text="Bone",
                            icon='BONE_DATA')
            elif driver.variables[i].type == 'LOC_DIFF':
                for i, target in enumerate(driver.variables[i].targets):
                    row = box.column()
                    col = row.column(align=True)

                    col.prop(
                        data=target,
                        property='id',
                        text="Object " + str(i + 1),
                        expand=True)

                    if target.id and target.id.type == 'ARMATURE':
                        col.prop_search(
                            data=target,
                            property='bone_target',
                            search_data=target.id.data,
                            search_property='bones',
                            text="Bone",
                            icon='BONE_DATA')

                    col.prop(
                        data=target,
                        property='transform_space',
                        text="Space")


class MESH_UL_BlenRig_shape_keys_plus(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        skp = context.scene.shape_keys_plus
        obj = active_data
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        key_block = item

        parents = utils.update_cache()['parents'][index]
        parent = get(parents, 0, None)
        is_folder = utils.is_key_folder(key_block)
        is_selected = utils.shape_key_selected(index)
        selections = utils.selected_shape_keys()

        use_edit_mode = obj.use_shape_key_edit_mode and obj.type == 'MESH'

        l1 = layout.row(align=True)
        l1.scale_x = 0.5

        # Check if this shape key belongs to a folder.
        if parent:
            # Get the number of folders this shape key is stacked in.
            for _ in range(utils.get_folder_stack_value(parent)):
                # Use the customizable folder indentation.
                for _ in range(skp.shape_key_indent_scale):
                    l1.separator(factor=2)

        if is_folder:
            icon_pair_value = utils.block_value(key_block.vertex_group, utils.icons)
            icon_swap_value = utils.block_value(key_block.vertex_group, utils.icons_swap)
            expand_value = utils.block_value(key_block.vertex_group, utils.expand)
            icon_pair = utils.get_icon_pair(icon_pair_value)
            icon_swap = icon_swap_value == 1

            if expand_value > 0:
                icon = icon_pair[1 if icon_swap else 0]
            else:
                icon = icon_pair[0 if icon_swap else 1]

            # Align the folder toggle button with the shape key icons.
            l1.separator(factor=3)

            op = l1.operator(
                operator='object.blenrig_folder_toggle',
                text="",
                icon=icon,
                emboss=False)

            op.index = index

            l2 = l1.row(align=True)
            l2.scale_x = 2
            l2.separator(factor=0.5)

            l2.prop(
                data=key_block,
                property='name',
                text="",
                emboss=False)
        else:
            l2 = l1.row()
            l2.scale_x = 2
            l2.active = not selections or is_selected

            l2.prop(
                data=key_block,
                property='name',
                text="",
                emboss=False,
                icon='FILE_TICK' if is_selected else 'SHAPEKEY_DATA')

        row = layout.row(align=True)

        if is_folder:
            if key_block.mute or (obj.mode == 'EDIT' and not use_edit_mode):
                row.active = False

            op = row.operator(
                operator='object.blenrig_folder_ungroup',
                text="",
                icon='X',
                emboss=False)

            op.index = index
        else:
            if key_block.mute or (obj.mode == 'EDIT' and not use_edit_mode):
                row.active = False
            if not item.id_data.use_relative:
                row.prop(
                    data=key_block,
                    property='frame',
                    text="",
                    emboss=False)
            elif index > 0:
                can_edit = not selections or selections and is_selected

                if can_edit:
                    row.prop(
                        data=key_block,
                        property='value',
                        text="",
                        emboss=False)
                else:
                    row.active = False
                    row.alignment = 'RIGHT'
                    row.label(text='{0:.3f}'.format(key_block.value))

            row.prop(
                data=key_block,
                property='mute',
                text="",
                icon='CHECKBOX_HLT',
                emboss=False)

            if index > 0 and not is_folder:
                op = row.operator(
                    operator='object.blenrig_shape_key_select',
                    text="",
                    # icon='CHECKBOX_HLT' if is_selected else 'CHECKBOX_DEHLT',
                    # emboss=False)
                    icon='LAYER_ACTIVE' if is_selected else 'REMOVE',
                    emboss=False)

                op.index = index
                op.mode = 'TOGGLE'

    def draw_filter(self, context, layout):
        skp = context.scene.shape_keys_plus

        row = layout.row()

        subrow = row.row(align=True)

        subrow.prop(
            data=self,
            property='filter_name',
            text="")

        icon = 'ZOOM_OUT' if self.use_filter_invert else 'ZOOM_IN'

        subrow.prop(
            data=self,
            property='use_filter_invert',
            text="",
            icon=icon)

        icon = 'FILE_FOLDER'

        subrow.prop(
            data=skp,
            property='show_filtered_folder_contents',
            text="",
            icon=icon)

        subrow = row.row(align=True)

        icon = 'HIDE_OFF'

        subrow.prop(
            data=skp,
            property='shape_key_limit_to_active',
            text="",
            icon=icon)

        if skp.shape_key_limit_to_active:
            subrow.prop(
                data=skp,
                property='filter_active_threshold',
                text="")

            icon = 'TRIA_LEFT' if skp.filter_active_below else 'TRIA_RIGHT'

            subrow.prop(
                data=skp,
                property='filter_active_below',
                text="",
                icon=icon)

    def filter_items(self, context, data, propname):
        flt_flags = []
        flt_name_flags = []
        flt_neworder = []

        skp = context.scene.shape_keys_plus
        shape_keys = context.object.data.shape_keys
        key_blocks = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list
        filtering_by_name = False
        name_filters = [False] * len(key_blocks)

        def filter_set(i, f):
            # self.bitflag_filter_item allows a shape key to be shown.
            # 0 will prevent a shape key from being shown.
            flt_flags[i] = self.bitflag_filter_item if f else 0

        def filter_get(i):
            return flt_flags[i] != 0

        if self.filter_name:
            filtering_by_name = True

            flt_flags = helper_funcs.filter_items_by_name(
                self.filter_name,
                self.bitflag_filter_item, key_blocks, 'name')

            for i in range(len(flt_flags)):
                if flt_flags[i] == self.bitflag_filter_item:
                    name_filters[i] = True
        else:
            # Initialize every shape key as visible.
            flt_flags = [self.bitflag_filter_item] * len(key_blocks)

        for idx, key in enumerate(key_blocks):
            cache = utils.update_cache()
            parents = cache['parents'][idx]
            is_folder = utils.is_key_folder(key)

            hidden = False

            if parents:
                parent_collapsed = False

                for p in parents:
                    expand_value = utils.block_value(
                        p.vertex_group,
                        utils.expand)

                    if expand_value == 0:
                        parent_collapsed = True
                        break

                if parent_collapsed and not filtering_by_name:
                    hidden = True

            if hidden:
                filter_set(idx, False)

            if filtering_by_name and parents:
                for p in parents:
                    parent_index = utils.get_key_index(p)
                    parent_hidden = not name_filters[parent_index]

                    if name_filters[idx] and parent_hidden:
                        filter_set(parent_index, True)

            if skp.show_filtered_folder_contents:
                if is_folder and filter_get(idx):
                    children = cache['children'][idx]

                    for i in range(len(children)):
                        filter_set(idx + 1 + i, True)

            if skp.shape_key_limit_to_active:
                if is_folder:
                    filter_set(idx, False)
                else:
                    val = skp.filter_active_threshold
                    below = skp.filter_active_below

                    in_active_range = \
                        key.value <= val if \
                        below else \
                        key.value >= val

                    filter_set(idx, in_active_range)

        return flt_flags, flt_neworder


########################################################################
################################# MENUS ################################
########################################################################


class MESH_MT_blenrig_shape_key_add_specials(bpy.types.Menu):
    bl_label = "Shape Key Add Specials"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            row = layout.row()

            row.menu(
                menu='MESH_MT_blenrig_shape_key_add_specials_selected',
                text='Selected (' + str(len(selections)) + ')',
                icon='FILE_TICK')

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_add',
            icon='FILE_TEXT',
            text="New Shape From Mix")

        op.type = 'FROM_MIX'

        row = layout.row()

        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_add',
            icon='NEWFOLDER',
            text="New Folder")

        op.type = 'FOLDER'

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_remove',
            icon='CANCEL',
            text="Clear Shape Keys")

        op.type = 'CLEAR'

class MESH_MT_blenrig_shape_key_add_specials_selected(bpy.types.Menu):
    bl_label = "Shape Key Add Specials (Selected)"

    def draw(self, context):
        layout = self.layout

        op = layout.operator(
            operator='object.blenrig_shape_key_add',
            icon='FILE_TEXT',
            text="New Shape From Mix")

        op.type = 'FROM_MIX_SELECTED'


class MESH_MT_blenrig_shape_key_copy_specials(bpy.types.Menu):
    bl_label = "Shape Key Copy Specials"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            row = layout.row()

            row.menu(
                menu='MESH_MT_blenrig_shape_key_copy_specials_selected',
                text='Selected (' + str(len(selections)) + ')',
                icon='FILE_TICK')

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEFLIPDOWN',
            text="Copy Shape Key, Mirrored")

        op.type = 'MIRROR'

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEFLIPDOWN',
            text="Copy Shape Key, Mirrored (Topology)")

        op.type = 'MIRROR_TOPOLOGY'


class MESH_MT_blenrig_shape_key_copy_specials_selected(bpy.types.Menu):
    bl_label = "Shape Key Copy Specials (Selected)"

    def draw(self, context):
        layout = self.layout

        op = layout.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEDOWN',
            text="Copy Shape Key")

        op.type = 'DEFAULT_SELECTED'

        op = layout.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEFLIPDOWN',
            text="Copy Shape Key, Mirrored")

        op.type = 'MIRROR_SELECTED'

        op = layout.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEFLIPDOWN',
            text="Copy Shape Key, Mirrored (Topology)")

        op.type = 'MIRROR_TOPOLOGY_SELECTED'


# class MESH_MT_blenrig_shape_key_remove_specials(bpy.types.Menu):
#     bl_label = "Shape Key Removal Specials"

#     def draw(self, context):
#         selections = utils.selected_shape_keys()

#         layout = self.layout

        # if selections:
        #     row = layout.row()

        #     row.menu(
        #         menu='MESH_MT_blenrig_shape_key_remove_specials_selected',
        #         text='Selected (' + str(len(selections)) + ')',
        #         icon='FILE_TICK')

        # row = layout.row()
        # row.enabled = not selections

        # op = row.operator(
        #     operator='object.blenrig_shape_key_remove',
        #     icon='CANCEL',
        #     text="Clear Shape Keys")

        # op.type = 'CLEAR'


# class MESH_MT_blenrig_shape_key_remove_specials_selected(bpy.types.Menu):
#     bl_label = "Shape Key Removal Specials (Selected)"

#     def draw(self, context):
#         layout = self.layout

#         op = layout.operator(
#             operator='object.blenrig_shape_key_remove',
#             icon='REMOVE',
#             text="Remove Shape Key")

#         op.type = 'DEFAULT_SELECTED'


class MESH_MT_blenrig_shape_key_other_specials(bpy.types.Menu):
    bl_label = "Other Shape Key Specials"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            row = layout.row()

            row.menu(
                menu='MESH_MT_blenrig_shape_key_other_specials_selected',
                text='Selected (' + str(len(selections)) + ')',
                icon='FILE_TICK')

        obj = context.object
        active_key = obj.active_shape_key
        is_active_folder = active_key and utils.is_key_folder(active_key)

        if active_key:
            row = layout.row()
            row.enabled = not selections

            row.menu(
                menu='OBJECT_MT_blenrig_shape_key_parent',
                icon='FILE_PARENT')

        row = layout.row()
        row.enabled = not selections

        if is_active_folder:
            row.menu(
                menu='OBJECT_MT_blenrig_folder_icon',
                icon='COLOR')
        else:
            row.menu(
                menu='OBJECT_MT_blenrig_folder_icon',
                icon='COLOR',
                text="Set Default Folder Icon to")

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.shape_key_mirror',
            icon='ARROW_LEFTRIGHT')

        op.use_topology = False

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.shape_key_mirror',
            text="Mirror Shape Key (Topology)",
            icon='ARROW_LEFTRIGHT')

        op.use_topology = True

        row = layout.row()
        row.enabled = not selections

        row.operator(
            operator='object.shape_key_transfer',
            icon='COPY_ID')

        row = layout.row()
        row.enabled = not selections

        row.operator(
            operator='object.join_shapes',
            icon='COPY_ID')

class MESH_MT_blenrig_shape_key_other_specials_selected(bpy.types.Menu):
    bl_label = "Other Shape Key Specials (Selected)"

    def draw(self, context):
        layout = self.layout

        layout.menu(
            menu='OBJECT_MT_blenrig_shape_key_parent_selected',
            text='Set Parent to',
            icon='FILE_PARENT')


class OBJECT_MT_blenrig_shape_key_parent(bpy.types.Menu):
    bl_label = "Set Parent to"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            layout.enabled = False

        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            key_blocks = shape_keys.key_blocks
            parents = utils.get_key_parents(active_key)
            parent = get(parents, 0, None)

            op = layout.operator(
                operator='object.blenrig_shape_key_parent',
                text='New Folder',
                icon='NEWFOLDER')

            op.type = 'NEW'
            op.child = active_key.name
            op.parent = parent.name if parent else ""

            if parent:
                # Only show the "Clear Parents" operator if the key has more
                # than one parent, otherwise only the "Unparent" operator.
                if len(parents) > 1:
                    op = layout.operator(
                        operator='object.blenrig_shape_key_parent',
                        text="Clear Parents",
                        icon='CANCEL')

                    op.type = 'CLEAR'
                    op.child = active_key.name
                    op.parent = parent.name

                op = layout.operator(
                    operator='object.blenrig_shape_key_parent',
                    text="Unparent from " + parent.name,
                    icon='X')

                op.type = 'UNPARENT'
                op.child = active_key.name
                op.parent = parent.name

            # Only allow parenting to a folder that this shape key isn't already related to.
            children = utils.get_folder_children(active_key)

            for key in key_blocks:
                is_folder = utils.is_key_folder(key)
                is_current_key = key == active_key
                is_parent = key == parent
                is_child = key in children
                key_parents = utils.get_key_parents(key)
                valid = is_folder and not is_current_key and not is_parent and not is_child

                if valid:
                    op = layout.operator(
                        operator='object.blenrig_shape_key_parent',
                        text=("  " * len(key_parents)) + key.name,
                        icon='FILE_FOLDER')

                    op.type = 'PARENT'
                    op.child = active_key.name
                    op.parent = key.name


class OBJECT_MT_blenrig_shape_key_parent_selected(bpy.types.Menu):
    bl_label = "Set Parent to (Selected)"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        shape_keys = obj.data.shape_keys
        active_key = obj.active_shape_key

        if active_key:
            key_blocks = shape_keys.key_blocks

            op = layout.operator(
                operator='object.blenrig_shape_key_parent',
                text='New Folder',
                icon='NEWFOLDER')

            op.type = 'NEW_SELECTED'

            op = layout.operator(
                operator='object.blenrig_shape_key_parent',
                text="Clear Parents",
                icon='CANCEL')

            op.type = 'CLEAR_SELECTED'

            op = layout.operator(
                operator='object.blenrig_shape_key_parent',
                text="Unparent",
                icon='X')

            op.type = 'UNPARENT_SELECTED'

            for key in key_blocks:
                is_folder = utils.is_key_folder(key)
                key_parents = utils.get_key_parents(key)

                if is_folder:
                    op = layout.operator(
                        operator='object.blenrig_shape_key_parent',
                        text=("  " * len(key_parents)) + key.name,
                        icon='FILE_FOLDER')

                    op.type = 'PARENT_SELECTED'
                    op.parent = key.name


class OBJECT_MT_blenrig_folder_icon(bpy.types.Menu):
    bl_label = "Set Folder Icon to"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            layout.enabled = False

        skp = context.scene.shape_keys_plus
        obj = context.object

        active_key = obj.active_shape_key
        is_active_folder = active_key and utils.is_key_folder(active_key)

        icons_default = skp.folder_icon_pair
        icons_default_swap = skp.folder_icon_swap

        icon_default_pair = utils.get_icon_pair(icons_default)
        icon_default = icon_default_pair[int(icons_default_swap)]
        icon_default_swap = icon_default_pair[int(not icons_default_swap)]

        if is_active_folder:
            icons_block = utils.block_value(active_key.vertex_group, utils.icons)
            icons_swap_block = utils.block_value(active_key.vertex_group, utils.icons_swap) == 1

            icon_active_pair = utils.get_icon_pair(icons_block)
            icon_active = icon_active_pair[int(icons_swap_block)]
            icon_active_swap = icon_active_pair[not int(icons_swap_block)]

            op = layout.operator(
                operator='object.blenrig_folder_icon',
                icon=icon_default,
                text=icon_default_pair[2] + " (Default)")

            op.icons = icons_default
            op.swap = icons_default_swap
            op.set_as_default = False

            opposite = layout.column()
            opposite.enabled = False

            op = opposite.operator(
                operator='object.blenrig_folder_icon',
                icon=icon_default_swap,
                text="")

            layout.separator(factor=0.5)

            op = layout.operator(
                operator='object.blenrig_folder_icon',
                icon=icon_active_swap,
                text="Swap (Active)")

            op.icons = icons_block
            op.swap = not icons_swap_block
            op.set_as_default = False

            opposite = layout.column()
            opposite.enabled = False

            op = opposite.operator(
                operator='object.blenrig_folder_icon',
                icon=icon_active,
                text="")

            layout.separator(factor=0.5)

        layout.menu(
            menu='OBJECT_MT_blenrig_folder_icons_standard',
            text="Standard")

        layout.menu(
            menu='OBJECT_MT_blenrig_folder_icons_special',
            text="Special")

        layout.menu(
            menu='OBJECT_MT_blenrig_folder_icons_misc',
            text="Miscellaneous")


class OBJECT_MT_blenrig_folder_icons_standard(bpy.types.Menu):
    bl_label = "Set Folder Icon to"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            layout.enabled = False

        skp = context.scene.shape_keys_plus
        obj = context.object

        active_key = obj.active_shape_key
        is_active_folder = active_key and utils.is_key_folder(active_key)

        for i, p in enumerate(utils.icon_pairs_standard):
            op = layout.operator(
                operator='object.blenrig_folder_icon',
                icon=p[0],
                text=p[2])

            op.icons = p[-1]
            op.swap = False
            op.set_as_default = not is_active_folder

            opposite = layout.column()
            opposite.enabled = False

            op = opposite.operator(
                operator='object.blenrig_folder_icon',
                icon=p[1],
                text=p[3])

            if i < len(utils.icon_pairs_standard) - 1:
                layout.separator(factor=0.5)


class OBJECT_MT_blenrig_folder_icons_special(bpy.types.Menu):
    bl_label = "Set Folder Icon to"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            layout.enabled = False

        skp = context.scene.shape_keys_plus
        obj = context.object

        active_key = obj.active_shape_key
        is_active_folder = active_key and utils.is_key_folder(active_key)

        for i, p in enumerate(utils.icon_pairs_special):
            op = layout.operator(
                operator='object.blenrig_folder_icon',
                icon=p[0],
                text=p[2])

            op.icons = p[-1]
            op.swap = False
            op.set_as_default = not is_active_folder

            opposite = layout.column()
            opposite.enabled = False

            op = opposite.operator(
                operator='object.blenrig_folder_icon',
                icon=p[1],
                text=p[3])

            if i < len(utils.icon_pairs_special) - 1:
                layout.separator(factor=0.5)


class OBJECT_MT_blenrig_folder_icons_misc(bpy.types.Menu):
    bl_label = "Set Folder Icon to"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            layout.enabled = False

        skp = context.scene.shape_keys_plus
        obj = context.object

        active_key = obj.active_shape_key
        is_active_folder = active_key and utils.is_key_folder(active_key)

        for i, p in enumerate(utils.icon_pairs_misc):
            op = layout.operator(
                operator='object.blenrig_folder_icon',
                icon=p[0],
                text=p[2])

            op.icons = p[-1]
            op.swap = False
            op.set_as_default = not is_active_folder

            opposite = layout.column()
            opposite.enabled = False

            op = opposite.operator(
                operator='object.blenrig_folder_icon',
                icon=p[1],
                text=p[3])

            if i < len(utils.icon_pairs_misc) - 1:
                layout.separator(factor=0.5)

class MESH_MT_blenrig_shape_key_generic_shapekeys(bpy.types.Menu):
    bl_label = "Generic BlenRig Shape Keys"

    def draw(self, context):
        selections = utils.selected_shape_keys()

        layout = self.layout

        if selections:
            row = layout.row()

            row.menu(
                menu='MESH_MT_blenrig_shape_key_copy_specials_selected',
                text='Selected (' + str(len(selections)) + ')',
                icon='FILE_TICK')

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEFLIPDOWN',
            text="Copy Shape Key, Mirrored")

        op.type = 'MIRROR'

        row = layout.row()
        row.enabled = not selections

        op = row.operator(
            operator='object.blenrig_shape_key_copy',
            icon='PASTEFLIPDOWN',
            text="Copy Shape Key, Mirrored (Topology)")

        op.type = 'MIRROR_TOPOLOGY'

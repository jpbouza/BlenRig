import bpy
from bpy_extras import view3d_utils
from math import radians, degrees
from mathutils import Matrix, Vector


# GET BLENRIG ARMATURE
def find_blenrig_armature_object(context):
    for ob in context.scene.objects:
        if ob.type == 'ARMATURE':
            if ob.data.rig_name == 'BlenRig':
                context.scene.blenrig_guide.arm_obj = ob
                return ob
    return None

def get_armature_object(context):
    if not context.scene.blenrig_guide.arm_obj:
        return find_blenrig_armature_object(context)
    return context.scene.blenrig_guide.arm_obj

def go_blenrig_pose_mode(context):
    if context.mode == 'POSE':
        return True
    arm = get_armature_object(context)
    if not arm:
        return False
    if context.mode != 'OBJECT':
        set_mode('OBJECT')
    if context.active_object != arm:
        set_active_object(context, arm)
    set_mode('POSE')
    return True

# REPROPORTION
def set_reproportion_on(context=None):
    if context:
        context.pose_object.data.reproportion = True
        context.pose_object.show_in_front = True

def set_reproportion_off(context=None):
    if context:
        context.pose_object.data.reproportion = False
        context.pose_object.show_in_front = False

# Display Type
def set_display_type(context, mode):
    context.pose_object.data.display_type = mode

# POSE
def deselect_all_pose_bones(context=None, invert=False):
    if context:
        for b in context.pose_object.pose.bones: #context.selected_pose_bones_from_active_object:
            b.bone.select = invert
    else:
        bpy.ops.pose.select_all(action='DESELECT' if not invert else 'SELECT')

def select_all_pose_bones(context=None):
    deselect_all_pose_bones(context, True)

# EDIT
def deselect_all_edit_bones(context=None, invert=False):
    if context:
        for b in context.active_object.data.edit_bones:
            b.select = b.select_head = b.select_tail = invert
    else:
        bpy.ops.armature.select_all(action='DESELECT' if not invert else 'SELECT')

def select_all_edit_bones(context=None):
    deselect_all_edit_bones(context, True)

# POSE
def deselect_pose_bone(context, bone_name, invert=False):
    if not context:
        return
    bone = context.pose_object.data.bones.get(bone_name, None)
    if bone:
        bone.select = invert

def select_pose_bone(context, bone_name):
    deselect_pose_bone(context, bone_name, True)
    bones = context.pose_object.data.bones
    bone = bones.get(bone_name, None)
    if bone:
        bones.active = bone

# EDIT
def deselect_edit_bone(context, bone_name, invert=False):
    if not context:
        return
    bone = context.active_object.data.edit_bones.get(bone_name, None)
    if bone:
        bone.select = bone.select_head = bone.select_tail = invert

def select_edit_bone(context, bone_name):
    deselect_edit_bone(context, bone_name, True)

# POSE
def select_pose_bones(context, *bone_names):
    if not context:
        return
    bones = context.pose_object.data.bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.select = True
            bones.active = bone

def deselect_pose_bones(context, *bone_names):
    if not context:
        return
    bones = context.pose_object.data.bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.select = False

# EDIT
def select_edit_bones(context, *bone_names):
    if not context:
        return
    bones = context.active_object.data.edit_bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.select = bone.select_head = bone.select_tail = True

def deselect_edit_bones(context, *bone_names):
    if not context:
        return
    bones = context.active_object.data.edit_bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.select = bone.select_head = bone.select_tail = False

# POSE / OBJECT
def hide_bones(context, *bone_names):
    if not context:
        return
    bones = context.pose_object.data.bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.hide = True

def unhide_bones(context, *bone_names):
    if not context:
        return
    bones = context.pose_object.data.bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.hide = False

# EDIT
def hide_edit_bones(context, *bone_names):
    if not context:
        return
    bones = context.active_object.data.edit_bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.hide = True

def unhide_edit_bones(context, *bone_names):
    if not context:
        return
    bones = context.active_object.data.edit_bones
    for name in bone_names:
        bone = bones.get(name, None)
        if bone:
            bone.hide = False

# POSE / OBJECT
def hide_all_bones(context):
    if context:
        for bone in context.pose_object.data.bones:
            bone.hide = True
    else:
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.pose.hide(unselected=False)

def unhide_all_bones(context):
    if context:
        for bone in context.pose_object.data.bones:
            bone.hide = False
    else:
        bpy.ops.pose.reveal()
        bpy.ops.pose.select_all(action='DESELECT')

def hide_selected_pose_bones(context):
    if context:
        for pose_bone in context.selected_pose_bones_from_active_object:
            pose_bone.bone.hide = True
    else:
        bpy.ops.pose.hide(unselected=False)

def hide_bones_in_layer(context, *layer_numbers, state=True):
    if not context:
        return
    pbones = context.pose_object.pose.bones
    for layer in layer_numbers:
        for b in pbones:
            if b.bone.layers[layer] == True:
                if state == True:
                    b.bone.hide = True
                if state == False:
                    b.bone.hide = False

# EDIT
def hide_all_edit_bones(context):
    for bone in context.active_object.data.edit_bones:
        bone.hide = True

def unhide_all_dit__bones(context):
    for bone in context.active_object.data.edit_bones:
        bone.hide = False

def hide_selected_edit_bones(context):
    for pose_bone in context.selected_editable_bones:
        pose_bone.bone.hide = True

###########

def set_viewpoint(viewpoint='RIGHT'):
    bpy.ops.view3d.view_axis(type=viewpoint)

def set_view_perspective(context, enable: bool):
    if enable and not context.space_data.region_3d.is_perspective:
        bpy.ops.view3d.view_persportho()
    elif not enable and context.space_data.region_3d.is_perspective:
        bpy.ops.view3d.view_persportho()

def frame_selected():
    bpy.ops.view3d.view_selected(use_all_regions=False)

def frame_points(*points):
    return

############ IMAGE UTILS

from os.path import exists, isfile, join, dirname
guides_dir = dirname(__file__)
def load_guide_image(guide_name: str, img_name: str, ghost: bool = True):
    path = join(guides_dir, guide_name, 'images', img_name)
    if not exists(path) or not isfile(path):
        return None
    img = bpy.data.images.load(path, check_existing=True)
    if ghost:
        img.name = '.' + img.name
    return img

def hide_image(image):
    if image.name.startswith('.'):
        return
    image.name = '.' + image.name

############

def get_regiondata_view3d(context):
    if not context:
        context = bpy.context
    return context.region, context.space_data.region_3d

def spacecoordstoscreencoords(context, p):
    return view3d_utils.location_3d_to_region_2d(*get_regiondata_view3d(context), p, default=None)

def inside(p, _p, _s):
    return ((_p[0] + _s[0]) > p[0] > _p[0]) and ((_p[1] + _s[1]) > p[1] > _p[1])

def near(a, b, d):
    return abs(a[0] - b[0]) < d and abs(a[1] - b[1]) < d

def set_mode(mode: str):
    bpy.ops.object.mode_set(mode=mode)

def set_active_object(context, _object):
    _object.select_set(state=True)
    context.view_layer.objects.active = _object

def toggle_pose_x_mirror(context, state):
    if context.mode == 'POSE':
        context.pose_object.pose.use_mirror_x = state

def move_global_z():
    bpy.ops.transform.translate('INVOKE_DEFAULT', orient_type ='GLOBAL', constraint_axis=(False, False, True), release_confirm=True)

def snap_selected_to_cursor():
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

def cursor_to_selected():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            c = bpy.context.copy()
            c['area'] = area
        else:
            print("No View3D, aborting.")

    bpy.ops.view3d.snap_cursor_to_active(c)

def mirror_pose():
    bpy.ops.pose.copy()
    bpy.ops.pose.paste(flipped=True)

#### Object to Temp Collection

def blenrig_temp_link(object):
    temp_collection = bpy.data.collections.get("BlenRig_temp")
    temp_objects = object
    if bpy.context.scene.collection.children.find("BlenRig_temp") == -1:
        if temp_collection:
                bpy.context.scene.collection.children.link(temp_collection)
        else:
            temp_collection = bpy.data.collections.new("BlenRig_temp")
            bpy.context.scene.collection.children.link(temp_collection)
        for ob in temp_objects:
            try:
                temp_collection.objects.link(ob)
            except:
                pass

def blenrig_temp_unlink():
    temp_collection = bpy.data.collections.get("BlenRig_temp")
    if bpy.context.scene.collection.children.find("BlenRig_temp") != -1:
        for ob in temp_collection.objects:
            temp_collection.objects.unlink(ob)
        bpy.context.scene.collection.children.unlink(temp_collection)

face_rig_objects = []

def collect_facemask():
    face_rig_objects.clear()
    for ob in bpy.data.objects:
        if hasattr(ob, 'parent'):
            if ob.parent == bpy.context.active_object:
                if "FaceRigMesh" in ob.name:
                    face_rig_objects.append(ob)
    return face_rig_objects

mdef_cage_objects = []

def collect_cage():
    mdef_cage_objects.clear()
    for ob in bpy.data.objects:
        if "MdefCage" in ob.name:
            mdef_cage_objects.append(ob)
    return mdef_cage_objects

mdef_weights_model_objects = []

def collect_mdef_weights_model():
    mdef_weights_model_objects.clear()
    for ob in bpy.data.objects:
        if "MDefWeightsModel" in ob.name:
            mdef_weights_model_objects.append(ob)
    return mdef_weights_model_objects

lattice_objects = []

def collect_lattice_objects():
    lattice_objects.clear()
    for ob in bpy.data.objects:
        if hasattr(ob, 'type') and hasattr(ob, 'parent'):
            if ob.type == 'LATTICE' and ob.parent == bpy.context.scene.blenrig_guide.arm_obj:
                lattice_objects.append(ob)
    return lattice_objects

#### Local View

def switch_out_local_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            bpy.ops.view3d.localview()
            if space.local_view: #check if using local view
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region} #override context
                        bpy.ops.view3d.localview(override) #switch to global view

#### Deselect all objects
def deselect_all_objects(context):
    if context.mode != 'OBJECT':
        set_mode('OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

### Check if object has modifiers
def check_mod_type(mod_type):
    active = bpy.context.active_object
    if hasattr(active, 'modifiers'):
        for mod in active.modifiers:
            if hasattr(mod, 'type'):
                if mod.type == mod_type:
                    return True

def check_mod_type_name(mod_type, mod_name):
    active = bpy.context.active_object
    if hasattr(active, 'modifiers'):
        for mod in active.modifiers:
            if hasattr(mod, 'type'):
                if mod.type == mod_type:
                    if mod.name == mod_name:
                        return True

#### Shapekey Creation
def add_shapekey(context, shape_name):
    ob=bpy.context.object
    if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys'):
        if hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            if shapekeys.find('Basis') == -1:
                Basis = ob.shape_key_add(from_mix=False)
                Basis.name = 'Basis'
            if shape_name in shapekeys:
                index = ob.data.shape_keys.key_blocks.find(shape_name)
                ob.active_shape_key_index = index
                ob.data.shape_keys.key_blocks[index].value = 1.0
                ob.use_shape_key_edit_mode = True
                #Rename Shapekeys Datablock
                ob.data.shape_keys.name = 'ShapeKeys'
            else:
                new_shape = ob.shape_key_add(from_mix=False)
                new_shape.name = shape_name
                if shape_name in shapekeys:
                    index = ob.data.shape_keys.key_blocks.find(shape_name)
                    ob.active_shape_key_index = index
                    ob.data.shape_keys.key_blocks[index].value = 1.0
                    ob.use_shape_key_edit_mode = True
                    #Rename Shapekeys Datablock
                    ob.data.shape_keys.name = 'ShapeKeys'
        #If no Shapekeys present
        else:
            Basis = ob.shape_key_add(from_mix=False)
            Basis.name = 'Basis'
            shapekeys = ob.data.shape_keys.key_blocks
            new_shape = ob.shape_key_add(from_mix=False)
            new_shape.name = shape_name
            #Rename Shapekeys Datablock
            ob.data.shape_keys.name = 'ShapeKeys'
            if shape_name in shapekeys:
                index = ob.data.shape_keys.key_blocks.find(shape_name)
                ob.active_shape_key_index = index
                ob.data.shape_keys.key_blocks[index].value = 1.0
                ob.use_shape_key_edit_mode = True

### Add Drivers
driver_data_path = []
driver_array_index = []

def add_drivers(object_item,d_data_path, d_array_index, array_check, d_extrapolation, d_hide, d_lock, d_mute, d_expression, d_type):
    driver_data_path[:] = []
    driver_array_index[:] = []
    if array_check == 'no_array':
        fcurve = object_item.driver_add(d_data_path)
    if array_check == 'array':
        fcurve = object_item.driver_add(d_data_path, d_array_index)
    fcurve.extrapolation = d_extrapolation
    fcurve.hide = d_hide
    fcurve.lock = d_lock
    fcurve.mute = d_mute
    if d_type == 'SCRIPTED':
        fcurve.driver.expression = d_expression
    fcurve.driver.type = d_type
    for m in fcurve.modifiers:
        fcurve.modifiers.remove(m)
    driver_data_path.append(fcurve.data_path)
    driver_array_index.append(fcurve.array_index)
    return (fcurve)

def add_shapekeys_driver(object_item,d_data_path, d_type, d_expression):
    driver_data_path[:] = []
    driver_array_index[:] = []
    fcurve = object_item.driver_add(d_data_path)
    fcurve.extrapolation = 'CONSTANT'
    fcurve.hide = False
    fcurve.lock = False
    fcurve.mute = False
    fcurve.driver.type = d_type
    if d_type == 'SCRIPTED':
        fcurve.driver.expression = d_expression
    for m in fcurve.modifiers:
        fcurve.modifiers.remove(m)
    driver_data_path.append(fcurve.data_path)
    driver_array_index.append(fcurve.array_index)
    return (fcurve)


def add_vars(current_driver, v_name, v_type, t_id, t_bone_target, t_data_path, t_transform_space, t_transform_type, t_rotation_mode):
    var = current_driver.driver.variables.new()
    var.name = v_name
    var.type = v_type
    target = var.targets[0]
    target.id = t_id
    if v_type == 'SINGLE_PROP':
        target.data_path = t_data_path
    if v_type == 'TRANSFORMS':
        target.bone_target = t_bone_target
        target.transform_space = t_transform_space
        target.transform_type = t_transform_type
        target.rotation_mode = t_rotation_mode

def add_vars_shapekeys(current_driver, v_name, ob_shapkeys, shape_name):
    var = current_driver.driver.variables.new()
    var.name = v_name
    var.type = 'SINGLE_PROP'
    target = var.targets[0]
    target.id_type = 'KEY'
    target.id = bpy.data.shape_keys[ob_shapkeys]
    target.data_path = 'key_blocks["' + shape_name + '"].value'


def add_mod_generator(current_driver, m_type, m_blend_in, m_blend_out, m_frame_start, m_frame_end, m_mode, m_mute, m_poly_order, m_use_additive, m_use_influence, m_use_restricted_range, m_co_0, m_co_1):
    mod = current_driver.modifiers.new(m_type)
    mod.blend_in = m_blend_in
    mod.blend_out = m_blend_out
    mod.frame_start = m_frame_start
    mod.frame_end = m_frame_end
    mod.mode = m_mode
    mod.mute = m_mute
    mod.poly_order = m_poly_order
    mod.use_additive = m_use_additive
    mod.use_influence = m_use_influence
    mod.use_restricted_range = m_use_restricted_range
    mod.coefficients[0] = m_co_0
    mod.coefficients[1] = m_co_1

def add_mod_generator_angle(current_driver, angle):
    mod = current_driver.modifiers.new('GENERATOR')
    mod.blend_in = 0.0
    mod.blend_out = 0.0
    mod.frame_start = 0.0
    mod.frame_end = 0.0
    mod.mode = 'POLYNOMIAL'
    mod.mute = False
    mod.poly_order = 1
    mod.use_additive = False
    mod.use_influence = False
    mod.use_restricted_range = False
    mod.coefficients[0] = 0.0
    mod.coefficients[1] = 1.0/radians(angle)

def add_mod_generator_location(current_driver, loc):
    mod = current_driver.modifiers.new('GENERATOR')
    mod.blend_in = 0.0
    mod.blend_out = 0.0
    mod.frame_start = 0.0
    mod.frame_end = 0.0
    mod.mode = 'POLYNOMIAL'
    mod.mute = False
    mod.poly_order = 1
    mod.use_additive = False
    mod.use_influence = False
    mod.use_restricted_range = False
    mod.coefficients[0] = 0.0
    mod.coefficients[1] = 1.0/loc

def add_mod_generator_location_offset(current_driver, x_offset, loc):
    mod = current_driver.modifiers.new('GENERATOR')
    mod.blend_in = 0.0
    mod.blend_out = 0.0
    mod.frame_start = 0.0
    mod.frame_end = 0.0
    mod.mode = 'POLYNOMIAL'
    mod.mute = False
    mod.poly_order = 1
    mod.use_additive = False
    mod.use_influence = False
    mod.use_restricted_range = False
    mod.coefficients[0] = x_offset
    mod.coefficients[1] = 1.0/loc

### Check if Shapekey has a Driver
def check_shapekey_driver(shape_name):
    active = bpy.context.active_object
    if hasattr(active, 'data') and hasattr(active.data, 'shape_keys') and hasattr(active.data.shape_keys, 'key_blocks'):
        if hasattr(active.data.shape_keys.key_blocks, 'data') and hasattr(active.data.shape_keys.key_blocks.data, 'animation_data'):
            if hasattr(active.data.shape_keys.key_blocks.data.animation_data, 'drivers'):
                for driver in active.data.shape_keys.key_blocks.data.animation_data.drivers:
                    if shape_name in driver.data_path:
                        return True

### Get Local Transforms of Bone For Driver Updater (Code by Niabot)
def bone_local_transforms(armature, bname, transform_type):
    bone        = armature.data.bones[bname]
    bone_ml     = bone.matrix_local
    bone_pose   = armature.pose.bones[bname]
    bone_pose_m = bone_pose.matrix

    if bone.parent:

        parent        = bone.parent
        parent_ml     = parent.matrix_local
        parent_pose   = bone_pose.parent
        parent_pose_m = parent_pose.matrix

        object_diff = parent_ml.inverted() @ bone_ml
        pose_diff   = parent_pose_m.inverted() @ bone_pose_m
        local_diff  = object_diff.inverted() @ pose_diff

    else:

        local_diff = bone_ml.inverted() @ bone_pose_m

    if transform_type == 'rot_x':
        transform = local_diff.to_euler('ZYX')[0]
    if transform_type == 'rot_y':
        transform = local_diff.to_euler('XZY')[1]
    if transform_type == 'rot_z':
        transform = local_diff.to_euler('XYZ')[2]
    if transform_type == 'loc_x':
        transform = local_diff.to_translation()[0]
    if transform_type == 'loc_y':
        transform = local_diff.to_translation()[1]
    if transform_type == 'loc_z':
        transform = local_diff.to_translation()[2]
    if transform_type == 'scale_x':
        transform = local_diff.to_scale()[0]
    if transform_type == 'scale_y':
        transform = local_diff.to_scale()[1]
    if transform_type == 'scale_z':
        transform = local_diff.to_scale()[2]
    return transform

#Actions Guide Properties Functions

#Drivers Update
def drivers_update():
    for d in bpy.context.active_object.animation_data.drivers:
        d.driver.type = d.driver.type

#Mouth Corners
def corner_out_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_mouth_corner_out
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].OUT_LIMIT_L = prop_value
                pbones["mouth_corner_R"].OUT_LIMIT_R = prop_value
                pbones["mouth_ctrl"].OUT_LIMIT = prop_value
                #Apply Bone Transform
                pbones["mouth_corner_L"].location[0] = -(prop_value)
                pbones["mouth_corner_R"].location[0] = prop_value

def corner_in_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_mouth_corner_in
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].IN_LIMIT_L = prop_value
                pbones["mouth_corner_R"].IN_LIMIT_R = prop_value
                pbones["mouth_ctrl"].IN_LIMIT = prop_value
                #Apply Bone Transform
                pbones["mouth_corner_L"].location[0] = prop_value
                pbones["mouth_corner_R"].location[0] = -(prop_value)

def corner_up_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_mouth_corner_up
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].UP_LIMIT_L = prop_value
                pbones["mouth_corner_R"].UP_LIMIT_R = prop_value
                pbones["mouth_ctrl"].SMILE_LIMIT = prop_value
                drivers_update()
                #Apply Bone Transform
                pbones["mouth_corner_L"].location[2] = prop_value
                pbones["mouth_corner_R"].location[2] = prop_value

def corner_down_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                guide_props = bpy.context.scene.blenrig_guide
                arm = guide_props.arm_obj
                prop_value = guide_props.guide_mouth_corner_down
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].DOWN_LIMIT_L = prop_value
                pbones["mouth_corner_R"].DOWN_LIMIT_R = prop_value
                pbones["mouth_ctrl"].constraints["Limit Rotation_NOREP"].min_y = radians(-90 * guide_props.guide_mouth_corner_up / guide_props.guide_mouth_corner_down)
                #Apply Bone Transform
                pbones["mouth_corner_L"].location[2] = -(prop_value)
                pbones["mouth_corner_R"].location[2] = -(prop_value)

def corner_back_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_mouth_corner_back
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].BACK_LIMIT_L = prop_value
                pbones["mouth_corner_R"].BACK_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["mouth_corner_L"].location[1] = -(prop_value)
                pbones["mouth_corner_R"].location[1] = -(prop_value)

def corner_forw_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_mouth_corner_forw
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].FORW_LIMIT_L = prop_value
                pbones["mouth_corner_R"].FORW_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["mouth_corner_L"].location[1] = prop_value
                pbones["mouth_corner_R"].location[1] = prop_value

#Jaw
def jaw_up_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_jaw_up
                pbones = arm.pose.bones

                #Update Properties
                pbones["maxi"].JAW_UP_LIMIT = prop_value
                #Apply Bone Transform
                pbones["maxi"].rotation_euler[0] = radians(prop_value)

def jaw_down_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_jaw_down
                pbones = arm.pose.bones

                #Update Properties
                pbones["maxi"].JAW_DOWN_LIMIT = prop_value
                #Apply Bone Transform
                pbones["maxi"].rotation_euler[0] = radians(-(prop_value))

#Cheeks
def cheek_up_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_cheek_up
                pbones = arm.pose.bones

                #Update Properties
                pbones["cheek_ctrl_L"].CHEEK_UP_LIMIT_L = prop_value
                pbones["cheek_ctrl_R"].CHEEK_UP_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["cheek_ctrl_L"].location[2] = prop_value
                pbones["cheek_ctrl_R"].location[2] = prop_value

def cheek_down_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_cheek_down
                pbones = arm.pose.bones

                #Update Properties
                pbones["cheek_ctrl_L"].CHEEK_DOWN_LIMIT_L = prop_value
                pbones["cheek_ctrl_R"].CHEEK_DOWN_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["cheek_ctrl_L"].location[2] = -(prop_value)
                pbones["cheek_ctrl_R"].location[2] = -(prop_value)

#Nose Frown
def nose_frown_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_nose_frown
                pbones = arm.pose.bones

                #Update Properties
                pbones["nose_frown_ctrl_L"].FROWN_LIMIT_L = prop_value
                pbones["nose_frown_ctrl_R"].FROWN_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["nose_frown_ctrl_L"].location[2] = prop_value
                pbones["nose_frown_ctrl_R"].location[2] = prop_value

#U_O_M
def u_o_m_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_u_o_m
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_ctrl"].U_M_CTRL_LIMIT = prop_value
                #Apply Bone Transform
                pbones["mouth_up_ctrl"].location[1] = prop_value
                pbones["mouth_low_ctrl"].location[1] = prop_value

#Mouth Frown
def mouth_frown_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_mouth_frown
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_frown_ctrl_L"].FROWN_LIMIT_L = prop_value
                pbones["mouth_frown_ctrl_R"].FROWN_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["mouth_frown_ctrl_L"].location[2] = -(prop_value)
                pbones["mouth_frown_ctrl_R"].location[2] = -(prop_value)

#Chin Frown
def chin_frown_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_chin_frown
                pbones = arm.pose.bones

                #Update Properties
                pbones["chin_frown_ctrl"].FROWN_LIMIT = prop_value
                #Apply Bone Transform
                pbones["chin_frown_ctrl"].location[2] = -(prop_value)

#Upper Eyelids
def eyelid_up_up_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_eyelid_up_up
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_up_ctrl_L"].EYELID_UP_LIMIT_L = prop_value
                pbones["eyelid_up_ctrl_R"].EYELID_UP_LIMIT_R= prop_value
                #Apply Bone Transform
                pbones["eyelid_up_ctrl_L"].location[2] = prop_value
                pbones["eyelid_up_ctrl_R"].location[2] = prop_value

def eyelid_up_down_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_eyelid_up_down
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_up_ctrl_L"].EYELID_DOWN_LIMIT_L = prop_value
                pbones["eyelid_up_ctrl_R"].EYELID_DOWN_LIMIT_R= prop_value
                #Apply Bone Transform
                pbones["eyelid_up_ctrl_L"].location[2] = -(prop_value)
                pbones["eyelid_up_ctrl_R"].location[2] = -(prop_value)

#Lower Eyelids
def eyelid_low_down_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_eyelid_low_down
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_low_ctrl_L"].EYELID_DOWN_LIMIT_L = prop_value
                pbones["eyelid_low_ctrl_R"].EYELID_DOWN_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["eyelid_low_ctrl_L"].location[2] = -(prop_value)
                pbones["eyelid_low_ctrl_R"].location[2] = -(prop_value)

def eyelid_low_up_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_eyelid_low_up
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_low_ctrl_L"].EYELID_UP_LIMIT_L = prop_value
                pbones["eyelid_low_ctrl_R"].EYELID_UP_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["eyelid_low_ctrl_L"].location[2] = prop_value
                pbones["eyelid_low_ctrl_R"].location[2] = prop_value

def eyelid_out_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_eyelid_out
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_up_ctrl_L"].EYELID_OUT_LIMIT_L = prop_value
                pbones["eyelid_up_ctrl_R"].EYELID_OUT_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["eye_def_L"].rotation_euler[2] = radians(prop_value)
                pbones["eye_def_R"].rotation_euler[2] = radians(-(prop_value))

def eyelid_in_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                prop_value = bpy.context.scene.blenrig_guide.guide_eyelid_in
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_up_ctrl_L"].EYELID_IN_LIMIT_L = prop_value
                pbones["eyelid_up_ctrl_R"].EYELID_IN_LIMIT_R = prop_value
                #Apply Bone Transform
                pbones["eye_def_L"].rotation_euler[2] = radians(-(prop_value))
                pbones["eye_def_R"].rotation_euler[2] = radians(prop_value)

#Shoulder Automatic Movement
def auto_shoulder_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                shoulder_auto_forw = bpy.context.scene.blenrig_guide.guide_shoulder_auto_forw
                shoulder_auto_back = bpy.context.scene.blenrig_guide.guide_shoulder_auto_back
                shoulder_auto_up = bpy.context.scene.blenrig_guide.guide_shoulder_auto_up
                shoulder_auto_down = bpy.context.scene.blenrig_guide.guide_shoulder_auto_down
                pbones = arm.pose.bones

                #Update Properties
                pbones["shoulder_L"]["SHLDR_AUTO_FORW_L"] = shoulder_auto_forw
                pbones["shoulder_R"]["SHLDR_AUTO_FORW_R"] = shoulder_auto_forw
                pbones["shoulder_L"]["SHLDR_AUTO_BACK_L"] = shoulder_auto_back
                pbones["shoulder_R"]["SHLDR_AUTO_BACK_R"] = shoulder_auto_back
                pbones["shoulder_L"]["SHLDR_AUTO_UP_L"] = shoulder_auto_up
                pbones["shoulder_R"]["SHLDR_AUTO_UP_R"] = shoulder_auto_up
                pbones["shoulder_L"]["SHLDR_AUTO_DOWN_L"] = shoulder_auto_down
                pbones["shoulder_R"]["SHLDR_AUTO_DOWN_R"] = shoulder_auto_down
                drivers_update()

#Foot Roll
def foot_roll_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                foot_roll_amp = bpy.context.scene.blenrig_guide.guide_foot_roll_amp
                foot_roll_toe_1 = bpy.context.scene.blenrig_guide.guide_foot_roll_toe_1
                foot_roll_toe_2 = bpy.context.scene.blenrig_guide.guide_foot_roll_toe_2
                pbones = arm.pose.bones

                #Update Properties
                pbones["foot_roll_ctrl_L"]["FOOT_ROLL_AMPLITUD_L"] = foot_roll_amp
                pbones["foot_roll_ctrl_L"]["TOE_1_ROLL_START_L"] = foot_roll_toe_1
                pbones["foot_roll_ctrl_L"]["TOE_2_ROLL_START_L"] = foot_roll_toe_2
                pbones["foot_roll_ctrl_R"]["FOOT_ROLL_AMPLITUD_R"] = foot_roll_amp
                pbones["foot_roll_ctrl_R"]["TOE_1_ROLL_START_R"] = foot_roll_toe_1
                pbones["foot_roll_ctrl_R"]["TOE_2_ROLL_START_R"] = foot_roll_toe_2
                drivers_update()

#Volume Variation
def vol_var_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                vol_var_arms = bpy.context.scene.blenrig_guide.guide_vol_var_arms
                vol_var_fingers = bpy.context.scene.blenrig_guide.guide_vol_var_fingers
                vol_var_legs = bpy.context.scene.blenrig_guide.guide_vol_var_legs
                vol_var_toes = bpy.context.scene.blenrig_guide.guide_vol_var_toes
                pbones = arm.pose.bones

                #Update Properties
                pbones["properties_arm_L"].volume_variation_arm_L = vol_var_arms
                pbones["properties_arm_L"].volume_variation_fingers_L = vol_var_fingers
                pbones["properties_leg_L"].volume_variation_leg_L = vol_var_legs
                pbones["properties_leg_L"].volume_variation_toes_L = vol_var_toes
                pbones["properties_arm_R"].volume_variation_arm_R = vol_var_arms
                pbones["properties_arm_R"].volume_variation_fingers_R = vol_var_fingers
                pbones["properties_leg_R"].volume_variation_leg_R = vol_var_legs
                pbones["properties_leg_R"].volume_variation_toes_R = vol_var_toes
                drivers_update()

#Floor Offset
def feet_floor_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                feet_floor = bpy.context.scene.blenrig_guide.guide_feet_floor
                pbones = arm.pose.bones

                #Update Properties
                pbones["sole_ctrl_L"].constraints["Floor_Foot_L_NOREP"].offset = feet_floor
                pbones["sole_ctrl_R"].constraints["Floor_Foot_R_NOREP"].offset = feet_floor

def facial_floor_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                eyelid_1_floor = bpy.context.scene.blenrig_guide.guide_eyelid_1_floor
                eyelid_2_floor = bpy.context.scene.blenrig_guide.guide_eyelid_2_floor
                eyelid_3_floor = bpy.context.scene.blenrig_guide.guide_eyelid_3_floor
                lip_1_floor = bpy.context.scene.blenrig_guide.guide_lip_1_floor
                lip_2_floor = bpy.context.scene.blenrig_guide.guide_lip_2_floor
                lip_3_floor = bpy.context.scene.blenrig_guide.guide_lip_3_floor
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_low_ctrl_1_mstr_L"].constraints["Floor_Eyelids_NOREP"].offset = eyelid_1_floor
                pbones["eyelid_low_ctrl_2_mstr_L"].constraints["Floor_Eyelids_NOREP"].offset = eyelid_2_floor
                pbones["eyelid_low_ctrl_3_mstr_L"].constraints["Floor_Eyelids_NOREP"].offset = eyelid_3_floor
                pbones["eyelid_low_ctrl_1_mstr_R"].constraints["Floor_Eyelids_NOREP"].offset = eyelid_1_floor
                pbones["eyelid_low_ctrl_2_mstr_R"].constraints["Floor_Eyelids_NOREP"].offset = eyelid_2_floor
                pbones["eyelid_low_ctrl_3_mstr_R"].constraints["Floor_Eyelids_NOREP"].offset = eyelid_3_floor
                pbones["lip_up_ctrl_1_mstr_L"].constraints["Floor_Lips"].offset = lip_1_floor
                pbones["lip_up_ctrl_2_mstr_L"].constraints["Floor_Lips"].offset = lip_2_floor
                pbones["lip_up_ctrl_3_mstr_L"].constraints["Floor_Lips"].offset = lip_3_floor
                pbones["lip_up_ctrl_1_mstr_R"].constraints["Floor_Lips"].offset = lip_1_floor
                pbones["lip_up_ctrl_2_mstr_R"].constraints["Floor_Lips"].offset = lip_2_floor
                pbones["lip_up_ctrl_3_mstr_R"].constraints["Floor_Lips"].offset = lip_3_floor

#Face Specials
def eyelids_up_follow_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                eyelid_up_up_follow = bpy.context.scene.blenrig_guide.guide_eyelid_up_up_follow
                eyelid_up_down_follow = bpy.context.scene.blenrig_guide.guide_eyelid_up_down_follow
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_up_ctrl_L"].EYE_UP_FOLLOW_L = eyelid_up_up_follow
                pbones["eyelid_up_ctrl_R"].EYE_UP_FOLLOW_R = eyelid_up_up_follow
                pbones["eyelid_up_ctrl_L"].EYE_DOWN_FOLLOW_L = eyelid_up_down_follow
                pbones["eyelid_up_ctrl_R"].EYE_DOWN_FOLLOW_R = eyelid_up_down_follow
                drivers_update()

def eyelids_low_follow_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                eyelid_low_up_follow = bpy.context.scene.blenrig_guide.guide_eyelid_low_up_follow
                eyelid_low_down_follow = bpy.context.scene.blenrig_guide.guide_eyelid_low_down_follow
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_low_ctrl_L"].EYE_UP_FOLLOW_L = eyelid_low_up_follow
                pbones["eyelid_low_ctrl_R"].EYE_UP_FOLLOW_R = eyelid_low_up_follow
                pbones["eyelid_low_ctrl_L"].EYE_DOWN_FOLLOW_L = eyelid_low_down_follow
                pbones["eyelid_low_ctrl_R"].EYE_DOWN_FOLLOW_R = eyelid_low_down_follow
                drivers_update()

def eyelid_auto_cheek_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                eyelid_low_cheek_follow = bpy.context.scene.blenrig_guide.guide_eyelid_auto_cheek
                pbones = arm.pose.bones

                #Update Properties
                pbones["eyelid_low_ctrl_L"].AUTO_CHEEK_L = eyelid_low_cheek_follow
                pbones["eyelid_low_ctrl_R"].AUTO_CHEEK_R = eyelid_low_cheek_follow
                drivers_update()

def cheek_auto_smile_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                cheek_auto_smile = bpy.context.scene.blenrig_guide.guide_cheek_auto_smile
                pbones = arm.pose.bones

                #Update Properties
                pbones["cheek_ctrl_L"].AUTO_SMILE_L = cheek_auto_smile
                pbones["cheek_ctrl_R"].AUTO_SMILE_R = cheek_auto_smile
                drivers_update()

def corner_auto_back_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                auto_back_value = bpy.context.scene.blenrig_guide.guide_mouth_corner_auto_back
                pbones = arm.pose.bones

                #Update Properties
                pbones["mouth_corner_L"].AUTO_BACK_L = auto_back_value
                pbones["mouth_corner_R"].AUTO_BACK_R = auto_back_value
                drivers_update()

#Lip Shaping
def lip_rigidity_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                lip_1_rigidity = bpy.context.scene.blenrig_guide.guide_lip_1_rigidity
                lip_2_rigidity = bpy.context.scene.blenrig_guide.guide_lip_2_rigidity
                lip_3_rigidity = bpy.context.scene.blenrig_guide.guide_lip_3_rigidity
                pbones = arm.pose.bones

                #Update Properties
                pbones["lip_up_ctrl_1_str_L"].constraints["Limit Distance_NOREP"].influence = lip_1_rigidity
                pbones["lip_up_ctrl_1_str_R"].constraints["Limit Distance_NOREP"].influence = lip_1_rigidity
                pbones["lip_low_ctrl_1_str_L"].constraints["Limit Distance_NOREP"].influence = lip_1_rigidity
                pbones["lip_low_ctrl_1_str_R"].constraints["Limit Distance_NOREP"].influence = lip_1_rigidity
                pbones["lip_up_ctrl_2_str_L"].constraints["Limit Distance_NOREP"].influence = lip_2_rigidity
                pbones["lip_up_ctrl_2_str_R"].constraints["Limit Distance_NOREP"].influence = lip_2_rigidity
                pbones["lip_low_ctrl_2_str_L"].constraints["Limit Distance_NOREP"].influence = lip_2_rigidity
                pbones["lip_low_ctrl_2_str_R"].constraints["Limit Distance_NOREP"].influence = lip_2_rigidity
                pbones["lip_up_ctrl_3_str_L"].constraints["Limit Distance_NOREP"].influence = lip_3_rigidity
                pbones["lip_up_ctrl_3_str_R"].constraints["Limit Distance_NOREP"].influence = lip_3_rigidity
                pbones["lip_low_ctrl_3_str_L"].constraints["Limit Distance_NOREP"].influence = lip_3_rigidity
                pbones["lip_low_ctrl_3_str_R"].constraints["Limit Distance_NOREP"].influence = lip_3_rigidity

def lip_curvature_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                lips_motion_curvature = bpy.context.scene.blenrig_guide.guide_lips_motion_curvature
                pbones = arm.pose.bones

                #Update Properties
                pbones["lip_up_line_L"].bone.bbone_easeout = lips_motion_curvature
                pbones["lip_up_line_R"].bone.bbone_easeout = lips_motion_curvature
                pbones["lip_zipper_line_L"].bone.bbone_easeout = lips_motion_curvature
                pbones["lip_zipper_line_R"].bone.bbone_easeout = lips_motion_curvature
                pbones["lip_low_line_L"].bone.bbone_easeout = lips_motion_curvature
                pbones["lip_low_line_R"].bone.bbone_easeout = lips_motion_curvature

def lip_override_update(self, context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1].__contains__('BlenRig_'):

                arm = bpy.context.scene.blenrig_guide.arm_obj
                lip_1_curvature_x_override = bpy.context.scene.blenrig_guide.guide_lip_1_curvature_override[0]
                lip_2_curvature_x_override = bpy.context.scene.blenrig_guide.guide_lip_2_curvature_override[0]
                lip_3_curvature_x_override = bpy.context.scene.blenrig_guide.guide_lip_3_curvature_override[0]
                lip_1_curvature_y_override = bpy.context.scene.blenrig_guide.guide_lip_1_curvature_override[1]
                lip_2_curvature_y_override = bpy.context.scene.blenrig_guide.guide_lip_2_curvature_override[1]
                lip_3_curvature_y_override = bpy.context.scene.blenrig_guide.guide_lip_3_curvature_override[1]
                lip_1_curvature_z_override = bpy.context.scene.blenrig_guide.guide_lip_1_curvature_override[2]
                lip_2_curvature_z_override = bpy.context.scene.blenrig_guide.guide_lip_2_curvature_override[2]
                lip_3_curvature_z_override = bpy.context.scene.blenrig_guide.guide_lip_3_curvature_override[2]
                pbones = arm.pose.bones

                #Update Properties
                pbones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"] = lip_1_curvature_x_override
                pbones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"] = lip_1_curvature_y_override
                pbones["lip_up_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"] = lip_1_curvature_z_override
                pbones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_X_L"] = lip_1_curvature_x_override
                pbones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_Y_L"] = lip_1_curvature_y_override
                pbones["lip_low_ctrl_1_mstr_L"]["CORNER_FOLLOW_Z_L"] = lip_1_curvature_z_override
                pbones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_X_R"] = lip_1_curvature_x_override
                pbones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_Y_R"] = lip_1_curvature_y_override
                pbones["lip_up_ctrl_1_mstr_R"]["CORNER_FOLLOW_Z_R"] = lip_1_curvature_z_override
                pbones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_X_R"] = lip_1_curvature_x_override
                pbones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_Y_R"] = lip_1_curvature_y_override
                pbones["lip_low_ctrl_1_mstr_R"]["CORNER_FOLLOW_Z_R"] = lip_1_curvature_z_override
                pbones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"] = lip_2_curvature_x_override
                pbones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"] = lip_2_curvature_y_override
                pbones["lip_up_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"] = lip_2_curvature_z_override
                pbones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_X_L"] = lip_2_curvature_x_override
                pbones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_Y_L"] = lip_2_curvature_y_override
                pbones["lip_low_ctrl_2_mstr_L"]["CORNER_FOLLOW_Z_L"] = lip_2_curvature_z_override
                pbones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_X_R"] = lip_2_curvature_x_override
                pbones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_Y_R"] = lip_2_curvature_y_override
                pbones["lip_up_ctrl_2_mstr_R"]["CORNER_FOLLOW_Z_R"] = lip_2_curvature_z_override
                pbones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_X_R"] = lip_2_curvature_x_override
                pbones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_Y_R"] = lip_2_curvature_y_override
                pbones["lip_low_ctrl_2_mstr_R"]["CORNER_FOLLOW_Z_R"] = lip_2_curvature_z_override
                pbones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"] = lip_3_curvature_x_override
                pbones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"] = lip_3_curvature_y_override
                pbones["lip_up_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"] = lip_3_curvature_z_override
                pbones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_X_L"] = lip_3_curvature_x_override
                pbones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_Y_L"] = lip_3_curvature_y_override
                pbones["lip_low_ctrl_3_mstr_L"]["CORNER_FOLLOW_Z_L"] = lip_3_curvature_z_override
                pbones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_X_R"] = lip_3_curvature_x_override
                pbones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_Y_R"] = lip_3_curvature_y_override
                pbones["lip_up_ctrl_3_mstr_R"]["CORNER_FOLLOW_Z_R"] = lip_3_curvature_z_override
                pbones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_X_R"] = lip_3_curvature_x_override
                pbones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_Y_R"] = lip_3_curvature_y_override
                pbones["lip_low_ctrl_3_mstr_R"]["CORNER_FOLLOW_Z_R"] = lip_3_curvature_z_override
                drivers_update()

# Assign Actions

def assign_action(action_name, frame):

    #Get Armature
    def get_armature():
        if hasattr(bpy.context.active_object, 'type'):
            if bpy.context.active_object.type == 'ARMATURE':
                return bpy.context.active_object

    #Get Action
    def get_action():
        armature = get_armature()
        print (armature)
        for b in armature.pose.bones:
            for C in b.constraints:
                if C.type == 'ACTION':
                    if action_name in C.action.name:
                        return C.action

    armature = get_armature()
    print (armature.name)
    action = get_action()
    print(action)

    armature.animation_data.action = action

    #Set Frame
    bpy.context.scene.frame_set(frame)

    #Enable Auto-Key
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = True

def clear_action():

    #Get Armature
    def get_armature():
        if hasattr(bpy.context.active_object, 'type'):
            if bpy.context.active_object.type == 'ARMATURE':
                return bpy.context.active_object

    #Remove Action
    armature = get_armature()
    armature.animation_data.action = None

    #Disable Auto-Key
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = False

def reset_all_bones_transforms():

    #Reset Transforms
    if hasattr(bpy.context.active_object, 'type'):
        if bpy.context.active_object.type == 'ARMATURE':
            armature = bpy.context.active_object
            for b in armature.pose.bones:
                b.matrix_basis = Matrix()
        if bpy.context.active_object.type == 'MESH':
            armature = bpy.context.scene.blenrig_guide.arm_obj
            for b in armature.pose.bones:
                b.matrix_basis = Matrix()

#Weights Guide Joint Rotation Functions
def joint_x6_update(self, context):
    guide_props = bpy.context.scene.blenrig_guide
    arm = guide_props.arm_obj
    prop_value = guide_props.guide_joint_transforms_X6
    rot_value_1 = guide_props.guide_rotation_1
    rot_value_2 = guide_props.guide_rotation_2
    rot_value_3 = guide_props.guide_rotation_3
    rot_value_4 = guide_props.guide_rotation_4
    rot_value_5 = guide_props.guide_rotation_5
    rot_value_6 = guide_props.guide_rotation_6
    loc_value_1 = guide_props.guide_location_1
    loc_value_2 = guide_props.guide_location_2
    loc_value_3 = guide_props.guide_location_3
    loc_value_4 = guide_props.guide_location_4
    loc_value_5 = guide_props.guide_location_5
    loc_value_6 = guide_props.guide_location_6
    scale_value_1 = guide_props.guide_scale_1
    scale_value_2 = guide_props.guide_scale_2
    scale_value_3 = guide_props.guide_scale_3
    scale_value_4 = guide_props.guide_scale_4
    scale_value_5 = guide_props.guide_scale_5
    scale_value_6 = guide_props.guide_scale_6
    t_bone = guide_props.guide_transformation_bone
    pbones = arm.pose.bones

    #Set Active Shapekey Function
    def active_shapekey(index):
        try:
            if guide_props.shapekeys_list_index == 1:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_1
            if guide_props.shapekeys_list_index == 2:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_2
            if guide_props.shapekeys_list_index == 3:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_3
            if guide_props.shapekeys_list_index == 4:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_4
            set_active_shapekey(guide_props.active_shapekey_name)
        except:
            pass

    reset_all_bones_transforms()

    #Apply Bone Transform

    if prop_value == 0:
        try:
            pbones[t_bone].matrix_basis = Matrix()
        except:
            pass
    if prop_value == 1:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_1[0]), radians(rot_value_1[1]), radians(rot_value_1[2]))
            pbones[t_bone].location = loc_value_1
            pbones[t_bone].scale = scale_value_1
        except:
            pass
        #Set Active Shapekey
        active_shapekey(0)

    if prop_value == 2:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_2[0]), radians(rot_value_2[1]), radians(rot_value_2[2]))
            pbones[t_bone].location = loc_value_2
            pbones[t_bone].scale = scale_value_2
        except:
            pass
        #Set Active Shapekey
        active_shapekey(1)

    if prop_value == 3:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_3[0]), radians(rot_value_3[1]), radians(rot_value_3[2]))
            pbones[t_bone].location = loc_value_3
            pbones[t_bone].scale = scale_value_3
        except:
            pass
        #Set Active Shapekey
        active_shapekey(2)

    if prop_value == 4:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_4[0]), radians(rot_value_4[1]), radians(rot_value_4[2]))
            pbones[t_bone].location = loc_value_4
            pbones[t_bone].scale = scale_value_4
        except:
            pass
        #Set Active Shapekey
        active_shapekey(3)

    if prop_value == 5:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_5[0]), radians(rot_value_5[1]), radians(rot_value_5[2]))
            pbones[t_bone].location = loc_value_5
            pbones[t_bone].scale = scale_value_5
        except:
            pass
        #Set Active Shapekey
        active_shapekey(4)

    if prop_value == 6:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_6[0]), radians(rot_value_6[1]), radians(rot_value_6[2]))
            pbones[t_bone].location = loc_value_6
            pbones[t_bone].scale = scale_value_6
        except:
            pass
        #Set Active Shapekey
        active_shapekey(5)

def joint_x4_update(self, context):
    guide_props = bpy.context.scene.blenrig_guide
    arm = guide_props.arm_obj
    prop_value = guide_props.guide_joint_transforms_X4
    rot_value_1 = guide_props.guide_rotation_1
    rot_value_2 = guide_props.guide_rotation_2
    rot_value_3 = guide_props.guide_rotation_3
    rot_value_4 = guide_props.guide_rotation_4
    loc_value_1 = guide_props.guide_location_1
    loc_value_2 = guide_props.guide_location_2
    loc_value_3 = guide_props.guide_location_3
    loc_value_4 = guide_props.guide_location_4
    scale_value_1 = guide_props.guide_scale_1
    scale_value_2 = guide_props.guide_scale_2
    scale_value_3 = guide_props.guide_scale_3
    scale_value_4 = guide_props.guide_scale_4
    t_bone = guide_props.guide_transformation_bone
    pbones = arm.pose.bones

    #Set Active Shapekey Function
    def active_shapekey(index):
        try:
            if guide_props.shapekeys_list_index == 1:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_1
            if guide_props.shapekeys_list_index == 2:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_2
            if guide_props.shapekeys_list_index == 3:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_3
            if guide_props.shapekeys_list_index == 4:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_4
            set_active_shapekey(guide_props.active_shapekey_name)
        except:
            pass

    reset_all_bones_transforms()

    #Apply Bone Transform

    if prop_value == 0:
        try:
            pbones[t_bone].matrix_basis = Matrix()
        except:
            pass
    if prop_value == 1:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_1[0]), radians(rot_value_1[1]), radians(rot_value_1[2]))
            pbones[t_bone].location = loc_value_1
            pbones[t_bone].scale = scale_value_1
        except:
            pass
        #Set Active Shapekey
        active_shapekey(0)

    if prop_value == 2:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_2[0]), radians(rot_value_2[1]), radians(rot_value_2[2]))
            pbones[t_bone].location = loc_value_2
            pbones[t_bone].scale = scale_value_2
        except:
            pass
        #Set Active Shapekey
        active_shapekey(1)

    if prop_value == 3:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_3[0]), radians(rot_value_3[1]), radians(rot_value_3[2]))
            pbones[t_bone].location = loc_value_3
            pbones[t_bone].scale = scale_value_3
        except:
            pass
        #Set Active Shapekey
        active_shapekey(2)

    if prop_value == 4:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_4[0]), radians(rot_value_4[1]), radians(rot_value_4[2]))
            pbones[t_bone].location = loc_value_4
            pbones[t_bone].scale = scale_value_4
        except:
            pass
        #Set Active Shapekey
        active_shapekey(3)

def joint_x2_update(self, context):
    guide_props = bpy.context.scene.blenrig_guide
    arm = guide_props.arm_obj
    prop_value = guide_props.guide_joint_transforms_X2
    rot_value_1 = guide_props.guide_rotation_1
    rot_value_2 = guide_props.guide_rotation_2
    loc_value_1 = guide_props.guide_location_1
    loc_value_2 = guide_props.guide_location_2
    scale_value_1 = guide_props.guide_scale_1
    scale_value_2 = guide_props.guide_scale_2
    t_bone = guide_props.guide_transformation_bone
    pbones = arm.pose.bones

    #Set Active Shapekey Function
    def active_shapekey(index):
        try:
            if guide_props.shapekeys_list_index == 1:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_1
            if guide_props.shapekeys_list_index == 2:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_2
            if guide_props.shapekeys_list_index == 3:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_3
            if guide_props.shapekeys_list_index == 4:
                guide_props.active_shapekey_name = bpy.context.scene.blenrig_shapekeys_list[index].list_4
            set_active_shapekey(guide_props.active_shapekey_name)
        except:
            pass

    reset_all_bones_transforms()

    #Apply Bone Transform

    if prop_value == 0:
        try:
            pbones[t_bone].matrix_basis = Matrix()
        except:
            pass
    if prop_value == 1:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_1[0]), radians(rot_value_1[1]), radians(rot_value_1[2]))
            pbones[t_bone].location = loc_value_1
            pbones[t_bone].scale = scale_value_1
        except:
            pass
        #Set Active Shapekey
        active_shapekey(0)

    if prop_value == 2:
        try:
            pbones[t_bone].rotation_euler = (radians(rot_value_2[0]), radians(rot_value_2[1]), radians(rot_value_2[2]))
            pbones[t_bone].location = loc_value_2
            pbones[t_bone].scale = scale_value_2
        except:
            pass
        #Set Active Shapekey
        active_shapekey(1)

#Set Active Vgroup for Weight Painting
def set_active_vgroup(v_group):
    active = bpy.context.active_object
    if not active:
        return False
    if active.type == 'MESH':
        try:
            index = active.vertex_groups[v_group].index
            active.vertex_groups.active_index = index
        except:
            pass

#Show All Bones in Weight Painting
def show_wp_bones_update(self, context):
    scn = bpy.context.scene
    guide_props = scn.blenrig_guide
    arm = guide_props.arm_obj
    pbones = arm.pose.bones
    prop_value = guide_props.guide_show_wp_bones

    if prop_value == True:
        for b in pbones:
            b.bone.hide = False
    else:
        bones = [b.bone for b in scn.blenrig_wp_bones]
        unhide_all_bones(context)
        select_all_pose_bones(context)
        deselect_pose_bones(context, *bones)
        hide_selected_pose_bones(context)

#Set Active Shapekey for Editting
def set_active_shapekey(shapekey_name):
    ob = bpy.context.active_object
    if not ob:
        return False
    if ob.type == 'MESH':
        if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'key_blocks'):
            shapekeys = ob.data.shape_keys.key_blocks
            index = shapekeys.find(shapekey_name)
            ob.active_shape_key_index = index

#Get Shapekey Driver Transform
def get_driver_transform(shapekey, default_value):
    guide_props = bpy.context.scene.blenrig_guide
    ob = guide_props.active_shp_obj


    #Get Active Shapekey Driver
    if hasattr(ob, 'data') and hasattr(ob.data, 'shape_keys') and hasattr(ob.data.shape_keys, 'animation_data') and hasattr(ob.data.shape_keys.animation_data, 'drivers'):
        for driver in ob.data.shape_keys.animation_data.drivers:
            d_path = driver.data_path
            if d_path == 'key_blocks["' + str(shapekey) + '"].value':
                return degrees(1 / driver.modifiers[0].coefficients[1])
    return default_value

#Propagate shapekey y other shapekeys
def blend_from_shape(destination_keys):
    ob = bpy.context.active_object
    shapekeys_list = destination_keys

    for shape in shapekeys_list:
        set_active_shapekey(shape)
        bpy.ops.mesh.blend_from_shape(shape=ob.active_shape_key.name, blend=1.0, add=False)

import bpy

armature=[]
mesh_deform=[]
surface_deform=[]
armature_name=[]
mesh_deform_name=[]
surface_deform_name=[]
lattices=[]
boneshapes=[]


###### Search name of MDef_cage  #####
def mdef_search(type):
    mdef_cage_objects = []
    mdef_cage_names = []
    sdef_cage_objects = []
    sdef_cage_names = []
    arm = bpy.context.active_object.name
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if type == 'MESH_DEFORM':
                    if ob_m.type == type:
                        if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                            cage = ob.modifiers[ob_m.name].object
                            if hasattr(cage, 'modifiers'):
                                for mod in cage.modifiers:
                                    if mod.type == 'ARMATURE':
                                        if mod.object.name == arm:
                                            if bpy.data.objects.get(ob.modifiers[ob_m.name].object.name) not in mdef_cage_objects:
                                                mdef_cage_objects.append(bpy.data.objects.get(ob.modifiers[ob_m.name].object.name))
                                                mdef_cage_names.append(ob.modifiers[ob_m.name].object.name)
    return mdef_cage_objects , mdef_cage_names
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if type == 'SURFACE_DEFORM':
                    if ob_m.type == type:
                        if hasattr(ob.modifiers[ob_m.name], 'target') and hasattr(ob.modifiers[ob_m.name].target, 'name'):
                            cage = ob.modifiers[ob_m.name].target
                            if hasattr(cage, 'modifiers'):
                                for mod in cage.modifiers:
                                    if mod.type == 'ARMATURE':
                                        if mod.object.name == arm:
                                            if bpy.data.objects.get(ob.modifiers[ob_m.name].target.name) not in sdef_cage_objects:
                                                sdef_cage_objects.append(bpy.data.objects.get(ob.modifiers[ob_m.name].target.name))
                                                sdef_cage_objects.append(ob.modifiers[ob_m.name].target.name)
    return sdef_cage_objects , sdef_cage_names

###### Search objets with modifiers  #####
def search_mod(type):
    arm = bpy.context.active_object.name

#Clean Variables
    mdef_cage_name =[]
    sdef_cage_name = []
    surface_deform = []
    mesh_deform = []
    armature = []
    surface_deform_name = []
    mesh_deform_name = []
    armature_name = []

    mdef_cage_name = mdef_search('MESH_DEFORM')
    sdef_cage_name = mdef_search('SURFACE_DEFORM')
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if ob_m.type == type:

                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        if ob.modifiers[ob_m.name].object in mdef_cage_name[0]:
                            if ob not in mesh_deform:
                                mesh_deform.append(ob)
                                mesh_deform_name.append(ob.name)

                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        if ob.modifiers[ob_m.name].object.name == arm:
                            if ob not in armature:
                                armature.append(ob)
                                armature_name.append(ob.name)

                    if hasattr(ob.modifiers[ob_m.name],'target') and hasattr(ob.modifiers[ob_m.name].target, 'name'):
                        if ob.modifiers[ob_m.name].target in sdef_cage_name[0]:
                            if ob not in surface_deform:
                                surface_deform.append(ob)
                                surface_deform_name.append(ob.name)

    if type == "ARMATURE":
        return armature, armature_name
    if type == "MESH_DEFORM":
        return mesh_deform, mesh_deform_name
    if type =="SURFACE_DEFORM":
        return surface_deform, surface_deform_name

###########  Toggle link/unlink objets with modifiers in BlenRig_temp #######
def blenrig_temp(type,lnk = True):
    if lnk:
        if type == "ARMATURE":
            link_objects(search_mod(type)[0])
        elif type == "MESH_DEFORM":
            link_objects(search_mod(type)[0])
        elif type == "SURFACE_DEFORM":
            link_objects(search_mod(type)[0])

    elif not lnk:
        if type == "ARMATURE":
            unlink_objects(search_mod(type)[0])
        elif type == "MESH_DEFORM":
            unlink_objects(search_mod(type)[0])
        elif type == "SURFACE_DEFORM":
            unlink_objects(search_mod(type)[0])

###### link objets in BlenRig_temp #####
def link_objects(objects):
    temp_collection = bpy.data.collections.get("BlenRig_temp")
    if objects:
        if bpy.context.scene.collection.children.find("BlenRig_temp") == -1:
            if temp_collection:
                bpy.context.scene.collection.children.link(temp_collection)
            else:
                temp_collection = bpy.data.collections.new("BlenRig_temp")
                bpy.context.scene.collection.children.link(temp_collection)
        for ob in objects:
            if not bpy.context.scene.collection.children[temp_collection.name].objects.get(ob.name):
                temp_collection.objects.link(ob)

###### Unlink objets in BlenRig_temp #####
def unlink_objects(objects):
    temp_collection = bpy.data.collections.get("BlenRig_temp")
    if objects:
        if bpy.context.scene.collection.children.get('BlenRig_temp'):
            for ob in objects:
                try:
                    temp_collection.objects.unlink(ob)
                except:
                    pass
            objects.clear()
            if len(bpy.data.collections['BlenRig_temp'].objects) < 1:
                bpy.context.scene.collection.children.unlink(temp_collection)

####### Search objets parent with  biped_blenrig (lattices) ######
def search_parent():
    arm = bpy.context.active_object.name
    for ob in bpy.data.objects:
        if hasattr(ob,'parent') and hasattr(ob.parent, 'name'):
            if not ob.name.startswith('cs_') and ob.parent.name == arm:
                lattices.append(ob)
    return lattices

####### Search BoneShapes #####
def search_boneshapes():
    arm = bpy.context.active_object.name
    for ob in bpy.data.objects:
        if hasattr(ob,'parent'):
            if ob.name.startswith('cs_'):
                boneshapes.append(ob)
    return boneshapes

###########  Toggle linking objets BoneShapes in BlenRig_temp #######
def blenrig_temp_boneshapes(lnk = True):
    if lnk:
        link_objects(search_boneshapes())
    elif not lnk:
        unlink_objects(search_boneshapes())

###########  Toggle linking objets Lattices and Parenting objects in BlenRig_temp #######
def blenrig_temp_parent(lnk = True):
    if lnk:
        link_objects(search_parent())
    elif not lnk:
        unlink_objects(search_parent())

###########  Toggle linking MDef_Cage in BlenRig_temp #######
def blenrig_temp_mdef_cage(lnk = True):
    if lnk:
        link_objects(mdef_search('MESH_DEFORM')[0])
    elif not lnk:
        unlink_objects(mdef_search('MESH_DEFORM')[0])

def blenrig_temp_sdef_cage(lnk = True):
    if lnk:
        link_objects(mdef_search('SURFACE_DEFORM')[0])
    elif not lnk:
        unlink_objects(mdef_search('SURFACE_DEFORM')[0])
import bpy

armature=[]
mesh_deform=[]
surface_deform=[]
lattices=[]
boneshapes=[]
mdef_cage=[]

###### Search name of MDef_cage  #####
def mdef_search_name(type="MESH_DEFORM"):
    arm = bpy.context.active_object.data.name    
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if ob_m.type == type:                    
                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        return (ob.modifiers[ob_m.name].object.name)

###### Find object_name of MDef_cage  #####
def mdef_find():
    for ob in bpy.data.objects:
        if ob.name == mdef_search_name():
            mdef_cage.append(ob)
            return mdef_cage

###### Search objets with modifiers  #####
def search_mod(type):
    arm = bpy.context.active_object.data.name    
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if ob_m.type == type:

                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        if ob.modifiers[ob_m.name].object.name == mdef_search_name():
                            mesh_deform.append(ob)

                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        if ob.modifiers[ob_m.name].object.name == arm:
                            armature.append(ob)

                    if hasattr(ob.modifiers[ob_m.name],'target') and hasattr(ob.modifiers[ob_m.name].target, 'name'):
                        surface_deform.append(ob)

    if type == "ARMATURE":
        return armature
    if type == "MESH_DEFORM":
        return mesh_deform
    if type =="SURFACE_DEFORM":
        return surface_deform 

###########  Toggle link/unlink objets with modifiers in BlenRig_temp #######
def blenrig_temp(type,lnk = True):
    if lnk:
        if type == "ARMATURE":
            armature = search_mod(type)
            link_objects(armature)                           
        elif type == "MESH_DEFORM":
            mesh_deform = search_mod(type)
            link_objects(mesh_deform)        
        elif type == "SURFACE_DEFORM":
            surface_deform = search_mod(type)
            link_objects(surface_deform)

    elif not lnk:
        if type == "ARMATURE":
            armature = search_mod(type)
            unlink_objects(armature)                            
        elif type == "MESH_DEFORM":
            mesh_deform = search_mod(type)
            unlink_objects(mesh_deform)        
        elif type == "SURFACE_DEFORM":
            surface_deform = search_mod(type)
            unlink_objects(surface_deform)

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
    arm = bpy.context.active_object.data.name
    for ob in bpy.data.objects:
        if hasattr(ob,'parent') and hasattr(ob.parent, 'name'):
            if not ob.name.startswith('cs_') and ob.parent.name == arm:
                lattices.append(ob)
    return lattices

####### Search BoneShapes #####
def search_boneshapes():
    arm = bpy.context.active_object.data.name
    for ob in bpy.data.objects:
        if hasattr(ob,'parent'):
            if ob.name.startswith('cs_'):
                boneshapes.append(ob)
    return boneshapes

###########  Toggle linking objets BoneShapes in BlenRig_temp #######
def blenrig_temp_boneshapes(lnk = True):
    if lnk:
        parent = search_boneshapes()
        link_objects(parent)        
    elif not lnk:
        parent = search_boneshapes()
        unlink_objects(parent)

###########  Toggle linking objets Lattices and Parenting objects in BlenRig_temp #######
def blenrig_temp_parent(lnk = True):
    if lnk:
        parent = search_parent()
        link_objects(parent)        
    elif not lnk:
        parent = search_parent()
        unlink_objects(parent)

###########  Toggle linking MDef_Cage in BlenRig_temp #######
def blenrig_temp_cage(lnk = True):
    if lnk:
        mdef_cage = mdef_find()
        link_objects(mdef_cage)        
    elif not lnk:
        mdef_cage = mdef_find()
        unlink_objects(mdef_cage)
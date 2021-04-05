import bpy

armature=[]
mesh_deform=[]
surface_deform=[]
lattices=[]
boneshapes=[]
mdef_cage=[]

###### Search name of MDef_cage  #####
def mdef_search(type="MESH_DEFORM"):
    arm = bpy.context.active_object.data.name    
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if ob_m.type == type:                    
                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        ob = bpy.data.objects.get(ob.modifiers[ob_m.name].object.name)
                        mdef_cage.append(ob)
                        return mdef_cage

###### Search objets with modifiers  #####
def search_mod(type):
    arm = bpy.context.active_object.data.name
    mdef_cage_name = mdef_search()    
    for ob in bpy.data.objects:
        if hasattr(ob,'modifiers'):
            for ob_m in ob.modifiers:
                if ob_m.type == type:

                    if hasattr(ob.modifiers[ob_m.name], 'object') and hasattr(ob.modifiers[ob_m.name].object, 'name'):
                        if ob.modifiers[ob_m.name].object.name == mdef_cage_name[0].name:
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
            link_objects(search_mod(type))                           
        elif type == "MESH_DEFORM":
            link_objects(search_mod(type))        
        elif type == "SURFACE_DEFORM":
            link_objects(search_mod(type))

    elif not lnk:
        if type == "ARMATURE":
            unlink_objects(search_mod(type))                            
        elif type == "MESH_DEFORM":
            unlink_objects(search_mod(type))        
        elif type == "SURFACE_DEFORM":
            unlink_objects(search_mod(type))

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
        link_objects(mdef_search())        
    elif not lnk:
        unlink_objects(mdef_search())
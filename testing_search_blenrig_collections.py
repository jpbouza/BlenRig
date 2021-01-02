# import bpy

# # lattices = []
# direct_parent = []
# child_item = []
# def search_blendrigs_collections(data):
#     path = []
#     for coll in data:
#         #print(coll.name, "childs:", len(coll.children), "objects:", len(coll.objects))
#         if coll.name not in direct_parent:
#             if len(coll.children) == 0:
#                 search_blendrigs_collections(coll.children)
#             else:
#                 # direct_parent
#                 #print("Con child_item")
#                 #print("[", coll.name, "]")
#                 for child in coll.children:
#                     if child.name not in child_item:
#                         #print("Child", child.name)
#                         if len(child.objects) > 0:
#                             for ob in child.objects:
#                                 #print("Object: ", ob.name, "in collection", child.name)
#                                 # buscando lattices:
#                                 #if hasattr(ob, 'parent'):
#                                     #if ob.parent:
#                                         #print(coll.name, ">", ob.name, ">", "parent", ob.parent.name)
#                                         #if child.name not in lattices:
#                                             #lattices.append(child.name)
#                                 if len(ob.modifiers) > 0:
#                                     # child.name is the important
#                                     if hasattr(ob.modifiers[0], 'object'):
#                                         path.append([coll.name, child.name, ob.name])
#                                         #print(' > '.join(path))
#                                     elif ob.name.startswith('cs_'):
#                                         path.append([coll.name, child.name, ob.name])
#                                 else:
#                                     if ob.name.startswith('cs_'):
#                                         path.append([coll.name, child.name, ob.name])
#                         child_item.append(child.name)
#                 direct_parent.append(coll.name)
#     return path


# blenrig_colls = search_blendrigs_collections(bpy.data.collections)
# controled_colls = []
# for coll in blenrig_colls:
#     if coll[1] not in controled_colls:
#         print(' > '.join(coll))
#         # print(coll[1])
#         controled_colls.append(coll[1])
# # print("direct_parent:", direct_parent)
# #print("child_item:", child_item)
# #print("lattices:", lattices)







# ####################################################################################################
# ####################################################################################################
# ################################## Probando con json: ##############################################
# ####################################################################################################
# ####################################################################################################
# import bpy
# import json


# direct_parent = []
# childrens = []
# # primero tengo q recolectar los childrens:
# for coll in reversed(bpy.data.collections):
#     if coll.name not in direct_parent:
#         padre = coll.name
#         if len(coll.children) > 0:
#             for child in coll.children:
#                 childrens.append(child.name)

# print(childrens)

# colecciones = {}
# direct_parent = []

# def search_blendrigs_collections(data_colls):
#     for coll in data_colls:
#         padre = coll
#         print(coll.name, "childs:", len(coll.children), "objects:", len(coll.objects))
#         if padre.name not in direct_parent:
#             if len(coll.children) > 0:
#                 if padre.name not in colecciones.keys():
#                     colecciones[padre.name] = []
#                 for child in coll.children:
#                     if len(colecciones) == 0:
#                         colecciones[padre.name].append([child.name])
#                     else:
#                         if padre.name not in colecciones.keys():
#                             colecciones[padre.name] = [child.name]
#                         else:
#                             if child.name not in colecciones[padre.name]:
#                                 colecciones[padre.name].append(child.name)
#                             else:
#                                 colecciones[padre.name] = [child.name]
#             direct_parent.append(coll.name)

# search_blendrigs_collections(bpy.data.collections)
# print(json.dumps(colecciones, indent=4))



# ####################################################################################################
# ####################################################################################################
# ################################## Probando dict a json: ###########################################
# ####################################################################################################
# ####################################################################################################

# import json

# p = []
# tree = {}
# def computar(data):
#     for coll in data:
#         if coll.name not in p:
#             if len(coll.children) > 0:
#                 p.append(coll.name)
#                 tree[coll.name] = [c.name for c in coll.children]

# computar(bpy.data.collections)
# print(p)
# print(tree)
# print(json.dumps(tree, indent=4))



# #########################################################################
# #################### know parent of a collection ########################
# #########################################################################
# def traverse_tree(t):
#     yield t
#     for child in t.children:
#         yield from traverse_tree(child)

# def parent_lookup(coll):
#     parent_lookup = {}
#     for coll in traverse_tree(coll):
#         for c in coll.children.keys():
#             parent_lookup.setdefault(c, coll.name)
#     return parent_lookup

# def get_parent_from_child_collection(target_coll):
#     # Get all collections of the scene and their parents in a dict
#     coll_scene = bpy.context.scene.collection
#     coll_parents = parent_lookup(coll_scene)
#     #
#     if target_coll in bpy.data.collections:
#         c = bpy.data.collections[target_coll]
#         #print ("Parent of " + c.name + " is " + coll_parents.get(c.name))
#         return coll_parents.get(c.name)
#     else:
#         print("unknown collection " + target_coll)
# #########################################################################

# get_parent_from_child_collection('tools')






# import json

# p = []
# tree = {}
# def computar(data):
#     for coll in data:
#         if coll.name not in p:
#             if len(coll.children) > 0:
#                 p.append(coll.name)
#                 tree[coll.name] = [c.name for c in coll.children]
#                 for c in coll.children:
#                     if len(c.children) > 0:
#                         computar(coll.children)

# computar(bpy.data.collections)
# #print(p)
# #print(tree)
# print(json.dumps(tree, indent=4))






#########################################################################
#########################################################################
#########################################################################
import bpy
import json

### for query real parent ###
def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)

def parent_lookup(coll):
    parent_lookup = {}
    for coll in traverse_tree(coll):
        for c in coll.children.keys():
            parent_lookup.setdefault(c, coll.name)
    return parent_lookup

def get_parent_from_child_collection(target_coll):
    # Get all collections of the scene and their parents in a dict
    coll_scene = bpy.context.scene.collection
    coll_parents = parent_lookup(coll_scene)
    #
    if target_coll in bpy.data.collections:
        c = bpy.data.collections[target_coll]
        #print ("Parent of " + c.name + " is " + coll_parents.get(c.name))
        return coll_parents.get(c.name)
    else:
        print("unknown collection " + target_coll)

### end for query real parent ###

class Procesadora:
    def __init__(self, tree={}, p=[], padre=''):
        self.tree = tree
        self.p = p
        self.padre = padre
    #
    def computar(self, item):
        self.padre = item.name
        if self.padre not in self.p:
            if self.padre not in self.tree and self.padre not in self.p:
                print("self.padre: " + self.padre)
                self.tree[self.padre] = []
            if hasattr(item, 'children') and len(item.children) > 0:
                pack = []
                for child in item.children:
                    if child.name not in self.p:
                        if len(child.children) > 0:
                            #print("break")
                            #last_p = list(self.tree)[-1] # at last parent append childs
                            #self.tree[last_p].append(self.computar(child))
                            rp = get_parent_from_child_collection(child.name)
                            print("rp: " + rp)
                            if rp in self.tree:
                                self.tree[rp].append(self.computar(child))
                            #
                            if child.name == self.padre:
                                del self.tree[child.name]
                        else:
                            # get real parent:
                            print('child.name: ' + child.name)
                            rp = get_parent_from_child_collection(child.name)
                            self.tree[rp].append(child.name)
                            pack.append(child.name)
                            self.p.append(child.name)
                            self.p.append(item.name)
                            self.p.append(self.padre)
                #
                return {self.padre: pack}
    #
    def preview(self):
        print(json.dumps(self.tree, indent=4))

ps = Procesadora()
data = bpy.context.scene.collection.children
for c in data:
    ps.computar(c)

ps.preview()




#########################################################################
#########################################################################
#########################################################################
master_collection = bpy.context.scene.collection

n = 0
def procesar(level, data):
    if len(data.children) > 0:
        print(level + "└[" + data.name + "]")
        for i in data.children:
            #print(i.name)
            procesar(level+"||", i)
    else:
        print(level + "└" + data.name)     

for p in master_collection.children:
    #print(p.name)
    if n == 0:
        print("[Maste collection]")
        n += 1
    level = "||"
    procesar(level, p)
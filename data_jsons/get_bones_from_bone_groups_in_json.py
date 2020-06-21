import bpy
import json

########################################################
######## GET JSON WITH ALL BONES BY BONE GROUPS ########

def get_bones_from_group(target):
    arm_name = bpy.context.active_object.name
    armature = bpy.data.objects[arm_name]
    grupo_target = armature.pose.bone_groups[target]
    bones = []
    for b in armature.pose.bones:
        if b.bone_group == grupo_target:
            bones.append(b.name)
    return bones

data = {}
data['bone_groups'] = []

for bg in bpy.context.active_object.pose.bone_groups:
    bones = get_bones_from_group(bg.name)
    data['bone_groups'].append({
        'name': bg.name,
        'bones': bones,
    })


# lo guardo en tmp y luego lo muevo a mano a data_jsons.
with open('/tmp/bone_groups.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

########################################################

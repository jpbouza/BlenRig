import bpy
from ...snap_points import BLENRIG_OT_SnapPoints

class BLENRIG_PT_Cage_snapping_panel(bpy.types.Panel):
    bl_label = "Cage_snapping"
    bl_idname = "BLENRIG_PT_Cage_snapping_panel"
    bl_parent_id = "BLENRIG_PT_BlenRig_5_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False
        
        if context.mode not in ["EDIT_MESH"]:
            return False

        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["MESH"]):
            for mod in bpy.context.active_object.modifiers:
                if (mod.type in ["ARMATURE", "MESH_DEFORM"]):
                    return True

    def draw(self, context):
        arm = context.active_object
        arm_data = context.active_object.data
        props = context.window_manager.blenrig_5_props
        ob = context.active_object
        mesh = ob.data
        layout = self.layout


        # Cage Setup
        if context.mode in ["EDIT_MESH"]:
            box = layout.column()
            col = box.column()
            row = col.row()
            # row.alignment = 'CENTER'
            row = layout.row(align=True)
            comb = row.row()
            # row = layout.row(heading="Mirror")
            sub = row.row(align=True)
            sub.prop(mesh, "use_mirror_x",text= "X-Mirror")
            row.prop(mesh, "use_mirror_topology")
            col.operator("blenrig.snap_points", text="Ajust Cage", icon="NONE")
            row = layout.row(heading="Distance Cage")
            row.prop(props,"ajust_distance_cage",text="%", slider=True)
            
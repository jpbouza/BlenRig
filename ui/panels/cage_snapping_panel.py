import bpy
from ...snap_points import BLENRIG_OT_SnapPoints,BLENRIG_OT_center_loop_cage

class BLENRIG_PT_Cage_snapping_panel(bpy.types.Panel):
    bl_label = "Cage_snapping"
    bl_idname = "BLENRIG_PT_Cage_snapping_panel"
    bl_parent_id = "BLENRIG_PT_blenrig_6_general"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    @classmethod
    def poll(cls, context):
        BlenRigPanelOptions = context.window_manager.BlenRigPanelSettings
        if not BlenRigPanelOptions.displayContext == 'RIGTOOLS':
            return False
        
        if context.mode not in ["EDIT_MESH"]:
            return False

        if not context.active_object:
            return False
        if (context.active_object.type in ["MESH"]):
            for mod in context.active_object.modifiers:
                if (mod.type in ["ARMATURE", "MESH_DEFORM"]):
                    return True
        for prop in context.active_object.items():
                if prop[0] == 'BlenRig':
                    return True

    def draw(self, context):
        arm = context.active_object
        arm_data = context.active_object.data
        props = context.window_manager.blenrig_6_props
        ob = context.active_object
        mesh = ob.data
        layout = self.layout


        # Cage Setup
        if context.mode in ["EDIT_MESH"]:
            box = layout.column()
            col = box.column()
            row = col.row()
            row = layout.row(align=True)
            comb = row.row()
            sub = row.row(align=True)
            sub.prop(mesh, "use_mirror_x",text= "X-Mirror")
            row.prop(mesh, "use_mirror_topology")
            col.operator("blenrig.snap_points", text="Adjust Cage", icon="NONE")
            col.operator("blenrig.center_loop_cage", text="Center loop Cage", icon="NONE")
            row = layout.row(heading="Distance Cage")
            row.prop(props,"adjust_distance_cage",text="value")
            
            # row =layout.column()
            # row =layout.row()
            # row = layout.row(heading="Smooth Cage")            
            # row.prop(props,"smooth_repeat",text="Repiter Smooth")
            # row =layout.row(heading="Smooth Factor")
            # row.prop(props,"smooth_factor",text="Factor Smooth", slider=True)


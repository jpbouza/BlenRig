from bpy.app.handlers import persistent, load_pre


@persistent
def on_load_pre(dummy):
    from . guide_ops import BlenrigGuide_BaseOperator
    if BlenrigGuide_BaseOperator.instance:
        BlenrigGuide_BaseOperator.instance = None
        BlenrigGuide_BaseOperator.finish_draw()

def register():
    load_pre.append(on_load_pre)

def unregister():
    if on_load_pre in load_pre:
        load_pre.remove(on_load_pre)

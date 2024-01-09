import bpy
import gpu
from gpu_extras.batch import batch_for_shader

indices = ((0, 1, 2), (2, 1, 3))

if (4,0,0) >= bpy.app.version:
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
else:
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

def vertices(x, y, w, h): return [(x, y),(x+w, y),(x, y+h),(x+w, y+h)]

def Draw_Rectangle(p,s,co):
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices(*p,*s)}, indices=indices)
    shader.bind()
    shader.uniform_float("color", co)
    batch.draw(shader)

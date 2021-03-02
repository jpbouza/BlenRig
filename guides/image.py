import gpu
import bgl
from gpu_extras.batch import batch_for_shader

def get_img_verts(x,y,w,h): return ((x,y),(x+w,y),(x+w,y+h),(x,y+h))
shader = gpu.shader.from_builtin('2D_IMAGE')

def Draw_Image(p,s,i):
    if i.gl_touch():
        raise Exception()
    batch = batch_for_shader(
        shader, 'TRI_FAN',
        {
            "pos": get_img_verts(*p,*s),
            "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
        },
    )
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, i.bindcode)

    shader.bind()
    shader.uniform_int("image", 0)
    batch.draw(shader)

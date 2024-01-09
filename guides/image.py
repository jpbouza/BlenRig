import bpy
import gpu
from gpu_extras.batch import batch_for_shader

if (4,0,0) >= bpy.app.version:
    shader = gpu.shader.from_builtin('IMAGE')
else:
    shader = gpu.shader.from_builtin('2D_IMAGE')

texture_cache: dict[str, gpu.types.GPUTexture] = {}

def get_img_verts(x, y, w, h):
    return (
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h)
    )

def Draw_Image(p,s,i):
    if not i:
        print("ERROR: Draw_Image -> Invalid Image!")
        return
    if i.name in texture_cache:
        texture = texture_cache[i.name]
    else:
        texture = gpu.texture.from_image(i)
        texture_cache[i.name] = texture
    batch = batch_for_shader(
        shader, 'TRI_FAN',
        {
            "pos": get_img_verts(*p, *s),
            "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
        },
    )
    shader.bind()
    shader.uniform_sampler("image", texture)
    batch.draw(shader)

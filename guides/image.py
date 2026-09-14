# import gpu
# from gpu_extras.batch import batch_for_shader


# shader = gpu.shader.from_builtin('IMAGE')

# texture_cache: dict[str, gpu.types.GPUTexture] = {}


# def get_img_verts(x, y, w, h):
#     return (
#         (x, y),
#         (x + w, y),
#         (x + w, y + h),
#         (x, y + h)
#     )


# def Draw_Image(p,s,i):
#     if not i:
#         print("ERROR: Draw_Image -> Invalid Image!")
#         return
#     if i.name in texture_cache:
#         texture = texture_cache[i.name]
#     else:
#         texture = gpu.texture.from_image(i)
#         texture_cache[i.name] = texture
#     batch = batch_for_shader(
#         shader, 'TRI_FAN',
#         {
#             "pos": get_img_verts(*p, *s),
#             "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
#         },
#     )
#     shader.bind()
#     shader.uniform_sampler("image", texture)
#     batch.draw(shader)

import gpu
from gpu_extras.batch import batch_for_shader

# -----------------------------------------------------------------------------
# Shader interface
# -----------------------------------------------------------------------------

vert_out = gpu.types.GPUStageInterfaceInfo("my_interface")
vert_out.smooth('VEC2', "texCoord_interp")

# -----------------------------------------------------------------------------
# Shader definition
# -----------------------------------------------------------------------------

info = gpu.types.GPUShaderCreateInfo()

info.push_constant('MAT4', "ModelViewProjectionMatrix")

info.vertex_in(0, 'VEC2', "pos")
info.vertex_in(1, 'VEC2', "texCoord")

info.vertex_out(vert_out)

info.sampler(0, 'FLOAT_2D', "image")

info.fragment_out(0, 'VEC4', "fragColor")

info.vertex_source(
'''
void main()
{
    texCoord_interp = texCoord;
    gl_Position = ModelViewProjectionMatrix * vec4(pos.xy, 0.0, 1.0);
}
'''
)

info.fragment_source(
'''
void main()
{
    fragColor = texture(image, texCoord_interp);
}
'''
)

shader = gpu.shader.create_from_info(info)

# -----------------------------------------------------------------------------
# Texture cache
# -----------------------------------------------------------------------------

texture_cache: dict[str, gpu.types.GPUTexture] = {}

# -----------------------------------------------------------------------------
# Geometry
# -----------------------------------------------------------------------------

def get_img_verts(x, y, w, h):
    return (
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h)
    )

# -----------------------------------------------------------------------------
# Draw image
# -----------------------------------------------------------------------------

def Draw_Image(p, s, i):

    if not i:
        print("ERROR: Draw_Image -> Invalid Image!")
        return

    # Texture cache
    if i.name in texture_cache:
        texture = texture_cache[i.name]
    else:
        texture = gpu.texture.from_image(i)
        texture_cache[i.name] = texture

    x, y = p
    w, h = s

    batch = batch_for_shader(
        shader,
        'TRIS',
        {
            "pos": (
                (x, y),
                (x + w, y),
                (x + w, y + h),

                (x, y),
                (x + w, y + h),
                (x, y + h),
            ),

            "texCoord": (
                (0, 0),
                (1, 0),
                (1, 1),

                (0, 0),
                (1, 1),
                (0, 1),
            ),
        },
    )

    gpu.state.blend_set('ALPHA')

    shader.bind()
    shader.uniform_sampler("image", texture)

    batch.draw(shader)

    gpu.state.blend_set('NONE')
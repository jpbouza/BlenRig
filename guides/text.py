from blf import (
    enable as text_enable, disable as text_disable,
    SHADOW, shadow as text_shadow, shadow_offset as text_shadow_offset,
    color as text_color, position as text_position, size as text_size,
    dimensions as text_dim, draw as text_draw, ROTATION, rotation as text_rotation,
    clipping as text_clipping, CLIPPING, KERNING_DEFAULT, WORD_WRAP, MONOCHROME, word_wrap as text_wrap
)


def Draw_Text(_x, _y, _text, _size, _dpi, _id = 0, _r = 1, _g = 1, _b = 1, _a = 1):
    text_color(_id, _r, _g, _b, _a)
    text_position(_id, _x, _y, 0)
    text_size(_id, _size, _dpi)
    text_draw(_id, _text)

def Draw_Text_Wrap(_x, _y, _w, _text, _size, _dpi, _id = 0, _r = 1, _g = 1, _b = 1, _a = 1):
    text_enable(_id, WORD_WRAP)
    text_wrap(_id, _w)
    Draw_Text(_x,_y,_text,_size,_dpi,_id,_r,_g,_b,_a)
    text_disable(_id, WORD_WRAP)

def SetSizeGetDim(_id, _size, _dpi, _txt):
    text_size(_id, _size, _dpi)
    return text_dim(_id, _txt)

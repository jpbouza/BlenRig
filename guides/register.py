# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy

def register():
    from .properties import BlenrigGuideData
    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    from bpy.utils import register_class
    register_class(BlenrigGuideData)
    scn.blenrig_guide = Pointer(type=BlenrigGuideData, name="Blenrig Guide")
    
    from .panel import BlendrigGuidePanel
    from .operator import VIEW3D_OT_blenrig_guide
    register_class(VIEW3D_OT_blenrig_guide)
    register_class(BlendrigGuidePanel)

def unregister():
    from .panel import BlendrigGuidePanel
    from .operator import VIEW3D_OT_blenrig_guide
    from bpy.utils import unregister_class
    unregister_class(BlendrigGuidePanel)
    unregister_class(VIEW3D_OT_blenrig_guide)

    from .properties import BlenrigGuideData
    from bpy.types import Scene as scn
    del scn.blenrig_guide
    unregister_class(BlenrigGuideData)

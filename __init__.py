bl_info = {
    "name": "One Click Bake",
    "author": "You",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from .bake_operator import OBJECT_OT_oneclick_bake


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_oneclick_bake.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_oneclick_bake)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_oneclick_bake)


if __name__ == "__main__":
    register()
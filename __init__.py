bl_info = {
    "name": "One Click Bake",
    "author": "Bronson",
    "version": (0, 6, 0),
    "blender": (3, 0, 0),
    "category": "Object",
    "description": "One-click baking directly into shader nodes",
}

import bpy

from .bake_operator import (
    OBJECT_OT_bake_albedo,
    OBJECT_OT_bake_normal,
    OBJECT_OT_bake_roughness,
)


class VIEW3D_PT_oneclick_bake(bpy.types.Panel):
    bl_label = "One Click Bake"
    bl_idname = "VIEW3D_PT_oneclick_bake"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bake"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.bake_albedo")
        layout.operator("object.bake_normal")
        layout.operator("object.bake_roughness")


classes = (
    OBJECT_OT_bake_albedo,
    OBJECT_OT_bake_normal,
    OBJECT_OT_bake_roughness,
    VIEW3D_PT_oneclick_bake,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
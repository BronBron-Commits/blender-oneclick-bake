import bpy
import os


# -------------------------
# SETUP
# -------------------------
def prepare(context):
    obj = context.active_object

    if not obj or obj.type != 'MESH':
        return None, "Select a mesh object"

    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    if not obj.active_material or not obj.active_material.use_nodes:
        return None, "Material with nodes required"

    if not obj.data.uv_layers:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    context.view_layer.objects.active = obj

    return obj, None


def get_principled(nodes):
    for n in nodes:
        if n.type == 'BSDF_PRINCIPLED':
            return n
    return None


def activate_node(node):
    tree = node.id_data

    for n in tree.nodes:
        n.select = False

    node.select = True
    tree.nodes.active = node


def save(img, obj_name, suffix):
    path = bpy.path.abspath(f"//bakes/{obj_name.lower()}_{suffix}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.filepath_raw = path
    img.file_format = 'PNG'
    img.save()


# -------------------------
# ALBEDO
# -------------------------
class OBJECT_OT_bake_albedo(bpy.types.Operator):
    bl_idname = "object.bake_albedo"
    bl_label = "Bake Albedo"

    def execute(self, context):
        obj, err = prepare(context)
        if err:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}

        scene = context.scene
        scene.render.engine = 'CYCLES'

        nodes = obj.active_material.node_tree.nodes
        links = obj.active_material.node_tree.links

        principled = get_principled(nodes)
        if not principled:
            return {'CANCELLED'}

        img = bpy.data.images.new(f"{obj.name}_albedo", 1024, 1024)

        tex = nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.location = principled.location.x - 300, principled.location.y

        activate_node(tex)

        scene.cycles.bake_type = 'DIFFUSE'
        scene.render.bake.use_pass_color = True
        scene.render.bake.use_clear = True

        bpy.ops.object.bake(type='DIFFUSE')

        save(img, obj.name, "albedo")

        links.new(tex.outputs["Color"], principled.inputs["Base Color"])

        return {'FINISHED'}


# -------------------------
# NORMAL
# -------------------------
class OBJECT_OT_bake_normal(bpy.types.Operator):
    bl_idname = "object.bake_normal"
    bl_label = "Bake Normal"

    def execute(self, context):
        obj, err = prepare(context)
        if err:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}

        scene = context.scene
        scene.render.engine = 'CYCLES'

        nodes = obj.active_material.node_tree.nodes
        links = obj.active_material.node_tree.links

        principled = get_principled(nodes)
        if not principled:
            return {'CANCELLED'}

        img = bpy.data.images.new(f"{obj.name}_normal", 1024, 1024)

        tex = nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.image.colorspace_settings.name = 'Non-Color'
        tex.location = principled.location.x - 300, principled.location.y - 200

        activate_node(tex)

        scene.cycles.bake_type = 'NORMAL'
        scene.render.bake.normal_space = 'TANGENT'
        scene.render.bake.use_clear = True

        bpy.ops.object.bake(type='NORMAL')

        save(img, obj.name, "normal")

        normal_map = nodes.new("ShaderNodeNormalMap")
        normal_map.location = tex.location.x + 200, tex.location.y

        links.new(tex.outputs["Color"], normal_map.inputs["Color"])
        links.new(normal_map.outputs["Normal"], principled.inputs["Normal"])

        return {'FINISHED'}


# -------------------------
# ROUGHNESS
# -------------------------
class OBJECT_OT_bake_roughness(bpy.types.Operator):
    bl_idname = "object.bake_roughness"
    bl_label = "Bake Roughness"

    def execute(self, context):
        obj, err = prepare(context)
        if err:
            self.report({'ERROR'}, err)
            return {'CANCELLED'}

        scene = context.scene
        scene.render.engine = 'CYCLES'

        nodes = obj.active_material.node_tree.nodes
        links = obj.active_material.node_tree.links

        principled = get_principled(nodes)
        if not principled:
            return {'CANCELLED'}

        img = bpy.data.images.new(f"{obj.name}_roughness", 1024, 1024)

        tex = nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.image.colorspace_settings.name = 'Non-Color'
        tex.location = principled.location.x - 300, principled.location.y - 400

        activate_node(tex)

        scene.cycles.bake_type = 'EMIT'
        scene.render.bake.use_clear = True

        bpy.ops.object.bake(type='EMIT')

        save(img, obj.name, "roughness")

        links.new(tex.outputs["Color"], principled.inputs["Roughness"])

        return {'FINISHED'}
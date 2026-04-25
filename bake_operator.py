import bpy

class OBJECT_OT_oneclick_bake(bpy.types.Operator):
    bl_idname = "object.oneclick_bake"
    bl_label = "One Click Bake"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        bpy.context.scene.render.engine = 'CYCLES'

        img = bpy.data.images.new("Bake_Albedo", width=1024, height=1024)

        mat = obj.active_material
        if not mat or not mat.use_nodes:
            self.report({'ERROR'}, "Object needs a material with nodes")
            return {'CANCELLED'}

        nodes = mat.node_tree.nodes
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = img
        nodes.active = tex_node

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        bpy.context.scene.cycles.bake_type = 'DIFFUSE'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_color = True

        bpy.ops.object.bake(type='DIFFUSE')

        self.report({'INFO'}, "Bake complete")
        return {'FINISHED'}
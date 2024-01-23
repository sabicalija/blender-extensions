import bpy

class SelectVertexOperator(bpy.types.Operator):
    bl_idname = "object.select_vertex_operator"
    bl_label = "Select Next Vertex"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            mesh = obj.data

            # Find the currently selected vertex
            selected_vertices = [v for v in mesh.vertices if v.select]
            if selected_vertices:
                current_vertex = selected_vertices[0]
                next_vertex_index = (current_vertex.index + 1) % len(mesh.vertices)
            else:
                next_vertex_index = 0

            # Switch to object mode to update the selection
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect all vertices
            for v in mesh.vertices:
                v.select = False

            # Select the next vertex
            mesh.vertices[next_vertex_index].select = True

            # Switch back to edit mode to see the selection
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class ResetVertexOperator(bpy.types.Operator):
    bl_idname = "object.reset_vertex_operator"
    bl_label = "Select Vertex 0"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            mesh = obj.data

            # Switch to object mode to update the selection
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect all vertices
            for v in mesh.vertices:
                v.select = False

            # Select the vertex with index 0
            if len(mesh.vertices) > 0:
                mesh.vertices[0].select = True

            # Switch back to edit mode to see the selection
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class SelectVertexByIndexOperator(bpy.types.Operator):
    bl_idname = "object.select_vertex_by_index_operator"
    bl_label = "Select Vertex By Index"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            mesh = obj.data

            # Switch to object mode to update the selection
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect all vertices
            for v in mesh.vertices:
                v.select = False

            # Select the vertex with the specified index
            vertex_index = obj.vertex_index
            if 0 <= vertex_index < len(mesh.vertices):
                mesh.vertices[vertex_index].select = True

            # Switch back to edit mode to see the selection
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class VertexSelectorPanel(bpy.types.Panel):
    bl_label = "Vertex Selector"
    bl_idname = "OBJECT_PT_vertex_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.active_object
        if obj and obj.type == 'MESH':
            mesh = obj.data

            # Display the total number of vertices
            row = layout.row()
            row.label(text="Total vertices: " + str(len(mesh.vertices)))

            # Display the currently selected vertex
            selected_vertices = [v for v in mesh.vertices if v.select]
            if selected_vertices:
                current_vertex = selected_vertices[0]
                row = layout.row()
                row.label(text="Selected vertex: " + str(current_vertex.index))

            # Button to select the next vertex
            row = layout.row()
            row.operator("object.select_vertex_operator")

            # Button to reset the position of the current vertex
            row = layout.row()
            row.operator("object.reset_vertex_operator")

            # Input box to enter the vertex index directly
            row = layout.row()
            row.prop(obj, "vertex_index", text="Vertex Index")

            # Button to select the vertex with the specified index
            row = layout.row()
            row.operator("object.select_vertex_by_index_operator")

def register():
    bpy.utils.register_class(SelectVertexOperator)
    bpy.utils.register_class(ResetVertexOperator)
    bpy.utils.register_class(SelectVertexByIndexOperator)
    bpy.utils.register_class(VertexSelectorPanel)

    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        max_vertex_index = len(obj.data.vertices) - 1
    else:
        max_vertex_index = 100  # Default value

    bpy.types.Object.vertex_index = bpy.props.IntProperty(
        name="Vertex Index",
        default=0,
        soft_min=0,
        soft_max=max_vertex_index,
    )

def unregister():
    bpy.utils.unregister_class(VertexSelectorPanel)
    bpy.utils.unregister_class(SelectVertexByIndexOperator)
    bpy.utils.unregister_class(ResetVertexOperator)
    bpy.utils.unregister_class(SelectVertexOperator)
    del bpy.types.Object.vertex_index

if __name__ == "__main__":
    register()

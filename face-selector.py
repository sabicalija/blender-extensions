import bpy

class SelectFaceOperator(bpy.types.Operator):
    bl_idname = "object.select_face_operator"
    bl_label = "Select Next Face"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            mesh = obj.data

            # Find the currently selected face
            selected_faces = [f for f in mesh.polygons if f.select]
            if selected_faces:
                current_face = selected_faces[0]
                next_face_index = (current_face.index + 1) % len(mesh.polygons)
            else:
                next_face_index = 0

            # Switch to edit mode and set the selection mode to faces
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='FACE')

            # Deselect all faces
            bpy.ops.mesh.select_all(action='DESELECT')

            # Switch to object mode to update the selection
            bpy.ops.object.mode_set(mode='OBJECT')

            # Select the next face
            mesh.polygons[next_face_index].select = True

            # Switch back to edit mode to see the selection
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class ResetFaceOperator(bpy.types.Operator):
    bl_idname = "object.reset_face_operator"
    bl_label = "Select Face 0"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            # Set the face_index property to 0
            obj.face_index = 0

            # Call the SelectFaceByIndexOperator
            bpy.ops.object.select_face_by_index_operator()

        return {'FINISHED'}

class SelectFaceByIndexOperator(bpy.types.Operator):
    bl_idname = "object.select_face_by_index_operator"
    bl_label = "Select Face By Index"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj.type == 'MESH':
            mesh = obj.data

            # Switch to edit mode and set the selection mode to faces
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='FACE')

            # Deselect all faces
            bpy.ops.mesh.select_all(action='DESELECT')

            # Switch to object mode to update the selection
            bpy.ops.object.mode_set(mode='OBJECT')

            # Select the face with the specified index
            face_index = obj.face_index
            if 0 <= face_index < len(mesh.polygons):
                mesh.polygons[face_index].select = True

            # Switch back to edit mode to see the selection
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class FaceSelectorPanel(bpy.types.Panel):
    bl_label = "Face Selector"
    bl_idname = "OBJECT_PT_face_selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.active_object
        if obj and obj.type == 'MESH':
            mesh = obj.data

            # Display the total number of faces
            row = layout.row()
            row.label(text="Total faces: " + str(len(mesh.polygons)))

            # Display the currently selected face
            selected_faces = [f for f in mesh.polygons if f.select]
            if selected_faces:
                current_face = selected_faces[0]
                row = layout.row()
                row.label(text="Selected face: " + str(current_face.index))

            # Button to select the next face
            row = layout.row()
            row.operator("object.select_face_operator")

            # Button to select face 0
            row = layout.row()
            row.operator("object.reset_face_operator")

            # Input box to enter the face index directly
            row = layout.row()
            row.prop(obj, "face_index", text="Face Index")

            # Button to select the face with the specified index
            row = layout.row()
            row.operator("object.select_face_by_index_operator")

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



def register():
    bpy.utils.register_class(SelectFaceOperator)
    bpy.utils.register_class(ResetFaceOperator)
    bpy.utils.register_class(SelectFaceByIndexOperator)
    bpy.utils.register_class(FaceSelectorPanel)

    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        max_polygon_index = len(obj.data.polygons) - 1
    else:
        max_polygon_index = 100  # Default value

    bpy.types.Object.face_index = bpy.props.IntProperty(
        name="Face Index",
        default=0,
        soft_min=0,
        soft_max=max_polygon_index,
    )

    bpy.types.Mesh.face_index_soft_max = bpy.props.IntProperty(
        name="Face Index Soft Max",
        default=100,  # Default value
    )

    # Update the soft_max whenever the mesh is updated
    @bpy.app.handlers.persistent
    def update_face_index_soft_max(dummy):
        for mesh in bpy.data.meshes:
            mesh.face_index_soft_max = len(mesh.polygons) - 1

    bpy.app.handlers.depsgraph_update_post.append(update_face_index_soft_max)

def unregister():
    bpy.utils.unregister_class(FaceSelectorPanel)
    bpy.utils.unregister_class(SelectFaceByIndexOperator)
    bpy.utils.unregister_class(ResetFaceOperator)
    bpy.utils.unregister_class(SelectFaceOperator)
    del bpy.types.Object.face_index
    del bpy.types.Mesh.face_index_soft_max

    bpy.app.handlers.depsgraph_update_post.clear()

if __name__ == "__main__":
    register()
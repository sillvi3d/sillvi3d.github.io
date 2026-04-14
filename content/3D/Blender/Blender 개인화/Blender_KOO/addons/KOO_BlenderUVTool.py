bl_info = {
    "name": "UV Tools Panel",
    "author": "Custom",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > UV Tools",
    "description": "Mark/Clear Seam, Mark/Clear Sharp, Smart UV Unwrap",
    "category": "UV",
}

import bpy


class UV_OT_mark_seam(bpy.types.Operator):
    bl_idname = "uv.custom_mark_seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}


class UV_OT_clear_seam(bpy.types.Operator):
    bl_idname = "uv.custom_clear_seam"
    bl_label = "Clear Seam"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=True)
        return {'FINISHED'}


class UV_OT_mark_sharp(bpy.types.Operator):
    bl_idname = "uv.custom_mark_sharp"
    bl_label = "Mark Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.mark_sharp()
        return {'FINISHED'}


class UV_OT_clear_sharp(bpy.types.Operator):
    bl_idname = "uv.custom_clear_sharp"
    bl_label = "Clear Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.mark_sharp(clear=True)
        return {'FINISHED'}


class UV_OT_smart_unwrap(bpy.types.Operator):
    bl_idname = "uv.custom_smart_unwrap"
    bl_label = "Smart UV Unwrap"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.uv.smart_project()
        return {'FINISHED'}


class UV_PT_tools_panel(bpy.types.Panel):
    bl_label = "UV Tools"
    bl_idname = "UV_PT_tools_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UV Tools"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Seam")
        row = layout.row(align=True)
        row.operator("uv.custom_mark_seam", text="Mark Seam", icon='RESTRICT_SELECT_OFF')
        row.operator("uv.custom_clear_seam", text="Clear Seam", icon='X')

        layout.separator()

        layout.label(text="Sharp")
        row = layout.row(align=True)
        row.operator("uv.custom_mark_sharp", text="Mark Sharp", icon='SHARPCURVE')
        row.operator("uv.custom_clear_sharp", text="Clear Sharp", icon='X')

        layout.separator()

        layout.label(text="Unwrap")
        layout.operator("uv.custom_smart_unwrap", text="Smart UV Unwrap", icon='UV')


classes = [
    UV_OT_mark_seam,
    UV_OT_clear_seam,
    UV_OT_mark_sharp,
    UV_OT_clear_sharp,
    UV_OT_smart_unwrap,
    UV_PT_tools_panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

# =============================================================
# KOO_BlendHub.py
# Author  : KOO
# Version : 1.3.0
# Created : 2025-xx-xx
# Desc    : 커스텀 툴 허브 UI
# -------------------------------------------------------------
# Changelog
# 1.0.0 - 초기 버전
# 1.1.0 - 자동 감지 시스템
# 1.2.0 - 토글/순서/단축키
# 1.2.2 - 단축키 Alt+` 변경
# 1.3.0 - Alt+1~9 각 순서 토글, 테스트 패널 내장
# =============================================================

bl_info = {
    "name"       : "KOO BlendHub",
    "author"     : "KOO",
    "version"    : (1, 3, 0),
    "blender"    : (4, 0, 0),
    "location"   : "View3D > Sidebar > BLEND",
    "description": "커스텀 툴 허브 패널",
    "category"   : "User",
}

import bpy

# -------------------------------------------------------------
# 전역 레지스트리
# -------------------------------------------------------------

_koo_registry = []

def register_koo_panel(label, draw_func):
    for e in _koo_registry:
        if e["label"] == label:
            e["draw"] = draw_func
            return
    _koo_registry.append({"label": label, "draw": draw_func})

def unregister_koo_panel(label):
    global _koo_registry
    _koo_registry = [e for e in _koo_registry if e["label"] != label]


# -------------------------------------------------------------
# 상태 PropertyGroup
# -------------------------------------------------------------

class KOO_PG_HubState(bpy.types.PropertyGroup):
    expanded_0 : bpy.props.BoolProperty(default=False)
    expanded_1 : bpy.props.BoolProperty(default=False)
    expanded_2 : bpy.props.BoolProperty(default=False)
    expanded_3 : bpy.props.BoolProperty(default=False)
    expanded_4 : bpy.props.BoolProperty(default=False)
    expanded_5 : bpy.props.BoolProperty(default=False)
    expanded_6 : bpy.props.BoolProperty(default=False)
    expanded_7 : bpy.props.BoolProperty(default=False)
    expanded_8 : bpy.props.BoolProperty(default=False)
    expanded_9 : bpy.props.BoolProperty(default=False)
    order      : bpy.props.StringProperty(default="")


def _get_order(state):
    n = len(_koo_registry)
    if not n:
        return []
    if not state.order:
        return list(range(n))
    try:
        order   = [int(x) for x in state.order.split(",") if x.strip().isdigit()]
        valid   = [i for i in order if i < n]
        missing = [i for i in range(n) if i not in valid]
        return valid + missing
    except:
        return list(range(n))


def _save_order(state, order):
    state.order = ",".join(str(i) for i in order)


def _get_exp(state, idx):
    return getattr(state, f"expanded_{min(idx, 9)}")


def _set_exp(state, idx, val):
    setattr(state, f"expanded_{min(idx, 9)}", val)


def _toggle_by_display(context, display_idx):
    if not hasattr(context.scene, 'koo_hub_state'):
        return
    state = context.scene.koo_hub_state
    order = _get_order(state)
    if display_idx < len(order):
        real = order[display_idx]
        _set_exp(state, real, not _get_exp(state, real))
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()


# -------------------------------------------------------------
# 오퍼레이터 — 토글 (패널 클릭용)
# -------------------------------------------------------------

class KOO_OT_TogglePanel(bpy.types.Operator):
    bl_idname = "koo.toggle_panel"
    bl_label  = "Toggle Panel"
    index     : bpy.props.IntProperty()

    def execute(self, context):
        _toggle_by_display(context, self.index)
        return {'FINISHED'}


# -------------------------------------------------------------
# 오퍼레이터 — 단축키 Alt+1~9
# -------------------------------------------------------------

class KOO_OT_HotkeyToggle(bpy.types.Operator):
    bl_idname  = "koo.hotkey_toggle"
    bl_label   = "KOO Hotkey Toggle"
    bl_options = {'REGISTER'}
    slot       : bpy.props.IntProperty()   # 0-based display index

    def execute(self, context):
        _toggle_by_display(context, self.slot)
        return {'FINISHED'}


# -------------------------------------------------------------
# 오퍼레이터 — 순서 이동
# -------------------------------------------------------------

class KOO_OT_MovePanel(bpy.types.Operator):
    bl_idname = "koo.move_panel"
    bl_label  = "Move Panel"
    index     : bpy.props.IntProperty()
    direction : bpy.props.StringProperty()

    def execute(self, context):
        state = context.scene.koo_hub_state
        order = _get_order(state)
        i = self.index
        if self.direction == 'UP' and i > 0:
            order[i], order[i-1] = order[i-1], order[i]
        elif self.direction == 'DOWN' and i < len(order) - 1:
            order[i], order[i+1] = order[i+1], order[i]
        _save_order(state, order)
        return {'FINISHED'}


# -------------------------------------------------------------
# UV Tools 오퍼레이터
# -------------------------------------------------------------

class KOO_OT_MarkSeam(bpy.types.Operator):
    bl_idname = "koo.mark_seam"; bl_label = "Mark Seam"; bl_options = {'REGISTER','UNDO'}
    def execute(self, c): bpy.ops.mesh.mark_seam(clear=False); return {'FINISHED'}

class KOO_OT_ClearSeam(bpy.types.Operator):
    bl_idname = "koo.clear_seam"; bl_label = "Clear Seam"; bl_options = {'REGISTER','UNDO'}
    def execute(self, c): bpy.ops.mesh.mark_seam(clear=True); return {'FINISHED'}

class KOO_OT_MarkSharp(bpy.types.Operator):
    bl_idname = "koo.mark_sharp"; bl_label = "Mark Sharp"; bl_options = {'REGISTER','UNDO'}
    def execute(self, c): bpy.ops.mesh.mark_sharp(); return {'FINISHED'}

class KOO_OT_ClearSharp(bpy.types.Operator):
    bl_idname = "koo.clear_sharp"; bl_label = "Clear Sharp"; bl_options = {'REGISTER','UNDO'}
    def execute(self, c): bpy.ops.mesh.mark_sharp(clear=True); return {'FINISHED'}

class KOO_OT_SmartUvUnwrap(bpy.types.Operator):
    bl_idname = "koo.smart_uv_unwrap"; bl_label = "Smart UV Unwrap"; bl_options = {'REGISTER','UNDO'}
    def execute(self, c): bpy.ops.uv.smart_project(); return {'FINISHED'}


# -------------------------------------------------------------
# 메인 허브 패널
# -------------------------------------------------------------

class KOO_PT_BlendHub(bpy.types.Panel):
    bl_label       = "KOO BlendHub  v1.3.0"
    bl_idname      = "KOO_PT_BlendHub"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = "BLEND"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Custom Tools by KOO", icon='MONKEY')

        if not _koo_registry:
            layout.label(text="등록된 툴 없음", icon='INFO')
            return

        state = context.scene.koo_hub_state
        order = _get_order(state)

        for di, real in enumerate(order):
            entry    = _koo_registry[real]
            expanded = _get_exp(state, real)
            box      = layout.box()
            header   = box.row(align=True)

            # 위아래 버튼
            col = header.column(align=True)
            up  = col.operator("koo.move_panel", text="", icon='TRIA_UP',   emboss=False)
            up.index = di; up.direction = 'UP'
            dn  = col.operator("koo.move_panel", text="", icon='TRIA_DOWN', emboss=False)
            dn.index = di; dn.direction = 'DOWN'

            # 토글 버튼
            tog       = header.operator(
                "koo.toggle_panel",
                text=entry["label"],
                icon='DISCLOSURE_TRI_DOWN' if expanded else 'DISCLOSURE_TRI_RIGHT',
                emboss=False,
            )
            tog.index = di

            # 단축키 힌트 (Alt+1 ~ Alt+9)
            if di < 9:
                hint         = header.row()
                hint.enabled = False
                hint.label(text=f"⌥{di+1}")

            if expanded:
                entry["draw"](box.column(), context)


# -------------------------------------------------------------
# UV / Test draw 함수
# -------------------------------------------------------------

def _draw_uv_tools(layout, context):
    layout.label(text="Seam")
    r = layout.row(align=True)
    r.operator("koo.mark_seam",  text="Mark",  icon='RESTRICT_SELECT_OFF')
    r.operator("koo.clear_seam", text="Clear", icon='X')
    layout.separator()
    layout.label(text="Sharp")
    r = layout.row(align=True)
    r.operator("koo.mark_sharp",  text="Mark",  icon='SHARPCURVE')
    r.operator("koo.clear_sharp", text="Clear", icon='X')
    layout.separator()
    layout.operator("koo.smart_uv_unwrap", text="Smart UV Unwrap", icon='UV')


def _draw_test_panel(layout, context):
    layout.label(text="테스트 패널 — 순서 확인용", icon='CHECKMARK')
    layout.label(text="이 패널이 보이면 등록 성공!")


# -------------------------------------------------------------
# 단축키 Alt+1 ~ Alt+9
# -------------------------------------------------------------

_KEY_MAP = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE']
addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    for slot, key in enumerate(_KEY_MAP):
        kmi      = km.keymap_items.new("koo.hotkey_toggle", type=key, value='PRESS', alt=True)
        kmi.properties.slot = slot
        addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


# -------------------------------------------------------------
# 등록
# -------------------------------------------------------------

classes = [
    KOO_PG_HubState,
    KOO_OT_TogglePanel,
    KOO_OT_HotkeyToggle,
    KOO_OT_MovePanel,
    KOO_OT_MarkSeam,
    KOO_OT_ClearSeam,
    KOO_OT_MarkSharp,
    KOO_OT_ClearSharp,
    KOO_OT_SmartUvUnwrap,
    KOO_PT_BlendHub,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.koo_hub_state = bpy.props.PointerProperty(type=KOO_PG_HubState)
    register_koo_panel("UV Tools  v1.0.0", _draw_uv_tools)
    register_koo_panel("Test Panel  v1.0.0", _draw_test_panel)
    register_keymaps()

def unregister():
    unregister_keymaps()
    unregister_koo_panel("UV Tools  v1.0.0")
    unregister_koo_panel("Test Panel  v1.0.0")
    if hasattr(bpy.types.Scene, 'koo_hub_state'):
        del bpy.types.Scene.koo_hub_state
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
---
title: Blender 커스텀 애드온 네이밍 규칙 및 구조
---

## 식별자

모든 커스텀 애드온은 접두사 `KOO_` 로 시작합니다. 본인이 직접 제작한 애드온임을 식별하기 위한 고유 식별자입니다.

---

## 파일명 규칙

```
KOO_[기능명].py
```

- 접두사: `KOO_` (고정)
- 기능명: PascalCase 적용
- 버전: 파일명에 포함하지 않음 → 코드 내부에서 관리

### 예시

|파일명|기능 설명|
|---|---|
|`KOO_BlendHub.py`|커스텀 툴 허브 UI (메인 패널)|
|`KOO_UvToolsPanel.py`|UV Seam / Sharp / Unwrap 툴|
|`KOO_BatchExporter.py`|FBX 일괄 익스포트|
|`KOO_MeshCleaner.py`|트랜스폼 Apply, 노멀 정리|
|`KOO_NamingTools.py`|오브젝트 이름 일괄 변경|
|`KOO_TextureChecker.py`|텍셀 밀도 / UV 겹침 확인|

---

## 코드 내부 구조 규칙

### 파일 상단 헤더 (필수)

```python
# =============================================================
# KOO_[기능명].py
# Author  : KOO
# Version : 1.0.0
# Created : YYYY-MM-DD
# Desc    : 기능 설명
# -------------------------------------------------------------
# Changelog
# 1.0.0 - 초기 버전
# 1.0.1 - 버그 수정 내용
# 1.1.0 - 기능 추가 내용
# =============================================================
```

### 버전 관리 규칙

|버전 구성|의미|
|---|---|
|Major (1.x.x)|구조적 변경 또는 대규모 기능 추가|
|Minor (x.1.x)|기능 추가|
|Patch (x.x.1)|버그 수정 / 소소한 수정|

### bl_info 필수 항목

```python
bl_info = {
    "name"       : "KOO [기능명]",
    "author"     : "KOO",
    "version"    : (1, 0, 0),
    "blender"    : (4, 0, 0),
    "location"   : "View3D > Sidebar > BLEND",
    "description": "기능 설명",
    "category"   : "User",
}
```

---

## 클래스 네이밍 규칙

블랜더 애드온 클래스는 타입별로 접두사가 정해져 있습니다.

|타입|형식|예시|
|---|---|---|
|Operator|`KOO_OT_[기능명]`|`KOO_OT_MarkSeam`|
|Panel|`KOO_PT_[패널명]`|`KOO_PT_UvTools`|
|Menu|`KOO_MT_[메뉴명]`|`KOO_MT_ExportMenu`|
|Property Group|`KOO_PG_[속성명]`|`KOO_PG_ExportSettings`|

`bl_idname` 은 소문자 + 언더스코어로 변환합니다.

```python
# 클래스명     : KOO_OT_MarkSeam
# bl_idname  : "koo.mark_seam"

# 클래스명     : KOO_PT_UvTools
# bl_idname  : "KOO_PT_UvTools"
```

---

## 허브 구조

모든 커스텀 패널은 `BLEND` 탭 하나에 집중 관리합니다. 새 패널 추가 시 반드시 `bl_parent_id = "KOO_PT_BlendHub"` 를 지정합니다.

```
BLEND 탭
└── KOO_PT_BlendHub        ← 메인 허브 (항상 최상단)
    ├── KOO_PT_UvTools     ← UV 툴
    ├── KOO_PT_MeshTools   ← 메시 툴 (예정)
    ├── KOO_PT_ExportTools ← 익스포트 툴 (예정)
    └── KOO_PT_NamingTools ← 네이밍 툴 (예정)
```

---

## 파일 디렉토리 구조

```
📁 Blender_KOO/
├── 📄 README.md                    ← 전체 설정 관리 문서
├── 📄 KOO_AddonNamingConvention.md ← 이 문서
├── 📁 addons/
│   ├── 📄 KOO_BlendHub.py
│   ├── 📄 KOO_UvToolsPanel.py      ← (허브에 통합 예정)
│   └── 📄 ...
├── 📁 presets/
│   ├── 📄 startup.blend
│   └── 📄 userpref.blend
└── 📁 docs/
    └── 📄 Troubleshooting.md
```

---

## 애드온 현황

|파일명|버전|상태|기능|
|---|---|---|---|
|`KOO_BlendHub.py`|1.0.0|운영중|커스텀 툴 허브 UI|
|||||

> 새 애드온 추가 시 위 표에 기록
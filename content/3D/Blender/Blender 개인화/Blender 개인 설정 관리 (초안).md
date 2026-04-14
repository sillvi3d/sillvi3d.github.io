---
title: Blender 개인 설정 관리 (초안)
---

## 버전 정보

- Blender: `5.1.0`
- 최종 업데이트: 2025-xx-xx
- 운영체제: Windows / Mac (해당 항목 유지)

---

## 설치 및 초기 셋팅 체크리스트

새 PC 또는 재설치 시 아래 순서대로 진행

- [ ] Blender 5.1.0 설치 (공홈 또는 Steam)
- [ ] Startup File 불러오기 (`startup.blend` 덮어쓰기)
- [ ] Preferences 불러오기 (`userpref.blend` 덮어쓰기)
- [ ] 애드온 설치 (아래 목록 참고)
- [ ] 커스텀 단축키 확인
- [ ] 유닛 셋팅 확인

---

## 유닛 셋팅

|항목|값|
|---|---|
|Unit System|Metric|
|Unit Scale|1.000000|
|Length|Centimeters|
|Rotation|Degrees|

> 익스포트 전 항상 Ctrl+A → Apply All Transform 필수

---

## Navigation 셋팅

|항목|값|
|---|---|
|Keymap Preset|Blender (기본)|
|Orbit Method|Turntable|
|Orbit Around Selection|ON|
|Zoom to Mouse Position|ON|
|Transform Navigation with Alt|ON|

> Snapping 단축키 → Shift+Q 로 커스텀 지정

---

## 커스텀 단축키 목록

|기능|단축키|비고|
|---|---|---|
|Snapping 메뉴|Shift+Q|기본값 Shift+Tab에서 변경|
||||
||||

> 추가 커스텀 단축키 발생 시 여기에 기록

---

## 뷰포트 셋팅

|항목|값|
|---|---|
|Clip Start|0.1 cm|
|Clip End|100000 cm|
|Grid Scale|10|
|Grid Subdivisions|10|

---

## Overlay 셋팅

|항목|상태|
|---|---|
|Wireframe Overlay|필요시 ON|
|Face Orientation|노멀 확인 시 ON|
|Statistics|필요시 ON|
|Seams|ON|

---

## 애드온 목록

### 내장 애드온 (활성화 필요)

|애드온|용도|
|---|---|
|Loop Tools|버텍스/엣지 원형 정렬 등|
|Node Wrangler|셰이더 노드 작업 편의|
|Magic UV|UV 복사/붙여넣기 등|
|Extra Mesh Objects|추가 프리미티브|

### 외부 애드온

|애드온|버전|용도|출처|
|---|---|---|---|
|TexTools|-|UV 작업 보조|GitHub|
|Zen UV|-|UV 종합 툴|Blender Market|
|Send to Unreal|-|언리얼 직접 연동|Epic Games GitHub|
|Mesh Align Plus|-|오브젝트 정렬|Blender Market|

### 커스텀 애드온 (직접 제작)

|파일명|버전|기능|
|---|---|---|
|uv_tools_panel.py|1.0|Mark/Clear Seam, Sharp, Smart UV Unwrap|
||||

---

## FBX 익스포트 프리셋

### 언리얼 엔진용

|항목|값|
|---|---|
|Scale|1.0|
|Apply Unit|ON|
|Apply Transform|ON|
|Forward Axis|-Z|
|Up Axis|Y|

### Substance Painter용

|항목|값|
|---|---|
|Scale|1.0|
|Apply Unit|ON|
|Smoothing Groups|ON|

---

## 파이프라인 워크플로우

### 게임 배경 에셋 기본 플로우

1. 블랜더에서 로우폴리 모델링
2. Ctrl+A → Apply All Transform
3. Mark Sharp + Mark Seam (동일 엣지에 동시 적용)
4. Shade Auto Smooth 180도
5. UV 언랩
6. FBX 익스포트 (언리얼 프리셋)
7. Substance Painter 베이크
8. 언리얼 임포트

### 하이폴/로우폴 베이크 플로우

1. 로우폴 먼저 실루엣 확정
2. 하이폴 제작 (베벨/서브디비전)
3. 네이밍 규칙 적용 (`_low` / `_high`)
4. Substance Painter 베이크
5. 노멀맵 확인 후 보정

---

## 네이밍 규칙

|타입|규칙|예시|
|---|---|---|
|스태틱 메시|SM_에셋명_파트명|SM_table_top|
|콜리전|UCX_에셋명|UCX_table|
|LOD|SM_에셋명_LOD0|SM_table_LOD0|

---

## 메모 / 트러블슈팅 기록

|날짜|문제|해결 방법|
|---|---|---|
|-|Plasticity OBJ 임포트 시 10배 스케일|임포트 Scale 0.1 설정|
|-|베벨 비대칭|Ctrl+A Apply Scale 누락|
|-|노멀 깨짐|Reset Vectors 후 Mark Sharp 재설정|
|-|||
---
title: (컴피 노드 사전) 자체 노드 KOO Naming Save
---

날짜 : 2026-04-20
링크: 자작 커스텀 노드 (ComfyUI-KOO-texture-naming)

## KOO Naming & Save 노드란?

워크플로우 안에 Save Image 노드가 여러 개 있을 때, 파일명을 한 곳에서 통합 관리하는 자작 커스텀 노드 팩.
에셋 이름이나 버전을 바꿀 때 Naming 노드 하나만 수정하면 모든 Save 노드에 반영된다.

## 한 줄 요약
> PBR 맵 파일명을 한 곳에서 자동 생성하고, 카운터 없이 깔끔하게 저장하는 노드 팩.

### 포함된 노드 종류

| 노드                     | 출력                                                           | 용도                       |
| ---------------------- | ------------------------------------------------------------ | ------------------------ |
| KOO Naming - PBR Full  | normal, roughness, metalness, height, basecolor, opacity     | PBR 풀세트 (6개)             |
| KOO Naming - PBR Basic | normal, roughness, basecolor                                 | PBR 기본 (3개)              |
| KOO Naming - PBR + AO  | normal, roughness, metalness, height, basecolor, opacity, ao | PBR + AO (7개)            |
| KOO Naming - Render    | color, depth, ao, shadow                                     | 렌더 패스 (4개)               |
| KOO Naming - Mask      | mask, invert_mask                                            | 마스크 (2개)                 |
| KOO Naming - Custom    | out_1 ~ out_8                                                | 직접 정의 (최대 8개)            |
| KOO Save Image         | —                                                            | STRING 파일명 입력, 카운터 없이 저장 |

---
## 노드가 하는 일

### Naming 노드
포맷 문자열 `{prefix}_{name}_{part}_{ver}_{map}` 에 입력값을 치환하여 각 맵별 파일명 STRING을 자동 생성한다.

입력 예시:
- prefix: `TEX`, name: `Delphinium`, part: `Leaf`, ver: `v1`

출력 예시:
- `TEX_Delphinium_Leaf_v1_Normal`
- `TEX_Delphinium_Leaf_v1_Roughness`
- `TEX_Delphinium_Leaf_v1_BaseColor`

포맷 문자열을 바꾸면 네이밍 구조 자체를 변경할 수 있다:
- `{name}_{map}` → `Delphinium_Normal`
- `{prefix}_{name}_{part}_{detail}_{ver}_{map}` → `TEX_A_leaves_front_v1_Normal`

비어있는 변수는 자동 생략되어 `__` 같은 이중 구분자가 남지 않는다.

### KOO Save Image
기본 Save Image 노드와 다른 점:
- filename을 STRING 입력 슬롯으로 받음 → Naming 노드와 직접 연결 가능
- 카운터(`_00001_`) 없이 깔끔한 파일명으로 저장
- 덮어쓰기 on/off 선택 가능
- subfolder 지정으로 output 안에 하위 폴더 정리 가능
- png, jpg, webp 포맷 선택

### 이 노드가 없을 때 (문제 상황)

Save Image 노드가 6개 있을 때 에셋 이름이 바뀌면 6개 노드의 filename_prefix를 하나씩 전부 수동 수정해야 한다. 실수로 하나를 빠뜨리면 파일명이 뒤섞인다.

---

## 사용 방법 및 필수 조건

#### 사용 방법
1. 노드 추가에서 "KOO" 검색
2. 용도에 맞는 Naming 노드 선택 (예: KOO Naming - PBR Full)
3. prefix, name, part, ver 입력
4. KOO Save Image 노드 추가
5. Naming 노드의 각 출력(normal, roughness 등) → KOO Save Image의 filename 입력에 연결
6. 이미지 소스 → KOO Save Image의 images 입력에 연결

#### 필수 조건
- ComfyUI GitHub 클론 설치 버전
- `custom_nodes/ComfyUI-KOO-texture-naming/` 폴더에 `__init__.py` 배치
- ComfyUI 재시작

## 참고

- 버전: v3.1.0
- 제작자: KOO
- 카테고리: KOO/naming
- 상세 제작 가이드: `ComfyUI 커스텀 노드 제작 인스트럭션.md`

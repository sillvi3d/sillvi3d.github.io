---
title: Mesh 생성 AI 워크플로우
---

날짜 : 2026-04-22

## 한 줄 요약

레퍼런스 → 이미지 준비 → 3D 생성 → Blender 후처리 → 언리얼 임포트 → 씬 셋팅. 블럭아웃 먼저, 라이팅 먼저, 프랍은 마지막.

---

## 전체 파이프라인

| 단계  | 작업         | 도구                              | 시간 목표   |
| --- | ---------- | ------------------------------- | ------- |
| 1   | 레퍼런스 수집    | Pinterest / ArtStation          | 10~15분  |
| 2   | 인풋 이미지 준비  | remove.bg / Photoshop / ComfyUI | 15~30분  |
| 3   | 3D 생성      | Hunyuan3D / Tripo3D / Meshy     | 20~40분  |
| 4   | 메시 후처리     | Blender                         | 30분~1시간 |
| 5   | 언리얼 임포트    | Unreal Engine 5                 | 10~20분  |
| 6   | 씬 배치 & 라이팅 | Unreal — Lumen / HDRI           | 30분~1시간 |

> ⚠️ 시간 초과 시 그 상태로 스크린샷 찍고 다음 씬으로 넘어갈 것. 완성이 목표가 아니라 반복 횟수가 목표.

---

## 인풋 이미지 준비

### 배경 제거 도구

- **remove.bg** — 빠른 배경 제거, 단순 오브젝트에 적합
- **Photoshop AI 제거** — 복잡한 오브젝트, 엣지 처리 우수
- **직접 촬영** — 흰 배경 + 자연광, 그림자 최소화

### 최적 이미지 조건

|항목|좋은 예|피해야 할 것|
|---|---|---|
|배경|순수 흰색 또는 단색 회색|복잡한 배경, 그라데이션|
|오브젝트 위치|프레임 중앙, 여백 10~15%|화면 끝에 걸리거나 잘린 것|
|촬영 각도|위에서 15~30도 내려다보기|완전 정면 (측면 정보 손실)|
|그림자|없거나 최소화|강한 그림자 (형태 왜곡)|
|해상도|최소 1024×1024, 권장 2048|512 이하 (디테일 손실)|
|라이팅|균일한 디퓨즈, 자연광|강한 직사광, 과노출|

### 삼면도 (멀티뷰) 인풋

ComfyUI에서 삼면도 생성 시 프롬프트:

```
"orthographic reference sheet, front view, side view, back view,
[오브젝트 묘사],
white background, flat diffuse lighting, no shadows,
technical reference, game asset prop"

네거티브:
"perspective distortion, shadow, gradient, depth of field,
blurry, stylized, cartoon, anime, 3D render"
```

> 💡 삼면도 생성 후 각 뷰를 크롭 → 3D AI 멀티뷰 인풋으로 사용

---

## 텍스트 프롬프트 작성 가이드

### 플랫폼별 스타일

|플랫폼|권장 스타일|언어|길이|특이사항|
|---|---|---|---|---|
|Hunyuan3D|자연어 + 핵심 키워드 혼합|영어 권장|40~70 단어|심플할수록 안정적|
|Tripo3D|자연어 중심, 상세 묘사 가능|영어|50~80 단어|자연어 이해 강함|
|Meshy|구조화된 태그 나열|영어|30~60 단어|태그 스타일 최적화|

> 💡 프롬프트 스윗스팟은 50~80 단어. 너무 길면 후반 키워드가 무시됨.

### 기본 프롬프트 공식

```
[오브젝트명] + [소재/텍스처] + [상태/연식] + [스타일] + [배경/기술조건]

예시:
"ancient stone wall module, mossy granite, weathered and cracked,
photorealistic, isolated on white background, game asset, single object"
```

### 실사 강조 태그

**Positive (반드시 포함)**

- `photorealistic`, `hyperdetailed`, `physically based material`
- `RAW photo`, `8k uhd`, `ultra sharp`
- `Nikon D850`, `50mm lens` — 카메라 명시 시 실사 느낌 강화
- `single object`, `isolated` — 배경 오염 방지

**Negative (스타일라이즈드 방지)**

- `cartoon, anime, stylized, painterly, illustration`
- `cel shading, toon, low poly, plastic, toy`
- `3D render, CGI, digital art`

---

## 오브젝트별 프롬프트 키워드

|오브젝트|핵심 키워드|소재 키워드|프롬프트 예시|
|---|---|---|---|
|자연석 / 바위|rock, boulder, natural formation|granite, basalt, mossy, weathered|`"weathered granite boulder, mossy surface, rough texture, photorealistic, white background, game asset"`|
|식물 / 나무|plant, tree, shrub, vegetation|bark texture, subsurface scattering, translucent leaves|`"old oak tree, detailed bark texture, dense foliage, photorealistic, isolated, subsurface scattering on leaves"`|
|돌담 / 석벽 모듈|stone wall, modular, tiling, seamless|limestone, mortar, aged, worn|`"modular stone wall segment, limestone blocks, worn mortar, photorealistic, game prop, tiling"`|
|성벽 모듈|castle wall, battlement, fortification|medieval, moss, battle-worn, cracked|`"medieval castle wall module, stone battlements, moss-covered, battle-worn, photorealistic, game asset"`|
|일상 프랍 (목재)|crate, barrel, furniture|oak, pine, worn wood, aged|`"old wooden crate, worn oak planks, metal corner brackets, aged, photorealistic, white background"`|
|일상 프랍 (금속)|iron, steel, industrial, chain|rust, oxidized, scratched, dented|`"rusty iron chain, heavily oxidized, thick links, photorealistic, isolated, physically based material"`|

> 💡 식물/자연물에는 `subsurface scattering` 키워드가 실사감에 특히 효과적 💡 모듈형 오브젝트(벽, 바닥)에는 `modular`, `tiling`, `seamless` 추가

---

## 3D AI 생성 실전 팁

### 반복 생성 전략

- 같은 오브젝트 최소 3~4회 생성 후 베스트 픽 선정
- Hunyuan 20회 활용법 : 같은 오브젝트 4~5회 + 다른 오브젝트 4~5회
- 각도 약간 다른 레퍼런스 이미지로 여러 번 시도

### 결과 품질 체크 기준

- [ ] 큰 구멍(hole) 없는지 — Blender에서 사전 확인
- [ ] 뒤집힌 노멀(inverted normals) 없는지
- [ ] 텍스처 해상도 — 최소 1K, 권장 2K
- [ ] 폴리곤 수 — 환경 프랍 기준 5K~30K

### Blender 후처리 체크리스트

- [ ] Auto Smooth 적용 — 딱딱한 로우폴리 느낌 완화
- [ ] Decimate Modifier — 과도한 폴리곤 수 감축
- [ ] UV 언래핑 확인 — AI 생성 텍스처 UV 깨짐 체크
- [ ] 스케일 정규화 — Apply Scale → 언리얼 단위계 맞춤

---

## 언리얼 임포트 & 씬 셋팅

### 임포트 설정

- Static Mesh로 임포트 (캐릭터 아니면 Skeletal Mesh 불필요)
- Auto Generate Collision — 환경 프랍은 체크
- Import Textures — GLB는 자동 내장, FBX는 별도 임포트
- Nanite 활성화 — 고폴리 디테일 메시에 적용 (UE5)

### 씬 셋팅 순서 (반드시 지킬 것)

1. 박스/모듈로 공간 구조만 잡기 (프랍 없음)
2. HDRI + Directional Light로 기본 라이팅 세팅
3. 카메라 앵글 고정 후 그 안에서만 드레싱
4. AI 생성 프랍 배치 — 카메라에 보이는 것만

> 💡 카메라 앵글 없이 씬 전체 채우는 건 시간 낭비. 뷰 고정 먼저.

---

## 파일 폴더 구조 템플릿

```
Content/
├── _Project/
│   ├── Maps/
│   ├── Meshes/
│   │   ├── Blockout/
│   │   ├── Props_Nature/          ← 자연물/식물
│   │   ├── Props_Architecture/    ← 벽/모듈
│   │   └── Props_Objects/         ← 일반 프랍
│   ├── Materials/
│   │   └── MI_/                   ← Material Instance
│   ├── Textures/
│   └── Lighting/
├── _AI_Assets/
│   ├── Raw/                       ← AI 원본 아웃풋
│   └── Processed/                 ← Blender 후처리 완료
└── ThirdParty/                    ← 마켓플레이스 등
```

> 💡 `_AI_Assets/Raw` 폴더에 원본 보관 → 후처리 실패 시 재작업 용이
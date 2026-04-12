---
title: Lady Fern
---

날짜 : 2026-04-11 
링크: https://en.wikipedia.org/wiki/Athyrium_filix-femina

## 한 줄 요약

중심부에서 방사형으로 뻗어나오는 밝은 라임 그린의 섬세한 깃털형 엽상체(frond)가 낮게 펼쳐지며 바닥을 덮는 지피형 양치식물.

## 식물 기본 정보

- 한국명 : 아씨고사리 (넓은 의미로 '고사리류')
- 영문명 : Lady Fern
- 학명 (Botanical name) : Athyrium filix-femina
- 분류 : 양치식물 (Pteridophyte) / 지피형 초화류
- 원산지 : 북반구 온대 전역 (유럽, 북미, 동아시아)

## 사이즈 레퍼런스

| 항목              | 최솟값  | 일반값   | 최댓값   | 비고                           |
| --------------- | ---- | ----- | ----- | ---------------------------- |
| 전체 높이           | 30cm | 60cm  | 90cm  | 환경·수분에 따라 편차 큼               |
| 전체 폭 (수관 폭)     | 50cm | 90cm  | 130cm | 높이보다 폭이 넓은 편                 |
| Frond(엽상체) 길이   | 30cm | 60cm  | 100cm | 엽병+엽축 합산                     |
| Pinnae(소엽) 길이   | 4cm  | 8cm   | 14cm  | frond 중단부가 가장 길고 끝으로 갈수록 짧아짐 |
| Pinnule(소소엽) 길이 | 5mm  | 10mm  | 18mm  | 잎 최소단위                       |
| Pinnule(소소엽) 너비 | 2mm  | 5mm   | 8mm   |                              |
| Trunk(근경) 지름    | —    | 1–2cm | —     | 지상 노출 거의 없음                  |
| 엽병(petiole) 길이  | 10cm | 25cm  | 40cm  | frond 전체 길이의 약 1/3           |
| 엽병(petiole) 지름  | 2mm  | 4mm   | 6mm   |                              |
**SpeedTree 세팅 시 기준값 (미터 단위):**
Trunk Length  →  0.01–0.02 m
Frond Length  →  0.6 m
Pinna Length  →  0.08 m
Pinnule Size  →  0.01 m

## 비주얼 특징

### 전체 실루엣

중심의 근경(根莖, rhizome)에서 여러 개의 엽상체(frond)가 방사형으로 펼쳐진다. 전체 형태는 낮고 넓은 분수형(fountain shape) — 높이 약 40–90cm, 폭 60–120cm. 중심부는 밀도가 높고 외곽으로 갈수록 엽상체가 아치형으로 처지며 지면에 가깝게 퍼진다. 수형 자체에 수직성보다 수평·방사성이 강하며, 바닥 그라운드커버로 자연스럽게 읽힌다.

### 줄기 · 가지

- 엽병(petiole, 잎자루): 중심에서 곧게 서다가 중단부터 아치형으로 휘어짐. 길이 20–40cm, 지름 3–5mm로 매우 가늘고 섬세함. 색상: 연두~황록(lime-green), 광택은 거의 없고 매트(matte)에 가까움. 표면에 작은 비늘(scale) 형태의 구조가 있어 미세한 질감이 있음.
- 엽축(rachis, 중심축): 엽병에서 이어지는 주맥. 동일한 라임 그린 색상. 분기 패턴: 좌우 교호(交互) 배열, 거의 대칭적으로 소엽(pinnae)이 붙음.

### 잎

- 구조: 2회 우상복엽(bipinnate) — frond → pinnae → pinnule 3단계 분절.
- 소엽(pinnae): 길이 5–12cm, 끝이 뾰족한 피침형(lanceolate). 역시 좌우 교호 배열, 간격이 일정하고 규칙적.
- 소소엽(pinnule): pinnae에서 다시 갈라진 최소 단위 잎. 끝에 톱니(serration) 있음. 크기: 길이 5–12mm, 너비 3–6mm.
- 색상: 전체적으로 밝은 라임 그린(lime green) — RGB 기준 약 (140, 200, 60) 영역. 광택: 거의 없음, 잎 표면이 매트하여 빛 반사보다 빛 투과(backlighting)가 두드러짐. 역광 시 잎맥이 실루엣처럼 비치는 반투명(translucency) 효과가 핵심 비주얼 포인트.
- 엽맥: 소소엽 수준에서 세밀한 평행 측맥이 육안으로 확인 가능, 텍스처 제작 시 normal map에 반영 필요.
- 밀도: 엽상체 하나에 pinnae 20–35쌍 이상, 전체적으로 매우 조밀하고 레이스 같은 인상.

### 꽃 · 열매 (optional)

양치식물이므로 꽃과 종자 없음. 생식은 포자(spore)로 이루어짐.

- 포자낭군(sorus): 성숙한 개체의 pinnule 뒷면에 타원형 또는 말굽형 갈색 점 형태로 배열. 주로 여름~초가을에 나타나며, 뒷면이기 때문에 정면에서는 잘 보이지 않음. 게임 에셋 수준에서는 텍스처 opacity mask에 선택적으로 표현 가능.

---

## SpeedTree 제작 플랜

### 노드 트리 구조

고사리는 Trunk(줄기)가 없는 대신 근경(rhizome)에서 엽상체(frond)가 직접 방사한다. SpeedTree의 계층 구조를 다음과 같이 매핑한다:

```
[Root / Trunk 대체]  ← 극도로 짧고 굵은 Trunk 제너레이터로 근경(rhizome) 표현
  └─ Frond Generator (Branch Lv1)   ← 엽상체 전체 (엽병 + 엽축)
       └─ Pinna Generator (Branch Lv2)  ← 각 소엽(pinnae) 좌우 배열
            └─ Pinnule Leaf Generator (Leaf)  ← 최소 잎 단위, 커스텀 메시 or 빌보드
```

> 전통적 Trunk → Branch 계층이 아닌, Trunk(근경) → Branch(frond) → Branch(pinna) → Leaf(pinnule) 구조임에 주의.

### 핵심 파라미터

|제너레이터|탭|파라미터명|설정 방향|
|---|---|---|---|
|Trunk (근경)|Generation|Length|0.03–0.06 (거의 땅속에 묻힌 느낌)|
|Trunk (근경)|Generation|Radius|0.04–0.08 (굵고 짧게)|
|Frond (Branch Lv1)|Generation|Count|12–20 (방사형 밀도)|
|Frond (Branch Lv1)|Generation|Length|0.5–0.9 (엽상체 전체 길이)|
|Frond (Branch Lv1)|Angles|Planar Angle|25–40° (지면 대비 낮게 펼치기)|
|Frond (Branch Lv1)|Angles|Gravity|+0.4–0.6 (끝부분 처짐 — 아치형 구현 핵심)|
|Frond (Branch Lv1)|Shape|Profile|S자형 커브 — 중단에서 처지기 시작|
|Pinna (Branch Lv2)|Generation|Count|20–35 쌍 (교호 배열)|
|Pinna (Branch Lv2)|Generation|Length|0.08–0.15|
|Pinna (Branch Lv2)|Angles|Spread Angle|70–85° (frond 축에서 거의 직각으로 펼침)|
|Pinna (Branch Lv2)|Angles|Planar Angle|180° Alternate (좌우 교호 배열)|
|Pinnule Leaf|Generation|Size|0.012–0.025 (매우 작은 낱잎)|
|Pinnule Leaf|Generation|Count|8–16 per pinna|
|Pinnule Leaf|Angles|Spread|60–75°|

### 텍스처 · 머티리얼

필요한 텍스처 맵:

1. **Pinnule Albedo (Base Color)** — 라임 그린 (#8CC83C 계열), 잎맥은 밝은 연두로 미세 표현. Substance Designer에서 'Leaf Veins' 노드를 활용해 엽맥 패턴 생성 권장.
2. **Opacity Mask** — 톱니형 pinnule 실루엣 컷아웃. 알파 채널에 저장. 포자낭군(sorus) 표현 시 뒷면 Opacity에 갈색 점 패턴 추가 가능.
3. **Normal Map** — 잎 표면의 평행 측맥 미세 요철. 강도는 낮게(0.3–0.5 수준).
4. **Translucency / Subsurface** — UE5 Two-Sided Foliage 셰이더에서 Translucency 값 활성화. 역광 시 잎이 반투명하게 빛나는 효과가 이 식물의 핵심 비주얼 — 반드시 적용.
5. **Roughness** — 전체적으로 높게 (0.7–0.9), 광택 없는 매트 질감.

UE5 머티리얼 슬롯: SpeedTree 익스포트 기준 `Branch`, `Leaf` 2개 슬롯이면 충분.

### Wind 설정 포인트

고사리는 Trunk가 없으므로 기존 나무 Wind 세팅과 구조가 다름:

- **Frond(Branch Lv1) Wind** : Primary Wind(1차 바람)를 적용. 엽병 전체가 좌우로 느리게 흔들리는 저주파 모션. → SpeedTree Wind 탭 > Branch Wind Strength: 0.3–0.5, Frequency: 낮게.
- **Pinna(Branch Lv2) Wind** : Secondary Wind(2차 바람). 소엽이 frond와 독립적으로 살짝 떨리는 느낌. → Branch Wind Strength: 0.15–0.25.
- **Pinnule Leaf Wind** : Leaf Flutter(잎 떨림). 바람에 pinnule이 미세하게 퍼덕이는 고주파 모션. → Leaf Wind Strength: 0.2–0.35, Turbulence: 0.3 내외.
- UE5 SpeedTree Wind 컴포넌트에서 Wind Speed를 낮게 설정(0.1–0.3) — 고사리는 폭풍보다 미풍에 반응하는 식물.

### LOD 전략

|LOD 단계|거리 기준|폴리곤 예산|변경 사항|
|---|---|---|---|
|LOD 0|0–5m|8,000–15,000 tri|풀 해상도, pinnule 낱잎 개별 렌더|
|LOD 1|5–15m|3,000–5,000 tri|Pinnule Leaf 수 50% 감소, pinna 수 유지|
|LOD 2|15–30m|800–1,500 tri|Pinna를 Billboard 1장으로 병합, Frond는 단순 판형|
|LOD 3|30m+|Billboard|전체를 2D Billboard 1–2장으로 대체|

VRAM 절약 팁:

- Pinnule 텍스처는 Atlas(아틀라스)로 묶어 1장의 2048×2048로 처리. 낱잎별 개별 텍스처 금지.
- LOD 2 이상에서는 Opacity Mask 해상도를 512로 다운샘플.
- 듀얼 GPU 환경(VRAM 8GB×2)에서 SpeedTree 뷰포트 렌더는 단일 GPU만 사용되므로, LOD 0 미리보기 시 텍스처 스트리밍 방식(Mipmap) 확인 권장.

---

## 제작 난이도

**중급 (입문~중급 경계)**

이유:

- Trunk 없는 구조 때문에 일반 나무 제작 워크플로우와 계층 설계가 달라 초반 혼란 가능.
- Pinnule 수가 많아 폴리곤 · Draw Call 관리가 필요하고, LOD 설계가 품질에 크게 영향.
- 단, 형태 자체는 좌우 대칭 · 규칙적 반복 구조여서 파라미터 패턴을 한번 잡으면 반복 적용이 쉬움.
- 텍스처는 Translucency 처리만 주의하면 비교적 심플.

## 참고

- 유사 식생 레퍼런스: Dryopteris filix-mas (수고사리), Matteuccia struthiopteris (타조고사리 — 더 수직적 실루엣)
- 관련 튜토리얼 타임코드: 재생목록 내 "Leaf / Frond 생성" 관련 영상, Branch Lv2 교호 배열 세팅 섹션 참고
- VRAM · 폴리곤 절약 팁: Pinnule은 메시 대신 Planar Billboard(단면 판) 사용 시 tri 수 60–70% 절감 가능. 단, 근거리(LOD 0)에서 두께감 없어 보일 수 있으므로 LOD 1부터 적용 권장.
---
title: (방법론) Speedtree 파일관리규약
---

날짜 : 2025-04-11 
버전: 1.3

## 최상위 폴더 네이밍 규칙

```
[종류명]

예시)
fern
oak
pine_scots
ivy
```

**규칙 근거**

- 식생 폴더는 종류가 핵심 식별자. 날짜는 의미 없음
- 소문자 영어, 띄어쓰기 대신 언더바
- 버전/날짜 관리는 내부 `4_render` 에서 처리

---

## 폴더 구조

```
fern/
├── 0_ref/
│   └── fern.purㅊ
│
├── 1_textures/
│   ├── raw/                  ← 다운받은 소스 완전 원본 (수정 금지)
│   │   ├── bark/
│   │   └── leaf/
│   └── processed/            ← Substance 등에서 가공한 최종 텍스처
│       ├── bark/
│       └── leaf/
│
├── 2_STP/                    ← .spm 소스 파일
│   ├── SPT_Fern_A.spm
│   ├── SPT_Fern_B.spm
│   └── SPT_Fern_C.spm
│
├── 3_export/
│   ├── mesh/
│   │   ├── SM_Fern_A.fbx
│   │   └── SM_Fern_B.fbx
│   └── texture/              ← 아틀라스 PNG (variation 공유)
│       ├── T_Fern_Leaf_D.png
│       └── T_Fern_Leaf_N.png
│
└── 4_render/
    ├── 260411_v1/
    ├── 260418_v2/
    └── 260501_final/
```

**포인트**

- `1_textures/raw` 는 원본 보존 전용. 수정은 반드시 `processed` 에서
- `3_export/texture` 는 variation 공유 → 메시만 variation별 별도 파일
- variation이 많아지면 `2_STP/` 안을 종별 서브폴더로 분리
- 날짜 추적이 필요한 건 `4_render` 안에서만

---

## 파일 네이밍 규칙

### .spm 소스 파일

```
SPT_[종류]_[변형].spm

예시)
SPT_Fern_A.spm
SPT_Fern_B.spm
SPT_Fern_Dead.spm
```

### 익스포트 메시

```
SM_[종류]_[변형].fbx

예시)
SM_Fern_A.fbx
SM_Fern_B.fbx
```

### 익스포트 텍스처

```
T_[종류]_[파츠]_[채널].png

예시)
T_Fern_Leaf_D.png
T_Fern_Leaf_N.png
T_Fern_Bark_D.png
```

|채널 접미사|내용|비고|
|---|---|---|
|`_D`|Diffuse / Base Color|A채널 = Opacity|
|`_N`|Normal Map|B채널 = Gloss, A채널 = AO|
|`_ORM`|AO(R), Roughness(G), Metallic(B)|UE5 표준 패킹|
|`_SSC`|Subsurface Color|잎 반투명 표현|
|`_H`|Height / Displacement||

### 노드 제너레이터 이름 (SpeedTree 내부)

```
[타입]_[역할]_[번호]

예시)
Tr_main / Br_01 / Lf_ring_01 / Lf_Pt_top_01
```

|약어|타입|설명|
|---|---|---|
|`Tr`|Trunk|줄기|
|`Br`|Branch|가지|
|`Lf`|Leaf|일반 메시 잎|
|`Lf_P`|Leaf Plane|평면 빌보드 잎|
|`Lf_V`|Leaf Volume|볼륨/클러스터 잎|
|`Lf_Pt`|Leaf Point|포인트 배치 잎|
|`Lf_R`|Leaf Ring|원형 배열 잎 레이어|
|`Lf_Sp`|Leaf Spine|척추형 배열 잎|
|`Sp`|Spine|가시/스파인|
|`Fr`|Frond|고사리형 엽상체|
|`Fl`|Flower|꽃|

---

## Variation 관리 방식

|변형 종류|방법|
|---|---|
|형태/배치가 다른 변형|Save As → 새 .spm 파일|
|시드만 다른 경미한 변형|같은 .spm 안에서 시드 번호만 기록|

텍스처는 variation 간 **공유**. 메시만 variation별로 별도 익스포트.

---

## 태그 규칙

`#speedtree` `#식생` `#UE5` `#네이밍`

---

## 변경 이력

|날짜|변경 내용|
|---|---|
|2025-04-11|최초 작성|
|2025-04-11|폴더 구조 개편, Variation 관리 방식 추가|
|2025-04-11|최상위 폴더 날짜 prefix 제거, 날짜를 4_render 하위로 이동|
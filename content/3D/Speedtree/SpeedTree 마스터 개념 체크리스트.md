---
title: SpeedTree 마스터 개념 체크리스트
---

## 노드 트리 구조

- [ ] Root → Trunk → Branch → Leaf 계층 관계 이해
- [ ] 부모 제너레이터 표면에서 자식이 생성되는 원리
- [ ] 제너레이터 추가 / 삭제 / 순서 변경 방법
- [ ] 노드 이름 관리 규칙
- [ ] Seed — 프로시저럴 랜덤성 개념, Variation 관리

---

## Trunk 제너레이터

- [ ] Length / Radius — 줄기 길이와 굵기
- [ ] Segments — 세그먼트 수와 폴리곤의 관계
- [ ] Taper — 줄기가 위로 갈수록 가늘어지는 정도
- [ ] Flares — 뿌리 부분 퍼짐 표현
- [ ] Kink — 줄기 굴곡
- [ ] Noise — 표면 울퉁불퉁함
- [ ] Mesh Welding — 가지와 줄기 연결부 지오메트리 처리

---

## Branch 제너레이터

- [ ] Frequency — 가지 수
- [ ] Angle — 가지가 줄기에서 뻗어나오는 각도
- [ ] Spread — 가지 퍼짐 범위
- [ ] Length — 가지 길이
- [ ] Gravity — 가지에 무게감 부여
- [ ] Flexibility — 가지 유연성
- [ ] Bifurcation — Y자 분기
- [ ] Branch Level 2 이상 계층 추가
- [ ] 파라미터 상속 — 부모 제너레이터 값이 자식에 미치는 영향

---

## Leaf 제너레이터

### 타입

- [ ] Plane — 평면 빌보드 잎
- [ ] Frond — 스파인 기반 엽상체 (고사리, 잔디)
- [ ] Volume / Cluster — 잎 덩어리 표현
- [ ] Point — 특정 위치에 잎 1개씩 배치
- [ ] Ring — 원형 배열
- [ ] Mesh — 외부 메시를 잎으로 사용

### 분포 제어

- [ ] Distribution — 잎이 가지 어디에 배치될지
- [ ] Frequency / Density — 잎 수
- [ ] Size / Size Variance — 잎 크기와 크기 변화량
- [ ] Gravity — 잎 처짐
- [ ] Noise — 잎 방향 불규칙성

### Frond 전용

- [ ] Frond count — 평면 장 수 (2 = 십자)
- [ ] Frond rotation — 장 사이 각도
- [ ] Frond width — 평면 폭

---

## Spine / Force

- [ ] Spine 제너레이터 — 가시 분포와 방향 제어
- [ ] Force 종류 — Gravity, Directional, Point
- [ ] Attractor — 특정 점으로 가지를 끌어당기는 방식
- [ ] Force로 비대칭 형태 만들기
- [ ] Attractor로 구조물을 감싸는 뿌리/덩굴 표현

---

## 텍스처 & 머티리얼

### 채널 패킹 구조

- [ ] `_D` 파일 — RGB = Diffuse, A = Opacity
- [ ] `_N` 파일 — RG = Normal, B = Gloss, A = AO
- [ ] `_ORM` — R = AO, G = Roughness, B = Metallic
- [ ] `_SSC` — Subsurface Color (잎 반투명)
- [ ] `_H` — Height / Displacement

### 머티리얼 슬롯

- [ ] Color / Diffuse 슬롯
- [ ] Opacity 슬롯 — Alpha Clip vs Alpha Blend 차이
- [ ] Normal 슬롯
- [ ] Gloss / Roughness 슬롯
- [ ] Subsurface 슬롯
- [ ] AO 슬롯
- [ ] Height 슬롯
- [ ] Custom 슬롯 (Emissive 등 커스텀 채널)
- [ ] Two-sided 설정 + Back 파라미터

### 아틀라스

- [ ] 아틀라스 개념 — 여러 텍스처를 하나에 패킹
- [ ] Non-wrapping / Everything 모드 차이
- [ ] Allow V wrapping — 줄기 타일링 보존
- [ ] Allow separate atlases
- [ ] Atlas size 설정 (4096 vs 8192)

---

## Compute AO

- [ ] AO(Ambient Occlusion) 개념 — 접힌 부위 음영
- [ ] SpeedTree 내 AO 계산 실행 방법
- [ ] AO 강도 조정

---

## Wind

- [ ] Wind 시스템 레이어 구조 — Global / Branch / Leaf Ripple
- [ ] Strength — 바람 세기
- [ ] Turbulence — 바람 불규칙성
- [ ] Responsiveness — 식생의 반응 속도
- [ ] 식생 종류별 Wind 세팅 차이 (나무 vs 풀꽃 vs 고사리)
- [ ] UE5에서 SpeedTree Wind 동작 확인

---

## LOD

- [ ] LOD 개념 — 거리에 따른 폴리곤 감소
- [ ] LOD 슬라이더로 각 단계 확인
- [ ] 세그먼트 자동 감소 원리
- [ ] Branch / Leaf Frequency의 LOD별 감소
- [ ] Billboard LOD — 원거리 평면 렌더
    - [ ] Faces 수 설정
    - [ ] Top-down 포함 여부
- [ ] Smooth LOD vs 즉각 전환

---

## 커스텀 메시 임포트

- [ ] Mesh 타입 제너레이터 개념
- [ ] Blender / 외부 툴에서 FBX 제작 후 SpeedTree 임포트
- [ ] 임포트 메시 피벗 설정
- [ ] 식생과 커스텀 메시 결합 (수술, 열매 등)

---

## Export

### Export To Game

- [ ] UE5 프리셋 선택 방법
- [ ] LOD 옵션 — All LODs / LODs + billboard
- [ ] Atlas 옵션 — Non-wrapping 설정
- [ ] Textures 옵션 — Format, Atlas size
- [ ] Lightmap UVs 포함 여부

### Export Mesh

- [ ] Group By 옵션 — Hierarchy / Material / Geometry type
- [ ] Transform — Swap YZ, Convert to unit
- [ ] Include 옵션 — Vertex blends, Leaf references
- [ ] Export Mesh vs Export To Game 용도 차이

---

## UE5 연결

- [ ] .st / .fbx UE5 임포트 방법
- [ ] 머티리얼 채널 분리 연결 — `_N` B채널 → Roughness (1-x 처리)
- [ ] Two Sided 머티리얼 설정
- [ ] Foliage Type 설정
- [ ] Foliage Tool로 씬 배치
- [ ] Wind 동작 확인
- [ ] LOD 전환 거리 설정

---

## 식생 유형별 설계 지식

### 실사 풀꽃

- [ ] 꽃잎 Ring 배치 구조
- [ ] 겹꽃잎 크기 그라디언트
- [ ] 수술 Point 배치 or 커스텀 메시

### 실사 활엽수

- [ ] 수종별 Branch 계층 구조 특성
- [ ] Bark 텍스처 V wrapping
- [ ] 잎 군집감 — Volume + Plane 혼합

### 실사 침엽수

- [ ] 침엽 Frond vs 커스텀 메시 선택 기준
- [ ] 침엽 밀도와 배치 특성

### 고사리

- [ ] Frond 엽상체 + 2차 소엽 구조
- [ ] 십자 플레인 줄기

### 덩굴 (아이비)

- [ ] 긴 Trunk 기반 구조
- [ ] Force로 늘어지는 형태 제어

### 선인장

- [ ] 다육질 Trunk 형태
- [ ] Spine 제너레이터 가시 분포

### 판타지 식생

- [ ] 비현실 색감 텍스처
- [ ] Emissive 채널 활용
- [ ] 과장된 형태 설계 원칙

### 뿌리 (구조물 감싸기)

- [ ] Attractor 기반 방향 제어
- [ ] 구조물 형태에 맞는 Force 조합
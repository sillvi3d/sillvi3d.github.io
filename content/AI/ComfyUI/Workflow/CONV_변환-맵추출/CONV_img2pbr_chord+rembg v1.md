---
title: CONV_img2pbr_chord+rembg v1
---

날짜 : 2026-04-18

## 한 줄 요약

실사 사진에서 배경 제거된 PNG + PBR 맵(Normal, Height, Roughness, Metalness)을 한 번에 추출하는 워크플로우. SpeedTree 텍스처 제작용.

## 기본 정보

- 이름: CONV_img2pbr_chord+rembg_v1
- 카테고리: CONV (변환/맵 추출)
- 날짜: 2026-04-18

## 입출력

- 입력: 이미지 (RGB, 자동으로 1024x1024 리사이즈됨)
- 출력: Basecolor PNG (배경 제거) / Normal / Height / Roughness / Metalness / Opacity Map (선택)

## 사용 모델

- 메인: chord_v1.safetensors (comfyui-chord)
- 배경 제거: InspyreNet Rembg (comfyui-inspyrenet-rembg), torchscript_jit: default
- LoRA: 없음
- VAE: 없음

## 노드 흐름

### 1. 이미지 입력 및 리사이즈
- `Load Image` → `ResizeAndPadImage` (1024x1024, padding: white, interpolation: lanczos)

### 2. PBR 맵 추출 (Chord PRB Texture 생성 그룹)
- `Chord - Load Model` (chord_v1.safetensors) → chord_model 출력
- `Chord - Material Estimation` ← chord_model + image 입력 → basecolor / normal / roughness / metalness 출력
- normal → `Save Image` (delphinium_leaf_01_normal)
- normal → `Chord - Normal to Height` → `Save Image` (delphinium_leaf_01_height)
- metalness → `Save Image` (delphinium_leaf_01_metaln...)
- roughness → `Save Image` (delphinium_leaf_01_rough...)

### 3. 배경 제거 (Remove BG 그룹)
- `Inspyrenet Rembg` ← image 입력 → IMAGE + MASK 출력
- `Preview Image`로 결과 확인

### 4. 마스크 후처리 (Mask Edit 그룹)
- `ThresholdMask` (value: 0.80) → `Blur Mask` (blur: 1.0) → `InvertMask`

### 5. 배경 제거된 Basecolor PNG 출력 (수정된 마스크로 PNG 생성 그룹)
- `Join Image with Alpha` ← image + 후처리된 mask → `Save Image` (delphinium_leaf_01_basecolor)

### 6. Opacity Map 출력 (선택, Map(Opacity) Map만 필요할 때 그룹)
- `Convert Mask to Image` → `Save Image`

## 설정값

- 해상도: 1024 x 1024 (ResizeAndPadImage로 강제 리사이즈)
- Steps: - (생성 모델 아님)
- CFG: - (생성 모델 아님)
- Sampler: - (생성 모델 아님)

## 커스텀 노드 목록

- comfyui-chord: Chord - Load Model, Chord - Material Estimation, Chord - Normal to Height
- comfyui-inspyrenet-rembg: Inspyrenet Rembg
- comfypsi_blur_mask: Blur Mask

## 주의사항

- 배경과 대비가 강한 이미지에서 가장 좋은 결과가 나옴
- Rembg 결과가 좋으면 마스크 후처리 없이 바로 Save Image에 연결해도 됨
- filename_prefix를 출력물에 맞게 수동 변경 필요 (현재 delphinium_leaf_01 기준)
- Chord 모델은 최초 실행 시 별도 설치 필요 (엔진 의존성 있음)

## 변경 이력

- v1: 최초 작성 — Chord PBR 추출 + InspyreNet 배경 제거 + 마스크 후처리 통합

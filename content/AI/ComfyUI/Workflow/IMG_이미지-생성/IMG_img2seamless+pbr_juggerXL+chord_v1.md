---
title: IMG_img2seamless+pbr_juggerXL+chord_v1
---

날짜 : 2026.04.10

## 한 줄 요약

입력 이미지를 시임리스 텍스쳐로 변환 후 PBR 맵 5종 추출

## 기본 정보

- 이름: IMG_img2seamless+pbr_juggerXL+chord_v1
- 카테고리: IMG
- 날짜: 2026-04-10

`이미지`

<img src="/AI/ComfyUI/Workflow/IMG_이미지-생성/assets/Pasted_image_20260410094240.png" width="300" />
## 입출력

- 입력: 이미지 (JPEG/PNG)
- 출력: 시임리스 텍스쳐 / Basecolor / Normal / Roughness / Metalness / Height

## 사용 모델

- 메인: juggernautXL_ragnarokBy.safetensors
- PBR 추출: chord_v1.safetensors
- LoRA: 없음
- VAE: 없음

## 설정값

- 해상도: 2048x2048 (Upscale) → 2048x2048 (KSampler)
- Steps: 30
- CFG: 7.0
- Sampler: dpmpp_2m_cfg_pp
- Scheduler: simple
- Denoise: 1.00

## 커스텀 노드

- [comfyui-seamless-tiling](https://github.com/spinagon/ComfyUI-seamless-tiling)
- comfyui-chord

## 워크플로우 구조

```
Load Image
→ Upscale Image (2048x2048)
→ Seamless Tile + Make Circular VAE
→ VAE Encode
→ KSampler
→ VAE Decode
→ Save Image (시임리스 텍스쳐)
→ CHORD Material Estimation
→ Basecolor / Normal / Roughness / Metalness / Height 저장
```

## 주의사항

- Raymnants 모델 못찾아서 JuggernautXL로 대체
- RGBA 이미지 입력 시 오류 발생 → RGB 이미지 사용 권장
- CHORD는 연구 전용 라이선스 (상업적 사용 금지)

## 변경 이력

- v1: 최초 작성
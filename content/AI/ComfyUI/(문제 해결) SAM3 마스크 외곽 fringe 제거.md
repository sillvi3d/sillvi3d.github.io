---
title: (문제 해결) SAM3 마스크 외곽 fringe 제거
---

## 상황

ComfyUI에서 SAM3 Text Segmentation(comfyui-sam3)으로 은행잎 이미지의 마스크를 추출한 뒤, JoinImageWithAlpha로 배경을 제거했을 때 잎 외곽에 초록색 찌꺼기(fringe)가 남는 문제.
![[Pasted image 20260416105454.png]]
![[Pasted image 20260416105502.png|200]]
- 사용 노드: (Down)Load SAM3 Model → SAM3 Text Segmentation → InvertMask → Blur Mask → JoinImageWithAlpha → Save Image
- text_prompt: "plant leaf with stem"
- confidence_threshold: 0.20
- GrowMask(expand: -3)로 수축시켜봤으나, 잎 전체가 깎여서 디테일이 손실됨
![[Pasted image 20260416105519.png|200]]
## 원인

SAM3는 세그멘테이션(영역 분류)에 특화된 모델이라, 마스크 경계가 픽셀 단위로 딱딱하게 잘림. 잎 끝처럼 얇고 복잡한 외곽선에서는 경계 픽셀에 배경색이 섞여 fringe가 발생함. GrowMask로 마스크를 수축시키면 찌꺼기뿐 아니라 잎 본체까지 함께 깎여 근본적 해결이 안 됨.

## 해결

### 방법 1: Blur → ThresholdMask 조합 (빠른 해결, 추가 설치 불필요)

기존 워크플로우에서 Blur Mask 이후에 ThresholdMask 노드(기본 내장)를 추가.

1. `Blur Mask`의 blur 값을 **3~5**로 크게 설정하여 경계를 부드럽게 만듦
2. `ThresholdMask`(threshold: **0.5**)를 연결하여 애매한 경계 픽셀을 제거

흐름:
```
SAM3 Text Segmentation → masks → InvertMask → Blur Mask (blur: 3~5) → ThresholdMask (threshold: 0.5) → JoinImageWithAlpha → Save Image
```

원리: 블러로 경계를 펴준 뒤 threshold로 다시 선명하게 잘라내면, 불확실한 경계 픽셀만 정리되고 본체는 유지됨.

### 방법 2: BiRefNet 사용 (근본적 해결, 커스텀 노드 설치 필요)

**comfyui-BiRefNet** 노드팩을 ComfyUI Manager에서 설치.

흐름:
```
Load Image → BiRefNet → image/mask 출력 → Save Image
```

BiRefNet은 경계 정제(boundary refinement)에 특화된 알파 매팅 모델이라, 잎 같은 복잡한 외곽선에서도 fringe가 거의 발생하지 않음.

## 참고

- SAM3의 `confidence_threshold`를 0.30~0.50으로 올리면 마스크 품질이 개선될 수 있음 (너무 높이면 잎 일부가 잘려나감)
- `text_prompt`를 "ginkgo leaf"처럼 구체적으로 지정하면 세그멘테이션 정밀도가 올라갈 수 있음
- comfyui-impact-pack의 **MaskMorphology** 노드로 erode/dilate를 세밀하게 제어하는 방법도 있음 (ComfyUI Manager에서 설치 가능)

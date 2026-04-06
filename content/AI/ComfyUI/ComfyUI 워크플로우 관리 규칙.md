---
title: ComfyUI 워크플로우 관리 규칙
---

날짜 : 26.04.06
버전: v1
##### 파일 네이밍 규칙

`[카테고리]_[입력]2[출력]_[핵심모델]_v[버전]`

##### 폴더구조

- 카테고리 약어

| 약어     | 분야               |
| ------ | ---------------- |
| `IMG`  | 이미지 생성           |
| `CTL`  | ControlNet/제어    |
| `CHR`  | 인물/얼굴            |
| `VID`  | 비디오              |
| `CONV` | 변환 (맵 추출, 형태 변환) |
| `EDIT` | 이미지 수정/편집        |
| `MESH` | 3D/뎁스            |
| `SEG`  | 세그멘테이션           |
| `AUTO` | 자동화/배치           |
- 입력/출력 약어

| 약어    | 의미                          |
| ----- | --------------------------- |
| `txt` | 텍스트 프롬프트                    |
| `img` | 이미지                         |
| `vid` | 비디오                         |
| `pbr` | PBR 맵 (Normal, Roughness 등) |
| `msk` | 마스크                         |
| `dep` | 뎁스맵                         |
| `3d`  | 3D 메시                       |


- 예시
```
TEX_img2pbr_chord_v1
TEX_txt2img_zturbo_v1
IMG_txt2img_flux_v1
IMG_img2img_sdxl_v1
CHR_img2img_reactor_v1
SEG_img2msk_sam_v1
TD_img2dep_midas_v1
```


##### 부가요소 표기 (필요할 때만)

```
IMG_txt2img_sdxl+L+CN_v1   (LoRA + ControlNet 사용)
TEX_img2pbr_chord+L_v1     (LoRA 사용)
```

|약어|의미|
|---|---|
|`+L`|LoRA|
|`+CN`|ControlNet|
|`+IP`|IP-Adapter|

##### 버전 관리

|표기|의미|
|---|---|
|`v1`|최초 작동 버전|
|`v2`|개선/수정|
|`_test`|실험 중|
|`_final`|완성본|

##### 변경 이력

| 날짜         | 변경 내용 |
| ---------- | ----- |
| 2026-04-06 | 최초 작성 |

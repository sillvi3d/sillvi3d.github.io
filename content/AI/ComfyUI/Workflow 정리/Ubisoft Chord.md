---
title: Ubisoft Chord
---

날짜 : 26.04.05
##### 한 줄 요약
- Input 이미지를 pbr 변환함 (상단 5개)
- Image를 1024로 변환한 뒤 bg 제거한 png와 마스크 추출 (하단 2개)

`이미지`

![[Pasted image 20260405181347.png]]
##### 주요 커스텀 노드/모델/로라

- chord 엔진
	- [관련 문서 - # Ubisoft Open-Sources the CHORD Model and ComfyUI Nodes for End-to-End PBR Material Generation](https://blog.comfy.org/p/ubisoft-open-sources-the-chord-model)
	- 연구 전용 엔진이라 상업용으로는 사용 불가한 것으로 알고 있음 (26.04기준)
- 기타 더 필요한 것은 매니저에서 다운로드
- t2i 워크플로우로 사용하기 위해서 추가로 필요한 것
	- 디퓨전 모델 [z-image-turbo](https://huggingface.co/Comfy-Org/z_image_turbo/tree/main/split_files/diffusion_models)
		- diffuse model 폴더에다가 넣기
		- 12g
	- vae - [Flux.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev/tree/main)
		- models/vae/
		- 동의 누르고 -> gate 모델은 hugging face에서 동의를 눌러야 쓸 수 있음
			![[Pasted image 20260402165637.png]]
		- files로 넘어간 뒤 ae.safetensors 만 다운로드
		- 335mb
	- 텍스트 인코더 - qwen_3_4b 텍스트 인코더
		- models/text_encoders/

##### 흐름

1. 먼저 제공된 [예시 워크플로우](https://github.com/ubisoft/ComfyUI-Chord/blob/main/example_workflows/chord_zimage_turbo_t2i_image_to_material.json)를 다운받아 컴피에서 불러오고 필요한 노드 install
2. 허깅페이스에서 chord 전용 엔진을 다운로드
	- 허깅페이스 토큰 넘버 알아야 함. 계정당 1번 인증
	- 또한 게이트 모델이라 허깅페이스에서 엑세스 동의해야 함.
2. PC에서 별도 폴더에다가 깃 클론한 뒤 내부 내용을 복사
3. comfyui의 경로에 붙여넣기
	- ComfyUI/models/checkpoints/chord_v1.safetensors
4. 나머지는 Comfy manager의 도움을 받아 완성

##### 핵심 설정값

| 항목  | 값   |
| --- | --- |
|     |     |

##### 결과물 · 샘플

![[chord_zimage_turbo_i2i_image_to_material_final.json]]
##### 특이사항
- 만약 1번 딴에서 진행이 안된다면
	- Vram 용량이 꽉 찬 것임
		- 이미지 사이즈나
		- step 줄이기
			![[Pasted image 20260402175754.png]]
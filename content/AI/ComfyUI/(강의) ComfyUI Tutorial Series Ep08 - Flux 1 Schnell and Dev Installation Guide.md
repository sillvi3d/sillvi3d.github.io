---
title: (강의) ComfyUI Tutorial Series Ep08 - Flux 1 Schnell and Dev Installation Guide
---

날짜 : 26.04.13
링크 : [ComfyUI Tutorial Series: Ep08 - Flux 1: Schnell and Dev Installation Guide](https://youtu.be/ImWHS5Ux36E?si=MCZZNC55egBPUWRu)

## 한 줄 요약

- 유튜브 영상에서 Flux 모델의 다양한 버전(Dev, Schnell, fp8, fp16, nf4) 설치, 워크플로우 구성, 성능 비교 및 Lora 적용 방법을 상세히 설명함.

## 핵심 내용

1.  Flux 모델 (Dev, Schnell) 및 버전 (fp8, fp16, nf4)의 특징과 라이선스 정보를 이해함.
2.  ComfyUI에서 Flux 모델 (fp8 버전)의 다운로드 및 설치, 그리고 기본 워크플로우를 구성함.
3.  Flux Guidance 노드 사용, 스타일 적용, 워크플로우 그룹화, 그리고 Lora를 Flux 모델에 적용하는 방법을 학습함.
4.  Dev 버전에서 발생하는 블러 이미지 문제를 해결하기 위한 Sampler 및 Scheduler 설정 변경 방법을 숙지함.
5.  정규 Dev (fp16) 버전과 저사양 VRAM을 위한 NF4 버전 설치, `bitsandbytes` 커스텀 노드 수동 설치 과정을 익힘.
6.  다양한 Flux 모델 버전(fp8, fp16, nf4) 간의 이미지 품질, 속도, VRAM 요구사항을 비교하여 적절한 모델 선택 가이드를 제공함.

## 따라한 것 · 실습

1.  **Flux 모델 개요 및 라이선스 이해**
	-   **Flux 모델 소개**
		-   Black Forest Labs에서 개발한 새로운 모델 패밀리인 Flux 버전 1을 소개함.
		-   고품질 이미지를 생성하지만 빠른 속도를 위해 좋은 컴퓨터를 요구함.
		-   최대 2메가픽셀의 다양한 비율 및 해상도를 지원함.
		-   **세 가지 버전 제공**:
			-   **Pro 버전**: 다운로드 불가, API로만 사용 가능.
			-   **Dev 버전**: 최상의 품질을 제공하지만 더 많은 리소스를 요구함.
				-   라이선스: 비상업적 (non-commercial).
				-   개인적인 해석: 모델 자체는 상업적 사용 불가, 모델로 생성된 이미지는 상업적 사용 가능. 단, Flux와 경쟁하는 새 모델 훈련에 생성된 이미지 사용 불가.
			-   **Schnell 버전**: 가장 빠르지만 Dev 버전에 비해 품질이 낮음.
				-   라이선스: Apache 2.0.
				-   개인적인 해석: 모델과 생성된 이미지 모두 상업적 사용 가능.
		-   **모델 종류 (GitHub 기준)**:
			-   `Flux Dev`: 일반/가장 큰 Dev 버전.
			-   `Flux Schnell`: 가장 작은 버전.
			-   `fp8 (floating point 8)` 버전: 더 작고 간단한 워크플로우를 요구하는 버전으로, Dev 및 Schnell 모두 제공함.
				-   이 영상에서는 주로 fp8 버전을 다룸.
				<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0208.png" width="300" />

2.  **Flux fp8 버전 설치 및 기본 워크플로우 구성**
	-   **모델 파일 다운로드 및 배치**
		-   `Flux Dev (fp8)` 모델 다운로드 (약 17GB).
		-   `Flux Schnell (fp8)` 모델 다운로드 (동일 사이즈).
		-   다운로드한 모델을 ComfyUI 설치 폴더 내 `ComfyUI > models > checkpoints` 폴더에 배치함.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0309.png" width="300" />
	-   **ComfyUI 업데이트**
		-   ComfyUI를 실행함.
		-   `Manager` 버튼 클릭.
		-   `Update All` 선택하여 ComfyUI를 최신 버전으로 업데이트함. (Flux 모델 인식에 필요한 새 노드 추가를 위함)
		-   업데이트 후 ComfyUI 재시작.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0351.png" width="300" />
	-   **예시 워크플로우 로드 및 실행 (빠른 시작)**
		-   Schnell 및 Dev 모델용 예시 이미지를 다운로드함 (이미지 내 워크플로우 포함).
		-   ComfyUI에서 `Load` 버튼 클릭.
		-   다운로드한 이미지 중 Schnell fp8 버전 이미지를 로드함.
		-   로드 후, 모델 목록에서 `flux-schnell-v1-fp8.safetensors` 모델이 선택되었는지 확인 (선택되지 않았다면 수동 선택).
		-   `Queue Prompt` 버튼을 클릭하여 워크플로우를 실행하고 결과 이미지를 확인.
		-   Dev fp8 버전 이미지로 동일하게 로드 및 실행하여 결과를 확인.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0410.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0422.png" width="300" />

3.  **SDXL 워크플로우를 Flux 워크플로우로 변환**
	-   **기본 SDXL 워크플로우 로드**
		-   기존에 사용하던 기본 SDXL 워크플로우를 로드함.
	-   **모델 로드 노드 변경**
		-   `Load Checkpoint` 노드에서 `flux-schnell-v1-fp8.safetensors` 모델을 선택함.
	-   **Empty Latent Image 노드 변경**
		-   기존 `Empty Latent Image` 노드를 삭제.
		-   `Add Node > Latent > Empty Latent Image (SD3)` 노드를 추가함.
		-   새 `Empty Latent Image (SD3)` 노드의 `LATENT` 출력을 `K Sampler`의 `latent_image` 입력에 연결함.
		-   이 노드의 배경색을 보라색으로 변경하여 식별하기 쉽게 함 (`Node Context Menu (우클릭) > Color > purple`).
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0515.png" width="300" />
	-   **프롬프트 노드 변경**
		-   `CLIP Text Encode (Positive)` 노드의 색상을 녹색으로, `CLIP Text Encode (Negative)` 노드의 색상을 빨간색으로 변경.
		-   Flux는 negative prompt를 지원하지 않으므로, `CLIP Text Encode (Negative)` 노드를 삭제하거나 `Collapse`하여 공간을 절약함.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0528.png" width="300" />
	-   **K Sampler 설정 (Schnell fp8)**
		-   `K Sampler` 노드의 설정을 변경함.
			-   `cfg`: `1` (CFG가 1이면 negative prompt를 무시함)
			-   `steps`: `4` (Schnell 버전은 4단계만 필요)
			-   `sampler_name`: `euler`
			-   `scheduler`: `simple`
		-   워크플로우를 실행하여 이미지 생성 테스트. (첫 실행 시 모델 로딩으로 인해 더 오래 걸림. RTX 4090 기준 3~4초 소요)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0600.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0604.png" width="300" />

4.  **Dev fp8 워크플로우 구성 및 Flux Guidance 노드 사용**
	-   **모델 변경**
		-   `Load Checkpoint` 노드에서 `flux-dev-v1-fp8.safetensors` 모델을 선택함.
	-   **K Sampler 설정 (Dev fp8)**
		-   `K Sampler` 노드의 `steps`를 `20` 또는 `30` (기본 20)으로 설정함.
	-   **Flux Guidance 노드 추가**
		-   `Add Node > Sampling > Flux Guidance` 노드를 추가함.
		-   이 노드의 `default value`는 `3.5`임. CFG가 1로 고정된 Flux에서 이미지에 영향을 줄 수 있는 유사 CFG 역할을 함 (Schnell 버전에는 영향을 미치지 않음).
		-   `CLIP Text Encode (Positive)` 노드의 `CONDITIONING` 출력을 `Flux Guidance` 노드의 `condition_in` 입력에 연결.
		-   `Flux Guidance` 노드의 `CONDITIONING` 출력을 `K Sampler` 노드의 `positive` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0702.png" width="300" />
	-   **워크플로우 실행**
		-   워크플로우를 실행하여 이미지 생성 테스트. (첫 실행 시 24초, 두 번째부터 14초 소요. 구형 PC(6GB VRAM)에서는 6분 소요됨)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0716.png" width="300" />
	-   **Flux Guidance 값 테스트**
		-   프롬프트: `a painting of a gnome`
		-   `seed`를 `fixed`로 설정하여 결과를 비교.
		-   `Flux Guidance` 기본값 `3.5`로 실행.
		-   `Flux Guidance` 값을 `3`으로 변경하여 실행하고 이전 결과와 비교. (값이 낮아지면 이미지 품질이 저하될 수 있으나, 때로는 흥미로운 페인팅 효과를 생성함. 1~100 사이 값 사용 가능, 20 이상은 효과 감소)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0744.png" width="300" />

5.  **Flux에 스타일 적용 (Episode 7 노드 필요)**
	-   (전제: Episode 7에서 소개된 추가 노드 및 스타일 설정이 완료되어 있어야 함)
	-   **스타일 셀렉터 노드 추가**
		-   `Add Node > Custom Nodes > ComfyUI_Comfy_Easy_Use > Multiple Style Selector` 노드를 추가함.
	-   **CLIP Text Encode 노드 변경**
		-   기존 `CLIP Text Encode (Positive)` 노드를 `Text Input` 노드로 변환함 (`Node Context Menu (우클릭) > Convert CLIPTextEncode to Text Input`).
	-   **프롬프트 연결 노드 추가**
		-   `Add Node > Custom Nodes > ComfyUI_Comfy_Easy_Use > Easy Positive` 노드를 추가함.
		-   `Add Node > Text > Text Concatenate` 노드를 추가함.
		-   `Easy Positive` 노드의 `POSITIVE` 출력을 `Text Concatenate` 노드의 `text_a` 입력에 연결.
		-   `Multiple Style Selector` 노드의 `STRING` 출력을 `Text Concatenate` 노드의 `text_b` 입력에 연결.
		-   `Text Concatenate` 노드의 `STRING` 출력을 `CLIP Text Encode (Prompt)` 노드 (이전 `CLIP Text Encode (Positive)` 변환 노드)의 `TEXT` 입력에 연결.
	-   **노드 정리 및 실행**
		-   노드들을 `Collapse` 및 재배치하여 워크플로우를 명확하게 정리.
		-   프롬프트를 입력하고 `Multiple Style Selector`에서 `cartoon_cute`와 같은 스타일을 선택.
		-   `seed`를 `fixed`로 설정하고 워크플로우 실행하여 스타일 적용 확인.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0900.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0907.png" width="300" />
	-   **스타일 영향 비교**
		-   프롬프트: `a gnome in a magical forest`
		-   `Multiple Style Selector`에서 `no style`을 선택하고 실행하여 기본 이미지 확인.
		-   동일 `seed`, 동일 프롬프트로 `impressionism painting` 스타일을 선택하고 실행하여 스타일 적용 전후 비교.
		-   다른 스타일(`portrait_cinematic_photography`, `biomechanical_art`)로도 테스트하여 스타일의 영향을 확인. (Flux는 SDXL보다 적은 스타일을 인식할 수 있으나 여전히 이미지에 영향을 미침)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0922.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0932.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___0955.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1004.png" width="300" />

6.  **컴팩트 워크플로우 그룹 생성**
	-   `Save Image` 노드를 제외한 모든 노드를 선택.
	-   `Node Context Menu (우클릭) > Convert to Group Node`를 선택.
	-   그룹 노드 이름을 지정함.
	-   그룹 노드 내부의 `negative prompt`는 Flux에서 사용되지 않으므로 인터페이스에서 숨김.
	-   생성된 그룹 노드를 통해 간소화된 인터페이스로 워크플로우를 사용할 수 있음.
	-   (추가 수정 후 다운로드 가능한 형태로 제공됨을 언급)
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1024.png" width="300" />
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1059.png" width="300" />

7.  **Schnell fp8과 Dev fp8 비교**
	-   **비교 워크플로우 구성**
		-   두 개의 워크플로우 (상단 Schnell, 하단 Dev)를 준비.
		-   두 워크플로우의 `CLIP Text Encode (Positive)` 노드를 `Text Input`으로 변환.
		-   `Add Node > Utils > Primitive` 노드를 추가하거나 `Comfy Easy Use`의 `Easy Positive` 노드를 사용하여 단일 프롬프트를 두 워크플로우에 연결.
		-   `seed`를 `fixed`로 설정하여 비교 일관성을 유지.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1120.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1150.png" width="300" />
	-   **이미지 품질 비교 (다양한 프롬프트)**
		-   `green sphere on a blue cube with a black background in 3D render style` 프롬프트로 테스트. (두 버전 모두 이해하지만 일부 seed에서 블러 현상 발생)
		-   `portrait of a woman` 프롬프트: Dev 버전이 더 사실적인 결과 생성.
		-   `portrait of a Viking in the rain at Golden hour` 프롬프트: Dev 버전이 더 사실적이고 비를 더 잘 표현함 (Schnell 버전은 비를 표현하지 못함).
		-   `a witch holding a sign with text` 프롬프트: Dev 버전이 텍스트를 더 잘 생성함.
		-   `cartoon warrior cat knight` 프롬프트: Dev 버전이 검과 방패를 더 잘 처리함.
		-   Dev 버전은 일반적으로 손과 세부 사항에서 Schnell 버전보다 실수가 적음.
		-   `penguin eating ice cream with a polar bear in the background` 프롬프트: Dev 버전이 아이스크림을 더 잘 표현함 (Schnell 버전은 실패).
		-   `fox and a bunny` 프롬프트: Dev 버전이 더 많은 디테일.
		-   `a crocodile with a wanted poster on the wall, $1,000 reward, crocodile featured on the poster` 프롬프트: Dev 버전이 더 나은 결과.
		-   `stairs to heaven in concept art` 프롬프트: 스타일 차이 확인.
		-   `photo of a hamburger` 프롬프트: 유사한 결과.
		-   `small flag that says free, white like a surrender flag` 프롬프트: 모델이 모든 요소를 잘 통합함.
		-   `Vector style design` 프롬프트: Dev 버전에서 블러 현상 발생 가능성 (해결책은 나중에 설명).
		-   `charming cute cat` 프롬프트: Dev 버전이 매력적인 고양이 생성.
		-   로고 및 프리젠테이션 목업 이미지 생성에서도 Dev 버전이 더 나은 결과.
		-   `oil painting of a king on a throne` 프롬프트: Dev 버전이 약간 더 나은 결과.
		-   **손 처리**: Flux 모델은 다른 모델보다 손을 더 잘 처리하는 경향이 있음.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1205.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1232.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1243.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1255.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1303.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1316.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1324.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1343.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1355.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1407.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1421.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1438.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1456.png" width="300" />

8.  **블러 이미지 해결 (Dev 버전)**
	-   Dev 버전에서 일부 `seed`에서 이미지가 흐릿하게 생성되는 문제가 발생할 수 있음.
	-   **K Sampler 설정 변경**
		-   `K Sampler` 노드의 `sampler_name`을 `dpmpp_2m`으로 변경.
		-   `K Sampler` 노드의 `scheduler`를 `sgm_uniform`으로 변경.
		-   동일 `seed`로 테스트 시 선명한 이미지 생성 확인.
		-   (워크플로우는 Discord를 통해 업데이트될 예정임을 언급)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1537.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1540.png" width="300" />

9.  **정규 Dev (fp16) 버전 설치 및 워크플로우 구성**
	-   최고급 비디오 카드 및 32GB 이상의 시스템 RAM을 가진 사용자에게 권장되는 버전.
	-   **추가 모델 파일 다운로드 및 배치**
		-   **CLIP 모델**: `https://huggingface.co/blackforestlabs/Flux-Dev-1-Official/tree/main` 에서 두 개의 `clip` 모델 다운로드.
			-   다운로드한 파일을 `ComfyUI > models > clip` 폴더에 배치.
		-   **VAE 파일**: `https://huggingface.co/blackforestlabs/Flux-Dev-1-Official/tree/main` 에서 `vae.safetensors` (VAE Safe Tensor) 파일 다운로드.
			-   다운로드한 파일을 `ComfyUI > models > vae` 폴더에 배치.
		-   **UNET (Flux 모델)**: `https://huggingface.co/blackforestlabs/Flux-Dev-1-Official/tree/main` 에서 약 23GB 크기의 `Flux-Dev-1.safetensors` 모델 다운로드.
			-   다운로드한 파일을 `ComfyUI > models > unet` 폴더에 배치.
	-   **예시 워크플로우 로드**
		-   정규 Dev 버전용 예시 이미지를 다운로드 (이미지 내 워크플로우 포함).
		-   ComfyUI에서 `Load` 버튼 클릭 후 해당 이미지 로드.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1710.png" width="300" />
	-   **워크플로우 특징**
		-   fp8 버전과 달리, `Load Checkpoint` 노드 외에 별도로 `Load CLIP Model` 노드가 두 개 사용됨.
		-   `Load VAE` 노드가 분리되어 있음.
		-   `dtype` 변경 옵션 (속도 향상 가능성).
		-   `Basic Guider` 및 `Custom Advanced Sampler` 노드가 사용됨 (일반 `K Sampler` 대신).
		-   `Empty Latent Image`의 `width`와 `height` 조정 기능이 포함됨.
		-   워크플로우가 더 복잡하며, 자동 해상도 조정 기능 포함.
		-   (첫 실행 시 35초, 두 번째부터 18초 소요)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1750.png" width="300" />

10. **정규 Dev (fp16) vs. Dev fp8 비교**
	-   **비교 워크플로우 구성**
		-   두 개의 워크플로우 (좌측 정규 Dev, 우측 Dev fp8)를 준비.
		-   단일 `Easy Positive` 노드를 사용하여 두 워크플로우에 프롬프트 연결.
		-   `seed`를 `fixed`로 설정.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___1850.png" width="300" />
	-   **이미지 품질 비교**
		-   `gnome` 프롬프트: fp8 버전에서 눈 디테일이 약간 떨어지지만 전반적으로 유사하며, 정규 버전이 달 디테일이 더 많음.
		-   `pixaroma book` 프롬프트: 두 버전 모두 텍스트를 정확하게 생성.
		-   `sign on an exotic island` 프롬프트: 작은 차이만 있음.
		-   `burger photo` 프롬프트: 매우 유사한 결과.
		-   **결론**: 대부분의 경우 정규 Dev 버전과 fp8 버전의 결과는 유사함. 정규 버전이 약간 더 나은 디테일을 제공하지만, 워크플로우 복잡도와 생성 시간 증가를 고려할 때 fp8 버전이 더 효율적일 수 있음.

11. **NF4 (Normalized Float 4-bit) 버전 설치 및 구성 (저사양 VRAM용)**
	-   낮은 VRAM을 가진 사용자를 위한 더 빠른 버전 (품질은 약간 낮음).
	-   **NF4 모델 다운로드**
		-   `Flux Schnell nf4` 및 `Flux Dev nf4` 모델을 다운로드.
		-   모델 파일 이름에 `BNB`가 포함된 버전을 다운로드해야 함 (`flux-schnell-v1-nf4-bnb.safetensors`, `flux-dev-v1-nf4-bnb.safetensors`).
		-   다운로드한 파일을 `ComfyUI > models > checkpoints` 폴더에 배치. (fp8 버전보다 작은 약 11GB 크기)
	-   **`bitsandbytes` 커스텀 노드 수동 설치**
		-   이 노드는 ComfyUI `Manager`에서 제공되지 않을 수 있으므로 수동으로 설치.
		-   `ComfyUI` 설치 폴더로 이동.
		-   `custom_nodes` 폴더로 이동.
		-   주소창에 `CMD`를 입력하고 Enter 키를 눌러 명령 프롬프트 창을 엶.
		-   다음 명령어를 입력하여 커스텀 노드를 클론.
			```bash
			git clone https://github.com/lucianopc/ComfyUI-bits-and-bytes-loader
			```
		-   **`bitsandbytes` Python 패키지 설치**
			-   동일한 명령 프롬프트 창에서 다음 명령어를 입력.
				```bash
				pip install bitsandbytes
				```
			-   (Portable ComfyUI에서 설치가 안 될 경우, ComfyUI 설치 폴더 내 `ComfyUI_windows_portable > python > Scripts` 폴더로 이동하여 `CMD`를 연 후 위 명령을 다시 시도)
		-   모든 명령 프롬프트 창을 닫음.
		-   ComfyUI를 실행하여 모든 것이 정상 작동하는지 확인.
		-   ComfyUI `Manager`를 통해 `Update All`을 다시 실행하고 ComfyUI 재시작.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2126.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2138.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2149.png" width="300" />

12. **NF4 워크플로우 구성 및 테스트**
	-   **Schnell nf4 워크플로우**
		-   기존 Schnell fp8 워크플로우를 로드.
		-   `Load Checkpoint` 노드를 삭제.
		-   `Add Node > Loaders > Checkpoint Loader (NF4)` 노드를 추가.
		-   `Checkpoint Loader (NF4)` 노드의 `MODEL` 출력을 `K Sampler`의 `model` 입력에 연결.
		-   `CLIP` 출력을 `CLIP Text Encode (Positive)` 및 (필요하다면) `CLIP Text Encode (Negative)`에 연결.
		-   `VAE` 출력을 `VAE Decode`의 `vae` 입력에 연결.
		-   `Checkpoint Loader (NF4)` 노드에서 `flux-schnell-v1-nf4-bnb.safetensors` 모델을 선택.
		-   워크플로우를 테스트 (첫 실행은 느리지만 이후 RTX 4090 기준 약 3초 소요).
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2242.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2303.png" width="300" />
	-   **Dev nf4 워크플로우**
		-   `Checkpoint Loader (NF4)` 노드에서 `flux-dev-v1-nf4-bnb.safetensors` 모델을 선택.
		-   `K Sampler`의 `steps`를 `20`으로 변경.
		-   `sampler_name`을 `dpmpp_2m`으로, `scheduler`를 `sgm_uniform`으로 변경 (블러 방지).
		-   Dev 버전이므로 `Flux Guidance` 노드를 추가하고 `CLIP Text Encode (Positive)`와 `K Sampler` 사이에 연결.
		-   워크플로우를 테스트.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2338.png" width="300" />

13. **fp8 vs. NF4 비교**
	-   **비교 워크플로우 구성**
		-   두 개의 워크플로우 (좌측 fp8, 우측 nf4)를 준비.
		-   단일 `Easy Positive` 노드를 사용하여 두 워크플로우에 프롬프트 연결.
		-   `seed`를 `fixed`로 설정.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2409.png" width="300" />
	-   **이미지 품질 비교**
		-   일부 프롬프트에서는 차이가 크고, 일부는 미미함.
		-   일반적으로 fp8 버전이 더 많은 디테일을 가짐.
		-   `robot` 이미지: fp8 버전이 눈 주변 디테일과 텍스처가 더 선명.
		-   `burger` 이미지: 텍스처는 거의 동일하나, fp8 버전이 미세하게 더 많은 텍스처.
		-   `cute hamster` 이미지: fp8 버전이 선명도와 디테일에서 더 우수 (nf4는 덜 선명).
		-   `dragon` 프롬프트: 이미지는 유사하나 뿔 모양이 다름.
		-   `pirate face` 이미지: fp8 버전이 눈에 띄게 선명.
		-   `monkey` 이미지: 유사하나 fp8 버전이 나무 텍스처가 약간 더 많음.
		-   `magician bunny` 이미지: fp8 버전의 토끼가 더 선명.
		-   `portrait` 이미지: fp8 버전이 코와 이마에 더 많은 텍스처.
		-   **결론**: 취향에 따라 다르지만, 일반적으로 fp8 버전이 더 높은 디테일과 선명도를 제공함.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2426.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2438.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2443.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2451.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2454.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2457.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2504.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2512.png" width="300" />

14. **Flux에 Lora 적용 (Realism Lora)**
	-   (Dev 버전과 호환되는 Lora 사용 필요. 여기서는 fp8 Dev 버전을 예시로 사용)
	-   **Realism Lora 다운로드 및 배치**
		-   Xlabs에서 출시한 Flux용 Realism Lora (ComfyUI 호환 버전)를 다운로드 (`https://huggingface.co/cchick/Flux-Realism-Lora/blob/main/flux_realism_lora_v1.safetensors`).
		-   다운로드한 Lora 파일을 `ComfyUI > models > loras` 폴더에 배치.
	-   **워크플로우 준비 및 Lora 적용 전 테스트**
		-   Dev fp8 워크플로우를 로드.
		-   `seed`를 `fixed`로 설정.
		-   `refresh` 버튼을 클릭하여 새로 다운로드한 Lora를 인식시킴.
		-   Lora 없이 워크플로우를 실행하여 기본 이미지 확인 (`plastic look`의 비현실적인 이미지 생성).
		-   생성된 이미지를 복사하여 나중에 비교할 수 있도록 옆에 붙여넣음.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2607.png" width="300" />
	-   **Lora 노드 추가 및 연결**
		-   `Add Node > Loaders > Load LoRA` 노드를 추가.
		-   `Load LoRA` 노드를 `Load Checkpoint` 노드와 `CLIP Text Encode` 노드들 사이에 배치.
		-   `Load Checkpoint` 노드의 `MODEL` 출력을 `Load LoRA` 노드의 `MODEL` 입력에 연결.
		-   `Load Checkpoint` 노드의 `CLIP` 출력을 `Load LoRA` 노드의 `CLIP` 입력에 연결.
		-   `Load LoRA` 노드의 `MODEL` 출력을 `K Sampler` 노드의 `model` 입력에 연결.
		-   `Load LoRA` 노드의 `CLIP` 출력을 `CLIP Text Encode (Positive)` (및 `Flux Guidance`를 통한 `K Sampler positive`)에 연결.
		-   `Load LoRA` 노드에서 `flux_realism_lora_v1.safetensors`를 선택.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2627.png" width="300" />
	-   **Lora 적용 후 테스트**
		-   동일 `seed`, 동일 프롬프트로 워크플로우를 다시 실행하여 Lora 적용 전후 이미지 비교.
		-   Lora 적용 후 이미지가 훨씬 더 사실적으로 생성됨을 확인.
		-   다른 프롬프트 (`portrait of a dog`)로도 테스트하여 Lora의 영향을 확인 (미묘하지만 사실적인 개선).
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2645.png" width="300" />
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2730.png" width="300" />

15. **Flux 모델 종합 비교 및 권장 사항**
	-   **Flux 버전별 특징 요약**
		-   **파일 크기**: 클수록 이미지 품질이 좋지만, 더 강력한 GPU (높은 VRAM)와 시스템 RAM이 필요.
		-   **생성 시간 (RTX 4090 기준)**:
			-   Schnell fp8: 3~4초
			-   Dev fp8: 14초 (20 steps)
			-   Dev fp16 (정규): 18초 (20 steps)
			-   Schnell nf4: 3초
			-   Dev nf4: 3초
		-   **품질**: 일반적으로 Dev 버전이 Schnell 버전보다 우수.
		-   **속도**: 파일 크기가 작을수록 빠름.
	-   **권장 사항**
		-   **로우엔드 GPU**: `Schnell` 버전부터 시작.
		-   **미드레인지 GPU**: `Dev floating Point 8` 버전 시도.
		-   **일부 카드에서 최고 속도**: `nf4` 버전.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep08_-_Flux_1___2752.png" width="300" />

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
---
title: (강의) ComfyUI Tutorial Series Ep10 - Flux GGUF and Custom Nodes
---

날짜 : 26.04.13
링크 : [ComfyUI Tutorial Series: Ep10 - Flux GGUF and Custom Nodes](https://youtu.be/Ym0oJpRbj4U?si=vrJTyTPZVZ6E4hc)

## 한 줄 요약

- ComfyUI에서 커스텀 노드를 관리하고 설치하는 방법, 특히 Flux GGUF 모델을 다운로드하고 워크플로우를 구성하며 Dev와 Schnell 버전의 성능 및 결과 차이를 비교하는 과정을 상세히 설명함.

## 핵심 내용

1.  ComfyUI 커스텀 노드의 설치, 제거, 관리 및 누락된 노드 처리 방법.
2.  Flux GGUF 모델 (Dev, Schnell) 및 관련 CLIP, VAE 모델 다운로드 및 폴더 구성.
3.  기존 워크플로우를 Flux GGUF 모델에 맞춰 재구성하는 단계별 과정.
4.  `RG3 Image Comparer`, `Primitive` 노드 등 유용한 커스텀 노드 활용법.
5.  Flux GGUF Dev 및 Schnell 모델의 속도, 품질, 특징 비교 분석.

## 따라한 것 · 실습

1.  ComfyUI Manager 업데이트 및 최신 소식 확인
	- ComfyUI 시작 후 `Manager` 버튼 클릭.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0021.png" width="300" />
	- Latest News에서 업데이트 내용을 확인. (메모리 이슈 수정 등)
	- `Update All` 버튼을 클릭하여 모든 항목을 업데이트.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0037.png" width="300" />
	- 업데이트 완료 메시지 확인 후 `Restart` 클릭.
	- Manager 버전을 확인하여 업데이트가 성공적으로 되었는지 확인.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0046.png" width="300" />

2.  커스텀 노드 관리
	- `Manager` > `Install Custom Nodes` 클릭.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0058.png" width="300" />
	- Filter에서 `Installed`를 선택하여 현재 설치된 커스텀 노드 목록을 확인.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0104.png" width="300" />
	- 각 노드의 ID, Title, Author, Stars, Last Update 정보를 확인 가능.
	- Stars 기준으로 정렬하여 인기 있는 노드를 확인 가능.
	- `Art Venture` 노드 제거: `Art Venture` 노드를 찾아 `Uninstall` 버튼 클릭 후 `OK`로 확인.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0137.png" width="300" />
	- `Restart` 버튼 클릭.
	- `Style CSV Loader` 노드 제거: `Style CSV Loader` 노드를 찾아 `Uninstall` 버튼 클릭 후 `OK`로 확인.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0151.png" width="300" />
	- 경고(Warning) 아이콘 클릭 시 노드 간의 충돌 가능성 확인 가능. (대부분 무시해도 되지만, 문제가 발생하면 노드 비활성화로 문제 해결 시도 가능)
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0155.png" width="300" />
	- `Restart` 버튼 클릭.

3.  누락된 커스텀 노드 처리 및 대체 노드 사용
	- 기존에 `Art Venture` 노드를 사용했던 워크플로우를 열면, 해당 노드가 빨간색으로 하이라이트되며 에러가 발생함.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0227.png" width="300" />
	- `Manager` > `Install Missing Custom Nodes`를 클릭.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0244.png" width="300" />
	- `Art Venture` 노드가 누락된 노드 목록에 표시됨을 확인.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0248.png" width="300" />
	- `Art Venture` 노드를 삭제하고 다른 노드로 대체.
		- `Add Node` (캔버스 더블 클릭) 후 `aio` 검색.
		- `AIO Preprocessor` 노드를 추가.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0306.png" width="300" />
		- 기존 연결(Image to Image)을 `AIO Preprocessor`의 `image` 입력과 연결하고, `AIO Preprocessor`의 `IMAGE` 출력을 `Apply Control Net` 노드의 `image` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0314.png" width="300" />
		- `AIO Preprocessor`에서 `canny`를 선택.
		- `Q Prompt`로 워크플로우 테스트.
	- ComfyUI 기본 `Canny` 노드로 대체:
		- `AIO Preprocessor` 노드 삭제.
		- `Add Node` (캔버스 더블 클릭) 후 `canny` 검색.
		- `Canny` 노드를 추가. (ComfyUI 기본 노드는 상단에 커스텀 노드 이름이 표시되지 않음)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0402.png" width="300" />
		- `Canny` 노드를 `Image to Image`의 `image` 입력에 연결하고, `Canny`의 `IMAGE` 출력을 `Apply Control Net`의 `image` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0408.png" width="300" />
		- `Q Prompt`로 워크플로우 테스트. (입력 이미지 연결 누락 시 빨간색 원 표시됨)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0412.png" width="300" />
		- `Canny` 노드의 추가 설정(low_threshold, high_threshold)을 확인.
	- `Style CSV Loader` 노드 대체
		- `Style CSV Loader`를 사용했던 워크플로우를 로드하면 에러가 발생함.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0429.png" width="300" />
		- `Manager` > `Install Missing Nodes`에서 `Styles Loader`가 목록에 보임.
		- 노드가 작동하지 않을 경우, 노드 제목 클릭 시 GitHub 페이지로 이동하여 설정 및 종속성 정보를 확인해야 함.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0447.png" width="300" />
		- `Style CSV Loader` 노드 삭제.
		- `Add Node` (캔버스 더블 클릭) 후 `prompt` 검색.
		- `WAS Node Suite`의 `Prompt Multiple Style Selector` 노드를 추가.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0519.png" width="300" />
		- `positive` 출력을 `Positive Text Encode` 노드의 `text` 입력에 연결하고, `negative` 출력을 `Negative Text Encode` 노드의 `text` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0527.png" width="300" />
		- 스타일을 선택하고 `Q Prompt`로 테스트.

4.  수동 커스텀 노드 삭제
	- `ComfyUI/custom_nodes` 폴더 내의 노드 중 `Manager`에 표시되지 않는 노드 확인. (예: `NF4`)
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0610.png" width="300" />
	- `NF4` 노드를 더 이상 사용하지 않으므로, `custom_nodes` 폴더에서 해당 폴더를 수동으로 삭제.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0637.png" width="300" />
	- ComfyUI `Restart`.
	- `NF4` 워크플로우를 로드하면 에러가 발생함을 확인.

5.  새로운 유틸리티 커스텀 노드 설치
	- `Manager` > `Install Custom Nodes` 클릭.
	- `Search` 바에 `GGUF` 입력 후 `City96`이 만든 `ComfyUI-GGUF` 노드 설치.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0704.png" width="300" />
	- `Restart` 하지 않고 추가 노드 설치.
	- `Search` 바에 `chris tools` 입력 후 `Chris-tools` 노드 설치. (메모리 모니터링 기능 포함)
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0715.png" width="300" />
	- `Search` 바에 `RG3` 입력 후 `RG3-CustomNodes` 노드 설치. (유용한 노드 포함)
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0722.png" width="300" />
	- `Restart` 클릭.

6.  Flux GGUF 모델 설치 및 구성
	- `Manager` > `Install Custom Nodes` > `Installed`에서 `ComfyUI-GGUF` 노드를 찾고, 노드 이름을 클릭하여 GitHub 페이지로 이동.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0734.png" width="300" />
	- GGUF 모델과 양자화(quantization)에 대한 정보를 확인.
	- GGUF 모델 다운로드 (링크는 영상 설명 또는 Discord에서 제공됨):
		- **UNet 모델**:
			- Dev 및 Schnell 모델 확인 (Q로 시작하는 이름은 양자화 버전).
			- 높은 숫자는 높은 정밀도를 의미하나, 더 많은 자원을 필요로 함.
			- 속도와 품질의 균형을 위해 `Q8` 버전 선택 (예: `flux_dev_q8_0.gguf`).
			- 다운로드 후 `ComfyUI/models/unet` 폴더에 저장. (checkpoint 폴더가 아님에 유의)
			<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0833.png" width="300" />
		- **CLIP 모델**:
			- 텍스트와 이미지 간 관계 이해를 도움.
			- `clip L` 모델 다운로드 후 `ComfyUI/models/clip` 폴더에 저장.
			<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0850.png" width="300" />
			- `T5` CLIP 모델 다운로드 (fp8, fp16 또는 양자화 버전). 품질과 성능을 위해 `Q8` 버전 선택.
			- 다운로드 후 `ComfyUI/models/clip` 폴더에 저장.
			<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0907.png" width="300" />
		- **VAE 모델**:
			- GGUF 모델은 VAE를 포함하지 않음.
			- VAE 모델 다운로드 후 `ComfyUI/models/vae` 폴더에 저장.
			<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0918.png" width="300" />
	- ComfyUI에서 `Refresh` 버튼을 클릭하여 새로 다운로드한 모델들을 목록에 반영.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_0939.png" width="300" />

7.  ComfyUI 인터페이스 및 노드 정보
	- `Chris Tools` 노드가 추가한 메모리 사용량 표시 도구 확인 (캔버스 우클릭).
	<!-- CAPT9 [09:47] Chris Tools 메모리 사용량 표시 -->
	- 노드 탐색: 캔버스 우클릭 > `Add Node` 또는 캔버스 더블 클릭하여 검색.
	- 커스텀 노드 식별:
		- 캔버스 더블 클릭 후 노드 검색 시, 커스텀 노드는 노드 상단에 해당 커스텀 노드의 이름이 표시됨.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1009.png" width="300" />
		- `Manager` > `Settings` > `Badge options`에서 `Nickname`을 `On`으로 설정하여 커스텀 노드 이름을 항상 표시하도록 설정. (기본 노드는 표시 안됨)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1025.png" width="300" />

8.  Flux GGUF 워크플로우 구축
	- 기존 FP8 Dev 버전 워크플로우를 기반으로 변경.
	- `Load Checkpoint` 노드 삭제.
	- `Add Node` (캔버스 더블 클릭) 후 `GGUF` 검색.
	- `GGUF UNet Loader` 노드 추가.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1118.png" width="300" />
	- `unet_name` 목록에서 다운로드한 `flux_dev_q8_0.gguf` 모델 선택.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1122.png" width="300" />
	- `Add Node` (캔버스 더블 클릭) 후 `Dual clip loader` 검색.
	- `Dual Clip Loader (GGUF version)` 노드 추가.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1132.png" width="300" />
	- `clip_name` 목록에서 `clip L` 모델 선택.
	- `T5_name` 목록에서 `T5 Q8` 모델 선택.
	- `type`을 `flux`로 설정.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1141.png" width="300" />
	- `Add Node` (캔버스 더블 클릭) 후 `Load VAE` 검색.
	- `Load VAE` 노드 추가.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1145.png" width="300" />
	- `vae_name` 목록에서 `flux_vae.safetensors` 모델 선택.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1147.png" width="300" />
	- **노드 연결**:
		- `GGUF UNet Loader`의 `MODEL` 출력을 `Text Encode (Positive)` 및 `Text Encode (Negative)` 노드의 `MODEL` 입력에 연결.
		- `Dual Clip Loader`의 `CLIP` 출력을 `Text Encode (Positive)` 및 `Text Encode (Negative)` 노드의 `CLIP` 입력에 연결. (네거티브 프롬프트를 사용하지 않아도 연결해야 함)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1209.png" width="300" />
		- `Load VAE`의 `VAE` 출력을 `VAE Decode` 노드의 `vae` 입력에 연결.
		- `Image to Image`를 사용하는 경우 `VAE Encode` 노드의 `vae` 입력에도 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1222.png" width="300" />
	- `Q Prompt`로 테스트. (첫 생성은 모델 로딩으로 인해 느리지만, 이후 생성은 더 빨라짐)

9.  Flux GGUF 성능 비교 (Q8 vs. Full Dev)
	- `Q8` 모델과 `Dev` 모델의 생성 속도 비교 (예: Q8 첫 생성 28초, 이후 16초; Dev 첫 생성 81초, 이후 20초).
	- `RG3 Image Comparer` 노드를 사용하여 이미지 품질 비교.
		- `Add Node` (캔버스 더블 클릭) 후 `image comparer` 검색.
		- `Image Comparer` 노드 추가.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1328.png" width="300" />
		- 테스트를 위해 `Load Image` 노드 2개를 추가하여 이미지 1과 이미지 2를 로드하고 `Image Comparer`에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1341.png" width="300" />
		- `Image Comparer`는 마우스를 움직여 두 이미지를 슬라이드하여 비교 가능. (`preview size` 조절 가능)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1354.png" width="300" />
	- 실제 워크플로우에 적용하여 비교.
		- `Dev Q8` 워크플로우를 전체 복사.
		- `Full Dev` 버전 워크플로우를 로드하고, 복사한 `Dev Q8` 워크플로우를 옆에 붙여넣기.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1424.png" width="300" />
		- 두 워크플로우의 `K Sampler` 노드에 `fixed` 시드를 설정하여 동일한 이미지를 생성하도록 준비.
		- 동일한 프롬프트 입력.
		- `Image Comparer` 노드를 추가.
		- `Dev Q8` 워크플로우의 `VAE Decode` 출력(`IMAGE`)을 `Image Comparer`의 `image_one` 입력에 연결.
		- `Full Dev` 워크플로우의 `VAE Decode` 출력(`IMAGE`)을 `Image Comparer`의 `image_two` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1500.png" width="300" />
		- **주의**: 고성능 그래픽 카드가 없으면 두 개의 큰 모델을 동시에 로드하는 것이 ComfyUI를 충돌시킬 수 있음.
		- `Q Prompt`로 실행 후 `Image Comparer`로 이미지 비교.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1515.png" width="300" />
		- 품질 차이는 미미하며, Q8이 더 빠름.
		- Q8 모델과 T5 CLIP 모델이 기존 버전에 비해 파일 크기가 절반인 것을 확인.

10. Flux GGUF 워크플로우에 스타일 추가
	- Episode 7을 참조하여 아트 스타일 추가 및 노드 구성.
	- `Prompt Multiple Style Selector` 노드 사용.
	- 스타일을 선택하고 `Q Prompt`로 테스트.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1626.png" width="300" />
	- 노드를 재배치하여 화면에 잘 맞게 정리하고 워크플로우 저장.

11. 컴팩트 버전 워크플로우 생성
	- 노드 그룹 전체 선택 후 우클릭 > `Convert group to nodes`를 선택.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1647.png" width="300" />
	- 일부 노드(예: `Load Image`, `Save Image`)는 그룹 밖에 두어 쉽게 크기 조절 가능하도록 함.
	- 그룹 변환 시 연결이 끊길 수 있으므로, 다시 연결해야 할 수 있음. (Undo 후 재시도 가능)
	- 숨겨진 노드가 있으면 연결이 끊어질 수 있으므로, 다시 보이게 하고 연결.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1711.png" width="300" />
	- 워크플로우 이름에 `compact`를 추가하여 저장.

12. Flux GGUF Schnell 버전 테스트
	- `Schnell Q8` 버전 UNet 모델을 다운로드하여 `ComfyUI/models/unet` 폴더에 저장.
	- `Dev Q8` 워크플로우를 로드.
	- `GGUF UNet Loader` 노드에서 `unet_name`을 `flux_dev_q8_0.gguf`에서 `flux_schnell_q8_0.gguf`로 변경.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1756.png" width="300" />
	- CLIP 모델은 `Schnell`에서도 동일하게 작동함.
	- **주의**: `Flux Guidance` 노드는 `Schnell`과 작동하지 않으므로 삭제해야 함.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1811.png" width="300" />
	- `Schnell`은 `4` 스텝만 필요하지만, `6` 또는 `8`로 설정 가능.
	- `Q Prompt`로 테스트. (첫 생성 17초, 이후 4초 이내로 매우 빠름)

13. Dev vs. Schnell 워크플로우 비교
	- `Schnell` 워크플로우에 `Dev` 워크플로우 노드를 복사하여 붙여넣기.
	- **시드(Seed) 공유 설정**:
		- `K Sampler` 노드를 우클릭 > `Convert widget to input` > `seed` 선택.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1846.png" width="300" />
		- 두 `K Sampler` 노드의 `seed` 입력을 활성화.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1852.png" width="300" />
		- `Add Node` (캔버스 더블 클릭) 후 `primitive` 검색.
		- `Primitive` 노드를 추가.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1856.png" width="300" />
		- `Primitive` 노드의 출력을 두 `K Sampler` 노드의 `seed` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1910.png" width="300" />
		- `Primitive` 노드의 옵션에서 `increment`를 선택하여 프롬프트 큐 시 시드가 1씩 증가하도록 설정.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1915.png" width="300" />
	- **프롬프트(Prompt) 공유 설정**:
		- `Text Encode` 노드를 우클릭 > `Convert widget to input` > `text` 선택. (두 워크플로우 모두)
		- `Add Node` (캔버스 더블 클릭) 후 `positive prompt` 검색.
		- `Comfy Easy Use`의 `Positive Prompt` 노드를 추가.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1949.png" width="300" />
		- `Positive Prompt` 노드의 출력을 두 워크플로우의 `Text Encode` 노드의 `text` 입력에 연결.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_1958.png" width="300" />
	- `Image Comparer` 노드를 추가하고, 각 워크플로우의 `VAE Decode` 출력을 연결하여 비교 준비.
	- `RG3 Label` 노드 추가:
		- `Add Node` (캔버스 더블 클릭) 후 `label` 검색.
		- `RG3-CustomNodes`의 `Label` 노드 추가.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2020.png" width="300" />
		- `Schnell Q8`, `Dev Q8` 등의 레이블을 추가하여 워크플로우를 명확하게 구분.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2025.png" width="300" />
	- 다양한 프롬프트로 테스트 및 결과 비교:
		- **Cartoon Ninja**: Schnell은 디테일 오류가 더 많음. Dev는 더 사실적.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2108.png" width="300" />
		- `Image Comparer` 속성 패널에서 `Click` 대신 `Slide` 옵션을 선호함.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2120.png" width="300" />
		- **Samurai Bunny**: 두 버전 모두 흥미로운 결과 생성.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2204.png" width="300" />
		- **Portrait (glasses, curly hair, white blouse)**: Schnell은 더 선명한 색상 대비, Dev는 더 사실적.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2220.png" width="300" />
		- **Viking (beard, dramatic ready to fight look)**: Schnell은 물체 표현에 어려움, 일러스트 스타일. Dev는 더 사실적이나 완벽하지 않음.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2236.png" width="300" />
		- **Gameplay Menu (pixaroma logo, three buttons with text)**: Schnell은 거의 근접했으나, 텍스트 오류. Dev는 추가 버튼 생성.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2256.png" width="300" />
		- **Dessert (chocolate cake with strawberry, pixaroma dessert on a napkin)**: Dev가 냅킨 텍스트와 딸기를 아름답게 표현.
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2318.png" width="300" />
		- **Vector Style Design (gnome silhouette on white background)**: Dev에서 특정 시드와 벡터 스타일/흰색 배경 프롬프트에서 흐린 이미지가 발생하는 문제 발견. (해결책 필요)
		<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2336.png" width="300" />

14. 커스텀 노드 검색 도구
	- ComfyUI Manager의 검색 기능은 제한적임.
	- `comfy.icu` 웹사이트 `Resources` > `Custom Nodes`에서 더 효과적으로 노드를 검색 가능.
	<img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep10_-_Flux_GGU_2414.png" width="300" />
	- 노드 클릭 시 상세 정보 및 GitHub 페이지로 이동 가능.

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

- Dev 모델에서 특정 시드와 벡터 스타일 프롬프트, 또는 흰색 배경을 지정할 때 이미지가 흐리게 생성되는 문제 원인 및 해결 방법.
- Flux GGUF 사용 시 나타나는 경고 메시지(If anyone knows of a fix please let me know it hasn't affected the speed but I don't like seeing errors)의 의미 및 해결 방법.
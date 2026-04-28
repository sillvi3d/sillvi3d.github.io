---
title: (강의) ComfyUI Tutorial Series Ep12 - How to Upscale Your AI Images
---

날짜 : 26.04.20
링크 : [ComfyUI Tutorial Series: Ep12 - How to Upscale Your AI Images](https://youtu.be/i8v9RbNy4Kw?si=4o08gsGMUgR97Ij)

## 한 줄 요약

- ComfyUI에서 다양한 업스케일 모델과 KSampler를 활용하여 이미지 크기를 늘리고 품질을 향상시키는 상세한 워크플로우를 단계별로 안내함.

## 핵심 내용

1.  ComfyUI 환경 설정: Custom 노드 및 업스케일 모델 설치.
2.  기본 업스케일링: `Upscale Image Using Model` 및 `Upscale Image By` 노드를 활용한 단순 배율 조절.
3.  창의적 업스케일링: `KSampler`와 `VAE Encode/Decode`를 결합하여 디테일을 추가하는 Image-to-Image 방식.
4.  성능 최적화: `Flux Resolution Calculator`와 `tile_size` 설정을 통한 VRAM 관리 및 처리 속도 향상.
5.  다양한 모델 활용: Flux, SDXL, SD 1.5 등 모델별 최적 설정 및 워크플로우 예시.
6.  결과 비교: `Image Comparer` 노드를 사용하여 업스케일 전후 및 모델별 결과 비교.

## 따라한 것 · 실습

1.  **ComfyUI 환경 준비**
    *   **Custom Nodes 설치**
        *   `Manager > Custom Nodes Manager`로 이동함.
        *   `All` 필터로 변경 후 `Control Alt AI nodes`를 검색함.
        *   `Install` 버튼을 클릭하여 설치함. (영상에서는 설치 후 재시작 버튼이 나타남을 보여주며, 바로 사용하지 않으므로 취소함.)
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0040.png" width="300" />
    *   **ComfyUI 업데이트**
        *   `Manager`에서 `Update All`을 선택하여 ComfyUI 및 설치된 노드들을 업데이트함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0054.png" width="300" />
    *   **Upscale 모델 설치**
        *   `Manager > Model Manager`로 이동함.
        *   필터를 `upscale`로 선택함.
        *   다음 모델들을 설치함:
            *   `CAX` (범용 모델)
            *   `Anime Sharp` (애니메이션, 벡터, 깔끔한 그래픽용)
            *   `Maybe Foolhardy` (선택 사항)
        *   설치 후 `Refresh` 버튼을 클릭하여 ComfyUI를 새로고침함. 재시작은 필요 없음.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0120.png" width="300" />
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0136.png" width="300" />
    *   **워크플로우 로드 (선택 사항)**
        *   강의자는 Discord에 공유된 워크플로우를 로드하여 설명함. (`File > Load` 또는 드래그 앤 드롭).
        *   (초반 워크플로우 시연은 복잡하므로 건너뛰고, `Clear` 후 직접 노드 구성부터 진행함.)

2.  **기본 이미지 업스케일링 (Simple Upscale)**
    *   캔버스에서 `Clear` 버튼을 클릭하여 모든 노드를 지움.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0224.png" width="300" />
    *   **Upscale 기본 구성**
        *   빈 공간을 더블 클릭하여 `upscale image using model` 노드를 검색 및 추가함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0630.png" width="300" />
        *   `upscale_model` 입력에서 드래그하여 `upscale model loader` 노드를 추가함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0638.png" width="300" />
        *   `Upscale Model Loader`에서 `upscale_model_name`으로 `CX model`을 선택함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0656.png" width="300" />
        *   빈 공간을 더블 클릭하여 `load image` 노드를 추가함.
        *   이미지를 로드함. (예: 인물 초상화)
        *   `Load Image` 노드의 `image` 출력을 `Upscale Image Using Model` 노드의 `image` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0712.png" width="300" />
        *   빈 공간을 더블 클릭하여 `save image` 노드를 추가함.
        *   `Upscale Image Using Model` 노드의 `image` 출력을 `Save Image` 노드의 `image` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0716.png" width="300" />
        *   `Queue Prompt`를 클릭하여 워크플로우를 실행함.
        *   결과 이미지가 원본 (1024px)보다 4배 커진 4096px로 생성됨을 확인 (모델이 4X 업스케일 모델이므로).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0738.png" width="300" />
    *   **업스케일 배율 조절**
        *   `Save Image` 노드 앞에 `upscale image by` 노드를 추가함.
        *   `Upscale Image Using Model` 노드의 `image` 출력을 `Upscale Image By` 노드의 `image` 입력에 연결함.
        *   `Upscale Image By` 노드의 `image` 출력을 `Save Image` 노드의 `image` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0802.png" width="300" />
        *   `Upscale Image By` 노드의 `upscale_method`를 `lanczos`로 선택함.
        *   `scale_by` 값을 `0.5`로 변경함. (4X 모델에 0.5를 적용하여 최종 2배 업스케일).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0814.png" width="300" />
        *   `Queue Prompt`를 실행하면 2048px 크기의 이미지가 생성됨.
    *   **이미지 비교: `Image Comparer` 활용**
        *   빈 공간을 더블 클릭하여 `image comparer` 노드를 추가함 (RG3 노드팩).
        *   `Load Image` 노드의 `image` 출력을 `Image Comparer` 노드의 `image_a` 입력에 연결함.
        *   `Upscale Image By` 노드의 `image` 출력을 `Image Comparer` 노드의 `image_b` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0834.png" width="300" />
        *   `Queue Prompt`를 실행하고 `Image Comparer` 노드를 확대하면 슬라이더를 움직여 원본과 업스케일된 이미지를 비교할 수 있음. 업스케일된 이미지가 더 선명하고 커진 것을 확인.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0842.png" width="300" />
    *   **모델별 비교**
        *   현재 워크플로우를 복제함 (Ctrl+C, Ctrl+V 또는 드래그 후 Alt+드래그).
        *   복제된 워크플로우의 `Upscale Model Loader`에서 `upscale_model_name`을 `anime_sharp`로 변경함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0914.png" width="300" />
        *   새 `Image Comparer` 노드를 추가함.
        *   첫 번째 워크플로우 (CAX)의 `Save Image` 노드에서 `image` 출력을 새 `Image Comparer`의 `image_a`에 연결함.
        *   두 번째 워크플로우 (Anime Sharp)의 `Save Image` 노드에서 `image` 출력을 새 `Image Comparer`의 `image_b`에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_0928.png" width="300" />
        *   `Queue Prompt`를 실행하고 비교하면, `anime_sharp` 모델이 벡터 이미지에 더 선명하고 깔끔한 가장자리를 제공함을 확인. `CAX` 모델은 약간의 '글로우'를 추가할 수 있음.

3.  **창의적 업스케일링 (Text-to-Image + Image-to-Image Upscale)**
    *   새 캔버스에 `Text to Image Flux` 워크플로우를 로드함 (에피소드 10에서 다룬 Guff 버전).
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1016.png" width="300" />
    *   **초기 해상도 제어: `Flux Resolution Calculator` 사용**
        *   `Empty Image` 노드 (또는 `Latent Image`) 노드의 `width`, `height` 위젯에서 `Right Click > Convert widget to input`을 선택하여 입력 포트로 변경함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1040.png" width="300" />
        *   빈 공간을 더블 클릭하여 `flux resolution calculator` 노드를 추가함 (Control Alt AI nodes 팩에 포함).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1028.png" width="300" />
        *   `Flux Resolution Calculator`의 `width` 출력을 `Empty Image`의 `width` 입력에 연결하고, `height` 출력을 `Empty Image`의 `height` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1050.png" width="300" />
        *   `Flux Resolution Calculator` 노드의 `megapixels`와 `aspect_ratio`를 설정함 (예: `1` megapixel, `Square`).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1110.png" width="300" />
    *   **1차 업스케일 (단순 배율)**
        *   `VAE Decode` 노드의 `image` 출력을 `upscale image by` 노드의 `image` 입력에 연결함.
        *   `upscale_method`는 `lanczos`, `scale_by`는 `2`로 설정함 (2배 업스케일).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1150.png" width="300" />
        *   `Upscale Image By` 노드의 `image` 출력을 `save image` 노드에 연결하여 1차 업스케일 결과(2048px)를 저장함.
    *   **2차 업스케일 (모델 활용)**
        *   `Upscale Image By` 노드의 `image` 출력을 `upscale image using model` 노드의 `image` 입력에 연결함.
        *   `upscale model loader` 노드를 추가하고 `model_name`을 `cax`로 설정한 후, `Upscale Image Using Model`에 `upscale_model`을 연결함.
        *   `Upscale Image Using Model` 노드의 `image` 출력을 다시 `upscale image by` 노드의 `image` 입력에 연결함.
        *   `Upscale Image By` 노드의 `scale_by`를 `0.5`로 설정함 (CAX가 4배 모델이므로 0.5를 곱해 최종 2배 효과).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1350.png" width="300" />
        *   `Upscale Image By` 노드의 `image` 출력을 `save image` 노드에 연결하여 2차 업스케일 결과(4096px)를 저장함.
    *   **`KSampler`를 통한 디테일 추가 (Image-to-Image)**
        *   `k sampler` 노드를 추가함.
        *   `Load Checkpoint` 노드의 `model` 출력을 `KSampler` 노드의 `model` 입력에 연결함.
        *   `CLIPTextEncode` (Positive) 노드의 `conditioning` 출력을 `KSampler` 노드의 `positive` 입력에 연결함.
        *   `CLIPTextEncode` (Negative) 노드의 `conditioning` 출력을 `KSampler` 노드의 `negative` 입력에 연결함. (노드가 축소되어 있으면 클릭하거나 `Right Click > Collapse`를 해제하여 연결함.)
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1515.png" width="300" />
        *   **픽셀 -> Latent -> 픽셀 변환**
            *   2차 업스케일을 담당하는 `Upscale Image By` 노드의 `image` 출력을 `vae encode` 노드의 `pixels` 입력에 연결함.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1550.png" width="300" />
            *   `VAE Encode` 노드의 `latent` 출력을 `KSampler` 노드의 `latent_image` 입력에 연결함.
            *   `KSampler` 노드의 `latent` 출력을 `vae decode` 노드의 `latent` 입력에 연결함.
            *   `VAE Decode` 노드의 `image` 출력을 `save image` 노드에 연결함.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1608.png" width="300" />
            *   **VAE 로드**: `Load Checkpoint`에 VAE가 내장되어 있지 않다면, 빈 공간을 더블 클릭하여 `load vae` 노드를 추가함.
            *   `Load VAE` 노드의 `vae` 출력을 `VAE Encode`와 `VAE Decode` 노드의 `vae` 입력에 연결함.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1638.png" width="300" />
        *   **`KSampler` 설정 (Flux 기준)**
            *   `cfg` 값을 `1`로 설정함 (Flux는 negative prompt를 무시하므로).
            *   `denoise` 값을 `0.8`에서 `0.95` 사이 (예: `0.85`)로 설정함. (값이 `1`이면 이미지가 완전히 새로 생성됨.)
            *   `sampler_name`은 `dpmpp_2m`, `scheduler`는 `karras`를 추천함.
            <!-- CAPT통 [17:08] KSampler 설정 화면 (CFG, Denoise, Sampler) -->
        *   **성능 최적화**:
            *   초기 생성 이미지 크기를 줄여 `KSampler`의 처리 시간을 단축함.
            *   `Flux Resolution Calculator` 노드의 `megapixels`를 `0.5`로 설정함. (초기 이미지 크기가 704px로 줄어들어 워크플로우가 빨라짐.)
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1835.png" width="300" />
        *   **최종 업스케일**
            *   `KSampler`를 거쳐 디테일이 추가된 이미지 (2048px)를 다시 한번 `Upscale Image Using Model`과 `Upscale Image By` 노드를 연결하여 최종 업스케일함. (앞서 사용한 노드들을 복사해서 연결 가능)
            *   `Upscale Model Loader`는 기존의 `cax` 모델을 재활용하거나 필요에 따라 새로운 모델 로더를 추가할 수 있음.
            *   `Upscale Image By`의 `scale_by`는 최종 원하는 크기에 따라 `0.5` (2배) 또는 `1` (4배)로 설정함.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_1940.png" width="300" />
            *   결과를 `save image` 노드에 연결하여 최종 이미지를 저장함.
        *   **결과 비교**
            *   `Image Comparer` 노드를 추가하여 초기 생성 이미지와 최종 업스케일 이미지(`image_a`: 초기 생성 `save image`, `image_b`: 최종 업스케일 `save image`)를 비교함.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2040.png" width="300" />
            *   또 다른 `Image Comparer` 노드를 추가하여 `KSampler` 후 이미지와 최종 업스케일 이미지를 비교함 (`image_a`: `KSampler` 후 `save image`, `image_b`: 최종 업스케일 `save image`).
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2050.png" width="300" />
            *   `Queue Prompt`를 실행하면 세 가지 이미지(초기 생성, KSampler 후, 최종 업스케일)와 두 가지 비교 결과를 확인할 수 있음. 최종 이미지가 훨씬 선명하고 디테일이 많음을 확인.

4.  **다양한 모델별 업스케일링 예시**
    *   **SDXL 워크플로우**
        *   Juggernaut X와 같은 SDXL 모델을 로드한 워크플로우를 사용함.
        *   `KSampler` 노드의 `denoise` 값 범위를 `0.2` ~ `0.4`로 조정함. (Flux와 다름).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2515.png" width="300" />
    *   **저 VRAM (SDXL Hyper) 워크플로우**
        *   `VAE Decode Tiled`, `VAE Encode Tiled` 노드를 사용하는 워크플로우를 사용함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2550.png" width="300" />
        *   `tile_size` 설정을 `512` 또는 `1024`로 조정하여 VRAM 사용량을 절약하고 GPU 메모리 부족으로 인한 오류를 방지함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2605.png" width="300" />
    *   **SD 1.5 워크플로우**
        *   Juggernaut Reborn과 같은 SD 1.5 모델을 로드한 워크플로우를 사용함.
        *   `denoise` 값을 모델에 맞게 조정함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2640.png" width="300" />
        *   결과 이미지는 SD 모델임에도 불구하고 좋은 디테일과 질감을 제공함.

5.  **간단한 업스케일러 (Simple Upscaler)**
    *   **워크플로우 구성**
        *   `load image` 노드 추가 및 이미지 로드.
        *   `upscale model loader` 노드 추가 및 모델 선택 (예: `CX model`).
        *   `upscale image using model` 노드 추가. `image`와 `upscale_model` 연결.
        *   `upscale image by` 노드 추가 및 `image` 연결, `scale_by` 설정.
        *   `save image` 노드 추가 및 최종 `image` 연결.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2738.png" width="300" />
    *   **결과 비교**
        *   `image comparer` 노드를 추가하여 원본 (`Load Image`의 `image`)과 업스케일된 이미지 (`Save Image` 앞의 `image`)를 비교함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2748.png" width="300" />
    *   **워크플로우 간소화**
        *   비교가 필요 없다면 `Image Comparer` 노드를 삭제하여 `Load Image` -> `Upscale Model Loader` + `Upscale Image Using Model` -> `Save Image`의 간소화된 워크플로우로 사용할 수 있음.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2810.png" width="300" />

6.  **콤팩트 버전의 Image-to-Image Upscaler (Flux)**
    *   화면에 모든 노드가 들어가도록 최적화된 Image-to-Image 업스케일러 (Flux) 워크플로우를 사용함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2840.png" width="300" />
    *   풍경 사진이나 애니메이션 이미지, 라인 아트 등 다양한 이미지에 적용하여 디테일이 향상되는 것을 확인함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2905.png" width="300" />
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2930.png" width="300" />
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep12_-_How_to_U_2940.png" width="300" />
    *   특히 Flux 모델과 함께 사용할 때 가장 좋은 업스케일 결과를 제공함을 강조함. RTX 4090 GPU 기준으로 1분 이내에 생성 및 업스케일이 가능하여 빠른 처리가 가능함.

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
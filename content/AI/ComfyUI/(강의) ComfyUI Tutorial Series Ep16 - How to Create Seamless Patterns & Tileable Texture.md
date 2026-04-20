---
title: (강의) ComfyUI Tutorial Series Ep16 - How to Create Seamless Patterns & Tileable Texture
---

날짜 : 26.04.20
링크 : [ComfyUI Tutorial Series Ep16 - How to Create Seamless Patterns & Tileable Textures](https://www.youtube.com/watch?v=QIvWdmqVx6E)

## 한 줄 요약

- 이 영상은 ComfyUI에서 특정 커스텀 노드를 활용하여 끊김 없는 패턴과 타일형 텍스처를 생성하고, 이를 다양한 방식으로 확인 및 조작하는 방법을 단계별로 설명함.

## 핵심 내용

1.  ComfyUI 환경 설정 및 필수 노드(`Seamless Tile`, `Circular VAE Decode Tile`, `Grid Filler`, `Offset Image`) 설치.
2.  Seamless 패턴 및 타일형 텍스처 생성을 위한 핵심 노드 연결 방법과 워크플로우 구축.
3.  생성된 패턴의 반복성 검증 (Photoshop 활용 및 ComfyUI `Grid Filler` 노드를 통한 시각적 확인).
4.  ChatGPT를 활용하여 효과적인 프롬프트를 생성하는 방법.
5.  `Offset Image` 노드를 사용하여 패턴의 위치를 조정하고 단방향 타일링을 구현하는 방법.
6.  ComfyUI에서 `Save Image` 노드의 `prefix` 설정을 통한 출력 파일 관리 방법.
7.  Seamless 패턴의 실제 적용 사례와 SD3/Flux 모델과의 호환성 한계점.

## 따라한 것 · 실습

1.  **Seamless 패턴 및 타일형 텍스처 개요**
    *   Seamless 패턴 및 타일형 텍스처는 3D 모델, 원단 인쇄, 웹 배경, 벽지, 포장지 등 다양한 프로젝트에 활용됨.
    *   타일링을 통해 번거로움 없이 더 큰 이미지를 쉽게 생산할 수 있음.

2.  **ComfyUI 환경 설정 및 필수 노드 설치**
    *   ComfyUI Manager 실행.
        *   Manager (`우클릭 빈 공간 > Manager`) 또는 ComfyUI 웹 UI에서 `Manager` 버튼 클릭.
    *   ComfyUI 및 노드 업데이트.
        *   `Manager > Update ComfyUI` 클릭.
        *   `Manager > Update All` 클릭.
        *   업데이트 완료 후 `Restart ComfyUI` 클릭하여 재시작.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0035.png" width="300" />
    *   `seamless tiling node` 설치.
        *   `Manager > Install Custom Nodes` 클릭.
        *   검색창에 `seamless tiling` 입력 후 `seamless tiling node` (by `spinon`) 찾아서 `Install` 클릭.
        *   설치 완료 후 `Restart ComfyUI` 클릭하여 재시작.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0048.png" width="300" />
    *   기본 SDXL 워크플로우 로드.
        *   `Load Default` 클릭 또는 `Load` 버튼 클릭하여 SDXL 기본 워크플로우 불러오기. (영상에서는 Ep3에서 다룬 기본 SDXL 워크플로우를 사용함)
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0100.png" width="300" />
        *   참고: SD1.x, SDXL 워크플로우에서 작동하며, SD3 또는 Flux에서는 작동하지 않음.

3.  **Seamless Tiling 워크플로우 구축**
    *   노드 간 간격 확보.
        *   `CheckpointLoader` 이후 `K-Sampler` 이전에 노드를 추가할 공간을 확보하기 위해 노드들을 옆으로 이동시킴.
    *   `Seamless Tile` 노드 추가.
        *   캔버스에서 `더블클릭` 후 `seamless` 검색, `Seamless Tile` 노드 선택.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0121.png" width="300" />
        *   `CheckpointLoader`의 `MODEL` 출력을 `Seamless Tile`의 `MODEL` 입력에 연결함.
        *   `Seamless Tile`의 `MODEL` 출력을 `K-Sampler`의 `model` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0130.png" width="300" />
        *   `Seamless Tile` 노드에는 `enable`, `tiling_x_only`, `tiling_y_only` 옵션이 있음. (초기에는 `enable`만 활성화)
    *   `VAE Decode` 노드 교체.
        *   기존 `VAE Decode` 노드를 삭제.
        *   캔버스에서 `더블클릭` 후 `circular vae decode tile` 검색, `Circular VAE Decode Tile` 노드 선택.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0152.png" width="300" />
        *   `K-Sampler`의 `LATENT` 출력을 `Circular VAE Decode Tile`의 `samples` 입력에 연결함.
        *   `CheckpointLoader`의 `VAE` 출력을 `Circular VAE Decode Tile`의 `vae` 입력에 연결함. (VAE가 모델에 포함된 경우 `CheckpointLoader`의 `VAE` 출력을 바로 연결함)
        *   `Circular VAE Decode Tile`의 `IMAGE` 출력을 `Save Image` 노드의 `images` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0158.png" width="300" />
        *   `Circular VAE Decode Tile` 노드의 색상을 파란색으로 변경하여 식별하기 쉽게 함. (`노드 우클릭 > Color` 메뉴 이용)
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0211.png" width="300" />
    *   프롬프트 추가 및 실행.
        *   `Positive Prompt`에 원하는 패턴을 설명하는 프롬프트를 입력함.
        *   예시 프롬프트: `"a field of various colorful flowers on a white background, minimal, flat design, illustration"`
        *   `Queue Prompt`를 클릭하여 이미지 생성.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0234.png" width="300" />
    *   생성된 이미지의 반복성 포토샵에서 확인.
        *   생성된 이미지를 Photoshop으로 복사/저장하여 불러옴.
        *   이미지를 복제하여 원본 이미지의 상하좌우에 배치하면 패턴이 완벽하게 반복되는 것을 확인할 수 있음.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0250.png" width="300" />
        *   패턴으로 정의: `Edit > Define Pattern`을 통해 Photoshop 패턴으로 저장 가능.
        *   새 문서에 `Pattern Layer`를 추가하여 저장된 패턴을 적용하고 스케일, 회전 등을 조작하여 활용 가능함. (스케일은 100%를 권장하며, 75%, 50%, 25% 등 작게 조절하는 것이 좋음. 크게 만드는 것은 권장하지 않음)
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0320.png" width="300" />
        *   작은 패턴 이미지는 웹사이트 배경 등으로 사용하여 빠른 로딩과 전체 화면 반복 효과를 얻을 수 있음.

4.  **ComfyUI 내에서 반복 이미지 확인 (Grid Filler)**
    *   `ey tools` (이전 에피소드에서 설치) 노드를 활용함.
    *   `Grid Filler` 노드 추가.
        *   캔버스에서 `더블클릭` 후 `ey tools` 검색, `Grid Filler` 노드 선택.
        *   `Circular VAE Decode Tile`의 `IMAGE` 출력을 `Grid Filler`의 `image` 입력에 연결함.
        *   새 `Save Image` 노드를 추가하고 `Grid Filler`의 `IMAGE` 출력을 `Save Image`의 `images` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0408.png" width="300" />
    *   `Grid Filler` 설정.
        *   `rows`와 `cols`를 `3`으로 설정하여 3x3 격자를 만듦.
        *   `gaps` 파라미터를 `0`으로 설정하여 격자 선을 제거함. (기본값인 `2`로 설정 시 검은색 간격이 생김)
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0441.png" width="300" />
        *   `grid_width`와 `grid_height` 파라미터는 기본적으로 `1024`로 설정되어 있음.
            *   원본 이미지(`1024px`)가 3x3 격자에 들어가도록 압축되어 최종 이미지 사이즈는 `1024px`로 유지됨. 즉, 각 타일은 `1024/3` 크기로 생성됨.
            *   만약 `rows`와 `cols`를 `2`로 설정하면 각 타일은 `512px`(`1024/2`) 크기로 생성됨.
        *   원본 이미지 크기를 유지한 채 반복하려면 `grid_width`와 `grid_height`를 `원본 이미지 크기 * 반복 횟수`로 설정해야 함.
            *   예시: `1024`px 이미지 3x3 반복 시, `grid_width`와 `grid_height`를 `1024 * 3 = 3072`로 설정.
            *   `grid_width`를 `3072`, `grid_height`를 `3072`로 변경.
            *   `Queue Prompt`를 클릭하여 재실행.
            *   생성된 최종 이미지의 크기가 `3072 x 3072`로 원본 이미지 크기(`1024 x 1024`)를 유지하며 3x3으로 반복됨을 확인할 수 있음.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0554.png" width="300" />
    *   Tiling 기능 비활성화 시 차이점 확인.
        *   `Seamless Tile` 노드의 `enable` 체크박스를 해제(`false`)한 후 `Queue Prompt`를 클릭하여 재실행.
        *   생성된 이미지에서 경계선이 생기고 패턴이 반복되지 않는 것을 확인할 수 있음.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0619.png" width="300" />

5.  **프롬프트 엔지니어링 및 생성 예시**
    *   ChatGPT를 이용한 프롬프트 생성 방법.
        *   ChatGPT에게 `stable diffusion prompt`를 요청함.
        *   예시: `"generate a stable diffusion prompt for flowers on a white background"`
        *   ChatGPT의 기억(memory) 기능을 활용하여 특정 스타일(`three-dimensional layer designs`)을 미리 저장해두거나, 특정 스타일을 제거해달라고 요청하여 프롬프트를 조정할 수 있음.
        *   따옴표 제거 등 추가적인 프롬프트 수정 요청도 가능함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0711.png" width="300" />
    *   다양한 프롬프트로 이미지 생성.
        *   `"a field of various colorful flowers on a white background, minimal, flat design, illustration"` 프롬프트로 생성.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0723.png" width="300" />
        *   `"wooden planks, minimalist, simple, oak wood type"` 프롬프트로 나무 패턴 생성. 시드를 변경하며 더 나은 결과를 얻을 수 있음.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0744.png" width="300" />

6.  **Offset Image 노드 활용**
    *   `Offset Image` 노드 추가.
        *   캔버스에서 `더블클릭` 후 `offset image` 검색, `Offset Image` 노드 선택.
        *   `Circular VAE Decode Tile`의 `IMAGE` 출력을 `Offset Image`의 `image` 입력에 연결함.
        *   새 `Save Image` 노드를 추가하고 `Offset Image`의 `IMAGE` 출력을 `Save Image`의 `images` 입력에 연결함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0759.png" width="300" />
    *   X/Y축 오프셋 조정.
        *   `offset_x_pct`, `offset_y_pct` 파라미터는 이미지의 x/y축을 기준으로 얼마만큼 이동시킬지 퍼센트로 지정함.
        *   초기 값 `0`으로 실행 시 원본과 동일함.
        *   `offset_x_pct`를 `10`, `20`, `50`, `80` 등으로 변경하면 이미지가 그만큼 X축으로 이동하며 반대편에서 나타남. `100`으로 설정하면 다시 원점으로 돌아옴.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0824.png" width="300" />
        *   `offset_y_pct`도 동일하게 Y축으로 이미지를 이동시킬 수 있음.
    *   `modify_in_place` 옵션.
        *   `modify_in_place` (기본값: `make_a_copy`) 옵션은 이미지 처리 방식을 결정함.
        *   `make_a_copy` 사용을 권장함. (과거 PC에서 오류가 발생한 경험이 있음)
    *   단방향 Tiling (X only, Y only) 기능 확인.
        *   `Seamless Tile` 노드에서 `enable`을 비활성화하고 `tiling_x_only`만 활성화.
        *   `Queue Prompt`를 클릭하면 X축 방향으로만 패턴이 반복됨.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0904.png" width="300" />
        *   `tiling_y_only`만 활성화하면 Y축 방향으로만 패턴이 반복됨.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0918.png" width="300" />
        *   도시 풍경 등 특정 방향으로만 반복이 필요한 경우 유용하게 활용됨.
        *   일반적으로는 `enable` (`x`, `y` 모두 반복)을 사용하는 것이 좋음.

7.  **출력 파일 관리**
    *   `Save Image` 노드의 `prefix` 설정.
        *   출력 폴더에 저장되는 이미지 파일 이름에 일정한 접두사를 붙여 파일들을 쉽게 구분할 수 있음.
        *   각 `Save Image` 노드에서 `prefix` 파라미터에 원하는 접두사를 입력함.
        *   예시: `pat`, `pat_o`, `pat_x3` 등.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_0956.png" width="300" />
        *   `Queue Prompt`를 실행하면 지정된 접두사가 붙은 이미지들이 출력 폴더에 생성됨.
        *   `Grid Filler`를 통해 `1024 * 5 = 5120` 픽셀 크기의 초대형 이미지를 생성할 수 있음.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_1014.png" width="300" />

8.  **마무리**
    *   **활용 사례**: 직물 디자인, 에코백 프린트, 머그컵 인쇄, 의류, 포장 디자인, 벽지, 랩핑지 등 다양한 분야에 적용 가능함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series_Ep16_-_How_to_Cr_1035.png" width="300" />
    *   **SD3/Flux 호환성 한계**: `seamless tiling node`는 SD3 또는 Flux 모델 아키텍처와 달라 작동하지 않음. 향후 개발되기를 기대함.

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
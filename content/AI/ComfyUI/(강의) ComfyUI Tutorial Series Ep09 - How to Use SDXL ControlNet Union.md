---
title: (강의) ComfyUI Tutorial Series Ep09 - How to Use SDXL ControlNet Union
---

날짜 : 26.04.13
링크 : [ComfyUI Tutorial Series: Ep09 - How to Use SDXL ControlNet Union](https://youtu.be/C0zykaDF1ts?si=k70E9L8t8q0u-w3J)

## 한 줄 요약

- ComfyUI에서 SDXL ControlNet Union 모델을 설치하고, 단일 또는 다중 Pre-processor를 활용하여 이미지의 구성과 스타일을 정밀하게 제어하는 방법을 단계별로 익힘.

## 핵심 내용

1.  **ControlNet Union SDXL 소개 및 설치**: SDXL용 통합 ControlNet Union 모델의 특징, 다운로드 및 설치 방법을 이해함.
2.  **ComfyUI 인터페이스 업데이트 및 커스텀 노드 설치**: ComfyUI의 새로운 인터페이스 기능과 ControlNet 사용에 필요한 `ComfyUI-Art-Venture`, `ControlNet Auxiliary Preprocessors`, `Comfyroll-Studio` 등의 커스텀 노드 설치 방법을 익힘.
3.  **ControlNet Pre-processor의 이해와 활용**: Canny, Depth, MLSD 등 다양한 Pre-processor의 역할과 특징을 파악하고, 이미지에서 특정 정보를 추출하는 방법을 실습함.
4.  **단일 ControlNet을 워크플로우에 통합**: SDXL 기본 텍스트-투-이미지 워크플로우에 단일 ControlNet을 추가하고, `Apply ControlNet` 노드와 `strength` 값을 조절하여 생성 이미지에 ControlNet의 영향을 적용하는 방법을 배움.
5.  **다중 ControlNet (Stacking) 워크플로우 구현**: `CR MultiControlNet Stack` 및 `CR Apply MultiControlNet` 노드를 사용하여 여러 ControlNet Pre-processor를 동시에 적용하고, 각 ControlNet의 `strength`를 조절하여 더욱 복합적인 이미지 제어를 수행하는 방법을 학습함.
6.  **생성 이미지의 비율 및 디테일 제어**: ControlNet 사용 시 이미지의 가로세로 비율 조정의 중요성과 Photoshop 등의 외부 도구를 활용하여 정확한 비율을 맞추는 방법을 이해함.

## 따라한 것 · 실습

### 1. ControlNet Union SDXL 소개 및 설치

1.  **ControlNet Union 모델의 이해**
    *   ControlNet Union은 SDXL용으로 특별히 설계된 통합 ControlNet 모델임.
    *   기존에는 포즈(pose)나 캐니(canny) 등 특정 용도에 따라 개별 모델이 필요했지만, Union 모델은 이 모든 옵션을 하나로 통합함.
    *   이 모델은 총 12가지의 컨트롤을 포함하며, 특정 구성을 일치시키는 이미지를 AI가 생성하도록 도움.
    *   ControlNet은 안정적인 확산(Stable Diffusion)을 위한 가이드 도구로, AI가 특정 구조나 스타일에 따라 이미지를 만들도록 지원함.
    *   ControlNet 모델은 특정 AI 모델(예: SD 1.5용은 SD 1.5 모델에만, SDXL용은 SDXL 모델에만)과 호환됨.
2.  **ControlNet Union 모델 다운로드**
    *   모델은 Hugging Face 페이지에서 다운로드 가능함.
    *   `Files and versions` 섹션으로 이동.
    *   나열된 두 모델 중 `Promax`라고 불리는 최신 모델을 선택함.
    *   `Download` 버튼 클릭.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0046.png" width="300" />
3.  **다운로드한 모델 ComfyUI에 저장**
    *   ComfyUI 설치 폴더로 이동함.
    *   `models` 폴더 안의 `controlnet` 폴더를 찾음.
    *   다운로드한 `Promax` 모델 파일을 이 `controlnet` 폴더에 저장함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0052.png" width="300" />

### 2. ComfyUI 업데이트 및 새 인터페이스 기능 소개 (선택 사항)

1.  **ComfyUI 업데이트**
    *   `Manager` 버튼을 클릭한 후 `Update ComfyUI`를 실행하여 최신 버전으로 업데이트함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0140.png" width="300" />
2.  **새로운 인터페이스 기능**
    *   **노드 미리보기**: 캔버스에서 더블 클릭 시, 왼쪽에 각 노드의 미리보기가 표시되어 노드 추가 전 확인 가능함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0149.png" width="300" />
    *   **설정 (Settings)**:
        *   메뉴 활성화/비활성화 및 위치(상단/하단) 조정 가능함.
        *   노드 라이브러리 (Node Library) 사이드바에서 노드를 검색, 폴더 확장, 드래그 앤 드롭으로 추가할 수 있음.
        *   노드 맵(Node Map)에서 노드를 활성화/비활성화(눈 아이콘)할 수 있음.
        *   하단에 `Manager`와 `Queue` 버튼이 있음.
    *   **테마 변경**: `Settings` 버튼을 통해 테마 색상 옵션(Light, Solarized, Arc, Obsidian 등) 변경 가능함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0235.png" width="300" />
    *   **이전 인터페이스로 복귀**: `Settings`에서 아래로 스크롤하여 `Disable new menu option`을 비활성화하면 원래 인터페이스로 돌아갈 수 있음.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0247.png" width="300" />

### 3. ControlNet 사용을 위한 커스텀 노드 설치

1.  **Custom Nodes Manager 진입**
    *   `Manager` > `Custom Nodes Manager`로 이동함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0300.png" width="300" />
2.  **필요한 커스텀 노드 설치**
    *   **ComfyUI Art Venture**:
        *   "Venture"로 검색하여 `ComfyUI-Art-Venture` 노드를 설치함.
        *   이 노드는 ControlNet Pre-processor를 포함하며 워크플로우에 필요함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0306.png" width="300" />
    *   **ControlNet Auxiliary Preprocessors**:
        *   "pre-processors"로 검색하여 `ControlNet Auxiliary Preprocessors` 노드를 설치함.
        *   이 노드는 추가적인 Pre-processor에 접근 가능하게 함.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0315.png" width="300" />
    *   **Comfyroll Studio**:
        *   "comfy roll"로 검색하여 `Comfyroll-Studio` 노드를 설치함.
        *   이 노드는 여러 ControlNet 모델을 스택(stack)하는 데 사용됨.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0325.png" width="300" />
3.  **ComfyUI 재시작**: 모든 노드 설치 후 `Restart` 버튼을 클릭하여 ComfyUI를 재시작함.

### 4. ControlNet Pre-processor 단독 사용 및 이해

1.  **빈 캔버스 준비**
    *   `Clear` 버튼을 사용하여 캔버스를 비움.
2.  **Pre-processor 노드 추가 및 연결**
    *   빈 공간을 더블 클릭하여 `controlnet pre-processor`를 검색하고 `ControlNet Pre-processor (Art Venture)` 노드를 추가함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0347.png" width="300" />
    *   `Load Image` 노드를 왼쪽에 연결함.
    *   `Preview Image` 또는 `Save Image` 노드를 오른쪽에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0402.png" width="300" />
3.  **Pre-processor 설정 및 실행**
    *   `preprocessor` 설정이 `none`인 경우, 실행해도 아무것도 나타나지 않음.
    *   `preprocessor` 드롭다운에서 `canny`를 선택하고 실행함. 결과로 Canny 맵이 생성됨.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0431.png" width="300" />
4.  **Pre-processor의 역할 이해**
    *   이미지가 AI 모델을 통과하기 전에 `preprocessor`에 의해 분석됨.
    *   `preprocessor`는 이미지에서 가장자리, 윤곽선, 깊이 등 특정 특징을 추출하는 필터나 스캐너처럼 작동함.
    *   입력 이미지를 AI가 쉽게 이해할 수 있는 형태로 단순화하여, 마치 건물을 짓기 위한 청사진(blueprint)을 만드는 것과 같음.
5.  **Pre-processor 설정 조정**
    *   `SD Version`을 `SDXL`로 선택함 (아직 SDXL 워크플로우를 추가하지 않았더라도 설정에 익숙해지기 위함).
    *   `Resolution`을 `512` 또는 `1024`로 선택함. 높은 해상도는 더 많은 픽셀과 세부 정보를 제공하지만, 너무 높으면 오류가 발생할 수 있음.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0528.png" width="300" />
    *   다른 이미지(예: 여성 사진)를 업로드하여 `preprocessor` 선택이 캡처되는 디테일 수준에 영향을 미치는 것을 확인함.
    *   `preprocessor`를 `depth` 등으로 변경하면 완전히 다른 맵이 생성됨.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0602.png" width="300" />
    *   동일한 이미지에 여러 `preprocessor`를 적용할 수 있음 (예: 건물 이미지에 Depth와 Canny 맵 동시 적용).
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0612.png" width="300" />
6.  **자주 사용되는 Pre-processor 설명**
    *   **Canny**:
        *   이미지의 가장자리(edges)를 감지함. 연필로 물체의 윤곽선을 그리는 것과 같음.
        *   주요 선과 경계를 강조하며, 물체의 구조가 중요한 이미지(라인 아트, 건축 디자인) 생성에 유용함.
    *   **Depth**:
        *   이미지의 3D 구조를 이해함. 사진에서 무엇이 가깝고 무엇이 먼지 인식하는 것과 같음.
        *   깊이감을 가진 이미지 생성에 도움이 되며, 원근법이 중요한 사실적인 장면에 유용함.
    *   **MLSD**:
        *   이미지에서 직선을 감지함 (예: 건축 사진). 자를 사용하여 스케치에 직선을 그리는 것과 같음.
        *   건물이나 기타 기하학적 형태의 구조를 강조하며, 건축 디자인, 도시 경관 등에 적합함.
    *   **Normal Map**:
        *   표면의 법선(surface normals)을 분석함 (표면이 향하는 방향을 나타내는 벡터). 표면의 질감(울퉁불퉁함, 평평함, 곡선형)을 이해하는 것과 같음.
        *   디테일한 질감을 생성하거나 3D와 같은 이미지의 사실성을 높이는 데 유용함.
    *   **Open Pose**:
        *   신체의 주요 지점(관절 등)을 식별하여 인간의 자세를 감지함. 사람이 서 있거나 움직이는 방식을 보여주기 위해 막대기 그림을 그리는 것과 같음.
        *   사람의 위치와 움직임이 중요한 이미지(액션 샷, 캐릭터 디자인)에 이상적임.
    *   **Scribble**:
        *   사용자가 간단한 스케치나 낙서(scribble)를 그리면 ControlNet이 이를 최종 이미지의 구조로 해석함.
        *   거친 초안을 만들고 AI가 이를 세련된 작품으로 바꾸는 것과 같음.
        *   개념을 빠르게 스케치하고 AI가 세부 사항을 채우도록 하는 데 유용함.
    *   **Segmentation**:
        *   콘텐츠(하늘, 땅, 개체 등)를 기반으로 이미지를 다른 영역이나 세그먼트로 분할함.
        *   각 요소를 분리하기 위해 그림의 다른 영역을 다양한 색상으로 칠하는 것과 같음.
        *   복잡한 환경이나 레이어드 구성을 만들 때와 같이 이미지의 다른 부분을 개별적으로 처리해야 하는 장면에 유용함.
    *   **오류 처리**: 특정 `preprocessor`에서 오류가 발생할 수 있으며, 이 경우 `command window`를 확인하여 오류 정보를 얻고 온라인에서 검색하여 해결할 수 있음 (영상 편집 후 ComfyUI 업데이트로 해결됨).

### 5. 단일 ControlNet을 기존 SDXL 워크플로우에 통합

1.  **SDXL 기본 워크플로우 로드**
    *   `SDXL basic text to image` 워크플로우를 로드함 (에피소드 3에서 다룬 것과 유사하며, `Juggernaut XL SDXL` 모델을 사용함).
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0902.png" width="300" />
    *   프롬프트 노드와 `K Sampler` 노드 사이에 공간을 확보함.
    *   (팁: 새 버전에서는 노드나 필드에 마우스를 올리면 간략한 설명이 표시됨.)
2.  **`Apply ControlNet` 노드 추가**
    *   빈 공간을 더블 클릭하여 `apply control net`을 검색하고 `Apply ControlNet` 노드를 추가함 (ComfyUI 기본 노드).
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0937.png" width="300" />
    *   **연결 변경**:
        *   `CLIP Text Encode (Positive)`의 `conditioning` 출력을 `Apply ControlNet` 노드의 `conditioning` 입력에 연결함.
        *   `Apply ControlNet` 노드의 `conditioning` 출력을 `K Sampler` 노드의 `positive` 입력에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_0954.png" width="300" />
3.  **`Load ControlNet Model` 노드 추가 및 연결**
    *   `Apply ControlNet` 노드의 `control_net` 입력에서 링크를 드래그하여 `Load ControlNet Model` 노드를 선택함.
    *   `control_net_name` 드롭다운에서 이전에 다운로드한 `ControlNet-Union-XL-Promax` 모델을 선택함. (다른 ControlNet 모델이 있다면 이 목록에 나타남.)
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1009.png" width="300" />
4.  **`ControlNet Pre-processor (Art Venture)` 노드 추가 및 연결**
    *   `Apply ControlNet` 노드의 `image` 입력에서 링크를 드래그하여 `ControlNet Pre-processor (Art Venture)` 노드를 추가함 (테스트에 사용했던 노드).
    *   `preprocessor` 드롭다운에서 `canny`를 선택함.
    *   `SD Version`은 `SDXL`, `Resolution`은 `1024`로 설정함.
    *   이 노드의 `image` 출력을 `Apply ControlNet` 노드의 `image` 입력에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1050.png" width="300" />
5.  **`Load Image` 노드 추가 및 연결**
    *   `Load Image` 노드를 추가하고, 이 노드의 `image` 출력을 `ControlNet Pre-processor (Art Venture)` 노드의 `image` 입력에 연결함.
    *   예시 이미지(Warrior 이미지)를 로드함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1106.png" width="300" />
6.  **Pre-processor 결과 미리보기**
    *   `ControlNet Pre-processor (Art Venture)` 노드의 `image` 출력에서 `Preview Image` 노드를 연결하여 Pre-processor의 결과를 확인할 수 있도록 함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1128.png" width="300" />
7.  **워크플로우 실행 및 결과 확인**
    *   초기 프롬프트와 Canny Pre-processor를 사용하여 실행함.
    *   **문제점**: 프롬프트가 `a robot holding a baseball bat`인데, Canny Pre-processor가 원본 워리어 이미지의 검 형태를 강하게 유지하여 야구 방망이를 얻기 어려움.
    *   **해결책 1 (Pre-processor 변경)**: `preprocessor`를 `depth`로 변경함. Depth 맵은 검의 손잡이 형태를 캡처하여 여전히 야구 방망이 생성에 어려움이 있을 수 있음.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1206.png" width="300" />
    *   **해결책 2 (프롬프트 조정)**: 프롬프트를 `a robot holding a sword` 등으로 변경하거나, `open pose`와 같은 Pre-processor를 사용할 수 있음.
    *   `depth` Pre-processor와 `robot holding a sword` 프롬프트를 사용했을 때 멋진 로봇 이미지를 얻음.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1219.png" width="300" />
    *   (팁: `open pose`를 사용하면 포즈를 유지하면서 다른 개체(야구 방망이)를 더 자유롭게 생성할 수 있음.)
    *   **ControlNet Strength 조절의 중요성**:
        *   `Apply ControlNet` 노드에는 `strength` 값이 있음.
        *   `strength`가 `1`에 가까울수록 ControlNet이 결과에 강하게 영향을 미 미치고, 입력 이미지에 가깝게 생성됨.
        *   `strength` 값을 줄이면(예: `0.3`, `0.2`) 원본 이미지의 영향이 줄어들고 AI가 더 많은 변화를 만들 수 있음.
        *   **예시**: 애니메이션 소녀 이미지에 `scribble` Pre-processor를 사용하고 프롬프트 `a cute cartoon bunny`를 입력했을 때, `strength`를 `0.2`로 낮추면 토끼 형태가 더 명확하게 나타남.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1427.png" width="300" />
    *   **이미지 품질의 중요성**:
        *   여성 인물 사진에 Canny를 사용했을 때, 얼굴에 충분한 대비가 없어 세부 정보가 충분히 캡처되지 않는 경우가 발생함.
        *   이미지의 요소가 더 명확하고 대비가 높을수록 Pre-processor가 더 많은 세부 정보를 추출할 수 있음.

### 6. 다중 ControlNet (Stacking) 사용 워크플로우

1.  **다중 ControlNet 노드 추가 및 연결 준비**
    *   `CR Stack`을 검색하여 `CR MultiControlNet Stack` 노드를 추가함 (Comfyroll Studio 커스텀 노드).
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1721.png" width="300" />
    *   이전의 `Apply ControlNet` 노드를 삭제함.
    *   `CR Apply MultiControlNet` 노드를 검색하여 추가함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1543.png" width="300" />
    *   `CR MultiControlNet Stack` 노드의 `control_net_stack` 출력을 `CR Apply MultiControlNet` 노드의 `control_net_stack` 입력에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1548.png" width="300" />
    *   `CLIP Text Encode (Positive)`의 `conditioning` 출력을 `CR Apply MultiControlNet` 노드의 `base_positive` 입력에 연결함.
    *   `CLIP Text Encode (Negative)`의 `conditioning` 출력을 `CR Apply MultiControlNet` 노드의 `base_negative` 입력에 연결함.
    *   `CR Apply MultiControlNet` 노드의 `conditioning` 출력을 `K Sampler` 노드의 `positive` 입력에 연결하고, `negative` 출력을 `K Sampler` 노드의 `negative` 입력에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1604.png" width="300" />
    *   `CR Apply MultiControlNet` 노드의 `switch`를 `on`으로 설정함 (ControlNet을 사용하지 않을 경우 `off`로 설정).
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1608.png" width="300" />
    *   `Load ControlNet Model` 노드는 더 이상 필요 없으므로 삭제함 (스택 노드에서 처리).
2.  **첫 번째 ControlNet Pre-processor 연결**
    *   기존의 `ControlNet Pre-processor (Art Venture)` 노드(예: Canny)의 `image` 출력을 `CR MultiControlNet Stack` 노드의 `image_1` 입력에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1629.png" width="300" />
3.  **두 번째 ControlNet Pre-processor 추가 및 연결**
    *   `ControlNet Pre-processor (Art Venture)` 노드를 복사하여 붙여넣기 함.
    *   동일한 `Load Image` 노드에서 `image` 출력을 이 새 Pre-processor 노드의 `image` 입력에 연결함.
    *   이 새 Pre-processor의 `preprocessor`를 `depth`로 설정함.
    *   이 노드의 `image` 출력을 `CR MultiControlNet Stack` 노드의 `image_2` 입력에 연결함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1638.png" width="300" />
    *   두 Pre-processor 노드 모두 `Preview Image`를 연결하여 결과를 미리 볼 수 있도록 함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1650.png" width="300" />
4.  **`CR MultiControlNet Stack` 노드 설정**
    *   `switch_1`과 `switch_2`를 `on`으로 설정함.
    *   `control_net_1`과 `control_net_2` 드롭다운에서 `ControlNet-Union-XL-Promax` 모델을 선택함.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1728.png" width="300" />
    *   각 ControlNet에 대해 `strength`, `start`, `end` 값을 조정할 수 있음 (ControlNet이 프로세스 후반에 적용되어 덜 엄격하게 제어되도록 조절 가능).
5.  **워크플로우 실행 및 결과 확인**
    *   두 ControlNet(Canny 및 Depth)이 모두 적용되어, 입력 이미지에 더 유사한 결과가 생성됨.
    *   `strength`를 조정하여 더 많은 자유도와 다양성을 얻을 수 있음.
    *   **예시**: 건물 이미지와 `apocalyptic building` 프롬프트를 사용하여 Canny와 Depth를 모두 `strength: 1`로 설정하면, 깊이감과 디테일이 모두 살아있는 결과물을 얻을 수 있음.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1756.png" width="300" />
6.  **저장된 워크플로우 활용 (Discord 제공)**
    *   강의 영상에서 단일 및 다중 ControlNet 워크플로우 저장본을 Discord 채널에서 제공함.
    *   **단일 ControlNet 워크플로우 설명**:
        *   `Load Checkpoint` 노드에서 반드시 SDXL 모델을 선택해야 함 (ControlNet Union은 SDXL 전용).
        *   `Apply ControlNet` 섹션에서 `strength`를 조절함.
        *   `Sampler` 설정은 SDXL 모델에 권장되는 설정을 사용함.
        *   `width`와 `height`를 조정할 수 있음.
        *   `Load Image` 노드에서 이미지를 업로드하고, `preprocessor`, `SDXL 모델`, `resolution`을 선택함.
        *   **이미지 크롭 방지**: ControlNet에 업로드한 이미지와 다른 가로세로 비율(aspect ratio)을 `width` / `height`에 설정하면 이미지가 잘릴 수 있음.
            *   **해결 방법**:
                *   `width`와 `height` 값을 수동으로 조절하여 대략적인 비율을 맞춤.
                *   Photoshop과 같은 외부 프로그램을 사용하여 원본 이미지의 `width`를 조정한 후, Photoshop이 자동으로 계산해주는 `height` 값을 ComfyUI에 입력하면 정확한 비율을 유지할 수 있음.
                <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_1946.png" width="300" />
    *   **다중 ControlNet 워크플로우 설명**:
        *   각 `ControlNet` 스위치를 `on/off`하여 활성화/비활성화함.
        *   여러 `preprocessor`를 선택하여 적용할 수 있음 (예: Canny, Depth, Scribble 등).
        *   **3개 이상의 ControlNet 스태킹**:
            *   `CR MultiControlNet Stack` 노드를 복제하고, 이 노드에 추가 이미지와 Pre-processor를 연결함.
            *   이 두 개의 `CR MultiControlNet Stack` 노드를 서로 연결하여 `CR Apply MultiControlNet` 노드에 최종적으로 연결함 (예: 첫 번째 스택의 `control_net_stack` 출력을 두 번째 스택의 `control_net_stack_in`에 연결한 뒤, 두 번째 스택의 `control_net_stack` 출력을 `CR Apply MultiControlNet`에 연결).
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep09_-_How_to_U_2100.png" width="300" />
        *   결과가 과도하게 처리된 것처럼 보인다면, 특정 `preprocessor`의 `weight` 값을 줄여서 ControlNet의 영향력을 낮출 수 있음.

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
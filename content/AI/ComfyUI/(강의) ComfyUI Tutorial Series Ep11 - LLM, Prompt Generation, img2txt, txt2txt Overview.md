---
title: (강의) ComfyUI Tutorial Series Ep11 - LLM, Prompt Generation, img2txt, txt2txt Overview
---

날짜 : 26.04.13
링크 : [ComfyUI Tutorial Series: Ep11 - LLM, Prompt Generation, img2txt, txt2txt Overview](https://youtu.be/yutYU97Bj7E?si=-EaGYONb_wzjvA1C0)

## 한 줄 요약

- ComfyUI에서 Florence-2를 사용한 이미지 기반 프롬프트 생성과 Serge LLM을 사용한 텍스트 기반 프롬프트 생성을 학습하고, 워크플로우 관리 및 통합 방법을 상세히 설명함.

## 핵심 내용

1.  Florence-2 Vision Language Model을 이용한 이미지 캡셔닝 및 프롬프트 생성 방법.
2.  ComfyUI 워크플로우에 이미지-텍스트 프롬프트 생성을 통합하는 방법.
3.  RG3 Custom Node Pack의 그룹 관리, Fast Toggles, Fast Groups Mutter, Any Switch 노드를 활용한 워크플로우 정리 및 제어 방법.
4.  Serge LLM을 이용한 텍스트 기반 프롬프트 생성 및 워크플로우 통합 방법.
5.  Text Concatenate 노드를 활용하여 Serge LLM의 지시어를 유연하게 구성하는 방법.
6.  LLM 모델 설치, 의존성 해결 및 워크플로우 실행 시 발생할 수 있는 문제 해결 방안.

## 따라한 것 · 실습

1.  **이미지에서 프롬프트 생성 (Florence-2)**
    *   **Florence-2 노드 설치**
        *   ComfyUI `Manager > Custom Nodes Manager`로 이동.
        *   검색창에 `Florence`를 입력.
        *   `ID 269`의 `ke`가 만든 노드를 선택하고 `Install` 클릭.
        *   ComfyUI 업데이트: `Manager > Update All` 클릭 후 업데이트 완료 시 `Restart` 버튼 클릭, `Confirm`하여 ComfyUI 재시작.
        *   Florence-2 종속성 설치:
            *   `Installed Nodes`에서 `Florence` 노드를 찾아 이름을 클릭하여 노드 페이지로 이동.
            *   `Installation` 섹션에서 필요한 종속성(requirements.txt)을 확인.
            *   `ComfyUI\ComfyUI_windows_portable` 폴더로 이동.
            *   주소창에 `CMD`를 입력하고 Enter.
            *   노드 페이지에서 제공된 긴 설치 명령어(`pip install -r ...`)를 복사하여 CMD 창에 붙여넣고 Enter.
            *   설치 완료 후 CMD 창을 닫고, ComfyUI 창도 닫은 후 ComfyUI를 재시작.
            *   참고: `llm` 폴더를 찾을 수 없다는 에러는 첫 워크플로우 실행 시 모델이 자동으로 다운로드되면 사라짐.
    *   **기본 Workflow 구성 (Image to Prompt)**
        *   Workflow를 지우고 새로 시작.
        *   캔버스를 더블 클릭하고 `Florence`를 검색하여 `Florence-2 Run` 노드 추가.
        *   `Load Image` 노드를 추가하고 `image` 출력을 `Florence-2 Run`의 `image` 입력에 연결.
        *   `Florence`를 다시 검색하여 `Download and Load Florence-2 Model` 노드 추가.
        *   `Download and Load Florence-2 Model` 노드의 `model` 출력을 `Florence-2 Run`의 `model` 입력에 연결.
        *   `Show Any` 노드(Comfy Easy Use Pack)를 추가하고 `Florence-2 Run`의 `caption` 출력을 `Show Any`의 `any` 입력에 연결.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_0330.png" width="300" />
        *   `Florence-2 Run` 노드의 `task` 옵션을 `caption` 또는 `detailed caption`으로 변경하여 프롬프트 상세도 조절. (`detailed caption`이 더 상세한 프롬프트 제공).
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_0409.png" width="300" />
        *   `model_name` 옵션에서 `sd3_captioner`, `cog_2.2`, `prompt_gen` 등 다른 Florence 모델을 선택하여 테스트 가능. (첫 실행 시 새 모델 다운로드됨).
    *   **SDXL Workflow에 통합 (Image to Prompt)**
        *   기본 SDXL Workflow를 로드 (예: 에피소드 3의 워크플로우).
        *   `Florence-2 Run`, `Load Image`, `Download and Load Florence-2 Model` 노드를 추가하고 위에서 설명한 대로 연결.
        *   기존 `CLIP Text Encode (Positive)` 노드의 `text` 위젯을 입력으로 전환: `CLIP Text Encode (Positive)` 노드 우클릭 > `Convert widget to input > Convert Text to input` 선택.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_0609.png" width="300" />
        *   `Florence-2 Run`의 `caption` 출력을 `CLIP Text Encode (Positive)`의 `text` 입력에 연결.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_0617.png" width="300" />
        *   `Florence-2 Run` 노드의 `task`를 `detailed caption`으로 설정하고 `Show Any` 노드를 연결하여 생성된 프롬프트를 확인하며 Workflow를 실행.
        *   Flux Dev workflow (에피소드 10)에도 동일하게 통합하여 테스트 가능.
    *   **워크플로우 관리 기능 활용**
        *   **특정 Workflow만 실행 (RG3 Custom Node Pack)**
            *   여러 Florence 모델을 사용하는 워크플로우를 복제하여 여러 개 준비.
            *   특정 워크플로우의 최종 노드(예: `Save Image`)에서 우클릭 > `Q selected output node` 선택 시 해당 워크플로우만 실행됨.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_0914.png" width="300" />
        *   **노드 그룹화 (Grouping)**
            *   원하는 노드들을 선택 > 캔버스 우클릭 > `Add group to selected nodes` 선택.
            *   생성된 그룹을 이동하면 그룹 내 노드 및 그룹이 닿는 노드들이 함께 이동함.
            *   그룹 우클릭 > `Edit Group` > `Title`을 `Florence-2 Base`와 같이 알아보기 쉽게 변경.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_0948.png" width="300" />
        *   **그룹 Fast Toggles (RG3 Custom Node Pack)**
            *   캔버스 우클릭 > `RG3 Comfy` > `Settings`로 이동.
            *   `Show Fast toggles in group headers`를 `Always`로 설정 > `Save`.
            *   각 그룹 헤더에 `Bypass` (화살표 아이콘)와 `Mute` (X 아이콘) 토글 버튼이 생성됨.
            *   `Bypass`: 그룹 내 처리 과정을 건너뛰지만, 데이터 흐름은 유지.
            *   `Mute`: 그룹 전체를 비활성화하여 처리 및 데이터 흐름을 중단.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_1038.png" width="300" />
        *   **Fast Groups Mutter (RG3 Custom Node Pack)**
            *   캔버스 더블 클릭 > `fast groups` 검색 > `Fast Groups Mutter` 노드 추가.
            *   캔버스 내 모든 그룹의 목록과 활성화/비활성화 스위치가 자동으로 표시됨.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_1122.png" width="300" />
            *   각 그룹 이름 옆의 화살표를 클릭하면 해당 그룹으로 화면 이동.
            *   `Fast Groups Mutter` 노드 우클릭 > `Properties Panel` 선택.
            *   `match_colors` 필드에 그룹 색상 이름(예: `Yellow`)을 입력하면 해당 색상의 그룹만 표시됨.
            *   `Color input` 드롭다운에서 사용 가능한 색상 이름을 확인 가능.
            *   `match_colors` 필드를 비워두면 모든 그룹이 표시됨.
        *   **Any Switch (RG3 Custom Node Pack) 활용**
            *   `Florence-2` 그룹의 제목을 `Prompt from Image`로 변경.
            *   `Positive` 노드 추가 (텍스트 입력 필드에 `My Prompt` 입력).
            *   캔버스 더블 클릭 > `any switch` 검색 > `Any Switch` 노드 추가.
            *   `Florence-2 Run` 노드의 `caption` 출력을 `Any Switch`의 `any1` 입력에 연결.
            *   `Positive` 노드의 `STRING` 출력을 `Any Switch`의 `any2` 입력에 연결.
            *   `Any Switch`의 `string` 출력을 `Show Any` 노드에 연결하여 어떤 프롬프트가 선택되는지 확인.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_1307.png" width="300" />
            *   `Prompt from Image` 그룹을 `mute`하면 `My Prompt`가 선택되고, `mute` 해제 시 `Florence-2`가 생성한 프롬프트가 선택됨.
            *   `any switch`는 연결된 입력 중 첫 번째 활성화된 입력을 선택함.
            *   Workflow 통합: Flux Dev workflow에 `Any Switch` 노드를 연결하고, `Any Switch`의 `string` 출력을 `CLIP Text Encode (Positive)` 노드의 `text` 입력에 연결.
            *   생성된 프롬프트를 복사 > `Prompt from Image` 그룹을 `mute` > `Positive` 노드에 복사한 프롬프트를 붙여넣고 수정 후 실행하여 커스텀 프롬프트 사용.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_1523.png" width="300" />

2.  **텍스트에서 프롬프트 생성 (Serge LLM)**
    *   **Serge LLM 노드 설치**
        *   `Manager > Custom Nodes Manager`로 이동.
        *   `Serge`를 검색하여 `ID 97`의 `SergeLLM` 노드 `Install` 클릭.
        *   설치 완료 후 `Restart` 및 `Okay`.
        *   모델 폴더 준비: `ComfyUI\models` 폴더 내에 `llm_gguf`라는 새 폴더 생성.
        *   `mistral` 모델 다운로드: [Hugging Face 링크](https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/tree/main)에서 `mistral` 모델(권장 `Q4` 버전)을 다운로드하여 `llm_gguf` 폴더에 배치.
        *   ComfyUI 재시작.
    *   **기본 Workflow 구성 (Text to Prompt)**
        *   캔버스를 지우고 새로 시작.
        *   캔버스 더블 클릭 > `llm` 검색 > `SergeLLM` 노드 추가.
        *   `Show Any` 노드를 추가하고 `SergeLLM`의 `generated` 출력을 `Show Any`의 `any` 입력에 연결.
        *   `SergeLLM` 노드의 `text` 필드에 프롬프트 지시어(예: `a cute cartoon cat`)를 입력.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_1900.png" width="300" />
        *   실행 시 `model missing` 에러가 발생할 수 있음: `SergeLLM` 노드의 `Refresh` 버튼을 클릭하여 모델 목록을 새로고침.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_1922.png" width="300" />
        *   새로운 프롬프트 결과를 얻기 위해서는 `seed`를 변경하거나 `text` 내용을 수정해야 함. (고정된 시드 사용 시 동일 결과 반복).
    *   **Workflow에 통합 (Text to Prompt)**
        *   Flux workflow를 로드.
        *   `SergeLLM` 노드 추가.
        *   `CLIP Text Encode (Positive)` 노드 우클릭 > `Convert widget to input > Convert Text to input` 선택.
        *   `SergeLLM` 노드의 `generated` 출력을 `CLIP Text Encode (Positive)`의 `text` 입력에 연결.
        *   `SergeLLM` 노드의 `generated` 출력을 `Show Any` 노드에 연결하여 생성된 프롬프트를 확인.
        *   `SergeLLM` 노드의 `text` 필드에 원하는 지시어(예: `a bunny in the forest`)를 입력하고 Workflow를 실행.
        <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_2025.png" width="300" />
    *   **고급 Prompt 생성 (Serge LLM)**
        *   **Instructions 입력으로 변환**
            *   `SergeLLM` 노드 우클릭 > `Convert widget to input > Convert instructions to input` 선택.
            *   `Positive` 노드를 추가하고 `STRING` 출력을 `SergeLLM`의 `instructions` 입력에 연결.
            *   `Positive` 노드 텍스트 필드에 `generate a prompt from`과 같은 지시어 입력.
            *   `SergeLLM` 노드의 `text` 필드에는 실제 프롬프트 주제(예: `a cute cartoon bunny`)를 입력.
        *   **Text Concatenate 노드 활용**
            *   `Text Concatenate` 노드를 추가.
            *   첫 번째 `Positive` 노드(내용: `generate a prompt for`)의 `STRING` 출력을 `Text Concatenate`의 `text_a` 입력에 연결.
            *   `Text Concatenate` 노드의 `delimiter`를 `space`로 변경.
            *   두 번째 `Positive` 노드(내용: `a cute cartoon bunny`)의 `STRING` 출력을 `Text Concatenate`의 `text_b` 입력에 연결.
            *   `Text Concatenate`의 `string` 출력을 `SergeLLM`의 `instructions` 입력에 연결.
            *   `Text Concatenate`의 `string` 출력을 `Show Any` 노드에 연결하여 결합된 지시어를 확인.
            <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_2215.png" width="300" />
        *   참고: 이미지 파일 경로를 `SergeLLM`의 `text` 입력으로 사용해 이미지 설명을 얻으려 시도할 수 있으나, Florence 모델만큼 정확하지 않음.
        *   `SergeLLM`의 `seed`는 `Random`으로 표시되지만 실제로는 고정되어 있으므로, 새로운 결과를 원할 경우 `seed` 값을 수동으로 변경해야 함.

3.  **ChatGPT를 활용한 프롬프트 생성 (Flux)**
    *   Discord의 `pixaroma workflows` 채널에서 Flux용 상세 프롬프트 생성 `formula`를 찾음.
    *   ChatGPT (Mini 버전 등)에 해당 `formula`를 붙여넣고 실행.
    *   생성된 프롬프트를 `Copy Code` 버튼을 클릭하여 복사.
    *   Flux workflow의 `Text Encode` 노드에 복사한 프롬프트를 붙여넣어 사용.
    <img src="/AI/ComfyUI/assets/yt_ComfyUI_Tutorial_Series__Ep11_-_LLM,_Pro_2638.png" width="300" />

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
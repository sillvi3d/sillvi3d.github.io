---
title: ComfyUI 주요 경로를 SSD로 설정하기
---

날짜 : 2026-04-18 
버전 : v3

## 한 줄 요약

외장 SSD에 ComfyUI의 모델·커스텀 노드·워크플로우·입출력 폴더를 통합 관리하여, 여러 PC에서 동일 환경으로 작업할 수 있게 세팅하는 가이드.

- 다른 model 안에 있는 것들은 yaml 설정으로 바로 연결이 되지만
- 커스텀 노드, 워크플로우, 입출력 폴더는 심볼릭 링크로 연결해야 함. 원본 경로의 폴더가 바로가기 아이콘으로 바뀌어야 정상 연결된 것.
    - 이 때 원본 폴더의 내용을 먼저 SSD로 복사 → 그 다음 관리자 권한 CMD에서 링크 명령 실행

---

## 사전 준비물

- 외장 SSD (USB 3.1 Gen2 이상 권장, 용량 1TB~2TB)
- ComfyUI GitHub 클론 설치 버전 (Desktop 버전 아님)
- Windows 11 환경
- 관리자 권한 CMD 사용 가능

---

## 전체 구조 이해

작업이 끝나면 아래와 같은 구조가 된다:

```
[C드라이브] ComfyUI 본체 (엔진)
    └── custom_nodes/              ──→  심볼릭 링크로 SSD 연결
    └── user/default/workflows/    ──→  심볼릭 링크로 SSD 연결
    └── input/                     ──→  심볼릭 링크로 SSD 연결
    └── output/                    ──→  심볼릭 링크로 SSD 연결
    └── models/                    ──→  비워도 됨 (SSD에서 읽음)

[SSD] ComfyUI_SSD (개인화 리소스 전부)
    ├── models/         ← extra_model_paths.yaml로 연결
    ├── custom_nodes/   ← 심볼릭 링크(Junction)로 연결
    ├── workflows/      ← 심볼릭 링크(Junction)로 연결
    ├── input/          ← 심볼릭 링크(Junction)로 연결
    └── output/         ← 심볼릭 링크(Junction)로 연결
```

핵심 원리:

- **모델(checkpoint, LoRA 등)** → `extra_model_paths.yaml` 설정 파일로 SSD 경로를 추가
- **커스텀 노드** → 심볼릭 링크(Junction)로 ComfyUI가 SSD 폴더를 자기 폴더처럼 인식
- **워크플로우** → 심볼릭 링크(Junction)로 ComfyUI Save 시 SSD에 직접 저장
- **입출력 폴더** → 심볼릭 링크(Junction)로 연결. 실행 인자 없이 자동 적용

---

## 설치 방법

### STEP 1. SSD에 폴더 구조 생성

1. SSD를 PC에 연결하고 드라이브 문자를 확인한다 (예: E:)
2. `setup_comfyui_ssd.py` 스크립트를 SSD 아무 곳에나 저장한다
3. CMD를 열고 아래 명령어를 실행한다:

```cmd
python setup_comfyui_ssd.py E
```

![[setup_comfyui_ssd.py]] (E 대신 본인의 SSD 드라이브 문자를 입력)

4. `E:\ComfyUI_SSD\` 아래에 폴더 구조와 설정 파일들이 자동 생성된다

생성되는 폴더 구조:

```
E:\ComfyUI_SSD\
├── models\
│   ├── checkpoints\      # 메인 모델 (SD 1.5, SDXL, Flux 등)
│   ├── loras\            # LoRA 모델
│   ├── vae\              # VAE 모델
│   ├── controlnet\       # ControlNet 모델
│   ├── embeddings\       # 텍스트 임베딩
│   ├── upscale_models\   # 업스케일 모델
│   ├── clip\             # CLIP 모델
│   ├── clip_vision\      # CLIP Vision (IP-Adapter용)
│   ├── ipadapter\        # IP-Adapter 모델
│   ├── sam\              # SAM 모델
│   ├── ultralytics\      # YOLO 등 감지 모델
│   └── inpaint\          # 인페인팅 전용 모델
├── custom_nodes\
├── input\
├── output\
├── workflows\
│   ├── AUTO_자동화\
│   ├── CONV_변환-맵추출\
│   ├── CTL_ControlNet-제어\
│   ├── EDIT_이미지-수정\
│   ├── IMG_이미지-생성\
│   ├── MESH_3D\
│   ├── SEG_세그멘테이션\
│   └── VID_비디오\
└── config\
    ├── extra_model_paths.yaml
    ├── run_comfyui_ssd.bat
    └── link_custom_nodes.bat
```

> **팁:** models 하위 폴더 안에 세부 폴더를 만들어도 ComfyUI가 재귀적으로 인식한다. 예: `checkpoints/SDXL/juggernautXL.safetensors` → 노드에서 `SDXL/juggernautXL.safetensors`로 표시됨

---

### STEP 2. 기존 모델 파일을 SSD로 이동

1. 기존 ComfyUI 경로의 models 폴더를 연다:
    
    ```
    C:\Users\User\Documents\ComfyUI\models\
    ```
    
2. 각 하위 폴더(checkpoints, loras, vae 등)의 **파일들**을 SSD의 대응하는 폴더로 복사한다:
    
    ```
    C:\...\models\checkpoints\*.safetensors  →  E:\ComfyUI_SSD\models\checkpoints\
    C:\...\models\loras\*.safetensors        →  E:\ComfyUI_SSD\models\loras\
    (나머지도 동일)
    ```
    
3. 복사가 끝나면 STEP 3을 먼저 완료하고, SSD 모델이 정상 인식되는지 확인한 뒤에 원본을 삭제한다
    

> **주의:** 복사 완료 + 정상 인식 확인 전까지 원본을 삭제하지 말 것!

---

### STEP 3. 모델 경로 연결 (extra_model_paths.yaml)

1. SSD의 설정 파일을 연다:
    
    ```
    E:\ComfyUI_SSD\config\extra_model_paths.yaml
    ```
    
2. `base_path`의 드라이브 문자가 본인의 SSD 문자와 맞는지 확인한다:
    
    ```yaml
    ssd_models:
        base_path: E:/ComfyUI_SSD/models/
        checkpoints: checkpoints/
        loras: loras/
        vae: vae/
        ...
    ```
    
3. 이 파일을 ComfyUI 루트 폴더에 복사한다:
    
    ```
    E:\ComfyUI_SSD\config\extra_model_paths.yaml
    → C:\Users\User\Documents\ComfyUI\extra_model_paths.yaml
    ```
    
4. ComfyUI를 실행하여 모델 목록에 SSD의 모델이 뜨는지 확인한다
    

> **확인 방법:** Load Checkpoint 노드를 클릭하면 모델 목록에 SSD에 넣은 모델이 보여야 한다.

---

### STEP 4~7. 심볼릭 링크 연결 (커스텀 노드 / 워크플로우 / 입력 / 출력)

4개 폴더 모두 같은 패턴으로 연결한다. **ComfyUI를 종료한 상태에서** 진행할 것.

#### 공통 패턴

모든 심볼릭 링크는 아래 3단계로 동일하다:

1. 기존 폴더 내용을 SSD로 복사 (먼저!)
2. `ren`으로 기존 폴더 이름 변경
3. `mklink /J`로 심볼릭 링크 생성

> **반드시 복사를 먼저 한다.** 순서를 안 지키면 빈 폴더가 연결되어 기존 파일이 전부 사라진 것처럼 보인다.

#### 관리자 권한 CMD를 연다

Windows 검색 → "cmd" 입력 → 우클릭 → **관리자 권한으로 실행**

#### STEP 4. 커스텀 노드

기존 내용을 `E:\ComfyUI_SSD\custom_nodes\`로 복사한 뒤:

```cmd
ren "C:\Users\User\Documents\ComfyUI\custom_nodes" custom_nodes_backup
```

```cmd
mklink /J "C:\Users\User\Documents\ComfyUI\custom_nodes" "E:\ComfyUI_SSD\custom_nodes"
```

#### STEP 5. 워크플로우

기존 내용을 `E:\ComfyUI_SSD\workflows\`로 복사한 뒤:

```cmd
ren "C:\Users\User\Documents\ComfyUI\user\default\workflows" workflows_backup
```

```cmd
mklink /J "C:\Users\User\Documents\ComfyUI\user\default\workflows" "E:\ComfyUI_SSD\workflows"
```

#### STEP 6. 입력 폴더

기존 내용을 `E:\ComfyUI_SSD\input\`으로 복사한 뒤:

```cmd
ren "C:\Users\User\Documents\ComfyUI\input" input_backup
```

```cmd
mklink /J "C:\Users\User\Documents\ComfyUI\input" "E:\ComfyUI_SSD\input"
```

#### STEP 7. 출력 폴더

기존 내용을 `E:\ComfyUI_SSD\output\`으로 복사한 뒤:

```cmd
ren "C:\Users\User\Documents\ComfyUI\output" output_backup
```

```cmd
mklink /J "C:\Users\User\Documents\ComfyUI\output" "E:\ComfyUI_SSD\output"
```

#### 연결 확인 (전체)

각 경로에 대해 아래 명령을 실행하여 확인:

```cmd
fsutil reparsepoint query "C:\Users\User\Documents\ComfyUI\custom_nodes"
fsutil reparsepoint query "C:\Users\User\Documents\ComfyUI\user\default\workflows"
fsutil reparsepoint query "C:\Users\User\Documents\ComfyUI\input"
fsutil reparsepoint query "C:\Users\User\Documents\ComfyUI\output"
```

**성공 기준:**

- `mklink` 실행 시 **"교차점을 만들었습니다"** 메시지
- `fsutil` 실행 시 **인쇄 이름에 SSD 경로**가 표시
- 탐색기에서 해당 폴더 아이콘에 **바로가기 화살표**가 붙어 있음

---

### STEP 8. 최종 확인

1. [ ] ComfyUI 실행
2. [ ] Load Checkpoint 노드에서 SSD의 모델이 목록에 뜨는가
3. [ ] 커스텀 노드가 정상 로딩되는가 (에러 없이 노드 검색 가능)
4. [ ] ComfyUI에서 워크플로우 Save 시 `E:\ComfyUI_SSD\workflows\`에 저장되는가
5. [ ] 이미지 생성 후 출력 파일이 `E:\ComfyUI_SSD\output\`에 저장되는가
6. [ ] ComfyUI Manager에서 새 노드를 설치하면 `E:\ComfyUI_SSD\custom_nodes\`에 들어가는가

모두 확인되면 `custom_nodes_backup`, `workflows_backup`, `input_backup`, `output_backup` 폴더는 삭제해도 된다.

---

## 필수 설정

1. `extra_model_paths.yaml`을 ComfyUI 루트 폴더에 배치 (모델 경로 인식용)
2. `mklink /J`로 심볼릭 링크 생성 — custom_nodes, workflows, input, output 4개 (관리자 권한 필수)

## 추천 설정

- SSD 드라이브 문자를 Windows 디스크 관리에서 고정 할당 (포트마다 문자가 바뀌는 것 방지)
- HF_TOKEN 환경변수를 실행 배치 파일에 등록 (Gated Model 다운로드용)
- models 하위에 용도별 세부 폴더 생성 (예: `checkpoints/SD15/`, `checkpoints/SDXL/`, `loras/style/`)

---

## 새 PC에서 연결할 때

다른 PC에서 SSD를 연결하여 같은 환경을 쓰려면:

### 사전 조건

- [ ] 해당 PC에 ComfyUI GitHub 클론 설치 (본체만 있으면 됨)
- [ ] SSD 드라이브 문자 확인 (예: F:)

### 1. 모델 경로 연결

`E:\ComfyUI_SSD\config\extra_model_paths.yaml`의 `base_path` 드라이브 문자를 새 PC의 SSD 문자로 수정한 뒤, ComfyUI 루트 폴더에 복사한다.

### 2. 심볼릭 링크 생성 (4개)

새 PC에서는 SSD에 이미 파일이 있으므로 복사 단계는 필요 없다. ComfyUI의 기존 빈 폴더만 ren → mklink 하면 된다.

관리자 CMD에서 아래를 실행한다. (경로는 새 PC의 ComfyUI 설치 경로와 SSD 드라이브 문자에 맞게 수정)

**커스텀 노드:**

```cmd
ren "[ComfyUI경로]\custom_nodes" custom_nodes_backup
mklink /J "[ComfyUI경로]\custom_nodes" "[SSD]:\ComfyUI_SSD\custom_nodes"
```

**워크플로우:**

```cmd
ren "[ComfyUI경로]\user\default\workflows" workflows_backup
mklink /J "[ComfyUI경로]\user\default\workflows" "[SSD]:\ComfyUI_SSD\workflows"
```

**입력:**

```cmd
ren "[ComfyUI경로]\input" input_backup
mklink /J "[ComfyUI경로]\input" "[SSD]:\ComfyUI_SSD\input"
```

**출력:**

```cmd
ren "[ComfyUI경로]\output" output_backup
mklink /J "[ComfyUI경로]\output" "[SSD]:\ComfyUI_SSD\output"
```

> `[ComfyUI경로]`와 `[SSD]`는 새 PC 환경에 맞게 바꿀 것. 예: `[ComfyUI경로]` → `D:\ComfyUI`, `[SSD]` → `F`

### 3. pip 의존성 설치

ComfyUI 실행 → ComfyUI Manager → **"Install Missing"** 실행

> 커스텀 노드의 코드는 SSD에서 공유되지만, pip 패키지는 PC마다 Python 환경에 설치해야 한다. "Install Missing"으로 대부분 자동 해결된다.

### 4. 확인

- [ ] 모델 목록 정상
- [ ] 커스텀 노드 정상 로딩
- [ ] 워크플로우 Save 시 SSD에 저장
- [ ] 출력 이미지 SSD에 저장

---

## 문제 발생 시

### 증상: bat 파일 실행 시 글자가 깨지고 에러 발생

- **원인:** bat 파일이 UTF-8로 저장되어 한글이 깨짐
- **해결:** bat 파일을 사용하지 말고, 관리자 CMD를 직접 열어서 명령어를 한 줄씩 복사·붙여넣기로 실행

### 증상: mklink 명령어가 두 줄로 나뉘어 실행됨

- **원인:** CMD에 붙여넣을 때 줄바꿈이 포함됨
- **해결:** 명령어를 반드시 **한 줄로** 복사하여 붙여넣기. 특히 긴 경로가 포함된 명령은 주의

### 증상: mklink 실행 시 "액세스가 거부되었습니다"

- **원인:** 관리자 권한 없이 실행
- **해결:** CMD를 반드시 **관리자 권한으로** 실행. (우클릭 → 관리자 권한으로 실행)

### 증상: backup 폴더가 안 보임

- **원인:** ren 명령이 실행되지 않았거나, 이미 다른 이름으로 변경됨
- **해결:** 탐색기에서 ComfyUI 루트 폴더를 직접 열어 확인. 해당 폴더가 아직 원본이면 그대로 SSD로 복사 후 ren → mklink 재실행

### 증상: fsutil 결과가 "파일이나 디렉터리가 재분석 지점이 아닙니다"

- **원인:** 심볼릭 링크가 생성되지 않음. 그냥 일반 폴더 상태
- **해결:** 해당 폴더를 ren으로 이름 변경 후 mklink /J 재실행

### 증상: 심볼릭 링크 성공했는데 ComfyUI Manager가 원래 경로에 노드를 설치함

- **원인:** 심볼릭 링크 생성 전에 ComfyUI를 실행하여 원본 폴더가 다시 생성됨
- **해결:** ComfyUI 완전 종료 → 원본 폴더 삭제 또는 ren → mklink 재실행

### 증상: SSD를 다른 포트에 꽂았더니 드라이브 문자가 바뀜

- **원인:** Windows가 USB 포트별로 다른 드라이브 문자를 할당
- **해결:** Windows 디스크 관리에서 SSD에 고정 드라이브 문자를 할당하거나, yaml 파일의 경로를 수정. (심볼릭 링크는 드라이브 문자가 바뀌면 끊어지므로 재생성 필요)

### 증상: 커스텀 노드 코드는 있는데 노드가 로딩 안 됨

- **원인:** 해당 노드의 pip 의존성이 현재 PC에 설치되지 않음
- **해결:** ComfyUI Manager → Install Missing 실행. 또는 해당 노드 폴더의 requirements.txt를 수동 설치: `pip install -r requirements.txt`

---

## 성능 참고

|항목|내장 NVMe SSD|외장 SSD (USB 3.2 Gen2)|외장 SSD (USB 3.0)|
|---|---|---|---|
|SDXL 모델 로딩|~3초|~4~5초|~8~12초|
|이미지 저장|즉시|즉시|즉시|
|생성 속도|GPU 의존|GPU 의존|GPU 의존|

- 모델이 VRAM에 올라간 이후의 생성 속도는 SSD 위치와 무관하게 동일
- 차이는 모델 최초 로딩, 모델 전환 시에만 발생
- USB 3.2 Gen2(~1,000MB/s)이면 내장 SSD 대비 체감 차이 미미

---

## 주의 사항

- ComfyUI를 종료한 뒤 SSD를 분리할 것. 모델 로딩 중 분리하면 파일 손상 위험
- SSD 없이 ComfyUI를 실행하면 심볼릭 링크(custom_nodes, workflows, input, output)가 끊어져 에러 발생. 반드시 SSD 연결 상태에서 실행
- extra_model_paths.yaml은 PC마다 복사해야 함 (ComfyUI 루트에 위치해야 인식)
- 심볼릭 링크는 PC마다 새로 생성해야 함 (링크 자체는 해당 PC에 종속)
- SSD 드라이브 문자가 바뀌면 심볼릭 링크가 끊어짐 → 드라이브 문자 고정 할당 권장
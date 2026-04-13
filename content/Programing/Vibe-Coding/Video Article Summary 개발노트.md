---
title: Video Article Summary 개발노트
---

날짜 : 2026-04-13

## 한 줄 설명

- 유튜브 링크 또는 아티클 URL을 넣으면 자동으로 옵시디언 마크다운 강의노트를 생성하는 Python 스크립트(yt_note.py)의 셋업 및 사용 가이드
- GUI를 제공하여 터미널 없이도 URL 입력 → 노트 생성이 가능함

## 용도

- 유튜브 강의 영상의 자막을 추출하여 자동으로 체계적 강의노트 생성
- 웹 아티클의 본문과 이미지를 추출하여 옵시디언 노트로 정리
- 영상의 특정 타임스탬프에서 캡쳐 이미지를 자동 추출하여 노트에 삽입

## 환경

|항목|내용|
|---|---|
|OS|Windows 10/11, macOS (둘 다 동작 확인됨)|
|Python|3.10 이상 (3.13.9에서 테스트)|
|AI API|Google Gemini (무료) 또는 Anthropic Claude (유료, 선택)|
|ffmpeg|캡쳐 이미지 추출용 (없으면 자동으로 경량 모드로 동작)|
|옵시디언|볼트 내부에 스크립트와 결과물 저장|

## 필요 라이브러리

```
py -m pip install youtube-transcript-api yt-dlp google-genai requests beautifulsoup4
```

> ⚠️ Windows에서 `pip`이 직접 안 되면 반드시 `py -m pip`으로 실행할 것. `python`이 아닌 `py`를 사용해야 함 (Windows Store 스텁 문제 회피)

|패키지|역할|
|---|---|
|youtube-transcript-api|유튜브 자막 추출 (다운로드 없이 API로)|
|yt-dlp|유튜브 영상 메타데이터 + 영상 다운로드 (캡쳐용)|
|google-genai|Google Gemini API 호출 (무료)|
|requests|아티클 웹페이지 다운로드|
|beautifulsoup4|아티클 HTML 파싱|
|anthropic|Claude API 호출 (선택, 유료. `py -m pip install anthropic`)|

## 파일 구조

```
obsidian-vault/
├── scripts/
│   └── video article summary/
│       ├── yt_note.py              ← 메인 스크립트
│       └── README_yt_note.md       ← 이 가이드
├── output/                          ← 생성된 노트 저장 위치 (자동 생성됨)
│   ├── (강의) 영상제목.md
│   └── (아티클) 아티클제목.md
└── 99. 이미지 파일들/               ← 캡쳐/아티클 이미지 저장 위치
    ├── yt_영상제목_0345.png         ← 유튜브 캡쳐 (타임스탬프 기반)
    └── art_아티클제목_00.jpg        ← 아티클 본문 이미지
```

> ℹ️ 경로는 하드코딩이 아님. 스크립트가 자기 자신의 위치에서 2단계 상위 폴더를 볼트 루트로 자동 감지함. 어떤 PC, 어떤 드라이브에서든 `scripts/하위폴더/yt_note.py` 구조만 유지하면 동작함.

## 실행 순서

### 0단계 · Python 설치 확인

```powershell
py --version
```

버전 번호가 나오면 OK. `py`가 안 되면 https://www.python.org/downloads/ 에서 설치. **설치 시 "Add python.exe to PATH" 체크박스를 반드시 체크할 것.**

> ⚠️ Windows에서 `python --version`이 버전 없이 `Python`만 출력되면 이것은 진짜 Python이 아니라 Windows Store 스텁임. 이 경우 `py`를 사용해야 함.

---

### 1단계 · 패키지 설치

```powershell
py -m pip install youtube-transcript-api yt-dlp google-genai requests beautifulsoup4
```

macOS인 경우:

```bash
python3 -m pip install youtube-transcript-api yt-dlp google-genai requests beautifulsoup4
```

---

### 2단계 · ffmpeg 설치 (캡쳐 기능용, 선택)

유튜브 영상에서 캡쳐 이미지를 자동 추출하려면 필요함. 없어도 스크립트는 동작하지만 캡쳐 없이 텍스트만 정리됨.

**Windows:**

```powershell
winget install ffmpeg
```

설치 후 **PowerShell을 닫고 새 창으로 열어야** PATH가 반영됨.

**macOS:**

```bash
brew install ffmpeg
```

설치 확인:

```powershell
ffmpeg -version
```

> ⚠️ ffmpeg는 PC마다 따로 설치해야 함. 한 PC에서 설치했다고 다른 PC에서 되는 것이 아님.

---

### 3단계 · Gemini API 키 발급 (무료)

1. https://aistudio.google.com/apikey 접속 (Google 계정 로그인)
2. "Create API Key" 클릭
3. 키 복사 (`AIza...` 형태)

**환경변수 설정:**

PowerShell (Windows):

```powershell
$env:GEMINI_API_KEY = "AIza여기에키붙여넣기"
```

macOS/Linux:

```bash
export GEMINI_API_KEY="AIza여기에키붙여넣기"
```

> ℹ️ 환경변수는 터미널을 닫으면 사라짐. 영구 설정하려면:
> 
> - Windows: `[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIza...", "User")`
> - macOS: `~/.zshrc`에 `export GEMINI_API_KEY="AIza..."` 추가
> 
> 또는 `yt_note.py` 상단의 `GEMINI_API_KEY` 변수에 직접 입력해도 됨.

---

### 4단계 · 스크립트 배치

다운로드받은 `yt_note.py`를 볼트 내부에 배치:

```
{옵시디언 볼트}/scripts/video article summary/yt_note.py
```

> ⚠️ 파일 인코딩이 **UTF-8**이어야 함. Claude에서 다운로드한 파일이 깨져 보이면 VS Code에서 열고 하단 인코딩 표시 클릭 → `Save with Encoding > UTF-8`로 저장.

---

### 5단계 · 실행

**GUI 모드 (권장):**

```powershell
cd "D:\99_Obsidian\obsidian-vault\scripts\video article summary"
py yt_note.py
```

→ 창이 뜨면 URL 입력 후 Generate 클릭

**CLI 모드:**

```powershell
py yt_note.py "https://youtu.be/영상ID"
py yt_note.py "https://example.com/article"
py yt_note.py "https://youtu.be/영상ID" --model claude
py yt_note.py "https://youtu.be/영상ID" --no-capture
```

## 핵심 동작 구조

### 유튜브 영상 처리 흐름

```
유튜브 URL 입력
  → yt-dlp로 메타데이터 추출 (제목, 채널, 길이)
  → youtube-transcript-api로 자막 추출 (한국어 우선 → 영어 → 자동생성)
  → Gemini/Claude API에 자막 전문 + 프롬프트 전송
  → AI가 마크다운 노트 생성 (<!-- CAPTURE [MM:SS] --> 주석 포함)
  → yt-dlp로 영상 임시 다운로드 (최저 화질)
  → ffmpeg로 CAPTURE 타임스탬프 프레임 추출 → PNG 저장
  → 주석을 ![[이미지.png|300]]으로 교체
  → 임시 영상 파일 자동 삭제
  → output/ 폴더에 (강의) 영상제목.md 저장
```

### 아티클 URL 처리 흐름

```
아티클 URL 입력
  → requests로 HTML 다운로드
  → BeautifulSoup으로 제목 + 본문 + 이미지 추출
  → 이미지를 [IMG_N] 플레이스홀더로 치환
  → Gemini/Claude API에 본문 + 프롬프트 전송
  → AI가 마크다운 노트 생성 (플레이스홀더 위치 유지)
  → 이미지 파일 다운로드 (10KB 미만 아이콘 자동 필터)
  → 플레이스홀더를 ![[이미지.png|300]]으로 교체
  → 위치 불명 이미지는 AI 2차 호출로 적절한 위치에 배치
  → output/ 폴더에 (아티클) 제목.md 저장
```

### 경로 자동 감지 원리

```python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))    # scripts/video article summary/
VAULT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # 볼트 루트 (2단계 상위)
OUTPUT_DIR = os.path.join(VAULT_ROOT, "output")
IMAGE_DIR = os.path.join(VAULT_ROOT, "99. 이미지 파일들")
```

이 구조 덕분에 D:, C:, /Users/ 어디든 동일하게 동작함.

## 비용

| AI 모델       | 비용               | 비고                                           |
| ----------- | ---------------- | -------------------------------------------- |
| Gemini (기본) | 무료               | 일 20회 호출 가능<br>부족할시 API(계정) 바꿔가며 사용은 가능      |
| Claude (선택) | 1회당 약 $0.05~0.15 | console.anthropic.com에서 API 키 발급 + 크레딧 구매 필요 |

> ℹ️ Gemini 무료 한도는 영상 길이와 무관함. 50분짜리든 10분짜리든 API 호출 1회. 아티클에서 이미지 위치 배정 시 2차 호출이 추가될 수 있음.

## 프롬프트 커스터마이징

`yt_note.py` 내부의 `build_prompt_youtube()` / `build_prompt_article()` 함수에서 AI 지시사항을 수정할 수 있음.

현재 설정된 주요 규칙:

- 빠짐없이 전체 내용 정리 (요약 아님)
- step by step 조작 순서 기록
- UI 메뉴 경로 표기 (`메뉴 > 하위메뉴`)
- 문체: "-함", "-음", "-임" 서술체 (경어체/반말 금지)
- 캡쳐 위치에 `<!-- CAPTURE [MM:SS] -->` 주석 삽입

변경하고 싶으면 해당 함수 내의 프롬프트 텍스트를 직접 수정하면 됨.

## 제작 과정 메모 (시행착오)

### 잘 된 것

- Gemini 무료 API로 Claude 수준의 정리 품질 확보
- `yt-dlp` + `youtube-transcript-api` 조합으로 영상 다운로드 없이 자막 추출 가능
- tkinter(Python 내장)로 GUI 구현하여 추가 설치 없이 모든 OS에서 동작
- 스크립트 위치 기반 동적 경로 감지로 멀티 PC 환경 대응

### 안 됐던 것 · 해결 방법

| 문제                                                                           | 원인                                      | 해결 방법                                               |
| ---------------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------------- |
| `pip` 명령어 인식 안 됨                                                             | Windows에서 pip이 PATH에 없음                 | `py -m pip install ...`로 실행                         |
| `python --version`이 버전 없이 "Python"만 출력                                       | Windows Store 스텁 (가짜 python)            | `py --version`으로 실행. `py`가 Windows Python Launcher  |
| `AttributeError: 'YouTubeTranscriptApi' has no attribute 'list_transcripts'` | youtube-transcript-api가 v1.x로 메이저 업데이트됨 | `YouTubeTranscriptApi()` 인스턴스 생성 후 `.list()` 호출로 변경 |
| ffmpeg 설치 후 인식 안 됨                                                           | 현재 PowerShell 세션에 PATH 미반영              | PowerShell 닫고 새 창 열기. 안 되면 PC 재부팅                   |
| ffmpeg가 다른 PC에서 안 됨                                                          | ffmpeg는 PC마다 개별 설치 필요                   | 각 PC에서 `winget install ffmpeg` 실행                   |
| `No module named 'yt_dlp'`                                                   | GUI 실행한 PC에 패키지 미설치                     | 해당 PC에서 `py -m pip install ...` 다시 실행               |
| 파일 한국어 깨짐                                                                    | 다운로드 시 UTF-8이 아닌 인코딩으로 저장됨              | VS Code에서 열고 `Save with Encoding > UTF-8`로 저장       |
| 아티클 이미지가 아이콘만 저장됨                                                            | zoom-icon 같은 장식용 img 태그를 본문 이미지로 오인     | URL/alt/class 패턴 필터 + 10KB 미만 파일 자동 삭제              |
| 아티클 이미지 0개 발견                                                                | JS 동적 로딩 사이트에서 img 태그에 src가 없음          | raw HTML 전체에서 정규식으로 이미지 URL 직접 검색하는 fallback 추가     |
| 같은 이미지가 2~3번 중복 저장                                                           | HTML에 같은 이미지가 크기별로 여러 번 등장              | URL 정규화 (크기 접미사/쿼리 파라미터 제거) 후 중복 비교                 |
| fallback 이미지가 노트 하단에만 모임                                                     | 텍스트 내 플레이스홀더 없이 발견된 이미지는 위치 불명          | AI 2차 호출로 노트 내용과 매칭하여 적절한 위치에 자동 삽입                 |
| `D:\` 하드코딩 경로가 다른 PC에서 안 맞음                                                  | 드라이브 문자가 PC마다 다름                        | 스크립트 자기 위치 기반 동적 경로 감지 (`os.path.dirname` 2단계)      |

### 새 환경 셋업 체크리스트

새 PC에서 처음 세팅할 때 순서대로 확인:

```
[ ] Python 설치 확인: py --version
[ ] 패키지 설치: py -m pip install youtube-transcript-api yt-dlp google-genai requests beautifulsoup4
[ ] ffmpeg 설치: winget install ffmpeg (Windows) / brew install ffmpeg (Mac)
[ ] ffmpeg 확인: ffmpeg -version (새 터미널에서)
[ ] Gemini API 키 설정: $env:GEMINI_API_KEY = "AIza..."
[ ] yt_note.py를 scripts/video article summary/ 에 배치
[ ] 인코딩 확인: VS Code에서 열어서 UTF-8인지 확인
[ ] 테스트 실행: py yt_note.py
```

## 개선하고 싶은 것

- 자막이 없는 영상 대응: Whisper STT 연동 (로컬 또는 API)
- 옵시디언 Shell Commands 플러그인 연동하여 옵시디언 내부에서 바로 실행
- 배치 처리: 여러 URL을 한 번에 입력하여 순차 처리

## 변경 이력

|날짜|변경 내용|
|---|---|
|2026-04-13|최초 작성. 경량 모드(자막만) → 풀 모드(캡쳐 포함) → Gemini 무료 전환 → GUI 추가 → 아티클 URL 지원 → 이미지 자동 추출 → 멀티 PC 동적 경로 대응|

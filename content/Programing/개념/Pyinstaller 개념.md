---
title: Pyinstaller 개념
---

날짜: 2026-04-08

##### 한 줄 정의.

- Python 스크립트를 Python 없이도 실행 가능한 단독 실행 파일(`.exe` / `.app`)로 패키징해주는 도구
- 파이썬.py 파일을 exe로 저장

##### 개요

- Python으로 만든 프로그램을 다른 사람에게 배포할 때, 상대방 PC에 Python이 없어도 바로 실행되게 만들어줌
- Python 인터프리터 + 라이브러리 + 스크립트를 하나로 묶어서 독립 실행 파일 생성
- "왜 내 컴퓨터에선 안 되냐"는 환경 문제를 없애줌

##### 핵심 개념

###### 번들링 (Bundling)

스크립트가 의존하는 Python 런타임, 표준 라이브러리, 외부 패키지를 전부 하나로 묶는 과정. 결과물은 Python이 없는 PC에서도 실행됨.

###### --onefile vs --onedir

`--onefile`: 모든 걸 `.exe` 파일 하나에 압축. 배포는 편하지만 실행 시 임시폴더에 압축 해제하므로 첫 실행이 느림.  
`--onedir` (기본값): 폴더째로 묶음. 실행은 빠르지만 폴더 전체를 배포해야 함.

###### --windowed (--noconsole)

GUI 프로그램에서 실행 시 검은 터미널(콘솔) 창이 같이 뜨는 걸 막아줌. tkinter 등 GUI 앱에 필수.

###### spec 파일

첫 빌드 시 자동 생성되는 `프로그램명.spec` 파일. 빌드 설정을 저장해두는 설정 파일로, 반복 빌드 시 이 파일을 수정해서 사용함.

##### 기본 사용법

```bash
# 설치
pip install pyinstaller

# 가장 기본 빌드
pyinstaller --onefile --windowed --name "앱이름" 스크립트.py

# 아이콘 포함
pyinstaller --onefile --windowed --name "앱이름" --icon=icon.ico 스크립트.py

# 빌드 후 dist/ 폴더 안에 exe 생성됨
```

##### 자주 쓰는 명령어 · 옵션

|명령어 · 옵션|설명|
|---|---|
|`--onefile`|단일 `.exe` 파일로 출력|
|`--onedir`|폴더 단위로 출력 (기본값)|
|`--windowed`|콘솔 창 숨김 (GUI 앱 필수)|
|`--name "이름"`|출력 파일명 지정|
|`--icon=파일.ico`|앱 아이콘 지정 (`.ico` 형식)|
|`--add-data "src;dst"`|추가 파일(이미지 등) 포함|
|`--clean`|이전 빌드 캐시 삭제 후 빌드|
|`--noconfirm`|덮어쓰기 확인 없이 바로 빌드|

##### 동작 원리

```
스크립트.py
    ↓
PyInstaller 분석
    ↓  import 추적 → 필요한 모듈 전부 수집
Python 런타임 + 라이브러리 + 스크립트 번들링
    ↓
[ --onefile ]         [ --onedir ]
단일 exe 생성          폴더(dist/앱이름/) 생성
    ↓                      ↓
실행 시 임시폴더에      폴더째로 바로 실행
압축 해제 후 실행
```

빌드 결과물은 `dist/` 폴더에 생기고, 빌드 중간 산출물은 `build/` 폴더에 생김. 배포할 때는 `dist/` 안의 것만 전달하면 됨.

##### 다른 것과의 비교

|항목|PyInstaller|cx_Freeze|Nuitka|
|---|---|---|---|
|사용 난이도|쉬움|보통|어려움|
|단일 파일|지원|미지원|지원|
|실행 속도|보통|보통|빠름 (컴파일)|
|크기|30~100MB|비슷|더 작음|
|인기 / 커뮤니티|매우 많음|적음|보통|

입문용으로는 PyInstaller가 압도적으로 쓰기 편함.

##### 주의사항 · 자주 하는 실수

- **실행 위치 오류** — 터미널에서 `.py` 파일이 있는 폴더로 `cd` 먼저 한 뒤 명령어 실행해야 함
- **파일명 공백·특수문자** — 파일명에 공백 있으면 따옴표로 감싸야 함 (`"md link gen.py"`)
- **파일명 하이픈 vs 언더바** — `md-link-gen.py`와 `md_link_gen.py`는 다른 파일. 명령어에 정확히 일치시켜야 함
- **빌드 OS 고정** — Windows에서 빌드해야 `.exe`, Mac에서 빌드해야 `.app`. 크로스 빌드 안 됨
- **백신 오탐** — PyInstaller로 만든 exe를 백신이 악성코드로 오탐하는 경우 있음. 정상 동작이므로 예외 처리하면 됨
- **용량** — Python 런타임 전체가 포함되므로 단순한 프로그램도 30~50MB는 기본
- **외부 프로그램 미포함** — Ollama 같은 별도 프로그램은 exe 안에 안 들어감. 사용자가 따로 설치해야 함

##### 참고 링크

- [PyInstaller 공식 문서](https://pyinstaller.org/en/stable/)
- [PyInstaller GitHub](https://github.com/pyinstaller/pyinstaller)
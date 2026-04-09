---
title: Pyinstaller exe 패키징 실전가이드
---

날짜 : 2026-04-08

## 한 줄 설명.

- Python 스크립트를 `.exe` 단독 실행 파일로 패키징하는 PyInstaller 실전 사용 가이드
- 딱히 파일 필요없이 터미널에서 패키징을 하는 것임.
	- 다만 이 과정을 bat 파일로 만들어 간단히 실행할수는 있음
## 용도

- Python이 없는 PC에서도 실행 가능한 프로그램 배포할 때
- 만든 툴을 다른 사람에게 넘기거나 다른 PC에서 쓸 때
- 터미널 없이 더블클릭으로 바로 실행되게 만들 때

## 만약 다른 사람이 이 exe를 쓴다면

| 항목          | 필요 여부 | 이유               |
| ----------- | ----- | ---------------- |
| Python      | ❌ 불필요 | exe 안에 이미 포함됨    |
| PyInstaller | ❌ 불필요 | 개발자 도구라 배포 대상 아님 |
| Ollama      | ✅ 필요  | Summary 기능 쓸 때만  |

## 환경

|항목|내용|
|---|---|
|Python 버전|3.13 (3.11 시도했으나 미설치 확인, 3.13으로 최종 성공)|
|OS|Windows 11|
|실행 방법|`python -m PyInstaller --onefile --windowed --name "앱이름" 스크립트.py`|

## 필요 라이브러리

|라이브러리|설치 명령어|용도|
|---|---|---|
|pyinstaller|`pip install pyinstaller`|exe 패키징 도구|

## 파일 구조

```
md-link-gen/
├── md-link-gen.py             ← 소스코드 (개발용)
├── icon.ico                   ← 앱 아이콘 (선택)
├── build.bat                  ← 빌드 자동화 스크립트
├── MD_Link_Gen_개발노트.md     ← 개발 문서
├── build/                     ← 빌드 중간산출물 (삭제 가능)
├── MD Link Gen.spec            ← 빌드 설정 파일 (자동 생성)
└── dist/
    └── MD Link Gen.exe         ← 최종 결과물 (이것만 배포)
```

## 핵심 코드

### 기본 빌드 명령어

```powershell
# pyinstaller 설치
pip install pyinstaller

# 빌드 (스크립트 파일이 있는 폴더에서 실행)
pyinstaller --onefile --windowed --name "MD Link Gen" md-link-gen.py

# 아이콘 포함 빌드
pyinstaller --onefile --windowed --name "MD Link Gen" --icon=icon.ico md-link-gen.py
```

### Python 버전 문제 해결 — 경로 직접 지정 방식 (최종 해결)

`py -3.11` 같은 버전 지정 명령어가 안 먹힐 때, Python 실행 파일 경로를 직접 지정하면 확실하게 동작함.

```powershell
# 1단계 — 설치된 Python 버전 확인
py --list
# 출력 예시:
# -V:3.13 *    Python 3.13 (64-bit)

# 2단계 — Python 설치 경로 확인
ls "C:\Users\사용자명\AppData\Local\Programs\Python\"
# 출력 예시:
# Python313
# Python314

# 3단계 — 해당 경로로 pyinstaller 최신 버전 재설치
& "C:\Users\madei\AppData\Local\Programs\Python\Python313\python.exe" -m pip install pyinstaller --upgrade

# 4단계 — 동일 경로로 빌드
& "C:\Users\madei\AppData\Local\Programs\Python\Python313\python.exe" -m PyInstaller --onefile --windowed --name "MD Link Gen" md-link-gen.py
```

> `py -3.11` 처럼 버전 지정 방식은 py 런처에 등록된 버전만 동작함. 런처에 없는 버전이거나 경로 문제가 있을 땐 위처럼 **python.exe 전체 경로를 직접 지정**하는 게 확실함.

### build.bat (더블클릭으로 빌드 자동화)

```bat
@echo off
cd /d %~dp0
"C:\Users\madei\AppData\Local\Programs\Python\Python313\python.exe" -m PyInstaller --onefile --windowed --name "MD Link Gen" md-link-gen.py
echo 빌드 완료!
pause
```

> `build.bat`은 `md-link-gen.py`와 같은 폴더에 저장. `%~dp0` 덕분에 어디서 실행해도 경로 자동 이동.

- 파일
	![[build.bat]]
## 실행 화면 · 결과

빌드 성공 시 `dist/` 폴더 안에 `MD Link Gen.exe` 생성 (약 30~50MB). 해당 exe 파일 하나만 어디든 옮겨서 단독 실행 가능.

## 제작 과정 메모

### 잘 된 것

- `--onefile` 덕분에 exe 하나만으로 어디서든 실행 가능
- `build.bat` 만들어두니 재빌드가 더블클릭 한 번으로 끝남
- Python 경로 직접 지정 방식으로 버전 문제 해결

### 안 됐던 것 · 해결 방법

|문제|원인|해결|
|---|---|---|
|`Script file does not exist` 오류|터미널 위치가 py 파일 있는 폴더가 아니었음|`cd` 로 해당 폴더 이동 후 명령어 실행|
|파일명 못 찾음 (`md_link_gen.py`)|실제 파일명은 `md-link-gen.py` (하이픈)인데 언더바로 입력|탐색기에서 확장명 표시 켜서 정확한 파일명 확인 후 수정|
|exe 실행 시 `오디날 찾기 실패` DLL 오류|PyInstaller가 오래된 버전이거나 Python과 궁합 문제|python.exe 경로 직접 지정 + `--upgrade` 로 pyinstaller 최신화 후 재빌드|
|`py -3.11` 명령어 안 됨|3.11이 py 런처에 등록되지 않았거나 미설치|`py --list` 로 실제 설치 버전 확인 → 3.13으로 진행|
|`py -3.13` 도 안 됨|py 런처 경유 방식 자체가 불안정|python.exe 전체 경로 직접 지정 (`& "C:\...\Python313\python.exe"`) 으로 해결|
|파일 확장자 안 보임|Windows 기본 설정이 확장명 숨김|탐색기 → 보기 → 표시 → 파일 확장명 체크|

### Claude한테 효과적이었던 프롬프트

- 오류 메시지를 스크린샷으로 찍어서 그대로 보여주니 원인 빠르게 파악
- `py --list`, `ls` 등 현재 상태 확인 명령어 결과를 공유하니 정확한 해결책 나옴

## 개선하고 싶은 것

- [ ] 아이콘 `.ico` 파일 추가해서 빌드
- [ ] 빌드 후 `dist/` 에서 exe 자동으로 상위 폴더로 복사하는 bat 개선
- [ ] 버전 관리 — 빌드할 때마다 날짜 붙여서 보관 (`MD Link Gen_20260408.exe`)

## 참고

- exe는 단독 파일로 어디든 이동 가능. `dist/` 폴더 통째로 옮길 필요 없음
- Summary 기능(Ollama) 포함된 exe는 실행 PC에 Ollama 별도 설치 필요
- 소스 수정 후엔 반드시 재빌드 필요 (exe는 빌드 시점 스냅샷)

## 변경 이력

|날짜|변경 내용|
|---|---|
|2026-04-08|최초 작성 — PyInstaller 설치 및 exe 빌드 성공, 시행착오 정리|
|2026-04-08|Python 버전 문제 해결 과정 추가 (경로 직접 지정 방식)|
---
title: AI 활용을 위한 기초 학습 체크리스트
---

- [ ] 코드 모듈식 관리
## 코드
- [ ] 터미널 사용방법
- [ ] 터미널 대용 프로그램 서치# AI 활용을 위한 기초 학습 체크리스트

비개발자가 Claude Code 및 AI 도구를 효과적으로 쓰기 위해 알아야 할 것들. "직접 코딩하는 능력"이 아니라 "AI가 하는 일을 이해하고 지시할 수 있는 능력"이 목표.

---

## 우선순위 A — 지금 당장 필요

### 터미널 기초

Claude Code는 터미널에서 동작한다. 최소한 이것만 알면 된다.

- [ ] `cd` — 폴더 이동
- [ ] `ls` / `dir` — 파일 목록 보기
- [ ] `pwd` — 현재 경로 확인
- [ ] `mkdir` — 폴더 만들기
- [ ] `cp` / `mv` / `rm` — 복사, 이동, 삭제
- [ ] `cat` / `type` — 파일 내용 보기
- [ ] 절대 경로 vs 상대 경로 차이 (`D:\99_Obsidian` vs `./0_Convention`)
- [ ] PowerShell과 CMD의 차이 (Windows)

### VS Code 기본 사용

터미널을 가장 편하게 쓸 수 있는 도구. Git UI도 내장.

- [ ] VS Code 설치 및 폴더 열기
- [ ] 내장 터미널 열기 (Ctrl+`)
- [ ] 파일 탐색, 검색, 열기
- [ ] VS Code에서 Git 변경사항 확인 (Source Control 패널)
- [ ] VS Code에서 커밋, 푸시, 풀 (버튼 클릭으로)
- [ ] 확장 프로그램 설치 (Python, GitLens 등)

### Git 실전 (지금 알고 있는 것 + 알파)

- [x] clone, commit, push, pull ← 이미 알고 있음
- [x] GitHub 레포 생성, Settings ← 이미 알고 있음
- [x] GitHub Actions 기본 ← 이미 알고 있음
- [ ] `git status` — 지금 뭐가 바뀌었는지 확인
- [ ] `git log --oneline` — 커밋 이력 간단히 보기
- [ ] `git diff` — 뭐가 바뀌었는지 상세히 보기
- [ ] `.gitignore` — 특정 파일/폴더를 Git 추적에서 제외
- [ ] branch 개념 — main 외에 작업용 가지 만들기 (당장은 안 써도 됨)
- [ ] `git stash` — 작업 중인 변경사항 임시 보관

---

## 우선순위 B — Claude Code 쓰면서 자연스럽게 익히기

### 파일 시스템 개념

- [ ] 환경 변수란 무엇인가 (PATH, ANTHROPIC_API_KEY 등)
- [ ] 환경 변수 설정 방법 (Windows: 시스템 설정 / PowerShell `$env:`)
- [ ] `.env` 파일 — API 키 같은 민감 정보를 코드에 안 넣는 방법
- [ ] 파일 권한 개념 (읽기/쓰기/실행)
- [ ] 심볼릭 링크 — 한 파일을 여러 곳에서 참조

### Python 읽기 능력

직접 짜는 게 아니라 Claude가 짠 코드를 읽고 이해하는 수준.

- [ ] 변수, 함수, if/else, for 루프 — 흐름을 읽을 수 있으면 됨
- [ ] `import` — 외부 라이브러리 가져오기
- [ ] `pip install` — 라이브러리 설치
- [ ] `try/except` — 에러 처리 구조
- [ ] `f-string` — `f"Hello {name}"` 같은 문자열 포맷
- [ ] 딕셔너리, 리스트 — `{}`, `[]` 구조 읽기
- [ ] `if __name__ == "__main__":` — 이게 왜 있는지

### 데이터 포맷 읽기

설정 파일을 읽고 수정할 수 있는 수준.

- [ ] JSON — `{"key": "value"}` 구조 이해, 쉼표/따옴표 규칙
- [ ] YAML — 들여쓰기 기반 구조 (GitHub Actions에서 이미 접함)
- [ ] Markdown — 이미 잘 쓰고 있음, 문법 정리 차원에서 복습
- [ ] TOML — 일부 설정 파일에서 사용 (`[section]` 구조)

---

## 우선순위 C — 확장 단계

### API 개념

- [ ] API란 무엇인가 — 프로그램끼리 대화하는 방법
- [ ] REST API 기초 — GET(읽기), POST(보내기) 개념만
- [ ] API 키 — 인증 방식, 왜 노출하면 안 되는지
- [ ] 요청/응답 구조 — JSON으로 주고받는 흐름
- [ ] rate limit — API 호출 제한이 있다는 것

### 패키지 매니저

- [x] pip (Python) ← 이미 사용 중
- [x] npm (Node.js) ← Claude Code 설치 시 사용함
- [ ] pip requirements.txt — 프로젝트 의존성 한 번에 설치
- [ ] 가상 환경 (venv) — 프로젝트별 Python 환경 분리

### 보안 기초

- [ ] SSH 키 — 비밀번호 없이 GitHub 접속 (현재는 HTTPS 사용 중일 가능성)
- [ ] 퍼블릭 레포에 API 키 올리면 안 되는 이유
- [ ] `.gitignore`로 민감 파일 제외하기
- [ ] GitHub Secrets — Actions에서 API 키 안전하게 쓰기 (이미 해봄)
- [ ] 2FA (이중 인증) — GitHub 계정 보안

### 자동화 개념

- [ ] cron / Windows 작업 스케줄러 — 정해진 시간에 스크립트 자동 실행
- [ ] Webhook — 이벤트 발생 시 자동 트리거
- [ ] CI/CD 개념 — 코드 push하면 자동으로 빌드/배포 (GitHub Actions가 이것)

---

## 학습 방법 추천

이 체크리스트를 따로 공부하려고 앉지 않아도 된다. **실제 작업을 하면서 자연스럽게 채워진다.**

지금까지도 그래왔다:

- Git? → 블로그 만들면서 배움
- GitHub Actions? → 레딧 크롤러 만들면서 배움
- pip? → Python 스크립트 만들면서 배움
- JSON? → API 연동하면서 배움

앞으로도 같은 방식으로:

- VS Code? → Claude Code 시작하면서 배움
- 환경 변수? → API 키 설정하면서 배움
- branch? → 코드 수정이 무서울 때 배움

체크리스트는 "다 끝내야 시작할 수 있다"가 아니라 "이런 게 있다는 걸 알아두고, 만나면 당황하지 않기 위한 지도"이다.
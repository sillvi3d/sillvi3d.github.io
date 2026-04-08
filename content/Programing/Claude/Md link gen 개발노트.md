---
title: Md link gen 개발노트
---

날짜 : 2026-04-08
관련 문서: [[Pyinstaller exe 패키징 실전가이드]]

##### 한 줄 설명.

URL을 붙여넣으면 Markdown 링크 형식(`- [제목](URL)`)을 자동 생성하고 클립보드에 복사해주는 데스크탑 도구

##### 용도

- 옵시디언, 틱틱 등 Markdown 기반 앱에 링크를 첨부할 때마다 `- [제목](URL)` 형식을 수동으로 작성하는 번거로움을 해결
- URL만 넣으면 페이지 제목을 자동으로 긁어와서 완성된 링크 문법을 즉시 클립보드에 올려줌
- Summary 버튼으로 해당 페이지의 본문을 로컬 AI(Ollama)가 2~3문장으로 요약해줌

##### 환경

| 항목        | 내용                      |
| --------- | ----------------------- |
| Python 버전 | 3.10 이상                 |
| OS        | Windows / macOS / Linux |
| 실행 방법     | `python md_link_gen.py` |
- 파일: 
	![[MD-link-gen.py]]

##### 필요 라이브러리

| 라이브러리       | 설치 명령어             | 용도                     |
| ----------- | ------------------ | ---------------------- |
| tkinter     | 기본 내장 (별도 설치 불필요)  | GUI                    |
| urllib      | 기본 내장 (별도 설치 불필요)  | HTTP 요청, URL 파싱        |
| html.parser | 기본 내장 (별도 설치 불필요)  | HTML 파싱 (제목·본문 추출)     |
| Ollama ⭐    | https://ollama.com | 로컬 LLM 서버 (Summary 기능) |

> Summary 기능 사용 시 Ollama 설치 및 모델 다운로드 필요
> 
> ```bash
> ollama pull gemma3   # 또는 llama3.2, mistral 등
> ```

##### 파일 구조
- 내가 굳이 알 필요는 없음
	
```
md_link_gen.py   ← 단일 파일로 전체 구성
│
├── TitleParser        HTML 파싱 클래스 (og:title, twitter:title, <title>, 본문 추출)
├── fetch_page()       URL → (제목, 본문, og:description) 반환
│     └── YouTube 감지 시 oEmbed API 우선 사용
├── summarize()        Ollama API 호출 → 2~3줄 요약 반환
├── check_ollama()     Ollama 실행 여부 및 설치 모델 목록 확인
└── App (tk.Tk)        GUI 메인 클래스
      ├── ResultBox    결과 표시 + 복사 버튼 컴포넌트
      ├── _start_gen   Generate 버튼 핸들러
      └── _start_summary  Summary 버튼 핸들러
```

##### 핵심 코드

###### 페이지 제목 추출 (og:title 우선)

```python
class TitleParser(HTMLParser):
    def best_title(self):
        # og:title → twitter:title → <title> 순으로 우선순위
        for candidate in (self.og_title, self.twitter_title, self.tag_title):
            t = candidate.strip()
            if t:
                return _clean_title(t)
        return ""
```

###### YouTube 전용 처리 (oEmbed API)

```python
def _fetch_youtube_title(url: str) -> str:
    api = ("https://www.youtube.com/oembed?url="
           + urllib.parse.quote(url, safe=":/?=&")
           + "&format=json")
    req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("title", "").strip()
```

###### Ollama 요약 호출

```python
def summarize(url, title, body, description, model):
    prompt = (
        "아래 웹페이지 내용을 한국어로 2~3문장으로 핵심만 요약해줘. "
        "불필요한 인사말이나 부연 설명 없이 요약 내용만 출력해.\n\n"
        + "\n\n".join(parts)
    )
    payload = json.dumps({
        "model": model,
        "stream": False,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    # POST → http://localhost:11434/api/chat
```

##### 실행 화면 · 결과

```
🔗 MD Link Gen  for Markdown
✅ Ollama 연결됨  |  모델: gemma3

모델 [ gemma3         ] ← 설치된 모델명 입력

URL [ https://youtu.be/xxxxxx              ] [✕]

[ ⚡ Generate & Copy ]  [ 📝 Summary ]

RESULT
┌─────────────────────────────────────────┐
│ - [영상 제목](https://youtu.be/xxxxxx)   │
└─────────────────────────────────────────┘

SUMMARY
┌─────────────────────────────────────────┐
│ 이 영상은 ...에 대해 설명합니다. ...      │
└─────────────────────────────────────────┘
```
<img src="/Programing/Claude/assets/Pasted_image_20260408110430.png" width="300" />

- Generate 결과 및 Summary 결과 모두 자동으로 클립보드 복사
- 각 박스 우측 `📋 복사` 버튼으로 개별 재복사 가능

##### 제작 과정 메모

###### 잘 된 것

- 외부 라이브러리 없이 Python 기본 내장만으로 GUI + HTTP 요청 + HTML 파싱 전부 구현
- Ollama 로컬 API 연동으로 완전 무료·오프라인 요약 기능 구현
- 스레딩 처리로 네트워크 요청 중 UI 멈춤 없이 동작

###### 안 됐던 것 · 해결 방법

| 문제                       | 원인                              | 해결                                             |
| ------------------------ | ------------------------------- | ---------------------------------------------- |
| YouTube 링크에서 제목 못 가져옴    | YouTube는 JS 렌더링 방식이라 HTML 파싱 불가 | YouTube oEmbed API(`youtube.com/oembed`) 별도 처리 |
| 일반 사이트 제목이 부정확           | `<title>` 태그에 사이트명이 붙어서 나옴      | `og:title` 메타태그 우선 파싱으로 변경                     |
| Summary에 Claude API 키 필요 | Anthropic API는 유료·키 필수          | Ollama 로컬 LLM으로 교체                             |

###### Claude한테 효과적이었던 프롬프트

- 문제 상황을 스크린샷과 함께 보여주니 원인 파악이 빨랐음
- "왜 안 되는지"보다 "이렇게 됐는데 고쳐줘" 식으로 결과 중심으로 요청
- 기능 추가 시 "기존 기능은 그대로 두고 ~만 추가해줘" 명시

##### 개선하고 싶은 것

- [ ] 전역 단축키 등록 (어디서든 앱 호출)
- [ ] 여러 URL 배치 처리
- [ ] 시스템 트레이 상주 (백그라운드 미니 모드)
- [ ] `- [제목](URL)` 외 다른 Markdown 형식 선택 옵션
- [ ] `.exe` / `.app` 패키징 (pyinstaller)

##### 변경 이력

| 날짜         | 변경 내용                                               |
| ---------- | --------------------------------------------------- |
| 2026-04-08 | 최초 작성 — tkinter GUI, 제목 자동 추출, 클립보드 복사              |
| 2026-04-08 | YouTube oEmbed API 처리 추가, og:title 우선 파싱으로 개선       |
| 2026-04-08 | Summary 버튼 추가 (최초 Claude API → Ollama 로컬 LLM으로 교체)  |
| 2026-04-08 | 헤더 문구 변경 `for Obsidian · TickTick` → `for Markdown` |

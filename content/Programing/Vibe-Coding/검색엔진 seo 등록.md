---
title: 검색엔진 seo 등록
---

날짜 : 2026-04-09

## 한 줄 설명.

- Quartz 기반 GitHub Pages 블로그를 Google/Naver 검색 포털에 등록하는 전체 과정
- 특이사항이 있다면 이 작업은 이미 많은 뜯어고침과 개인화가 된.. Quartz 코드 기반으로 수정이 된 것이라 파일을 그대로 써도 호환이 안될 수 있습니다..

## 용도

- 블로그 글이 Google, Naver 검색 결과에 노출되게 하기
- 검색 엔진 크롤러가 블로그를 인식하고 색인할 수 있도록 세팅

## 환경

|항목|내용|
|---|---|
|블로그 엔진|Quartz v4.5.2|
|호스팅|GitHub Pages (sillvi3d.github.io)|
|OS|Windows 11|
|발행 방법|publish.py → Ctrl+Shift+P (Shell Commands)|

## 필요 라이브러리

없음 (기존 publish.py 그대로 사용)

## 파일 구조

```
sillvi3d.github.io/
├── quartz.config.ts              ← enableSPA: false 로 변경
├── quartz/
│   ├── components/
│   │   └── Head.tsx              ← 구글/네이버 메타태그 추가
│   └── static/
│       └── robots.txt            ← 새로 생성
```

## 핵심 코드

###### robots.txt — `sillvi3d.github.io/quartz/static/` 에 새 파일 생성

```
User-agent: *
Allow: /

Sitemap: https://sillvi3d.github.io/sitemap.xml
```
![[robots.txt]]
###### Head.tsx — `<title>` 바로 아래에 두 줄 추가

```tsx
<title>{title}</title>
<meta name="google-site-verification" content="a2lsjTo72JaTNWz3dQ6uZjoMqrOWGmyCdFPiwOEMLUM" />
<meta name="naver-site-verification" content="2097ea480ce8a0de5345f8e56b923d2590f7068f" />
```
![[Head.tsx]]
###### quartz.config.ts — enableSPA 변경

```ts
enableSPA: false,   // 네이버 크롤러가 메타태그를 읽을 수 있도록
```
![[quartz.config.ts]]
## 실행 순서

### 1단계 · robots.txt 만들기

`sillvi3d.github.io/quartz/static/` 폴더 안에 `robots.txt` 파일을 새로 만들고 위의 내용을 붙여넣는다. Ctrl+Shift+P로 발행하면 `sillvi3d.github.io/robots.txt` 로 자동 배포된다. (참고: `public` 폴더는 없고 `static` 폴더가 루트에 배포됨)

---

### 2단계 · Google Search Console 등록

1. https://search.google.com/search-console 접속
2. URL 접두어 방식으로 `https://sillvi3d.github.io` 입력
3. 소유권 확인 방법 → **HTML 태그** 선택
4. `<meta name="google-site-verification" content="...">` 에서 content 값 복사
5. `sillvi3d.github.io/quartz/components/Head.tsx` 열기
6. `<title>` 바로 아래에 메타태그 한 줄 추가
7. Ctrl+Shift+P 발행 → GitHub Actions 초록불 확인 후 **확인** 클릭
8. 소유권 확인 성공 후 좌측 메뉴 → **Sitemaps** → `sitemap.xml` 제출

> ⚠️ HTML 파일 방식은 publish.py가 content 폴더를 초기화할 때 파일이 삭제되므로 사용 불가. 반드시 HTML 태그 방식으로 진행할 것.

---

### 3단계 · Naver Search Advisor 등록

1. https://searchadvisor.naver.com 접속 → 웹마스터 도구
2. `https://sillvi3d.github.io` 사이트 등록
3. 소유권 확인 → **HTML 태그** 선택
4. `<meta name="naver-site-verification" content="...">` 에서 content 값 복사
5. `Head.tsx`에 구글 태그 아래에 네이버 태그도 추가
6. `quartz.config.ts`에서 `enableSPA: false` 로 변경 (네이버 크롤러가 SPA에서 메타태그를 못 읽음)
7. Ctrl+Shift+P 발행 → GitHub Actions 초록불 확인 후 소유 확인 클릭
8. 소유권 확인 성공 후 요청 → **사이트맵 제출** → `https://sillvi3d.github.io/sitemap.xml`
9. 요청 → **RSS 제출** → `https://sillvi3d.github.io/index.xml`

> ℹ️ sitemap.xml과 index.xml(RSS)은 Quartz가 자동 생성하므로 별도 작업 불필요.

---

### 4단계 · 색인 반영 대기

등록을 완료해도 실제 검색 결과에 노출되려면 각 포털의 크롤러가 사이트를 방문해야 한다. 빠르게 하려면 Google Search Console → **URL 검사** → `https://sillvi3d.github.io` → **색인 생성 요청** 을 하면 우선순위로 크롤링된다.

|포털|예상 반영 시간|
|---|---|
|Google|수일 ~ 2주|
|Naver|2주 ~ 4주|

## 제작 과정 메모

### 잘 된 것

- `Head.tsx`에 메타태그 직접 추가하는 방식으로 구글/네이버 소유권 확인 성공
- `robots.txt`를 `quartz/static/` 폴더에 넣으면 루트에 자동 배포됨
- `sitemap.xml`, `index.xml` 은 Quartz가 자동 생성

### 안 됐던 것 · 해결 방법

| 문제                     | 원인                                    | 해결 방법                                          |
| ---------------------- | ------------------------------------- | ---------------------------------------------- |
| `robots.txt` 404       | `quartz/public/` 폴더가 없음               | `quartz/static/` 폴더에 넣어야 함                     |
| HTML 파일 소유권 확인 실패      | `publish.py`가 content 초기화 시 파일 삭제     | HTML 태그 방식으로 변경                                |
| 네이버 소유권 확인 실패          | `enableSPA: true` 상태에서 크롤러가 메타태그 못 읽음 | `enableSPA: false` 로 변경 후 재배포                  |
| 빌드 실패                  | `Header.tsx`에 `Head.tsx` 내용을 실수로 붙여넣음 | 두 파일 각각 올바른 내용으로 복구                            |
| `git pull --rebase` 오류 | unstaged changes 충돌                   | `publish.py`에 `git stash` / `git stash pop` 추가 |
- 소소한 이슈 - head, header 구분을 잘하자.

|파일|역할|
|---|---|
|`Head.tsx`|HTML `<head>` 태그 → 메타태그, SEO, 폰트 등|
|`Header.tsx`|블로그 상단 UI → 로고, 제목 등 화면에 보이는 헤더|

## Claude한테 효과적이었던 프롬프트

- 파일 전체를 업로드해서 "이 파일 수정해줘" 방식이 효과적
- 에러 메시지 스크린샷을 그대로 보여주면 원인 빠르게 파악 가능

## 개선하고 싶은 것

- 각 글 frontmatter에 `description` 추가해서 검색결과 노출 품질 높이기

## 변경 이력

|날짜|변경 내용|
|---|---|
|2026-04-09|최초 작성 / Google + Naver SEO 등록 완료|

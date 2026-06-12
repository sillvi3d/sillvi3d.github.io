import os, requests, time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# ── 설정 ──────────────────────────────────────────
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (compatible; blender-digest-bot/1.0)"}
VAULT_BASE   = "5_Trend/Blender"
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

# r/blender — flair 기반 크롤링
BLENDER_FLAIRS = [
    "Critique my work",
    "Original content showcase",
    "Discussion",
    "Free tools & Assets",
    "Need help!",
]
FLAIR_EMOJI = {
    "Critique my work"          : "🎨",
    "Original content showcase" : "✨",
    "Discussion"                : "💬",
    "Free tools & Assets"       : "🛠️",
    "Need help!"                : "🆘",
}
FLAIR_LIMIT = {
    "Critique my work"          : 3,
    "Original content showcase" : 5,
    "Discussion"                : 3,
    "Free tools & Assets"       : 3,
    "Need help!"                : 3,
}

# r/blenderhelp — hot 크롤링
PINNED_KEYWORDS = [
    "please read", "read before", "read this before",
    "don't get banned", "do not post", "announcement",
    "rules", "welcome to", "community highlight", "mod post",
]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")
VAULT_PATH = f"{VAULT_BASE}/{year_month}"
# ─────────────────────────────────────────────────


def sanitize(text: str) -> str:
    return text.replace('"', "'").replace('\\', '').replace('\n', ' ').strip()


def llm(prompt: str) -> str:
    for attempt in range(5):
        time.sleep(3)
        try:
            res = requests.post(
                "https://models.inference.ai.azure.com/chat/completions",
                headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"},
                json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
                timeout=60,
            )
            if res.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  429 Too Many Requests — {wait}초 대기 후 재시도 ({attempt+1}/5)")
                time.sleep(wait)
                continue
            res.raise_for_status()
            data = res.json()
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return f"_요약 실패: {str(data)[:200]}_"
        except Exception as e:
            if attempt < 4:
                time.sleep(15)
            else:
                return f"_요약 실패: {str(e)[:100]}_"
    return "_요약 실패: 재시도 한도 초과_"


def is_pinned(title: str) -> bool:
    return any(kw in title.lower() for kw in PINNED_KEYWORDS)


def _fetch_rss(url: str) -> requests.Response:
    """RSS URL을 가져오되, 429 시 재시도."""
    for attempt in range(5):
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 429:
            wait = 30 * (attempt + 1)
            print(f"  429 Too Many Requests — {wait}초 대기 후 재시도 ({attempt+1}/5)")
            time.sleep(wait)
            continue
        res.raise_for_status()
        return res
    return None


# ── r/blender flair 크롤링 ────────────────────────
def fetch_blender_flair(flair: str, limit: int = 10) -> list[dict]:
    url = (
        f"https://www.reddit.com/r/blender/search.rss"
        f"?q=flair%3A%22{flair.replace(' ', '+').replace('&', '%26').replace('!', '%21')}%22"
        f"&restrict_sr=1&sort=new&limit={limit}"
    )
    res = _fetch_rss(url)
    if res is None:
        print(f"  ⚠️ [r/blender {flair}] 5회 재시도 후에도 429 — 빈 결과 반환")
        return []
    ns   = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(res.text)
    posts = []
    for e in root.findall("atom:entry", ns):
        link = e.find("atom:link", ns)
        posts.append({
            "title"  : sanitize(e.findtext("atom:title", "", ns)),
            "url"    : link.attrib.get("href", "") if link is not None else "",
            "content": sanitize(e.findtext("atom:content", "", ns)[:400]),
        })
    return posts[:FLAIR_LIMIT[flair]]


# ── r/blenderhelp hot 크롤링 ─────────────────────
def fetch_blenderhelp(limit: int = 20) -> list[dict]:
    url = f"https://www.reddit.com/r/blenderhelp/hot.rss?limit={limit}"
    res = _fetch_rss(url)
    if res is None:
        print(f"  ⚠️ [r/blenderhelp] 5회 재시도 후에도 429 — 빈 결과 반환")
        return []
    ns   = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(res.text)
    posts = []
    for e in root.findall("atom:entry", ns):
        link    = e.find("atom:link", ns)
        title   = sanitize(e.findtext("atom:title", "", ns))
        content = sanitize(e.findtext("atom:content", "", ns))
        if is_pinned(title):
            print(f"    [SKIP 공지] {title[:50]}")
            continue
        solved = "solved" in title.lower() or "solved" in content.lower()
        posts.append({
            "title"  : title,
            "url"    : link.attrib.get("href", "") if link is not None else "",
            "content": content[:400],
            "solved" : solved,
        })
        if len(posts) >= 15:
            break
    return posts


# ── 요약 함수 ────────────────────────────────────
def summarize_flair(flair: str, posts: list) -> str:
    if not posts:
        return "_해당 플레어의 글이 없습니다._"
    posts_txt = "\n\n".join(
        f"[{i+1}] {p['title']}\nURL: {p['url']}\n내용: {p['content'] or '(이미지/링크 글)'}"
        for i, p in enumerate(posts)
    )
    limit = FLAIR_LIMIT[flair]
    return llm(f"""Reddit r/blender [{flair}] 최근 글 목록:

{posts_txt}

한국어로 정리해주세요:
1. **주요 트렌드** (2~3줄)
2. **주목할 만한 글** (상위 {limit}개, 한 줄 소개 + URL)
3. **오늘의 키워드** (#태그 형식)""")


def summarize_help(posts: list) -> str:
    if not posts:
        return "_오늘 수집된 글이 없습니다._"
    posts_txt = "\n\n".join(
        f"[{i+1}] {'[Solved]' if p['solved'] else '[Unsolved]'} {p['title']}\n"
        f"URL: {p['url']}\n내용: {p['content'] or '(링크 글)'}"
        for i, p in enumerate(posts)
    )
    return llm(f"""아래는 Reddit r/blenderhelp의 오늘 HOT 글 목록입니다.

{posts_txt}

한국어로 정리해주세요:

### 🔥 주요 이슈
* (전체 트렌드 1~3줄)

### 🟠 HOT 질문 Top 5
각 글에 대해:
**N. 🟢 Solved / 🔴 Unsolved — [제목](URL)**
> 한두 줄 요약

### 💡 키워드
#키워드1 #키워드2 #키워드3""")


# ── DAILY ─────────────────────────────────────────
def run_daily():
    os.makedirs(VAULT_PATH, exist_ok=True)

    # ── Part 1: r/blender (flair) ──
    flair_data = {}
    for i, flair in enumerate(BLENDER_FLAIRS):
        if i > 0:
            print("  ⏳ rate limit 방지 10초 대기...")
            time.sleep(10)
        print(f"[r/blender {flair}] 크롤링 중...")
        posts = fetch_blender_flair(flair)
        print(f"  → {len(posts)}개 수집")
        flair_data[flair] = (summarize_flair(flair, posts), posts)

    # ── Part 2: r/blenderhelp (hot) ──
    print("  ⏳ rate limit 방지 10초 대기...")
    time.sleep(10)
    print("[r/blenderhelp] 크롤링 중...")
    help_posts = fetch_blenderhelp()
    print(f"  → {len(help_posts)}개 수집")
    help_summary = summarize_help(help_posts)

    # ── 마크다운 빌드 ──
    md = build_daily_md(flair_data, help_posts, help_summary)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 블렌더 데일리 저장: {path}")


def build_daily_md(flair_data: dict, help_posts: list, help_summary: str) -> str:
    lines = [
        "---",
        f"title: Blender Daily — {today_str}",
        f"date: {today_str}",
        "tags: [blender, 3d, reddit, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        "",
        "# r/blender",
        "",
    ]
    for flair, (summary, posts) in flair_data.items():
        emoji = FLAIR_EMOJI[flair]
        lines += [
            f"## {emoji} {flair}",
            f"_수집된 글: {len(posts)}개_",
            "",
            summary,
            "",
            "---",
            "",
        ]
    lines += [
        "# r/blenderhelp",
        "",
        f"_수집된 글: {len(help_posts)}개_",
        "",
        help_summary,
    ]
    return "\n".join(lines)


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"
    contents   = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 블렌더 위클리: 데일리 파일 없음")
        return
    print(f"[Blender Weekly {week_label}] 요약 중...")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(f"Blender Weekly — {week_label}", "[blender, 3d, reddit, weekly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 블렌더 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"
    contents    = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 블렌더 먼슬리: 데일리 파일 없음")
        return
    print(f"[Blender Monthly {month_label}] 요약 중...")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(f"Blender Monthly — {month_label}", "[blender, 3d, reddit, monthly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 블렌더 먼슬리 저장: {path}")


# ── 공통 유틸 ─────────────────────────────────────
def read_daily_files(start: datetime, end: datetime) -> str:
    contents, cur = [], start
    while cur <= end:
        ds = cur.strftime("%Y-%m-%d")
        ym = cur.strftime("%Y_%m")
        p  = f"{VAULT_BASE}/{ym}/{ds}.md"
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                contents.append(f"=== {ds} ===\n{f.read()}")
        cur += timedelta(days=1)
    return "\n\n".join(contents)


def summarize_period(contents: str, period: str, date_range: str) -> str:
    return llm(f"""아래는 Blender Reddit {period} 데일리 요약 모음입니다 ({date_range}).
r/blender와 r/blenderhelp 내용이 모두 포함되어 있습니다.

{contents[:8000]}

다음 형식으로 한국어 정리:

## 트렌드 3줄 요약
* (트렌드 1)
* (트렌드 2)
* (트렌드 3)

---

# r/blender

## 🎨 Critique my work
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## ✨ Original content showcase
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 5
* 제목 — URL
### 3. {period} 키워드

---

## 💬 Discussion
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 🛠️ Free tools & Assets
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 🆘 Need help!
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드

---

# r/blenderhelp

## 🟠 가장 많이 등장한 문제 Top 5
### N. 🟢/🔴 제목
> 문제 요약 및 해결 여부

### {period} 키워드
#키워드1 #키워드2 #키워드3""")


def build_period_md(title: str, tags: str, date_range: str, summary: str) -> str:
    return "\n".join([
        "---",
        f"title: {title}",
        f"date: {today_str}",
        f"tags: {tags}",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST ({date_range})",
        "",
        summary,
    ])


# ── 메인 ──────────────────────────────────────────
def main():
    run_daily()
    if now_kst.weekday() == 6:
        print("\n[일요일] 블렌더 위클리 실행")
        run_weekly()
    if now_kst.day == 28:
        print("\n[28일] 블렌더 먼슬리 실행")
        run_monthly()


if __name__ == "__main__":
    main()

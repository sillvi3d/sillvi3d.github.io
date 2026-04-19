import os, requests, time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# ── 설정 ──────────────────────────────────────────
SUBREDDITS = {
    "news"      : {"emoji": "📰", "label": "r/news (미국)"},
    "worldnews" : {"emoji": "🌐", "label": "r/worldnews (국제)"},
    "economy"   : {"emoji": "💰", "label": "r/economy (경제)"},
}
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (compatible; world-news-digest-bot/1.0)"}
VAULT_BASE   = "0_Blog/AI/Trend/News"
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")
VAULT_PATH = f"{VAULT_BASE}/{year_month}"
# ─────────────────────────────────────────────────


def sanitize(text: str) -> str:
    return text.replace('"', "'").replace('\\', '').replace('\n', ' ').strip()


def llm(prompt: str) -> str:
    time.sleep(3)
    res = requests.post(
        "https://models.inference.ai.azure.com/chat/completions",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"},
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
        timeout=60,
    )
    res.raise_for_status()
    data = res.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"_요약 실패: {str(data)[:200]}_"


def fetch_posts(subreddit: str, limit: int = 10) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/top.rss?t=day&limit={limit}"
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    ns   = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(res.text)
    posts = []
    for e in root.findall("atom:entry", ns):
        link = e.find("atom:link", ns)
        posts.append({
            "title"  : sanitize(e.findtext("atom:title", "", ns)),
            "url"    : link.attrib.get("href", "") if link is not None else "",
            "content": sanitize(e.findtext("atom:content", "", ns)[:300]),
        })
    return posts


def summarize_news(sr: str, info: dict, posts: list) -> str:
    if not posts:
        return "_오늘 수집된 글이 없습니다._"
    posts_txt = "\n\n".join(
        f"[{i+1}] {p['title']}\nURL: {p['url']}\n내용: {p['content'] or '(링크 글)'}"
        for i, p in enumerate(posts)
    )

    if sr == "worldnews":
        extra = """
### 🔥 지역별 주요 이슈
각 글을 지역별로 분류해서 정리해주세요:
* 🇺🇸 미국: ~~
* 🇨🇳 중국: ~~
* 🇷🇺 러시아: ~~
* 🇪🇺 유럽: ~~
* 기타: ~~
"""
    elif sr == "economy":
        extra = """
### 📊 오늘의 경제 시그널
금리, 물가, 시장 관련 핵심 내용을 1~2줄로 요약해주세요.
"""
    else:
        extra = ""

    return llm(f"""Reddit {info['label']} 오늘의 TOP 글 목록:

{posts_txt}
{extra}
한국어로 정리해주세요:

### 🏆 Top 3 인기글
* **[제목](URL)** — 한줄 설명 (3개)

### 💡 오늘의 키워드
#키워드1 #키워드2 #키워드3""")


def summarize_overall(data: dict) -> str:
    titles = []
    for sr, d in data.items():
        label = SUBREDDITS[sr]['label']
        for p in d["posts"][:3]:
            titles.append(f"[{label}] {p['title']}")
    combined = "\n".join(titles)
    return llm(f"다음 뉴스 제목들을 보고 오늘의 핵심 이슈 3줄을 한국어로 요약해주세요. 각 줄은 *로 시작:\n\n{combined}")


def build_daily_md(data: dict, overall: str) -> str:
    lines = [
        "---",
        f"title: World News Daily — {today_str}",
        f"date: {today_str}",
        "tags: [news, world, economy, reddit, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        "",
        "## 🌍 오늘의 세계 3줄 요약",
        "",
        overall,
        "",
        "---",
        "",
    ]
    for sr, info in SUBREDDITS.items():
        d = data[sr]
        lines += [
            f"## {info['emoji']} {info['label']}",
            f"_수집된 글: {len(d['posts'])}개_",
            "",
            d["summary"],
            "",
            "---",
            "",
        ]
    return "\n".join(lines)


# ── DAILY ─────────────────────────────────────────
def run_daily():
    os.makedirs(VAULT_PATH, exist_ok=True)
    data = {}
    for sr, info in SUBREDDITS.items():
        print(f"[{info['label']}] 크롤링 중...")
        posts = fetch_posts(sr)
        print(f"  → {len(posts)}개 수집")
        data[sr] = {"posts": posts, "summary": summarize_news(sr, info, posts)}
    overall = summarize_overall(data)
    md   = build_daily_md(data, overall)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 월드뉴스 데일리 저장: {path}")


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"
    contents   = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 월드뉴스 위클리: 데일리 파일 없음")
        return
    print(f"[World News Weekly {week_label}] 요약 중...")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(f"World News Weekly — {week_label}", "[news, world, economy, reddit, weekly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 월드뉴스 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"
    contents    = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 월드뉴스 먼슬리: 데일리 파일 없음")
        return
    print(f"[World News Monthly {month_label}] 요약 중...")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(f"World News Monthly — {month_label}", "[news, world, economy, reddit, monthly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 월드뉴스 먼슬리 저장: {path}")


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
    return llm(f"""아래는 뉴스/경제 Reddit {period} 데일리 요약 모음입니다 ({date_range}).

{contents[:8000]}

다음 형식으로 한국어 정리:

## 🌍 트렌드 3줄 요약
* (트렌드 1)
* (트렌드 2)
* (트렌드 3)

---

## 📰 r/news (미국)
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 🌐 r/worldnews (국제)
### 1. 지역별 주요 이슈
* 🇺🇸 미국: ~~
* 🇨🇳 중국: ~~
* 기타: ~~
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 💰 r/economy (경제)
### 1. 주요 경제 시그널
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드""")


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
        print("\n[일요일] 월드뉴스 위클리 실행")
        run_weekly()
    if now_kst.day == 28:
        print("\n[28일] 월드뉴스 먼슬리 실행")
        run_monthly()


if __name__ == "__main__":
    main()
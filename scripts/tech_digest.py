import os, requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# ── 설정 ──────────────────────────────────────────
SUBREDDITS   = {
    "technology": {"emoji": "🌐", "label": "r/technology"},
    "claude"    : {"emoji": "🤖", "label": "r/claude"},
}
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (compatible; tech-digest-bot/1.0)"}
VAULT_BASE   = "0_Blog/AI/Trend/AI_Tech"
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")
VAULT_PATH = f"{VAULT_BASE}/{year_month}"
# ─────────────────────────────────────────────────


def llm(prompt: str) -> str:
    res = requests.post(
        "https://models.inference.ai.azure.com/chat/completions",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"},
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
        timeout=60,
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def fetch_posts(subreddit: str, mode: str = "top", limit: int = 15) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/{mode}.rss?t=day&limit={limit}"
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    ns   = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(res.text)
    posts = []
    for e in root.findall("atom:entry", ns):
        link = e.find("atom:link", ns)
        posts.append({
            "title"  : e.findtext("atom:title", "", ns),
            "url"    : link.attrib.get("href", "") if link is not None else "",
            "content": e.findtext("atom:content", "", ns)[:300],
        })
    return posts


# ── DAILY ─────────────────────────────────────────
def run_daily():
    os.makedirs(VAULT_PATH, exist_ok=True)
    data = {}
    for sr, info in SUBREDDITS.items():
        print(f"[{info['label']}] 크롤링 중...")
        posts = fetch_posts(sr)
        print(f"  → {len(posts)}개 수집")
        data[sr] = {"posts": posts, "summary": summarize_daily(sr, info, posts)}

    overall = summarize_overall(data)
    md   = build_daily_md(data, overall)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 테크 데일리 저장: {path}")


def summarize_daily(sr: str, info: dict, posts: list) -> str:
    if not posts:
        return "_오늘 수집된 글이 없습니다._"
    posts_txt = "\n\n".join(
        f"[{i+1}] {p['title']}\nURL: {p['url']}\n내용: {p['content'] or '(링크 글)'}"
        for i, p in enumerate(posts)
    )
    return llm(f"""Reddit {info['label']} 오늘의 TOP 글 목록:

{posts_txt}

한국어로 정리해주세요:

### 🏆 Top 3 인기글
* **[제목](URL)** — 한줄 설명 (3개)

### 💡 오늘의 키워드
#키워드1 #키워드2 #키워드3""")


def summarize_overall(data: dict) -> str:
    combined = "\n\n".join(
        f"[{SUBREDDITS[sr]['label']}]\n" +
        "\n".join(f"- {p['title']}" for p in d["posts"][:5])
        for sr, d in data.items()
    )
    return llm(f"""오늘의 테크/AI Reddit 주요 글 목록:

{combined}

전체를 아우르는 핵심 이슈 3줄 요약:
* (이슈 1)
* (이슈 2)
* (이슈 3)""")


def build_daily_md(data: dict, overall: str) -> str:
    lines = [
        "---",
        f"title: Tech Reddit Daily — {today_str}",
        f"date: {today_str}",
        "tags: [tech, ai, reddit, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        "",
        "## 🔥 오늘의 TOP 이슈",
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


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"
    contents   = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 테크 위클리: 데일리 파일 없음")
        return
    print(f"[Tech Weekly {week_label}] 요약 중...")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(f"Tech Reddit Weekly — {week_label}", "[tech, ai, reddit, weekly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 테크 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"
    contents    = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 테크 먼슬리: 데일리 파일 없음")
        return
    print(f"[Tech Monthly {month_label}] 요약 중...")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(f"Tech Reddit Monthly — {month_label}", "[tech, ai, reddit, monthly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 테크 먼슬리 저장: {path}")


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
    return llm(f"""아래는 Tech/AI Reddit {period} 데일리 요약 모음입니다 ({date_range}).

{contents[:8000]}

다음 형식으로 한국어 정리:

## 🔥 트렌드 3줄 요약
* (트렌드 1)
* (트렌드 2)
* (트렌드 3)

---

## 🌐 r/technology
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드
#키워드

---

## 🤖 r/claude
### 1. 주요 트렌드 요약
### 2. 가장 주목받은 Top 3
* 제목 — URL
### 3. {period} 키워드
#키워드""")


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
        print("\n[일요일] 테크 위클리 실행")
        run_weekly()
    if now_kst.day == 28:
        print("\n[28일] 테크 먼슬리 실행")
        run_monthly()


if __name__ == "__main__":
    main()

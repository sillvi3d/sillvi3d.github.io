import os, requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# ── 설정 ──────────────────────────────────────────
SUBREDDIT    = "blenderhelp"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (compatible; blender-digest-bot/1.0)"}
VAULT_BASE   = "0_Blog/3D/Blender_Help"
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")
VAULT_PATH = f"{VAULT_BASE}/{year_month}"

PINNED_KEYWORDS = [
    "please read", "read before", "read this before",
    "don't get banned", "do not post", "announcement",
    "rules", "welcome to", "community highlight", "mod post",
]
# ─────────────────────────────────────────────────


def sanitize(text: str) -> str:
    return text.replace('"', "'").replace('\\', '').replace('\n', ' ').strip()


def llm(prompt: str) -> str:
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


def is_pinned(title: str) -> bool:
    return any(kw in title.lower() for kw in PINNED_KEYWORDS)


def fetch_posts(limit: int = 20) -> list[dict]:
    url = f"https://www.reddit.com/r/{SUBREDDIT}/hot.rss?limit={limit}"
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
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


# ── DAILY ─────────────────────────────────────────
def run_daily():
    os.makedirs(VAULT_PATH, exist_ok=True)
    print(f"[r/blenderhelp] 크롤링 중...")
    posts = fetch_posts()
    print(f"  → {len(posts)}개 수집")
    summary = summarize_daily(posts)
    md   = build_daily_md(posts, summary)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 블렌더헬프 데일리 저장: {path}")


def summarize_daily(posts: list) -> str:
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

## 🔥 오늘의 주요 이슈
* (전체 트렌드 1)
* (전체 트렌드 2)
* (전체 트렌드 3)

---

## 🟠 오늘의 HOT 질문 Top 5
각 글에 대해 다음 형식으로:

### N. 🟢 Solved 또는 🔴 Unsolved
**[제목](URL)**
> 한두 줄 내용 요약

---

## 💡 오늘의 키워드
#키워드1 #키워드2 #키워드3""")


def build_daily_md(posts: list, summary: str) -> str:
    return "\n".join([
        "---",
        f"title: Blender Help Daily — {today_str}",
        f"date: {today_str}",
        "tags: [blender, 3d, reddit, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        f"_수집된 글: {len(posts)}개_",
        "",
        summary,
    ])


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"
    contents   = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 블렌더헬프 위클리: 데일리 파일 없음")
        return
    print(f"[BlenderHelp Weekly {week_label}] 요약 중...")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(f"Blender Help Weekly — {week_label}", "[blender, 3d, reddit, weekly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 블렌더헬프 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"
    contents    = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 블렌더헬프 먼슬리: 데일리 파일 없음")
        return
    print(f"[BlenderHelp Monthly {month_label}] 요약 중...")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(f"Blender Help Monthly — {month_label}", "[blender, 3d, reddit, monthly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 블렌더헬프 먼슬리 저장: {path}")


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
    return llm(f"""아래는 r/blenderhelp {period} 데일리 요약 모음입니다 ({date_range}).

{contents[:8000]}

다음 형식으로 한국어 정리:

## 🔥 트렌드 3줄 요약
* (트렌드 1)
* (트렌드 2)
* (트렌드 3)

---

## 🟠 가장 많이 등장한 문제 Top 5
### N. 🟢/🔴 제목
> 문제 요약 및 해결 여부

---

## 💡 {period} 키워드
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
        print("\n[일요일] 블렌더헬프 위클리 실행")
        run_weekly()
    if now_kst.day == 28:
        print("\n[28일] 블렌더헬프 먼슬리 실행")
        run_monthly()


if __name__ == "__main__":
    main()
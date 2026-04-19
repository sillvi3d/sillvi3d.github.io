import os, requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# ── 설정 ──────────────────────────────────────────
SUBREDDIT    = "comfyui"
FLAIRS       = ["Workflow Included", "News", "Tutorial"]
FLAIR_EMOJI  = {"Workflow Included": "🟢", "News": "🔴", "Tutorial": "🟡"}
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (compatible; comfyui-digest-bot/1.0)"}
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")          # 예: 2026_04
VAULT_BASE = "0_Blog/AI/Trend/ComfyUI"
VAULT_PATH = f"{VAULT_BASE}/{year_month}"       # 예: 0_Blog/AI/ComfyUI/Daily/2026_04
# ─────────────────────────────────────────────────


# ── LLM 호출 ──────────────────────────────────────
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


# ── Reddit RSS 크롤링 ──────────────────────────────
def fetch_posts(flair: str, since_ts: float) -> list[dict]:
    url = (
        f"https://www.reddit.com/r/{SUBREDDIT}/search.rss"
        f"?q=flair%3A%22{flair.replace(' ', '+')}%22"
        f"&restrict_sr=1&sort=new&limit=50"
    )
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    ns    = {"atom": "http://www.w3.org/2005/Atom"}
    root  = ET.fromstring(res.text)
    filtered = []
    for e in root.findall("atom:entry", ns):
        updated = e.findtext("atom:updated", "", ns)
        try:
            post_ts = datetime.fromisoformat(updated.replace("Z", "+00:00")).timestamp()
        except Exception:
            continue
        if post_ts < since_ts:
            continue
        link = e.find("atom:link", ns)
        filtered.append({
            "title"   : sanitize(e.findtext("atom:title", "", ns)),
            "url"     : link.attrib.get("href", "") if link is not None else "",
            "selftext": sanitize(e.findtext("atom:content", "", ns)[:500]),
        })
    return filtered


# ── DAILY ─────────────────────────────────────────
def run_daily():
    os.makedirs(VAULT_PATH, exist_ok=True)
    since_ts = (now_kst - timedelta(hours=24)).timestamp()
    summaries = {}
    for flair in FLAIRS:
        print(f"[{flair}] 크롤링 중...")
        posts = fetch_posts(flair, since_ts)
        print(f"  → {len(posts)}개 수집")
        summaries[flair] = (summarize_daily(flair, posts), posts)
    md = build_daily_md(summaries)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 데일리 저장: {path}")


def summarize_daily(flair: str, posts: list[dict]) -> str:
    if not posts:
        return "_해당 플레어의 글이 없습니다._"
    posts_txt = "\n\n".join(
        f"[{i+1}] {p['title']}\nURL: {p['url']}\n내용: {p['selftext'] or '(이미지/링크 글)'}"
        for i, p in enumerate(posts)
    )
    return llm(f"""Reddit r/comfyui [{flair}] 최근 24시간 글 목록:

{posts_txt}

한국어로 정리해주세요:
1. **주요 트렌드** (2~3줄)
2. **주목할 만한 글** (상위 3개, 한 줄 소개 + URL)
3. **오늘의 키워드** (#태그 형식)""")


def build_daily_md(summaries: dict) -> str:
    lines = [
        "---",
        f"title: ComfyUI Reddit Daily — {today_str}",
        f"date: {today_str}",
        "tags: [comfyui, reddit, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        "",
    ]
    for flair, (summary, posts) in summaries.items():
        lines += [f"## {FLAIR_EMOJI[flair]} {flair}", f"_수집된 글: {len(posts)}개_", "", summary, "", "---", ""]
    return "\n".join(lines)


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"

    contents = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 위클리 요약할 데일리 파일 없음")
        return

    print(f"[Weekly {week_label}] 요약 중... ({date_range})")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(
        title=f"ComfyUI Reddit Weekly — {week_label}",
        tags="[comfyui, reddit, weekly]",
        date_range=date_range,
        summary=summary,
    )
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"

    contents = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 먼슬리 요약할 데일리 파일 없음")
        return

    print(f"[Monthly {month_label}] 요약 중... ({date_range})")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(
        title=f"ComfyUI Reddit Monthly — {month_label}",
        tags="[comfyui, reddit, monthly]",
        date_range=date_range,
        summary=summary,
    )
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 먼슬리 저장: {path}")


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


def summarize_period(daily_contents: str, period: str, date_range: str) -> str:
    return llm(f"""아래는 Reddit r/comfyui의 {period} 데일리 요약 모음입니다 ({date_range}).

{daily_contents[:8000]}

다음 형식으로 한국어로 정리해주세요:

## 트렌드 3줄 요약
* (전체 트렌드 1)
* (전체 트렌드 2)
* (전체 트렌드 3)

---

## 🟢 Workflow Included
### 1. 주요 트렌드 요약
(서술형 요약)
### 2. 가장 주목받은 Top 3
* 제목 — URL
* 제목 — URL
* 제목 — URL
### 3. {period} 키워드
#키워드1 #키워드2 #키워드3

---

## 🔴 News
### 1. 주요 트렌드 요약
(서술형 요약)
### 2. 가장 주목받은 Top 3
* 제목 — URL
* 제목 — URL
* 제목 — URL
### 3. {period} 키워드
#키워드1 #키워드2

---

## 🟡 Tutorial
### 1. 주요 트렌드 요약
(서술형 요약)
### 2. 가장 주목받은 Top 3
* 제목 — URL
* 제목 — URL
* 제목 — URL
### 3. {period} 키워드
#키워드1 #키워드2""")


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
    is_sunday = now_kst.weekday() == 6
    is_28th   = now_kst.day == 28

    run_daily()

    if is_sunday:
        print("\n[일요일] 위클리 요약 실행")
        run_weekly()

    if is_28th:
        print("\n[28일] 먼슬리 요약 실행")
        run_monthly()


if __name__ == "__main__":
    main()
import os, requests, time, re
from datetime import datetime, timezone, timedelta

try:
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

# ── 설정 ──────────────────────────────────────────
SOURCES = {
    "news"  : {"url": "https://www.gamemeca.com/news.php",   "emoji": "📰", "label": "뉴스"},
    "review": {"url": "https://www.gamemeca.com/review.php", "emoji": "🎮", "label": "리뷰"},
}
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
VAULT_BASE   = "5_Trend/Culture/Game"
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")
VAULT_PATH = f"{VAULT_BASE}/{year_month}"

# 크롤링 기준: 전일 00:00 KST ~ 현재
yesterday_start = (now_kst.replace(hour=0, minute=0, second=0, microsecond=0)
                   - timedelta(days=1))
# ─────────────────────────────────────────────────


def sanitize(text: str) -> str:
    return text.replace('"', "'").replace('\\', '').replace('\n', ' ').strip()


def llm(prompt: str, retry: int = 5) -> str:
    for attempt in range(retry):
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
                print(f"  429 Too Many Requests — {wait}초 대기 후 재시도 ({attempt+1}/{retry})")
                time.sleep(wait)
                continue
            res.raise_for_status()
            data = res.json()
            choice = data["choices"][0]
            if choice.get("finish_reason") == "content_filter":
                return "_콘텐츠 필터로 인해 요약이 제한되었습니다._"
            return choice["message"]["content"]
        except (KeyError, IndexError):
            return "_요약 실패_"
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(15)
            else:
                return f"_요약 실패: {str(e)[:100]}_"
    return "_요약 실패: 재시도 한도 초과_"


# ── 게임메카 크롤링 ──────────────────────────────
def fetch_gamemeca(source_key: str, max_pages: int = 5) -> list[dict]:
    """게임메카 페이지에서 전일~오늘 기사 전수 크롤링."""
    info = SOURCES[source_key]
    all_articles = []

    for page in range(1, max_pages + 1):
        url = f"{info['url']}?p={page}" if page > 1 else info["url"]
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            res.raise_for_status()
        except Exception as e:
            print(f"  ⚠️ [{source_key} p{page}] 요청 실패: {e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        articles_on_page = []
        stop_paging = False

        # 기사 링크 추출: view.php?gid=XXXXX 패턴
        for a_tag in soup.find_all("a", href=re.compile(r"view\.php\?gid=\d+")):
            title = a_tag.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            href = a_tag.get("href", "")
            if not href.startswith("http"):
                href = f"https://www.gamemeca.com/{href}"

            # 기사 주변에서 날짜 추출
            date_str = ""
            parent = a_tag.parent
            if parent:
                # 부모~조부모 범위에서 날짜 패턴 탐색
                for ancestor in [parent, parent.parent]:
                    if ancestor:
                        text = ancestor.get_text(" ", strip=True)
                        match = re.search(r"(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})", text)
                        if match:
                            date_str = match.group(1)
                            break

            # 날짜 파싱 & 필터
            article_dt = None
            if date_str:
                try:
                    article_dt = datetime.strptime(date_str, "%Y.%m.%d %H:%M").replace(tzinfo=KST)
                except ValueError:
                    pass

            if article_dt and article_dt < yesterday_start:
                stop_paging = True
                continue

            # 설명 추출 시도
            desc = ""
            if parent:
                for el in parent.find_all(["p", "span", "div"]):
                    t = el.get_text(strip=True)
                    if len(t) > 30 and t != title and not re.match(r"\d{4}\.\d{2}\.\d{2}", t):
                        desc = sanitize(t[:200])
                        break

            articles_on_page.append({
                "title": sanitize(title),
                "url"  : href,
                "date" : date_str,
                "desc" : desc,
            })

        # 중복 제거 후 추가
        seen = {a["url"] for a in all_articles}
        for a in articles_on_page:
            if a["url"] not in seen:
                seen.add(a["url"])
                all_articles.append(a)

        print(f"    p{page}: {len(articles_on_page)}개 추출")
        if stop_paging:
            print(f"    → 전일 이전 기사 도달, 페이징 중단")
            break
        time.sleep(2)  # 페이지 간 딜레이

    return all_articles


# ── 요약 ─────────────────────────────────────────
def summarize_source(source_key: str, info: dict, articles: list) -> str:
    if not articles:
        return "_오늘 수집된 기사가 없습니다._"
    articles_txt = "\n\n".join(
        f"[{i+1}] {a['title']}\nURL: {a['url']}"
        + (f"\n요약: {a['desc']}" if a['desc'] else "")
        + (f"\n날짜: {a['date']}" if a['date'] else "")
        for i, a in enumerate(articles)
    )
    return llm(f"""게임메카 [{info['label']}] 최근 기사 전체 목록:

{articles_txt}

한국어로 다음 형식에 맞춰 정리해주세요.
이 섹션은 HOT 기사가 아니라 **전수 크롤링**이므로, 모든 기사를 빠짐없이 포함해야 합니다.

### 📋 전체 기사 목록
각 기사를 카테고리별로 분류하여 정리:

**🔥 주요 뉴스** (업계 전반에 영향을 미치는 소식)
* **[제목](URL)** — 한줄 설명

**🎮 신작/업데이트** (게임 출시, 업데이트, 이벤트)
* **[제목](URL)** — 한줄 설명

**🏢 업계 동향** (인사, 실적, 협력, e스포츠)
* **[제목](URL)** — 한줄 설명

**🌏 해외 소식** (해외 게임/업계 뉴스)
* **[제목](URL)** — 한줄 설명

### 💡 오늘의 키워드
#키워드1 #키워드2 #키워드3""")


def summarize_overall(data: dict) -> str:
    titles = []
    for key, d in data.items():
        label = SOURCES[key]["label"]
        for a in d["articles"][:5]:
            titles.append(f"[{label}] {a['title'][:80]}")
    combined = "\n".join(titles)
    return llm(f"""다음은 오늘의 게임메카 주요 기사 제목 목록입니다.

{combined}

오늘의 게임 업계 핵심 이슈를 3줄로 요약해주세요:
* (이슈 1)
* (이슈 2)
* (이슈 3)""")


def build_daily_md(data: dict, overall: str) -> str:
    lines = [
        "---",
        f"title: Game News Daily — {today_str}",
        f"date: {today_str}",
        "tags: [game, news, review, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        f"> 출처: 게임메카 (gamemeca.com)",
        "",
        "## 🎯 오늘의 게임 3줄 요약",
        "",
        overall,
        "",
        "---",
        "",
    ]
    for key, info in SOURCES.items():
        d = data[key]
        lines += [
            f"## {info['emoji']} {info['label']}",
            f"_수집된 기사: {len(d['articles'])}개_",
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
    for i, (key, info) in enumerate(SOURCES.items()):
        if i > 0:
            print("  ⏳ rate limit 방지 5초 대기...")
            time.sleep(5)
        print(f"[게임메카 {info['label']}] 크롤링 중...")
        articles = fetch_gamemeca(key)
        print(f"  → 총 {len(articles)}개 수집")
        data[key] = {
            "articles": articles,
            "summary" : summarize_source(key, info, articles),
        }
    overall = summarize_overall(data)
    md   = build_daily_md(data, overall)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 게임 데일리 저장: {path}")


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"
    contents   = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 게임 위클리: 데일리 파일 없음")
        return
    print(f"[Game Weekly {week_label}] 요약 중...")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(f"Game News Weekly — {week_label}", "[game, news, weekly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 게임 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"
    contents    = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 게임 먼슬리: 데일리 파일 없음")
        return
    print(f"[Game Monthly {month_label}] 요약 중...")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(f"Game News Monthly — {month_label}", "[game, news, monthly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 게임 먼슬리 저장: {path}")


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
    return llm(f"""아래는 게임메카 {period} 데일리 요약 모음입니다 ({date_range}).

{contents[:8000]}

다음 형식으로 한국어 정리:

## 🎯 트렌드 3줄 요약
* (트렌드 1)
* (트렌드 2)
* (트렌드 3)

---

## 📰 뉴스 하이라이트
### 1. {period} 주요 이슈
(서술형 요약)
### 2. 가장 주목받은 기사 Top 5
* 제목 — URL
### 3. {period} 키워드
#키워드

---

## 🎮 리뷰 하이라이트
### 1. {period} 주요 리뷰
(서술형 요약)
### 2. 주목할 리뷰 Top 3
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
        f"> 출처: 게임메카 (gamemeca.com)",
        "",
        summary,
    ])


# ── 메인 ──────────────────────────────────────────
def main():
    run_daily()
    if now_kst.weekday() == 6:
        print("\n[일요일] 게임 위클리 실행")
        run_weekly()
    if now_kst.day == 28:
        print("\n[28일] 게임 먼슬리 실행")
        run_monthly()


if __name__ == "__main__":
    main()

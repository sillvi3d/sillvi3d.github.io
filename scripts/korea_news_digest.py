import os, requests, time, re
from datetime import datetime, timezone, timedelta

try:
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

# ── 설정 ──────────────────────────────────────────
SECTIONS = {
    "economy"  : {"emoji": "💰", "label": "경제"},
    "industry" : {"emoji": "🏭", "label": "산업"},
    "politics" : {"emoji": "🏛️", "label": "정치"},
    "society"  : {"emoji": "👥", "label": "사회"},
}
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS      = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
VAULT_BASE   = "5_Trend/News/Korea"
MONTH_ABBR   = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

KST        = timezone(timedelta(hours=9))
now_kst    = datetime.now(KST)
today_str  = now_kst.strftime("%Y-%m-%d")
year_month = now_kst.strftime("%Y_%m")
VAULT_PATH = f"{VAULT_BASE}/{year_month}"
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


# ── 한경 크롤링 ──────────────────────────────────
def fetch_hankyung(section: str) -> list[dict]:
    """한국경제 섹션 페이지에서 기사 목록 추출."""
    url = f"https://www.hankyung.com/{section}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except Exception as e:
        print(f"  ⚠️ [{section}] 페이지 요청 실패: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    seen_urls = set()

    # 모든 기사 링크 추출
    for a_tag in soup.find_all("a", href=re.compile(r"/article/")):
        title = a_tag.get_text(strip=True)
        if not title or len(title) < 8:
            continue
        href = a_tag.get("href", "")
        if not href.startswith("http"):
            href = f"https://www.hankyung.com{href}"
        if href in seen_urls:
            continue
        seen_urls.add(href)

        # 기사 주변에서 날짜 추출 시도
        date_str = ""
        parent = a_tag.parent
        if parent:
            text_around = parent.get_text(" ", strip=True)
            date_match = re.search(r"(\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2})", text_around)
            if date_match:
                date_str = date_match.group(1)

        # 기사 주변에서 설명 추출 시도
        desc = ""
        next_sib = a_tag.find_next_sibling(string=True)
        if next_sib and len(next_sib.strip()) > 20:
            desc = sanitize(next_sib.strip()[:200])
        if not desc and parent:
            for p in parent.find_all(["p", "span", "div"]):
                t = p.get_text(strip=True)
                if len(t) > 30 and t != title:
                    desc = sanitize(t[:200])
                    break

        articles.append({
            "title": sanitize(title),
            "url"  : href,
            "date" : date_str,
            "desc" : desc,
        })

    # 최신 기사 상위 25개 반환 (페이지 순서가 최신순)
    return articles[:25]


# ── 요약 ─────────────────────────────────────────
def summarize_section(section: str, info: dict, articles: list) -> str:
    if not articles:
        return "_오늘 수집된 기사가 없습니다._"
    articles_txt = "\n\n".join(
        f"[{i+1}] {a['title']}\nURL: {a['url']}\n"
        + (f"요약: {a['desc']}\n" if a['desc'] else "")
        + (f"날짜: {a['date']}" if a['date'] else "")
        for i, a in enumerate(articles[:20])
    )

    section_prompts = {
        "economy": "금리, 환율, 물가, GDP 등 거시경제 지표와 경제정책 중심으로",
        "industry": "반도체, 자동차, 조선, 에너지 등 산업 동향 중심으로",
        "politics": "정치 이슈, 정책 변화, 국회 동향 중심으로",
        "society": "사회 이슈, 교육, 복지, 사건사고 중심으로",
    }
    focus = section_prompts.get(section, "")

    return llm(f"""한국경제 [{info['label']}] 섹션 오늘의 주요 기사 목록:

{articles_txt}

{focus} 한국어로 정리해주세요:

### 📌 핵심 이슈 (3줄 요약)
* (이슈 1)
* (이슈 2)
* (이슈 3)

### 🏆 주목할 기사 Top 5
* **[제목](URL)** — 한줄 설명

### 💡 오늘의 키워드
#키워드1 #키워드2 #키워드3""")


def summarize_overall(data: dict) -> str:
    titles = []
    for sec, d in data.items():
        label = SECTIONS[sec]["label"]
        for a in d["articles"][:5]:
            titles.append(f"[{label}] {a['title'][:80]}")
    combined = "\n".join(titles)
    return llm(f"""다음은 오늘의 한국경제 주요 기사 제목 목록입니다.

{combined}

전체적인 한국 뉴스 흐름을 3줄로 요약해주세요:
* (핵심 이슈 1)
* (핵심 이슈 2)
* (핵심 이슈 3)""")


def build_daily_md(data: dict, overall: str) -> str:
    lines = [
        "---",
        f"title: Korea News Daily — {today_str}",
        f"date: {today_str}",
        "tags: [korea, news, economy, politics, daily]",
        "---",
        "",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        f"> 출처: 한국경제 (hankyung.com)",
        "",
        "## 🇰🇷 오늘의 한국 3줄 요약",
        "",
        overall,
        "",
        "---",
        "",
    ]
    for sec, info in SECTIONS.items():
        d = data[sec]
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
    for i, (sec, info) in enumerate(SECTIONS.items()):
        if i > 0:
            print("  ⏳ rate limit 방지 5초 대기...")
            time.sleep(5)
        print(f"[한경 {info['label']}] 크롤링 중...")
        articles = fetch_hankyung(sec)
        print(f"  → {len(articles)}개 수집")
        data[sec] = {
            "articles": articles,
            "summary" : summarize_section(sec, info, articles),
        }
    overall = summarize_overall(data)
    md   = build_daily_md(data, overall)
    path = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 한국뉴스 데일리 저장: {path}")


# ── WEEKLY ────────────────────────────────────────
def run_weekly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    monday     = now_kst - timedelta(days=6)
    week_num   = now_kst.isocalendar()[1]
    week_label = f"W{week_num:02d}"
    date_range = f"{monday.strftime('%Y-%m-%d')} ~ {today_str}"
    contents   = read_daily_files(monday, now_kst)
    if not contents:
        print("⚠️ 한국뉴스 위클리: 데일리 파일 없음")
        return
    print(f"[Korea News Weekly {week_label}] 요약 중...")
    summary = summarize_period(contents, "주간", date_range)
    md = build_period_md(f"Korea News Weekly — {week_label}", "[korea, news, weekly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{week_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 한국뉴스 위클리 저장: {path}")


# ── MONTHLY ───────────────────────────────────────
def run_monthly():
    os.makedirs(VAULT_PATH, exist_ok=True)
    month_label = MONTH_ABBR[now_kst.month - 1]
    month_start = now_kst.replace(day=1)
    date_range  = f"{month_start.strftime('%Y-%m-%d')} ~ {today_str}"
    contents    = read_daily_files(month_start, now_kst)
    if not contents:
        print("⚠️ 한국뉴스 먼슬리: 데일리 파일 없음")
        return
    print(f"[Korea News Monthly {month_label}] 요약 중...")
    summary = summarize_period(contents, "월간", date_range)
    md = build_period_md(f"Korea News Monthly — {month_label}", "[korea, news, monthly]", date_range, summary)
    path = os.path.join(VAULT_PATH, f"{month_label}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 한국뉴스 먼슬리 저장: {path}")


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
    return llm(f"""아래는 한국 뉴스 {period} 데일리 요약 모음입니다 ({date_range}).
출처: 한국경제 (경제, 산업, 정치, 사회)

{contents[:8000]}

다음 형식으로 한국어 정리:

## 🇰🇷 트렌드 3줄 요약
* (트렌드 1)
* (트렌드 2)
* (트렌드 3)

---

## 💰 경제
### 1. 주요 이슈 요약
### 2. 핵심 기사 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 🏭 산업
### 1. 주요 이슈 요약
### 2. 핵심 기사 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 🏛️ 정치
### 1. 주요 이슈 요약
### 2. 핵심 기사 Top 3
* 제목 — URL
### 3. {period} 키워드

---

## 👥 사회
### 1. 주요 이슈 요약
### 2. 핵심 기사 Top 3
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
        f"> 출처: 한국경제 (hankyung.com)",
        "",
        summary,
    ])


# ── 메인 ──────────────────────────────────────────
def main():
    run_daily()
    if now_kst.weekday() == 6:
        print("\n[일요일] 한국뉴스 위클리 실행")
        run_weekly()
    if now_kst.day == 28:
        print("\n[28일] 한국뉴스 먼슬리 실행")
        run_monthly()


if __name__ == "__main__":
    main()

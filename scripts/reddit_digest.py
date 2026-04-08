import os
import requests
from datetime import datetime, timezone, timedelta

# ── 설정 ──────────────────────────────────────────
SUBREDDIT   = "comfyui"
FLAIRS      = ["Workflow Included", "News", "Tutorial"]
FLAIR_EMOJI = {"Workflow Included": "🟢", "News": "🔴", "Tutorial": "🟡"}
VAULT_PATH  = "content/ComfyUI-Daily"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]   # Actions가 자동 주입
HEADERS     = {"User-Agent": "comfyui-digest-bot/1.0"}

KST = timezone(timedelta(hours=9))
now_kst   = datetime.now(KST)
today_str = now_kst.strftime("%Y-%m-%d")
since_ts  = (now_kst - timedelta(hours=24)).timestamp()
# ─────────────────────────────────────────────────


def fetch_posts(flair: str) -> list[dict]:
    url = (
        f"https://www.reddit.com/r/{SUBREDDIT}/search.json"
        f"?q=flair%3A%22{flair.replace(' ', '+')}%22"
        f"&restrict_sr=1&sort=new&limit=50"
    )
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    posts = res.json()["data"]["children"]

    filtered = []
    for p in posts:
        d = p["data"]
        if d.get("created_utc", 0) < since_ts:
            continue
        filtered.append({
            "title"   : d.get("title", ""),
            "url"     : f"https://reddit.com{d.get('permalink', '')}",
            "score"   : d.get("score", 0),
            "comments": d.get("num_comments", 0),
            "selftext": d.get("selftext", "")[:500],
        })
    return filtered


def summarize(flair: str, posts: list[dict]) -> str:
    if not posts:
        return "_해당 플레어의 글이 없습니다._"

    posts_txt = "\n\n".join(
        f"[{i+1}] {p['title']}\n"
        f"URL: {p['url']}\n"
        f"Score: {p['score']} | Comments: {p['comments']}\n"
        f"내용: {p['selftext'] or '(이미지/링크 글)'}"
        for i, p in enumerate(posts)
    )

    prompt = f"""아래는 Reddit r/comfyui의 [{flair}] 플레어 글 목록입니다 (최근 24시간).

{posts_txt}

다음 형식으로 한국어로 정리해주세요:

1. **주요 트렌드** (2~3줄 요약)
2. **주목할 만한 글** (상위 3개, 각각 한 줄 소개 + URL 포함)
3. **오늘의 키워드** (태그 형식, 예: #FLUX #ControlNet)"""

    res = requests.post(
        "https://models.inference.ai.azure.com/chat/completions",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type" : "application/json",
        },
        json={
            "model"   : "meta-llama-3.1-70b-instruct",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def build_markdown(summaries: dict[str, tuple[str, list]]) -> str:
    lines = [
        "---",
        f"title: ComfyUI Daily — {today_str}",
        f"date: {today_str}",
        "tags: [comfyui, reddit, daily]",
        "---",
        "",
        f"# ComfyUI Reddit Daily — {today_str}",
        f"> 자동 생성: {now_kst.strftime('%Y-%m-%d %H:%M')} KST",
        "",
    ]
    for flair, (summary, posts) in summaries.items():
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
    return "\n".join(lines)


def main():
    os.makedirs(VAULT_PATH, exist_ok=True)

    summaries = {}
    for flair in FLAIRS:
        print(f"[{flair}] 크롤링 중...")
        posts = fetch_posts(flair)
        print(f"  → {len(posts)}개 수집")
        summary = summarize(flair, posts)
        summaries[flair] = (summary, posts)

    md = build_markdown(summaries)
    filepath = os.path.join(VAULT_PATH, f"{today_str}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ 저장 완료: {filepath}")


if __name__ == "__main__":
    main()

# ============================================================
# resummarize.py — 요약 실패분 재요약 도구
# ------------------------------------------------------------
# v1.0  2026-08-24  신규 생성
#
# 무엇을 하나:
#   llm_client 가 _Meta/digest_raw/ 에 남긴 "원본 프롬프트"를 다시 LLM 에
#   넣어 요약을 만들고, 대응하는 5_Trend/**/{날짜}.md 안의
#   '_요약 실패: ...' 자리를 교체한다.
#
# 왜 필요한가:
#   2026-08 사고처럼 요약 API 가 죽으면 파일은 생성되지만 내용이 빈다.
#   원본 프롬프트가 보존돼 있으면 API 를 고친 뒤 소급 복구가 가능하다.
#   (※ 2026-08 실패분은 이 아카이브 기능이 생기기 전이라 원본이 없다.
#      그 기간은 이 도구로 복구할 수 없다 — README 참고)
#
# 사용법 (obsidian-vault 루트에서 실행):
#   GEMINI_API_KEY=xxx python scripts/resummarize.py --list
#   GEMINI_API_KEY=xxx python scripts/resummarize.py --date 2026-09-01
#   GEMINI_API_KEY=xxx python scripts/resummarize.py --all --apply
# ============================================================

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 재요약 자체는 원본 아카이브를 다시 남기지 않는다 (중복 방지)
os.environ.setdefault("DIGEST_ARCHIVE_RAW", "0")
from llm_client import llm  # noqa: E402

RAW_DIR = os.environ.get("DIGEST_RAW_DIR", "_Meta/digest_raw")
TREND_DIR = "5_Trend"
FAIL_RE = re.compile(r"_요약 실패:[^\n]*_")

# 원본 아카이브 파일명 태그 → 담당 볼트 폴더
TAG_TO_DIRS = {
    "reddit_digest":     ["5_Trend/ComfyUI"],
    "tech_digest":       ["5_Trend/AI_Tech"],
    "blender_digest":    ["5_Trend/Blender"],
    "world_news_digest": ["5_Trend/News/Global"],
    "korea_news_digest": ["5_Trend/News/Korea"],
    "game_digest":       ["5_Trend/Culture/Game"],
}


def failed_files() -> list[str]:
    out = []
    for path in glob.glob(f"{TREND_DIR}/**/*.md", recursive=True):
        try:
            with open(path, encoding="utf-8") as f:
                if FAIL_RE.search(f.read()):
                    out.append(path)
        except OSError:
            continue
    return sorted(out)


def raw_files(date: str | None) -> list[str]:
    pattern = f"{RAW_DIR}/**/{date or '*'}_*.md"
    return sorted(glob.glob(pattern, recursive=True))


def parse_raw(path: str) -> tuple[str, str, str, str]:
    """파일명 {date}_{tag}_{seq}.md 를 분해하고 프롬프트 본문을 돌려준다."""
    base = os.path.basename(path)[:-3]
    date, tag, seq = base.split("_")[0], "_".join(base.split("_")[1:-1]), base.split("_")[-1]
    with open(path, encoding="utf-8") as f:
        body = f.read()
    body = re.sub(r"^<!--.*?-->\s*", "", body, flags=re.S)
    return date, tag, seq, body


def target_md(date: str, tag: str) -> str | None:
    ym = date[:4] + "_" + date[5:7]
    for base in TAG_TO_DIRS.get(tag, []):
        cand = f"{base}/{ym}/{date}.md"
        if os.path.exists(cand):
            return cand
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="요약 실패분 재요약")
    ap.add_argument("--date", help="복구할 날짜 (YYYY-MM-DD)")
    ap.add_argument("--all", action="store_true", help="아카이브 전체 대상")
    ap.add_argument("--list", action="store_true", help="요약 실패 파일만 나열")
    ap.add_argument("--apply", action="store_true", help="실제로 파일을 수정 (없으면 dry-run)")
    args = ap.parse_args()

    if args.list:
        bad = failed_files()
        print(f"요약 실패가 남아 있는 파일: {len(bad)}개")
        for p in bad:
            print(" ", p)
        avail = {parse_raw(r)[0] for r in raw_files(None)}
        print(f"\n원본 아카이브가 있는 날짜: {len(avail)}개")
        for d in sorted(avail):
            print(" ", d)
        return 0

    if not (args.date or args.all):
        ap.error("--date 또는 --all 중 하나가 필요합니다 (--list 로 현황 확인)")

    raws = raw_files(args.date)
    if not raws:
        print(f"❌ 원본 아카이브를 찾지 못했습니다: {RAW_DIR}")
        print("   (2026-08 이전 실패분은 원본이 저장되지 않아 복구 불가)")
        return 1

    fixed = skipped = 0
    for raw in raws:
        date, tag, seq, prompt = parse_raw(raw)
        md = target_md(date, tag)
        if not md:
            print(f"⏭  대상 md 없음: {raw}")
            skipped += 1
            continue
        with open(md, encoding="utf-8") as f:
            content = f.read()
        if not FAIL_RE.search(content):
            print(f"✔  이미 정상: {md}")
            skipped += 1
            continue

        print(f"🔁 재요약: {md}  ← {os.path.basename(raw)}")
        summary = llm(prompt)
        if summary.startswith("_요약 실패"):
            print(f"   ❌ 재요약도 실패 — 중단: {summary[:120]}")
            return 1

        new = FAIL_RE.sub(lambda _: summary, content, count=1)
        if args.apply:
            with open(md, "w", encoding="utf-8") as f:
                f.write(new)
            print("   ✅ 반영 완료")
        else:
            print(f"   (dry-run) 앞부분: {summary[:120]}...")
        fixed += 1

    print(f"\n완료 — 재요약 {fixed}건, 건너뜀 {skipped}건"
          + ("" if args.apply else "  ※ dry-run 이므로 파일은 바뀌지 않았습니다 (--apply 추가)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

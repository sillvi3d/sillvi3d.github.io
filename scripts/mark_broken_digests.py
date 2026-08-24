# ============================================================
# mark_broken_digests.py — 복구 불가 구간 정리
# ------------------------------------------------------------
# v1.0  2026-08-24  신규 생성
#
# 2026-07-31 ~ 2026-08-2x 구간은 GitHub Models 폐지로 요약이 실패했고,
# 당시에는 원본 수집 데이터를 저장하지 않았기 때문에 재요약이 불가능하다.
# (사용 피드도 top.rss?t=day / hot.rss / 뉴스 프론트페이지라 소급 수집 불가)
#
# 그대로 두면 블로그에 날 HTTP 에러 문자열이 노출되므로,
# 사람이 읽을 수 있는 안내 문구로 바꾼다.
#
# 사용법 (obsidian-vault 루트에서):
#   python scripts/mark_broken_digests.py              # dry-run
#   python scripts/mark_broken_digests.py --apply
#   python scripts/mark_broken_digests.py --apply --from 2026-07-31 --to 2026-08-24
# ============================================================

import argparse
import glob
import os
import re
import sys

FAIL_RE = re.compile(r"_요약 실패:[^\n]*_")
NOTICE = (
    "> ⚠️ 이 날짜의 자동 요약은 생성되지 않았습니다.\n"
    "> 요약에 사용하던 GitHub Models API가 2026-07-30 서비스 종료되어\n"
    "> 2026-07-31 ~ 2026-08-24 구간의 요약이 누락되었습니다. "
    "(수집 자체는 정상 동작했습니다)\n"
    "> 이후 Google Gemini API로 전환하여 복구되었습니다."
)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def in_range(path: str, lo: str, hi: str) -> bool:
    m = DATE_RE.search(os.path.basename(path))
    if m:
        return lo <= m.group(1) <= hi
    # W31.md / AUG.md 같은 주간/월간 파일은 상위 폴더의 연-월로 판단
    ym = os.path.basename(os.path.dirname(path)).replace("_", "-")
    return lo[:7] <= ym <= hi[:7]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="lo", default="2026-07-31")
    ap.add_argument("--to", dest="hi", default="2026-08-24")
    ap.add_argument("--apply", action="store_true", help="없으면 dry-run")
    a = ap.parse_args()

    hits = 0
    for path in sorted(glob.glob("5_Trend/**/*.md", recursive=True)):
        if not in_range(path, a.lo, a.hi):
            continue
        with open(path, encoding="utf-8") as f:
            src = f.read()
        if not FAIL_RE.search(src):
            continue
        n = len(FAIL_RE.findall(src))
        out = FAIL_RE.sub(NOTICE, src)
        hits += 1
        print(f"{'✅' if a.apply else '  '} {path}  ({n}곳)")
        if a.apply:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)

    print(f"\n대상 파일 {hits}개"
          + ("" if a.apply else "  ※ dry-run — 실제 수정은 --apply"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

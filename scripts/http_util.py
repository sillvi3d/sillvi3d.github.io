# ============================================================
# http_util.py — digest 스크립트 공통 HTTP 수집 계층
# ------------------------------------------------------------
# v1.0  2026-11-20  신규 생성
#
# 왜 만들었나:
#   reddit/tech/blender/world_news 네 스크립트는 res.raise_for_status() 를
#   맨몸으로 호출하고 있었다. 429 는 재시도하지만 403·404·5xx 나
#   네트워크 오류는 그대로 예외가 되어 스크립트가 exit 1 로 죽는다.
#   워크플로는 fail-fast 라서 첫 스크립트(ComfyUI)가 죽으면
#   나머지 5개 소스는 실행조차 못 하고 커밋도 안 된다.
#   → 2026-11-10 ~ 11-20, 20회 연속 전면 실패의 실제 피해 원인.
#
#   한 소스의 장애는 그 소스만 비워야 한다. 그게 이 모듈의 전부다.
#
# 설계:
#   - fetch() 는 절대 예외를 던지지 않는다. 실패하면 None.
#   - 429 / 5xx / 네트워크 오류 → 백오프 재시도
#   - 403 / 404 / 410 → 재시도 무의미하므로 즉시 포기 (응답 본문 일부를 로그에)
#   - 실패는 _Meta/digest_raw/<YYYY_MM>/<날짜>_fetch_errors.log 에 누적 기록.
#     워크플로 마지막 검사 스텝이 이 파일을 보고 실행을 실패 처리한다.
#     → 데이터는 커밋되고, 경보는 울린다.
# ============================================================

import os
import time
from datetime import datetime, timedelta, timezone

import requests

KST = timezone(timedelta(hours=9))

RAW_DIR = os.environ.get("DIGEST_RAW_DIR", "_Meta/digest_raw")
ERROR_LOG_SUFFIX = "_fetch_errors.log"

DEFAULT_ATTEMPTS = int(os.environ.get("DIGEST_HTTP_ATTEMPTS", "5"))
DEFAULT_TIMEOUT = int(os.environ.get("DIGEST_HTTP_TIMEOUT", "15"))

# 재시도해도 소용없는 상태코드 (차단/삭제)
HARD_FAIL = {400, 401, 403, 404, 410, 451}

# 이 프로세스에서 발생한 수집 실패
errors: list[str] = []


def _script_tag() -> str:
    import __main__
    raw = os.path.basename(getattr(__main__, "__file__", "digest") or "digest")
    return os.path.splitext(raw)[0] or "digest"


def _record(label: str, url: str, reason: str) -> None:
    """수집 실패를 기록한다. 워크플로 검사 스텝이 이 파일을 읽는다."""
    line = f"{datetime.now(KST).isoformat()}\t{_script_tag()}\t{label}\t{reason}\t{url}"
    errors.append(line)
    try:
        now = datetime.now(KST)
        d = os.path.join(RAW_DIR, now.strftime("%Y_%m"))
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, now.strftime("%Y-%m-%d") + ERROR_LOG_SUFFIX)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"  ⚠️ 수집 실패 기록 자체가 실패: {e}")


def fetch(
    url: str,
    headers: dict | None = None,
    *,
    label: str = "",
    timeout: int = DEFAULT_TIMEOUT,
    attempts: int = DEFAULT_ATTEMPTS,
) -> str | None:
    """HTTP GET. 성공하면 본문 문자열, 실패하면 None. 예외를 밖으로 던지지 않는다."""
    tag = f"[{label}] " if label else ""
    reason = "원인 불명"

    for attempt in range(max(1, attempts)):
        try:
            res = requests.get(url, headers=headers, timeout=timeout)
        except Exception as e:
            reason = f"{type(e).__name__}: {e}"
            print(f"  ⚠️ {tag}요청 실패 — {reason}")
            if attempt + 1 >= attempts:
                break
            time.sleep(5 * (attempt + 1))
            continue

        code = res.status_code

        if code == 200:
            return res.text

        if code == 429:
            reason = "429 Too Many Requests"
            if attempt + 1 >= attempts:
                break
            wait = 30 * (attempt + 1)
            print(f"  ⏳ {tag}429 — {wait}초 대기 후 재시도 ({attempt + 1}/{attempts})")
            time.sleep(wait)
            continue

        if code in HARD_FAIL:
            # 차단/삭제: 재시도해도 결과가 달라지지 않는다
            reason = f"HTTP {code}"
            body = (res.text or "").strip().replace("\n", " ")[:200]
            print(f"  ❌ {tag}{reason} — 재시도 생략. 응답: {body}")
            break

        reason = f"HTTP {code}"
        print(f"  ⚠️ {tag}{reason}")
        if attempt + 1 >= attempts:
            break
        time.sleep(5 * (attempt + 1))

    print(f"  ❌ {tag}수집 실패 — {reason} (이 소스는 비워두고 계속 진행)")
    _record(label or "-", url, reason)
    return None


def error_count() -> int:
    return len(errors)

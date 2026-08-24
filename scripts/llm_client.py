# ============================================================
# llm_client.py — digest 스크립트 공통 LLM 클라이언트 (Google Gemini)
# ------------------------------------------------------------
# v1.0  2026-08-24  신규 생성 (GitHub Models 2026-07-30 폐지 대응)
# v1.1  2026-08-24  모델 선택 로직 전면 수정
#   v1.0 의 버그:
#     - 자동 탐색이 모델을 찾아도 "이미 후보 목록에 있으면" 사용하지 않고
#       실패로 끝냈다. (found not in candidates 조건이 잘못됨)
#     - 404/429 를 매 호출마다 처음부터 다시 시도해서 호출 하나에 수 분씩 걸렸다.
#     - 429 응답 본문을 찍지 않아 원인(쿼터 초과 vs 일시적)을 알 수 없었다.
#   v1.1 의 방식:
#     1) 시작 시 ListModels 로 "이 키가 실제로 쓸 수 있는 모델"을 한 번만 조회하고
#        전체 목록을 로그에 남긴다.
#     2) 존재하는 모델만 시도 순서에 넣는다. (없는 모델에 요청 자체를 안 보냄)
#     3) 404(없음)/429(쿼터)로 판정된 모델은 프로세스 전체에서 기억해 다시 안 쓴다.
#     4) 성공한 모델은 맨 앞으로 고정 → 이후 호출은 곧바로 성공.
#     5) 429 는 응답의 retryDelay 를 존중하고, 본문을 찍어 원인을 남긴다.
#
#   설계 원칙 (같은 사고 재발 방지):
#     - 프로바이더 교체 지점을 이 파일 하나로 모은다.
#     - 모델 ID 가 바뀌어도 실제 목록 조회로 살아남는다.
#     - 요약에 넣은 원본을 항상 아카이브한다 → 나중에 재요약 가능.
#     - 실패를 조용히 넘기지 않는다.
# ============================================================

import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

# ── 설정 ──────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY", "")
API_BASE = os.environ.get(
    "GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta"
)

# 선호 순서. 실제로 존재하는 것만 골라 쓴다. 여기 없어도 목록에서 자동 보충.
PREFERRED = [
    m.strip()
    for m in os.environ.get(
        "GEMINI_MODEL",
        "gemini-2.5-flash,gemini-2.5-flash-lite,gemini-flash-latest,"
        "gemini-flash-lite-latest,gemini-2.0-flash,gemini-2.0-flash-lite",
    ).split(",")
    if m.strip()
]

ATTEMPTS_PER_MODEL = int(os.environ.get("GEMINI_ATTEMPTS", "2"))
BASE_DELAY = float(os.environ.get("GEMINI_BASE_DELAY", "2"))   # 호출 간 최소 간격(초)
MAX_WAIT = 45                                                  # 429 대기 상한(초)
TIMEOUT = 90

RAW_DIR = os.environ.get("DIGEST_RAW_DIR", "_Meta/digest_raw")
ARCHIVE_RAW = os.environ.get("DIGEST_ARCHIVE_RAW", "1") != "0"

FAIL_MARKER = "_요약 실패"
KST = timezone(timedelta(hours=9))

# 이 프로세스에서 발생한 요약 실패 (워크플로 검증 단계에서 활용)
failures: list[str] = []

# ── 프로세스 전역 상태 ─────────────────────────────
_available: list[str] | None = None   # ListModels 결과 (None = 아직 조회 안 함)
_order: list[str] = []                # 시도 순서
_dead: set[str] = set()               # 404 로 판정된 모델
_quota: set[str] = set()              # 429 로 판정된 모델
_good: str | None = None              # 성공한 모델 (맨 앞 고정)
_call_seq = 0
_last_call_at = 0.0


# ── HTTP ──────────────────────────────────────────
def _request(url: str, payload: dict | None = None) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="POST" if data else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:                      # 네트워크/타임아웃 → 0 (재시도 대상)
        return 0, f"{type(e).__name__}: {e}"


def _retry_delay(body: str) -> float | None:
    """429 응답의 RetryInfo.retryDelay('23s')를 초로 환산."""
    m = re.search(r'"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"', body)
    return float(m.group(1)) if m else None


# ── 모델 목록 / 시도 순서 ──────────────────────────
def _fetch_available() -> list[str]:
    global _available
    if _available is not None:
        return _available
    status, body = _request(f"{API_BASE}/models?key={API_KEY}&pageSize=1000")
    if status != 200:
        print(f"  ⚠️ 모델 목록 조회 실패({status}): {body[:300]}")
        _available = []
        return _available
    try:
        models = json.loads(body).get("models", [])
    except Exception as e:
        print(f"  ⚠️ 모델 목록 파싱 실패: {e}")
        _available = []
        return _available

    # 채팅 요약에 쓸 수 없는 계열은 애초에 후보에서 뺀다
    EXCLUDE = ("embedding", "aqa", "imagen", "veo", "tts")
    _available = [
        n
        for n in (
            m["name"].split("/")[-1]
            for m in models
            if "generateContent" in m.get("supportedGenerationMethods", [])
        )
        if not any(k in n for k in EXCLUDE)
    ]
    print(f"  📋 이 키로 쓸 수 있는 모델 {len(_available)}개:")
    print(f"     {', '.join(_available)}")
    return _available


def _rank(name: str) -> int:
    """저렴하고 무료 티어가 관대한 모델을 앞으로."""
    s = 0
    if "flash" in name:
        s -= 20
    if "lite" in name:
        s -= 5
    if "latest" in name:
        s -= 2
    if "pro" in name:
        s += 10
    for bad in ("thinking", "image", "vision", "embedding", "tts",
                "audio", "live", "native", "preview", "exp", "learnlm", "gemma"):
        if bad in name:
            s += 40
    return s


def _build_order() -> list[str]:
    global _order
    if _order:
        return _order
    avail = _fetch_available()
    if not avail:
        # 목록 조회가 막힌 경우엔 선호 목록을 그대로 시도한다
        _order = list(PREFERRED)
        print(f"  🔀 (목록 조회 불가) 시도 순서: {', '.join(_order)}")
        return _order

    head = [m for m in PREFERRED if m in avail]
    tail = sorted([m for m in avail if m not in head], key=_rank)
    _order = head + tail
    print(f"  🔀 시도 순서(앞 6개): {', '.join(_order[:6])}")
    return _order


def _candidates() -> list[str]:
    order = [m for m in _build_order() if m not in _dead and m not in _quota]
    if _good and _good in order:
        order = [_good] + [m for m in order if m != _good]
    return order


# ── 원본 아카이브 ─────────────────────────────────
def _script_tag() -> str:
    import __main__
    raw = os.path.basename(getattr(__main__, "__file__", "digest") or "digest")
    tag = re.sub(r"[^0-9A-Za-z_.-]", "_", os.path.splitext(raw)[0]).strip("_")
    return tag or "digest"


def _archive(prompt: str, seq: int) -> None:
    """요약에 넣은 원본을 저장한다. 요약이 실패해도 나중에 재요약할 수 있게."""
    if not ARCHIVE_RAW:
        return
    try:
        now = datetime.now(KST)
        d = os.path.join(RAW_DIR, now.strftime("%Y_%m"))
        os.makedirs(d, exist_ok=True)
        path = os.path.join(
            d, f"{now.strftime('%Y-%m-%d')}_{_script_tag()}_{seq:02d}.md"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"<!-- digest raw prompt | {_script_tag()} | {now.isoformat()} -->\n\n")
            f.write(prompt)
    except Exception as e:
        print(f"  ⚠️ 원본 아카이브 실패: {e}")


# ── 공개 API ──────────────────────────────────────
def llm(prompt: str, retry: int = ATTEMPTS_PER_MODEL) -> str:
    """프롬프트를 요약해 문자열로 반환. 실패 시 '_요약 실패: ...' 문자열."""
    global _good, _call_seq, _last_call_at

    _call_seq += 1
    _archive(prompt, _call_seq)

    if not API_KEY:
        msg = f"{FAIL_MARKER}: GEMINI_API_KEY 환경변수가 비어 있습니다._"
        failures.append(msg)
        print(f"  ❌ {msg}")
        return msg

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 4096},
    }

    cands = _candidates()
    if not cands:
        why = []
        if _dead:
            why.append(f"404: {', '.join(sorted(_dead))}")
        if _quota:
            why.append(f"429(쿼터): {', '.join(sorted(_quota))}")
        msg = (f"{FAIL_MARKER}: 사용 가능한 모델이 없습니다 — "
               f"{' / '.join(why) or '모델 목록 비어 있음'}_")
        failures.append(msg)
        print(f"  ❌ {msg}")
        return msg

    last_err = "원인 불명"

    for model in cands:
        url = f"{API_BASE}/models/{model}:generateContent?key={API_KEY}"

        for attempt in range(max(1, retry)):
            gap = BASE_DELAY - (time.time() - _last_call_at)
            if gap > 0:
                time.sleep(gap)
            status, body = _request(url, payload)
            _last_call_at = time.time()

            if status == 200:
                try:
                    cand = json.loads(body)["candidates"][0]
                    text = "".join(
                        p.get("text", "") for p in cand["content"]["parts"]
                    ).strip()
                except (KeyError, IndexError, ValueError):
                    last_err = f"응답 파싱 실패: {body[:200]}"
                    print(f"  ⚠️ {last_err}")
                    break
                if text:
                    if _good != model:
                        print(f"  ✅ 요약 모델: {model}")
                        _good = model
                    return text
                last_err = f"빈 응답 (finishReason={cand.get('finishReason')})"
                print(f"  ⚠️ {last_err}")
                break

            if status == 404:
                _dead.add(model)
                last_err = f"404 모델 없음: {model}"
                print(f"  ⚠️ 모델 '{model}' 없음(404) — 후보에서 제외")
                break

            if status == 429:
                if attempt == 0:
                    print(f"  ⏳ 429 [{model}] {body[:220]}")
                if attempt + 1 >= retry:
                    _quota.add(model)
                    last_err = f"429 쿼터 초과: {model}"
                    print(f"  ⚠️ '{model}' 쿼터 초과 — 후보에서 제외")
                    break
                wait = min(MAX_WAIT, _retry_delay(body) or (8 * (attempt + 1)))
                print(f"     {wait:.0f}초 대기 후 재시도 ({attempt + 1}/{retry})")
                time.sleep(wait)
                continue

            if status in (401, 403):
                last_err = f"{status} 인증/권한 실패 — API 키를 확인하세요: {body[:200]}"
                print(f"  ❌ {last_err}")
                failures.append(last_err)
                return f"{FAIL_MARKER}: {last_err}_"

            if status in (0, 500, 502, 503, 504):
                last_err = f"{status} {body[:160]}"
                if attempt + 1 >= retry:
                    print(f"  ⚠️ {last_err} — 다음 모델로")
                    break
                print(f"  ⚠️ {last_err} — 8초 후 재시도")
                time.sleep(8)
                continue

            last_err = f"{status} {body[:200]}"
            print(f"  ⚠️ {last_err}")
            break

    msg = f"{FAIL_MARKER}: {last_err[:220]}_"
    failures.append(last_err)
    print(f"  ❌ 요약 실패: {last_err[:220]}")
    return msg


def failure_count() -> int:
    return len(failures)

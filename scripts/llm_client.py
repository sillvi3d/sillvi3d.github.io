# ============================================================
# llm_client.py — digest 스크립트 공통 LLM 클라이언트
# ------------------------------------------------------------
# v1.0  2026-08-24  신규 생성
#   배경: 기존 GitHub Models 엔드포인트
#         (https://models.inference.ai.azure.com/chat/completions)
#         가 2026-07-30 서비스 완전 폐지됨.
#         → 07-31~08-05 401 Unauthorized
#         → 08-06~      404 Not Found
#         결과적으로 8월 내내 모든 digest의 요약이 실패했다.
#
#   설계 원칙 (같은 사고 재발 방지):
#     1) 프로바이더 교체 지점을 이 파일 하나로 모은다.
#     2) 모델 ID가 바뀌어도 자동 탐색으로 살아남는다.
#     3) 요약에 넣은 원본 데이터를 항상 아카이브한다.
#        → 요약이 실패해도 나중에 재요약이 가능하다.
#     4) 실패를 조용히 넘기지 않는다. (실패 카운터 + 마커)
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
API_BASE = "https://generativelanguage.googleapis.com/v1beta"

# 우선순위대로 시도. 앞의 모델이 404면 다음으로 넘어간다.
MODEL_CANDIDATES = [
    m.strip()
    for m in os.environ.get(
        "GEMINI_MODEL",
        "gemini-2.5-flash,gemini-flash-latest,gemini-2.0-flash,gemini-1.5-flash",
    ).split(",")
    if m.strip()
]

MAX_ATTEMPTS = 5
BASE_DELAY = 2          # 호출 간 기본 간격(초)
TIMEOUT = 90

# 원본 프롬프트 아카이브 경로 (Quartz ignorePatterns 의 _Meta/** 안 → 블로그 미노출)
RAW_DIR = os.environ.get("DIGEST_RAW_DIR", "_Meta/digest_raw")
ARCHIVE_RAW = os.environ.get("DIGEST_ARCHIVE_RAW", "1") != "0"

FAIL_MARKER = "_요약 실패"

KST = timezone(timedelta(hours=9))

# 이 프로세스에서 발생한 요약 실패 수 (워크플로 검증 단계에서 활용)
failures: list[str] = []

_resolved_model: str | None = None
_call_seq = 0


# ── 내부 유틸 ─────────────────────────────────────
def _post(url: str, payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # 네트워크/타임아웃 등 — status 0 은 재시도 대상
        return 0, f"{type(e).__name__}: {e}"


def _get(url: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, f"{type(e).__name__}: {e}"


def _discover_model() -> str | None:
    """모델 ID가 전부 404일 때 실제 사용 가능한 모델을 API 에서 찾는다."""
    status, body = _get(f"{API_BASE}/models?key={API_KEY}&pageSize=200")
    if status != 200:
        print(f"  ⚠️ 모델 목록 조회 실패 ({status}): {body[:200]}")
        return None
    try:
        models = json.loads(body).get("models", [])
    except Exception:
        return None

    usable = [
        m["name"].split("/")[-1]
        for m in models
        if "generateContent" in m.get("supportedGenerationMethods", [])
    ]
    # flash 계열(저렴/무료 티어 관대) 우선
    for kw in ("flash-latest", "flash", ""):
        for name in usable:
            if kw in name and "thinking" not in name and "image" not in name:
                print(f"  🔍 자동 탐색된 모델: {name}")
                return name
    return None


def _archive(prompt: str, tag: str, seq: int) -> None:
    """요약에 넣은 원본 프롬프트를 저장한다.

    이번 사고처럼 요약 API 가 죽어도 수집된 글 제목/URL/본문이
    여기에 남아 있으므로 나중에 재요약이 가능하다.
    """
    if not ARCHIVE_RAW:
        return
    try:
        now = datetime.now(KST)
        d = os.path.join(RAW_DIR, now.strftime("%Y_%m"))
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f"{now.strftime('%Y-%m-%d')}_{tag}_{seq:02d}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"<!-- digest raw prompt | {tag} | {now.isoformat()} -->\n\n")
            f.write(prompt)
    except Exception as e:  # 아카이브 실패가 본 작업을 막아선 안 된다
        print(f"  ⚠️ 원본 아카이브 실패: {e}")


def _script_tag() -> str:
    import __main__
    raw = os.path.basename(getattr(__main__, "__file__", "digest") or "digest")
    tag = os.path.splitext(raw)[0]
    tag = re.sub(r"[^0-9A-Za-z_.-]", "_", tag).strip("_")
    return tag or "digest"


# ── 공개 API ──────────────────────────────────────
def llm(prompt: str, retry: int = MAX_ATTEMPTS, _archived: bool = False) -> str:
    """프롬프트를 요약해 문자열로 반환. 실패 시 '_요약 실패: ...' 문자열."""
    global _resolved_model, _call_seq
    if not _archived:
        _call_seq += 1
        _archive(prompt, _script_tag(), _call_seq)

    if not API_KEY:
        msg = f"{FAIL_MARKER}: GEMINI_API_KEY 환경변수가 설정되지 않았습니다._"
        failures.append(msg)
        print(f"  ❌ {msg}")
        return msg

    candidates = ([_resolved_model] if _resolved_model else []) + [
        m for m in MODEL_CANDIDATES if m != _resolved_model
    ]
    last_err = "원인 불명"

    for model in candidates:
        url = f"{API_BASE}/models/{model}:generateContent?key={API_KEY}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 4096},
        }

        for attempt in range(retry):
            time.sleep(BASE_DELAY)
            status, body = _post(url, payload)

            if status == 200:
                try:
                    data = json.loads(body)
                    cand = data["candidates"][0]
                    text = "".join(
                        p.get("text", "") for p in cand["content"]["parts"]
                    ).strip()
                    if text:
                        _resolved_model = model
                        return text
                    last_err = f"빈 응답 (finishReason={cand.get('finishReason')})"
                except (KeyError, IndexError, ValueError):
                    last_err = f"응답 파싱 실패: {body[:200]}"
                break  # 200 인데 내용이 이상하면 재시도 의미 없음

            if status in (0, 429, 500, 502, 503, 504):
                wait = min(60, 10 * (attempt + 1))
                print(f"  {status} — {wait}초 대기 후 재시도 ({attempt + 1}/{retry})")
                last_err = f"{status} {body[:120]}"
                time.sleep(wait)
                continue

            if status == 404:
                print(f"  ⚠️ 모델 '{model}' 없음(404) — 다음 후보로 전환")
                last_err = f"404 모델 없음: {model}"
                break  # 다음 모델 후보로

            if status in (401, 403):
                last_err = f"{status} 인증/권한 실패 — API 키를 확인하세요: {body[:160]}"
                print(f"  ❌ {last_err}")
                failures.append(last_err)
                return f"{FAIL_MARKER}: {last_err}_"

            last_err = f"{status} {body[:160]}"
            print(f"  ⚠️ {last_err}")
            time.sleep(5)

    # 후보 전부 실패 → 실제 사용 가능한 모델 자동 탐색 후 1회 재시도
    if _resolved_model is None:
        found = _discover_model()
        if found and found not in candidates:
            _resolved_model = found
            return llm(prompt, retry=2, _archived=True)

    msg = f"{FAIL_MARKER}: {last_err[:200]}_"
    failures.append(last_err)
    print(f"  ❌ 요약 실패: {last_err[:200]}")
    return msg


def failure_count() -> int:
    return len(failures)

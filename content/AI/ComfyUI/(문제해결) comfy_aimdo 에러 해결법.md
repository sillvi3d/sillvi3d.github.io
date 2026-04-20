---
tags: [문제해결, AI이미지]
---

# comfy_aimdo access violation 에러 (KSampler)

## 상황

ComfyUI에서 Seamless Tiling 워크플로우 실행 시 KSampler 노드에서 에러 발생.
GPU: NVIDIA RTX PRO 4500 Blackwell / 드라이버: 595.97 (최신)

```
OSError: exception: access violation reading 0x000001F6BD00E000
```

에러 발생 위치:
```
comfy_aimdo\model_vbar.py → lib.vbars_analyze()
comfy_aimdo\model_vbar.py → lib.vbar_prioritize()
```

간헐적으로 한 번은 성공하고 다음에 실패하는 패턴.

## 원인

`comfy_aimdo`는 ComfyUI의 VRAM 최적화 패키지인데, Blackwell 아키텍처(RTX PRO 4500 등)와 호환성 문제가 있었음. comfy_aimdo 내부의 vbar(VRAM 관리) 함수가 메모리에 잘못 접근하면서 access violation 발생.

## 해결

1. ComfyUI 코어 + 의존 패키지를 최신으로 업데이트

```bash
cd C:\Users\madei\Documents\ComfyUI
git pull
venv\Scripts\activate
pip install -r requirements.txt
```

2. ComfyUI 재시작

## 주의

- `comfy_aimdo`를 단독으로 `pip uninstall` 하면 ComfyUI 코어가 이 패키지에 의존하고 있어서 Load Checkpoint부터 에러남 (`ModuleNotFoundError: No module named 'comfy_aimdo.model_mmap'`). 단독 제거 금지.
- `git pull` + `pip install -r requirements.txt`를 세트로 해야 comfy_aimdo 버전도 함께 맞춰짐.

## 참고

- 이 PC: RTX PRO 4500 Blackwell, 드라이버 595.97
- Blackwell 아키텍처는 2025~2026년 출시라 일부 패키지가 아직 완전 지원하지 않을 수 있음
- 비슷한 에러 재발 시 `git pull` + `pip install -r requirements.txt` 먼저 시도

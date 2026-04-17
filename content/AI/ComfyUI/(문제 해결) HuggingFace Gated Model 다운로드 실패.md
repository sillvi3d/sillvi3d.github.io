---
title: (문제 해결) HuggingFace Gated Model 다운로드 실패
---

## 상황

ComfyUI에서 RMBG-2.0 등 특정 커스텀 노드를 사용할 때, 모델 다운로드 과정에서 Hugging Face API 요청이 발생하며 모델을 받지 못하는 문제.
<img src="/AI/ComfyUI/assets/Pasted_image_20260416105027.png" width="300" />
## 원인

해당 모델이 Hugging Face의 **Gated Model**(게이트 모델)로 설정되어 있어, 라이선스 동의 및 인증 토큰 없이는 다운로드가 차단됨.

## 해결

1. 브라우저에서 모델 페이지에 접속 (예: https://huggingface.co/1038lab/RMBG-2.0)
2. Hugging Face 계정으로 로그인 후, 라이선스 동의 버튼 클릭
3. https://huggingface.co/settings/tokens 에서 Access Token 생성
4. ComfyUI 실행 전 터미널에서 환경변수 등록:
   ```
   set HF_TOKEN=hf_your_token_here
   ```
5. 또는 ComfyUI 실행 배치 파일(예: `run_nvidia_gpu.bat`)에 위 명령을 추가하여 매번 입력하지 않도록 설정

## 참고

- 모든 모델이 게이트 모델은 아님 — 상업적 제한 또는 연구 목적 라이선스가 붙은 모델만 해당
- SAM3, BiRefNet 등은 별도 동의 없이 바로 다운로드 가능

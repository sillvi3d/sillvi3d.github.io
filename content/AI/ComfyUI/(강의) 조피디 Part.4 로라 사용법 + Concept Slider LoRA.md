---
title: (강의) 조피디 Part.4 로라 사용법 + Concept Slider LoRA
---

날짜 : 26.04.08
링크 : [ComfyUI 완벽 가이드 강의 Part.4 로라 사용법 + Concept Slider LoRA](https://youtu.be/6m41gY2Tr7s?si=n66nB1YA0Dm3Dj0t)
## 한 줄 요약

- Load LoRA로 로라를 불러올 수 있다
- 모든 로라는 반드시 베이스 모델을 잘 확인하자
## 핵심 내용

- [[LoRA란 무엇인가]]

## 따라한 것 · 실습

1. 로라는 기본적으로 load loRA 노드를 사용해서 불러올 수 있음
	- [Add More Details](https://civitai.com/models/82098/add-more-details-detail-enhancer-tweaker-lora) 로라를 사용해 볼 것임
		- 다운로드 후 > model > loRA 폴더에 넣기
			- 로라별로 civitAI 들어가보면 설명란에 값의 범위를 추천해줌
				- between 0.5 and 1 weight
				- 더 은은한 효과를 원하시면 0.5보다 낮은 가중치를 사용
				- 음수 가중치를 적용했을 때 흥미로운 결과가 나오는 경우도 있다
	- 로라의 구성
		- strength model: 모델에 적용하는 가중치
		- strength clip: 프롬프트에 적용하는 가중치
2. 로라가 있는 워크플로우와 로라가 없는 워크플로우를 비교해보기 위해 이렇게 셋팅을 했다.
	- 이렇게 두 아웃풋이 만들어지는 워크플로우에서 비교할 경우 rgthree의 image compare(rgthree) 노드를 이용하면 편리하다.
		- `Add more detail` 로라를 사용했었다.
		- 슬라이더를 움직여보면 로라를 적용한 쪽의 아웃풋이 훨씬 선명하고 디테일이 있는 것을 볼 수 있다.

`이미지`

![[IMG_txt2img_juggerXL_LoRA-compare_v1.png]]

## 컨셉 슬라이더 로라
- 프롬프트를 수정하지 않고도 원하는 속성을 세밀하게 제어할 수 있는 로라 기술
	- 다양한 종류가 있고 `이름`+ `Slider` 조합으로 되어있다
		<img src="/AI/ComfyUI/assets/Pasted_image_20260408094342.png" width="300" />
		- Civit ai에서 다운받아 사용할 수 있다.
			- 오늘 사용해볼 것은 age silder, emotion slider, skin tone slider이다
				- 이러한 슬라이드 로라들은 상세 페이지를 보면 가중치 범위를 작성해 두었다
					<img src="/AI/ComfyUI/assets/Pasted_image_20260408094537.png" width="300" />
					- [Age Slider](https://civitai.com/models/128417/age-slider)
					- [Emotion Sliders - happy-v1 | Stable Diffusion 1.x LoRA](https://civitai.com/models/119494/emotion-sliders)
					- [Desi Skin Tone Slider +/- (LECO LoRA, SD 1.5, Experimental) - v1.0 | Stable Diffusion 1.x LoRA](https://civitai.com/models/132427/desi-skin-tone-slider-leco-lora-sd-15-experimental)
1. Load LoRA 3개를 쭉이어 3개를 연결한다.
2. 그리고 각 로라 앞에 Primitive 노드를 꺼낸 뒤 strengt_model/clip을 각각 연결한다.
	- 약간 offset값을 abs 노드로 따로 빼서 관리하는 느낌이다.
	- 가시성을 높이기 위한 장치라고 보면 된다.
		- 과거에는 각 노드들에 convert to 위젯을 해줘야 인풋을 받을 수 있는 형태로 바뀌었는데 업데이트 이후에는 바로 인풋을 연결할 수 있는 형태로 바뀌었다.
		- 또한 구 Auto Queue 기능이 현재는 Run 옆에 토글을 열어 선택하는 방식으로 바뀌었다
			- Auto Queue (on Change): 옵션이 변경될 때 자동으로 이미지를 생성하는 옵션이다
			- Auto Queue (instance): 계속 queue
	- -로 갈수록 나이 어려짐

<img src="/AI/ComfyUI/assets/Pasted_image_20260408175837.png" width="600" />
<img src="/AI/ComfyUI/assets/Pasted_image_20260408175911.png" width="300" />
## 내가 추가로 발견한 것

- 로라는 2개가 있는데 두번째 것을 선택해야 clip 인풋이 있음
	- Load LoRA
	- Load LoRA(Model and clip)

- 컴피 UI가 업데이트되면서 UI가 많이 바뀌었다.
	 <img src="/AI/ComfyUI/assets/Pasted_image_20260408171650.png" width="100" />
	- 월/주 단위로 바뀌다보니까 몇년 전 튜토리얼을 봐도 달라진게 많다.
	- 클러드에게 물어보면 바뀐 점을 잘 알려줄 것이다.

- 로라가 작동하지 않는 것 같다면 Base model을 확인하자
	- SDXL의 체크포인트를 쓸 경우(juggernut) -> SD1.5 기반 로라는 사용 안됨
	- 공식: `체크포인트 베이스 = LoRA 베이스`
		- 나같은 경우에도 저거넛을 썼는데 로라 가중치 적용이 안되어 봤더니 해당 문제였다

|구버전|최신 버전|
|---|---|
|`Auto Queue - instant`|**Run (Instant)**|
|`Auto Queue - change`|**Run (On Change)**|
|일반 실행|**Run**|

## 모르는 것 · 나중에 확인

- 
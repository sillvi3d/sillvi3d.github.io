---
title: (강의) 조피디 Part.3 Custom Node 추천 1
---

날짜 : 26.04.06
링크 : [comfyUI 완벽 가이드 강의 Part.3 Custom Node 추천]([https://www.youtube.com/@jopdlab](https://youtu.be/U0hV2UEGo_0?si=JgjCuCRWo65eeJ4c))

##### 한 줄 요약


##### 핵심 내용

1. Custom Script
2. WD14 Tagger
3. rgthree (RG3)
4. KJNode
5. Use Everywhere

##### 따라한 것 · 실습

- 커스텀 노드 설치방법

```
1. Github에서 Custom Node URL 복사하여 설치
2. Github에서 Custom Node 파일 다운로드 후 설치
3. ComfyUI Manager를 사용하여 Custom Nodes 설치
4. ComfyUI Manager를 사용하여 Git URL로 설치
```

- manager > custom node manager

1. Custom Script
	- 세부기능 1) 프롬프트를 작성할 때 emb~ 이라고 치면
		- 내가 보유한 임베딩 리스트를 보여주고 선택하면 자동으로 입력해주어 편리
		<img src="/AI/ComfyUI/assets/Pasted_image_20260406221115.png" width="300" />
	- 세부기능 2) 빈공간 우클릭하면 Arrange 메뉴 2개가 생겨있다
		- 클릭하면 전체 노드를 좌측/우측 기준으로 자동 정렬(정리)해준다
		<img src="/AI/ComfyUI/assets/Pasted_image_20260406221310.png" width="200" />
	- 세부기능 3) 노드의 커스텀 색상을 바꿀 수 있다
		<img src="/AI/ComfyUI/assets/Pasted_image_20260406221413.png" width="200" />
	- 세부기능 4) 워크플로우를 json이 아닌 이미지로 저장
		- json은 용량이 적지만 열어보기 전까지 어떤 워크플로우인지 확인 어렵다
		- 화면 우클릭 > workflow image > png
			<img src="/AI/ComfyUI/assets/Pasted_image_20260406221527.png" width="200" />
		- 이러한 이미지로 저장이 되고
			- 이것을 화면에 드래그하면 바로 불러와진다
				<img src="/AI/ComfyUI/assets/Pasted_image_20260406221617.png" width="200" />

2. WD14 Tagger (WD 태거)
	- 이미지를 분석하여 텍스트로 바꿔주는 기능
	1.  I2I 워크플로우를 꺼내보자
	2. load image에다가 WD14 tagger연결
	3. WD14 tagger의 string을 clip text encode에 연결
	- Queue를 돌려보면 가장 먼저 WD tagger가 이미지를 분석한 뒤 텍스트로 변환하는 것을 볼 수 있다.
		- 결과물을 보면 인풋 이미지와 비슷한 아웃풋이 나온다.
		- 슈퍼미트보이는 프롬프트를 잘 못 쓴다ㅋㅋ
			<img src="/AI/ComfyUI/assets/Pasted_image_20260406223329.png" width="300" />
		- 두번째 이미지는 제법 인풋과 아웃풋이 비슷하다
			<img src="/AI/ComfyUI/assets/Pasted_image_20260406223330.png" width="300" />
			<img src="/AI/ComfyUI/assets/Pasted_image_20260406223430.png" width="200" />
	- 추가 기능) 굳이 queue를 돌리지 않아도 우클릭 > WD tagger 클릭하면 팝업으로 이미지를 분석하여 준다
		<img src="/AI/ComfyUI/assets/Pasted_image_20260406223540.png" width="200" />
		<img src="/AI/ComfyUI/assets/Pasted_image_20260406223556.png" width="200" />
3. rgthree (RG3)
	- 복잡한 워크플로우에서 최종 선택한 노드에 대해서 연결된 노드만 queue하고 싶을 때 사용하여 시간과 리소스를 절약
		- 세부 기능 1) 모든 옵션을 동일하게 설정하고 샘플 수치만 바꾼 2개의 이미지를 비교하려고 한다.
			- 이 상태에서 queue하게 되면 2개의 save이미지가 전부 뽑히는데 특정 한 부분만 queue하고 싶을 때가 있다
				<img src="/AI/ComfyUI/assets/Pasted_image_20260406223829.png" width="300" />
			- 그럴 때 save 이미지 우클릭 > queue selected output nodes (rgthree)
				- 이 save image 노드와 연결된 노드들만 작동하면서 1개의 이미지만 저장된다.
		- 세부기능2) Fast group bypasser(rgthree)
			 - 이 노드는 약간 리모콘 같은 것이다. 별도의 연결은 필요없다.
			 - 그룹을 생성하면 자동으로 노드에 뜨고 
				 - yes는 활성화 no는 비활성화 상태로 바꾼다
				 - 화살표 누르면 해당 그룹으로 이동된다
				 <img src="/AI/ComfyUI/assets/Pasted_image_20260406225008.png" width="300" />
		- 세부 기능 3) Image compare (rgthree)
			- 이미지 2장을 슬라이더로 비교하게 해주는 노드이다
			- A, B 이미지 인풋을 입력한 뒤 플레이버튼을 눌러주거나 queue를 하면 슬라이더로 비교할 수 있다
			 <img src="/AI/ComfyUI/assets/Pasted_image_20260406230455.png" width="300" />


4. KJNode
- 컴피에서 노드를 연결하다보면 굉장히 복잡해질 경우가 많다. 연결선들을 깔끔하게 정리할 필요가 있어진다.
	- 세부기능 1) SetNode/GetNode
		1. SetNode 노드를 꺼내고 constant에 `model`이라고 입력한다
			- 그러면 이름이 Set_model이라고 변경된다
			- Load checkpoint의 model을 set model에 연결한다
		2. Get Node를 꺼내서 constant 클릭 > `model` 선택
			- 그러면 이름이 Get_model이라고 변경된다
				- 노드의 출력도 보라색으로 알아서 변경된다
		3. 이런식으로 직접 연결 없이도 연결이 가능하다.
			- 노드 선이 뒤로 숨지 않아 연결이 직관적이다
				<img src="/AI/ComfyUI/assets/Pasted_image_20260406231209.png" width="400" />

5. Use Everywhere
	- 세부 기능 1) Anything everywhere
		- 연결선없이 원격으로 노드를 연결해주는 노드
		1. Empty latent에 해당 노드를 연결해주니
			- Ksampler의 latent image 인풋에 불이 들어와있는 것을 볼 수 있다
				= `원격으로 연결되었다`
				<img src="/AI/ComfyUI/assets/Pasted_image_20260406231545.png" width="300" />
		2. 더 편한 사용을 위해 좌하단의 setting > Use everything
			- 두개를 바꾸기
				<img src="/AI/ComfyUI/assets/Pasted_image_20260406231854.png" width="200" />
				- 마우스를 올리면 연결선이 애니메이션으로 보임
					<img src="/AI/ComfyUI/assets/Pasted_image_20260406231947.png" width="200" />
				- 만약 인풋을 많이 받고 싶으면 초창기에는 Anything everywhere3라는 별도 노드가 있었는데 지금은 그냥 추가하는대로 계속 포트가 생김
					<img src="/AI/ComfyUI/assets/Pasted_image_20260406232130.png" width="200" />


##### 내가 추가로 발견한 것

- ComfyUI가 업데이트 되면서 Convert Widget to input 기능이 사라졌다.
	- 기존) 노드 우클릭 > convert를 해야 해당 노드에 인풋을 받을 수 있도록 노드가 바뀌었는데
	- 변경 후) 연결선을드래그하여 위젯 가까이에 가져가면 자동으로 연결 포인트가 생긴다.
		<img src="/AI/ComfyUI/assets/Pasted_image_20260406222820.png" width="300" />

- rgthree 현재 가장 최신 버전 다운로드시 관련 노드들이 뜨지 않는데 1.0.2511~ 버전을 사용해보자
	- [관련 레딧](https://www.reddit.com/r/comfyui/comments/1mslljs/clean_and_fresh_install_of_confyui_fast_groups/?show=original)있는 것보니 꽤나 일어나는 이슈인 것 같다.

##### 모르는 것 · 나중에 확인

- 
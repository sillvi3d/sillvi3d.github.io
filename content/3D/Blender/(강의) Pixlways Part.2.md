---
title: (강의) Pixlways Part.2
---

날짜 : 26.04.05
링크 : [pixlway](https://youtube.com/shorts/vMVr58gYp9Q?si=P57Yam_kcmAqthP6)

#blender
##### 한 줄 요약

##### 핵심 내용

##### `F vs J vs K`
- F - **Fill 
	- 선택한 버텍스나 엣지를 기준으로 채워주는 기능인데 상황에 따라 다르게 동작합니다.
		- **버텍스 2개 선택 시** → 두 버텍스 사이에 엣지 생성
		- **버텍스 3개 이상 선택 시** → 선택한 버텍스들을 연결해서 페이스 생성
		- **열린 엣지 루프 선택 시** → 루프를 막아서 페이스 생성
- J - join
	- 같은 페이스 안에 있는 버텍스 2개를 연결해서 페이스를 분할할 때 씀
		- 예를 들어 큰 엔곤 페이스 안에서 버텍스 2개 선택 후 `J` 누르면 그 페이스가 두 개로 쪼개집니다. 
		- 엔곤을 쿼드로 정리할 때 자주 쓰는 방식입니다.

`F` 와 차이점은 `F` 는 엣지나 페이스를 새로 만드는 거고, `J` 는 기존 페이스를 분할하는 개념입니다.

- 저 반구 모양에 면을 쪼갠다고 했을 때
	- F를  쓰면 edge가 face를 자르지 않고 두 버텍스 사이를 연결하기만 함
		<img src="/3D/Blender/assets/Pasted_image_20260405232104.png" width="200" />
	- J를 써줘야 함. J를 쓰면 face가 나눠짐
		<img src="/3D/Blender/assets/Pasted_image_20260405232302.png" width="200" />

- K - knife
	- 아예 칼로 자름. 확실하게 vertex 쪼개짐

###### `bevel 코너 처리 방법`

**Miter Outer / Inner**
- 코너 처리 방식
	- `Sharp` — 날카롭게 처리. 기본값.
		<img src="/3D/Blender/assets/Pasted_image_20260405233140.png" width="200" />
	- `Patch` — 코너를 패치 형태로 처리.
		<img src="/3D/Blender/assets/Pasted_image_20260405233210.png" width="200" />
	- `Arc` — 코너를 호 형태로 둥글게 처리. 튜토리얼에서 쓰는 이유는 코너가 더 자연스럽게 나오기 때문.
		- 둥근 코너에 사용하기 좋음
			<img src="/3D/Blender/assets/Pasted_image_20260405233239.png" width="200" />

##### 따라한 것 · 실습

1. k > c하면 뒷면까지 잘림
	- xray 모드에서 위쪽 절반 face 삭제
	<img src="/3D/Blender/assets/Pasted_image_20260405233534.png" width="300" />
2. fill로 edge들 채우기
	<img src="/3D/Blender/assets/Pasted_image_20260405233620.png" width="300" />
3. 루프 추가
	- ctrl r
		<img src="/3D/Blender/assets/Pasted_image_20260405233639.png" width="300" />
4. J로 면 정리
	<img src="/3D/Blender/assets/Pasted_image_20260405233756.png" width="300" />
5. 루프 추가
	<img src="/3D/Blender/assets/Pasted_image_20260405233837.png" width="300" />
6. J로 면정리 후 버텍스 와이어프레임 정리
	<img src="/3D/Blender/assets/Pasted_image_20260405234005.png" width="300" />
7. s > z > 0한 뒤
	<img src="/3D/Blender/assets/Pasted_image_20260405234048.png" width="300" />
8. 버텍스 스냅으로 아래로 내리기
	<img src="/3D/Blender/assets/Pasted_image_20260405234326.png" width="300" />
9. bevel
	<img src="/3D/Blender/assets/Pasted_image_20260405234442.png" width="300" />
10. J로 면 정리
	<img src="/3D/Blender/assets/Pasted_image_20260405234508.png" width="200" />

##### 내가 추가로 발견한 것

- 

##### 모르는 것 · 나중에 확인

- 
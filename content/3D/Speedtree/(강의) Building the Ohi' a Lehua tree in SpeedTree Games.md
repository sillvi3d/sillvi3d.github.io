---
title: (강의) Building the Ohi' a Lehua tree in SpeedTree Games
---

날짜 : 26.05.09
링크 : [Building the Ohi' a Lehua tree in SpeedTree Games](https://youtu.be/ejEXJnEkBsY?si=VZu2K4qKikiLALQ)
https://kr.pinterest.com/pin/48273027230889153/

## 한 줄 요약

- 유튜브 강의 영상에서는 SpeedTree Games를 사용하여 오하이 레후아(Ohi'a Lehua) 나무를 계획하고, 개별 구성 요소(잎, 꽃, 가지)를 절차적으로 생성하며 텍스처를 베이킹하고, LOD 및 바람 애니메이션, 전역 조명 등 게임 엔진에 최적화된 최종 모델을 조립 및 내보내는 전반적인 과정을 시연함.

## 핵심 내용

1.  실제 나무를 분석하여 SpeedTree 모델링에 적합한 구성 요소(가지, 잎, 꽃 등)로 분해하는 계획 수립.
2.  재사용 가능한 텍스처와 재질 편집기를 활용하여 나뭇가지, 잎, 꽃, 봉오리 등의 세부 요소를 절차적으로 생성하고, 계절 및 자연적 변형을 포함한 텍스처를 베이킹하는 과정.
3.  베이킹된 텍스처 컷아웃(cutout)들을 사용하여 SpeedTree 내에서 게임 모델 트리를 조립하고, 나무의 실루엣과 3D 효과를 구현하는 방법.
4.  SpeedTree 9의 새로운 기능인 Feature Vertices를 포함하여 Radial Segments, Link Segments 등의 조정을 통해 나무 모델의 기하학적 구조를 최적화하고 세부적인 디테일을 추가하는 방법.
5.  Level of Detail(LOD)을 설정하여 카메라 거리에 따라 폴리곤 수를 효율적으로 줄이면서도 나무의 시각적 품질을 유지하는 방법.
6.  나무에 사실적인 바람 애니메이션과 전역 조명(Global Lighting) 효과를 적용하고 조정하는 방법.
7.  최종적으로 게임 엔진(Unity, Unreal Engine)으로 나무 모델을 내보내고, 텍스처 아틀라스(Atlas)를 최적화하는 방법.

## 따라한 것 · 실습

1.  **SpeedTree 모델 계획 수립 (01:15)**
	- 오하이 나무의 구성 요소를 퍼즐처럼 분해하여 계획함.
		- **기하학적 요소 (Geometry)**:
			- 트렁크(Trunk) 및 큰 가지(Big branches): 이들은 지오메트리로 처리되므로 베이킹이 필요 없음.
		- **베이킹이 필요한 요소 (Baked textures)**:
			- 중간 가지(Medium branches): 많은 디테일을 포함하며 폴리곤 절약에 도움.
			- 잔가지(Twigs): 나무 밑동의 '베어(bare)' 효과를 만드는 데 유용.
			- 잎이 달린 작은 가지의 측면 뷰(Side views of little branches with leaf): 나무의 큰 실루엣을 만드는 데 도움.
			- 잎의 상단 뷰(Top view of leaves): 가지 끝의 별 모양 잎을 3D 효과로 표현.
			- 꽃(Flowers)과 봉오리(Buds): 상단 뷰와 측면 뷰를 모두 사용.
	- 계획을 바탕으로 모델링 시작: 잎이 달린 가지의 측면 뷰부터 시작함.

2.  **측면 뷰 가지와 잎 생성 (03:03)**
	- **텍스처 임포트 및 재활용 (03:08)**
		- 새 SpeedTree 씬에서 필요한 텍스처를 모두 임포트함.
		- 이 경우, 유칼립투스 잎 텍스처를 재활용하여 처음부터 다시 만들 필요 없이 유사한 형태를 활용함.
		- Photoshop, Substance Painter 등 외부 툴로 직접 제작하거나 타사 에셋 사용도 가능함.
		- 모든 잎 변형(variants), 계절, 손상(damage) 텍스처가 동일한 Normal, Gloss, Opacity 맵을 공유하여 시간을 절약함.
	- **재질 편집기에서 변형 생성 (03:41)**
		- Material Editor에서 Dead Leaf와 같은 잎 변형을 직접 만들 수 있음.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0345.png" width="300" />
		- 기존 잎의 파라미터를 조정하여 새 잎 모양을 만듦.
	- **가지의 기본 형태인 튜브 생성 (04:34)**
		- `Right Click` > `Add Geometry` > `Tube`를 선택하여 모델 시작. (튜토리얼 학습 시 튜브로 시작하는 것을 권장)
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0437.png" width="300" />
		- 튜브에 바크(bark) 텍스처를 할당함.
		- 작은 디테일이므로 노이즈를 줄이기 위해 타일링(tiling)을 약간 줄임.
		- 가지가 로봇 팔처럼 보이지 않도록 '계단 모양(stair shape)'을 만들어 좀 더 유기적으로 보이게 함.
	- **잎 추가 및 조정 (05:38)**
		- 튜브를 `Right Click` > `Add Geometry` > `Leaf` 선택하여 잎을 추가함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0542.png" width="300" />
		- 텍스처 베이킹 시 소수점 작업을 피하기 위해 모든 것을 크게 스케일업(scale up)하는 것을 선호함.
		- 잎을 태양을 향하도록 정렬함.
		- `Next Generation` 설정을 변경하여 잎이 쌍으로 묶이도록 함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0606.png" width="300" />
		- `Spiral` 값을 추가하여 더 자연스럽게 만듦.
		- 잎이 가지의 조금 더 위쪽에서 시작하고, 가지의 아랫부분은 잎이 없도록 (`Denser`, `Start higher on the branch`) 조정함.
		- 잎의 실루엣을 만듦: 위쪽과 아래쪽 잎은 작게, 중간 잎은 크게 (`Smaller at the top`, `Smaller at the bottom`) 조정함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0640.png" width="300" />
		- 잎에 변형을 추가함: `Fold` 및 `Curl` 속성을 사용하여 잎을 구부림.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0655.png" width="300" />
		- 위쪽의 어린 잎은 덜 구부러지도록 조정함.
		- 잎이 매우 두껍기 때문에 너무 많이 구부러지지 않도록 주의함.
	- **조기 테스트의 중요성 (07:22)**
		- 디테일에 너무 몰두하여 시간을 낭비하지 않도록, 작업물을 자주 테스트할 것을 권장함.
		- 베이킹 후, 간단한 모델을 만들어 엔진(DCC)으로 보내 실제 카메라 뷰와 플레이어 시점에서 어떻게 보이는지 확인함.
		- 아무도 보지 못할 디테일에 시간을 낭비하지 않기 위함. (데드라인이 없다면 최대한 많은 디테일 추가 가능)
	- **재질 할당 및 변형 (08:14)**
		- 재질 세트(Material Set)를 사용하지 않고, 가지의 높이에 따라 특정 변형을 주기 위해 개별 재질을 할당함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0829.png" width="300" />
		- 참조 이미지를 보면 위쪽에는 어린 잎이 많으므로, Pale Green 잎이 위쪽에 오도록 커브를 조정함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0858.png" width="300" />
		- Darker Green 잎은 반대 커브를 사용하여 아래쪽에 나타나도록 함. (커브 복사/붙여넣기 사용)
		- 손상된(Damaged) 잎은 아래쪽에서 더 빨리 나타나도록 커브를 조정함. (복사/붙여넣기)
		- 떨어진(Fall) 잎과 죽은(Dead) 잎도 동일하게 아래쪽에서 더 빨리 나타나도록 조정함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_0947.png" width="300" />
		- 디테일을 미세 조정하여 완벽하게 보이도록 함 (빠른 작업 진행).
		- 직접 촬영한 참조 이미지가 이 과정에서 매우 유용함. 인터넷 사진은 '꾸며진' 경우가 많아 현실적이지 않을 수 있음.
		- 손상된 잎이나 빈 공간을 추가하여 더 현실적으로 보이게 함.
	- **가지 변형 추가 (10:28)**
		- 가지 끝이 카메라를 향하도록 약간 구부려 더 보기 좋게 함.
		- 가지에 범프(bumpy) 효과를 주기 위해 `Lumps` (덩어리)를 추가하여 노멀 맵을 더 흥미롭게 만듦. (죽처럼 보이지 않도록 과하지 않게)
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1050.png" width="300" />
	- **장면 내에서 변형 생성 (11:05)**
		- 단일 가지를 베이킹하면 반복성이 느껴질 수 있으므로, 여러 가지 변형을 한 장면 내에서 직접 생성함.
		- 이는 시간 절약 및 수정 용이성에 매우 효과적임.
		- `Modeler`에서 카메라를 추가하고 그 위치를 저장하는 기능이 새로 추가됨 (추후 시연).
		- **Spine Only 가지 생성 (11:56)**:
			- `Branch`를 추가하고 `Spine Only`로 설정하여 시각적으로 보이지 않게 함. 이는 다른 가지를 지지하는 역할만 함.
			<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1201.png" width="300" />
			- 커브를 사용하여 가지의 위치에 따라 변형을 만듦.
			- `Absolute Steps`를 사용하여 잎이 시작하는 위치를 다르게 조정함 (일부는 낮게, 일부는 높게).
			<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1249.png" width="300" />
			- `Start Angle`도 커브를 사용하여 변경함. 잎이 적은 가지는 더 구부러지게 만듦.
			<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1328.png" width="300" />
		- **잎 밀도 조정 (13:34)**:
			- 잎들이 너무 빽빽하게 붙어있는 것처럼 보이므로, 잎들 사이의 간격(space)을 늘림. (이후 카메라 조정에 용이).
			<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1342.png" width="300" />
			- 일부 잎을 제거하여 더 자연스럽게 보이게 하고, 폴리곤 수를 최적화함.
			- 적은 폴리곤으로도 평평해 보이지 않도록 잎 밀도를 낮게 유지하는 것이 중요함.
			- 엔진으로 내보내 자주 테스트하여 최적의 밀도를 찾음.

3.  **꽃과 봉오리 모델링 (14:50)**
	- **절차적 접근 방식 (15:13)**
		- ZBrush나 DCC에서 모델링 후 SpeedTree로 임포트하는 대신, SpeedTree의 제너레이터(generator)를 사용하여 절차적으로 만드는 것이 더 스마트한 방법임.
		- 절차적 접근 방식을 사용하면 수정(꽃잎 제거/추가)이 매우 쉬움.
	- **봉오리 생성 (16:01)**
		- `Branch`를 사용하여 구형(sphere)을 만듦 (이례적이지만 효과적인 방법).
		- 작은 봉오리(buds)를 생성함. 여름 단계에서 피어날 봉오리들임.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1611.png" width="300" />
		- 유칼립투스 잎 텍스처를 재활용하여 봉오리를 만듦 (추가 작업 없이 재질 편집기에서 색상 변경).
		- 잎의 `Season` 섹션에 있는 `Curl` 속성을 사용하여 봉오리가 피어나도록(bloom open) 만듦.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1651.png" width="300" />
	- **수술(Filament) 생성 (17:19)**
		- `Branch`를 사용하여 필라멘트(수술)를 생성함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1724.png" width="300" />
		- `Gradient`를 적용하여 단색보다 더 깊이감 있는 텍스처를 만듦.
		- 커브를 추가하여 뾰족한 모양 대신 부드러운 모양으로 만듦.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1747.png" width="300" />
		- `Alpha Clip` 때문에 렌더링 시 깜박거리거나 이상하게 보이지 않도록 필라멘트를 참조 이미지보다 약간 두껍게 만듦.
	- **꽃밥(Anthers) 생성 (18:04)**
		- 작은 접시 모양의 노란색 꽃밥(Anthers)을 필라멘트 끝에 생성함.
		- `Branch`를 사용하여 다른 가지 위에 추가하는 방식으로 간단하게 만듦.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1819.png" width="300" />
		- 미세 조정을 통해 로봇 같은 모양이 아닌 더 자연스러운 형태로 만듦.
		- 잎과 마찬가지로 일부 꽃밥을 제거하여 자연스럽게 보이게 함.
	- **계절 변화 테스트 (18:45)**
		- 계절을 변경하며 봉오리가 피어나고, 필라멘트가 나타나며, 겨울에는 모든 것이 시드는지 확인함.

4.  **베이킹된 텍스처 마무리 (19:03)**
	- **텍스처 디테일 편집 (19:05)**
		- 절차적 속성(procedural properties)을 사용하여 모든 것을 만든 후, 텍스처의 완성도를 높이기 위해 개별 편집을 시작함.
		- 잎들이 서로 겹치지 않도록 하고, 밀도가 너무 높지 않으며, 보기 좋게 만듦.
		- `Handy Handy Thing` 툴을 사용하여 디테일을 추가할 수 있음.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_1930.png" width="300" />
		- 잎들을 더 제거하여 숨 쉴 공간을 주고, 실루엣(silhouette)을 더 쉽게 읽을 수 있도록 함.
		- 가지 하나를 제거하여 총 3개의 가지 변형만 남김. (나중에 아틀라스 베이킹 시 각 가지가 더 많은 공간을 확보하도록)
	- **겨울 잎 표현 (20:04)**
		- `Season` 속성의 `Curl`과 `Fold`를 사용하여 겨울 끝 무렵 잎들이 매우 슬프게(sad looking) 보이도록 만듦.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2013.png" width="300" />
	- **카메라 추가 (20:19)**
		- 텍스처 베이킹 전 마지막 단계는 카메라를 추가하는 것임.
		- 베이킹할 뷰 앵글에 자신을 배치한 후, `Camera` 옵션에서 `Drop a camera here`를 선택함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2033.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2036.png" width="300" />
		- 카메라의 `Width`와 `Height`를 조정함. 작은 미리보기 창에 보이는 것이 베이킹될 결과물임.
		- 모든 가지에 대해 동일한 작업을 반복함. 카메라 위치, 폭, 높이는 언제든지 다시 조정할 수 있음.
		- 이전에는 카메라 재설정의 용이성을 위해 탑 뷰(top view)에서 베이킹했지만, 이제는 이럴 필요가 없음.
		- 시네마 모델처럼 지면에서 하늘로 향하는 방식으로 카메라를 배치함.
	- **텍스처 베이킹 (21:41)**
		- `Export Textures`는 매우 쉬움.
		- 내보낼 카메라를 선택하고 `Resolution`을 선택함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2156.png" width="300" />
		- 카메라에서 직접 베이킹하므로 `Aspect Ratio`는 이미 완벽함.
		- 기본적으로 PBR 재질 생성에 필요한 모든 맵이 포함되어 있음. 맵을 추가하거나 제거할 수 있음.
		- 스크립트를 사용하여 특정 목적으로 재질을 내보낼 수도 있음.
		- 모델에 계절 변형이 있으므로, `Spring`, `Summer`, `Fall Transition`, `Fall`, `Winter` 등 모든 계절을 내보내도록 설정함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2242.png" width="300" />
		- (다른 베이킹된 텍스처들 시연: 가지, 탑 뷰, 최적화된 모델용 텍스처)

5.  **컷아웃을 이용한 나무 조립 (23:02)**
	- **구성 요소 배치 계획 재확인 (23:02)**
		- 큰 가지(big branch)는 지오메트리에 부착됨.
		- 그 위에 잔가지(twigs)가 부착됨.
		- 잔가지 위에 잎의 측면 뷰(side views of leaves)가 부착됨.
		- 그 위에 잎과 꽃의 상단 뷰(top view of leaves and flowers)가 컵 모양으로 3D 효과를 주며 부착됨.
	- **SpeedTree 초기 설정 (23:45)**
		- SpeedTree로 돌아와, 트렁크(trunk)와 큰 가지(big branches)를 시각적 지지대(visual support)로 추가함. (최종 메쉬는 동료가 만듦)
		- 베이킹된 모든 텍스처를 임포트하고 `Material Sets`로 그룹화하여 계절별 관리를 용이하게 함.
	- **큰 가지 컷아웃 생성 (24:10)**
		- `Cutout Editor`를 열고 몇 개의 정점(vertices)을 추가하여 가지가 제대로 변형되도록 함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2418.png" width="300" />
		- 게임 모델이므로 불필요한 점은 추가하지 않도록 절제함.
		- 피벗 포인트(pivot point)를 배치하고, 잔가지용 앵커(anchor)를 배치함.
	- **잔가지 컷아웃 생성 및 배치 (24:40)**
		- 동일한 과정으로 잔가지에 정점을 추가하고, 중간에 몇 개를 넣어 접히도록(fold) 함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2446.png" width="300" />
		- 잔가지를 나무에 배치함: 아래 지오메트리와 정렬하여 자연스럽게 나오도록 환영(illusion)을 줌.
		- 큰 가지에 있는 앵커에 잔가지를 배치함.
		- 잔가지들이 모두 위를 향하도록 정렬함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2515.png" width="300" />
		- 이제 봉오리와 잎의 상단 뷰를 위한 앵커를 추가함.
	- **잎, 봉오리, 꽃 컷아웃 생성 및 배치 (25:28)**
		- 잎, 봉오리, 꽃 컷아웃을 생성함.
		- 피벗 포인트는 중앙에 배치함. 그곳이 가지에 부착되어 컵 모양(cup shape)을 만들고 싶은 위치이기 때문.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2539.png" width="300" />
		- 모든 컷아웃을 재질에 할당하여 나중에 계절을 전환할 수 있도록 함.
		- 새로 생성된 컷아웃을 가지 위에 배치함.
		- 언제든지 돌아와서 조정한 것을 수정할 수 있음.
		- 잎을 추가하면 이미 작은 컵 모양이 형성되어 실루엣이 살아나는 것을 볼 수 있음.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2610.png" width="300" />
	- **측면 뷰 잎과 꽃 배치 (26:17)**
		- 잔가지 위에 추가하는 잎의 측면 뷰를 위한 컷아웃을 다시 생성함.
		- 꽃의 탑 베이크(top bake)를 위한 앵커 포인트를 상단에 추가함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2630.png" width="300" />
		- (`Alpha Overdraw`는 게임 엔진에서 비용이 많이 들므로) 빈 공간이 너무 많지 않도록 텍스처에 따라 컷아웃을 재조정하는 경우가 있음.
		- 측면 뷰와 꽃을 그 위에 추가하여 모든 각도에서 잘 보이도록 함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2655.png" width="300" />
	- **변형 적용 및 시즌 테스트 (27:00)**
		- 마지막 변형에 대해 동일한 과정을 반복함.
		- 텍스처 예산이 부족한 경우, 너무 많은 변형은 아틀라스 공간을 줄이므로, 2~3가지 유형의 가지로도 충분할 수 있음.
		- 컷아웃 배치 완료 직전, 값에 변형(variance)을 추가하여 더 자연스럽게 보이도록 함.
		- 시즌을 테스트하여 모든 것이 올바른지 확인함.

6.  **최종 마무리 및 최적화 (27:59)**
	- **트렁크 및 메인 가지 조정 (28:08)**
		- `Radial Segments`가 낮아 거친 그림자가 생기는 문제를 해결함.
		- `Segments` 탭에서 `Radial Segments`를 `Scribe` 모드로 변경하여 삼각형을 확인.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2844.png" width="300" />
		- 플레이어 높이(Player Height)에서 중요하므로, 트렁크 하단에 `Radial Segments`를 더 추가하여 폴리곤을 늘리고, 상단에는 줄임.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2905.png" width="300" />
		- `Link Segments`가 하단에서 울퉁불퉁하게 보이는 문제를 해결하기 위해, `Big Branches`의 `Link Segments`를 하단에 몇 개 더 추가하고 모두 나무 밑동(base)으로 몰아 부드러운 곡선을 만듦.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_2932.png" width="300" />
		- `Radial Weld` 영역에서도 세그먼트를 줄여 폴리곤을 절약할 수 있음. `Scaler` 값을 낮춤.
		- 다음 계층(tier)에서는 `Weld`를 끄고 `Skin Tab`을 활성화하여 폴리곤을 절약함.
		- 메인 가지의 `Extension` 때문에 상단에 불필요한 폴리곤이 생기는 경우, `Segments` 탭에서 `Radial Segments`를 줄임.
	- **Feature Vertices 사용 (SpeedTree 9 신기능) (30:51)**
		- 이 기능은 높이 맵(height map)을 기반으로 특정 영역에 추가 정점을 생성하고 당기거나 밀어 넣어 세부 디테일을 추가하면서, 나머지 가지는 최적화를 유지하는 기능임.
		- **커스텀 맵 가져오기**: 디테일이 적은 단순한 Upright/Cavity 맵을 가져와 사용함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3137.png" width="300" />
		- **바크 컷아웃에 적용**: `Cutout` 탭에서 바크 재질의 `Edit` 버튼을 누름.
		- `Show Height`를 활성화하여 가져온 맵을 확인.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3154.png" width="300" />
		- `Add Area`를 선택하고 흰색의 `High` 영역 섹션을 잘라내어 약간의 범프(bump) 영역을 만듦.
		- `Tessellation Slider`를 사용하여 높은(High), 중간(Medium), 낮은(Low) 디테일을 설정함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3227.png" width="300" />
		- **기능 활성화**: 각 제너레이터의 `Segment` 탭에서 `Features Mesh Enabled`를 선택하여 활성화함. 많은 폴리곤이 나타나는 것을 볼 수 있음.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3247.png" width="300" />
		- `Repeat Tile`도 여기서 나타남.
		- `Stitching Style`을 `Preserve Cross Section` 또는 `No New Segments` 등으로 변경하여 블렌딩을 조정함. (서로 전환하며 테스트 필요)
		- `Displacement` 설정: `Height Map`이 재질에 맞춰 `Fit to Geometry`로 설정됨.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3404.png" width="300" />
		- `Displacement`를 밀어 올리면 특정 영역에서 훨씬 더 많은 디테일이 나타나는 것을 볼 수 있음.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3435.png" width="300" />
		- 이 디테일이 나무 상단으로 계속 이어지는 것을 원하지 않으면, `Segment` 탭에서 `Keep Chance`를 사용하여 나무 상단에서 기능을 끌 수 있음.
		- 게임 트리는 일반적으로 이 기능을 두 번째 계층에는 적용하지 않음 (비용 절약).
		- (텍스처를 켜고 Displacement를 과장하여 효과 확인)
	- **형태 조정 (35:08)**
		- `Shape Displacement`를 조정하고, 약간 `Twist`를 주거나 `Flares`를 추가하여 모양을 조정함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3519.png" width="300" />
		- 나무가 땅속으로 잘 들어가도록 `Offset`을 조정하고, `Skin Tab`을 사용하여 밑동을 닫아 빈 공간이 보이지 않도록 함.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3541.png" width="300" />
	- **다양한 변형 추가 (36:02)**
		- 나무를 더 사실적으로 만들기 위해 `Spine` 탭에서 `Angles`와 `Parent Curl` 설정에 `Variance`를 추가하여 더 유기적인 모양을 만듦.
		<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3625.png" width="300" />

7.  **LOD(Level of Details) 설정 (36:50)**
	- **LOD 활성화**: `Global Properties`에서 `LODs`를 켬. (기본 3단계, 최대 6단계 가능)
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3840.png" width="300" />
	- 모든 컷아웃에 대해 `High`, `Medium`, `Low` 세트를 만듦. (이 과정은 빠르게 진행)
	- `Slider`를 스크럽하여 LOD 전환을 확인.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_3858.png" width="300" />
	- **LOD 조정**: `Big Branches`의 `Weight`를 낮추고 `Scale`을 줄여 크기를 약간 작게 함.
	- `Screen Area Closer`와 `Far`를 사용하여 전환 지점을 조정하여 자연스러운 LOD 전환을 만듦.
	- 클러스터(Cluster) 재질(잎)의 `Weight`를 더 공격적으로(aggressively) 낮추고, 개수를 줄임.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4002.png" width="300" />
	- `Main Shape` 잎(큰 잎)은 다른 3D 잎보다 더 유지되도록 `Weight`를 높임.
	- (조정 과정 시연: `Weight`와 `Scale`을 반복적으로 변경하며 균형을 찾음)
	- 커브를 사용하여 나무를 따라 `Weight`를 조정함. (예: 아래쪽 잎에 더 강조를 주고 위쪽은 줄임)
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4134.png" width="300" />
	- **반복적인 테스트**: 뒤로 물러서서 무엇이 보이는지, 보이지 않는지 확인하고 `Weights`와 `Curves`를 조정함.
	- `Segments`를 줄이는 커브를 가지를 따라 적용하고, 중요한 부분이 이상하게 보이거나 깨지면 세그먼트를 추가하며 조절함.
	- 목표: 25,000 폴리곤의 나무를 3,000 폴리곤으로 줄이면서도 실루엣을 보존하는 것.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4247.png" width="300" />

8.  **바람 설정 (43:03)**
	- **바람 활성화**: 상단 `Fan` 아이콘을 `Right Click`하여 `Turn the wind on`을 선택하거나 `Property Tab`의 `Wind` 섹션에서 활성화함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4308.png" width="300" />
	- `Legacy Unity Unreal Engines`를 선택하여 유니티/언리얼 엔진용으로 설정함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4316.png" width="300" />
	- **Wind Wizard 사용**: `Wind Wizard`를 실행하여 클러스터 텍스처들이 잎인지 확인시킴.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4331.png" width="300" />
	- (텍스처 이름이 통일되어 있지 않다면 재명명 권장)
	- 움직이지 않아야 할 부분(예: 맨 밑의 가지)의 바람을 끔. (Leaf 6, 7 등)
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4411.png" width="300" />
	- (일부 가지는 다른 요소를 지지하므로 바람이 적용될 수 있으나, 너무 심하면 조정)
	- `Legacy Weight`를 약간 낮춰 움직임의 강도를 조절함.
	- 가지에도 애니메이션이 적용되었는지 확인함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4446.png" width="300" />
	- **가지 바람 조정**: `Wind` 탭에서 `Height Exponent`를 변경하여 가지의 흔들림을 조정함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4505.png" width="300" />
	- `Distance`와 `Frequency`를 늘려 상단 가지가 더 많이 흔들리도록 함.
	- `Global Height Exponent`는 바람이 나무의 어느 높이에 영향을 미치는지 결정함. (높으면 상단, 낮으면 하단 움직임)
	- 첫 번째 튜브(trunk)에는 Global Wind 설정이 이미 움직임을 주므로, 두 번째 및 세 번째 계층에 바람을 전략적으로 배치하는 것이 더 효과적임.
	- (계속 조정하며 원하는 움직임을 만듦)
	- 커브의 끝은 강한 바람 설정(hurricane level)을 나타냄. 강한 바람에서 이상해 보인다면 `Distance`와 `Frequency`를 낮춤.

9.  **글로벌 조명 컨트롤 (SpeedTree 9 신기능) (46:44)**
	- **문제점**: `Normal`을 켰을 때, 클러스터들이 균일하게 밝게 조명되어 실제 트렁크와 밝기 차이가 나는 문제를 해결함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4704.png" width="300" />
	- 이전 버전에서는 각 클러스터에 개별적으로 조명 조정을 했음.
	- **전역 조명 적용**: 조명 조정을 할 잎/꽃 제너레이터를 모두 선택한 후, `Lighting` 탭으로 이동하여 `Global`을 선택함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4750.png" width="300" />
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4751.png" width="300" />
	- 이는 나무의 영역(areas)을 기반으로 `Per Set` 조정을 가능하게 함.
	- `Large` 또는 `Huge` 설정을 사용하면 노멀들이 원형으로 퍼지도록 회전함.
	- `Roll out normals`를 밀어서 모든 노멀들이 바깥쪽으로 향하도록 함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4815.png" width="300" />
	- (노멀을 끄고 실제 클러스터 조명이 어떻게 보이는지 확인)
	- HDRP(HDRP)가 너무 밝다면 끌 수 있음.
	- **개별 조정**: 특정 요소(예: 꽃)는 개별적으로 원하는 방향으로 향하도록 조정할 수 있음.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_4847.png" width="300" />
	- 각 계층 또는 잎에 대해 `Global` 또는 `Legacy` (로컬 컨트롤 포함) 중 필요한 조명 설정을 적용함.

10. **최종 익스포트 및 변형 (49:18)**
	- **나무 변형 만들기**: 게임에 사용할 여러 변형을 만듦.
		- `Freehand Edits`를 사용하여 특정 용도(specific use case)에 맞게 만듦.
		- 크기를 줄여 관목(shrubby) 형태의 낮은 캐노피 버전을 만듦.
		- 여러 트렁크(multiple trunk)를 가진 버전을 만들 수도 있음.
		- 이 프로젝트에서는 2~3개의 작은 식물과 큰 데스크탑 버전을 만들었음.
	- **게임 엔진으로 내보내기**: `Export to Game`을 선택함.
	- `ST` (SpeedTree Unity 파일) 형식으로 내보냄.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_5011.png" width="300" />
	- `Show Atlas`를 통해 내보낼 텍스처 아틀라스를 미리 볼 수 있음.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_5023.png" width="300" />
	- 아틀라스 공간을 절약하려면, `Variations`를 포함하지 않도록 설정할 수 있음. (계절 전환이 원인으로 보임)
	- `Allow Wrapping`을 활성화하여 텍스처 공간을 최적화함.
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_5102.png" width="300" />
	- `Packaging for Unity`를 선택함.
	- `Presets`에서 `Unity preset` 또는 `Unity One Draw Call` (아틀라스에 모든 것을 넣는 현재 방식)을 선택할 수 있음.
	- `OK`를 눌러 내보냄.
	- (내보낸 나무를 Unity HDRP 샘플 씬에서 확인하는 모습)
	<img src="/3D/Speedtree/assets/yt_Building_the_Ohi'_a_Lehua_tree_in_SpeedT_5136.png" width="300" />

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
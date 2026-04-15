---
title: (강의) Flower Power Part 2
---

날짜 : 26.04.14
링크 : [Flower Power: Part 2](https://www.youtube.com/live/zCIC99fsxc?si=eHEfYptw-L1VQ2)

## 한 줄 요약

- 속도 트리를 사용하여 고폴리 VFX 꽃 모델을 저폴리 게임용 모델로 최적화하고, 클러스터 파일을 만들어 텍스처 아틀라스 및 3D 효과를 구현하며, 다양한 모델링 기법으로 세부적인 외형을 조정하는 과정을 설명함.

## 핵심 내용

1.  **VFX 모델 최적화**: 고폴리 VFX 모델을 게임에 적합한 저폴리곤 모델로 변환하는 일반적인 전략을 설명함.
2.  **클러스터 파일 생성 및 활용**: 꽃의 특정 부분을 2D 텍스처 클러스터로 만들어 메인 모델에 부착하여 폴리곤 수를 절감하고 효율성을 높이는 방법을 시연함.
3.  **UI 조작 및 최적화 기법**: Batch Leaves를 Leaf Mesh로 변환, Trunk, Segment, Skin 탭의 다양한 속성(Radial, Weld Scaler, Pruning)을 조정하여 폴리곤 수를 줄이는 방법을 상세히 다룸.
4.  **앵커 포인트 활용**: 클러스터 텍스처에 앵커 포인트를 설정하고, 이를 활용하여 메인 모델에 꽃잎, 꽃, 스템 등 다양한 부품을 정확한 위치와 방향으로 부착하는 방법을 설명함.
5.  **디테일 조절 및 현실감 부여**: Cutout Editor를 이용한 폴리곤 최적화, Geometry 탭의 Fold, Curl, Gravity, Ancestor, Variance 설정을 통해 꽃잎과 꽃의 모양에 현실적인 변화를 주는 방법을 보여줌.
6.  **SpeedTree 9 신규 기능 소개**: 검색 바, 오류 알림, Freehand 모드 (줄기 모양을 빠르게 조절) 등 SpeedTree 9에서 추가된 편리한 기능들을 간략히 소개함.

## 따라한 것 · 실습

1.  **인트로 및 작업 목표 설정**
	- 지난주에 만든 189,000 폴리곤의 거대한 VFX 꽃 모델을 게임에 최적화하는 것을 목표로 함.
	- SpeedTree 9을 사용하나, 대부분의 기능은 SpeedTree 8에서도 적용 가능함을 언급함.
	<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1200.png" width="300" />
2.  **프로젝트 저장 및 초기 폴리곤 확인**
	- 현재 파일을 `File > Save As`로 `hero_plant`라는 이름으로 저장함.
	- 현재 폴리곤 수가 189k임을 확인.
	<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1445.png" width="300" />
	<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1450.png" width="300" />
3.  **VFX 꽃 모델 최적화 시작**
	1.  **불필요한 디테일 제거**
		- `Node Editor`에서 "little details"에 해당하는 노드들을 선택하고 `Delete` 키를 눌러 삭제함. 이는 폴리곤 수가 매우 높기 때문임.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1515.png" width="300" />
	2.  **Batch Leaves를 Leaf Mesh로 변환**
		- `Node Editor`에서 모든 `Batch Leaves` 노드를 선택함.
		- 선택된 노드 중 하나를 `Right-click > Convert To Leaf Mesh`를 선택하여 Leaf Mesh로 변환함.
		- 이 과정은 게임 모델에서 폴리곤을 크게 절감하는 중요한 단계임.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1547.png" width="300" />
	3.  **추가적인 잎/가지 정리**
		- "extra leaves" (작은 팔/돌기) 노드들을 삭제함.
		- 남아있는 잎 노드의 `Gen` 탭으로 이동하여 `Length` 및 `Start Angle` 등의 설정을 조절하여 잎의 위치를 아래로 이동시키거나 형태를 조정함.
		- "frond holders" (꽃을 지탱하던 가지) 노드들을 삭제함. 이는 폴리곤 수가 높기 때문임.
		- 메인 꽃/줄기 수를 줄임.
	4.  **꽃 줄기 길이 및 형태 조정**
		- 꽃 노드의 `Spine` 탭으로 이동하여 `Length` 커브를 최대로 올려 길이를 거의 일정하게 만듦. (꽃들이 사라지거나 길어지는 현상 방지).
		- "little tiny inside petals" 노드들을 삭제함.
		- 꽃 노드의 `Geometry` 탭에서 `Gravity`, `Fold`, `Curl` 값을 조정하여 너무 과도하게 휘거나 접힌 형태를 완화함.
		- 가지/꽃 노드에 적용되었던 `Force` 및 `Ancestor` 설정을 제거하거나 비활성화함.
		- `Spine` 탭에서 `Start Angle`을 조절하여 꽃의 시작 각도를 변경하고 전체적인 형태를 다듬음.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1742.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_1950.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_2035.png" width="300" />
4.  **클러스터 파일 생성 (상단 꽃 텍스처)**
	1.  **새 파일 열기 및 저장**
		- `File > Open`을 선택하여 지난주에 사용한 `larkspur` 파일을 다시 염.
		- `File > Save As`를 선택하여 `cluster`라는 이름으로 저장함.
	2.  **클러스터 모델 준비**
		- `Node Editor`에서 모든 잎과 불필요한 디테일 노드를 삭제함.
		- `Viewport`에서 `XY Plane`을 선택하여 뷰포트를 평면으로 전환함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_2330.png" width="300" />
		- `Trunk` 노드를 선택하고 `Spine` 탭으로 이동하여 `Start Angle` 값을 조절(예: 0.5)하여 모델 전체를 옆으로 눕힘. 위에서 바라보는 텍스처를 만들기 위함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_2357.png" width="300" />
		- 남아있는 꽃/꽃잎의 `Phyllotaxy` (예: `Opposite`) 및 간격을 조정함.
	3.  **꽃잎 가지치기 및 형태 조정**
		- `Spine` 탭으로 이동하여 `Pruning > General Pruning` 설정을 사용하여 대부분의 꽃잎을 제거하고, `Trunk`에 가까운 상단 몇 개만 남김. 이 커브를 복사하여 다른 꽃잎 노드에도 붙여넣어 일관된 가지치기를 적용함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_2708.png" width="300" />
		- 필요한 경우 개별 꽃잎 노드의 `Gin > Knockout` 설정을 사용하여 특정 꽃잎을 수동으로 제거함. (노드가 `extent only`로 설정된 경우 `Knockout`이 작동하지 않을 수 있음을 주의).
		- 작은 꽃 중앙 부분의 `Skin` 탭에서 `Edit`을 클릭하여 크기를 줄임.
	4.  **텍스처 크기 설정 및 내보내기**
		- `Global Properties > Window Properties > Show`를 선택하여 화면 공간을 확인하고, 텍스처 크기를 조정함(예: 2048x2048과 같이 길고 얇은 비율로 조정하여 아틀라스에 효율적으로 배치).
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3043.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3050.png" width="300" />
		- `File > Export Material`을 선택하여 클러스터 텍스처를 내보냄.
			- 비율이 일치하는지 확인.
			- `Strength Colors`가 켜져 있는지 확인 (알파 채널이 올바르게 색상을 가지도록).
			- 모든 PBR 맵을 내보냄.
			- `clusters` 폴더에 `new_cluster_top_flower`와 같은 이름으로 저장함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3105.png" width="300" />
	5.  **SpeedTree 9 신규 기능 소개**
		- `Property` 창에 검색 바가 추가되어 특정 속성을 빠르게 찾을 수 있음을 언급함 (V8에는 없음).
		- 느낌표 아이콘 형태의 오류 알림 기능이 추가되어 문제 발생 시 해결 방법을 자세히 안내함을 언급함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3158.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3217.png" width="300" />
5.  **클러스터 파일 통합 (Hero Tree)**
	1.  **메인 줄기 조정**
		- `hero_plant` 파일로 돌아옴.
		- `main stem` 노드를 선택하여 길이를 조금 줄임.
		- `Trunk` 노드의 `Extend` 속성을 `None`으로 설정함.
	2.  **Leaf Mesh 추가 및 텍스처 적용**
		- `Generators` 탭에서 `Add Leaf Mesh`를 클릭하여 새로운 `Leaf Mesh` 노드를 추가함.
		- `Leaf Mesh` 노드의 `Generate` 탭에서 `Absolute`를 `0`으로 설정하고 `Parent`를 `Extension`으로 설정하여 줄기 끝에 부착되도록 함.
		- `Material` 탭에서 `Import`를 클릭하여 방금 생성한 `new_cluster_top_flower` 텍스처를 가져옴.
		- `Material` 탭에서 `Two-sided`를 활성화함.
	3.  **Cutout 설정 및 앵커 정의**
		- `Material` 탭에서 `Cutout > Edit`을 클릭함.
		- `Pivot Point`를 줄기와의 연결 지점에 배치함.
		- 최소 폴리곤을 위한 컷아웃 형태를 정의함 (예: 직선).
		- 꽃 부착을 위한 앵커 포인트를 정의함.
			- `Anchor 1`: 양쪽에서 나오는 꽃을 위해 외부를 향하는 방향으로 앵커를 배치.
			- `Anchor 2`: 중앙에 배치되는 꽃을 위해 직선으로 향하는 앵커를 배치.
			- `Anchor 3`: 상단에 배치되어 2D 텍스처를 가리는 꽃을 위해 약간 더 말린 형태로 앵커를 배치.
		- `Save`를 클릭하여 컷아웃 설정을 저장함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3602.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3815.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_3945.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_4048.png" width="300" />
	4.  **클러스터 위치 및 형태 조정**
		- `Leaf Mesh` 노드의 `Size`를 조절하여 클러스터의 크기를 맞춤.
		- `Orientation` 탭에서 `Sky Influence`를 높여 클러스터가 위를 향하도록 조절한 후, `Final Adjustments`를 사용하여 정확한 위치와 각도로 배치함.
		- 기존 꽃 (`Tube` 노드)의 `Start Angle`을 조정하여 클러스터와 줄기의 연결 부위를 가리도록 위로 밀어 올림.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_4207.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_4215.png" width="300" />
6.  **폴리곤 수 최적화 - 추가 조정**
	1.  **메인 줄기 최적화**
		- `main stem` 노드 선택 > `Segment` 탭 > `Scribe` 항목으로 이동.
		- `Link Segments` 값을 줄임.
		- `Weld Scaler` 값을 줄임.
		- `Radial Segments`를 `0` 또는 `1`과 같이 매우 낮은 값으로 줄임.
		- `Weld Offset` 값을 조정하여 텍스처가 늘어나거나 깨지는 아티팩트를 방지함.
		- `Tip` 세그먼트 수를 줄여 끝 부분을 최적화함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_4550.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_4640.png" width="300" />
	2.  **꽃잎 최적화 (개별 Leaf Mesh)**
		- 각 `petal Leaf Mesh` 노드를 선택 > `Cutout > Edit`.
		- 기존 컷아웃을 `Clear`함.
		- 훨씬 더 간단한 저폴리곤 컷아웃 (예: 3점 삼각형)을 새로 만듦.
		- 앵커 포인트를 꽃잎의 기저부에 설정함.
		- 필요한 경우 `Low`, `Medium`, `High` LOD 컷아웃을 정의함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_4905.png" width="300" />
	3.  **꽃잎 형태 및 현실감 조정**
		- `Geometry` 탭에서 `Gravity`, `Fold`, `Curl` 값을 조정하여 저폴리곤 컷아웃으로 인해 발생할 수 있는 각진 형태를 완화함.
		- `Ancestor` 및 `Curve` 설정을 확인하고 필요에 따라 조정하여 원치 않는 형태를 방지함.
		- `Start Angle`에 `Variance`를 추가하여 꽃잎들이 동일하게 보이지 않도록 자연스러운 변화를 줌.
		- `Cohesive` 옵션을 활성화하여 `Variance`가 꽃잎 개별이 아닌 꽃 전체에 적용되도록 함.
7.  **개별 꽃 클러스터 파일 생성**
	1.  **새 파일 열기 및 저장**
		- 기존 파일을 열고 `File > Save As`를 선택하여 `flower_cluster`라는 이름으로 저장함.
	2.  **클러스터 모델 준비**
		- 메인 줄기를 숨김.
		- `Trunk` 노드의 `Generation` 탭에서 `Interval`을 `1`로 설정하여 하나의 꽃/꽃잎만 남김.
		- 꽃 줄기 (`Tube` 노드)를 늘려 꽃의 적절한 크기를 만듦.
		- `Gin` 탭에서 `Rotation`을 사용하여 꽃잎이 위를 향하도록 회전함.
		- `Forks`에서 `Force`를 삭제함.
		- 꽃잎 (`petal`)의 `Spine > Start Angle`, `Ancestor`, `Curve` 설정을 조정함.
		- `Node Mode`를 사용하여 꽃잎들을 배열하거나 `Gin > Rotation`의 `Spiral` 설정을 사용하여 나선형으로 배치함.
		- 꽃잎이 `Batch Leaves`인 경우 `Convert to Leaf Mesh`로 변환함.
		- `Geometry` 탭에서 `Curl` 및 `Fold` 설정을 조정하여 꽃잎이 과도하게 말리지 않고 평평하게 보이도록 함.
		- `Tube` 노드의 `Spine > Length` 커브 (예: 1.01)를 조정하여 말린 꽃잎을 폄.
		- 꽃 중앙에 작은 지지대 또는 중심 부분을 배치함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_5740.png" width="300" />
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_6058.png" width="300" />
	3.  **텍스처 내보내기**
		- `File > Export Material`을 선택하여 `flower_cluster_texture`라는 이름으로 저장함.
		- (미리 만들어둔 클러스터: 중앙 부분이 말려 3D 효과를 내는 클러스터도 보여줌.)
8.  **개별 꽃 클러스터 통합**
	1.  **Leaf Mesh 추가 및 텍스처 적용**
		- `hero_plant` 파일로 돌아옴.
		- `Material` 탭에서 `Import`를 클릭하여 `flower_cluster_texture`를 가져옴.
		- `Material > Cutout > Edit`을 클릭.
			- 앵커를 중앙에 설정.
			- 접고 구부릴 수 있는 기본 형태를 정의.
		- `Generators` 탭에서 `Add Leaf Mesh`를 클릭하여 새로운 `Leaf Mesh` 노드를 추가함.
		- `Material`을 방금 가져온 `flower_cluster_texture`로 설정함.
		- `Two-sided`를 활성화함.
	2.  **위치 및 형태 조정**
		- `Size`를 조절하여 꽃의 크기를 맞춤.
		- `Orientation` 탭에서 `Sky Influence` 및 `Final Adjustments`를 사용하여 꽃의 위치를 조절함.
		- `Fold` 및 `Curl` 값을 조정하여 꽃 모양을 만듦.
		- `Gin` 탭에서 `Anchor`를 `1`로 설정하여 이전에 정의한 `Anchor 1` 위치에 꽃이 배치되도록 함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_6755.png" width="300" />
	3.  **클러스터 베이스 앵커 조정**
		- `base texture` (이전 클러스터)의 `Cutout > Edit`으로 돌아가 불필요한 앵커 포인트를 삭제하여 혼잡도를 줄임.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_6910.png" width="300" />
9.  **작은 줄기/내부 부품 클러스터 생성**
	1.  **새 파일 열기 및 저장**
		- 새 파일을 열고 `File > Save As`를 `stem_parts_cluster`라는 이름으로 저장함.
	2.  **클러스터 모델 준비**
		- `Viewport`에서 `XY Plane`을 설정함.
		- `Lighting`을 `Standard`로 변경하여 가시성을 높임.
		- `Add Trunk`를 클릭하여 `Trunk` 노드를 추가함.
		- `Spine > Length`를 `0.5`로, `Start Angle`을 `0.5`로 설정하여 줄기를 평평하게 눕힘.
		- 원하는 각도로 회전함.
		- `Skin` 탭 > `Profile Curve`를 사용하여 매우 작게 만듦.
		- 여러 세그먼트(예: 3개)를 추가하여 구부릴 수 있도록 함.
		- `W` 키 (스크린 공간 이동)를 사용하여 여러 개의 작은 줄기 모델을 배치하여 아틀라스 패킹을 위해 정렬함.
		- `E` 키 (스크린 공간 회전)를 사용하여 회전함.
		- **SpeedTree 9 Freehand Mode**: `Generators > Freehand Mode > Bend Tool`을 사용하여 줄기 모양을 빠르고 자유롭게 구부려 만듦. (SpeedTree 8에서는 `Spine > Late Noise`를 사용하여 유사한 효과를 낼 수 있음).
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_7400.png" width="300" />
	3.  **텍스처 내보내기**
		- `File > Export Material`을 선택하여 `stem_parts_cluster_texture`라는 이름으로 저장함.
10. **작은 줄기/내부 부품 클러스터 통합**
	1.  **Leaf Mesh 추가 및 텍스처 적용**
		- `hero_plant` 파일로 돌아옴.
		- `Material` 탭에서 `Import`를 클릭하여 `stem_parts_cluster_texture`를 가져옴.
		- `Material` 탭에서 `Add` 버튼을 클릭하여 세 개의 컷아웃을 추가함.
		- 각 `Cutout > Edit`을 클릭.
			- 단일 삼각형 모양을 만듦.
			- `Pivot Point`를 기저부에 설정하고 방향을 맞춤.
		- `Generators` 탭에서 `Add Leaf Mesh`를 클릭하여 새로운 `Leaf Mesh` 노드를 추가함.
		- `Material`을 `stem_parts_cluster_texture`로 설정하고 `Two-sided`를 활성화함.
		- `Gin` 탭에서 `Anchor`를 `2`로 설정하여 `Anchor 2` 위치에 배치되도록 함.
	2.  **위치 및 형태 조정 (3D 효과)**
		- `Size`를 조절하고 `Orientation > Sky Influence`, `Final Adjustments`, `Fold`, `Curl`을 사용하여 배치함.
		- 이 `Leaf Mesh` 노드를 `Copy`하여 `Paste`함.
		- 복사된 노드의 `Orientation`을 조정하여 첫 번째 세트와 반대 방향으로 회전시켜 거울상으로 배치, 3D 효과를 만듦. `Variance`를 추가하여 너무 대칭적이지 않게 함.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_8200.png" width="300" />
11. **상단 봉오리 (Cluster Anchor 3) 통합**
	1.  **Leaf Mesh 추가 및 텍스처 적용**
		- 기존 `Leaf Mesh` (예: 꽃 클러스터)를 `Copy`하여 `Paste`함.
		- `Gin` 탭에서 `Anchor`를 `3`으로 설정함.
	2.  **형태 및 크기 조정**
		- `Fold`, `Twist`를 조절하여 봉오리 형태를 만듦.
		- `Skin` 탭에서 `Size > Along Trunk` 커브를 사용하여 봉오리들이 위쪽으로 갈수록 작아지도록 크기를 조절함.
		- `Variance`를 추가하여 봉오리의 모양을 다양하게 만듦.
12. **최종 조정 및 간격 채우기**
	1.  **앵커 포인트 추가**
		- `base texture` (메인 클러스터 텍스처)의 `Cutout > Edit`으로 돌아가 `Anchor 2` (내부 줄기)에 앵커 포인트를 더 추가하여 간격을 채움.
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_8750.png" width="300" />
	2.  **불필요한 부분 제거**
		- 특정 `Leaf Mesh` (예: Leaf 2 - 줄기)의 `Gin > Knockout` 설정을 `According to Leaf 2` (또는 `Trunk`)로 조정하여 하단의 과도한 부분을 제거함.
	3.  **전체적인 형태 및 현실감**
		- `Frond` 노드의 `Curl`과 `Length` (`Skin > Along Trunk`)를 조정하여 전체적인 꽃의 형태와 현실감을 높임.
		- 꽃/꽃잎의 `Fold`, `Curl`, `Twist`, `Face`에 `Variance`를 추가하여 단조로움을 깨고 자연스러운 모습을 연출함.
	4.  **최종 폴리곤 확인**
		- 최종 폴리곤 수를 확인하고 추가적인 최적화가 필요한 경우, `Leaf` 노드의 최적화나 LOD (Level of Details) 설정을 통해 진행할 수 있음을 언급함 (LOD는 추후 스트림에서 다룰 예정).
		<img src="/3D/Speedtree/assets/yt_Flower_Power__Part_2_9010.png" width="300" />

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
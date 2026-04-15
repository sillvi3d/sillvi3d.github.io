---
title: (강의) Flower Power  Part 1
---

날짜 : 26.04.14
링크 : [Flower Power | Part 1](https://www.youtube.com/live/tvMuF9_bHyY?si=rHwmj72hWX68Eh9V)

## 한 줄 요약

- SpeedTree v9 (v8 호환)을 사용하여 하이폴리곤 델피늄(Larkspur) 꽃 모델을 만드는 상세한 튜토리얼로, 줄기, 잎, 꽃잎, 수술 등 각 부분의 생성부터 디테일 조정 및 컬러 바리에이션 적용 방법까지 다룸.

## 핵심 내용

1.  SpeedTree에서 나무 구성 요소를 활용하여 복잡한 꽃 모델을 제작하는 방법.
2.  줄기, 잎, 꽃잎, 수술 등 식물 각 부분의 모델링 및 텍스처 적용 과정.
3.  `Skin`, `Generation`, `Spine`, `Material`, `Forces` 탭 등 SpeedTree UI의 주요 기능 활용법.
4.  `Weld`, `Phyllotaxy`, `Planar Force`, `Parent Curls` 등 고급 모델링 기법을 이용한 디테일 추가.
5.  `Weight` 기능을 활용하여 꽃잎 색상의 자연스러운 그라데이션 및 분포를 구현하는 방법.
6.  모델링 중 발생할 수 있는 문제점 (예: 브랜치가 보이지 않는 경우, 충돌) 해결 방안.
7.  Generator 모드와 Node 모드의 차이 및 사용 시기, LOD(Level of Detail) 관리의 중요성.

## 따라한 것 · 실습

1.  **SpeedTree v9 준비 및 초기 설정**
    *   SpeedTree v9 (v8 호환 가능)을 사용하며, PBR 텍스처는 미리 로드되어 있음.
    *   튜토리얼은 `VFX 모델`을 기준으로 진행하며, 다음 주에는 게임용 모델을 다룰 예정임을 언급함.
    *   참고할 델피늄(Larkspur) 꽃의 레퍼런스 이미지들을 준비함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_0944.png" width="300" />

2.  **줄기(Trunk) 생성 및 설정**
    *   `Add > Trunk`를 선택하여 기본 줄기를 추가함.
    *   꽃의 높이를 2~3피트(약 60~90cm) 정도로 설정함.
    *   `Skin` 탭에서 `Radius` 값을 매우 작게 조절하여 줄기를 가늘게 만듦.
        *   Tip: 작은 수치는 슬라이더보다 직접 입력하는 것이 정확함.
    *   `Skin` 탭에서 `Start Radius`를 `End Radius`보다 약간 작게 하여 줄기 끝이 가늘어지게 만듦.
    *   `Generation` 탭에서 `Length`를 조절하여 줄기 하단을 땅에 약간 묻히도록 함.
        *   이는 여러 개의 꽃을 배치할 때 땅의 불규칙성에 신경 쓰지 않게 함.
    *   줄기에 적합한 녹색 `Stem` 텍스처를 드래그 앤 드롭으로 적용함.
    *   `Material` 탭에서 `Hue`와 `Saturation`을 조절하여 줄기의 녹색을 자연스럽게 만듦.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_1140.png" width="300" />

3.  **잎사귀(Leaves) 생성 및 배치**
    *   `Trunk` 노드를 선택한 상태에서 `Add > Branches`를 선택하여 잎사귀를 위한 `Tube` 브랜치를 추가함.
    *   `Generation` 탭에서 `Mode`를 `Interval`로 설정함.
    *   `First`와 `Last` 값을 조절하여 잎이 줄기의 특정 구간에만 생성되도록 함 (예: `Last` 0.5로 줄기 하반부에 집중).
    *   `Frequency`를 증가시켜 잎의 개수를 늘림.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_1320.png" width="300" />
    *   `Skin` 탭에서 `Weld`를 활성화하여 잎 브랜치와 줄기가 자연스럽게 연결되도록 함.
    *   `Spine` 탭에서 `Start Angle`을 조절하여 잎 브랜치의 방향을 설정함.
    *   `Percent Apparent` 대신 `Absolute` 값을 사용하여 작은 꽃에서 잎 길이를 보다 정밀하게 제어함.
    *   `Add > Frond`를 선택하여 잎 텍스처를 적용할 `Frond`를 추가함.
    *   `Toolbar > Collision`을 비활성화하여 모델링 중 오브젝트 간 충돌 계산으로 인한 지연을 방지함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_1604.png" width="300" />
    *   `Cutouts and Meshes` 탭에서 미리 준비된 `Larkspur Leaf` (daisy 1) 컷아웃을 확인. 이 컷아웃은 높은 폴리곤으로 테셀레이션되어 디테일이 높음.
    *   `Frond` 노드를 선택하고 `Material` 탭에서 `daisy 1` 텍스처를 적용함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_1740.png" width="300" />
    *   `Geometry` 탭에서 `Boundary` 값을 조절하여 잎사귀가 줄기 브랜치에 잘 연결되도록 함. `Variance`를 추가하여 잎 모양에 변화를 줌.
    *   `Generation` 탭에서 `Spiral` 모드를 사용하여 잎들이 줄기 주위에 나선형으로 배치되도록 함. `Count`를 조절하여 잎의 수를 맞춤.
    *   `Frond` 노드의 `Spine` 탭에서 `Width`에 `Variance`를 주어 잎 크기에 변화를 줌.
    *   `Fold`와 `Curl`을 조절하여 잎의 끝이 아래로 살짝 말리도록 함.
    *   `Roll`에 `Variance`를 주어 잎 끝이 3D 형태로 보이도록 함.
    *   `Left/Right` `Variance`를 추가하여 잎이 좌우로 불규칙하게 움직이도록 함.
    *   잎사귀를 지지하는 `Tube` 노드의 `Spine` 탭에서 `Gravity`를 조절하여 잎 브랜치가 아래로 처지도록 하고, `Variance`를 추가하여 자연스러운 비대칭을 만듦.
    *   `Ancestor`에 `Variance`를 추가하여 더욱 다양한 움직임을 표현함.
    *   `Start Angle` 커브를 사용하여 줄기 상단의 잎은 위로 살짝 올라가도록 조정함.
    *   **Q&A**: 잎의 두께감을 표현하는 방법
        *   Photoshop에서 노멀맵을 수정하여 가장자리에 살짝 튀어나온 듯한 효과를 줌.
        *   SpeedTree의 `Lighting` 설정에서 `Puffy` 옵션을 활용하여 노멀 방향을 조정, 빛이 닿는 방식에 변화를 주어 가장자리가 두툼해 보이게 함.
        *   `Visualize > Normals`를 통해 노멀 방향을 확인하며 조절함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_2320.png" width="300" />
    *   잎 브랜치(`Tube`)의 `Skin` 탭에서 `Profile Curve`를 조절하여 끝 부분을 0으로 만들어 잎이 붙는 부분만 남기고 브랜치 끝은 가늘게 만듦.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_2445.png" width="300" />
    *   `Cutouts and Meshes` 탭에서 잎 `Cutout`의 각도를 조절하여 줄기에 더 잘 붙도록 만듦.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_2510.png" width="300" />
    *   잎 브랜치(`Tube`)의 `Segments` 탭에서 `Absolute` 값을 조절하여 브랜치 세그먼트 수를 최적화하고, 상단 불필요한 세그먼트를 제거함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_2630.png" width="300" />
    *   `Skin` 탭의 `Spread`와 `Offset`을 사용하여 `Weld` 영역을 조절, 줄기와 잎의 연결 부위를 더 자연스럽게 만듦.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_2720.png" width="300" />
    *   `Skin` 탭에서 `Shape Weld` 기능을 사용하여 용접 영역의 형태를 세밀하게 조정할 수 있음 (작은 부분에 적용 권장).
    *   Ctrl+Left 클릭으로 모든 뷰를 원래대로 돌림.

4.  **꽃받침(Flower Holder) 생성**
    *   `Trunk` 노드를 선택하고 `Add > Trunk Tube`를 선택하여 꽃을 지탱할 `Tube` 브랜치를 추가함.
    *   `Generation` 탭에서 `First`와 `Last`를 `1`로 설정하고 `Extend`를 켜서 줄기 끝 부분에만 생성되도록 함.
    *   `Skin` 탭에서 `Clamp Parent`를 활성화하여 부모 브랜치보다 굵어지지 않게 함.
    *   `Generation` 탭에서 `Absolute`를 `1`로 설정.
    *   `Skin` 탭의 `Kill Ratio Value`가 `0`이 아닌 경우 브랜치가 보이지 않을 수 있으므로, `0`으로 설정하여 문제를 해결함.
    *   `Generation` 탭에서 `Mode`를 `Phyllotaxy`로 설정하고 `Decussate`를 선택하여 브랜치들이 교차하며 배열되도록 함. `Length` 값을 줄여 브랜치 간 간격을 좁힘.
    *   `Length` 탭에서 `Absolute` 값을 `0`으로 설정하여 이 브랜치들을 매우 짧게 만듦.
    *   `Length` 탭의 `According to Trunk` 커브를 사용하여 줄기 하단 브랜치는 더 길게, 상단 브랜치는 더 짧게 만듦. `Extend` 옵션을 활용하여 줄기 끝 부분은 길게 유지함.
    *   `Skin` 탭에서 `Weld`를 활성화하고 `Radius`를 매우 작게 조절함.
    *   `Profile Curve`를 사용하여 꽃받침의 끝 부분을 가늘게 만듦.
    *   `Spine` 탭의 `Start Angle`을 조절하여 꽃받침이 위로 향하도록 하고, `Ancestor`에 음수 값을 주어 살짝 꺾이게 만듦.
    *   `Forces` 탭에서 `Add Force > Planar`를 선택하여 평면 강도를 추가하고 `H` 키로 숨김.
    *   `Tube` 노드의 `Forces` 탭에서 `Planar`를 선택하고 `Profile Curve`를 조절하여 브랜치 끝 부분에만 `Planar` 힘이 작용하도록 함 (꽃들이 밖을 향하게 함).
    *   `Skin` 탭에서 `Profile Curve`를 조절하여 꽃받침 베이스 부분을 살짝 부풀리고 `Seal End`를 활성화하여 끝을 막음.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_3820.png" width="300" />
    *   작업 내용을 `Save As`로 저장함.

5.  **꽃잎(Petals) 생성**
    *   꽃받침(`Tube`) 노드를 선택하고 `Add > Frond`를 선택하여 꽃잎을 추가함.
    *   `Focus` 모드 (`F` 키)로 전환하여 하나의 꽃잎에 집중하여 작업함.
    *   `Spine` 탭에서 `Alignment`를 `0`으로 설정하여 꽃잎이 부모 브랜치에 정렬되도록 함.
    *   `Roll`을 `0.5` 또는 `-0.5`로 조절하여 꽃잎이 밖을 향하도록 함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_4005.png" width="300" />
    *   미리 준비된 꽃잎 텍스처 (Azalea leaf를 포토샵에서 페인팅하여 제작)를 `Material` 탭에서 적용함.
    *   꽃받침 `Tube` 노드의 `Generation` 탭에서 `Count`를 `5`로 설정하여 꽃잎 5개를 만듦.
    *   **Q&A**: 다른 메시(채소, 과일)를 추가하는 방법
        *   `Meshes` 탭에서 `Add`를 눌러 `.OBJ`나 `.FBX` 파일을 불러옴.
        *   트리에 `Leaf` 노드를 추가한 뒤 `Material` 탭에서 불러온 메시를 선택하고, 해당 메시에 맞는 텍스처를 지정함.
        *   SpeedTree v8 모델은 꽃 전체를 별도 파일로 만들어 `Static Mesh`로 가져와 사용하는 경우가 많음. 이렇게 하면 충돌 처리가 용이함.
    *   `Frond` 노드의 `Spine` 탭에서 `Ancestor`를 사용하여 꽃잎의 방향을 밖으로 조절함.
    *   `Length` 탭에서 `According to Trunk` 커브를 조절하여 꽃잎의 길이가 줄기 상단으로 갈수록 짧아지도록 만듦.
    *   `Start Angle`을 조절하여 꽃잎이 바깥쪽으로 펼쳐지게 함.
    *   `Frond` 노드의 `Geometry` 탭에서 `Width`를 조절하여 꽃잎들이 서로 겹치도록 하거나 간격을 조절함.
    *   `Roll`을 조절하여 꽃잎이 3D 형태로 살짝 비틀리게 함.
    *   `Left/Right Variance`를 추가하여 꽃잎들이 불규칙하게 배열되도록 함.
    *   `Spine` 탭에서 `Curl`을 추가하여 꽃잎 가장자리가 안쪽으로 살짝 말리도록 함.
    *   `Width` 탭의 `Profile Curve`를 사용하여 꽃잎 끝 부분의 형태를 조절하여 뾰족하거나 둥글게 만듦.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_4610.png" width="300" />
    *   `Ancestor`에 `Variance`를 추가할 때 `Uniform` 대신 `Cohesive`를 사용하여 꽃 개체별로 다른 형태를 갖도록 함.
    *   꽃받침 `Tube` 노드의 `Spine` 탭에서 `Parent Curls` (v9 기능, v8에서는 `Forces` 사용)을 조절하여 줄기에 붙는 꽃잎의 방향에 미세한 변화를 줌.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_4720.png" width="300" />

6.  **두 번째 꽃잎 레이어 생성**
    *   기존 꽃잎(`Tube` 노드)을 Ctrl+C, Ctrl+V로 복사하여 두 번째 레이어를 만듦.
    *   새로 생성된 `Tube` 노드의 `Icon Color`를 변경하여 구분하기 쉽게 함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_5010.png" width="300" />
    *   `Spine` 탭의 `Ancestor`를 조절하여 두 번째 레이어의 꽃잎들이 첫 번째 레이어보다 살짝 위로 올라가도록 만듦.
    *   `Generation` 탭의 `Rotation`을 조절하여 두 번째 레이어의 꽃잎들이 첫 번째 레이어와 겹치지 않고 교차하도록 회전시킴.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_5100.png" width="300" />
    *   두 꽃잎(`Tube`) 노드를 동시에 선택한 후 `Skin` 탭에서 `Spine Only`를 활성화하여 폴리곤 수를 줄임.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_5120.png" width="300" />

7.  **꽃봉오리(Closed Buds) 및 크기 조정**
    *   두 꽃잎 `Tube` 노드를 동시에 선택한 상태에서 `Spine` 탭의 `Ancestor` 커브를 조절함. `According to Trunk`를 선택하고 줄기 상단(오른쪽)으로 갈수록 꽃잎이 닫히도록 커브를 만듦.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_5235.png" width="300" />
    *   `Length` 탭의 `According to Trunk` 커브를 조절하여 줄기 상단의 꽃잎은 작아지고, 중간 부분은 커지며, 하단은 중간 크기가 되도록 만듦.
    *   꽃받침(`Tube`) 노드의 전체 `Radius`를 줄여 꽃 크기를 전체적으로 작게 만듦.
    *   줄기 (`Tube`) `Length` 탭에서 `Absolute` 값을 조절하여 줄기 길이 비율을 재조정함.
    *   두 `Frond` 노드를 선택한 상태에서 `Spine` 탭의 `Curl`과 `Fold` 커브를 조절함. `According to Trunk`를 선택하고 줄기 상단에서 강하게 안으로 말리도록 커브를 설정하여 꽃봉오리를 완성함.
    *   안쪽 꽃잎(`Frond` 중 하나)만 선택하여 `Ancestor` 커브를 조절, 하단 꽃잎은 더 평평하게 펼쳐지도록 하여 디테일을 추가함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_5440.png" width="300" />
    *   **Q&A**: Generator Mode vs Node Mode
        *   `Generator Mode`: 노드 전체에 걸쳐 파라미터를 조절하여 절차적 생성을 가능하게 함. `Randomize` 기능이 적용되며 재사용성이 높음. 대부분의 모델링 작업에 권장됨.
        *   `Node Mode`: 특정 노드 하나에만 적용되는 수동 편집. `Randomize` 시 사라지며, 다른 노드에 복사할 수 없음. 매우 구체적인 디테일 조정 시에만 사용함.
        *   `Focus` 툴 (`F` 키)을 활용하면 특정 부분에 집중하여 작업하기 좋음.

8.  **수술(Stamen) 및 내부 꽃잎 생성**
    *   꽃잎 `Tube` 노드를 선택하고 `Add > Leaf Mesh`를 선택함. (강사는 처음에 `Branch Tube`를 추가하려다 `Leaf Mesh`가 더 적합하다고 판단함).
    *   `Leaf Mesh` 노드의 `Gin` 탭에서 `Absolute`를 `0`으로 설정하고 `Extend`를 켜서 브랜치 끝에만 생성되도록 함.
    *   미리 준비된 `Stamen` 메시를 `Cutouts and Meshes` 탭에서 불러옴 (4개의 잎으로 구성된 단순한 형태의 수술 메시). 이 메시에는 각 끝에 `Anchor` 포인트가 설정되어 있음.
    *   `Leaf Mesh` 노드의 `Material` 탭에서 `Stamen` 텍스처를 적용함.
    *   `Spine` 탭에서 `Sky Facing`을 활성화하여 수술이 위를 향하도록 함.
    *   `Parent Controls`의 `Up` 값을 조절하여 수술을 위로 올림. `Size`를 매우 작게 조절하여 실제 수술 크기에 맞춤.
    *   `Fold`와 `Curl`을 조절하여 수술이 안으로 살짝 말리도록 형태를 잡음.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_6120.png" width="300" />
    *   `Leaf Mesh` 노드를 선택한 상태에서 `Add > Batch Leaf`를 선택함. `Batch Leaf`는 `Anchor` 포인트가 있는 메시의 각 앵커에 잎을 추가함.
    *   미리 준비된 `Green Inside Bud` 텍스처를 `Material` 탭에서 적용함.
    *   `Size`를 매우 작게 조절하여 내부 꽃잎을 만듦. 앵커 방향에 따라 자동으로 정렬됨.
    *   `Fold`와 `Twist`에 `Variance`를 추가하여 내부 꽃잎들이 불규칙하게 말리도록 함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_6310.png" width="300" />
    *   내부 꽃잎 (`Batch Leaf`) 노드의 `Gin` 탭에서 `According to Trunk` 커브를 조절하여 줄기 상단에서는 내부 꽃잎이 나타나지 않도록 `Last` 값을 `0`으로 설정함 (꽃봉오리 내부에는 보이지 않도록).

9.  **색상 가중치(Weight)를 이용한 꽃잎 색상 변화**
    *   두 `Frond` 노드(꽃잎)를 동시에 선택함.
    *   `Material` 탭에서 `+` 버튼을 눌러 여러 가지 색상의 꽃잎 텍스처 (`Deep Blue`, `Light Blue`, `Blue Purple`, `Green`)를 추가함.
    *   `Material` 탭의 각 텍스처 옆에 있는 `Weight` 섹션에서 커브를 조절하여 색상 분포를 설정함.
        *   `Green` 꽃잎: `According to Trunk` 커브를 사용하여 줄기 끝(상단)에만 `Green` 꽃잎이 나타나도록 `Last` 값을 `0`에 가깝게 설정함.
        *   `Light Blue`와 `Blue Purple` 꽃잎: `According to Trunk` 커브를 사용하여 줄기 중간 부분에 주로 나타나고, 상단과 하단에는 적게 나타나도록 설정함.
        *   `Deep Blue` 꽃잎: `According to Trunk` 커브를 사용하여 줄기 하단에 주로 나타나고, 상단에는 나타나지 않도록 `Last` 값을 `0`에 가깝게 설정함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_6710.png" width="300" />
    *   각 커브를 섬세하게 조절하여 원하는 꽃잎 색상 그라데이션과 분포를 만듦.

10. **최종 확인 및 추가 디테일**
    *   꽃이 너무 듬성듬성해 보이면 잎이나 꽃잎의 `Frequency`를 늘리거나 두 번째 세트를 추가함.
    *   중간에 작은 조각들을 추가하여 밀도를 높이고 사실감을 더함.
    *   `Collision` 옵션을 켜고 모델링을 확인하여 꽃잎들이 자연스럽게 겹치고 있는지 확인함.
    *   `High`, `Medium`, `Low` 해상도 모델을 확인 (`Spine` 탭 > `Segments` 탭 > `Resolution` 조절)하여 폴리곤 수를 관리함.
    <img src="/3D/Speedtree/assets/yt_Flower_Power___Part_1_7215.png" width="300" />
    *   `Wind` 설정을 추가하여 애니메이션을 준비함.
    *   여러 개의 꽃을 배치하려면, `Gin` 탭에서 `Count`를 늘리거나, `Randomize` 후 외부 프로그램으로 가져가 스폰하여 사용함.

## 내가 추가로 발견한 것

- 

## 모르는 것 · 나중에 확인

-
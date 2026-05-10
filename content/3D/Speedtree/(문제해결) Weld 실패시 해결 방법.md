---
title: (문제해결) Weld 실패시 해결 방법
---

## 상황

`Tube_Trunk_Cap` 제너레이터에서 다음 에러 메시지 발생.

> **Weld failed (branch too high on parent)**

<img src="/3D/Speedtree/assets/Pasted_image_20260509105239.png" width="300" />
## 원인

자식 가지(Tube_Trunk_Cap)가 부모 스파인의 너무 끝 쪽에 배치되어
Weld(연결부 처리) 공간이 부족해서 실패.

Gen 탭 → Boundaries → `Last` 값이 높을수록 부모 스파인 끝 쪽에 가지가 생성되어 발생 확률 증가.

## 해결

1. 에러 메시지창 → **Generator** 버튼 클릭하여 해당 제너레이터로 이동
2. `Tube_Trunk_Cap` → **Gen 탭** → **Boundaries → Last** 값을 높임
3. `0.99`로 설정 후 에러 해소 확인
	<img src="/3D/Speedtree/assets/Pasted_image_20260509105211.png" width="300" />
## 참고

- Last 값은 부모 스파인에서 가지가 배치되는 마지막 위치 (0~1 정규화)
- Last를 높이면 가지가 스파인 더 위쪽까지 배치되지만, 너무 낮으면 Weld 공간 부족 발생
- 에러창 버튼: `First` = 첫 번째 오류 가지 선택 / `All` = 전체 선택 / `Generator` = 해당 제너레이터로 이동

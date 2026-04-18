---
title: 원격으로 PC 켜고 Pasec 접속 셋팅 guide
---

날짜 : 2026-04
버전 : 1.0

## 한 줄 요약

스마트폰으로 집 PC 전원을 원격으로 켜고, 다른 PC에서 Parsec으로 접속하는 환경을 구축한다.

---

## 사전 준비

- ipTIME 공유기 (다른 브랜드는 설정 위치가 다를 수 있음)
- Windows PC (집, 원격 접속 대상)
- 접속하는 PC 또는 맥북
- 스마트폰
- Parsec 계정 (parsec.app 에서 가입)

---

## 설치 방법

### STEP 1. Windows PC — 네트워크 어댑터 WOL 설정

1. 윈도우 검색창에 **장치 관리자** 입력 후 실행
2. **네트워크 어댑터** 옆 화살표 클릭해서 목록 펼치기
3. 유선 랜카드 이름 (예: Realtek Gaming 2.5GbE Family Controller) **더블클릭**
   - ⚠️ 카테고리 자체를 클릭하면 탭이 안 나옴. 안에 있는 어댑터 이름을 클릭해야 함
4. **전원 관리** 탭 클릭
5. 아래 3개 항목 모두 체크
   - 전원을 절약하기 위해 컴퓨터가 이 장치를 끌 수 있음
   - 이 장치를 사용하여 컴퓨터의 대기 모드를 종료할 수 있음
   - **매직 패킷에서만 컴퓨터의 대기 모드를 종료할 수 있음** ← 이게 핵심
6. 확인 클릭

---

### STEP 2. Windows PC — 바이오스 WOL 설정

1. PC 재부팅
2. 부팅 중 **Del** 또는 **F2** 키 연타해서 바이오스 진입
3. 메인보드 브랜드별 경로:
   - **ASRock**: Advanced → ACPI Configuration → Pcie Devices Power On → **Enabled**
   - ASUS: Advanced → APM Configuration → Power On By PCI-E → Enabled
   - MSI: Settings → Advanced → Wake Up Event Setup → Resume By PCI-E → Enabled
   - Gigabyte: Settings → Platform Power → Wake on LAN → Enabled
4. **F10** 눌러서 저장 후 재부팅

---

### STEP 3. Windows PC — MAC 주소 확인

1. 윈도우 검색창에 **cmd** 입력 후 실행
2. `ipconfig /all` 입력 후 엔터
3. 유선 랜카드 항목 (Realtek Gaming 등) 에서 **물리적 주소** 확인
   - 형식: XX-XX-XX-XX-XX-XX
4. 이 값을 메모해둠 (이후 공유기 등록에 사용)

---

### STEP 4. Windows PC — 내부 IP 확인

1. cmd 에서 `ipconfig` 입력
2. **IPv4 주소** 확인 (예: 192.168.0.xxx)
3. 메모해둠 (포트포워딩에 사용)

---

### STEP 5. ipTIME 공유기 — WOL 등록

1. 브라우저 주소창에 **192.168.0.1** 입력
   - ⚠️ 집 와이파이에 연결된 상태에서만 접속 가능
   - 초기 아이디/비밀번호는 보통 **admin/admin**
2. 고급설정 → 특수기능 → **WOL**
3. 연결된 기기 목록에서 집 PC 찾아서 MAC 주소 등록
   - ⚠️ 맥북이나 다른 기기가 아닌 **원격 접속 대상 PC**의 MAC 주소를 등록해야 함

---

### STEP 6. ipTIME 공유기 — DDNS 설정

1. 고급설정 → 특수기능 → **DDNS**
2. 호스트 이름 입력 (예: myhome123 → myhome123.iptime.org 형식으로 생성됨)
   - ⚠️ 이름에 개인정보 포함 금지 (이름, 전화번호 등)
   - 너무 단순한 이름도 피하기
3. 이메일 입력 후 등록
4. 생성된 도메인 주소 메모 (예: myhome123.iptime.org)

---

### STEP 7. ipTIME 공유기 — Parsec 포트포워딩

1. 고급설정 → NAT/라우터 관리 → **포트포워딩**
2. 규칙 추가:
   - 규칙 이름: Parsec
   - 프로토콜: **UDP**
   - 외부 포트: 9000 ~ 9000
   - 내부 IP주소: STEP 4에서 확인한 PC IP (192.168.0.xxx)
   - 내부 포트: 9000 ~ 9000
3. 추가 클릭

---

### STEP 8. 스마트폰 — WOL 앱 설정

1. 스마트폰에 **ipTIME WOL** 앱 설치
2. 앱 실행 후 공유기 등록
3. 등록하면 집 PC가 목록에 자동으로 뜸
4. 원격 접속 포트: **9** 입력
   - ⚠️ 0이나 1로 설정하면 작동 안 됨. 반드시 9

---

### STEP 9. Parsec 설치 및 설정

**집 PC (호스트):**
1. parsec.app 에서 Parsec 다운로드 및 설치
2. 계정 로그인
3. 설정 → Host 탭 → **Enable Host** 켜기
4. Parsec이 백그라운드에서 항상 실행 중인 상태 유지

**접속하는 PC / 맥북 (클라이언트):**
1. Parsec 설치 및 **동일한 계정**으로 로그인
2. Computers 탭에서 집 PC 확인

---

## 필수 설정

1. **Parsec 2단계 인증(2FA) 활성화**
   - Parsec 계정 설정 → Security → Two-Factor Authentication 켜기
   - 스마트폰 인증 앱(Google Authenticator 등)으로 연동
2. **ipTIME 관리자 비밀번호 변경**
   - 초기값 admin/admin 은 반드시 변경
   - 시스템 관리 → 관리자 설정 → 비밀번호 변경

---

## 추천 설정

- Parsec 계정 비밀번호는 비밀번호 관리자 앱(Bitwarden 등)으로 관리
- 집 PC 내부 IP를 고정 IP로 설정해두면 포트포워딩이 안 꼬임
  - 제어판 → 네트워크 연결 → 속성 → IPv4 → 수동 입력

---

## 문제 발생 시

### 문제 1. Parsec Computers 탭에 집 PC가 안 뜸
- 집 PC Parsec이 실행 중인지 확인
- 맥북과 집 PC가 **동일한 Parsec 계정**으로 로그인 되어있는지 확인
- 집 PC Parsec 설정 → Host 탭 → Enable Host 켜져 있는지 확인

### 문제 2. WOL 앱으로 켜지지 않음
- ipTIME WOL 앱 원격 접속 포트가 **9**인지 확인 (0이나 1 아님)
- ipTIME 공유기 WOL 등록된 MAC 주소가 **집 PC 유선 랜카드** MAC 주소인지 확인
  - 맥북 MAC 주소를 잘못 등록하는 실수 주의
- 바이오스 WOL 설정이 Enabled 인지 재확인

### 문제 3. Failed to connect to Parsec STUN servers [-6024] 에러
- 원인 1: 같은 공유기 안에서 접속 시도 (헤어핀 NAT 문제)
  - **해결**: 접속하는 기기를 스마트폰 핫스팟으로 바꿔서 테스트. 외부 네트워크(회사, 카페 등)에서는 정상 작동함
- 원인 2: Parsec 포트포워딩 미설정
  - **해결**: STEP 7 포트포워딩 설정 확인. 프로토콜이 **UDP**인지 확인

### 문제 4. 같은 네트워크에서 테스트가 안 됨
- 집 안에서 테스트할 때는 스마트폰 핫스팟으로 바꾸고 테스트
- 외부(회사, 카페)에서는 정상 작동함

---

## 보안 관리 포인트

### 현재 열려있는 것들
- ipTIME DDNS 도메인 (외부에서 공유기 식별 가능)
- UDP 9000 포트 (Parsec 연결용으로 외부에 열림)
- WOL 기능 (외부에서 PC 전원 제어 가능)

### 관리해야 할 것들
- **Parsec 2FA 반드시 유지** → 비밀번호 유출되어도 2FA 있으면 접근 불가
- **Parsec 비밀번호 주기적으로 변경**
- **ipTIME 관리자 비밀번호 강하게 유지**
- 사용하지 않는 기간이 길어지면 포트포워딩 규칙 비활성화 권장
- DDNS 주소를 타인과 공유하지 않기

---

## 맥북 반납 시 정리해야 할 설정

1. **Parsec 로그아웃**
   - Parsec 앱 → 계정 → Sign Out
   - Parsec 웹사이트에서 해당 기기 세션 종료 확인

2. **ipTIME WOL 앱 삭제**
   - 앱 삭제 전 공유기 연결 정보 제거

3. **Parsec 계정 연결 기기에서 맥북 제거**
   - parsec.app 로그인 → 계정 설정 → 연결된 기기 목록에서 맥북 삭제

4. **맥북 Apple ID 로그아웃**
   - 시스템 설정 → Apple ID → 로그아웃

5. **맥북 초기화 (필요시)**
   - 시스템 설정 → 일반 → 전송 또는 재설정 → 모든 콘텐츠 및 설정 지우기

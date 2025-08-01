# Juppelin (주플린) 개발 작업 목록

## 📋 프로젝트 개발 단계

### 🎯 1단계: 프로젝트 초기 설정 및 기본 구조 (1-2주)

#### 1.1 프로젝트 환경 설정
- [ ] **프로젝트 디렉토리 구조 생성**
  ```
  juppelin/
  ├── frontend/
  ├── backend/
  ├── shared/
  ├── tests/
  ├── docs/
  ├── config/
  └── logs/
  ```

- [ ] **Python 가상환경 설정**
  - [ ] requirements.txt 작성
  - [ ] 가상환경 생성 및 활성화
  - [ ] 핵심 라이브러리 설치 (Flask, Pandas, Plotly, etc.)

- [ ] **개발 도구 설정**
  - [ ] Git 저장소 초기화
  - [ ] .gitignore 설정
  - [ ] 코드 포맷터 설정 (Black, Flake8)
  - [ ] 개발 환경 설정 문서 작성

#### 1.2 기본 백엔드 구조 구축
- [ ] **Flask 애플리케이션 초기 설정**
  - [ ] `backend/app.py` 메인 애플리케이션 파일 생성
  - [ ] 기본 라우터 설정
  - [ ] CORS 설정
  - [ ] 환경 변수 관리 (.env 파일)

- [ ] **데이터베이스 초기 설정**
  - [ ] SQLite 데이터베이스 스키마 생성
  - [ ] 데이터베이스 모델 정의
  - [ ] 마이그레이션 스크립트 작성

- [ ] **로깅 시스템 구축**
  - [ ] 로그 설정 파일 작성
  - [ ] 로그 디렉토리 구조 생성
  - [ ] 기본 로깅 함수 구현

#### 1.3 프론트엔드 기본 구조
- [ ] **HTML/CSS/JavaScript 기본 틀**
  - [ ] `frontend/index.html` 메인 페이지 생성
  - [ ] CSS 프레임워크 선택 및 설정
  - [ ] IntelliJ Dark Theme 색상 팔레트 적용

- [ ] **기본 레이아웃 구현**
  - [ ] 헤더 컴포넌트
  - [ ] 좌우 분할 패널 레이아웃
  - [ ] 상태바 컴포넌트

---

### 🔧 2단계: 핵심 기능 개발 (3-4주)

#### 2.1 코드 셀 시스템 구축
- [ ] **Jupyter Kernel 연동**
  - [ ] Jupyter Kernel 클라이언트 구현
  - [ ] 코드 실행 엔진 개발
  - [ ] 실행 결과 처리 시스템

- [ ] **코드 셀 UI 컴포넌트**
  - [ ] 코드 편집기 (Monaco Editor 또는 CodeMirror)
  - [ ] 셀 추가/삭제 기능
  - [ ] 실행 버튼 및 상태 표시
  - [ ] 셀 번호 및 실행 카운트 표시

- [ ] **코드 실행 API**
  - [ ] POST `/api/execute` 엔드포인트
  - [ ] 비동기 코드 실행 처리
  - [ ] 실행 결과 반환 시스템
  - [ ] 오류 처리 및 메시지 표시

#### 2.2 데이터 수집 시스템 개발
- [ ] **API 클라이언트 구현**
  - [ ] 바이낸스 API 클라이언트 (`backend/services/binance_client.py`)
  - [ ] API 키 관리 시스템
  - [ ] 레이트 리미팅 처리
  - [ ] 연결 오류 처리

- [ ] **데이터 수집 서비스**
  - [ ] `DataCollectionService` 클래스 구현
  - [ ] OHLCV 데이터 수집 함수
  - [ ] 데이터 검증 및 정제
  - [ ] 로컬 저장 기능 (CSV, Excel, Parquet)

- [ ] **사용자 함수 라이브러리**
  - [ ] `load_binance_data()` 함수 구현
  - [ ] `load_local_data()` 함수 구현
  - [ ] `save_analysis_result()` 함수 구현
  - [ ] 함수 도움말 및 문서화

#### 2.3 파일 관리 시스템
- [ ] **로컬 파일 시스템 관리**
  - [ ] 데이터 디렉토리 구조 생성
  - [ ] 파일 메타데이터 관리
  - [ ] 파일 목록 조회 API
  - [ ] 파일 삭제 및 정리 기능

- [ ] **데이터 파일 처리**
  - [ ] 다양한 형식 지원 (CSV, Excel, Parquet)
  - [ ] 파일 크기 제한 및 압축
  - [ ] 파일 무결성 검사

---

### 📊 3단계: 기술 지표 및 시각화 (2-3주)

#### 3.1 기술 지표 라이브러리 개발
- [ ] **기본 기술 지표 구현**
  - [ ] MACD 계산 함수
  - [ ] 볼린저 밴드 계산 함수
  - [ ] RSI 계산 함수
  - [ ] 이동평균선 계산 함수

- [ ] **고급 기술 지표**
  - [ ] 스토캐스틱
  - [ ] Williams %R
  - [ ] 피보나치 되돌림
  - [ ] 거래량 지표 (OBV, VWAP)

- [ ] **사용자 인터페이스 함수**
  - [ ] `calculate_macd()` 사용자 함수
  - [ ] `calculate_bollinger_bands()` 사용자 함수
  - [ ] `calculate_rsi()` 사용자 함수
  - [ ] 함수 파라미터 검증 및 기본값 설정

#### 3.2 시각화 시스템 구축
- [ ] **차트 렌더링 엔진**
  - [ ] Plotly 기반 차트 시스템
  - [ ] 다크 테마 차트 스타일 적용
  - [ ] 차트 크기 및 레이아웃 자동 조정

- [ ] **기본 차트 타입 구현**
  - [ ] 캔들스틱 차트 (`plot_candlestick()`)
  - [ ] 선 그래프 (`plot_line()`)
  - [ ] 히스토그램 (`plot_histogram()`)
  - [ ] 히트맵 (`plot_heatmap()`)

- [ ] **복합 차트 기능**
  - [ ] 기술 지표 오버레이
  - [ ] 다중 차트 레이아웃
  - [ ] 차트 간 연동 기능

#### 3.3 우측 패널 시각화 영역
- [ ] **차트 컨테이너 시스템**
  - [ ] 동적 차트 영역 생성
  - [ ] 차트 크기 조절 기능
  - [ ] 차트 배치 관리

- [ ] **실시간 차트 업데이트**
  - [ ] WebSocket을 통한 차트 데이터 전송
  - [ ] 차트 상태 관리
  - [ ] 메모리 사용량 최적화

---

### 🎨 4단계: UI/UX 개선 및 고급 기능 (2-3주)

#### 4.1 사용자 인터페이스 고도화
- [ ] **코드 편집기 고급 기능**
  - [ ] 구문 강조 (Python syntax highlighting)
  - [ ] 자동 완성 기능
  - [ ] 코드 폴딩
  - [ ] 들여쓰기 자동 조정

- [ ] **셀 관리 기능**
  - [ ] 셀 순서 변경 (드래그 앤 드롭)
  - [ ] 셀 복사/붙여넣기
  - [ ] 셀 타입 변경 (Code/Markdown)
  - [ ] 셀 병합/분할

- [ ] **키보드 단축키**
  - [ ] Shift+Enter: 셀 실행 및 다음 셀 이동
  - [ ] Ctrl+Enter: 현재 셀 실행
  - [ ] Alt+Enter: 셀 실행 및 새 셀 생성
  - [ ] 기타 편집 단축키

#### 4.2 데이터 필터링 및 분석 도구
- [ ] **데이터 필터링 UI**
  - [ ] 심볼 선택 드롭다운
  - [ ] 날짜 범위 선택기
  - [ ] 봉 개수 슬라이더
  - [ ] 실시간 필터 적용

- [ ] **분석 도구 패널**
  - [ ] 사전 정의된 함수 목록
  - [ ] 함수 검색 기능
  - [ ] 함수 파라미터 입력 폼
  - [ ] 원클릭 함수 삽입

#### 4.3 파일 및 세션 관리
- [ ] **노트북 저장/로드**
  - [ ] .ipynb 형식으로 세션 저장
  - [ ] 저장된 노트북 로드
  - [ ] 자동 저장 기능
  - [ ] 세션 히스토리 관리

- [ ] **데이터 파일 관리 UI**
  - [ ] 파일 브라우저 패널
  - [ ] 파일 정보 표시 (크기, 생성일)
  - [ ] 파일 미리보기
  - [ ] 파일 삭제 확인 다이얼로그

---

### 🔍 5단계: 고급 분석 기능 및 최적화 (2-3주)

#### 5.1 고급 분석 시나리오 구현
- [ ] **볼린저 밴드 분석 시나리오**
  - [ ] 하단 터치 시 거래량 변화 감지
  - [ ] 밴드 폭 변화 분석
  - [ ] 스퀴즈/확장 패턴 감지

- [ ] **RSI 분석 시나리오**
  - [ ] 과매도/과매수 구간 감지
  - [ ] 다이버전스 패턴 분석
  - [ ] RSI 기반 진입/청산 신호

- [ ] **복합 지표 분석**
  - [ ] MACD + RSI 조합 분석
  - [ ] 다중 시간프레임 분석
  - [ ] 상관관계 분석

#### 5.2 성능 최적화
- [ ] **데이터 처리 최적화**
  - [ ] 대용량 데이터 청크 처리
  - [ ] 메모리 사용량 모니터링
  - [ ] 캐싱 시스템 구현

- [ ] **UI 반응성 개선**
  - [ ] 비동기 차트 렌더링
  - [ ] 프로그레스 바 구현
  - [ ] 백그라운드 작업 처리

- [ ] **API 호출 최적화**
  - [ ] 요청 배치 처리
  - [ ] 캐시된 데이터 활용
  - [ ] 레이트 리미팅 효율화

#### 5.3 오류 처리 및 사용자 경험
- [ ] **포괄적 오류 처리**
  - [ ] API 연결 오류 처리
  - [ ] 데이터 처리 오류 처리
  - [ ] 차트 렌더링 오류 처리

- [ ] **사용자 피드백 시스템**
  - [ ] 토스트 알림 시스템
  - [ ] 진행률 표시
  - [ ] 상태 메시지 표시

---

### 🧪 6단계: 테스트 및 문서화 (1-2주)

#### 6.1 테스트 구현
- [ ] **단위 테스트**
  - [ ] 기술 지표 계산 테스트
  - [ ] API 클라이언트 테스트
  - [ ] 데이터 처리 함수 테스트

- [ ] **통합 테스트**
  - [ ] 전체 워크플로우 테스트
  - [ ] API 엔드포인트 테스트
  - [ ] 파일 저장/로드 테스트

- [ ] **사용자 시나리오 테스트**
  - [ ] 데이터 수집부터 시각화까지
  - [ ] 오류 상황 시나리오
  - [ ] 성능 벤치마크

#### 6.2 문서화 및 사용자 가이드
- [ ] **API 문서 작성**
  - [ ] 함수 레퍼런스
  - [ ] 파라미터 설명
  - [ ] 사용 예제

- [ ] **사용자 매뉴얼**
  - [ ] 설치 가이드
  - [ ] 기본 사용법
  - [ ] 고급 기능 활용법
  - [ ] 문제 해결 가이드

---

### 🚀 7단계: 배포 준비 및 최종 테스트 (1주)

#### 7.1 배포 패키지 준비
- [ ] **실행 스크립트 작성**
  - [ ] `run_juppelin.py` 메인 실행 파일
  - [ ] 설치 스크립트 (`install.sh` / `install.bat`)
  - [ ] 환경 설정 체크 스크립트

- [ ] **설정 파일 템플릿**
  - [ ] API 키 설정 템플릿
  - [ ] 환경 변수 템플릿
  - [ ] 설정 가이드 문서

#### 7.2 최종 검증
- [ ] **전체 시스템 테스트**
  - [ ] 클린 환경에서 설치 테스트
  - [ ] 모든 주요 기능 동작 확인
  - [ ] 성능 및 안정성 검증

- [ ] **문서 최종 검토**
  - [ ] README.md 업데이트
  - [ ] 라이선스 파일 추가
  - [ ] 버전 정보 및 체인지로그

---

## 📊 개발 일정 요약

| 단계 | 기간 | 주요 산출물 | 완료 기준 |
|------|------|-------------|-----------|
| 1단계 | 1-2주 | 프로젝트 구조, 기본 환경 | Flask 앱 실행, 기본 UI 표시 |
| 2단계 | 3-4주 | 코드 셀, 데이터 수집 | 코드 실행 및 데이터 로드 가능 |
| 3단계 | 2-3주 | 기술 지표, 기본 시각화 | 차트 출력 및 지표 계산 가능 |
| 4단계 | 2-3주 | UI/UX 개선, 고급 기능 | 완전한 사용자 인터페이스 |
| 5단계 | 2-3주 | 고급 분석, 최적화 | 성능 최적화 및 복합 분석 |
| 6단계 | 1-2주 | 테스트, 문서화 | 모든 기능 테스트 완료 |
| 7단계 | 1주 | 배포 준비 | 배포 가능한 패키지 완성 |

**총 개발 기간: 12-18주 (약 3-4개월)**

---

## 🎯 우선순위 및 중요도

### 🔥 Critical (1단계 완료 필수)
- 프로젝트 환경 설정
- 기본 Flask 백엔드
- 코드 셀 실행 시스템
- 바이낸스 API 연동

### ⭐ High (MVP 완성을 위한 필수)
- 기본 기술 지표 (MACD, RSI, 볼린저 밴드)
- 캔들스틱 차트 및 선 그래프
- 파일 저장/로드 기능
- 기본 UI 레이아웃

### 📈 Medium (사용성 개선)
- 고급 UI 기능
- 추가 기술 지표
- 성능 최적화
- 오류 처리 개선

### 🎁 Nice to Have (추후 개발)
- 고급 분석 시나리오
- 실시간 데이터 스트리밍
- 다양한 API 지원
- 클라우드 배포 지원

---

## 📝 개발 팀 역할 분담 제안

### Backend Developer
- 데이터 수집 시스템
- 기술 지표 라이브러리
- API 엔드포인트
- 데이터베이스 관리

### Frontend Developer  
- UI/UX 구현
- 차트 시각화
- 사용자 인터페이스
- 반응형 레이아웃

### Full-stack Developer
- 시스템 통합
- 성능 최적화
- 테스트 및 디버깅
- 배포 환경 구성

이 작업 목록을 기반으로 체계적인 개발을 진행하시면 됩니다!

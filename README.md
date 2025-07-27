# 🚀 Juppelin (주플린)

로컬 기반의 데이터 분석 및 시각화 도구

## 📋 소개

Juppelin은 Google Colab과 유사한 환경에서 암호화폐 데이터를 수집하고 기술적 분석을 수행할 수 있는 로컬 웹 애플리케이션입니다.

### 🎯 주요 특징

- 🖥️ **로컬 실행**: 클라우드 의존성 없이 완전히 로컬에서 동작
- 📊 **직관적 UI**: IntelliJ Dark Theme 기반의 세련된 인터페이스
- 📈 **기술적 분석**: MACD, RSI, 볼린저 밴드 등 다양한 기술 지표
- 🔗 **API 연동**: 바이낸스, 코인게코 등 주요 거래소 데이터 수집
- 📝 **Jupyter 스타일**: 코드 셀 기반의 대화형 분석 환경

## 🛠️ 설치 및 실행

### 필수 요구사항

- Python 3.8 이상
- Windows 10/11 (현재 버전)

### 빠른 시작

1. **저장소 클론**
   ```bash
   git clone https://github.com/pablochen/Juppelin.git
   cd Juppelin
   ```

2. **Windows에서 실행**
   ```batch
   start_juppelin.bat
   ```

3. **웹 브라우저에서 접속**
   ```
   http://localhost:8888
   ```

### 수동 설치

1. **가상환경 생성**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/macOS
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **환경 설정**
   ```bash
   copy .env.template .env
   # .env 파일에서 API 키 설정
   ```

4. **서버 실행**
   ```bash
   python backend/app.py
   ```

## 🔧 환경 설정

### API 키 설정

`.env` 파일에서 다음 항목들을 설정해주세요:

```env
# 바이낸스 API (선택사항)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET_KEY=your_binance_secret_key_here

# 코인게코 API (선택사항)
COINGECKO_API_KEY=your_coingecko_api_key_here
```

> **참고**: API 키 없이도 기본 기능은 사용 가능합니다.

## 📖 사용법

### 기본 사용법

1. **데이터 수집**
   ```python
   # 바이낸스에서 비트코인 데이터 수집
   data = load_binance_data('BTCUSDT', '2025-01-01', 30)
   ```

2. **기술 지표 계산**
   ```python
   # MACD 계산
   macd = calculate_macd(data)
   
   # RSI 계산
   rsi = calculate_rsi(data, period=14)
   ```

3. **시각화**
   ```python
   # 캔들스틱 차트
   plot_candlestick(data)
   
   # 기술 지표 차트
   plot_technical_analysis(data, indicators=['macd', 'rsi'])
   ```

### 고급 기능

```python
# 복합 분석
data = load_binance_data('ETHUSDT', '2025-01-01', 60, '1h')
bb = calculate_bollinger_bands(data, period=20, std_dev=2)
plot_line(bb, columns=['upper', 'middle', 'lower'])
```

## 📁 프로젝트 구조

```
Juppelin/
├── backend/                 # 백엔드 서버
│   ├── app.py              # 메인 Flask 애플리케이션
│   ├── static/             # 정적 파일 (CSS, JS)
│   └── templates/          # HTML 템플릿
├── config/                 # 설정 파일
├── local_data/             # 로컬 데이터 저장소
│   ├── raw_data/           # 원본 데이터
│   └── processed_data/     # 처리된 데이터
├── logs/                   # 로그 파일
├── tests/                  # 테스트 파일
├── requirements.txt        # Python 의존성
├── run_juppelin.py        # 실행 스크립트
└── start_juppelin.bat     # Windows 실행 파일
```

## 🎨 UI 스크린샷

### 메인 인터페이스
- 좌측: 코드 편집기 (Jupyter 셀 스타일)
- 우측: 시각화 영역 (차트 출력)
- 하단: 상태바 (연결 상태, 저장소 사용량)

### 다크 테마
- IntelliJ IDEA 다크 테마 기반
- 개발자 친화적인 색상 팔레트
- 가독성 최적화

## 🔧 개발 현황

### ✅ 완료된 기능 (1단계)
- [x] 프로젝트 기본 구조
- [x] Flask 백엔드 서버
- [x] 기본 웹 UI (IntelliJ Dark Theme)
- [x] 코드 셀 시스템
- [x] SocketIO 실시간 통신
- [x] 로깅 시스템

### 🚧 개발 중 (2단계)
- [ ] Jupyter Kernel 연동
- [ ] 바이낸스 API 클라이언트
- [ ] 기본 기술 지표 라이브러리
- [ ] 데이터 저장/로드 시스템

### 📋 예정 기능 (3단계 이후)
- [ ] 고급 시각화 (Plotly 차트)
- [ ] 더 많은 기술 지표
- [ ] 데이터 필터링 UI
- [ ] 성능 최적화

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

- 📧 Issues: [GitHub Issues](https://github.com/pablochen/Juppelin/issues)
- 📖 문서: [Wiki](https://github.com/pablochen/Juppelin/wiki)

## 🙏 감사의 말

- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크
- [Plotly](https://plotly.com/python/) - 시각화 라이브러리
- [TA-Lib](https://mrjbq7.github.io/ta-lib/) - 기술적 분석 라이브러리
- [CCXT](https://github.com/ccxt/ccxt) - 암호화폐 거래소 API

---

**Juppelin** - 로컬에서 시작하는 데이터 분석 여행 🚀

# Juppelin (주플린) 설계 문서

## 1. 시스템 아키텍처

### 1.1 전체 시스템 구조
```
┌─────────────────────────────────────────────────────────────┐
│                    Juppelin System                         │
├─────────────────┬───────────────────────────────────────────┤
│   Frontend UI   │            Backend Services              │
│                 │                                           │
│ ┌─────────────┐ │ ┌─────────────┐ ┌─────────────────────┐   │
│ │   Left      │ │ │   Jupyter   │ │   Data Collection   │   │
│ │   Panel     │ │ │   Kernel    │ │   Service           │   │
│ │ (Code Cells)│ │ │             │ │                     │   │
│ └─────────────┘ │ └─────────────┘ └─────────────────────┘   │
│                 │                                           │
│ ┌─────────────┐ │ ┌─────────────┐ ┌─────────────────────┐   │
│ │   Right     │ │ │ Technical   │ │   File Management   │   │
│ │   Panel     │ │ │ Indicators  │ │   Service           │   │
│ │(Visualization)│ │ Library     │ │                     │   │
│ └─────────────┘ │ └─────────────┘ └─────────────────────┘   │
└─────────────────┴───────────────────────────────────────────┘
                              │
                    ┌─────────────────┐
                    │  Local Storage  │
                    │                 │
                    │ ├─ CSV Files    │
                    │ ├─ Excel Files  │
                    │ └─ Parquet Files│
                    └─────────────────┘
                              │
                    ┌─────────────────┐
                    │  External APIs  │
                    │                 │
                    │ ├─ Binance API  │
                    │ └─ CoinGecko API│
                    └─────────────────┘
```

### 1.2 기술 스택
- **Frontend**: HTML5, CSS3, JavaScript (React/Vue.js)
- **Backend**: Python (Flask/FastAPI)
- **Notebook Engine**: Jupyter Kernel
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Technical Analysis**: TA-Lib, Pandas-TA
- **API Client**: requests, ccxt (cryptocurrency exchange library)

## 2. 사용자 인터페이스 설계

### 2.1 메인 레이아웃
```
┌─────────────────────────────────────────────────────────────────┐
│                     Juppelin Header                            │
│  Logo │ File │ Edit │ Run │ Settings │           Dark Theme    │
├─────────────────────────────────┬───────────────────────────────┤
│                                 │                               │
│           Left Panel            │          Right Panel         │
│         (Code Editor)           │       (Visualization)        │
│                                 │                               │
│ ┌─────────────────────────────┐ │ ┌───────────────────────────┐ │
│ │  [+] Add Cell               │ │ │                           │ │
│ └─────────────────────────────┘ │ │                           │ │
│                                 │ │      Chart Area 1         │ │
│ ┌─────────────────────────────┐ │ │                           │ │
│ │ Cell 1: [Code]              │ │ │                           │ │
│ │ import pandas as pd         │ │ └───────────────────────────┘ │
│ │ data = load_binance_data()  │ │                               │
│ │                             │ │ ┌───────────────────────────┐ │
│ │           [Run]             │ │ │                           │ │
│ └─────────────────────────────┘ │ │      Chart Area 2         │ │
│                                 │ │                           │ │
│ ┌─────────────────────────────┐ │ │                           │ │
│ │ Cell 2: [Code]              │ │ └───────────────────────────┘ │
│ │ macd = calculate_macd(data) │ │                               │
│ │ plot_macd(macd)             │ │                               │
│ │                             │ │                               │
│ │           [Run]             │ │                               │
│ └─────────────────────────────┘ │                               │
├─────────────────────────────────┴───────────────────────────────┤
│                        Status Bar                              │
│  Ready │ Last Updated: 2025-07-27 │ Local Storage: 2.3GB      │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 색상 팔레트 (IntelliJ Dark Theme 기반)
```css
:root {
  /* 배경색 */
  --bg-primary: #2B2B2B;        /* 메인 배경 */
  --bg-secondary: #3C3F41;      /* 패널 배경 */
  --bg-tertiary: #4E5254;       /* 버튼, 입력창 */
  
  /* 텍스트 색상 */
  --text-primary: #A9B7C6;      /* 기본 텍스트 */
  --text-secondary: #6B6B6B;    /* 보조 텍스트 */
  --text-highlight: #FFC66D;    /* 강조 텍스트 */
  
  /* 액센트 색상 */
  --accent-blue: #6897BB;       /* 링크, 버튼 */
  --accent-green: #6A8759;      /* 성공, 완료 */
  --accent-red: #CC7832;        /* 오류, 경고 */
  --accent-orange: #FFC66D;     /* 진행중 */
  
  /* 차트 색상 */
  --chart-line-1: #61DAFB;      /* 메인 라인 */
  --chart-line-2: #FF6B6B;      /* 보조 라인 */
  --chart-line-3: #4ECDC4;      /* 추가 라인 */
  --chart-background: #1E1E1E;  /* 차트 배경 */
}
```

### 2.3 컴포넌트 설계

#### 2.3.1 코드 셀 컴포넌트
```javascript
interface CodeCell {
  id: string;
  content: string;
  cellType: 'code' | 'markdown';
  executionCount: number;
  isRunning: boolean;
  output: CellOutput[];
  metadata: CellMetadata;
}

interface CellOutput {
  outputType: 'display_data' | 'execute_result' | 'error';
  data: any;
  mimeType: string;
}
```

#### 2.3.2 차트 컴포넌트
```javascript
interface ChartComponent {
  id: string;
  title: string;
  chartType: 'line' | 'candlestick' | 'heatmap' | 'histogram';
  data: ChartData;
  config: ChartConfig;
  position: ChartPosition;
}

interface ChartConfig {
  width: number;
  height: number;
  showLegend: boolean;
  theme: 'dark' | 'light';
  interactivity: boolean;
}
```

## 3. 데이터 아키텍처

### 3.1 데이터 플로우
```
External APIs → Data Collection → Local Storage → Data Processing → Visualization
     ↓              ↓                 ↓               ↓              ↓
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Binance    │ │   API       │ │   CSV/      │ │  Technical  │ │   Chart     │
│  CoinGecko  │ │   Client    │ │   Excel/    │ │  Indicators │ │   Render    │
│             │ │   Service   │ │   Parquet   │ │   Library   │ │   Engine    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### 3.2 데이터 모델

#### 3.2.1 OHLCV 데이터 구조
```python
class OHLCVData:
    """OHLCV 캔들스틱 데이터 모델"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    symbol: str
    interval: str  # '1m', '5m', '1h', '1d', etc.
```

#### 3.2.2 기술 지표 데이터 구조
```python
class TechnicalIndicator:
    """기술 지표 기본 클래스"""
    name: str
    parameters: Dict[str, Any]
    data: pandas.DataFrame
    calculation_method: str

class MACDIndicator(TechnicalIndicator):
    """MACD 지표"""
    macd_line: pandas.Series
    signal_line: pandas.Series
    histogram: pandas.Series
    fast_period: int = 12
    slow_period: int = 26
    signal_period: int = 9
```

### 3.3 파일 저장 구조
```
local_data/
├── raw_data/
│   ├── binance/
│   │   ├── BTCUSDT_1d_2025-01-01_to_2025-07-27.csv
│   │   ├── ETHUSDT_1h_2025-07-01_to_2025-07-27.parquet
│   │   └── ...
│   └── coingecko/
│       └── market_data_2025-07-27.xlsx
├── processed_data/
│   ├── technical_indicators/
│   │   ├── BTCUSDT_macd_analysis.csv
│   │   └── ETHUSDT_bollinger_bands.csv
│   └── analysis_results/
└── user_notebooks/
    ├── analysis_session_2025-07-27.ipynb
    └── trading_strategy_backtest.ipynb
```

## 4. 핵심 서비스 설계

### 4.1 데이터 수집 서비스

#### 4.1.1 API 클라이언트 인터페이스
```python
class DataCollectionService:
    """데이터 수집 서비스"""
    
    def __init__(self):
        self.binance_client = BinanceClient()
        self.coingecko_client = CoinGeckoClient()
    
    def collect_ohlcv_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str,
        source: str = 'binance'
    ) -> pandas.DataFrame:
        """OHLCV 데이터 수집"""
        pass
    
    def save_data(
        self,
        data: pandas.DataFrame,
        filename: str,
        file_format: str = 'csv'
    ) -> bool:
        """수집된 데이터 로컬 저장"""
        pass
```

#### 4.1.2 데이터 수집 함수 라이브러리
```python
# 사용자가 호출할 수 있는 함수들
def load_binance_data(
    symbol: str,
    start_date: str,
    days: int,
    interval: str = '1d'
) -> pandas.DataFrame:
    """바이낸스 데이터 수집 및 로드"""
    pass

def load_local_data(filename: str) -> pandas.DataFrame:
    """로컬 저장된 데이터 로드"""
    pass

def save_analysis_result(
    data: pandas.DataFrame,
    filename: str,
    format: str = 'csv'
) -> bool:
    """분석 결과 저장"""
    pass
```

### 4.2 기술 지표 라이브러리

#### 4.2.1 기술 지표 계산 함수
```python
class TechnicalIndicatorLibrary:
    """기술 지표 계산 라이브러리"""
    
    @staticmethod
    def calculate_macd(
        data: pandas.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
        price_column: str = 'close'
    ) -> pandas.DataFrame:
        """MACD 계산"""
        pass
    
    @staticmethod
    def calculate_bollinger_bands(
        data: pandas.DataFrame,
        period: int = 20,
        std_dev: float = 2.0,
        price_column: str = 'close'
    ) -> pandas.DataFrame:
        """볼린저 밴드 계산"""
        pass
    
    @staticmethod
    def calculate_rsi(
        data: pandas.DataFrame,
        period: int = 14,
        price_column: str = 'close'
    ) -> pandas.DataFrame:
        """RSI 계산"""
        pass
```

#### 4.2.2 사용자 함수 인터페이스
```python
# 사용자가 셀에서 호출하는 함수들
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """MACD 계산 (사용자 친화적 인터페이스)"""
    return TechnicalIndicatorLibrary.calculate_macd(data, fast_period, slow_period, signal_period)

def calculate_bollinger_bands(data, period=20, std_dev=2.0):
    """볼린저 밴드 계산"""
    return TechnicalIndicatorLibrary.calculate_bollinger_bands(data, period, std_dev)

def calculate_rsi(data, period=14):
    """RSI 계산"""
    return TechnicalIndicatorLibrary.calculate_rsi(data, period)
```

### 4.3 시각화 서비스

#### 4.3.1 차트 렌더링 엔진
```python
class VisualizationService:
    """시각화 서비스"""
    
    def __init__(self):
        self.theme = 'dark'
        self.color_palette = self._load_color_palette()
    
    def create_candlestick_chart(
        self,
        data: pandas.DataFrame,
        title: str = None,
        height: int = 400
    ) -> dict:
        """캔들스틱 차트 생성"""
        pass
    
    def create_line_chart(
        self,
        data: pandas.DataFrame,
        columns: List[str],
        title: str = None
    ) -> dict:
        """선 그래프 생성"""
        pass
    
    def create_heatmap(
        self,
        data: pandas.DataFrame,
        title: str = None
    ) -> dict:
        """히트맵 생성"""
        pass
```

#### 4.3.2 사용자 시각화 함수
```python
# 사용자가 셀에서 호출하는 시각화 함수들
def plot_candlestick(data, symbol=None, start_candles=0, num_candles=100):
    """캔들스틱 차트 표시"""
    pass

def plot_line(data, columns=None, title=None):
    """선 그래프 표시"""
    pass

def plot_technical_analysis(data, indicators=['macd', 'rsi'], symbol=None):
    """기술 지표 복합 차트 표시"""
    pass

def plot_correlation_heatmap(data, assets=None):
    """상관관계 히트맵 표시"""
    pass
```

## 5. 백엔드 API 설계

### 5.1 REST API 엔드포인트

#### 5.1.1 코드 실행 API
```python
# POST /api/execute
{
  "cell_id": "string",
  "code": "string",
  "cell_type": "code"
}

# Response
{
  "execution_count": 1,
  "outputs": [
    {
      "output_type": "execute_result",
      "data": {...},
      "metadata": {}
    }
  ],
  "status": "success" | "error",
  "error_message": "string"
}
```

#### 5.1.2 데이터 관리 API
```python
# GET /api/data/files
{
  "directory": "string",
  "file_type": "csv" | "xlsx" | "parquet"
}

# POST /api/data/collect
{
  "symbol": "string",
  "start_date": "string",
  "days": "number",
  "interval": "string",
  "filename": "string"
}

# GET /api/data/load/{filename}
```

#### 5.1.3 시각화 API
```python
# POST /api/visualize
{
  "chart_type": "candlestick" | "line" | "heatmap" | "histogram",
  "data": "dataframe_json",
  "config": {
    "title": "string",
    "width": "number",
    "height": "number",
    "theme": "dark" | "light"
  }
}

# Response
{
  "chart_id": "string",
  "chart_data": "plotly_json",
  "status": "success" | "error"
}
```

### 5.2 WebSocket 통신
```python
# 실시간 코드 실행 상태 업데이트
{
  "type": "execution_status",
  "cell_id": "string",
  "status": "running" | "completed" | "error",
  "progress": "number"
}

# 차트 업데이트
{
  "type": "chart_update",
  "chart_id": "string",
  "chart_data": "plotly_json"
}
```

## 6. 데이터베이스 설계

### 6.1 SQLite 로컬 데이터베이스
```sql
-- 사용자 세션 관리
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT UNIQUE,
    created_at TIMESTAMP,
    last_accessed TIMESTAMP,
    notebook_path TEXT
);

-- 데이터 파일 메타데이터
CREATE TABLE data_files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    file_path TEXT,
    file_type TEXT,
    symbol TEXT,
    start_date DATE,
    end_date DATE,
    interval TEXT,
    file_size INTEGER,
    created_at TIMESTAMP
);

-- 코드 실행 히스토리
CREATE TABLE execution_history (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    cell_id TEXT,
    code TEXT,
    execution_count INTEGER,
    execution_time REAL,
    status TEXT,
    created_at TIMESTAMP
);
```

## 7. 보안 설계

### 7.1 API 키 관리
```python
# config/api_keys.py
class APIKeyManager:
    """API 키 안전 관리"""
    
    def __init__(self):
        self.config_file = 'config/api_config.json'
        self.env_file = '.env'
    
    def get_binance_api_key(self) -> str:
        """바이낸스 API 키 조회"""
        # 환경 변수 우선, 설정 파일 대안
        pass
    
    def set_api_key(self, service: str, api_key: str, secret_key: str = None):
        """API 키 설정 (암호화 저장)"""
        pass
```

### 7.2 로컬 데이터 보안
- 사용자 데이터는 로컬 파일시스템에만 저장
- API 키는 암호화하여 저장
- 세션 토큰을 통한 접근 제어

## 8. 오류 처리 및 로깅

### 8.1 오류 처리 전략
```python
class ErrorHandler:
    """중앙 집중식 오류 처리"""
    
    @staticmethod
    def handle_api_error(error: Exception, context: str) -> dict:
        """API 호출 오류 처리"""
        return {
            "error_type": "api_error",
            "message": str(error),
            "context": context,
            "user_message": "데이터 수집 중 오류가 발생했습니다."
        }
    
    @staticmethod
    def handle_analysis_error(error: Exception, code: str) -> dict:
        """분석 코드 실행 오류 처리"""
        return {
            "error_type": "analysis_error",
            "message": str(error),
            "code": code,
            "user_message": "분석 실행 중 오류가 발생했습니다."
        }
```

### 8.2 로깅 시스템
```python
import logging

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/juppelin.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('juppelin')
```

## 9. 성능 최적화

### 9.1 데이터 처리 최적화
- Pandas 연산 최적화
- 대용량 데이터 청크 단위 처리
- 메모리 사용량 모니터링

### 9.2 UI 반응성 최적화
- 차트 렌더링 최적화 (Plotly 설정)
- 코드 실행 비동기 처리
- 프로그레스 바를 통한 사용자 피드백

## 10. 테스트 전략

### 10.1 단위 테스트
```python
# tests/test_technical_indicators.py
import unittest
from juppelin.indicators import TechnicalIndicatorLibrary

class TestTechnicalIndicators(unittest.TestCase):
    
    def test_macd_calculation(self):
        """MACD 계산 테스트"""
        pass
    
    def test_bollinger_bands_calculation(self):
        """볼린저 밴드 계산 테스트"""
        pass
```

### 10.2 통합 테스트
- API 연동 테스트
- 데이터 수집 및 저장 테스트
- 시각화 렌더링 테스트

### 10.3 사용자 시나리오 테스트
- 전체 분석 워크플로우 테스트
- 오류 상황 시나리오 테스트
- 성능 벤치마크 테스트

## 11. 배포 및 설정

### 11.1 로컬 환경 설정
```bash
# requirements.txt
flask==2.3.2
pandas==2.0.3
numpy==1.24.3
plotly==5.15.0
jupyter==1.0.0
ccxt==4.0.62
python-dotenv==1.0.0
sqlite3
```

### 11.2 실행 스크립트
```python
# run_juppelin.py
import os
import subprocess
from juppelin.app import create_app

def main():
    # 환경 설정 확인
    # 로컬 데이터 디렉토리 생성
    # Flask 앱 실행
    app = create_app()
    app.run(host='localhost', port=8888, debug=True)

if __name__ == '__main__':
    main()
```

이 설계 문서는 Juppelin 시스템의 전체적인 구조와 구현 방향을 제시합니다. 각 섹션별로 세부 구현이 필요하며, 개발 진행에 따라 설계가 보완될 수 있습니다.

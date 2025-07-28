"""
User Functions Library
사용자가 코드 셀에서 호출할 수 있는 함수들
"""

import sys
import os
import pandas as pd
import numpy as np
from typing import Optional, Union

# 백엔드 서비스 모듈 경로 추가
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

# 서비스 모듈들을 안전하게 임포트
_data_service = None
_tech_indicators = None
_viz_service = None
_services_loaded = False

try:
    # 백엔드 서비스 모듈 경로 추가
    backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    
    from services.data_collection import DataCollectionService
    from services.technical_indicators import TechnicalIndicators
    from services.visualization import VisualizationService
    
    # 전역 서비스 인스턴스
    _data_service = DataCollectionService()
    _tech_indicators = TechnicalIndicators()
    _viz_service = VisualizationService()
    _services_loaded = True
    
except ImportError as e:
    pass  # 서비스 모듈 임포트 실패 시 무시
except Exception as e:
    pass  # 서비스 초기화 실패 시 무시

def test_services():
    """서비스 로드 상태 테스트"""
    try:
        print(f"Services loaded: {_services_loaded}")
        print(f"Data service: {_data_service is not None}")
        print(f"Tech indicators: {_tech_indicators is not None}")
        print(f"Viz service: {_viz_service is not None}")
        return _services_loaded
    except Exception as e:
        print(f"테스트 함수 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def hello_world():
    """가장 간단한 테스트"""
    print("Hello World!")
    return "OK"

def simple_test():
    """매우 간단한 테스트"""
    try:
        print("Hello from Juppelin!")
        print("Simple test completed successfully.")
        print("Ready for data analysis!")
        return True
    except Exception as e:
        print(f"Simple test failed: {str(e)}")
        return False

# 기술 지표 및 시각화 함수들

def calculate_macd(
    data: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    price_column: str = 'close'
) -> pd.DataFrame:
    """
    MACD 계산
    
    사용 예시:
        macd = calculate_macd(data)
        print(macd.head())
    
    Args:
        data: OHLCV 데이터
        fast_period: 빠른 EMA 기간 (기본값: 12)
        slow_period: 느린 EMA 기간 (기본값: 26)
        signal_period: 시그널 라인 기간 (기본값: 9)
        price_column: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        MACD 데이터가 포함된 DataFrame
    """
    try:
        print(f"📊 MACD 계산 중... (fast={fast_period}, slow={slow_period}, signal={signal_period})")
        
        if _tech_indicators is None:
            raise ImportError("기술적 지표 서비스를 사용할 수 없습니다.")
        
        price_data = data[price_column]
        macd_result = _tech_indicators.calculate_macd(price_data, fast_period, slow_period, signal_period)
        
        print(f"✅ MACD 계산 완료: {len(macd_result)}행")
        return macd_result
        
    except Exception as e:
        print(f"❌ MACD 계산 실패: {str(e)}")
        raise

def calculate_rsi(
    data: pd.DataFrame,
    period: int = 14,
    price_column: str = 'close'
) -> pd.Series:
    """
    RSI 계산
    
    사용 예시:
        rsi = calculate_rsi(data, period=14)
        print(f"현재 RSI: {rsi.iloc[-1]:.2f}")
    
    Args:
        data: OHLCV 데이터
        period: 계산 기간 (기본값: 14)
        price_column: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        RSI 값이 포함된 Series
    """
    try:
        print(f"📊 RSI 계산 중... (period={period})")
        
        if _tech_indicators is None:
            raise ImportError("기술적 지표 서비스를 사용할 수 없습니다.")
        
        price_data = data[price_column]
        rsi_result = _tech_indicators.calculate_rsi(price_data, period)
        
        print(f"✅ RSI 계산 완료: {len(rsi_result)}행")
        return rsi_result
        
    except Exception as e:
        print(f"❌ RSI 계산 실패: {str(e)}")
        raise

def calculate_bollinger_bands(
    data: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2.0,
    price_column: str = 'close'
) -> pd.DataFrame:
    """
    볼린저 밴드 계산
    
    사용 예시:
        bb = calculate_bollinger_bands(data)
        print(bb.tail())
    
    Args:
        data: OHLCV 데이터
        period: 이동평균 기간 (기본값: 20)
        std_dev: 표준편차 배수 (기본값: 2.0)
        price_column: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        볼린저 밴드 데이터가 포함된 DataFrame
    """
    try:
        print(f"📊 볼린저 밴드 계산 중... (period={period}, std_dev={std_dev})")
        
        if _tech_indicators is None:
            raise ImportError("기술적 지표 서비스를 사용할 수 없습니다.")
        
        price_data = data[price_column]
        bb_result = _tech_indicators.calculate_bollinger_bands(price_data, period, std_dev)
        
        print(f"✅ 볼린저 밴드 계산 완료: {len(bb_result)}행")
        return bb_result
        
    except Exception as e:
        print(f"❌ 볼린저 밴드 계산 실패: {str(e)}")
        raise

def calculate_sma(
    data: pd.DataFrame,
    period: int,
    price_column: str = 'close'
) -> pd.Series:
    """
    단순 이동평균선 계산
    
    사용 예시:
        sma20 = calculate_sma(data, 20)
        sma50 = calculate_sma(data, 50)
    
    Args:
        data: OHLCV 데이터
        period: 이동평균 기간
        price_column: 가격 컬럼명 (기본값: 'close')
    
    Returns:
        SMA 값이 포함된 Series
    """
    try:
        print(f"📊 SMA{period} 계산 중...")
        
        if _tech_indicators is None:
            raise ImportError("기술적 지표 서비스를 사용할 수 없습니다.")
        
        price_data = data[price_column]
        sma_result = _tech_indicators.calculate_sma(price_data, period)
        
        print(f"✅ SMA{period} 계산 완료: {len(sma_result)}행")
        return sma_result
        
    except Exception as e:
        print(f"❌ SMA{period} 계산 실패: {str(e)}")
        raise

# 시각화 함수들

def plot_candlestick(
    data: pd.DataFrame,
    symbol: str = None,
    start_candles: int = 0,
    num_candles: int = 100,
    show_volume: bool = True
) -> None:
    """
    캔들스틱 차트 표시
    
    사용 예시:
        plot_candlestick(data, symbol='BTCUSDT')
        plot_candlestick(data, num_candles=50, show_volume=False)
    
    Args:
        data: OHLCV 데이터
        symbol: 심볼명 (제목용)
        start_candles: 시작 캔들 인덱스
        num_candles: 표시할 캔들 개수
        show_volume: 거래량 표시 여부
    """
    try:
        print(f"📊 캔들스틱 차트 생성 중...")
        
        # 데이터 필터링
        if len(data) > num_candles:
            end_idx = start_candles + num_candles
            filtered_data = data.iloc[start_candles:end_idx]
        else:
            filtered_data = data
        
        if _viz_service is None:
            raise ImportError("시각화 서비스를 사용할 수 없습니다.")
        
        title = f"{symbol} 캔들스틱 차트" if symbol else "캔들스틱 차트"
        
        chart_data = _viz_service.create_candlestick_chart(
            filtered_data, 
            title=title,
            show_volume=show_volume
        )
        
        # 차트 표시 (현재는 JSON 출력, 나중에 실제 차트로 변경)
        print(f"✅ 캔들스틱 차트 생성 완료")
        print(f"📈 표시된 캔들 수: {len(filtered_data)}")
        
        # 간단한 통계 출력
        print(f"📊 기간 통계:")
        print(f"   최고가: ${filtered_data['high'].max():.2f}")
        print(f"   최저가: ${filtered_data['low'].min():.2f}")
        print(f"   평균 거래량: {filtered_data['volume'].mean():.0f}")
        
    except Exception as e:
        print(f"❌ 캔들스틱 차트 생성 실패: {str(e)}")

def plot_line(
    data: pd.DataFrame,
    columns: list = None,
    title: str = None
) -> None:
    """
    선 그래프 표시
    
    사용 예시:
        plot_line(data, columns=['close'])
        plot_line(macd, columns=['macd', 'signal'])
    
    Args:
        data: 데이터
        columns: 표시할 컬럼 리스트
        title: 차트 제목
    """
    try:
        if columns is None:
            # 숫자형 컬럼 자동 선택
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            columns = numeric_cols[:5]  # 최대 5개까지
        
        print(f"📊 선 그래프 생성 중... (컬럼: {columns})")
        
        if _viz_service is None:
            raise ImportError("시각화 서비스를 사용할 수 없습니다.")
        
        chart_title = title or f"선 그래프 ({', '.join(columns)})"
        
        chart_data = _viz_service.create_line_chart(
            data,
            columns=columns,
            title=chart_title
        )
        
        print(f"✅ 선 그래프 생성 완료")
        print(f"📈 표시된 라인: {len(columns)}개")
        
        # 각 컬럼의 통계 출력
        for col in columns:
            if col in data.columns:
                values = data[col].dropna()
                if len(values) > 0:
                    print(f"   {col}: 평균 {values.mean():.4f}, 최대 {values.max():.4f}, 최소 {values.min():.4f}")
        
    except Exception as e:
        print(f"❌ 선 그래프 생성 실패: {str(e)}")

def plot_technical_analysis(
    data: pd.DataFrame,
    indicators: list = ['macd', 'rsi'],
    symbol: str = None
) -> None:
    """
    기술적 분석 복합 차트 표시
    
    사용 예시:
        plot_technical_analysis(data, indicators=['macd', 'rsi'])
        plot_technical_analysis(data, indicators=['bollinger'], symbol='BTCUSDT')
    
    Args:
        data: OHLCV 데이터
        indicators: 표시할 기술 지표 리스트
        symbol: 심볼명
    """
    try:
        print(f"📊 기술적 분석 차트 생성 중... (지표: {indicators})")
        
        # 지표별 계산
        indicator_data = {}
        
        for indicator in indicators:
            if indicator.lower() == 'macd':
                indicator_data['MACD'] = calculate_macd(data)
            elif indicator.lower() == 'rsi':
                rsi_values = calculate_rsi(data)
                indicator_data['RSI'] = pd.DataFrame({'rsi': rsi_values})
            elif indicator.lower() in ['bollinger', 'bb']:
                indicator_data['볼린저밴드'] = calculate_bollinger_bands(data)
        
        if not indicator_data:
            print("❌ 유효한 지표가 없습니다.")
            return
        
        if _viz_service is None:
            raise ImportError("시각화 서비스를 사용할 수 없습니다.")
        
        title = f"{symbol} 기술적 분석" if symbol else "기술적 분석"
        
        chart_data = _viz_service.create_technical_analysis_chart(
            data,
            indicators=indicator_data,
            title=title
        )
        
        print(f"✅ 기술적 분석 차트 생성 완료")
        print(f"📈 포함된 지표: {len(indicator_data)}개")
        
    except Exception as e:
        print(f"❌ 기술적 분석 차트 생성 실패: {str(e)}")

def plot_correlation_heatmap(
    data: pd.DataFrame,
    assets: list = None
) -> None:
    """
    상관관계 히트맵 표시
    
    사용 예시:
        plot_correlation_heatmap(combined_data)
    
    Args:
        data: 데이터
        assets: 자산 리스트 (컬럼 필터링용)
    """
    try:
        print(f"📊 상관관계 히트맵 생성 중...")
        
        # 자산별 필터링
        if assets:
            available_cols = [col for col in assets if col in data.columns]
            filtered_data = data[available_cols]
        else:
            # 숫자형 컬럼만 선택
            filtered_data = data.select_dtypes(include=[np.number])
        
        if _viz_service is None:
            raise ImportError("시각화 서비스를 사용할 수 없습니다.")
        
        chart_data = _viz_service.create_correlation_heatmap(
            filtered_data,
            title="상관관계 히트맵"
        )
        
        print(f"✅ 상관관계 히트맵 생성 완료")
        print(f"📈 분석된 컬럼: {len(filtered_data.columns)}개")
        
    except Exception as e:
        print(f"❌ 상관관계 히트맵 생성 실패: {str(e)}")

def load_binance_data(
    symbol: str,
    start_date: str,
    days: int,
    interval: str = '1d'
) -> pd.DataFrame:
    """
    바이낸스에서 데이터 수집
    
    사용 예시:
        data = load_binance_data('BTCUSDT', '2025-01-01', 30)
    
    Args:
        symbol: 거래 쌍 (예: 'BTCUSDT', 'ETHUSDT')
        start_date: 시작 날짜 ('YYYY-MM-DD' 형식)
        days: 수집할 일수
        interval: 봉 간격 ('1m', '5m', '15m', '30m', '1h', '4h', '1d' 등)
    
    Returns:
        OHLCV 데이터가 포함된 pandas DataFrame
    """
    try:
        if _data_service is None:
            raise ImportError("데이터 수집 서비스를 사용할 수 없습니다.")
        df = _data_service.collect_binance_data(
            symbol=symbol,
            start_date=start_date,
            days=days,
            interval=interval,
            save_file=True
        )
        # DataFrame이 반환될 때는 출력하지 않음 (중복 탭 방지)
        return df
    except Exception as e:
        raise

def load_local_data(filename: str) -> pd.DataFrame:
    """
    로컬에 저장된 데이터 로드
    
    사용 예시:
        data = load_local_data('BTCUSDT_1d_2025-01-01_to_2025-01-31.csv')
    
    Args:
        filename: 파일명 (확장자 포함)
    
    Returns:
        로드된 pandas DataFrame
    """
    try:
        print(f"📁 로컬 파일을 로드하는 중: {filename}")
        
        df = _data_service.load_local_data(filename)
        
        print(f"✅ 파일 로드 완료: {len(df)}행")
        if hasattr(df.index, 'min') and hasattr(df.index, 'max'):
            print(f"📅 기간: {df.index.min()} ~ {df.index.max()}")
        
        return df
        
    except Exception as e:
        print(f"❌ 파일 로드 실패: {str(e)}")
        raise

def save_analysis_result(
    data: pd.DataFrame,
    filename: str,
    format: str = 'csv'
) -> str:
    """
    분석 결과 저장
    
    사용 예시:
        save_analysis_result(result_data, 'my_analysis', 'csv')
    
    Args:
        data: 저장할 pandas DataFrame
        filename: 파일명 (확장자 제외)
        format: 파일 형식 ('csv', 'xlsx', 'parquet')
    
    Returns:
        저장된 파일 경로
    """
    try:
        print(f"💾 분석 결과를 저장하는 중: {filename}.{format}")
        
        file_path = _data_service.save_analysis_result(data, filename, format)
        
        print(f"✅ 저장 완료: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"❌ 저장 실패: {str(e)}")
        raise

def list_files(directory: str = 'raw_data') -> None:
    """
    로컬 파일 목록 출력
    
    사용 예시:
        list_files()  # raw_data 폴더
        list_files('processed_data')  # processed_data 폴더
    
    Args:
        directory: 조회할 디렉토리 ('raw_data' 또는 'processed_data')
    """
    try:
        print(f"📂 {directory} 폴더의 파일 목록:")
        
        file_info = _data_service.list_local_files(directory)
        
        if file_info['total_files'] == 0:
            print("   📭 파일이 없습니다.")
            return
        
        print(f"   📊 총 {file_info['total_files']}개 파일")
        print()
        
        for file in file_info['files'][:10]:  # 최근 10개만 표시
            size_mb = round(file['size'] / (1024 * 1024), 2) if file['size'] > 1024 * 1024 else f"{round(file['size'] / 1024, 1)}KB"
            if file['size'] > 1024 * 1024:
                size_str = f"{size_mb}MB"
            else:
                size_str = f"{round(file['size'] / 1024, 1)}KB"
            
            print(f"   📄 {file['name']}")
            print(f"      📏 크기: {size_str}")
            print(f"      📅 수정: {file['modified'][:19]}")
            print()
        
        if file_info['total_files'] > 10:
            print(f"   ... 그 외 {file_info['total_files'] - 10}개 파일")
        
    except Exception as e:
        print(f"❌ 파일 목록 조회 실패: {str(e)}")

def get_file_info(filename: str) -> None:
    """
    파일 상세 정보 출력
    
    사용 예시:
        get_file_info('BTCUSDT_1d_2025-01-01_to_2025-01-31.csv')
    
    Args:
        filename: 조회할 파일명
    """
    try:
        print(f"파일 정보: {filename}")
        
        if _data_service is None:
            print("데이터 서비스를 사용할 수 없습니다.")
            return
        
        info = _data_service.get_file_info(filename)
        
        print(f"   크기: {info['size_mb']}MB ({info['size']:,} bytes)")
        print(f"   생성일: {info['created'][:19]}")
        print(f"   수정일: {info['modified'][:19]}")
        print(f"   형식: {info['extension']}")
        
        if info.get('preview'):
            print(f"   미리보기 (처음 5행):")
            for i, row in enumerate(info['preview']):
                print(f"      {i+1}: {row}")
        
    except Exception as e:
        print(f"파일 정보 조회 실패: {str(e)}")
        import traceback
        traceback.print_exc()

def show_help():
    """간단한 도움말"""
    print("Juppelin Help")
    print("=============")
    print("simple_test() - Simple test")
    print("test_services() - Check services")
    print("show_help() - Show this help")
    print("=============")
    return "Help displayed"

# 별칭 함수들
help = show_help
ls = list_files

# 사용자가 바로 사용할 수 있도록 함수들을 전역으로 내보내기
__all__ = [
    # 테스트
    'hello_world',
    'simple_test',
    'test_services',
    
    # 데이터 관리
    'load_binance_data',
    'load_local_data', 
    'save_analysis_result',
    'list_files',
    'get_file_info',
    
    # 기술 지표
    'calculate_macd',
    'calculate_rsi',
    'calculate_bollinger_bands',
    'calculate_sma',
    
    # 시각화
    'plot_candlestick',
    'plot_line',
    'plot_technical_analysis',
    'plot_correlation_heatmap',
    
    # 도움말
    'show_help',
    'help',
    'ls'
]

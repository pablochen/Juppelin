"""
Technical Indicators Library
기술적 분석 지표 계산 라이브러리
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """기술 지표 계산 클래스"""
    
    @staticmethod
    def calculate_sma(data: pd.Series, period: int) -> pd.Series:
        """단순 이동평균선 (Simple Moving Average)"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """지수 이동평균선 (Exponential Moving Average)"""
        return data.ewm(span=period).mean()
    
    @staticmethod
    def calculate_macd(
        data: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> pd.DataFrame:
        """
        MACD (Moving Average Convergence Divergence) 계산
        
        Args:
            data: 가격 데이터 (일반적으로 종가)
            fast_period: 빠른 EMA 기간 (기본값: 12)
            slow_period: 느린 EMA 기간 (기본값: 26)
            signal_period: 시그널 라인 기간 (기본값: 9)
        
        Returns:
            MACD 라인, 시그널 라인, 히스토그램이 포함된 DataFrame
        """
        try:
            # EMA 계산
            ema_fast = TechnicalIndicators.calculate_ema(data, fast_period)
            ema_slow = TechnicalIndicators.calculate_ema(data, slow_period)
            
            # MACD 라인 계산
            macd_line = ema_fast - ema_slow
            
            # 시그널 라인 계산 (MACD의 EMA)
            signal_line = TechnicalIndicators.calculate_ema(macd_line, signal_period)
            
            # 히스토그램 계산
            histogram = macd_line - signal_line
            
            # 결과 DataFrame 생성
            result = pd.DataFrame({
                'macd': macd_line,
                'signal': signal_line,
                'histogram': histogram
            }, index=data.index)
            
            logger.info(f"MACD 계산 완료: {len(result)}개 데이터")
            return result
            
        except Exception as e:
            logger.error(f"MACD 계산 실패: {e}")
            raise
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        RSI (Relative Strength Index) 계산
        
        Args:
            data: 가격 데이터
            period: 계산 기간 (기본값: 14)
        
        Returns:
            RSI 값이 포함된 Series
        """
        try:
            # 가격 변화 계산
            delta = data.diff()
            
            # 상승분과 하락분 분리
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            # 평균 상승분과 하락분 계산 (Wilder's smoothing)
            avg_gain = gain.ewm(alpha=1/period).mean()
            avg_loss = loss.ewm(alpha=1/period).mean()
            
            # RS (Relative Strength) 계산
            rs = avg_gain / avg_loss
            
            # RSI 계산
            rsi = 100 - (100 / (1 + rs))
            
            logger.info(f"RSI 계산 완료: {len(rsi)}개 데이터")
            return rsi
            
        except Exception as e:
            logger.error(f"RSI 계산 실패: {e}")
            raise
    
    @staticmethod
    def calculate_bollinger_bands(
        data: pd.Series,
        period: int = 20,
        std_dev: float = 2.0
    ) -> pd.DataFrame:
        """
        볼린저 밴드 (Bollinger Bands) 계산
        
        Args:
            data: 가격 데이터
            period: 이동평균 기간 (기본값: 20)
            std_dev: 표준편차 배수 (기본값: 2.0)
        
        Returns:
            상단밴드, 중간밴드(SMA), 하단밴드가 포함된 DataFrame
        """
        try:
            # 중간밴드 (SMA) 계산
            middle_band = TechnicalIndicators.calculate_sma(data, period)
            
            # 표준편차 계산
            std = data.rolling(window=period).std()
            
            # 상단밴드와 하단밴드 계산
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            # 결과 DataFrame 생성
            result = pd.DataFrame({
                'upper': upper_band,
                'middle': middle_band,
                'lower': lower_band,
                'bandwidth': (upper_band - lower_band) / middle_band * 100
            }, index=data.index)
            
            logger.info(f"볼린저 밴드 계산 완료: {len(result)}개 데이터")
            return result
            
        except Exception as e:
            logger.error(f"볼린저 밴드 계산 실패: {e}")
            raise
    
    @staticmethod
    def calculate_stochastic(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        k_period: int = 14,
        d_period: int = 3
    ) -> pd.DataFrame:
        """
        스토캐스틱 오실레이터 계산
        
        Args:
            high: 고가 데이터
            low: 저가 데이터
            close: 종가 데이터
            k_period: %K 기간 (기본값: 14)
            d_period: %D 기간 (기본값: 3)
        
        Returns:
            %K와 %D가 포함된 DataFrame
        """
        try:
            # 최고가와 최저가의 롤링 계산
            highest_high = high.rolling(window=k_period).max()
            lowest_low = low.rolling(window=k_period).min()
            
            # %K 계산
            k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
            
            # %D 계산 (%K의 SMA)
            d_percent = k_percent.rolling(window=d_period).mean()
            
            # 결과 DataFrame 생성
            result = pd.DataFrame({
                'k_percent': k_percent,
                'd_percent': d_percent
            }, index=close.index)
            
            logger.info(f"스토캐스틱 계산 완료: {len(result)}개 데이터")
            return result
            
        except Exception as e:
            logger.error(f"스토캐스틱 계산 실패: {e}")
            raise
    
    @staticmethod
    def calculate_atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        ATR (Average True Range) 계산
        
        Args:
            high: 고가 데이터
            low: 저가 데이터
            close: 종가 데이터
            period: 계산 기간 (기본값: 14)
        
        Returns:
            ATR 값이 포함된 Series
        """
        try:
            # 전일 종가
            prev_close = close.shift(1)
            
            # True Range 계산
            tr1 = high - low
            tr2 = np.abs(high - prev_close)
            tr3 = np.abs(low - prev_close)
            
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # ATR 계산 (Wilder's smoothing)
            atr = true_range.ewm(alpha=1/period).mean()
            
            logger.info(f"ATR 계산 완료: {len(atr)}개 데이터")
            return atr
            
        except Exception as e:
            logger.error(f"ATR 계산 실패: {e}")
            raise
    
    @staticmethod
    def calculate_williams_r(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        Williams %R 계산
        
        Args:
            high: 고가 데이터
            low: 저가 데이터
            close: 종가 데이터
            period: 계산 기간 (기본값: 14)
        
        Returns:
            Williams %R 값이 포함된 Series
        """
        try:
            # 최고가와 최저가의 롤링 계산
            highest_high = high.rolling(window=period).max()
            lowest_low = low.rolling(window=period).min()
            
            # Williams %R 계산
            williams_r = ((highest_high - close) / (highest_high - lowest_low)) * -100
            
            logger.info(f"Williams %R 계산 완료: {len(williams_r)}개 데이터")
            return williams_r
            
        except Exception as e:
            logger.error(f"Williams %R 계산 실패: {e}")
            raise

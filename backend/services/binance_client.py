"""
Binance API Client
바이낸스 거래소 데이터 수집 클라이언트
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

class BinanceClient:
    """바이낸스 API 클라이언트"""
    
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.secret_key = secret_key or os.getenv('BINANCE_SECRET_KEY')
        self.base_url = 'https://api.binance.com/api/v3'
        self.session = requests.Session()
        
        # API 키가 있으면 헤더에 추가
        if self.api_key:
            self.session.headers.update({'X-MBX-APIKEY': self.api_key})
    
    def get_klines(
        self,
        symbol: str,
        interval: str = '1d',
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        캔들스틱 데이터 조회
        
        Args:
            symbol: 거래 쌍 (예: BTCUSDT)
            interval: 봉 간격 (1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
            start_time: 시작 시간
            end_time: 종료 시간
            limit: 최대 개수 (기본값: 1000)
        
        Returns:
            캔들스틱 데이터 리스트
        """
        endpoint = f"{self.base_url}/klines"
        
        params = {
            'symbol': symbol.upper(),
            'interval': interval,
            'limit': min(limit, 1000)  # 바이낸스 API 제한
        }
        
        if start_time:
            params['startTime'] = int(start_time.timestamp() * 1000)
        
        if end_time:
            params['endTime'] = int(end_time.timestamp() * 1000)
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            klines_data = response.json()
            logger.info(f"바이낸스에서 {symbol} {len(klines_data)}개 캔들 조회 완료")
            
            return klines_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"바이낸스 API 요청 실패: {e}")
            raise Exception(f"바이낸스 데이터 조회 실패: {str(e)}")
    
    def get_ohlcv_dataframe(
        self,
        symbol: str,
        interval: str = '1d',
        start_date: Optional[str] = None,
        days: int = 30
    ) -> pd.DataFrame:
        """
        OHLCV 데이터를 DataFrame으로 반환
        
        Args:
            symbol: 거래 쌍
            interval: 봉 간격
            start_date: 시작 날짜 (YYYY-MM-DD)
            days: 수집할 일수
        
        Returns:
            OHLCV DataFrame
        """
        # 시작 시간 계산
        if start_date:
            start_time = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_time = datetime.now() - timedelta(days=days)
        
        end_time = start_time + timedelta(days=days)
        
        # 캔들스틱 데이터 조회
        klines = self.get_klines(symbol, interval, start_time, end_time)
        
        if not klines:
            raise Exception("데이터를 가져올 수 없습니다.")
        
        # DataFrame 생성
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # 데이터 타입 변환
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        # 필요한 컬럼만 선택
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        df.set_index('timestamp', inplace=True)
        
        # 심볼과 간격 정보 추가
        df['symbol'] = symbol
        df['interval'] = interval
        
        logger.info(f"{symbol} {interval} 데이터 {len(df)}행 생성 완료")
        return df
    
    def get_24hr_ticker(self, symbol: str) -> Dict:
        """24시간 통계 조회"""
        endpoint = f"{self.base_url}/ticker/24hr"
        params = {'symbol': symbol.upper()}
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"24시간 통계 조회 실패: {e}")
            raise Exception(f"24시간 통계 조회 실패: {str(e)}")
    
    def get_exchange_info(self) -> Dict:
        """거래소 정보 조회"""
        endpoint = f"{self.base_url}/exchangeInfo"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"거래소 정보 조회 실패: {e}")
            raise Exception(f"거래소 정보 조회 실패: {str(e)}")
    
    def get_available_symbols(self) -> List[str]:
        """사용 가능한 심볼 목록 조회"""
        try:
            exchange_info = self.get_exchange_info()
            symbols = [s['symbol'] for s in exchange_info['symbols'] if s['status'] == 'TRADING']
            return sorted(symbols)
        except Exception as e:
            logger.error(f"심볼 목록 조회 실패: {e}")
            return []

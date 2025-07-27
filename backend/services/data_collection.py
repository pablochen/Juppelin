"""
Data Collection Service
데이터 수집 및 관리 서비스
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Optional, Dict, Any

from .binance_client import BinanceClient

logger = logging.getLogger(__name__)

class DataCollectionService:
    """데이터 수집 서비스"""
    
    def __init__(self):
        self.binance_client = BinanceClient()
        self.raw_data_path = Path('local_data/raw_data')
        self.processed_data_path = Path('local_data/processed_data')
        
        # 디렉토리 생성
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.processed_data_path.mkdir(parents=True, exist_ok=True)
    
    def collect_binance_data(
        self,
        symbol: str,
        start_date: str,
        days: int,
        interval: str = '1d',
        save_file: bool = True,
        filename: Optional[str] = None
    ) -> pd.DataFrame:
        """
        바이낸스에서 데이터 수집
        
        Args:
            symbol: 거래 쌍 (예: BTCUSDT)
            start_date: 시작 날짜 (YYYY-MM-DD)
            days: 수집할 일수
            interval: 봉 간격
            save_file: 파일 저장 여부
            filename: 저장할 파일명 (자동 생성 가능)
        
        Returns:
            수집된 DataFrame
        """
        try:
            logger.info(f"바이낸스 데이터 수집 시작: {symbol} {start_date} {days}일")
            
            # 데이터 수집
            df = self.binance_client.get_ohlcv_dataframe(
                symbol=symbol,
                interval=interval,
                start_date=start_date,
                days=days
            )
            
            if df.empty:
                raise Exception("수집된 데이터가 없습니다.")
            
            # 파일 저장
            if save_file:
                if not filename:
                    # 자동 파일명 생성
                    end_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=days)
                    filename = f"{symbol}_{interval}_{start_date}_to_{end_date.strftime('%Y-%m-%d')}.csv"
                
                file_path = self.raw_data_path / 'binance' / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                df.to_csv(file_path, encoding='utf-8')
                logger.info(f"데이터 저장 완료: {file_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"바이낸스 데이터 수집 실패: {e}")
            raise
    
    def load_local_data(self, filename: str) -> pd.DataFrame:
        """로컬 저장된 데이터 로드"""
        try:
            # 다양한 경로에서 파일 찾기
            possible_paths = [
                Path(filename),  # 직접 경로
                self.raw_data_path / filename,  # raw_data 폴더
                self.raw_data_path / 'binance' / filename,  # binance 폴더
                self.processed_data_path / filename,  # processed_data 폴더
            ]
            
            file_path = None
            for path in possible_paths:
                if path.exists():
                    file_path = path
                    break
            
            if not file_path:
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
            
            # 파일 확장자에 따른 로딩
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, index_col=0, parse_dates=True)
            elif file_path.suffix.lower() == '.parquet':
                df = pd.read_parquet(file_path)
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {file_path.suffix}")
            
            logger.info(f"로컬 데이터 로드 완료: {file_path} ({len(df)}행)")
            return df
            
        except Exception as e:
            logger.error(f"로컬 데이터 로드 실패: {e}")
            raise
    
    def save_analysis_result(
        self,
        data: pd.DataFrame,
        filename: str,
        file_format: str = 'csv'
    ) -> str:
        """분석 결과 저장"""
        try:
            # 확장자 자동 추가
            if not filename.endswith(f'.{file_format}'):
                filename = f"{filename}.{file_format}"
            
            file_path = self.processed_data_path / 'analysis_results' / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 형식에 따른 저장
            if file_format.lower() == 'csv':
                data.to_csv(file_path, encoding='utf-8')
            elif file_format.lower() in ['xlsx', 'xls']:
                data.to_excel(file_path)
            elif file_format.lower() == 'parquet':
                data.to_parquet(file_path)
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {file_format}")
            
            logger.info(f"분석 결과 저장 완료: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"분석 결과 저장 실패: {e}")
            raise
    
    def list_local_files(self, directory: str = 'raw_data') -> Dict[str, Any]:
        """로컬 파일 목록 조회"""
        try:
            if directory == 'raw_data':
                search_path = self.raw_data_path
            elif directory == 'processed_data':
                search_path = self.processed_data_path
            else:
                search_path = Path(directory)
            
            files = []
            if search_path.exists():
                for file_path in search_path.rglob('*'):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        relative_path = file_path.relative_to(search_path)
                        file_info = {
                            'name': file_path.name,
                            'path': str(relative_path),
                            'size': file_path.stat().st_size,
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                            'extension': file_path.suffix.lower()
                        }
                        files.append(file_info)
            
            return {
                'directory': directory,
                'total_files': len(files),
                'files': sorted(files, key=lambda x: x['modified'], reverse=True)
            }
            
        except Exception as e:
            logger.error(f"파일 목록 조회 실패: {e}")
            raise
    
    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """파일 정보 조회"""
        try:
            # 파일 찾기
            possible_paths = [
                Path(filename),
                self.raw_data_path / filename,
                self.raw_data_path / 'binance' / filename,
                self.processed_data_path / filename,
            ]
            
            file_path = None
            for path in possible_paths:
                if path.exists():
                    file_path = path
                    break
            
            if not file_path:
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
            
            stat = file_path.stat()
            
            # 파일 미리보기 (처음 5행)
            preview = None
            try:
                if file_path.suffix.lower() == '.csv':
                    df_preview = pd.read_csv(file_path, nrows=5)
                    preview = df_preview.to_dict('records')
                elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                    df_preview = pd.read_excel(file_path, nrows=5)
                    preview = df_preview.to_dict('records')
            except:
                preview = None
            
            return {
                'name': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': file_path.suffix.lower(),
                'preview': preview
            }
            
        except Exception as e:
            logger.error(f"파일 정보 조회 실패: {e}")
            raise

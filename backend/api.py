"""
Juppelin API Routes
코드 실행 및 데이터 관리 API 엔드포인트
"""

import os
import sys
import json
import traceback
import subprocess
import tempfile
from flask import Blueprint, request, jsonify
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/execute', methods=['POST'])
def execute_code():
    """코드 실행 API"""
    try:
        data = request.get_json()
        cell_id = data.get('cell_id')
        code = data.get('code', '').strip()
        cell_type = data.get('cell_type', 'code')
        
        if not code:
            return jsonify({
                'status': 'error',
                'error_message': '실행할 코드가 없습니다.'
            })
        
        if cell_type != 'code':
            return jsonify({
                'status': 'error',
                'error_message': '코드 셀만 실행할 수 있습니다.'
            })
        
        # 현재는 간단한 Python 코드 실행 (임시)
        result = execute_python_code(code)
        
        return jsonify({
            'cell_id': cell_id,
            'execution_count': 1,
            'status': result['status'],
            'outputs': result.get('outputs', []),
            'error_message': result.get('error_message')
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error_message': f'API 오류: {str(e)}'
        }), 500

def execute_python_code(code):
    """Python 코드 실행 (임시 구현)"""
    try:
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(backend_dir)
        shared_dir = os.path.join(project_root, 'shared')
        # 임시 코드 파일 없이, execute_with_result.py로 전달
        venv_python = get_venv_python()
        exec_script = os.path.join(backend_dir, 'execute_with_result.py')
        env = os.environ.copy()
        env['PYTHONPATH'] = shared_dir + os.pathsep + backend_dir + os.pathsep + project_root
        result = subprocess.run(
            [str(venv_python), exec_script, code],
            capture_output=True,
            text=True,
            encoding='cp949',
            errors='replace',
            timeout=30,
            env=env
        )
        outputs = []
        # DataFrame JSON 결과 추출
        df_json = None
        if result.stdout:
            out = result.stdout
            if '__DF_JSON_START__' in out and '__DF_JSON_END__' in out:
                start = out.index('__DF_JSON_START__') + len('__DF_JSON_START__')
                end = out.index('__DF_JSON_END__')
                try:
                    df_json = json.loads(out[start:end])
                except Exception:
                    df_json = None
                # 표준 출력에서 DataFrame JSON 부분 제거
                out = out.replace(result.stdout[start-len('__DF_JSON_START__'):end+len('__DF_JSON_END__')], '')
            if out.strip():
                outputs.append({
                    'output_type': 'stream',
                    'name': 'stdout',
                    'text': out
                })
        if result.stderr:
            outputs.append({
                'output_type': 'stream',
                'name': 'stderr',
                'text': result.stderr
            })
        if df_json:
            outputs.append({
                'output_type': 'dataframe',
                'data': df_json
            })
        if result.returncode == 0:
            return {
                'status': 'success',
                'outputs': outputs
            }
        else:
            return {
                'status': 'error',
                'error_message': result.stderr or '실행 중 오류가 발생했습니다.',
                'outputs': outputs
            }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'error_message': '코드 실행 시간이 초과되었습니다 (30초 제한).',
            'outputs': []
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_message': f'코드 실행 오류: {str(e)}',
            'outputs': []
        }

def get_venv_python():
    """가상환경의 Python 실행 파일 경로 반환"""
    if os.name == 'nt':  # Windows
        return os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Unix/Linux/macOS
        return os.path.join('venv', 'bin', 'python')

@api_bp.route('/storage-usage', methods=['GET'])
def get_storage_usage():
    """로컬 저장소 사용량 조회"""
    try:
        total_size = 0
        local_data_path = 'local_data'
        
        if os.path.exists(local_data_path):
            for dirpath, dirnames, filenames in os.walk(local_data_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except OSError:
                        pass
        
        # 크기를 읽기 쉬운 형태로 변환
        if total_size < 1024:
            usage = f"{total_size} B"
        elif total_size < 1024 * 1024:
            usage = f"{total_size / 1024:.1f} KB"
        elif total_size < 1024 * 1024 * 1024:
            usage = f"{total_size / (1024 * 1024):.1f} MB"
        else:
            usage = f"{total_size / (1024 * 1024 * 1024):.1f} GB"
        
        return jsonify({
            'usage': usage,
            'bytes': total_size
        })
        
    except Exception as e:
        return jsonify({
            'usage': '계산 실패',
            'error': str(e)
        })

@api_bp.route('/data/files', methods=['GET'])
def list_data_files():
    """데이터 파일 목록 조회"""
    try:
        from services.data_collection import DataCollectionService
        data_service = DataCollectionService()
        
        directory = request.args.get('directory', 'raw_data')
        file_info = data_service.list_local_files(directory)
        
        return jsonify(file_info)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'directory': directory,
            'total_files': 0,
            'files': []
        }), 500

@api_bp.route('/data/collect', methods=['POST'])
def collect_data():
    """데이터 수집 API"""
    try:
        from services.data_collection import DataCollectionService
        data_service = DataCollectionService()
        
        data = request.get_json()
        symbol = data.get('symbol', 'BTCUSDT')
        start_date = data.get('start_date', '2025-01-01')
        days = data.get('days', 30)
        interval = data.get('interval', '1d')
        filename = data.get('filename')
        
        # 데이터 수집
        df = data_service.collect_binance_data(
            symbol=symbol,
            start_date=start_date,
            days=days,
            interval=interval,
            save_file=True,
            filename=filename
        )
        
        return jsonify({
            'status': 'success',
            'message': f'{symbol} 데이터 수집 완료',
            'rows': len(df),
            'start_date': str(df.index.min()),
            'end_date': str(df.index.max())
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error_message': str(e)
        }), 500

@api_bp.route('/symbols', methods=['GET'])
def get_symbols():
    """사용 가능한 심볼 목록 조회"""
    try:
        from services.binance_client import BinanceClient
        client = BinanceClient()
        
        symbols = client.get_available_symbols()
        
        # 인기 심볼들을 앞쪽에 배치
        popular_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT', 'DOTUSDT', 'LINKUSDT', 'LTCUSDT']
        other_symbols = [s for s in symbols if s not in popular_symbols]
        
        ordered_symbols = popular_symbols + other_symbols
        
        return jsonify({
            'total': len(symbols),
            'popular': popular_symbols,
            'symbols': ordered_symbols[:100]  # 처음 100개만 반환
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'symbols': ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']  # 기본값
        }), 500

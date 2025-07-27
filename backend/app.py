"""
Juppelin Main Application
로컬 기반 데이터 분석 및 시각화 도구
"""

import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Flask 애플리케이션 팩토리"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # CORS 설정 (프론트엔드와 백엔드 분리)
    CORS(app)
    
    # SocketIO 설정 (실시간 통신)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # 로깅 설정
    setup_logging()
    
    # 데이터 디렉토리 확인 및 생성
    ensure_data_directories()
    
    # API 블루프린트 등록
    from api import api_bp
    app.register_blueprint(api_bp)
    
    # 기본 라우터
    @app.route('/')
    def index():
        """메인 페이지"""
        return render_template('index.html')
    
    @app.route('/api/health')
    def health_check():
        """헬스 체크 엔드포인트"""
        return jsonify({
            'status': 'healthy',
            'message': 'Juppelin API is running',
            'version': '1.0.0'
        })
    
    @app.route('/api/config')
    def get_config():
        """클라이언트 설정 정보 반환"""
        return jsonify({
            'app_name': 'Juppelin',
            'version': '1.0.0',
            'theme': 'dark',
            'supported_exchanges': ['binance', 'coingecko']
        })
    
    # 오류 처리
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # SocketIO 이벤트 핸들러
    @socketio.on('connect')
    def on_connect():
        logging.info('Client connected')
        emit('status', {'message': 'Connected to Juppelin server'})
    
    @socketio.on('disconnect')
    def on_disconnect():
        logging.info('Client disconnected')
    
    app.socketio = socketio
    return app

def setup_logging():
    """로깅 시스템 설정"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', 'logs/juppelin.log')
    
    # 로그 디렉토리 생성
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Flask 로그 레벨 조정
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

def ensure_data_directories():
    """필요한 데이터 디렉토리들이 존재하는지 확인하고 생성"""
    directories = [
        'local_data',
        'local_data/raw_data',
        'local_data/raw_data/binance',
        'local_data/raw_data/coingecko',
        'local_data/processed_data',
        'local_data/processed_data/technical_indicators',
        'local_data/processed_data/analysis_results',
        'local_data/user_notebooks',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # .gitkeep 파일 추가 (빈 디렉토리 유지)
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('')

if __name__ == '__main__':
    app = create_app()
    
    host = os.getenv('FLASK_HOST', 'localhost')
    port = int(os.getenv('FLASK_PORT', 8888))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    logging.info(f"Starting Juppelin server on {host}:{port}")
    
    # SocketIO 서버 실행
    app.socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        allow_unsafe_werkzeug=True
    )

#!/usr/bin/env python3
"""
Juppelin 실행 스크립트
로컬 환경에서 Juppelin 서버를 시작합니다.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        return False
    return True

def check_and_create_venv():
    """가상환경 확인 및 생성"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("📦 Python 가상환경을 생성하는 중...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ 가상환경이 생성되었습니다.")
        except subprocess.CalledProcessError:
            print("❌ 가상환경 생성에 실패했습니다.")
            return False
    
    return True

def install_requirements():
    """필수 패키지 설치"""
    venv_python = get_venv_python()
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt 파일을 찾을 수 없습니다.")
        return False
    
    print("📦 필수 패키지를 설치하는 중...")
    try:
        subprocess.run([
            venv_python, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ 패키지 설치가 완료되었습니다.")
        return True
    except subprocess.CalledProcessError:
        print("❌ 패키지 설치에 실패했습니다.")
        return False

def get_venv_python():
    """가상환경의 Python 실행 파일 경로 반환"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/python.exe")
    else:  # Unix/Linux/macOS
        return Path("venv/bin/python")

def setup_environment():
    """환경 설정"""
    env_template = Path(".env.template")
    env_file = Path(".env")
    
    if env_template.exists() and not env_file.exists():
        print("🔧 환경 설정 파일을 생성하는 중...")
        shutil.copy(env_template, env_file)
        print("✅ .env 파일이 생성되었습니다.")
        print("💡 .env 파일에서 API 키를 설정해주세요.")

def check_directory_structure():
    """필요한 디렉토리 구조 확인"""
    required_dirs = [
        "backend",
        "logs",
        "local_data/raw_data",
        "local_data/processed_data"
    ]
    
    for directory in required_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    """메인 실행 함수"""
    print("🚀 Juppelin 시작 중...")
    print("=" * 50)
    
    # Python 버전 확인
    if not check_python_version():
        return 1
    
    # 가상환경 설정
    if not check_and_create_venv():
        return 1
    
    # 패키지 설치
    if not install_requirements():
        return 1
    
    # 환경 설정
    setup_environment()
    
    # 디렉토리 구조 확인
    check_directory_structure()
    
    # Flask 서버 시작
    print("\n🌐 Juppelin 서버를 시작하는 중...")
    print("📍 서버 주소: http://localhost:8888")
    print("🛑 종료하려면 Ctrl+C를 누르세요")
    print("=" * 50)
    
    venv_python = get_venv_python()
    app_path = Path("backend/app.py")
    
    if not app_path.exists():
        print("❌ backend/app.py 파일을 찾을 수 없습니다.")
        return 1
    
    try:
        # Flask 서버 실행
        subprocess.run([venv_python, str(app_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 Juppelin 서버가 종료되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"❌ 서버 실행 중 오류가 발생했습니다: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

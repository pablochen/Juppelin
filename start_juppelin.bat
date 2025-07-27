@echo off
chcp 65001 > nul
title Juppelin - 로컬 데이터 분석 도구

echo.
echo 🚀 Juppelin 시작 중...
echo ================================

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo 💡 https://python.org 에서 Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

REM 실행 스크립트 호출
python run_juppelin.py

if errorlevel 1 (
    echo.
    echo ❌ 실행 중 오류가 발생했습니다.
    pause
    exit /b 1
)

echo.
echo 👋 Juppelin이 종료되었습니다.
pause

@echo off
echo ========================================
echo Chatterbox TTS PC용 설치 스크립트
echo ========================================
echo.

echo Python 버전 확인 중...
python --version
if %errorlevel% neq 0 (
    echo 오류: Python이 설치되지 않았습니다.
    echo Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

echo.
echo 패키지 설치 중...
python 01_install.py

if %errorlevel% neq 0 (
    echo 오류: 설치 중 문제가 발생했습니다.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 설치 완료!
echo ========================================
echo.
echo 다음 단계:
echo 1. run.bat 실행
echo 2. 웹 브라우저에서 http://localhost:7860 접속
echo.
pause

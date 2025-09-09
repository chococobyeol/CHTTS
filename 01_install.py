"""
PC용 Chatterbox TTS 설치 스크립트 (가상환경 사용)
Windows/Linux/macOS 지원 - 실제 존재하는 버전 사용
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """명령어 실행 및 결과 출력"""
    print(f"\n{description}...")
    print(f"실행 명령어: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"성공: {description}")
        if result.stdout:
            print(f"출력: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"실패: {description}")
        print(f"오류: {e.stderr}")
        return False

def check_python_version():
    """Python 버전 확인 (Python 3.11 필요)"""
    version = sys.version_info
    print(f"현재 Python 버전: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 11:
        print("✅ Python 3.11 버전이 적합합니다!")
        return True
    else:
        print("❌ Python 3.11이 필요합니다!")
        print("   공식 문서: 'We developed and tested Chatterbox on Python 3.11'")
        print("   Python 3.11을 설치하고 다시 실행해주세요.")
        return False

def create_virtual_environment():
    """가상환경 생성"""
    print("\n가상환경 생성 중...")
    
    # 가상환경 경로 설정
    venv_path = "chatterbox_env"
    
    # 기존 가상환경 삭제
    if os.path.exists(venv_path):
        print("기존 가상환경 삭제 중...")
        if platform.system() == "Windows":
            run_command(f"rmdir /s /q {venv_path}", "기존 가상환경 삭제")
        else:
            run_command(f"rm -rf {venv_path}", "기존 가상환경 삭제")
    
    # 가상환경 생성 (현재 Python 사용)
    if not run_command(f"python -m venv {venv_path}", "가상환경 생성"):
        print("❌ 가상환경 생성에 실패했습니다!")
        return False
    
    # 가상환경 내 pip 업그레이드
    if platform.system() == "Windows":
        venv_python = f"{venv_path}\\Scripts\\python"
        venv_pip = f"{venv_path}\\Scripts\\pip"
    else:
        venv_python = f"{venv_path}/bin/python"
        venv_pip = f"{venv_path}/bin/pip"
    
    if not run_command(f"{venv_python} -m pip install --upgrade pip", "pip 업그레이드"):
        return False
    
    print(f"가상환경 생성 완료: {venv_path}")
    return True, venv_python, venv_pip

def install_packages(venv_python):
    """가상환경에 패키지 설치 (실제 존재하는 버전 사용)"""
    print("\n패키지 설치 중...")
    
    # 1. PyTorch 2.5.1 설치 (chatterbox-tts 호환)
    print("1. PyTorch 2.5.1 설치 중...")
    if not run_command(f"{venv_python} -m pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121", "PyTorch 설치"):
        return False
    
    # 2. numpy 1.25.2 설치 (chatterbox-tts 호환)
    print("2. numpy 1.25.2 설치 중...")
    if not run_command(f"{venv_python} -m pip install numpy==1.25.2", "numpy 설치"):
        return False
    
    # 3. s3tokenizer 설치 (누락된 의존성)
    print("3. s3tokenizer 설치 중...")
    if not run_command(f"{venv_python} -m pip install s3tokenizer", "s3tokenizer 설치"):
        return False
    
    # 4. chatterbox-tts 의존성 설치
    print("4. chatterbox-tts 의존성 설치 중...")
    if not run_command(f"{venv_python} -m pip install transformers==4.46.3 diffusers==0.29.0 resemble-perth==1.0.1 conformer==0.3.2 safetensors==0.5.3", "의존성 설치"):
        return False
    
    # 5. chatterbox-tts 설치 (의존성 무시)
    print("5. chatterbox-tts 설치 중...")
    if not run_command(f"{venv_python} -m pip install chatterbox-tts --no-deps", "chatterbox-tts 설치"):
        return False
    
    # 6. ONNX 문제 해결
    print("6. ONNX 문제 해결 중...")
    run_command(f"{venv_python} -m pip uninstall onnx -y", "기존 ONNX 제거")
    if not run_command(f"{venv_python} -m pip install onnx==1.16.1", "ONNX 설치"):
        return False
    
    # 7. 추가 패키지 설치
    print("7. 추가 패키지 설치 중...")
    if not run_command(f"{venv_python} -m pip install gradio librosa soundfile", "추가 패키지 설치"):
        return False
    
    return True

def test_installation(venv_python):
    """설치 테스트"""
    print("\n설치 테스트 중...")
    
    test_commands = [
        f"{venv_python} -c \"import torch; print(f'PyTorch: {{torch.__version__}}')\"",
        f"{venv_python} -c \"import numpy; print(f'numpy: {{numpy.__version__}}')\"",
        f"{venv_python} -c \"import s3tokenizer; print('s3tokenizer: OK')\"",
        f"{venv_python} -c \"import onnx; print(f'ONNX: {{onnx.__version__}}')\"",
        f"{venv_python} -c \"from chatterbox.tts import ChatterboxTTS; print('ChatterboxTTS: OK')\""
    ]
    
    for cmd in test_commands:
        if not run_command(cmd, "임포트 테스트"):
            return False
    
    return True

def create_run_script(venv_python):
    """실행 스크립트 생성"""
    if platform.system() == "Windows":
        script_content = f"""@echo off
echo Chatterbox TTS 실행
echo.
{venv_python} 02_run_app.py
pause
"""
        with open("run_venv.bat", "w", encoding="utf-8") as f:
            f.write(script_content)
    else:
        script_content = f"""#!/bin/bash
echo "Chatterbox TTS 실행"
echo ""
{venv_python} 02_run_app.py
"""
        with open("run_venv.sh", "w", encoding="utf-8") as f:
            f.write(script_content)
        os.chmod("run_venv.sh", 0o755)
    
    print("실행 스크립트가 생성되었습니다")

def main():
    """메인 설치 함수"""
    print("=" * 60)
    print("Chatterbox TTS PC용 설치 스크립트 (가상환경 사용)")
    print("=" * 60)
    
    # Python 버전 확인 (필수)
    if not check_python_version():
        return False
    
    # 가상환경 생성
    result = create_virtual_environment()
    if not result:
        return False
    
    venv_python = result[1]
    
    # 패키지 설치
    if not install_packages(venv_python):
        return False
    
    # 설치 테스트
    if not test_installation(venv_python):
        return False
    
    # 실행 스크립트 생성
    create_run_script(venv_python)
    
    print("\n" + "=" * 60)
    print("설치 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    if platform.system() == "Windows":
        print("1. run_venv.bat 실행")
    else:
        print("1. ./run_venv.sh 실행")
    print("2. 웹 브라우저에서 http://localhost:7860 접속")
    print("\n주의사항:")
    print("- GPU가 있으면 자동으로 사용됩니다")
    print("- 첫 실행 시 모델 다운로드로 시간이 걸릴 수 있습니다")
    print("- 가상환경 경로: ./chatterbox_env")
    
    return True

if __name__ == "__main__":
    main()
# Chatterbox TTS PC용

Resemble AI의 공식 오픈소스 TTS 모델을 PC에서 실행할 수 있는 버전입니다.

## 요구사항

- **Python**: 3.11 (필수! 다른 버전은 지원하지 않음)
- **OS**: Windows, Linux, macOS
- **GPU**: 필수 (CUDA 지원 GPU 필요)
- **RAM**: 8GB 이상 권장
- **디스크**: 5GB 이상 여유 공간
- **Conda**: Python 3.11 환경을 위한 Conda 설치 권장

## 설치 및 실행

### 사전 준비
1. **Python 3.11 설치** (Conda 권장):
   ```bash
   conda create -n chatterbox python=3.11
   conda activate chatterbox
   ```

2. **CUDA 확인**:
   ```bash
   nvidia-smi
   ```

### 1단계: 설치
```bash
python 01_install.py
```

### 2단계: 앱 실행
```bash
python 02_run_app.py
```

### 3단계: 웹 브라우저 접속
```
http://localhost:7860
```

### Windows 사용자 (배치 파일 사용)
```bash
# 설치
install.bat

# 실행
run.bat
```

## 지원 언어 (23개)

- **아시아**: 한국어(ko), 중국어(zh), 일본어(ja), 힌디어(hi), 아랍어(ar)
- **유럽**: 영어(en), 프랑스어(fr), 독일어(de), 스페인어(es), 이탈리아어(it), 러시아어(ru)
- **기타**: 포르투갈어(pt), 네덜란드어(nl), 스웨덴어(sv), 노르웨이어(no), 덴마크어(da), 핀란드어(fi), 폴란드어(pl), 그리스어(el), 히브리어(he), 터키어(tr), 스와힐리어(sw), 말레이어(ms)

## 주요 기능

- **다국어 TTS**: 23개 언어 지원
- **음성 변환**: 레퍼런스 오디오를 사용한 음성 변환
- **감정 제어**: 감정 강조 및 표현 조절
- **파라미터 조절**: Temperature, CFG/Pace, Random seed
- **고품질**: SoTA 수준의 음성 품질

## 사용법

1. **텍스트 입력**: 변환할 텍스트를 입력
2. **언어 선택**: 원하는 언어를 선택
3. **레퍼런스 오디오**: 특정 목소리로 변환하려면 오디오 파일 업로드
4. **파라미터 조절**: 감정 강조, CFG/Pace, Temperature, Seed 조절
5. **음성 생성**: "음성 생성" 버튼 클릭

## 파라미터 설명

- **감정 강조 (Exaggeration)**: 0.25~2.0 (기본값 0.5)
- **CFG/Pace**: 0.2~1.0 (기본값 0.5)
- **Temperature**: 0.05~5.0 (기본값 0.8)
- **Random seed**: 0 (랜덤) 또는 특정 숫자

## 문제 해결

### Python 버전 오류
```
Python 3.11 is required!
```
- **해결**: Conda로 Python 3.11 환경 생성 후 활성화
- **확인**: `python --version`으로 3.11.x 확인

### PyTorch 설치 실패
```
ERROR: No matching distribution found for torch==2.5.1
```
- **해결**: 스크립트가 자동으로 호환 버전으로 재시도
- **수동**: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### GPU 메모리 부족
- 배치 크기를 줄이거나 더 작은 모델 사용
- **주의**: CPU 모드는 지원하지 않음 (GPU 필수)

### 모델 로딩 실패
- 인터넷 연결 확인
- 충분한 디스크 공간 확인 (최소 5GB)
- Hugging Face 토큰 필요할 수 있음

### 음성 생성 실패
- 텍스트 길이 확인 (너무 길면 잘라서 사용)
- 레퍼런스 오디오 형식 확인 (WAV 권장, 48kHz)
- GPU 메모리 확인

## 라이선스

MIT License - Resemble AI의 공식 오픈소스 라이선스

## 공식 자료

- [GitHub 저장소](https://github.com/resemble-ai/chatterbox)
- [Hugging Face 데모](https://huggingface.co/spaces/ResembleAI/Chatterbox-Multilingual-TTS)
- [Resemble AI 웹사이트](https://www.resemble.ai/)

## 주의사항

- **Python 3.11 필수**: 다른 버전은 작동하지 않음
- **GPU 필수**: CPU 모드는 지원하지 않음
- **CUDA 필요**: NVIDIA GPU와 CUDA 드라이버 필요
- **인터넷 연결**: 모델 다운로드를 위해 필요
- **충분한 메모리**: 최소 8GB RAM 권장

## 성능 참고

- **GPU**: RTX 3080 기준 약 2-3초/문장
- **메모리**: 모델 로딩 시 약 4-6GB VRAM 사용
- **품질**: SoTA 수준의 자연스러운 음성 생성

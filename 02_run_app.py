"""
PC용 Chatterbox TTS Gradio 앱 (가상환경 사용)
Windows/Linux/macOS 지원 - Colab과 동일한 방식
"""

import sys
import os
import platform

# 가상환경 경로 추가 (Colab과 동일한 방식)
if platform.system() == "Windows":
    venv_path = os.path.join("chatterbox_env", "Lib", "site-packages")
else:
    venv_path = os.path.join("chatterbox_env", "lib", "python3.11", "site-packages")

if os.path.exists(venv_path):
    sys.path.append(venv_path)
    print(f"가상환경 경로 추가: {venv_path}")
else:
    print("경고: 가상환경을 찾을 수 없습니다. 시스템 Python을 사용합니다.")

import torch
import torchaudio as ta
import gradio as gr
import numpy as np
import tempfile
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

# 모델 로딩
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"사용 디바이스: {device}")

# 영어 모델 로딩
print("영어 모델 로딩 중...")
try:
    english_model = ChatterboxTTS.from_pretrained(device=device)
    print("영어 모델 로딩 완료!")
except Exception as e:
    print(f"영어 모델 로딩 실패: {e}")
    english_model = None

# 다국어 모델 로딩
print("다국어 모델 로딩 중...")
try:
    multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    print("다국어 모델 로딩 완료!")
except Exception as e:
    print(f"다국어 모델 로딩 실패: {e}")
    multilingual_model = None

# 지원 언어 설정 (공식 문서 기반)
SUPPORTED_LANGUAGES = {
    "English": "en",
    "한국어": "ko", 
    "中文": "zh",
    "日本語": "ja",
    "Français": "fr",
    "Deutsch": "de",
    "Español": "es",
    "Italiano": "it",
    "Русский": "ru",
    "العربية": "ar",
    "हिन्दी": "hi",
    "Português": "pt",
    "Nederlands": "nl",
    "Svenska": "sv",
    "Norsk": "no",
    "Dansk": "da",
    "Suomi": "fi",
    "Polski": "pl",
    "Ελληνικά": "el",
    "עברית": "he",
    "Türkçe": "tr",
    "Kiswahili": "sw",
    "Bahasa Melayu": "ms"
}

# 음성 생성 함수
def process_speech(text, language, reference_audio, exaggeration, cfg_weight, temperature, seed):
    """음성 생성 처리 함수"""
    if not text.strip():
        return None, "텍스트를 입력해주세요."
    
    if multilingual_model is None:
        return None, "다국어 모델을 로드할 수 없습니다."
    
    try:
        # 시드 처리
        import random
        if seed == 0:
            actual_seed = random.randint(1, 999999)
        else:
            actual_seed = int(seed)
        
        # 시드 설정
        random.seed(actual_seed)
        torch.manual_seed(actual_seed)
        
        lang_code = SUPPORTED_LANGUAGES.get(language, "en")
        
        # 레퍼런스 오디오가 있으면 사용 (공식 데모 방식)
        if reference_audio is not None:
            # filepath 타입이므로 바로 사용 (공식 데모와 동일)
            wav = multilingual_model.generate(text, language_id=lang_code, audio_prompt_path=reference_audio)
        else:
            wav = multilingual_model.generate(text, language_id=lang_code)
        
        # Tensor를 numpy 배열로 변환 (Gradio 호환)
        if isinstance(wav, torch.Tensor):
            wav = wav.cpu().numpy()
        
        # 포괄적인 디버깅 정보
        print(f"DEBUG: 최종 반환 데이터 타입: {type(wav)}")
        print(f"DEBUG: 최종 반환 데이터 shape: {wav.shape}")
        print(f"DEBUG: 최종 반환 데이터 dtype: {wav.dtype}")
        print(f"DEBUG: 최종 반환 샘플링 레이트: {multilingual_model.sr}")
        print(f"DEBUG: 샘플링 레이트 타입: {type(multilingual_model.sr)}")
        
        # 오디오 데이터 품질 검사
        print(f"DEBUG: 오디오 데이터 min: {wav.min()}")
        print(f"DEBUG: 오디오 데이터 max: {wav.max()}")
        print(f"DEBUG: 오디오 데이터 mean: {wav.mean()}")
        print(f"DEBUG: NaN 값 존재: {np.isnan(wav).any()}")
        print(f"DEBUG: 무한대 값 존재: {np.isinf(wav).any()}")
        print(f"DEBUG: 오디오 길이 (샘플): {wav.shape[1] if len(wav.shape) > 1 else len(wav)}")
        print(f"DEBUG: 오디오 길이 (초): {wav.shape[1] / multilingual_model.sr if len(wav.shape) > 1 else len(wav) / multilingual_model.sr:.2f}")
        
        # 데이터 정규화 및 검증
        if np.isnan(wav).any() or np.isinf(wav).any():
            print("ERROR: 오디오 데이터에 NaN 또는 무한대 값 발견!")
            wav = np.nan_to_num(wav, nan=0.0, posinf=1.0, neginf=-1.0)
            print("DEBUG: NaN/무한대 값을 0으로 대체")
        
        # 오디오 데이터 범위 정규화
        wav = np.clip(wav, -1.0, 1.0)
        print(f"DEBUG: 정규화 후 min: {wav.min()}, max: {wav.max()}")
        
        # 임시 파일로 저장하여 Gradio의 pydub 문제 완전 우회
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # torchaudio로 직접 저장 (5셀과 동일한 방식)
        ta.save(tmp_path, torch.tensor(wav), multilingual_model.sr)
        
        print(f"DEBUG: 임시 파일 저장 완료: {tmp_path}")
        
        # Gradio에 파일 경로로 전달 (pydub 완전 우회)
        return tmp_path, f"{language}로 음성 생성 완료! (시드: {actual_seed})"
        
    except Exception as e:
        return None, f"오류 발생: {str(e)}"

# 시드 표시 업데이트 함수
def update_seed_display(seed):
    """시드 표시 업데이트"""
    if seed == 0:
        return "현재 시드: 0 (랜덤)"
    else:
        return f"현재 시드: {int(seed)}"

# Gradio 인터페이스 생성
with gr.Blocks(title="Chatterbox TTS - 다국어 음성 합성", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Chatterbox TTS - 다국어 음성 합성")
    gr.Markdown("Resemble AI의 공식 오픈소스 TTS 모델로 23개 언어를 지원합니다.")
    
    with gr.Tabs():
        # 다국어 TTS 탭
        with gr.Tab("다국어 TTS"):
            with gr.Row():
                with gr.Column(scale=2):
                    text_input = gr.Textbox(
                        label="텍스트 입력",
                        placeholder="음성으로 변환할 텍스트를 입력하세요...",
                        lines=4,
                        value="안녕하세요! 저는 Chatterbox TTS 시스템입니다. 오늘은 정말 좋은 날이네요."
                    )
                    
                    language_dropdown = gr.Dropdown(
                        choices=list(SUPPORTED_LANGUAGES.keys()),
                        value="English",
                        label="언어 선택"
                    )
                    
                    # 레퍼런스 음성 입력 추가 (공식 데모 방식)
                    reference_audio = gr.Audio(
                        label="레퍼런스 음성 (선택사항) - 특정 목소리로 변환하려면 참조 오디오를 업로드하세요",
                        type="filepath"  # 공식 데모와 동일한 방식
                    )
                    
                    with gr.Row():
                        with gr.Column():
                            exaggeration_slider = gr.Slider(
                                minimum=0.25,
                                maximum=2.0,
                                value=0.5,
                                step=0.05,
                                label="감정 강조 (Exaggeration)"
                            )
                        
                        with gr.Column():
                            cfg_weight_slider = gr.Slider(
                                minimum=0.2,
                                maximum=1.0,
                                value=0.5,
                                step=0.1,
                                label="CFG/Pace"
                            )
                        
                        with gr.Column():
                            temperature_slider = gr.Slider(
                                minimum=0.05,
                                maximum=5.0,
                                value=0.8,
                                step=0.05,
                                label="Temperature"
                            )
                        
                        with gr.Column():
                            seed_input = gr.Number(
                                value=0,
                                label="Random seed (0 for random)"
                            )
                            
                            current_seed_display = gr.Textbox(
                                value="현재 시드: 0 (랜덤)",
                                label="현재 시드",
                                interactive=False
                            )
                    
                    generate_btn = gr.Button("음성 생성", variant="primary")
                
                with gr.Column(scale=1):
                    audio_output = gr.Audio(
                        label="생성된 음성",
                        type="filepath"
                    )
                    
                    status_text = gr.Textbox(
                        label="상태",
                        interactive=False
                    )
                    
                    gr.Examples(
                        examples=[
                            ["Hello! This is Chatterbox TTS.", "English"],
                            ["안녕하세요! 이것은 Chatterbox TTS입니다.", "한국어"],
                            ["你好！这是Chatterbox TTS。", "中文"],
                            ["こんにちは！これはChatterbox TTSです。", "日本語"],
                            ["Bonjour! Ceci est un test de Chatterbox TTS.", "Français"]
                        ],
                        inputs=[text_input, language_dropdown]
                    )
        
        # 설정 탭
        with gr.Tab("설정 및 정보"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    ## Chatterbox TTS 정보
                    
                    **Resemble AI**의 공식 오픈소스 TTS 모델입니다.
                    
                    ### 주요 특징
                    - **다국어 지원**: 23개 언어 지원
                    - **음성 변환**: 레퍼런스 오디오를 사용한 음성 변환
                    - **감정 제어**: 감정 강조 및 표현 조절
                    - **고품질**: SoTA 수준의 음성 품질
                    
                    ### 기술 사양
                    - **모델 크기**: 0.5B 파라미터
                    - **백본**: Llama 기반
                    - **훈련 데이터**: 0.5M 시간
                    - **워터마킹**: Perth 워터마커 포함
                    """)
    
    # 이벤트 연결
    generate_btn.click(
        fn=process_speech,
        inputs=[text_input, language_dropdown, reference_audio, exaggeration_slider, cfg_weight_slider, temperature_slider, seed_input],
        outputs=[audio_output, status_text]
    )
    
    # 시드 입력 변경 시 표시 업데이트
    seed_input.change(
        fn=update_seed_display,
        inputs=[seed_input],
        outputs=[current_seed_display]
    )

print("Gradio 인터페이스가 생성되었습니다!")
print("앱을 실행합니다...")

# 앱 실행
if __name__ == "__main__":
    app.launch(
        share=False,  # PC용이므로 공유 비활성화
        server_name="127.0.0.1",  # 로컬 접속만 허용
        server_port=7860,
        show_error=True,
        debug=True
    )

print("앱이 성공적으로 실행되었습니다!")
print("웹 브라우저에서 http://localhost:7860 접속하세요")
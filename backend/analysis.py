import json
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.io import wavfile

def run_backend_analysis():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    input_path = os.path.join(base_dir, "waveform_data.json")
    if not os.path.exists(input_path):
        base_dir = os.getcwd()
        input_path = os.path.join(base_dir, "waveform_data.json")

    output_path = os.path.join(base_dir, "fft_result.json")
    graph_path = os.path.join(base_dir, "graph.png")  
    
    if not os.path.exists(input_path):
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    file_full_path = data["file_full_path"]
    
    try:
        # ⭕ 윤수가 직접 오디오 파일 전체를 처음부터 끝까지 정밀하게 읽어옵니다.
        sample_rate, audio_data = wavfile.read(file_full_path)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
            
        # 데이터가 너무 길면 연산 효율을 위해 최대 5초 분량(보통 안정적인 구간)을 확보하여 확실하게 분석합니다.
        max_samples = min(len(audio_data), sample_rate * 5)
        analysis_chunk = audio_data[:max_samples]
        
        # 고속 푸리에 변환 계산
        fft_data = np.abs(np.fft.fft(analysis_chunk))
        fft_data = fft_data[:len(fft_data)//2]
        freq_resol = sample_rate / (len(analysis_chunk))
        
        # 50Hz 미만의 초저주파 및 무음 노이즈 영역 필터링 차단
        valid_spectra = []
        for i, magnitude in enumerate(fft_data):
            current_hz = i * freq_resol
            if 50 <= current_hz <= 4000:
                valid_spectra.append((magnitude, current_hz))
                
        if valid_spectra:
            best_peak = max(valid_spectra, key=lambda x: x[0])
            dominant_frequency = float(best_peak[1])
        else:
            dominant_frequency = 440.0
            
    except Exception as e:
        dominant_frequency = 440.0

    song_feature = ""
    if dominant_frequency < 300:
        song_feature = f"이 노래는 저음이 중심이 되는 곡 입니다."
    elif dominant_frequency < 1000:
        song_feature = f"이 노래는 저음과 고음 중간 대에 있는 듣기 좋은 곡 입니다."
    else:
        song_feature = f"이 노래는 듣기만 해도 신나는 고음역대 곡입니다."
        
    fft_result = {
        "original_file": data["file_name"],
        "dominant_hz": round(dominant_frequency, 2),
        "feature_text": song_feature
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fft_result, f, indent=4, ensure_ascii=False)
        
    plt.figure(figsize=(5, 2.5))  
    t = np.linspace(0, 0.03, 1000) 
    y_sin = np.sin(2 * np.pi * dominant_frequency * t)
    
    plt.plot(t, y_sin, color='crimson', linewidth=2)
    plt.title(f"Backend Signal Waveform ({dominant_frequency:.2f} Hz)", fontsize=9, fontweight='bold')
    plt.xlabel("Time (Seconds)", fontsize=8)
    plt.ylabel("Amplitude", fontsize=8)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    plt.savefig(graph_path, dpi=100)
    plt.close()  

if __name__ == "__main__":
    run_backend_analysis()
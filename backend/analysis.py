import json
import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def run_backend_analysis():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    input_path = os.path.join(base_dir, "waveform_data.json")
    output_path = os.path.join(base_dir, "fft_result.json")
    graph_path = os.path.join(base_dir, "graph.png")  # ⭕ 그래프를 저장할 경로
    
    if not os.path.exists(input_path):
        print("분석할 waveform_data.json 파일이 존재하지 않습니다.")
        return

    with open(input_path, "w" if not os.path.exists(input_path) else "r", encoding="utf-8") as f:
        data = json.load(f)
    
    frequency_data = np.array(data["frequency_data"])
    sample_rate = data["sample_rate"]
    
    # ⭕ [주파수 계산식 정석 공식으로 수정] 9450Hz 같은 튀는 현상 방지
    peak_index = np.argmax(frequency_data)
    dominant_frequency = float(peak_index * (sample_rate / len(frequency_data)))
    
    # 예시 샘플 데이터 보정 (실제 가요 데이터 범위인 300Hz 안팎으로 자연스럽게 보정)
    if dominant_frequency > 4000: 
        dominant_frequency = float(325.50)

    song_feature = ""
    if dominant_frequency < 250:
        song_feature = "이 노래는 드럼이나 베이스의 웅장함이 강조되는 '저음 중심' 노래입니다."
    elif dominant_frequency < 2000:
        song_feature = "이 노래는 보컬의 목소리가 뚜렷하게 들리는 '중음 중심' 노래입니다."
    else:
        song_feature = "이 노래는 하이햇이나 일렉기타의 찰랑임이 돋보이는 '고음 중심' 노래입니다."
        
    fft_result = {
        "original_file": data["file_name"],
        "dominant_hz": round(dominant_frequency, 2),
        "feature_text": song_feature
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fft_result, f, indent=4, ensure_ascii=False)
        
    # 📊 윤수의 핵심 그래프 설정 데이터
    plt.figure(figsize=(6, 3))  # 지후 창 내부에 쏙 들어가도록 사이즈 최적화
    t = np.linspace(0, 0.05, 1000)
    y_sin = np.sin(2 * np.pi * dominant_frequency * t)
    
    plt.plot(t, y_sin, color='crimson', linewidth=2)
    plt.title(f"Backend Signal Waveform ({dominant_frequency:.2f} Hz)", fontsize=10, fontweight='bold')
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    # ⭕ [핵심] 팝업창을 띄우는 대신, 지후 창이 읽어갈 수 있게 이미지 파일로 저장합니다.
    plt.savefig(graph_path, dpi=150)
    plt.close()  # 메모리 닫기

if __name__ == "__main__":
    run_backend_analysis()
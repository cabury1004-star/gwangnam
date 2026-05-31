import json
import os
import numpy as np
import matplotlib.pyplot as plt

def run_backend_analysis():
    input_path = "waveform_data.json"
    output_path = "fft_result.json"
    
    if not os.path.exists(input_path):
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    frequency_data = np.array(data["frequency_data"])
    sample_rate = data["sample_rate"]
    
    # FFT 분석 및 피크 주파수 도출
    peak_index = np.argmax(frequency_data)
    dominant_frequency = float(peak_index * sample_rate / (len(frequency_data) * 2))
    
    song_feature = ""
    if dominant_frequency < 250:
        song_feature = "이 노래는 드럼이나 베이스 웅장함이 강조되는 '저음 중심' 노래입니다."
    elif dominant_frequency < 2000:
        song_feature = "이 노래는 보컬의 목소리가 뚜렷하게 들리는 '중음 중심' 노래입니다."
    else:
        song_feature = "이 노래는 하이햇이나 일렉기타의 찰랑임이 돋보이는 '고음 중심' 노래입니다."
        
    fft_result = {
        "original_file": data["file_name"],
        "dominant_hz": round(dominant_frequency, 2),
        "feature_text": song_feature
    }
    
    # 📂 2. 두 번째 파일 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fft_result, f, indent=4, ensure_ascii=False)
        
    # 📊 윤수의 3번 핵심 요구사항: 백엔드 그래프 띄우기
    plt.figure(figsize=(9, 3.5))
    t = np.linspace(0, 0.05, 1000)
    y_sin = np.sin(2 * np.pi * dominant_frequency * t)
    
    plt.plot(t, y_sin, color='crimson', linewidth=2)
    plt.title(f"윤수 2번 결과: 백엔드 추출 사인파 ({dominant_frequency:.2f} Hz)", fontproperties="Malgun Gothic", fontsize=11, fontweight='bold')
    plt.xlabel("시간 (Seconds)", fontproperties="Malgun Gothic")
    plt.ylabel("진폭 (Amplitude)", fontproperties="Malgun Gothic")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    print("📢 윤수의 그래프 창을 닫으면 지후2 결과창으로 넘어갑니다.")
    plt.show() # 이 그래프 창을 X 버튼 눌러서 닫으면 이 스크립트가 완전히 종료되면서 app.py가 다음으로 넘어갑니다!

if __name__ == "__main__":
    run_backend_analysis()
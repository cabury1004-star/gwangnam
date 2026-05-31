import json
import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def run_backend_analysis():
    # ⭕ [제출용 최종 경로 보정] 윤수 코드도 실제 app.exe가 작동하는 진짜 폴더 위치를 찾습니다.
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # 언제나 메인 프로그램과 같은 물리 폴더 내의 json 파일들을 바라보도록 강제 고정
    input_path = os.path.join(base_dir, "waveform_data.json")
    output_path = os.path.join(base_dir, "fft_result.json")
    
    if not os.path.exists(input_path):
        print("분석할 waveform_data.json 파일이 존재하지 않습니다.")
        return

    # 지후1이 만들어놓은 데이터 읽기
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    frequency_data = np.array(data["frequency_data"])
    sample_rate = data["sample_rate"]
    
    # FFT 분석 및 피크 주파수 도출
    peak_index = np.argmax(frequency_data)
    dominant_frequency = float(peak_index * sample_rate / (len(frequency_data) * 2))
    
    # 대표 주파수 대역별 텍스트 매칭
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
    
    # 📂 지후2 창이 읽을 수 있도록 결과 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fft_result, f, indent=4, ensure_ascii=False)
        
    # 📊 윤수의 핵심 그래프 설정 데이터 (내부 연산용)
    plt.figure(figsize=(9, 3.5))
    t = np.linspace(0, 0.05, 1000)
    y_sin = np.sin(2 * np.pi * dominant_frequency * t)
    
    plt.plot(t, y_sin, color='crimson', linewidth=2)
    plt.title(f"윤수 결과: 백엔드 추출 사인파 ({dominant_frequency:.2f} Hz)", fontproperties="Malgun Gothic", fontsize=11, fontweight='bold')
    plt.xlabel("시간 (Seconds)", fontproperties="Malgun Gothic")
    plt.ylabel("진폭 (Amplitude)", fontproperties="Malgun Gothic")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    # 🚫 중간 팝업창을 생략하고 지후2 창으로 바로 매끄럽게 넘어가기 위해 창 띄우기(show)는 숨깁니다.
    # plt.show() 

if __name__ == "__main__":
    run_backend_analysis()
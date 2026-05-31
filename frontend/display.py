import tkinter as tk
from tkinter import messagebox
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_final_result():
    input_path = "fft_result.json"
    
    if not os.path.exists(input_path):
        messagebox.showerror("에러", "최종 결과 파일이 없습니다.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        result_data = json.load(f)
        
    file_name = result_data["original_file"]
    dominant_hz = result_data["dominant_hz"]
    feature_text = result_data["feature_text"]

    # UI 및 윤수의 그래프를 동시에 표현할 메인 창 설정
    root = tk.Tk()
    root.title("지후2: 최종 FFT 분석 결과")
    root.geometry("550x550")
    root.config(bg="#f9fafe")
    root.resizable(False, False)
    
    tk.Label(root, text="🎵 최종 FFT 분석 리포트 🎵", font=("맑은 고딕", 14, "bold"), bg="#f9fafe", fg="#4A90E2").pack(pady=15)
    tk.Label(root, text=f"분석 음원: {file_name}", font=("맑은 고딕", 10, "bold"), bg="#f9fafe", fg="#555555").pack()
    
    # Hz 수치 표현
    hz_frame = tk.Frame(root, bg="#eef2f9", padx=15, pady=8)
    hz_frame.pack(pady=10)
    tk.Label(hz_frame, text="가장 주된 주파수 (Dominant Frequency)", font=("맑은 고딕", 9), bg="#eef2f9", fg="#666666").pack()
    tk.Label(hz_frame, text=f"✨ {dominant_hz} Hz ✨", font=("맑은 고딕", 16, "bold"), bg="#eef2f9", fg="#D0021B").pack()
    
    # 특징 텍스트 표현
    feature_frame = tk.Frame(root, bg="#ffffff", highlightbackground="#dddddd", highlightthickness=1, padx=20, pady=10)
    feature_frame.pack(pady=5, fill="x", padx=40)
    tk.Label(feature_frame, text="💡 음악적 특징 분석 결과", font=("맑은 고딕", 9, "bold"), bg="#ffffff", fg="#888888").pack(anchor="w")
    tk.Label(feature_frame, text=feature_text, font=("맑은 고딕", 10), bg="#ffffff", fg="#333333", wraplength=450, justify="center").pack(pady=5)
    
    # 📊 [지후2 핵심] 윤수 백엔드에서 받아온 주파수 기반 그래프를 창 내부에 그리기
    fig, ax = plt.subplots(figsize=(5, 2.2))
    t = np.linspace(0, 0.05, 1000)
    y_sin = np.sin(2 * np.pi * dominant_hz * t)
    
    ax.plot(t, y_sin, color='crimson', linewidth=2) # 윤수의 상징 빨간색 그래프
    ax.set_title(f"백엔드 연산 기반 대표 사인파 ({dominant_hz} Hz)", fontproperties="Malgun Gothic", fontsize=10, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.6)
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=15, fill="both", expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    show_final_result()
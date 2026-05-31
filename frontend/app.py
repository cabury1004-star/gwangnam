import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import subprocess # 다른 파이썬 파일을 강제로 실행시키는 도구

def process_audio(file_path, file_name):
    try:
        print(f"\n📥 [지후1] 파일 입력 성공 -> {file_name}")
        y, sr = librosa.load(file_path, sr=None)
        
        # 주파수 데이터 추출 및 수식화
        stft_result = np.abs(librosa.stft(y))
        stft_db = librosa.amplitude_to_db(stft_result, ref=np.max)
        frequency_energy = np.mean(stft_db, axis=1).tolist()
        
        transfer_data = {
            "file_name": file_name,
            "sample_rate": sr,
            "frequency_data": frequency_energy
        }
        
        # 📂 1. 첫 번째 파일 저장
        output_path = "waveform_data.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transfer_data, f, indent=4)
        print(f"💾 [지후1 완료] 수식화 파일 저장 성공!")
        
        # ----------------------------------------------------
        # 🔥 [핵심] 여기서 윤수 백엔드 프로그램을 자동으로 실행시킵니다!
        # ----------------------------------------------------
        print("\n🚀 [자동 릴레이 1단계] 윤수의 백엔드 프로그램(analysis.py)을 실행합니다...")
        
        # backend/analysis.py를 실행하고 끝날 때까지 기다림
        backend_script = os.path.join("backend", "analysis.py")
        subprocess.run(["py", backend_script], check=True)
        
        # ----------------------------------------------------
        # 🔥 [핵심] 윤수 프로그램이 끝나면 지후2 프로그램을 자동으로 실행시킵니다!
        # ----------------------------------------------------
        print("\n🚀 [자동 릴레이 2단계] 지후2의 최종 결과창(display.py)을 실행합니다...")
        
        display_script = os.path.join("frontend", "display.py")
        subprocess.Popen(["py", display_script]) # 얘는 창을 띄우고 지후1은 종료하기 위해 Popen 사용
        
        # 작업이 다 끝났으니 메인 프로그램 종료
        root.destroy()
        
    except Exception as e:
        messagebox.showerror("오류", f"처리 중 에러 발생:\n{e}")

def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="1번: 오디오 파일(.wav) 선택",
        filetypes=[("WAV Audio Files", "*.wav")]
    )
    if file_path:
        file_name = file_path.split("/")[-1]
        label_status.config(text=f"선택된 파일: {file_name}", fg="green")
        process_audio(file_path, file_name)

# UI 설정
root = tk.Tk()
root.title("gwangnam 프로젝트 - 마스터 입력창")
root.geometry("450x230")
root.resizable(False, False)
root.config(bg="#f5f6f8")

tk.Label(root, text="광남 FFT 시스템 - 지후1", font=("맑은 고딕", 16, "bold"), bg="#f5f6f8", fg="#333333", pady=15).pack()
tk.Label(root, text="파일을 넣으면 윤수 ➡️ 지후2 프로그램이 자동 연쇄 실행됩니다.", font=("맑은 고딕", 9), bg="#f5f6f8", fg="#666666").pack()

btn_open = tk.Button(root, text="📁 오디오 파일(.wav) 입력하기", command=open_file_dialog, font=("맑은 고딕", 11, "bold"), bg="#4A90E2", fg="white", padx=20, pady=10, cursor="hand2")
btn_open.pack(pady=15)

label_status = tk.Label(root, text="현재 입력된 파일이 없습니다.", font=("맑은 고딕", 10, "italic"), bg="#f5f6f8", fg="#999999")
label_status.pack()

root.mainloop()
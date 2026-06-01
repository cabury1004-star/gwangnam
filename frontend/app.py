import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageTk  # ⭕ 안전한 png 로딩을 위해 다시 포함 (윤수 컴엔 pillow가 빌드 시 같이 묶일 겁니다)

def run_frontend_app():
    root = tk.Tk()
    root.title("지후 마스터 창 (통합 실행기)")
    root.geometry("500x200")

    def select_file():
        file_path = filedialog.askopenfilename(
            title="노래 파일(.wav)을 선택하세요",
            filetypes=[("WAV files", "*.wav")]
        )
        
        if not file_path:
            return

        print(f"\n📥 [지후1] 파일 입력 성공 -> {os.path.basename(file_path)}")
        
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        waveform_json_path = os.path.join(base_dir, "waveform_data.json")

        # 기존 결과 파일들 청소
        for target_file in ["graph.png", "fft_result.json"]:
            t_path = os.path.join(base_dir, target_file)
            if os.path.exists(t_path):
                try: os.remove(t_path)
                except: pass

        try:
            sample_rate, audio_data = wavfile.read(file_path)
            if len(audio_data.shape) > 1:
                audio_data = audio_data[:, 0]
            
            fft_segments = np.abs(np.fft.fft(audio_data[:44100]))
            real_frequency_data = [float(x) for x in fft_segments[:len(fft_segments)//2]]

        except Exception as e:
            messagebox.showerror("파일 읽기 실패", f"선택한 WAV 파일을 읽을 수 없습니다.\n오류 내용: {str(e)}")
            return

        mock_waveform_data = {
            "file_name": os.path.basename(file_path),
            "sample_rate": int(sample_rate),
            "frequency_data": real_frequency_data  
        }

        with open(waveform_json_path, "w", encoding="utf-8") as f:
            json.dump(mock_waveform_data, f, indent=4, ensure_ascii=False)
        print("💾 [지후1 완료] 진짜 주파수 데이터 수식화 성공!")

        print("\n🚀 [자동 릴레이 1단계] 윤수의 백엔드 프로그램(analysis.py)을 실행합니다...")
        
        analysis_exe_path = os.path.join(base_dir, "analysis.exe")

        try:
            if os.path.exists(analysis_exe_path):
                subprocess.run([analysis_exe_path], check=True)
            else:
                backend_script = os.path.join(base_dir, "..", "backend", "analysis.py")
                if not os.path.exists(backend_script):
                    backend_script = os.path.join(base_dir, "backend", "analysis.py")
                subprocess.run(["py", backend_script], check=True)
            
            print("✨ [릴레이 완료] 윤수 분석 종료. 지후2 창으로 바통 터치!")
            show_result_window(base_dir)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("오류", f"처리 중 에러 발생:\nCommand {e.cmd} returned non-zero exit status {e.returncode}.")

    label = tk.Label(root, text="노래 분석 마스터 프로그램", font=("Malgun Gothic", 14, "bold"))
    label.pack(pady=20)

    btn = tk.Button(root, text="노래 파일 선택 (.wav)", command=select_file, bg="royalblue", fg="white", font=("Malgun Gothic", 11, "bold"), padx=10, pady=5)
    btn.pack(pady=10)

    root.mainloop()

def show_result_window(base_dir):
    result_json_path = os.path.join(base_dir, "fft_result.json")
    graph_img_path = os.path.join(base_dir, "graph.png")  # .png로 변경
    
    if not os.path.exists(result_json_path):
        messagebox.showerror("오류", "윤수의 분석 결과 파일(fft_result.json)을 찾을 수 없습니다.")
        return

    with open(result_json_path, "r", encoding="utf-8") as f:
        result_data = json.load(f)

    res_window = tk.Toplevel()
    res_window.title("지후2 - 최종 분석 리포트")
    res_window.geometry("600x580")  
    res_window.attributes("-topmost", True)

    tk.Label(res_window, text="🎵 오디오 주파수 분석 최종 리포트 🎵", font=("Malgun Gothic", 14, "bold"), fg="darkgreen").pack(pady=10)
    
    info_text = f"분석 파일: {result_data.get('original_file', '알 수 없음')}\n" \
                f"대표 피크 주파수: {result_data.get('dominant_hz', 0)} Hz\n" \
                f"📋 음악 특징: {result_data.get('feature_text', '특징 없음')}"

    tk.Label(res_window, text=info_text, font=("Malgun Gothic", 11), justify="left", wraplength=550).pack(pady=10, padx=20)
    
    # ⭕ Pillow 라이브러리를 이용하여 PNG 이미지를 안전하게 로딩하고 크기를 맞춰 배치
    if os.path.exists(graph_img_path):
        try:
            img = Image.open(graph_img_path)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(res_window, image=photo)
            img_label.image = photo  
            img_label.pack(pady=5)
        except Exception as e:
            tk.Label(res_window, text=f"[그래프 로딩 실패]: {str(e)}", fg="red").pack()

    tk.Button(res_window, text="확인 완료", command=res_window.destroy, width=15, font=("Malgun Gothic", 10), bg="lightgray").pack(pady=15)

if __name__ == "__main__":
    run_frontend_app()
import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def run_frontend_app():
    # 메인 윈도우 생성
    root = tk.Tk()
    root.title("지후 마스터 창 (통합 실행기)")
    root.geometry("500x200")

    def select_file():
        # 파일 선택 창 열기
        file_path = filedialog.askopenfilename(
            title="노래 파일(.wav)을 선택하세요",
            filetypes=[("WAV files", "*.wav")]
        )
        
        if not file_path:
            return

        print(f"\n📥 [지후1] 파일 입력 성공 -> {os.path.basename(file_path)}")
        
        # ⭕ [제출용 최종 경로 보정] 실행 파일(.exe)의 실제 위치를 계산합니다.
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # 데이터를 주고받을 json 파일 경로 설정
        waveform_json_path = os.path.join(base_dir, "waveform_data.json")

        # 임시로 파형 데이터 수식화 파일 생성 (지후1의 역할)
        mock_waveform_data = {
            "file_name": os.path.basename(file_path),
            "sample_rate": 44100,
            "frequency_data": [100, 200, 300, 1500, 300, 200, 100]  # 가상의 주파수 데이터
        }

        with open(waveform_json_path, "w", encoding="utf-8") as f:
            json.dump(mock_waveform_data, f, indent=4, ensure_ascii=False)
        print("💾 [지후1 완료] 수식화 파일 저장 성공!")

        print("\n🚀 [자동 릴레이 1단계] 윤수의 백엔드 프로그램(analysis.py)을 실행합니다...")
        
        # 같은 폴더에 빌드된 analysis.exe가 있는지 확인
        analysis_exe_path = os.path.join(base_dir, "analysis.exe")

        try:
            if os.path.exists(analysis_exe_path):
                # 1️⃣ (.exe 제출 버전) 폴더 내의 analysis.exe를 다이렉트로 실행
                subprocess.run([analysis_exe_path], check=True)
            else:
                # 2️⃣ (개발자 테스트 버전) py 명령어로 파이썬 파일 실행
                backend_script = os.path.join(base_dir, "..", "backend", "analysis.py")
                if not os.path.exists(backend_script):
                    # 경로가 꼬였을 때를 대비한 2차 방어선
                    backend_script = os.path.join(base_dir, "backend", "analysis.py")
                subprocess.run(["py", backend_script], check=True)
            
            print("✨ [릴레이 완료] 윤수 분석 종료. 지후2 창으로 바통 터치!")
            
            # 🏁 [자동 릴레이 2단계] 지후2 결과 리포트 창 띄우기
            show_result_window(base_dir)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("오류", f"처리 중 에러 발생:\nCommand {e.cmd} returned non-zero exit status {e.returncode}.")

    # 화면 UI 구성
    label = tk.Label(root, text="노래 분석 마스터 프로그램", font=("Malgun Gothic", 14, "bold"))
    label.pack(pady=20)

    btn = tk.Button(root, text="노래 파일 선택 (.wav)", command=select_file, bg="royalblue", fg="white", font=("Malgun Gothic", 11, "bold"), padx=10, pady=5)
    btn.pack(pady=10)

    root.mainloop()

def show_result_window(base_dir):
    # 윤수가 저장한 결과를 읽어와서 보여주는 지후2 결과 창
    result_json_path = os.path.join(base_dir, "fft_result.json")
    
    if not os.path.exists(result_json_path):
        messagebox.showerror("오류", "윤수의 분석 결과 파일(fft_result.json)을 찾을 수 없습니다.")
        return

    with open(result_json_path, "r", encoding="utf-8") as f:
        result_data = json.load(f)

    res_window = tk.Toplevel()
    res_window.title("지후2 - 최종 분석 리포트")
    res_window.geometry("550", "250")

    tk.Label(res_window, text="🎵 오디오 주파수 분석 최종 리포트 🎵", font=("Malgun Gothic", 14, "bold"), fg="darkgreen").pack(pady=15)
    
    info_text = f"분석 파일: {result_data['original_file']}\n" \
                f"대표 피크 주파수: {result_data['dominant_hz']} Hz\n\n" \
                f"📋 음악 특징:\n{result_data['feature_text']}"

    tk.Label(res_window, text=info_text, font=("Malgun Gothic", 11), justify="left", wraplength=500).pack(pady=10)
    tk.Button(res_window, text="확인 완료", command=res_window.destroy, width=15, font=("Malgun Gothic", 10)).pack(pady=15)

if __name__ == "__main__":
    run_frontend_app()
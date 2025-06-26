#!/usr/bin/env python3
"""
Streamlit 앱 실행 스크립트
"""
import subprocess
import sys
import os

def run_streamlit():
    """Streamlit 앱 실행"""
    try:
        # 현재 디렉토리에서 streamlit_app.py 실행
        script_dir = os.path.dirname(os.path.abspath(__file__))
        streamlit_file = os.path.join(script_dir, "streamlit_app.py")
        
        print("🚀 Streamlit 앱을 시작합니다...")
        print(f"📁 실행 파일: {streamlit_file}")
        print("🌐 브라우저에서 http://localhost:8501 로 접속하세요")
        print("⏹️  종료하려면 Ctrl+C를 누르세요")
        print("-" * 50)
        
        # Streamlit 실행
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", streamlit_file,
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Streamlit 앱이 종료되었습니다.")
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    run_streamlit()

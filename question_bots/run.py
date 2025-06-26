"""
Streamlit 앱 실행 스크립트
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Streamlit 앱 실행"""
    
    # 현재 디렉터리 확인
    current_dir = Path(__file__).parent
    app_file = current_dir / "app.py"
    
    if not app_file.exists():
        print("❌ app.py 파일을 찾을 수 없습니다!")
        return
    
    print("🚀 Streamlit 앱을 시작합니다...")
    print(f"📁 위치: {app_file}")
    print()
    print("💡 브라우저가 자동으로 열리지 않으면 다음 주소로 접속하세요:")
    print("   http://localhost:8501")
    print()
    print("⏹️  종료하려면 Ctrl+C를 누르세요")
    print("="*50)
    
    try:
        # Streamlit 실행
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file),
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 앱을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()

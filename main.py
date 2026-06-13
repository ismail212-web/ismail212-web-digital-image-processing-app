#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess

def check_pywebview():
    try:
        import webview
        return True
    except ImportError:
        return False

def run_streamlit_only(port=8501, dev=False):
    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", "app/streamlit_app.py",
                "--server.headless", "true",
                "--server.port", str(port),
                "--server.address", "localhost",
                "--browser.gatherUsageStats", "false",
                "--global.developmentMode=false"]
    if dev:
        sys.argv.append("--server.runOnSave=true")
    stcli.main()

def run_web_mode(port=8501, dev=False):
    print(f"🌐 Menjalankan dalam mode WEB di http://localhost:{port}")
    cmd = [sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py",
           "--server.port", str(port)]
    if dev:
        cmd.extend(["--server.runOnSave", "true"])
    subprocess.run(cmd)

def run_desktop_mode(port=8501):
    if not check_pywebview():
        print("❌ pywebview belum terinstal!")
        print("   Silakan jalankan: pip install pywebview")
        sys.exit(1)
    print("🖥️  Menjalankan dalam mode DESKTOP...")
    from desktop.app import main as desktop_main
    desktop_main(port=port)

def main():
    parser = argparse.ArgumentParser(description="Digital Image Processing Lab")
    parser.add_argument("--web", action="store_true", help="Jalankan sebagai web")
    parser.add_argument("--streamlit-only", action="store_true", help="Internal: hanya jalankan Streamlit")
    parser.add_argument("--port", type=int, default=8501, help="Port server")
    parser.add_argument("--dev", action="store_true", help="Mode developer")
    args = parser.parse_args()
    
    if args.streamlit_only:
        run_streamlit_only(port=args.port, dev=args.dev)
    elif args.web:
        run_web_mode(port=args.port, dev=args.dev)
    else:
        run_desktop_mode(port=args.port)

if __name__ == "__main__":
    main()

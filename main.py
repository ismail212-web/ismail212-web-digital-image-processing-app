#!/usr/bin/env python3
"""
Digital Image Processing Lab - Desktop & Web Entry Point
Usage:
    python main.py              # Jalankan sebagai aplikasi desktop
    python main.py --web        # Jalankan sebagai web (browser)
    python main.py --port 8502  # Gunakan port custom
    python main.py --dev        # Mode developer (auto-reload)
"""
import sys
import os
import argparse
import subprocess

def check_pywebview():
    """Cek apakah pywebview terinstal."""
    try:
        import webview
        return True
    except ImportError:
        return False

def run_web_mode(port=8501, dev=False):
    """Jalankan aplikasi dalam mode web (browser)."""
    print(f"🌐 Menjalankan dalam mode WEB di http://localhost:{port}")
    cmd = [sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py",
           "--server.port", str(port)]
    if dev:
        cmd.extend(["--server.runOnSave", "true"])
    subprocess.run(cmd)

def run_desktop_mode():
    """Jalankan aplikasi dalam mode desktop (jendela native)."""
    if not check_pywebview():
        print("❌ pywebview belum terinstal!")
        print("   Silakan jalankan: pip install pywebview")
        print("   Atau gunakan mode web: python main.py --web")
        sys.exit(1)
    
    print("🖥️  Menjalankan dalam mode DESKTOP...")
    from desktop.app import main as desktop_main
    desktop_main()

def main():
    parser = argparse.ArgumentParser(description="Digital Image Processing Lab")
    parser.add_argument("--web", action="store_true", help="Jalankan sebagai web (browser)")
    parser.add_argument("--port", type=int, default=8501, help="Port server (default: 8501)")
    parser.add_argument("--dev", action="store_true", help="Mode developer (auto-reload)")
    
    args = parser.parse_args()
    
    if args.web:
        run_web_mode(port=args.port, dev=args.dev)
    else:
        run_desktop_mode()

if __name__ == "__main__":
    main()

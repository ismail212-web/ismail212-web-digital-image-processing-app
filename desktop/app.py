import sys, os, json

try:
    import webview
except ImportError:
    print("❌ pywebview belum diinstal. Jalankan: pip install pywebview")
    sys.exit(1)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from desktop.logger import setup_logger
from desktop.launcher import StreamlitLauncher

def load_config():
    config_path = os.path.join(project_root, "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "window": {"title": "DIP Lab", "width": 1280, "height": 800, "resizable": True, "fullscreen": False},
            "streamlit": {"port": 8501, "host": "localhost"},
            "paths": {"streamlit_app": "app/streamlit_app.py"},
            "features": {"enable_devtools": False}
        }

def main():
    logger = setup_logger()
    logger.info("Aplikasi Desktop DIP Lab dimulai.")
    config = load_config()
    win_cfg = config.get("window", {})
    st_cfg = config.get("streamlit", {})
    path_cfg = config.get("paths", {})

    launcher = StreamlitLauncher(
        port=st_cfg.get("port", 8501),
        host=st_cfg.get("host", "localhost"),
        app_path=path_cfg.get("streamlit_app", "app/streamlit_app.py")
    )

    try:
        launcher.start()
    except Exception as e:
        logger.error(f"Gagal memulai Streamlit: {e}")
        sys.exit(1)

    window = webview.create_window(
        title=win_cfg.get("title", "Digital Image Processing Lab"),
        url=launcher.url,
        width=win_cfg.get("width", 1280),
        height=win_cfg.get("height", 800),
        resizable=win_cfg.get("resizable", True),
        fullscreen=win_cfg.get("fullscreen", False)
    )

    def on_closed():
        logger.info("Jendela ditutup. Menghentikan server...")
        launcher.stop()
        logger.info("Aplikasi berakhir.")

    window.events.closed += on_closed
    webview.start(debug=config.get("features", {}).get("enable_devtools", False))

if __name__ == "__main__":
    main()

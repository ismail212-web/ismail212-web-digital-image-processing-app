import subprocess, sys, time, urllib.request, urllib.error, os

class StreamlitLauncher:
    def __init__(self, port=8501, host="localhost", app_path="app/streamlit_app.py"):
        self.port = port
        self.host = host
        self.app_path = app_path
        self.process = None
        self.url = f"http://{host}:{port}"

    def start(self):
        print(f"🚀 Memulai server Streamlit di {self.url}...")
        cmd = [sys.executable, "-m", "streamlit", "run", self.app_path,
               "--server.headless", "true", "--server.port", str(self.port),
               "--server.address", self.host, "--browser.gatherUsageStats", "false"]
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL, cwd=os.getcwd())
        self._wait_for_server()

    def _wait_for_server(self, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if urllib.request.urlopen(self.url, timeout=2).getcode() == 200:
                    print("✅ Server Streamlit siap!")
                    return
            except urllib.error.URLError:
                pass
            time.sleep(0.5)
        raise RuntimeError("⏱️ Timeout: Gagal memulai server Streamlit.")

    def stop(self):
        if self.process:
            print("🛑 Menghentikan server Streamlit...")
            self.process.terminate()
            self.process.wait()
            print("✅ Server Streamlit dihentikan.")

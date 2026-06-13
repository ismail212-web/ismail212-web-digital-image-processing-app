#!/usr/bin/env python3
"""
Build script untuk Digital Image Processing Lab Desktop
Usage:
    python build.py build-app     # Build untuk macOS (.app)
    python build.py build-exe     # Build untuk Windows (.exe)
    python build.py clean         # Bersihkan folder build
"""
import sys
import os
import subprocess
import shutil

def clean_build():
    """Bersihkan folder build dan dist."""
    print("🧹 Membersihkan folder build...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   ✅ {folder}/ dihapus")
    for ext in [".spec"]:
        for f in os.listdir("."):
            if f.endswith(ext):
                os.remove(f)
                print(f"   ✅ {f} dihapus")
    print("✅ Pembersihan selesai!")

def build_app():
    """Build aplikasi desktop menggunakan PyInstaller."""
    print("�� Memulai build aplikasi desktop...")
    
    # Module yang TIDAK dibutuhkan (exclude untuk mempercepat build)
    excludes = [
        "tensorflow", "torch", "keras", "theano",
        "scipy", "pandas", "seaborn", "plotly",
        "sklearn", "scikit-learn", "xgboost", "lightgbm",
        "notebook", "jupyter", "ipython", "IPython",
        "sphinx", "pytest", "setuptools", "pip",
        "matplotlib.backends.backend_qt5agg",
        "matplotlib.backends.backend_qt4agg",
        "matplotlib.backends.backend_gtk3agg",
        "matplotlib.backends.backend_tkagg",
    ]
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "DIPLab",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--log-level", "WARN",
        "--add-data", "app:app",
        "--add-data", "src:src",
        "--add-data", "modules:modules",
        "--add-data", "utils:utils",
        "--add-data", "data:data",
        "--add-data", "assets:assets",
        "--add-data", "config.json:.",
        "--hidden-import", "webview",
        "--hidden-import", "cv2",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "reportlab",
        "--hidden-import", "streamlit",
        "--collect-all", "streamlit",
    ]
    
    # Tambahkan exclude modules
    for module in excludes:
        cmd.extend(["--exclude-module", module])
    
    cmd.append("main.py")
    
    print("   Menjalankan PyInstaller (dengan exclude module)...")
    print(f"   Mengexclude: {len(excludes)} module yang tidak dipakai")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ BUILD BERHASIL!")
        if sys.platform == "darwin":
            print(f"   📦 Aplikasi macOS: dist/DIPLab.app")
            print(f"   🚀 Jalankan dengan: open dist/DIPLab.app")
        elif sys.platform == "win32":
            print(f"   📦 Aplikasi Windows: dist/DIPLab.exe")
        else:
            print(f"   📦 Aplikasi Linux: dist/DIPLab")
    else:
        print("\n❌ BUILD GAGAL!")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python build.py build-app     # Build aplikasi desktop")
        print("  python build.py clean         # Bersihkan folder build")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "clean":
        clean_build()
    elif command in ["build-app", "build-exe", "build"]:
        build_app()
    else:
        print(f"❌ Perintah tidak dikenal: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

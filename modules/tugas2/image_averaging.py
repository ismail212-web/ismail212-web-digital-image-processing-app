# modules/tugas2/image_averaging.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path

def run():
    st.markdown("### ➕ Arithmetic Operation: Image Averaging")

    base = Path(__file__).resolve().parents[2] / "assets"
    fig_path = base / "image_averaging_figure.png"
    default_clean = base / "galaxy_ngc3314.png"

    # --- Tampilkan materi buku ---
    if fig_path.exists():
        st.image(str(fig_path), use_container_width=True)

    with st.expander("📘 Penjelasan Proses & Kegunaan", expanded=True):
        st.markdown("""
**Proses yang dilakukan:**
1. Ambil gambar yang sama sebanyak K kali (dalam buku: K = 8, 16, 64, 128)
2. Setiap pengambilan ditambah *additive Gaussian noise* (mean=0, σ=64)
3. Jumlahkan semua gambar, lalu bagi dengan K: `g_avg = (1/K) * Σ g_i`

**Kenapa noise hilang?**
- Noise bersifat acak (+ dan -), kalau dirata-rata → mendekati 0
- Sinyal asli (galaksi) tetap sama di setiap frame → tetap terlihat

**Kegunaan nyata:**
- **Astronomi:** foto galaksi NGC 3314 dari NASA (seperti di buku)
- **Medis:** X-ray low-dose, MRI
- **Satelit:** citra malam hari
- **Kamera HP:** Night mode (ambil 10 foto lalu di-average)

Rumus buku: noise berkurang sebesar √K. K=128 → noise turun ~11x.
        """)

    st.divider()

    # --- Upload ---
    up = st.file_uploader(
        "Upload gambar bersih (a) — support PNG, JPG, TIF",
        type=["png","jpg","jpeg","tif","tiff","bmp"]
    )

    if up:
        clean = cv2.imdecode(np.frombuffer(up.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    elif default_clean.is_file():
        clean = cv2.imread(str(default_clean), cv2.IMREAD_GRAYSCALE)
    else:
        st.warning("Upload gambar (a) dulu")
        return

    clean = cv2.resize(clean, (300, 300))

    # --- Simulasi ---
    def noisy(img, sigma=64):
        n = np.random.normal(0, sigma, img.shape).astype(np.float32)
        return np.clip(img.astype(np.float32) + n, 0, 255).astype(np.uint8)

    b = noisy(clean)
    Ks = [8, 16, 64, 128]
    results = []
    for K in Ks:
        acc = np.zeros_like(clean, dtype=np.float32)
        for _ in range(K):
            acc += noisy(clean)
        results.append((acc / K).astype(np.uint8))

    # --- Tampilan 1 layar ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(clean, caption="(a) Original", width=180)
        st.image(results[0], caption="(c) K=8", width=180)
    with c2:
        st.image(b, caption="(b) Noisy σ=64", width=180)
        st.image(results[1], caption="(d) K=16", width=180)
    with c3:
        st.image(results[2], caption="(e) K=64", width=180)
        st.image(results[3], caption="(f) K=128", width=180)
# modules/tugas2/smoothing_hubble.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path


def run():
    st.markdown(
        "### 🌌 Materi 2 — Sub-Modul 7b: Smoothing + Thresholding (FIGURE 3.36)"
    )

    # --- path assets ---
    here = Path(__file__).resolve()
    base = here.parents[2] / "assets"
    if not base.exists():
        base = here.parents[1] / "assets"

    fig_path = base / "smoothing_linear_filter_cont_figure.png"
    default_hubble = base / "hubble_original.png"  # opsional, kalau kamu punya

    # --- tampilkan gambar buku ---
    if fig_path.exists():
        st.image(
            str(fig_path),
            caption="FIGURE 3.36 — Hubble smoothing & thresholding",
            use_container_width=True,
        )
    else:
        st.warning("Letakkan smoothing_linear_filter_cont_figure.png di assets/")

    with st.expander("📘 Proses FIGURE 3.36", expanded=True):
        st.markdown("""
**(a) → (b) → (c)**
1. **(a) Original** Hubble: banyak bintang kecil + noise
2. **(b) Smoothing 15×15** averaging mask → bintang kecil hilang, yang besar jadi blur
3. **(c) Thresholding** (b) → ambil objek terang saja, jadi mask putih

**Kegunaan nyata:** deteksi objek besar di astronomi, hilangkan bintang kecil sebelum counting galaxies.
        """)

    st.divider()

    # --- upload ---
    up = st.file_uploader(
        "Upload gambar Hubble (atau pakai default)",
        type=["png", "jpg", "jpeg", "tif"],
        key="hubble_up",
    )

    if up:
        img = cv2.imdecode(np.frombuffer(up.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    elif default_hubble.exists():
        img = cv2.imread(str(default_hubble), cv2.IMREAD_GRAYSCALE)
    else:
        # pakai placeholder hitam dengan titik-titik kalau belum ada
        st.info("Upload gambar (a) dulu — contohnya gambar Hubble")
        return

    img = cv2.resize(img, (400, 400))

    # --- kontrol ---
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        ksize = st.slider("Ukuran kernel averaging (b)", 3, 31, 15, step=2)
    with col_s2:
        thresh = st.slider("Threshold untuk (c)", 0, 255, 80)

    # --- proses (b) ---
    blur = cv2.blur(img, (ksize, ksize))

    # --- proses (c) ---
    _, binary = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)

    # --- tampil 1 layar 3 kolom ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(img, caption="(a) Original", use_container_width=True)
    with c2:
        st.image(
            blur, caption=f"(b) Averaging {ksize}×{ksize}", use_container_width=True
        )
    with c3:
        st.image(binary, caption=f"(c) Threshold={thresh}", use_container_width=True)

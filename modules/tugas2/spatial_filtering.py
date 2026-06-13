# modules/tugas2/spatial_filtering.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path


def show_image_centered(img, caption=""):
    st.image(img, caption=caption, width="stretch")


def run():
    st.markdown("### 🎨 Materi 2 — Sub-Modul 7: Spatial Filtering (Smoothing)")

    # --- cari assets dengan 2 kemungkinan lokasi ---
    here = Path(__file__).resolve()
    base1 = here.parents[2] / "assets"  # project/assets
    base2 = here.parents[1] / "assets"  # modules/assets
    base = base1 if (base1 / "smoothing_moving_average_figure.png").exists() else base2

    fig_path = base / "smoothing_moving_average_figure.png"
    default_img = base / "smoothing_test_pattern.png"

    # DEBUG - hapus setelah muncul
    st.caption(f"DEBUG path: {fig_path} | exists: {fig_path.exists()}")

    # --- tampilkan materi buku ---
    if fig_path.exists():
        st.image(
            str(fig_path),
            caption="FIGURE 3.35 — Smoothing Linear Filter",
            width="stretch",
        )
    else:
        st.warning(
            "⚠️ File smoothing_moving_average_figure.png tidak ditemukan di assets/"
        )

    with st.expander("📘 Proses yang dilakukan (FIGURE 3.35)", expanded=True):
        st.markdown("""
**Smoothing Linear Filter: Moving Average (Box Filter)**
1. Kernel kotak n×n (semua nilai = 1/n²) digeser ke seluruh gambar
2. Piksel tengah = rata-rata tetangganya
3. Buku pakai n = 3, 5, 9, 15, 35

**Efek:** n kecil = detail tajam, n besar = blur total, objek kecil hilang
**Kegunaan:** pre-processing OCR, hilangkan noise, simulasi defocus.
        """)

    st.divider()

    uploaded = st.file_uploader(
        "Upload Gambar (atau pakai default):",
        type=["jpg", "jpeg", "png", "tif", "tiff"],
        key="sf_up",
    )

    if uploaded:
        img_bgr = cv2.imdecode(
            np.frombuffer(uploaded.read(), np.uint8), cv2.IMREAD_COLOR
        )
    elif default_img.is_file():
        img_bgr = cv2.imread(str(default_img))
    else:
        st.info("⬆ Upload gambar dulu")
        return

    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.resize(img_gray, (400, 400))

    mode = st.selectbox(
        "Pilih Filter:",
        [
            "Moving Average (Box) - FIGURE 3.35",
            "Gaussian Blur",
            "Median Filter",
            "Laplacian",
            "Unsharp Masking",
        ],
    )

    ksize = (
        st.select_slider("Ukuran Kernel n:", [3, 5, 9, 15, 35], value=9)
        if "Moving" in mode
        else st.select_slider("Kernel:", [3, 5, 7, 9, 11], value=5)
    )

    if "Moving" in mode:
        result = cv2.blur(img_gray, (ksize, ksize))
    elif "Gaussian" in mode:
        result = cv2.GaussianBlur(img_gray, (ksize, ksize), 0)
    elif "Median" in mode:
        result = cv2.medianBlur(img_gray, ksize)
    elif "Laplacian" in mode:
        lap = cv2.Laplacian(img_gray, cv2.CV_64F, ksize=3)
        result = np.clip(img_gray - lap, 0, 255).astype(np.uint8)
    else:
        blur = cv2.GaussianBlur(img_gray, (ksize, ksize), 0)
        result = np.clip(img_gray * 1.5 - blur * 0.5, 0, 255).astype(np.uint8)

    c1, c2 = st.columns(2)
    with c1:
        show_image_centered(img_gray, "Citra Asli (a)")
    with c2:
        show_image_centered(result, f"Hasil: {mode} (n={ksize})")

    if "Moving" in mode and st.checkbox(
        "Tampilkan semua n seperti buku (3,5,9,15,35)", True
    ):
        cols = st.columns(5)
        for i, n in enumerate([3, 5, 9, 15, 35]):
            with cols[i]:
                st.image(
                    cv2.blur(img_gray, (n, n)), caption=f"n={n}", width=120
                )  # <-- typo sudah dibetulkan

# modules/tugas2/sobel_gradient.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path


def show_centered(img, caption="", width=300):
    st.markdown(
        '<div style="display:flex;justify-content:center">', unsafe_allow_html=True
    )
    st.image(img, caption=caption, width=width, clamp=True)
    st.markdown("</div>", unsafe_allow_html=True)


def run():
    st.markdown(
        "### 🎨 Materi 2 — Sub-Modul 11: Sobel Gradient (First Order Derivative)"
    )
    st.markdown("---")

    # --- GAMBAR CONTOH DARI PDF ---
    st.markdown("#### 📘 Contoh Buku (Gonzalez hal 16-17)")

    here = Path(__file__).resolve()
    base = here.parents[2] / "assets"
    if not base.exists():
        base = here.parents[1] / "assets"

    kernel_path = base / "sobel_kernels.png"
    gradient_path = base / "sobel_gradient.png"

    col_a, col_b = st.columns(2)
    with col_a:
        if kernel_path.exists():
            st.image(
                str(kernel_path),
                caption="Sobel operators untuk ∂P/∂x dan ∂P/∂y",
                width="stretch",
            )
    with col_b:
        if gradient_path.exists():
            st.image(
                str(gradient_path),
                caption="Hasil: P, ∂y, ∂x, |∇P|",
                width="stretch",
            )

    with st.expander("📖 Penjelasan"):
        st.markdown("""
        - **Kernel kiri** (-1,0,1) menghitung turunan horizontal **∂P/∂x**
        - **Kernel kanan** (-1,-2,-1) menghitung turunan vertikal **∂P/∂y**
        - **|∇P| = sqrt( (∂x)² + (∂y)² )** = magnitude gradient (tepi putih di background hitam)
        - Gambar beras ini adalah contoh resmi dari PDF Tugas 2 halaman 16-17
        """)

    st.markdown("---")
    st.markdown("#### 💻 Coba Sendiri")

    uploaded = st.file_uploader(
        "Upload gambar (disarankan grayscale):",
        type=["jpg", "jpeg", "png", "tif", "bmp"],
        key="sobel_up",
    )
    if not uploaded:
        st.info("⬆️ Upload gambar beras atau objek dengan tepi jelas")
        return

    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    # Hitung Sobel
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    # Normalisasi untuk display
    sobel_x_disp = cv2.convertScaleAbs(sobel_x)
    sobel_y_disp = cv2.convertScaleAbs(sobel_y)

    magnitude = cv2.magnitude(sobel_x, sobel_y)
    magnitude_disp = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(
        np.uint8
    )

    # Tampilkan 2x2 grid seperti di buku
    c1, c2 = st.columns(2)
    with c1:
        show_centered(img, "P (Asli)", 280)
        show_centered(sobel_x_disp, "∂P/∂x", 280)
    with c2:
        show_centered(sobel_y_disp, "∂P/∂y", 280)
        show_centered(magnitude_disp, "|∇P| (Magnitude)", 280)

    st.markdown("---")
    with st.expander("⚙️ Parameter"):
        ksize = st.select_slider("Ukuran kernel Sobel:", [1, 3, 5, 7], value=3)
        if ksize != 3:
            sx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
            sy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
            mag = cv2.normalize(
                cv2.magnitude(sx, sy), None, 0, 255, cv2.NORM_MINMAX
            ).astype(np.uint8)
            show_centered(mag, f"|∇P| dengan ksize={ksize}", 350)

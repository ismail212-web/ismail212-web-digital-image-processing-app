# modules/tugas1/image_viewer.py
import streamlit as st
import cv2
import numpy as np
from utils.image_utils import show_image_centered


def run():
    st.markdown("### 📷 Materi 1 — Sub-Modul 1: Image Viewer & Operasi Dasar Piksel")
    st.markdown("""
    Eksperimen ini memvisualisasikan struktur internal citra digital:
    representasi array piksel, distribusi histogram, dan konversi RGB ↔ Grayscale.
    """)

    # --- GAMBAR CONTOH ---
    st.markdown(
        "**1. Modul untuk membuka dan menampilkan image berwarna. Dilengkapi dengan menu untuk mengubah tampilan image berwarna menjadi grayscale.**"
    )

    col_ex1, col_ex2 = st.columns([2, 1])
    with col_ex1:
        st.image(
            "assets/soal1_grayscale_ramp.jpg",
            caption="Contoh: Grayscale ramp (10 level keabuan)",
            width="stretch",
        )
    with col_ex2:
        st.image(
            "assets/soal1_mach_band.jpg",
            caption="Gambar 2 di pojok kanan gambar 1",
            width="stretch",
        )

    st.info(
        "💡 Klik kanan > 'Save image as...' pada gambar di atas untuk pakai sebagai bahan uji, atau upload gambar sendiri di bawah."
    )
    st.markdown("---")

    uploaded = st.file_uploader(
        "Upload Gambar:", type=["jpg", "jpeg", "png", "bmp", "tif", "tiff"]
    )
    if uploaded is None:
        st.info("⬆ Silakan upload gambar untuk memulai.")
        return

    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img_bgr is None:
        st.error("Gagal membaca gambar.")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    h, w = img_gray.shape

    st.markdown("#### 📏 Informasi Citra")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lebar", f"{w} px")
    c2.metric("Tinggi", f"{h} px")
    c3.metric("Total Piksel", f"{w*h:,}")

    st.markdown("#### 🖼 Tampilan Citra")
    col_a, col_b = st.columns(2)
    with col_a:
        show_image_centered(img_rgb, caption="Citra Asli (RGB)")
    with col_b:
        show_image_centered(img_gray, caption="Citra Grayscale")

    st.markdown("#### 🔢 Sampel Nilai Piksel (5×5 pojok kiri atas)")
    st.dataframe(img_gray[:5, :5].astype(int))

    with st.expander("📚 Teori & Pembahasan"):
        st.markdown("""
        - **Piksel** = picture element, unit terkecil citra digital
        - **Grayscale 8-bit**: rentang intensitas 0 (hitam) – 255 (putih)
        - **Formula luminositas**: `Gray = 0.299R + 0.587G + 0.114B`
        - **Histogram** menunjukkan distribusi frekuensi nilai intensitas piksel
        """)

# modules/tugas2/histogram_eq.py
import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Helper lokal (biar tidak tergantung utils)
def show_image_centered(image, caption: str = ""):
    st.markdown(
        '<div style="display:flex;justify-content:center">', unsafe_allow_html=True
    )
    if isinstance(image, plt.Figure):
        st.pyplot(image, clear_figure=True)
    else:
        st.image(image, caption=caption, width=280)
    st.markdown("</div>", unsafe_allow_html=True)


def run():
    st.markdown("### 🎨 Materi 2 — Sub-Modul 2: Histogram Equalization & CLAHE")
    st.markdown("---")

    # --- TAMPILKAN GAMBAR CONTOH ---
    st.markdown("#### 📘 Contoh Buku (Gonzalez)")

    here = Path(__file__).resolve()
    base = here.parents[2] / "assets"
    if not base.exists():
        base = here.parents[1] / "assets"

    contoh_path = base / "contoh_contrast_stretching.png"

    if contoh_path.exists():
        st.image(
            str(contoh_path),
            caption="Fig 3.10 & 3.18 — Pollen low-contrast (dipakai untuk HEQ & Contrast Stretching)",
            width=700,
        )
    else:
        st.warning("Simpan 'contoh_contrast_stretching.png' di folder assets/")

    with st.expander("📖 Kenapa pakai gambar ini?", expanded=False):
        st.markdown("""
        - Gambar pollen ini adalah contoh resmi dari buku Gonzalez
        - Di PDF Tugas 2 halaman 5 dipakai untuk **Contrast Stretching**
        - Di buku asli, gambar yang sama dipakai untuk demo **Histogram Equalization**
        - Jadi 1 gambar = 2 materi (hemat, dan sesuai instruksi dosen)
        """)

    st.markdown("---")
    st.markdown("#### 💻 Coba Sendiri")

    uploaded = st.file_uploader(
        "Upload Gambar:", type=["jpg", "jpeg", "png", "tif"], key="he_up"
    )
    if uploaded is None:
        st.info("⬆️ Silakan upload gambar low-contrast (pollen.tif direkomendasikan)")
        return

    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img_bgr is None:
        st.error("Gagal membaca gambar.")
        return

    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Kontrol CLAHE
    c1, c2 = st.columns(2)
    with c1:
        clip_limit = st.slider("CLAHE Clip Limit:", 1.0, 10.0, 2.0, 0.5)
    with c2:
        tile_size = st.select_slider("CLAHE Tile Size:", [4, 8, 16, 32], value=8)

    img_heq = cv2.equalizeHist(img_gray)
    clahe_obj = cv2.createCLAHE(
        clipLimit=clip_limit, tileGridSize=(tile_size, tile_size)
    )
    img_clahe = clahe_obj.apply(img_gray)

    # Tampilkan 3 gambar
    col1, col2, col3 = st.columns(3)
    with col1:
        show_image_centered(img_gray, caption="Asli")
    with col2:
        show_image_centered(img_heq, caption="Global HEQ")
    with col3:
        show_image_centered(img_clahe, caption=f"CLAHE (clip={clip_limit})")

    # Histogram
    st.markdown("#### 📊 Perbandingan Histogram")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    for ax, img, title in zip(
        axes, [img_gray, img_heq, img_clahe], ["Asli", "HEQ", "CLAHE"]
    ):
        ax.hist(img.ravel(), bins=256, range=[0, 256], color="#002d62", alpha=0.7)
        ax.set_title(title)
        ax.set_xlabel("Intensitas")
        ax.set_ylabel("Frekuensi")
        ax.tick_params(labelsize=8)
    plt.tight_layout()
    show_image_centered(fig, caption="Histogram menjadi rata setelah HEQ")
    plt.close(fig)

    with st.expander("📚 Teori & Pembahasan"):
        st.markdown("""
        - **HEQ Global**: mendistribusikan histogram ke seluruh rentang [0,255] menggunakan CDF
        - **CLAHE**: versi local HEQ + clip limit untuk mencegah noise
        - **Bedanya dengan Contrast Stretching**: HEQ mengubah bentuk histogram (non-linear), sedangkan stretching hanya menarik linear
        """)

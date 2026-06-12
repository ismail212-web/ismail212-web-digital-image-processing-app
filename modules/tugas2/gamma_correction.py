# modules/tugas2/gamma_correction.py
import streamlit as st
import cv2
import numpy as np
from utils import show_image_centered


def run():
    st.markdown(
        "### 🎨 Materi 2 — Sub-Modul 1: Gamma Correction (Power-Law Transformation)"
    )
    st.markdown("Kiri = Contoh buku (MRI & Aerial). Kanan = Hasil Anda setelah upload.")
    st.markdown("---")

    uploaded = st.file_uploader(
        "📤 Upload Gambar:", type=["jpg", "jpeg", "png", "tif"], key="gc_up"
    )

    img_rgb = None
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img_bgr is not None:
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**📘 Contoh Buku**")
        st.image(
            "assets/contoh_gamma_mri.jpg",
            caption="Figure 3.8 — MRI spine: γ = 0.6, 0.4, 0.3",
            use_container_width=True,
        )
        st.image(
            "assets/contoh_gamma_aerial.jpg",
            caption="Figure 3.9 — Aerial: γ = 3.0, 4.0, 5.0",
            use_container_width=True,
        )

    with c2:
        st.markdown("**💻 Hasil Anda**")
        if img_rgb is None:
            st.info("Upload gambar dulu — pakai MRI atau foto gelap/terang")
        else:
            gamma = st.slider("Nilai Gamma (γ):", 0.1, 5.0, 1.0, 0.1)
            c_const = st.slider("Konstanta c:", 0.5, 2.0, 1.0, 0.1)

            lut = np.array(
                [
                    min(255, int(c_const * (i / 255.0) ** gamma * 255))
                    for i in range(256)
                ],
                dtype=np.uint8,
            )
            img_gamma = cv2.LUT(img_rgb, lut)

            col_a, col_b = st.columns(2)
            with col_a:
                show_image_centered(img_rgb, caption="Asli")
            with col_b:
                show_image_centered(img_gamma, caption=f"γ={gamma}, c={c_const}")

            effect = (
                "🌑 Lebih GELAP (γ>1)"
                if gamma > 1
                else ("☀ Lebih TERANG (γ<1)" if gamma < 1 else "✅ Tidak berubah")
            )
            st.info(f"**Efek:** {effect}")

    with st.expander("📚 Teori & Pembahasan"):
        st.markdown("""
        - **s = c · r^γ**
        - **γ < 1**: angkat area gelap (cocok untuk MRI, X-ray)
        - **γ > 1**: tekan area terang (cocok untuk foto aerial yang washout)
        - **γ = 1**: identitas
        """)

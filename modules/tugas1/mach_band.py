# modules/tugas1/mach_band.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils.image_utils import show_image_centered


def run():
    st.markdown("### 👁️ Materi 1 — Sub-Modul 2: Mach Band Effect")
    st.markdown("""
    Eksperimen ini mendemonstrasikan fenomena persepsi visual dimana mata
    memperkuat kontras di perbatasan antar tingkat keabuan.
    """)

    # --- GAMBAR CONTOH ---
    st.markdown("**2. Modul yang menampilkan fenomena mach band effect**")
    st.image(
        "assets/soal1_mach_band.jpg",
        caption="Contoh: 4 kotak abu-abu identik terlihat berbeda karena latar belakang",
        width=400,
    )
    st.info(
        "💡 Gambar kiri adalah grayscale ramp, kanan-atas adalah simultaneous contrast — keduanya memicu Mach Band."
    )
    st.markdown("---")

    # --- SIMULASI ---
    st.markdown("#### 🧪 Simulasi Mach Band")

    # buat gradient 10 level
    levels = st.slider("Jumlah level keabuan", 5, 20, 10)

    gradient = np.tile(np.linspace(0, 1, levels), (80, 1))

    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.imshow(gradient, cmap="gray", aspect="auto", vmin=0, vmax=1)
    ax.set_title(f"Simulasi Mach Band - {levels} level", fontsize=12, pad=10)
    ax.set_xlabel("Perbatasan terlihat lebih terang/gelap (ilusi)")
    ax.axis("off")

    show_image_centered(
        fig, caption="Perhatikan garis terang/gelap di tiap batas — padahal tidak ada"
    )

    with st.expander("📚 Teori & Pembahasan"):
        st.markdown("""
        - **Mach Band Effect**: ditemukan oleh Ernst Mach (1865)
        - **Penyebab**: Lateral inhibition di retina — sel saraf menekan aktivitas tetangganya
        - **Aplikasi**: 
          1. Desain UI (menghindari banding pada gradient)
          2. Radiologi (bisa salah baca tepi tumor)
          3. Fotografi (halo di HDR)
        - **Simultaneous Contrast**: kotak abu-abu yang sama terlihat beda di latar gelap vs terang
        """)

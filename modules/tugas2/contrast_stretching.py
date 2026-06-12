# modules/tugas2/contrast_stretching.py
import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt


def run():
    st.markdown("### 🎨 Materi 2 — Sub-Modul 3: Contrast Stretching")
    st.markdown("---")

    # ATAS: contoh buku - kecilin biar muat
    st.markdown("#### 📘 Contoh Buku")
    st.image(
        "assets/contoh_contrast_stretching.png",
        caption="Before → After + histogram",
        width=700,
    )  # <— kunci: width tetap, bukan full

    st.markdown("---")
    st.markdown("#### 💻 Hasil Anda")

    uploaded = st.file_uploader(
        "Upload gambar low-contrast:", type=["jpg", "jpeg", "png", "tif"], key="cs_up"
    )
    if not uploaded:
        st.info("Upload file pollen .tif")
        return

    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    c1, c2 = st.columns(2)
    p_low = c1.slider("Percentile Bawah", 0, 49, 2)
    p_high = c2.slider("Percentile Atas", 51, 100, 98)

    v_low = int(np.percentile(img_gray, p_low))
    v_high = int(np.percentile(img_gray, p_high))
    img_stretched = np.clip(
        (img_gray.astype(np.float32) - v_low) / max(v_high - v_low, 1) * 255, 0, 255
    ).astype(np.uint8)

    # BAWAH: 2 gambar + histogram, ukuran sama kayak contoh
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        st.image(img_gray, caption=f"Asli", width=220)
    with col_b:
        st.image(img_stretched, caption=f"Stretched", width=220)
    with col_c:
        fig, ax = plt.subplots(figsize=(2.2, 1.6))  # kecil
        ax.hist(img_stretched.ravel(), bins=64, color="gray")
        ax.set_title("Histogram", fontsize=8)
        ax.tick_params(labelsize=6)
        plt.tight_layout()
        st.pyplot(fig)

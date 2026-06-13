# modules/tugas1/quantization.py
import streamlit as st
import cv2
import numpy as np


def quantize_gray(img_gray, levels):
    """Kurangi level keabuan ke 'levels' (2-256)"""
    if levels >= 256:
        return img_gray
    step = 256 // levels
    q = (img_gray // step) * step
    # stretch biar kontras tetap terlihat
    if levels > 1:
        q = ((q / 255.0) * (levels - 1) / (levels - 1) * 255).astype(np.uint8)
    return q


def run():
    st.markdown("### 🎨 Materi 1 — Sub-Modul 4: Quantization & False Contouring")
    st.markdown("Kiri = Contoh buku (8 level). Kanan = Hasil Anda setelah upload.")
    st.markdown("---")

    uploaded = st.file_uploader(
        "📤 Upload gambar (pakai tower.jpg)",
        type=["jpg", "jpeg", "png"],
        key="quant_up",
    )

    img_gray = None
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**📘 Contoh Buku**")
        st.image(
            "assets/contoh_tower_levels.png",
            caption="256 → 128 → 64 → 32 → 16 → 8 → 4 → 2 level",
            width="stretch",
        )

    with c2:
        st.markdown("**💻 Hasil Anda**")
        if img_gray is None:
            st.info("Upload gambar dulu")
        else:
            levels = [256, 128, 64, 32, 16, 8, 4, 2]
            top = st.columns(4)
            bot = st.columns(4)
            for i, lvl in enumerate(levels):
                q = quantize_gray(img_gray, lvl)
                q_vis = cv2.resize(q, (180, 180), interpolation=cv2.INTER_NEAREST)
                col = top[i] if i < 4 else bot[i - 4]
                with col:
                    st.image(q_vis, caption=f"{lvl} level", width="stretch")

# modules/tugas1/spatial_resolution.py
import streamlit as st
import cv2
import numpy as np
import base64


def run():
    st.markdown("### 🔍 Materi 1 — Sub-Modul 3: Spatial Resolution")
    st.markdown("Kiri = Contoh buku. Kanan = Hasil Anda (setelah upload).")

    versi = st.radio(
        "Pilih:",
        ["Versi 1: 4 gambar", "Versi 2: Besar → kecil", "Versi 3: 6 gambar"],
        horizontal=True,
    )
    st.markdown("---")

    uploaded = st.file_uploader(
        "📤 Upload gambar untuk dibandingkan",
        type=["jpg", "jpeg", "png"],
        key="spatial_up",
    )
    img = None
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ===== VERSI 1 =====
    if versi.startswith("Versi 1"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📘 Contoh Buku**")
            st.image("assets/contoh_tower_4.png", width="stretch")
        with c2:
            st.markdown("**💻 Hasil Anda**")
            if img is None:
                st.info("Upload gambar dulu")
            else:
                r1c1, r1c2 = st.columns(2)
                r2c1, r2c2 = st.columns(2)
                for col, sz in [(r1c1, 256), (r1c2, 128), (r2c1, 64), (r2c2, 32)]:
                    small = cv2.resize(img, (sz, sz), cv2.INTER_NEAREST)
                    vis = cv2.resize(small, (220, 220), cv2.INTER_NEAREST)
                    with col:
                        st.image(vis, caption=f"{sz}x{sz}", width="stretch")

    # ===== VERSI 2 =====
    elif versi.startswith("Versi 2"):
        c1, c2 = st.columns([1.1, 1.4])
        with c1:
            st.markdown("**📘 Contoh Buku**")
            st.image("assets/contoh_rose_cascade.png", width="stretch")
        with c2:
            st.markdown("**💻 Hasil Anda**")
            if img is None:
                st.info("Upload gambar dulu")
            else:
                sizes = [512, 256, 128, 64, 32, 16]
                disp_w = [200, 140, 95, 65, 45, 35]
                html = '<div style="display:flex; align-items:flex-start; gap:14px; overflow-x:auto; padding-top:4px;">'
                for sz, dw in zip(sizes, disp_w):
                    small = cv2.resize(img, (sz, sz), cv2.INTER_NEAREST)
                    _, buf = cv2.imencode(
                        ".png", cv2.cvtColor(small, cv2.COLOR_RGB2BGR)
                    )
                    b64 = base64.b64encode(buf).decode()
                    html += f'<div style="text-align:center;"><img src="data:image/png;base64,{b64}" style="width:{dw}px;height:{dw}px;image-rendering:pixelated;border-radius:6px;border:1px solid #ddd;"><div style="font-size:12px;margin-top:3px;">{sz}</div></div>'
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

    # ===== VERSI 3 - INI YANG KEMARIN HILANG =====
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📘 Contoh Buku**")
            st.image("assets/contoh_rose_6grid.png", width="stretch")
        with c2:
            st.markdown("**💻 Hasil Anda**")
            if img is None:
                st.info("Upload gambar dulu")
            else:
                sizes = [256, 128, 64, 32, 16, 8]
                top = st.columns(3)
                bot = st.columns(3)
                for i, sz in enumerate(sizes):
                    small = cv2.resize(img, (sz, sz), cv2.INTER_NEAREST)
                    vis = cv2.resize(small, (160, 160), cv2.INTER_NEAREST)
                    col = top[i] if i < 3 else bot[i - 3]
                    with col:
                        st.image(vis, caption=str(sz), width="stretch")

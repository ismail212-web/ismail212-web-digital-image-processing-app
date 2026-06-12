# modules/tugas2/logic_operations.py
import streamlit as st
import cv2
import numpy as np


def run():
    st.markdown("### 🎨 Materi 2 — Sub-Modul 4: Logic Operations")
    st.markdown("**Application: Crop areas of interest**")

    tab1, tab2 = st.tabs(["📘 Gambar Buku", "🧪 Praktikum"])

    with tab1:
        st.image("assets/logic_operations_capitol.png", use_container_width=True)

    with tab2:
        up = st.file_uploader(
            "Upload 1 Gambar Capitol:", type=["jpg", "jpeg", "png", "tif", "tiff"]
        )
        if not up:
            st.info("Upload gambar Capitol.")
            return

        img = cv2.imdecode(np.frombuffer(up.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        h, w = img.shape

        op = st.selectbox(
            "Pilih Operasi:", ["AND (A & B)", "OR (A | B)", "NOT (A)", "XOR (A ^ B)"]
        )

        # === KOORDINAT PRESISI BUKU (sudah diukur pixel) ===
        # Kotak TIDAK di tengah, tapi center-horizontal di puncak kubah
        x1 = int(w * 0.440)
        y1 = int(h * 0.025)
        x2 = int(w * 0.565)
        y2 = int(h * 0.265)

        # --- Helper buat teks center ---
        def put_center_text(image, text, color):
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 2.0
            thickness = 4
            (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
            x = (w - tw) // 2
            y = int(h * 0.58)
            cv2.putText(image, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)

        # AND
        mask_and = np.zeros((h, w), dtype=np.uint8)
        mask_and[y1:y2, x1:x2] = 225
        put_center_text(mask_and, "AND", 255)
        result_and = np.zeros((h, w), dtype=np.uint8)
        result_and[y1:y2, x1:x2] = img[y1:y2, x1:x2]  # <-- ISI GAMBAR ASLI

        # OR
        mask_or = np.full((h, w), 225, dtype=np.uint8)
        mask_or[y1:y2, x1:x2] = 0
        put_center_text(mask_or, "OR", 0)
        result_or = np.full((h, w), 235, dtype=np.uint8)
        result_or[y1:y2, x1:x2] = img[y1:y2, x1:x2]  # <-- ISI GAMBAR ASLI

        # NOT
        result_not = cv2.bitwise_not(img)
        mask_not = np.full((h, w), 120, dtype=np.uint8)
        put_center_text(mask_not, "NOT", 255)

        # XOR
        # XOR — buat mask baru biar teks tidak dobel
        mask_xor = np.zeros((h, w), dtype=np.uint8)
        mask_xor[y1:y2, x1:x2] = 225
        put_center_text(mask_xor, "XOR", 255)
        # menjadi ini
        result_xor = np.zeros((h, w), dtype=np.uint8)
        result_xor[y1:y2, x1:x2] = cv2.bitwise_not(img[y1:y2, x1:x2])

        # Pilih
        if op.startswith("AND"):
            mask, result = mask_and, result_and
            cap_m, cap_r = "Image mask", "Result Region of Interest"
        elif op.startswith("OR"):
            mask, result = mask_or, result_or
            cap_m, cap_r = "Image mask", "Result Region of Interest"
        elif op.startswith("NOT"):
            mask, result = mask_not, result_not
            cap_m, cap_r = "NOT (tidak pakai mask)", "Result NOT"
        else:
            mask, result = mask_xor, result_xor
            cap_m, cap_r = "Image mask", "Result XOR"

        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(img, use_container_width=True)
            st.markdown(
                "<p style='text-align:center'>Original<br>image</p>",
                unsafe_allow_html=True,
            )
        with c2:
            st.image(mask, use_container_width=True)
            st.markdown(
                f"<p style='text-align:center'>{cap_m}</p>", unsafe_allow_html=True
            )
        with c3:
            st.image(result, use_container_width=True)
            st.markdown(
                f"<p style='text-align:center'>{cap_r}</p>", unsafe_allow_html=True
            )

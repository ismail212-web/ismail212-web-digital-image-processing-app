# modules/tugas2/arithmetic_subtraction_result.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path


def run():
    st.markdown("### ➖ Arithmetic Operation: Subtraction")
    st.caption("Application: Mask mode radiography in angiography")

    # --- path ---
    base = Path(__file__).resolve().parents[2] / "assets"
    fig_path = base / "arithmetic_subtraction_figure.png"
    default_mask = base / "arithmetic_subtraction_mask.png"
    default_result = base / "arithmetic_subtraction_result.png"

    # 1. Gambar buku kecil
    if fig_path.exists():
        st.image(str(fig_path), caption="FIGURE 3.29 — Gonzalez & Woods", width=430)

    st.divider()

    # 2. Dua uploader sejajar
    c_up1, c_up2 = st.columns(2)
    with c_up1:
        up_mask = st.file_uploader(
            "1. Upload MASK (a)",
            type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"],
            key="mask",
        )
    with c_up2:
        up_live = st.file_uploader(
            "2. Upload LIVE (sesudah kontras)",
            type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"],
            key="live",
        )

    # pakai default kalau belum upload
    if up_mask:
        mask = cv2.imdecode(
            np.frombuffer(up_mask.read(), np.uint8), cv2.IMREAD_GRAYSCALE
        )
    elif default_mask.is_file():
        mask = cv2.imread(str(default_mask), cv2.IMREAD_GRAYSCALE)
    else:
        st.info("Upload gambar MASK dulu")
        return

    if up_live:
        live = cv2.imdecode(
            np.frombuffer(up_live.read(), np.uint8), cv2.IMREAD_GRAYSCALE
        )
    else:
        st.info("Upload gambar LIVE untuk proses")
        return

    # samakan ukuran
    live = cv2.resize(live, (mask.shape[1], mask.shape[0]))

    # 3. Proses subtraction yang benar
    # pakai absdiff biar tidak negatif, lalu kontras
    hasil = cv2.absdiff(live, mask)
    hasil = cv2.normalize(hasil, None, 0, 255, cv2.NORM_MINMAX)
    hasil = cv2.equalizeHist(hasil)  # biar pembuluh putih seperti buku

    # 4. Tampilkan 3 gambar kecil dalam 1 baris
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(mask, caption="(a) Mask", width=190)
    with c2:
        st.image(live, caption="Live", width=190)
    with c3:
        st.image(hasil, caption="(b) Live - Mask", width=190)

    st.caption("Hasil = |Live - Mask| → pembuluh darah terlihat putih")

"""
Modul UI untuk Pencocokan Sidik Jari (Fraud Detection).
Menggunakan core algorithms dari src/fingerprint/matching
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image as PILImage
import pandas as pd
from datetime import datetime
from io import BytesIO
from src.fingerprint.matching import match_fingerprints

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_OK = True
except Exception:
    REPORTLAB_OK = False


def load_img_safe(uploaded_file):
    try:
        img = PILImage.open(uploaded_file)
        if getattr(img, "n_frames", 1) > 1:
            img.seek(0)
        if img.mode in ("I;16", "I;16B", "I"):
            arr = np.array(img).astype(np.float32)
            arr = np.clip(arr, 0, arr.max())
            if arr.max() > 0:
                arr = arr / arr.max() * 255.0
            return arr.astype(np.uint8)
        return np.array(img.convert("L"))
    except Exception as e:
        st.error(f"Gagal baca gambar: {e}")
        return None


def run():
    st.markdown("## 🔐 Deteksi Kecurangan Sidik Jari (SIFT Matching)")
    st.caption("Mencocokkan fitur lokal menggunakan SIFT + FLANN + Lowe's Ratio Test")

    c1, c2 = st.columns(2)
    with c1:
        up_a = st.file_uploader("Barang Bukti A (TKP)", type=["jpg", "jpeg", "png", "tif", "tiff"], key="fp_a")
    with c2:
        up_b = st.file_uploader("Barang Bukti B (Terduga)", type=["jpg", "jpeg", "png", "tif", "tiff"], key="fp_b")

    if not (up_a and up_b):
        st.info("Upload kedua sidik jari untuk memulai pencocokan.")
        return

    img_a = load_img_safe(up_a)
    img_b = load_img_safe(up_b)
    if img_a is None or img_b is None:
        return

    with st.spinner("Sedang mengekstrak fitur dan mencocokkan..."):
        # Panggil fungsi matching dari src/
        match_result = match_fingerprints(img_a, img_b, ratio_threshold=0.75)

    good_matches = match_result["good_matches"]
    num_match = len(good_matches)
    score = match_result["similarity_score"]
    is_match = match_result["is_match"]

    # Visualisasi
    st.markdown("### 🎯 Hasil Pencocokan")
    
    if num_match > 0:
        match_img = cv2.drawMatches(img_a, match_result["kp1"], img_b, match_result["kp2"], good_matches[:50], None, flags=2)
        match_img_rgb = cv2.cvtColor(match_img, cv2.COLOR_BGR2RGB)
        st.image(match_img_rgb, caption=f"Good Matches: {num_match} titik", width="stretch")
    else:
        st.warning("⚠️ Tidak ada kecocokan fitur yang ditemukan.")

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Similarity Score", f"{score:.2f}%")
    with col_res2:
        status_text = "✅ POSITIF (Cocok)" if is_match else "❌ NEGATIF (Tidak Cocok)"
        st.metric("Status Identitas", status_text)
        
    st.warning(
        f"**CATATAN:** Standar minimal pencocokan manual adalah 12 titik minutiae. "
        f"Pendekatan *feature-based* (SIFT) ini menemukan **{num_match} good matches**."
    )

    # PDF Generation (Opsional, tetap dipertahankan)
    if REPORTLAB_OK:
        if st.button("📄 Generate Laporan PDF", type="primary"):
            buf = BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4)
            styles = getSampleStyleSheet()
            story = [
                Paragraph("LAPORAN ANALISIS DAKTILOSKOPI DIGITAL", styles["Title"]),
                Spacer(1, 12),
                Paragraph(f"Tanggal: {datetime.now().strftime('%d %B %Y')}", styles["Normal"]),
                Paragraph("Analis: Ismail Pamudji (NIM: 14250035)", styles["Normal"]),
                Spacer(1, 24),
                Paragraph("HASIL MATCHING", styles["Heading2"]),
            ]
            data = [
                ["Parameter", "Nilai"],
                ["Jumlah Good Matches", str(num_match)],
                ["Similarity Score", f"{score:.2f}%"],
                ["Status", "POSITIF" if is_match else "NEGATIF"]
            ]
            t = Table(data, colWidths=[200, 200])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(t)
            doc.build(story)
            buf.seek(0)
            st.download_button(
                "⬇️ Download PDF",
                buf,
                f"Laporan_SidikJari_{datetime.now().strftime('%Y%m%d')}.pdf",
                "application/pdf",
            )

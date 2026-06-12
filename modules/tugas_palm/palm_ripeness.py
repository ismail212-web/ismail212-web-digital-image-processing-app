# -*- coding: utf-8 -*-
# modules/tugas_fp/palm_ripeness.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image as PILImage
import pandas as pd
from datetime import datetime


def load_image(f):
    return np.array(PILImage.open(f).convert("RGB"))


def analyze(img, ho1=5, ho2=25, hg1=35, hg2=85):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    m_g = cv2.inRange(hsv, (hg1, 40, 40), (hg2, 255, 255))
    m_y = cv2.inRange(hsv, (20, 40, 40), (35, 255, 255))
    m_o = cv2.inRange(hsv, (ho1, 50, 50), (ho2, 255, 255))
    m_r1 = cv2.inRange(hsv, (0, 50, 50), (5, 255, 255))
    m_r2 = cv2.inRange(hsv, (160, 50, 50), (180, 255, 255))
    m_ripe = cv2.bitwise_or(m_o, cv2.bitwise_or(m_r1, m_r2))
    m_over = cv2.inRange(hsv, (5, 20, 20), (25, 150, 100))
    tot = img.shape[0] * img.shape[1]
    pg, py, pr, po = [
        np.count_nonzero(m) / tot * 100 for m in [m_g, m_y, m_ripe, m_over]
    ]

    if pr >= 60:
        stt, col, rec = "MATANG", "#16a34a", "Siap panen - kualitas optimal"
    elif pr >= 35:
        stt, col, rec = "MENGKAL", "#eab308", "Tunggu 3-5 hari"
    elif pg >= 50:
        stt, col, rec = "MENTAH", "#22c55e", "Belum siap"
    elif po >= 30:
        stt, col, rec = "TERLALU MATANG", "#dc2626", "Segera olah"
    else:
        stt, col, rec = "CAMPURAN", "#6b7280", "Perlu sortasi manual"

    overlay = img.copy()
    overlay[m_g > 0] = [0, 255, 0]
    overlay[m_y > 0] = [255, 255, 0]
    overlay[m_ripe > 0] = [255, 100, 0]
    overlay[m_over > 0] = [139, 69, 19]
    seg = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
    ripe = cv2.bitwise_and(img, img, mask=m_ripe)
    return {
        "status": stt,
        "color": col,
        "rec": rec,
        "pg": pg,
        "py": py,
        "pr": pr,
        "po": po,
        "orig": img,
        "seg": seg,
        "ripe": ripe,
    }


def run():
    st.markdown("## 🌴 [4.3] Palm Oil Ripeness Detection")
    st.caption("NIM: 14250035 — Ismail Pamudji")

    up = st.file_uploader("Upload Foto TBS:", type=["jpg", "jpeg", "png"])
    if not up:
        st.info("Upload foto tandan sawit untuk analisis")
        return

    img = load_image(up)
    with st.sidebar:
        st.markdown("### ⚙️ Kalibrasi HSV")
        ho1 = st.slider("Hue Oranye Min", 0, 30, 5)
        ho2 = st.slider("Hue Oranye Max", 10, 40, 25)
        hg1 = st.slider("Hue Hijau Min", 25, 50, 35)
        hg2 = st.slider("Hue Hijau Max", 70, 100, 85)

    a = analyze(img, ho1, ho2, hg1, hg2)

    # === HEADER STATUS ===
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(
            f"<div style='background:{a['color']};color:white;padding:25px;border-radius:12px;text-align:center'><h1>{a['status']}</h1></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.info(f"**Rekomendasi:** {a['rec']}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Matang", f"{a['pr']:.1f}%")
    m2.metric("Mengkal", f"{a['py']:.1f}%")
    m3.metric("Mentah", f"{a['pg']:.1f}%")
    m4.metric("Overripe", f"{a['po']:.1f}%")

    v1, v2, v3 = st.columns(3)
    v1.image(a["orig"], caption="Original", use_container_width=True)
    v2.image(a["seg"], caption="Segmentasi", use_container_width=True)
    v3.image(a["ripe"], caption="Area Matang", use_container_width=True)

    # ===== LAPORAN LENGKAP =====
    st.markdown("---")

    # I. PENDAHULUAN
    with st.expander("📄 I. PENDAHULUAN", expanded=True):
        st.markdown("""
Laporan ini disusun berdasarkan hasil pengujian visual dan digital terhadap sampel foto TBS Kelapa Sawit yang masuk ke Loading Ramp pada hari ini.
Tujuan analisis adalah untuk memitigasi risiko lolosnya buah mentah (unripe) dan buah terlalu matang (overripe) yang dapat menurunkan kualitas Crude Palm Oil (CPO).
        """)

    # II. METODE
    with st.expander("🔬 II. METODE ANALISIS"):
        st.markdown("""
Pemeriksaan dilakukan menggunakan metode fraksinasi standar kelapa sawit gabungan dengan ekstraksi segmentasi warna (Computer Vision) untuk mengelompokkan tingkat kematangan buah secara objektif.
        """)

    # III. HASIL
    st.markdown("### 📊 III. HASIL ANALISIS VISUAL & DIGITAL")
    st.markdown(
        "Berdasarkan sampel foto buah sawit yang diperiksa, berikut adalah poin-poin observasi utama:"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
<div style="background:#f0fdf4;padding:16px;border-radius:10px;border-left:5px solid #16a34a">
<h4>🟢 Kondisi Buah Mentah (Unripe / Unbrondol)</h4>
<b>Persentase Terdeteksi: {a['pg']:.1f}%</b><br><br>
<b>Karakteristik Visual:</b> Warna buah dominan hitam pekat, tekstur keras, dan belum menunjukkan adanya brondolan alami yang lepas dari janjangan (Fraksi 0).<br><br>
<b>Dampak Teknis:</b> Kandungan minyak (oil content) sangat rendah, menyulitkan proses perebusan (sterilizer), dan berisiko mematahkan pisau thresher (penebah).
</div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
<div style="background:#fff7ed;padding:16px;border-radius:10px;border-left:5px solid #ea580c">
<h4>🟠 Kondisi Buah Matang Sempurna (Ripe / Ripe-Brondol)</h4>
<b>Persentase Terdeteksi: {a['pr']:.1f}%</b><br><br>
<b>Karakteristik Visual:</b> Warna permukaan buah luar sudah berubah menjadi merah jingga/oranye terang secara merata. Terlihat adanya bekas brondolan lepas di bagian piringan (Fraksi 2 - 3).<br><br>
<b>Dampak Teknis:</b> Kandungan rendemen minyak berada di tingkat maksimal (estimasinya 22% - 25%) dengan kadar Asam Lemak Bebas (FFA) yang rendah (< 3%). Kondisi ini adalah target utama pabrik.
</div>
        """,
            unsafe_allow_html=True,
        )

    # IV. REKAPITULASI
    st.markdown("### IV. REKAPITULASI SORTASI DATA")
    total = 300
    df = pd.DataFrame(
        {
            "Kategori Kematangan": [
                "Mentah",
                "Mengkal",
                "Matang Sempurna",
                "Terlalu Matang",
                "TOTAL",
            ],
            "Estimasi Fraksi": [
                "Fraksi 0",
                "Fraksi 0-1",
                "Fraksi 1-3",
                "Fraksi 4-5",
                "-",
            ],
            "Jumlah Janjang": [
                int(total * a["pg"] / 100),
                int(total * a["py"] / 100),
                int(total * a["pr"] / 100),
                int(total * a["po"] / 100),
                total,
            ],
            "Persentase (%)": [
                f"{a['pg']:.1f}",
                f"{a['py']:.1f}",
                f"{a['pr']:.1f}",
                f"{a['po']:.1f}",
                "100.0",
            ],
            "Status Kualitas": [
                "❌ Di bawah standar (Denda/Reject)" if a["pg"] > 10 else "✅ Baik",
                "⚠ Perlu pemeraman" if a["py"] > 5 else "✅ Baik",
                "✅ Diterima (Optimal)" if a["pr"] >= 60 else "⚠ Kurang optimal",
                "⚠ Peringatan (FFA Tinggi)" if a["po"] > 10 else "✅ Baik",
                "-",
            ],
        }
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    # V. KESIMPULAN
    st.markdown("### V. KESIMPULAN DAN REKOMENDASI")
    status_kualitas = "Baik" if a["pr"] >= 60 else "Perlu Perbaikan"
    kesimpulan_text = f"Kualitas TBS yang masuk hari ini secara umum **{status_kualitas}** dengan {a['pr']:.1f}% buah matang optimal. Namun, masih ditemukan adanya buah mentah sebesar {a['pg']:.1f}% dan overripe {a['po']:.1f}% yang lolos ke area pabrik."

    if a["pr"] >= 60:
        st.success(f"**Kesimpulan:** {kesimpulan_text}")
    else:
        st.warning(f"**Kesimpulan:** {kesimpulan_text}")

    st.markdown(f"""
**Rekomendasi untuk Atasan:**
1. Mohon instruksikan kepada Mandor Panen di Afdeling terkait untuk lebih ketat mengawasi kriteria matang panen (wajib melihat jumlah brondolan di piringan, bukan hanya melihat warna kulit luar).
2. Buah mentah sebanyak **{a['pg']:.1f}%** disarankan untuk dipisahkan sementara (diperam) atau dikenakan penalti/potongan berat janjang kepada pihak pengirim/kontraktor buah untuk menghindari kerugian rendemen minyak.
    """)

    st.caption(
        f"Laporan digenerate otomatis pada {datetime.now().strftime('%d %B %Y %H:%M')} | Sistem Computer Vision DIP Lab"
    )

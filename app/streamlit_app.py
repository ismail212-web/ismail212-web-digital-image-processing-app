import sys
import os
# Tambahkan root direktori proyek ke sys.path agar bisa import 'modules' dan 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st

# ==========================================
# PASTE KODE CSS INI DI BARIS ATAS APP KAMU
# ==========================================
st.markdown(
    """
    <style>
    /* 1. Memaksa teks biasa, judul, dan status kuis di sidebar rata kiri */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown div,
    [data-testid="stSidebar"] .stMarkdown span {
        text-align: left !important;
        justify-content: flex-start !important;
    }

    /* 2. Memaksa teks pada Radio Button (Pilihan Materi) rata kiri */
    [data-testid="stSidebar"] .stRadio div [role="radiogroup"] {
        text-align: left !important;
        align-items: flex-start !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        text-align: left !important;
    }

    /* 3. Memaksa Selectbox / Dropdown Modul rata kiri */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox div {
        text-align: left !important;
    }

    /* 4. Overwrite jika ada fungsi pembungkus HTML center yang bandel */
    [data-testid="stSidebar"] [style*="text-align: center"],
    [data-testid="stSidebar"] [style*="text-align:center"] {
        text-align: left !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# APP.PY - DIGITAL IMAGE PROCESSING LAB - NIM 14250035
# BERDASARKAN WARNA ADV IR PERTEMUAN 11.PDF
# ==========================================================

import streamlit as st
import os
import time
from datetime import datetime
from matplotlib.figure import Figure

# ==========================================================
# IMPORT MODUL
# ==========================================================
from modules import MASTER_LAB_REGISTRY
from modules.kuis_akhir import (
    run as run_kuis,
)
from modules.kuis_modul import (
    run_kuis_modul,
)

# ==========================================================
# KONFIGURASI KUNCI
# ==========================================================
from kunci import (
    KUIS_MODUL,
    MATERI_TERBUKA,
    KUIS_AKHIR_TERBUKA,
    BYPASS_SEMUA,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Digital Image Processing Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# SEO META TAGS
# ==========================================================
st.markdown(
    """
    <head>
    <meta name="description" content="Digital Image Processing Lab - Praktikum Mandiri Pengolahan Citra Digital - NIM 14250035">
    <meta name="keywords" content="Digital Image Processing, OpenCV, Python, Streamlit, FFT, Histogram, Filtering, Fingerprint, Palm Oil Ripeness">
    <meta name="author" content="Ismail Pamudji">
    <meta property="og:title" content="Digital Image Processing Lab">
    <meta property="og:description" content="Praktikum Interaktif Pengolahan Citra Digital Berbasis Python dan Streamlit">
    </head>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# KONSTANTA
# ==========================================================
APP_TITLE = "Digital Image Processing Lab"
APP_SUBTITLE = "Praktikum Mandiri Pengolahan Citra Digital"
NAMA_MAHASISWA = "Ismail Pamudji"
NIM_MAHASISWA = "14250035"
UNIVERSITAS = "Universitas Nusa Mandiri"
FAKULTAS = "Fakultas Teknologi Informasi"
PRODI = "Ilmu Komputer"

# ==========================================================
# FILE ASSETS
# ==========================================================
LOGO_FILE = next(
    (
        f
        for f in ["Pelajaran_1.jpeg", "Pelajaran_1.jpg", "Pelajaran_1.png"]
        if os.path.exists(f)
    ),
    "Pelajaran_1.jpeg",
)
COVER_FILE = "Pelajaran.png"


# ==========================================================
# CSS HELPER
# ==========================================================
def inject_css(hide_sidebar: bool = True):
    sidebar_rule = (
        """
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div,
        button[kind="header"]{
            display:none!important;
            visibility:hidden!important;
            width:0!important;
        }
        """
        if hide_sidebar
        else ""
    )

    st.markdown(
        f"""
        <style>
        {sidebar_rule}

        /* === BACKGROUND & GENERAL === */
        .stApp {{ background:#a8d8ea!important; }}
        .block-container {{ padding-top:1.5rem; padding-bottom:2rem; max-width:100%!important; }}
        p, span, label, li, ol, ul, .stMarkdown {{ color:#000000!important; }}
        h1 {{ color:#4a0e4e!important; font-weight:800!important; }}
        h2 {{ color:#1e3a5f!important; font-weight:700!important; }}
        h3 {{ color:#1e5631!important; font-weight:700!important; }}

        /* === SIDEBAR: PERBAIKAN RATA KIRI TOTAL (IKON + TEKS) === */
        /* === SIDEBAR BUTTON RATA KIRI === */
        section[data-testid="stSidebar"] .stButton {{
            width:100% !important;
        }}

        section[data-testid="stSidebar"] .stButton > button {{
            width:100% !important;
            display:flex !important;
            align-items:center !important;
            justify-content:flex-start !important;
            text-align:left !important;
            padding-left:12px !important;
        }}

        section[data-testid="stSidebar"] .stButton > button div {{
            width:100% !important;
            text-align:left !important;
            justify-content:flex-start !important;
        }}

        section[data-testid="stSidebar"] .stButton > button p {{
            width:100% !important;
            text-align:left !important;
            margin:0 !important;
        }}

        section[data-testid="stSidebar"] .stButton > button span {{
            width:100% !important;
            text-align:left !important;
            
            }}

        /* === LAINNYA (tetap seperti sebelumnya) === */
        @keyframes fadeInUp {{
            0% {{ opacity:0; transform:translateY(25px); }}
            100% {{ opacity:1; transform:translateY(0); }}
        }}
        .welcome-container {{ animation: fadeInUp 1.4s ease-out; width:100%; }}
        .welcome-text-1 {{ color:#4a0e4e!important; font-size:42px!important; font-weight:800!important; text-align:center; margin:30px 0 10px 0; }}
        .welcome-text-2 {{ color:#1e5631!important; font-size:28px!important; font-style:italic; text-align:center; margin-bottom:40px; }}

        div.stButton > button {{
            background:#ffffff!important;
            color:#002d62!important;
            border-radius:12px!important;
            border:2px solid #002d62!important;
            font-weight:bold!important;
            box-shadow: 0 6px 18px rgba(0,0,0,.15);
            transition:.3s;
        }}
        div.stButton > button:hover {{
            background:#e8f0fe!important;
            transform:scale(1.02);
        }}

        section[data-testid="stSidebar"] {{
            background:#e8f4f8!important;
            min-width:320px!important;
            max-width:320px!important;
            border-right:2px solid #b0d4e8!important;
        }}
        section[data-testid="stSidebar"] * {{
            color:#000000!important;
        }}

        [data-testid="stProgress"] > div > div {{
            background: linear-gradient(90deg, #00aa44, #22c55e)!important;
            border-radius:999px!important;
        }}
        .img-center {{ display:flex!important; justify-content:center!important; align-items:center!important; width:100%!important; }}
        [data-testid="stImage"] {{ display:flex!important; justify-content:center!important; }}
        [data-testid="stImage"] img {{ margin:0 auto!important; }}

        .nim-badge {{ background:#0ea5e9; border-radius:8px; padding:10px 14px; margin-bottom:16px; }}
        .locked-btn {{ background:#1a2744; color:#94a3b8; border-radius:8px; padding:8px 10px; margin:3px 0; font-size:13px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# IMAGE HELPER
# ==========================================================
def show_image_centered(image, caption: str = "", width: int = None):
    import io as _io

    if isinstance(image, Figure):
        buf = _io.BytesIO()
        image.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        buf.seek(0)
        image = buf
    if width:
        st.image(image, width=width, caption=caption)
    else:
        st.image(image, caption=caption, use_container_width=True)


# ==========================================================
# QUIZ HELPER
# ==========================================================
def quiz_passed(materi: str):
    if BYPASS_SEMUA:
        return True
    for key in ["Materi 1", "Materi 2", "Materi 3", "Materi 4", "Materi 5"]:
        if key in materi:
            if KUIS_MODUL.get(key, False):
                return True
            return st.session_state.get(f"kuis_modul_passed_{key}", False)
    return True


# ==========================================================
# MAIN
# ==========================================================
def main():
    # ======================================================
    # SESSION STATE
    # ======================================================
    if "aplikasi_terbuka" not in st.session_state:
        st.session_state.aplikasi_terbuka = False
    if "mode_kuis" not in st.session_state:
        st.session_state.mode_kuis = False
    if "splash_done" not in st.session_state:
        st.session_state.splash_done = False
    if "menu_aktif" not in st.session_state:
        st.session_state.menu_aktif = "Normal"

    if "pilihan_materi" not in st.session_state:
        daftar_materi = list(MASTER_LAB_REGISTRY.keys())
        st.session_state.pilihan_materi = daftar_materi[0] if daftar_materi else " "

    if "pilihan_sub" not in st.session_state:
        st.session_state.pilihan_sub = "Belum Dipilih"

    if "progress_materi" not in st.session_state:
        daftar_materi = list(MASTER_LAB_REGISTRY.keys())
        st.session_state.progress_materi = {m: False for m in daftar_materi}

    if "progress_sub" not in st.session_state:
        st.session_state.progress_sub = {
            m: {sub: False for sub in subs.keys()}
            for m, subs in MASTER_LAB_REGISTRY.items()
        }

    # ======================================================
    # COVER 1: SPLASH SCREEN
    # ======================================================
    if not st.session_state.splash_done:
        inject_css(hide_sidebar=True)
        SPLASH_DURASI_DETIK = 10
        SLEEP_PER_STEP = SPLASH_DURASI_DETIK / 700

        _, col_center, _ = st.columns([1, 2, 1])
        with col_center:
            st.markdown(
                """
            <div style="background: rgba(255,255,255,0.90); border-left: 6px solid #2d3748; border-radius: 14px; padding: 28px 32px; margin-bottom: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.12); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size:10px; color:#2d3748; letter-spacing:4px; text-transform:uppercase; font-weight:800; margin-bottom:10px;">Institusi</div>
                <div style="font-size:26px; font-weight:900; color:#000000; line-height:1.2; margin-bottom:6px;">Universitas Nusa Mandiri</div>
                <div style="width:36px; height:4px; background:#2d3748; border-radius:2px; margin-bottom:10px;"></div>
                <div style="font-size:16px; font-weight:700; color:#000000; margin-bottom:3px;">Fakultas Teknologi Informasi</div>
                <div style="font-size:15px; font-weight:600; color:#333333;">Ilmu Komputer</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
            <div style="background: rgba(255,255,255,0.90); border-left: 6px solid #90cdf4; border-radius: 14px; padding: 28px 32px; margin-bottom: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.12); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size:10px; color:#90cdf4; letter-spacing:4px; text-transform:uppercase; font-weight:800; margin-bottom:10px;">Aplikasi</div>
                <div style="font-size:26px; font-weight:900; color:#000000; line-height:1.2; margin-bottom:6px;">Digital Image Processing Lab</div>
                <div style="width:36px; height:4px; background:#90cdf4; border-radius:2px; margin-bottom:10px;"></div>
                <div style="font-size:15px; font-weight:600; color:#000000; margin-bottom:12px;">Praktikum Mandiri Pengolahan Citra Digital</div>
                <div style="display:inline-block; background:rgba(246,173,85,0.10); border:1.5px solid #f6ad55; border-radius:8px; padding:7px 16px; font-size:13px; color:#000000; font-weight:700;">NIM : 14250035 &nbsp;|&nbsp; Ismail Pamudji</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            if os.path.exists(LOGO_FILE):
                _, foto_col, _ = st.columns([1, 2, 1])
                with foto_col:
                    st.image(LOGO_FILE, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        _, col_pb, _ = st.columns([1, 2, 1])
        with col_pb:
            progress_bar = st.progress(0)
            progress_text = st.empty()

        for i in range(101):
            with col_pb:
                progress_bar.progress(i)
                progress_text.markdown(
                    f"<div style='text-align:center; font-size:15px; color:#f6ad55; font-weight:600; margin-top:6px;'>⏳ Loading Application... <b>{i}%</b></div>",
                    unsafe_allow_html=True,
                )
            time.sleep(SLEEP_PER_STEP)

        st.session_state.splash_done = True
        st.rerun()

    # ======================================================
    # MODE KUIS AKHIR
    # ======================================================
    if st.session_state.mode_kuis:
        inject_css(hide_sidebar=True)
        run_kuis()
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⬅ Exit Quiz & Return", use_container_width=True):
                st.session_state.mode_kuis = False
                st.rerun()
        return

    # ======================================================
    # COVER 3: WELCOME SCREEN
    # ======================================================
    if not st.session_state.aplikasi_terbuka:
        inject_css(hide_sidebar=True)
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        if os.path.exists(COVER_FILE):
            _, img_col, _ = st.columns([2, 6, 2])
            with img_col:
                st.image(COVER_FILE, use_container_width=True)
        else:
            st.warning(f"File cover tidak ditemukan: {COVER_FILE}")

        st.markdown(
            f"""
            <div style="text-align:center; margin-top:20px;">
                <h1>{APP_TITLE}</h1>
                <h3>Praktikum Interaktif Berbasis Python, OpenCV dan Streamlit</h3>
                <p class="welcome-text-1">Selamat Datang</p>
                <h1>Praktikum Mandiri Pengolahan Citra Digital</h1>
            </div>
        """,
            unsafe_allow_html=True,
        )

        _, _, col_btn, _, _ = st.columns([1, 1, 2, 1, 1])
        with col_btn:
            if st.button(
                "🚀 Buka Aplikasi", use_container_width=True, key="btn_buka_app"
            ):
                st.session_state.aplikasi_terbuka = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ======================================================
    # DASHBOARD & SIDEBAR
    # ======================================================
    inject_css(hide_sidebar=False)
    with st.sidebar:
        st.markdown("##  DIP Lab")
        st.markdown(
            f"""
            <div class="nim-badge">
                <b>NIM:</b> {NIM_MAHASISWA}<br>
                <b>Nama:</b> {NAMA_MAHASISWA}
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        daftar_materi = list(MASTER_LAB_REGISTRY.keys())
        selesai = sum(1 for v in st.session_state.progress_materi.values() if v)
        total = len(daftar_materi)
        persen = int(selesai / total * 100) if total > 0 else 0

        st.markdown(f"#### 📊 Progress\n{selesai}/{total} Materi Selesai")
        st.progress(persen / 100)
        st.caption(f"{persen}% Complete")
        st.markdown("---")
        st.markdown("####  Materi")

        for i, materi in enumerate(daftar_materi):
            aktif = st.session_state.pilihan_materi == materi
            selesai_materi = st.session_state.progress_materi.get(materi, False)
            materi_key = next((k for k in MATERI_TERBUKA if k in materi), None)

            if BYPASS_SEMUA:
                terbuka = True
            elif materi_key and MATERI_TERBUKA.get(materi_key, False):
                terbuka = True
            elif i == 0:
                terbuka = True
            else:
                materi_sebelumnya = daftar_materi[i - 1]
                terbuka = st.session_state.progress_materi.get(materi_sebelumnya, False)

            if selesai_materi:
                ikon = "✅"
            elif aktif:
                ikon = "▶"
            elif terbuka:
                ikon = "🔓"
            else:
                ikon = "🔒"

            label = f"{ikon} {materi}"
            if terbuka:
                if st.button(label, key=f"materi_{i}", use_container_width=True):
                    st.session_state.pilihan_materi = materi
                    st.session_state.pilihan_sub = "Belum Dipilih"
                    st.session_state.menu_aktif = (
                        "Normal"  # Reset menu jika ganti materi
                    )
                    st.rerun()
            else:
                st.markdown(
                    f'<div class="locked-btn">{label}</div>', unsafe_allow_html=True
                )

        st.markdown("---")
        pilihan_materi = st.session_state.pilihan_materi
        daftar_sub = list(MASTER_LAB_REGISTRY.get(pilihan_materi, {}).keys())
        if daftar_sub:
            st.markdown("#### 🔬 Sub Modul")
            for idx, sub in enumerate(daftar_sub):
                aktif_sub = st.session_state.pilihan_sub == sub
                sudah_buka = st.session_state.progress_sub.get(pilihan_materi, {}).get(
                    sub, False
                )
                if sudah_buka:
                    ikon = "✅"
                elif aktif_sub:
                    ikon = "▶"
                else:
                    ikon = "📄"
                if st.button(
                    f"{ikon} {sub}", key=f"sub_{idx}", use_container_width=True
                ):
                    st.session_state.pilihan_sub = sub
                    st.session_state.menu_aktif = (
                        "Normal"  # Reset ke normal jika pindah sub-modul
                    )
                    st.rerun()

        st.markdown("---")
        semua_selesai = all(
            st.session_state.progress_materi.get(m, False) for m in daftar_materi
        )
        kuis_akhir_bisa = BYPASS_SEMUA or KUIS_AKHIR_TERBUKA or semua_selesai
        st.markdown("#### 🎯 Evaluasi")
        if kuis_akhir_bisa:
            if st.button("📝 Kuis Akhir", use_container_width=True, type="primary"):
                st.session_state.mode_kuis = True
                st.rerun()
        else:
            st.markdown(
                '<div class="locked-btn">📝 Kuis Akhir<br><small>Selesaikan semua materi terlebih dahulu</small></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button("🏠 Kembali ke Cover", use_container_width=True):
            st.session_state.aplikasi_terbuka = False
            st.session_state.menu_aktif = "Normal"
            st.rerun()

        # ======================================================
    # MAIN CONTENT AREA
    # ======================================================
    pilihan_materi = st.session_state.pilihan_materi
    pilihan_sub = st.session_state.pilihan_sub
    st.markdown(f"# 📚 {pilihan_materi}")
    st.caption(f"Sub Modul Aktif: {pilihan_sub}")
    st.markdown("---")

    col1, col2 = st.columns([5, 1])

    with col1:
        # Hapus kotak HTML yang bermasalah
        # Ganti dengan teks biasa atau st.info()
        st.markdown(f"**Materi Aktif:** {pilihan_materi}")
        st.markdown(f"**Sub Modul:** {pilihan_sub}")
        st.markdown("---")
        st.info("""
        Silakan pilih salah satu sub-modul dari *sidebar* untuk memulai praktikum.  
        Modul praktikum ini dirancang untuk memberikan pemahaman mendalam tentang prinsip-prinsip dasar dan teknik-teknik lanjut dalam **Pengolahan Citra Digital**, merujuk pada konsep-konsep fundamental yang diuraikan dalam literatur standar seperti Gonzalez & Woods.
        """)

    with col2:
        jumlah_sub = len(MASTER_LAB_REGISTRY.get(pilihan_materi, {}))
        selesai_sub = sum(
            1
            for v in st.session_state.progress_sub.get(pilihan_materi, {}).values()
            if v
        )
        progress_sub = int(selesai_sub / jumlah_sub * 100) if jumlah_sub > 0 else 0
        st.metric("Progress", f"{progress_sub}%")

    if pilihan_sub == "Belum Dipilih":
        st.markdown("""
        👋 **Selamat Datang**

        Silakan pilih salah satu sub-modul dari *sidebar* untuk memulai praktikum. Modul praktikum ini dirancang untuk memberikan pemahaman mendalam tentang prinsip-prinsip dasar dan teknik-teknik lanjut dalam **Pengolahan Citra Digital**, merujuk pada konsep-konsep fundamental yang diuraikan dalam literatur standar seperti Gonzalez & Woods.

        **Materi yang Tersedia Meliputi:**
        *   **Image Fundamentals (Dasar-Dasar Citra):** Membahas konsep dasar citra digital, seperti resolusi spasial dan intensitas, sistem koordinat piksel, dan representasi matematis citra.
        *   **Histogram Processing (Pemrosesan Histogram):** Menjelaskan histogram citra dan teknik-teknik penguatan kontras berdasarkan manipulasi histogram, seperti *histogram equalization* dan *matching*.
        *   **Frequency Domain (Domain Frekuensi):** Memperkenalkan transformasi Fourier dan aplikasinya dalam pengolahan citra, termasuk operasi filtering di domain frekuensi untuk tujuan *smoothing* dan *sharpening*.
        *   **Segmentation (Segmentasi):** Menjelaskan metode-metode untuk membagi citra menjadi wilayah-wilayah yang bermakna, mencakup pendekatan berbasis ambang batas (*thresholding*), *edge detection*, dan *region growing*.
        *   **Feature Extraction (Ekstraksi Ciri):** Fokus pada teknik-teknik untuk mengekstrak informasi penting dari citra, seperti deteksi *minutiae* pada sidik jari atau fitur-fitur tekstur dan bentuk.
        *   **Mini Project:** Integrasi pengetahuan dari modul-modul sebelumnya dalam sebuah proyek kecil untuk menyelesaikan permasalahan pengolahan citra secara komprehensif.

        **Selamat Belajar! 🚀**
        """)
        return

    modul_aktif = MASTER_LAB_REGISTRY.get(pilihan_materi, {}).get(pilihan_sub)
    if modul_aktif is None:
        st.error("Sub modul tidak ditemukan.")
        return

    try:
        modul_aktif()
        st.session_state.progress_sub[pilihan_materi][pilihan_sub] = True
    except Exception as e:
        st.error(f"Error menjalankan modul:\n\n{e}")
        return

    semua_sub_selesai = all(
        st.session_state.progress_sub.get(pilihan_materi, {}).values()
    )
    if semua_sub_selesai:
        st.session_state.progress_materi[pilihan_materi] = True

    st.markdown("---")
    materi_key = next(
        (
            k
            for k in ["Materi 1", "Materi 2", "Materi 3", "Materi 4", "Materi 5"]
            if k in pilihan_materi
        ),
        None,
    )
    if materi_key:
        st.markdown("## 🎯 Evaluasi Materi")
        passed = st.session_state.get(f"kuis_modul_passed_{materi_key}", False)
        if passed:
            st.success("✅ Kuis modul sudah lulus.")
        else:
            if st.button(f"📝 Kerjakan Kuis {materi_key}", use_container_width=True):
                run_kuis_modul(materi_key)

    # ======================================================
    # FOOTER
    # ======================================================
    st.markdown("---")
    total_materi = len(MASTER_LAB_REGISTRY)
    materi_selesai = sum(1 for v in st.session_state.progress_materi.values() if v)
    progress_total = (
        round(materi_selesai / total_materi * 100, 1) if total_materi > 0 else 0
    )

    st.markdown(
        f"""
    <div style="background:#4a5568; padding:20px; border-radius:12px; border:1px solid #2d3748; margin-top:30px;">
        <h3 style="text-align:center; color: #e2e8f0;">📊 Ringkasan Progress</h3>
        <p style="text-align:center; font-size:18px; color: #e2e8f0;">Materi Selesai: <b>{materi_selesai}/{total_materi}</b></p>
        <p style="text-align:center; font-size:18px; color: #e2e8f0;">Total Progress: <b>{progress_total}%</b></p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.progress(progress_total / 100)

    st.markdown("---")
    st.markdown(
        f"""
    <div style="text-align:center; padding:20px;">
        <h3 style="color: #f6ad55;">🔬 {APP_TITLE}</h3> 
        <p style="color: #e2e8f0;">{APP_SUBTITLE}</p>
        <p style="color: #e2e8f0;"><b>{NAMA_MAHASISWA}</b></p>
        <p style="color: #e2e8f0;">NIM: {NIM_MAHASISWA}</p>
        <p style="color: #e2e8f0;">{PRODI} - {FAKULTAS}</p>
        <p style="color: #e2e8f0;">{UNIVERSITAS}</p>
        <p style="color:gray; font-size:12px;">Built with Python • Streamlit • OpenCV • NumPy • Matplotlib</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    main()

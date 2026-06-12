# 🔬 Digital Image Processing Lab

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=22&duration=4000&pause=1000&color=4A0E4E&center=true&vCenter=true&width=700&lines=Aplikasi+Praktikum+Mandiri;Pengolahan+Citra+Digital;Universitas+Nusa+Mandiri;NIM+14250035" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-Latest-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-Latest-11557C?style=for-the-badge&logo=python&logoColor=white" />
  <br>
  <img src="https://img.shields.io/badge/Mahasiswa-Ismail_Pamudji-1E5631?style=for-the-badge" />
  <img src="https://img.shields.io/badge/NIM-14250035-4A0E4E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>

---

## 📖 Deskripsi

**Digital Image Processing Lab** adalah aplikasi praktikum mandiri berbasis web yang dirancang untuk membantu mahasiswa memahami konsep pengolahan citra digital secara interaktif. Aplikasi ini mengimplementasikan berbagai algoritma pengolahan citra dari buku referensi *"Digital Image Processing"* oleh **Rafael C. Gonzalez & Richard E. Woods**.

Aplikasi ini dikembangkan sebagai tugas akhir mata kuliah **Pengolahan Citra Digital** di **Universitas Nusa Mandiri**, dengan fokus pada implementasi praktis dari teori-teori pengolahan citra menggunakan Python, OpenCV, dan Streamlit.

---

## ✨ Fitur Utama

### 🎯 Sistem Pembelajaran Interaktif

- ✅ **Splash Screen** dengan animasi fade-in yang elegan
- ✅ **4 Materi Utama** dengan penjelasan teoretis lengkap
- ✅ **15 Sub-Modul Eksperimen** yang dapat dijalankan langsung
- ✅ **Progress Tracking** untuk memantau perkembangan belajar
- ✅ **Sequential Unlock** — materi terbuka berurutan
- ✅ **Quiz Gate System** — harus lulus kuis per-modul (≥3/4 benar) untuk lanjut

### 📚 Materi yang Tersedia

| No | Materi | Sub-Modul | Isi |
|----|--------|-----------|-----|
| 1 | 📷 **Elemen & Operasi Piksel** | 4 modul | Image Viewer, Mach Band, Spatial Resolution, Quantization |
| 2 | 🎨 **Transformasi & Operasi Citra** | 7 modul | Gamma Correction, Histogram Eq (CLAHE), Contrast Stretching, Logic Ops, Subtraction (DSA), Averaging, Spatial Filtering |
| 3 | 🌊 **Filtering Spasial & Frekuensi** | 2 modul | FFT Analysis & DC Component, Frequency Domain Filters (Ideal / Butterworth / Gaussian) |
| 4 | 🧬 **Analisis Sidik Jari** | 2 modul | Fingerprint Processing & Minutiae Extraction, Fingerprint Fraud Detection (SIFT) |

### 🎓 Sistem Evaluasi

- 📝 **Kuis Per-Modul** — 4 soal per materi, minimal **3 benar** untuk lanjut (built-in di `modules/__init__.py`)
- 📝 **Kuis Akhir** — **41 soal** komprehensif dari semua materi (`modules/kuis_akhir.py`)
- 🏆 **Sertifikat Kompetensi** — otomatis digenerate dari `data/template_cert.html` setelah lulus kuis akhir (≥75%)
- 🗄️ **Database Sertifikat** — tersimpan di `data/sertifikat_db.json`

---

## 🛠️ Tech Stack

| Layer | Library |
|-------|---------|
| **Web App** | Streamlit ≥1.28 |
| **Image Processing** | OpenCV ≥4.8, scikit-image |
| **Numerik** | NumPy, SciPy |
| **Visualisasi** | Matplotlib |
| **Utilitas** | Pillow (PIL) |

---

## 📦 Instalasi

```bash
# 1. Clone repository
git clone https://github.com/ismail212-web/dip-app.git
cd dip-app

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Buka browser di `http://localhost:8501`

> ⚠️ Pastikan file `Pelajaran.png` ada di folder root (sejajar dengan `app.py`) untuk splash screen.

---

## 📂 Struktur Project Lengkap

```
dip-app/
│
├── app.py                              ← Entry point utama (routing 3 halaman)
├── requirements.txt                    ← Dependencies
├── README.md                           ← Dokumentasi
├── Pelajaran.png                       ← Cover image splash screen (WAJIB ADA)
│
├── modules/                            ← Semua modul praktikum
│   ├── __init__.py                     ← ★ MASTER REGISTRY + kuis_modul + shim
│   │                                      berisi: MASTER_LAB_REGISTRY,
│   │                                              _QUESTION_BANK (16 soal),
│   │                                              run_kuis_modul()
│   ├── kuis_akhir.py                   ← Kuis akhir 41 soal + sertifikat
│   │
│   ├── tugas1/                         ← Materi 1: Elemen & Operasi Piksel
│   │   ├── __init__.py                 ← EXPERIMEN_TUGAS1 (4 sub-modul)
│   │   ├── image_viewer.py
│   │   ├── mach_band.py
│   │   ├── spatial_resolution.py
│   │   └── quantization.py
│   │
│   ├── tugas2/                         ← Materi 2: Transformasi & Operasi Citra
│   │   ├── __init__.py                 ← EXPERIMEN_TUGAS2 (7 sub-modul)
│   │   ├── gamma_correction.py
│   │   ├── histogram_eq.py
│   │   ├── contrast_stretching.py
│   │   ├── logic_operations.py
│   │   ├── image_subtraction.py
│   │   ├── image_averaging.py
│   │   └── spatial_filtering.py
│   │
│   ├── tugas_fft/                      ← Materi 3: Filtering Spasial & Frekuensi
│   │   ├── __init__.py                 ← EXPERIMEN_FFT (2 sub-modul)
│   │   ├── fft_analysis.py             ← 2D FFT & DC Component Removal
│   │   └── frequency_filters.py        ← Ideal / Butterworth / Gaussian Filter
│   │
│   └── tugas_fp/                       ← Materi 4: Analisis Sidik Jari
│       ├── __init__.py                 ← EXPERIMEN_FP (2 sub-modul)
│       ├── fingerprint.py              ← CLAHE, Otsu, Thinning, Minutiae
│       └── fingerprint_fraud.py        ← SIFT + FLANN + Lowe's Ratio Test
│
├── data/                               ← Data persisten
│   ├── template_cert.html              ← Template HTML sertifikat (WAJIB ADA)
│   └── sertifikat_db.json              ← Database peserta (auto-create)
│
├── utils/                              ← Fungsi utilitas bersama
│   ├── __init__.py
│   └── image_utils.py                  ← show_image_centered()
│
└── assets/                             ← Aset statis tambahan
```

---

## 🔗 Diagram Koneksi Antar File

```
app.py
 │
 ├── from modules import MASTER_LAB_REGISTRY
 │       └── modules/__init__.py
 │               ├── MASTER_LAB_REGISTRY ──────────────────────────────┐
 │               ├── run_kuis_modul()  [shim → sys.modules]            │
 │               ├── from .tugas1    → EXPERIMEN_TUGAS1 (4 fungsi)     │
 │               ├── from .tugas2    → EXPERIMEN_TUGAS2 (7 fungsi)     │
 │               ├── from .tugas_fft → EXPERIMEN_FFT   (2 fungsi)      │
 │               └── from .tugas_fp  → EXPERIMEN_FP    (2 fungsi)      │
 │                                                                      │
 ├── from modules.kuis_akhir import run  ──→ kuis_akhir.py             │
 │       └── data/template_cert.html                                   │
 │       └── data/sertifikat_db.json                                   │
 │                                                                      │
 └── MASTER_LAB_REGISTRY[materi][sub]()  ◀──────────────────────────── ┘
         dipanggil saat user memilih sub-modul di sidebar

Setiap sub-modul (*.py) mengimpor:
  from utils import show_image_centered   ← utils/image_utils.py
```

---

## 🚀 Alur Penggunaan

```
[Splash Screen]
   │  klik "🚀 Buka Aplikasi"
   ▼
[Dashboard] ── Sidebar: Materi (🔒/🔓/✅) + Sub-Modul + Progress Bar
   │
   ├── Pilih Sub-Modul → jalankan fungsi dari MASTER_LAB_REGISTRY
   │       └── navigasi ⬅️ Previous / ✅ Done & Next ➡️
   │
   └── Sub-Modul Terakhir → 📝 Kuis Per-Modul (4 soal, min 3 benar)
           │  LULUS
           ▼
       [Materi Berikutnya] atau [Kuis Akhir jika materi terakhir]
               │  skor ≥ 75% dari 41 soal
               ▼
           [🏆 Sertifikat HTML digenerate + disimpan ke DB]
```

---

## 📊 Algoritma yang Diimplementasikan

### Materi 1
- Konversi Grayscale: `0.299R + 0.587G + 0.114B` (ITU-R BT.601)
- Mach Band & Lateral Inhibition
- Spatial Downsampling (efek pixelation)
- Kuantisasi & False Contouring

### Materi 2
- Gamma Correction: `s = c · r^γ`
- Histogram Equalization Global + CLAHE (Clip Limit Adaptive)
- Contrast Stretching dengan percentile
- Logic Operations: AND, OR, NOT, XOR
- Image Subtraction (prinsip DSA)
- Image Averaging: SNR meningkat √N
- Spatial Filtering: Gaussian, Median, Laplacian, Unsharp Masking

### Materi 3
- 2D FFT: `np.fft.fft2()` + `np.fft.fftshift()`
- DC Component Removal (zero area 3×3 di pusat spektrum)
- Ideal Filter, Butterworth Filter `H = 1/(1+(D/D0)^2n)`, Gaussian Filter `H = exp(-D²/2D0²)`
- Inverse FFT untuk rekonstruksi citra

### Materi 4
- CLAHE → Otsu Binarization → Morphological Cleaning → Zhang-Suen Thinning
- Crossing Number untuk ekstraksi Minutiae (Ridge Ending CN=1, Bifurcation CN=3)
- SIFT + FLANN Matcher + Lowe's Ratio Test untuk fraud detection

---

## 🎓 Referensi Akademik

- 📖 **Gonzalez & Woods** (2018). *Digital Image Processing*, 4th Ed. Pearson.
- 📄 **Zhang & Suen** (1984). A fast parallel algorithm for thinning digital patterns. *ACM*.
- 📄 **Lowe** (2004). Distinctive Image Features from Scale-Invariant Keypoints. *IJCV*.
- 📄 **Otsu** (1979). A threshold selection method from gray-level histograms. *IEEE Trans. SMC*.

---

## 👨‍💻 Penulis

| | |
|---|---|
| **Nama** | Ismail Pamudji |
| **NIM** | 14250035 |
| **Program** | S2 Ilmu Komputer |
| **Institusi** | Universitas Nusa Mandiri |
| **GitHub** | [@ismail212-web](https://github.com/ismail212-web) |
| **LinkedIn** | [Ismail Pamudji](https://www.linkedin.com/in/ismail-pamudji-503540214) |

---

## 📜 Lisensi

MIT License — Copyright © 2026 Ismail Pamudji — Universitas Nusa Mandiri

---

<div align="center">

**Made with ❤️ & ☕ by Ismail Pamudji — Universitas Nusa Mandiri © 2026**

[![Share on WhatsApp](https://img.shields.io/badge/Share_on-WhatsApp-25D366?style=for-the-badge&logo=whatsapp)](https://wa.me/?text=Aplikasi%20DIP%20Lab%20🔬%20https://github.com/ismail212-web/dip-app)
[![Share on LinkedIn](https://img.shields.io/badge/Share_on-LinkedIn-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/ismail212-web/dip-app)

</div>

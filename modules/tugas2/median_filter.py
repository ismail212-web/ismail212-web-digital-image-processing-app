# modules/tugas2/median_filter.py
import streamlit as st
import cv2
import numpy as np
from pathlib import Path


def add_salt_pepper(img, amount=0.05):
    """Tambah noise salt & pepper seperti buku"""
    noisy = img.copy()
    h, w = img.shape
    num_salt = int(amount * h * w * 0.5)
    num_pepper = int(amount * h * w * 0.5)

    # salt (putih)
    coords = [np.random.randint(0, i - 1, num_salt) for i in (h, w)]
    noisy[coords[0], coords[1]] = 255

    # pepper (hitam)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in (h, w)]
    noisy[coords[0], coords[1]] = 0
    return noisy


def run():
    st.markdown("### 🔧 Materi 2 — Sub-Modul 9: Order-Statistic Filters (FIGURE 3.37)")

    # --- path assets ---
    here = Path(__file__).resolve()
    base = here.parents[2] / "assets"
    if not base.exists():
        base = here.parents[1] / "assets"

    fig_path = base / "order_statistic_median_figure.png"

    # --- tampilkan gambar buku ---
    if fig_path.exists():
        st.image(
            str(fig_path),
            caption="FIGURE 3.37 — Median vs Averaging untuk salt-and-pepper",
            width="stretch",
        )
    else:
        st.warning("Simpan order_statistic_median_figure.png di assets/")

    with st.expander("📘 Proses FIGURE 3.37", expanded=True):
        st.markdown("""
**(a) → (b) → (c)**
1. **(a) Original + salt & pepper noise** — X-ray circuit board kena bintik hitam-putih
2. **(b) Averaging 3×3** — noise berkurang tapi masih buram, bintik masih kelihatan
3. **(c) Median 3×3** — noise HILANG TOTAL, tepi tetap tajam!

**Kenapa median menang?** Averaging rata-rata semua piksel (bintik ikut kehitung). Median ambil nilai tengah — bintik ekstrem langsung dibuang.

**Kegunaan nyata:** bersihkan foto lama, X-ray medis, CCTV malam hari.
        """)

    st.divider()

    # --- upload ---
    up = st.file_uploader(
        "Upload gambar circuit/X-ray (atau pakai contoh)",
        type=["png", "jpg", "jpeg", "tif", "tiff"],
        key="median_up",
    )

    if up:
        img = cv2.imdecode(np.frombuffer(up.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    else:
        # buat contoh circuit sederhana kalau belum upload
        img = np.ones((400, 400), dtype=np.uint8) * 180
        cv2.rectangle(img, (50, 50), (350, 350), 100, -1)
        cv2.rectangle(img, (150, 150), (300, 300), 50, 3)
        st.info("Upload gambar (a) untuk hasil real — ini hanya contoh")

    img = cv2.resize(img, (400, 400))

    # --- kontrol ---
    col1, col2 = st.columns(2)
    with col1:
        noise = st.slider("Jumlah salt & pepper (a)", 0.01, 0.2, 0.05, step=0.01)
    with col2:
        ksize = st.slider("Ukuran kernel (b & c)", 3, 9, 3, step=2)

    # --- proses (a) ---
    noisy = add_salt_pepper(img, noise)

    # --- proses (b) averaging ---
    blur = cv2.blur(noisy, (ksize, ksize))

    # --- proses (c) median ---
    median = cv2.medianBlur(noisy, ksize)

    # --- tampil 1 layar 3 kolom ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(
            noisy, caption=f"(a) + noise {noise*100:.0f}%", width="stretch"
        )
    with c2:
        st.image(
            blur, caption=f"(b) Averaging {ksize}×{ksize}", width="stretch"
        )
    with c3:
        st.image(
            median, caption=f"(c) Median {ksize}×{ksize}", width="stretch"
        )

    st.success("💡 Perhatikan: median bersihkan bintik tanpa blur tepi!")

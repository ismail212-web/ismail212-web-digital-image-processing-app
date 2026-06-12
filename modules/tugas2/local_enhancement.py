# modules/tugas2/local_enhancement.py
import streamlit as st, cv2, numpy as np, os


def show_book(path, caption=""):
    if os.path.exists(path):
        st.image(path, caption=f"Gambar Buku (tidak diubah) — {caption}")


def he_local(i):
    return cv2.createCLAHE(2.0, (7, 7)).apply(i)


def stat(i, k0, k1, k2, E):
    f = i.astype(np.float32)
    MG, DG = f.mean(), f.std()
    m = cv2.blur(f, (3, 3))
    s = np.sqrt(np.maximum(cv2.blur(f * f, (3, 3)) - m * m, 0))
    mk = (m <= k0 * MG) & (s >= k1 * DG) & (s <= k2 * DG)
    o = f.copy()
    o[mk] *= E
    return (
        np.clip(o, 0, 255).astype(np.uint8),
        s.astype(np.uint8),
        mk.astype(np.uint8) * 255,
    )


def run():
    st.markdown("### 🎨 Materi 2 — Sub-Modul 8: Peningkatan Lokal")
    t1, t2, t3 = st.tabs(["📘 Pengantar", "1️⃣ HE Lokal", "2️⃣ Statistik"])

    with t1:
        st.write("Peningkatan lokal bekerja pada jendela kecil.")
        show_book("assets/contoh_tungsten_before.png", "Tungsten")

    with t2:
        st.markdown("**HE Lokal - Contoh Buku**")
        st.image(
            "assets/contoh_local_hist.png", caption="Buku: Asli | HE Global | HE Lokal"
        )

        up = st.file_uploader(
            "Unggah gambar", type=["png", "jpg", "jpeg", "tif", "tiff"], key="h"
        )
        if up:
            im = cv2.imdecode(np.frombuffer(up.read(), np.uint8), 0)
            g = cv2.equalizeHist(im)
            l = he_local(im)
            st.markdown("#### Hasil Upload Kamu")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("1. Asli")
                st.image(im, width=200)
            with c2:
                st.write("2. HE Global")
                st.image(g, width=200)
            with c3:
                st.write("3. HE Lokal")
                st.image(l, width=200)

    with t3:
        st.markdown("**Statistik - Contoh Buku**")
        show_book("assets/contoh_local_stat_rumus.png", "Rumus")
        show_book("assets/contoh_tungsten_after.png", "Hasil")

        up2 = st.file_uploader(
            "Unggah SEM", type=["png", "jpg", "jpeg", "tif", "tiff"], key="s"
        )
        k0 = st.slider("k0", 0.1, 1.0, 0.4, 0.05)
        k1 = st.slider("k1", 0.0, 0.2, 0.02, 0.01)
        k2 = st.slider("k2", 0.1, 1.0, 0.4, 0.05)
        E = st.slider("E", 1.0, 6.0, 4.0, 0.5)
        if up2:
            im = cv2.imdecode(np.frombuffer(up2.read(), np.uint8), 0)
            o, v, m = stat(im, k0, k1, k2, E)
            st.markdown("#### Hasil Upload Kamu")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.write("1. Asli")
                st.image(im, width=200)
            with c2:
                st.write("2. Variance")
                st.image(v, width=200)
            with c3:
                st.write("3. Mask")
                st.image(m, width=200)
            with c4:
                st.write("4. Hasil")
                st.image(o, width=200)

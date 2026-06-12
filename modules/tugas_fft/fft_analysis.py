# modules/tugas_fft/fft_analysis.py

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def run():

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown("## ⚙ Materi 3 : Filtering Frekuensi — FFT Analysis & DC Component")

    st.markdown("---")

    # =====================================================
    # CONTOH PDF
    # =====================================================
    st.markdown("### 📘 Contoh Soal dari PDF")

    here = Path(__file__).resolve()

    assets = here.parents[2] / "assets"

    if not assets.exists():
        assets = here.parents[1] / "assets"

    soal1 = assets / "soal1_fft.png"
    soal2 = assets / "soal2_dc.png"

    tab1, tab2 = st.tabs(
        [
            "📊 Soal 1 - FFT Shift",
            "⚡ Soal 2 - DC Removal",
        ]
    )

    with tab1:

        if soal1.exists():

            st.image(
                str(soal1),
                caption="Original → DFT → FFT Shift",
                use_container_width=True,
            )

        else:

            st.warning("File soal1_fft.png tidak ditemukan")

    with tab2:

        if soal2.exists():

            st.image(
                str(soal2),
                caption="Set F(0,0)=0",
                use_container_width=True,
            )

        else:

            st.warning("File soal2_dc.png tidak ditemukan")

    with st.expander("📖 Penjelasan"):

        st.markdown("""
### Soal 1

Transformasi citra dari domain spasial ke domain frekuensi menggunakan 2D FFT.

Tahapan:

- Original Image
- 2D DFT
- FFT Shift

### Soal 2

Komponen DC merupakan rata-rata intensitas citra.

Dengan mengatur:

F(0,0)=0

maka komponen DC dihilangkan sehingga citra tampak seperti high-pass filtering.
""")

    st.markdown("---")

    # =====================================================
    # UPLOAD
    # =====================================================
    uploaded_file = st.file_uploader(
        "Upload Image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "bmp",
            "tif",
            "tiff",
        ],
    )

    if uploaded_file is None:

        st.info("⬆️ Upload gambar untuk memulai eksperimen FFT")

        return

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8,
    )

    img_bgr = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR,
    )

    if img_bgr is None:

        st.error("Gagal membaca gambar")

        return

    img_gray = cv2.cvtColor(
        img_bgr,
        cv2.COLOR_BGR2GRAY,
    )

    rows, cols = img_gray.shape

    # =====================================================
    # INFO IMAGE
    # =====================================================
    st.markdown("### 📏 Informasi Citra")

    st.info(f"""
Ukuran : {rows} x {cols}

Mean : {np.mean(img_gray):.2f}

Std : {np.std(img_gray):.2f}
""")

    # =====================================================
    # FFT
    # =====================================================
    f_transform = np.fft.fft2(img_gray)

    magnitude_dft = 20 * np.log(np.abs(f_transform) + 1)

    f_shift = np.fft.fftshift(f_transform)

    magnitude_shift = 20 * np.log(np.abs(f_shift) + 1)

    # =====================================================
    # NORMALISASI DISPLAY
    # =====================================================
    dft_view = cv2.normalize(
        magnitude_dft,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    ).astype(np.uint8)

    shift_view = cv2.normalize(
        magnitude_shift,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    ).astype(np.uint8)

    # =====================================================
    # SOAL 1
    # =====================================================
    st.markdown("## 📊 Soal 1 : FFT Analysis")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.image(
            img_gray,
            caption="Original Image",
            use_container_width=True,
        )

    with c2:

        st.image(
            dft_view,
            caption="2D DFT",
            use_container_width=True,
        )

    with c3:

        st.image(
            shift_view,
            caption="2D FFT Shift",
            use_container_width=True,
        )

    # =====================================================
    # STATISTIK FFT
    # =====================================================
    st.markdown("### 📈 Statistik FFT")

    crow = rows // 2
    ccol = cols // 2

    dc_component = np.abs(
        f_shift[
            crow,
            ccol,
        ]
    )

    total_energy = np.sum(np.abs(f_shift) ** 2)

    dc_ratio = (dc_component**2 / total_energy) * 100

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "DC Component",
            f"{dc_component:,.0f}",
        )

    with m2:

        st.metric(
            "Total Energy",
            f"{total_energy:.2e}",
        )

    with m3:

        st.metric(
            "DC Ratio %",
            f"{dc_ratio:.2f}",
        )

    # =====================================================
    # PROFILE SPECTRUM
    # =====================================================
    st.markdown("### 📉 Spectrum Profile")

    fig, ax = plt.subplots(
        1,
        2,
        figsize=(12, 4),
    )

    im = ax[0].imshow(
        magnitude_shift,
        cmap="inferno",
    )

    ax[0].set_title("Magnitude Spectrum")

    plt.colorbar(
        im,
        ax=ax[0],
    )

    ax[1].plot(
        magnitude_shift[crow, :],
        label="Horizontal",
    )

    ax[1].plot(
        magnitude_shift[:, ccol],
        "--",
        label="Vertical",
    )

    ax[1].legend()

    ax[1].grid(True)

    ax[1].set_title("Spectrum Profile")

    plt.tight_layout()

    st.pyplot(fig)

    # =====================================================
    # SOAL 2
    # =====================================================
    st.markdown("## ⚡ Soal 2 : DC Component Removal")

    remove_dc = st.checkbox("Set F(0,0)=0")

    if remove_dc:

        f_shift_dc = f_shift.copy()

        # hapus DC
        f_shift_dc[
            crow,
            ccol,
        ] = 0

        magnitude_dc = 20 * np.log(np.abs(f_shift_dc) + 1)

        f_ishift = np.fft.ifftshift(f_shift_dc)

        img_back = np.real(np.fft.ifft2(f_ishift))

        img_back = cv2.normalize(
            img_back,
            None,
            0,
            255,
            cv2.NORM_MINMAX,
        ).astype(np.uint8)

    else:

        magnitude_dc = magnitude_shift

        img_back = img_gray.copy()

    dc_view = cv2.normalize(
        magnitude_dc,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    ).astype(np.uint8)

    c1, c2, c3 = st.columns(3)

    with c1:

        st.image(
            img_gray,
            caption="Original",
            use_container_width=True,
        )

    with c2:

        st.image(
            dc_view,
            caption="Set F(0,0)=0",
            use_container_width=True,
        )

    with c3:

        st.image(
            img_back,
            caption="Result",
            use_container_width=True,
        )

    # =====================================================
    # DOWNLOAD
    # =====================================================
    st.markdown("## 💾 Download")

    success, buffer = cv2.imencode(
        ".png",
        img_back,
    )

    if success:

        filename = "fft_dc_removed.png" if remove_dc else "fft_original.png"

        st.download_button(
            "⬇ Download Hasil",
            buffer.tobytes(),
            file_name=filename,
            mime="image/png",
        )

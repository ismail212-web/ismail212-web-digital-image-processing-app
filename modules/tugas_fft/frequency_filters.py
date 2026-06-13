# modules/tugas_fft/frequency_filters.py

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================================
# FFT UTILITIES
# ==========================================================


def compute_2d_fft(img_gray):
    """
    Forward FFT dan FFT Shift
    """

    dft = np.fft.fft2(img_gray)

    dft_shift = np.fft.fftshift(dft)

    magnitude = 20 * np.log(np.abs(dft_shift) + 1)

    magnitude_norm = cv2.normalize(
        magnitude,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    ).astype(np.uint8)

    return (
        dft,
        dft_shift,
        magnitude,
        magnitude_norm,
    )


def apply_inverse_fft(dft_shift):
    """
    Inverse FFT
    """

    f_ishift = np.fft.ifftshift(dft_shift)

    img_back = np.fft.ifft2(f_ishift)

    img_back = np.abs(img_back)

    img_back = cv2.normalize(
        img_back,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    )

    return img_back.astype(np.uint8)


# ==========================================================
# FILTER MASKS
# ==========================================================


def generate_filter_mask(
    shape,
    cutoff,
    filter_type,
    mode="lowpass",
    order=2,
):
    """
    Ideal
    Butterworth
    Gaussian
    """

    rows, cols = shape

    crow = rows // 2
    ccol = cols // 2

    u = np.arange(rows)
    v = np.arange(cols)

    U, V = np.meshgrid(
        u,
        v,
        indexing="ij",
    )

    D = np.sqrt((U - crow) ** 2 + (V - ccol) ** 2)

    # --------------------------------

    if filter_type == "Ideal":

        H = np.zeros(
            (rows, cols),
            dtype=np.float32,
        )

        H[D <= cutoff] = 1

    elif filter_type == "Butterworth":

        H = 1 / (1 + (D / (cutoff + 1e-6)) ** (2 * order))

    elif filter_type == "Gaussian":

        H = np.exp(-(D**2) / (2 * (cutoff**2 + 1e-6)))

    else:

        H = np.ones(
            (rows, cols),
            dtype=np.float32,
        )

    # --------------------------------

    if mode == "highpass":

        H = 1 - H

    return H


# ==========================================================
# QUALITY METRICS
# ==========================================================


def calculate_mse(
    img1,
    img2,
):
    return np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)


def calculate_psnr(
    img1,
    img2,
):

    mse = calculate_mse(
        img1,
        img2,
    )

    if mse == 0:
        return 99.0

    return 20 * np.log10(255.0 / np.sqrt(mse))


# ==========================================================
# LOAD ASSETS
# ==========================================================


def load_assets():

    here = Path(__file__).resolve()

    assets = here.parents[2] / "assets"

    if not assets.exists():

        assets = here.parents[1] / "assets"

    return {
        "soal3": assets / "soal3_lpf.png",
        "soal4": assets / "soal4_hpf.png",
        "soal5": assets / "soal5_combined.png",
        "pattern": assets / "characters_test_pattern.tif",
    }


# ==========================================================
# MAIN APP
# ==========================================================


def run():

    st.markdown("### ⚙ Materi 3: Filtering Frekuensi")

    st.write(
        "**Sub-Modul:** " "Frequency Domain Filters " "(Ideal, Butterworth, Gaussian)"
    )

    st.caption("Referensi: Gonzalez & Woods")

    st.markdown("---")

    asset = load_assets()

    pilihan_eksperimen = st.selectbox(
        "🔬 Pilih Eksperimen",
        [
            "3. Lowpass Filters",
            "4. Highpass Filters",
            "5. LPF vs HPF",
        ],
    )

    # =====================================
    # PREVIEW PDF
    # =====================================

    if pilihan_eksperimen == "3. Lowpass Filters":

        if asset["soal3"].exists():

            st.image(
                str(asset["soal3"]),
                width="stretch",
            )

    elif pilihan_eksperimen == "4. Highpass Filters":

        if asset["soal4"].exists():

            st.image(
                str(asset["soal4"]),
                width="stretch",
            )

    else:

        if asset["soal5"].exists():

            st.image(
                str(asset["soal5"]),
                width="stretch",
            )

    st.markdown("---")

    # =====================================
    # INPUT IMAGE
    # =====================================

    use_sample = st.checkbox("Gunakan gambar contoh PDF")

    uploaded_file = st.file_uploader(
        "Unggah Citra",
        type=[
            "png",
            "jpg",
            "jpeg",
            "tif",
            "tiff",
        ],
    )

    img_gray = None

    if use_sample and asset["pattern"].exists():

        img_gray = cv2.imread(
            str(asset["pattern"]),
            cv2.IMREAD_GRAYSCALE,
        )

    elif uploaded_file is not None:

        file_bytes = np.asarray(
            bytearray(uploaded_file.read()),
            dtype=np.uint8,
        )

        img_src = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR,
        )

        img_gray = cv2.cvtColor(
            img_src,
            cv2.COLOR_BGR2GRAY,
        )

    if img_gray is None:

        st.info("⬆️ Upload gambar " "atau gunakan " "gambar contoh PDF")

        return

    rows, cols = img_gray.shape

    st.image(
        img_gray,
        caption="Input Image",
        width="stretch",
    )

    st.info(f"""
Ukuran : {rows} x {cols}

Mean : {np.mean(img_gray):.2f}

Std : {np.std(img_gray):.2f}
""")

    (
        dft,
        dft_shift,
        magnitude,
        magnitude_norm,
    ) = compute_2d_fft(img_gray)

    # ==========================
    # PART 2
    # ==========================
    # =====================================
    # PARAMETER FILTER
    # =====================================

    cutoff = st.slider(
        "Cutoff Frequency (D0)",
        min_value=5,
        max_value=150,
        value=40,
    )

    order = st.slider(
        "Butterworth Order (n)",
        min_value=1,
        max_value=10,
        value=2,
    )

    crow = rows // 2
    ccol = cols // 2

    # =====================================
    # LOWPASS FILTERS
    # =====================================

    if pilihan_eksperimen == "3. Lowpass Filters":

        st.markdown("## 📘 Soal 3 : Lowpass Filters")

        H_ilp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Ideal",
            "lowpass",
        )

        H_blp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Butterworth",
            "lowpass",
            order,
        )

        H_glp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Gaussian",
            "lowpass",
        )

        res_ilp = apply_inverse_fft(dft_shift * H_ilp)

        res_blp = apply_inverse_fft(dft_shift * H_blp)

        res_glp = apply_inverse_fft(dft_shift * H_glp)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.image(
                img_gray,
                caption="Original",
                width="stretch",
            )

        with c2:
            st.image(
                res_ilp,
                caption="Ideal LPF",
                width="stretch",
            )

        with c3:
            st.image(
                res_blp,
                caption=f"Butterworth LPF (n={order})",
                width="stretch",
            )

        with c4:
            st.image(
                res_glp,
                caption="Gaussian LPF",
                width="stretch",
            )

        st.markdown("### 📈 Evaluasi Lowpass")

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "Ideal MSE",
                f"{calculate_mse(img_gray, res_ilp):.2f}",
            )

            st.metric(
                "Ideal PSNR",
                f"{calculate_psnr(img_gray, res_ilp):.2f}",
            )

        with m2:

            st.metric(
                "Butterworth MSE",
                f"{calculate_mse(img_gray, res_blp):.2f}",
            )

            st.metric(
                "Butterworth PSNR",
                f"{calculate_psnr(img_gray, res_blp):.2f}",
            )

        with m3:

            st.metric(
                "Gaussian MSE",
                f"{calculate_mse(img_gray, res_glp):.2f}",
            )

            st.metric(
                "Gaussian PSNR",
                f"{calculate_psnr(img_gray, res_glp):.2f}",
            )

        st.markdown("### 📊 Spectrum")

        fig, ax = plt.subplots(
            1,
            3,
            figsize=(12, 4),
        )

        ax[0].imshow(
            H_ilp,
            cmap="gray",
        )

        ax[0].set_title("Ideal LPF Mask")

        ax[1].imshow(
            H_blp,
            cmap="gray",
        )

        ax[1].set_title("Butterworth LPF")

        ax[2].imshow(
            H_glp,
            cmap="gray",
        )

        ax[2].set_title("Gaussian LPF")

        st.pyplot(fig)

    # =====================================
    # HIGHPASS FILTERS
    # =====================================

    elif pilihan_eksperimen == "4. Highpass Filters":

        st.markdown("## 📘 Soal 4 : Highpass Filters")

        H_ihp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Ideal",
            "highpass",
        )

        H_bhp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Butterworth",
            "highpass",
            order,
        )

        H_ghp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Gaussian",
            "highpass",
        )

        res_ihp = apply_inverse_fft(dft_shift * H_ihp)

        res_bhp = apply_inverse_fft(dft_shift * H_bhp)

        res_ghp = apply_inverse_fft(dft_shift * H_ghp)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.image(
                img_gray,
                caption="Original",
                width="stretch",
            )

        with c2:
            st.image(
                res_ihp,
                caption="Ideal HPF",
                width="stretch",
            )

        with c3:
            st.image(
                res_bhp,
                caption=f"Butterworth HPF (n={order})",
                width="stretch",
            )

        with c4:
            st.image(
                res_ghp,
                caption="Gaussian HPF",
                width="stretch",
            )

        st.markdown("### 📈 Evaluasi Highpass")

        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric(
                "Ideal MSE",
                f"{calculate_mse(img_gray, res_ihp):.2f}",
            )

        with m2:
            st.metric(
                "Butterworth MSE",
                f"{calculate_mse(img_gray, res_bhp):.2f}",
            )

        with m3:
            st.metric(
                "Gaussian MSE",
                f"{calculate_mse(img_gray, res_ghp):.2f}",
            )

    # ==========================
    # PART 3
    # ==========================
    # =====================================
    # SOAL 5
    # LPF VS HPF
    # =====================================

    else:

        st.markdown("## 📘 Soal 5 : LPF vs HPF")

        H_glp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Gaussian",
            "lowpass",
        )

        H_ghp = generate_filter_mask(
            (rows, cols),
            cutoff,
            "Gaussian",
            "highpass",
        )

        out_lp = apply_inverse_fft(dft_shift * H_glp)

        out_hp = apply_inverse_fft(dft_shift * H_ghp)

        c1, c2, c3 = st.columns(3)

        with c1:

            st.image(
                img_gray,
                caption="Original",
                width="stretch",
            )

        with c2:

            st.image(
                out_lp,
                caption=f"Gaussian LPF (D0={cutoff})",
                width="stretch",
            )

        with c3:

            st.image(
                out_hp,
                caption=f"Gaussian HPF (D0={cutoff})",
                width="stretch",
            )

        st.markdown("### 📈 Perbandingan Kualitas")

        m1, m2 = st.columns(2)

        with m1:

            st.metric(
                "LPF MSE",
                f"{calculate_mse(img_gray, out_lp):.2f}",
            )

            st.metric(
                "LPF PSNR",
                f"{calculate_psnr(img_gray, out_lp):.2f}",
            )

        with m2:

            st.metric(
                "HPF MSE",
                f"{calculate_mse(img_gray, out_hp):.2f}",
            )

            st.metric(
                "HPF PSNR",
                f"{calculate_psnr(img_gray, out_hp):.2f}",
            )

        st.markdown("### 📊 Transfer Function")

        fig, ax = plt.subplots(
            1,
            2,
            figsize=(10, 4),
        )

        ax[0].imshow(
            H_glp,
            cmap="gray",
        )

        ax[0].set_title("Gaussian LPF Mask")

        ax[1].imshow(
            H_ghp,
            cmap="gray",
        )

        ax[1].set_title("Gaussian HPF Mask")

        plt.tight_layout()

        st.pyplot(fig)

        result_download = out_lp

    # =====================================
    # DOWNLOAD
    # =====================================

    st.markdown("---")
    st.markdown("## 💾 Download Hasil")

    if pilihan_eksperimen == "3. Lowpass Filters":

        result_download = res_glp

    elif pilihan_eksperimen == "4. Highpass Filters":

        result_download = res_ghp

    success, buffer = cv2.imencode(
        ".png",
        result_download,
    )

    if success:

        filename = (
            pilihan_eksperimen.lower().replace(" ", "_").replace(".", "") + ".png"
        )

        st.download_button(
            "⬇ Download Result",
            buffer.tobytes(),
            file_name=filename,
            mime="image/png",
        )

    # =====================================
    # FFT VISUALIZATION
    # =====================================

    st.markdown("---")
    st.markdown("## 🌊 FFT Visualization")

    fig, ax = plt.subplots(
        1,
        2,
        figsize=(12, 4),
    )

    ax[0].imshow(
        img_gray,
        cmap="gray",
    )

    ax[0].set_title("Original Image")

    ax[0].axis("off")

    ax[1].imshow(
        magnitude_norm,
        cmap="inferno",
    )

    ax[1].set_title("Magnitude Spectrum")

    ax[1].axis("off")

    plt.tight_layout()

    st.pyplot(fig)

    # =====================================
    # FOOTER
    # =====================================

    st.markdown("---")

    st.success(
        "Eksperimen selesai. "
        "Bandingkan pengaruh LPF dan HPF "
        "terhadap karakteristik citra pada domain frekuensi."
    )

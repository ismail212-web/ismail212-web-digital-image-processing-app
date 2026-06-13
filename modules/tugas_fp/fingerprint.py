"""
Modul UI untuk Ekstraksi Minutiae Sidik Jari.
Menggunakan core algorithms dari src/fingerprint/
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image as PILImage
from src.fingerprint.preprocessing import preprocess_fingerprint
from src.fingerprint.thinning import apply_thinning
from src.fingerprint.minutiae import extract_minutiae, draw_minutiae


def load_img_safe(uploaded_file):
    """Baca JPG/PNG/TIF dengan aman, output grayscale uint8"""
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
    st.markdown("## 🔍 Ekstraksi Minutiae Sidik Jari")
    st.caption("Pipeline: CLAHE → Otsu Binarization → Morphology → Thinning → Crossing Number")
    
    uploaded_file = st.file_uploader("Upload Citra Sidik Jari", type=["jpg", "jpeg", "png", "tif", "tiff"])
    
    if uploaded_file is None:
        st.info("Silakan upload citra sidik jari untuk memulai analisis.")
        return

    img = load_img_safe(uploaded_file)
    if img is None:
        return

    with st.spinner("Sedang memproses citra..."):
        # 1. Preprocessing (mengembalikan dict berisi semua tahap)
        prep_result = preprocess_fingerprint(img)
        
        # 2. Thinning
        skeleton = apply_thinning(prep_result["cleaned"])
        
        # 3. Minutiae Extraction
        minutiae = extract_minutiae(skeleton, border_margin=10)
        
        # 4. Visualisasi
        vis_img = draw_minutiae(skeleton, minutiae)
        vis_img_rgb = cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)

    # Tampilan UI (Tetap sama seperti sebelumnya)
    st.markdown("### 📊 Hasil Pemrosesan")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Citra Asli (Grayscale)**")
        st.image(prep_result["original"], width="stretch")
        st.markdown("**Setelah CLAHE**")
        st.image(prep_result["enhanced"], width="stretch")
        
    with col2:
        st.markdown("**Binarization (Otsu)**")
        st.image(prep_result["binary"], width="stretch")
        st.markdown("**Noise Removal (Morphology)**")
        st.image(prep_result["cleaned"], width="stretch")

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Skeleton (Thinning)**")
        st.image(skeleton, width="stretch")
    with col4:
        st.markdown("**Deteksi Minutiae**")
        st.image(vis_img_rgb, width="stretch")
        
    st.success(
        f"✅ Ditemukan: **{len(minutiae['ridge_endings'][0])} Ridge Ending** (🔴) "
        f"dan **{len(minutiae['bifurcations'][0])} Bifurcation** (🟢). "
        f"Total: **{minutiae['total']} titik**."
    )
    
    with st.expander("📝 Penjelasan Algoritma"):
        st.markdown("""
        - **Crossing Number (CN)** dihitung pada matriks tetangga 3x3.
        - **CN = 1**: Ridge Ending (Ujung garis).
        - **CN = 3**: Bifurcation (Percabangan garis).
        - Area tepi (border) diabaikan untuk mencegah deteksi minutiae palsu.
        """)

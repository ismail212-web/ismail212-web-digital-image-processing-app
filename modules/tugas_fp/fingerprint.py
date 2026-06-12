# -*- coding: utf-8 -*-
import streamlit as st
import cv2
import numpy as np
from PIL import Image as PILImage
import tempfile, time, random
from datetime import datetime
from io import BytesIO

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Image as RLImage,
    )
    from reportlab.lib.styles import getSampleStyleSheet

    REPORTLAB_OK = True
except:
    REPORTLAB_OK = False


# ── HELPER ──────────────────────────────────
def load_image(uploaded):
    try:
        img = PILImage.open(uploaded)
        if getattr(img, "n_frames", 1) > 1:
            img.seek(0)
        if img.mode in ("I;16", "I;16B", "I"):
            arr = np.array(img).astype(np.float32)
            arr = (arr / arr.max() * 255).astype(np.uint8)
            return cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)
        return np.array(img.convert("RGB"))
    except Exception as e:
        st.error(f"Gagal baca gambar: {e}")
        return None


def preprocess(img_rgb):
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    enh = cv2.createCLAHE(3.0, (8, 8)).apply(gray)
    blur = cv2.GaussianBlur(enh, (3, 3), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    clean = cv2.morphologyEx(
        cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel), cv2.MORPH_CLOSE, kernel
    )
    return gray, enh, binary, clean


def skeletonize(bin_img):
    try:
        return cv2.ximgproc.thinning(bin_img)
    except:
        skel = np.zeros_like(bin_img)
        el = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        img = bin_img.copy()
        while True:
            open_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, el)
            temp = cv2.subtract(img, open_img)
            eroded = cv2.erode(img, el)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded
            if cv2.countNonZero(img) == 0:
                break
        return skel


def crossing_number(n):
    p = [n[0, 1], n[0, 2], n[1, 2], n[2, 2], n[2, 1], n[2, 0], n[1, 0], n[0, 0]]
    p = [1 if v > 0 else 0 for v in p]
    return sum(abs(p[i] - p[(i + 1) % 8]) for i in range(8)) / 2


def extract_minutiae(skel):
    end, bif = [], []
    s = (skel > 0).astype(np.uint8)
    h, w = s.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if s[y, x]:
                cn = crossing_number(s[y - 1 : y + 2, x - 1 : x + 2])
                if cn == 1:
                    end.append((x, y))
                elif cn == 3:
                    bif.append((x, y))
    return end, bif


def draw_minutiae(gray, end, bif):
    out = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    for x, y in end:
        cv2.circle(out, (x, y), 3, (255, 0, 0), 1)
    for x, y in bif:
        cv2.circle(out, (x, y), 3, (0, 255, 0), 1)
    return out


def analyze_quality(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    bright = np.mean(g)
    cont = np.std(g)
    enh = cv2.createCLAHE(3.0, (8, 8)).apply(g)
    _, bin = cv2.threshold(enh, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ridge = np.count_nonzero(bin) / bin.size * 100
    status = (
        "Baik"
        if 70 < bright < 190 and cont > 35 and 8 < ridge < 45
        else "Perlu perhatian"
    )
    return {"bright": bright, "cont": cont, "ridge": ridge, "status": status}


def save_temp(img):
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    PILImage.fromarray(
        img if len(img.shape) == 3 else cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    ).save(f.name)
    return f.name


def create_forensic_frame(img_left, img_right, points, n_lines):
    h = 400
    w = int(img_left.shape[1] * h / img_left.shape[0])
    left = cv2.resize(img_left, (w, h))
    right = cv2.resize(img_right, (w, h))
    combined = np.hstack([left, right])
    sx = w / img_left.shape[1]
    sy = h / img_left.shape[0]
    for i in range(min(n_lines, len(points))):
        x, y = points[i]
        x1, y1 = int(x * sx), int(y * sy)
        x2, y2 = x1 + w, y1
        cv2.line(combined, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.circle(combined, (x1, y1), 4, (255, 0, 0), -1)
        cv2.circle(combined, (x2, y2), 4, (255, 0, 0), -1)
    return combined


# ── MAIN ────────────────────────────────────
def run():
    st.markdown("## 🧬 [4.1] Fingerprint Recognition")
    st.caption("NIM: 14250035 — Ismail Pamudji")

    up = st.file_uploader(
        "📤 Upload 1 Sidik Jari", type=["jpg", "jpeg", "png", "bmp", "tif", "tiff"]
    )
    if not up:
        st.warning("Silakan upload 1 gambar sidik jari")
        return

    img_rgb = load_image(up)
    if img_rgb is None:
        return

    gray, enh, bin_img, clean = preprocess(img_rgb)
    skel = skeletonize(clean)
    endings, bifs = extract_minutiae(skel)
    minutiae_img = draw_minutiae(gray, endings, bifs)
    quality = analyze_quality(img_rgb)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Status", quality["status"])
    c2.metric("Ending", len(endings))
    c3.metric("Bifurcation", len(bifs))
    c4.metric("Ridge %", f"{quality['ridge']:.1f}")

    # Perbandingan
    st.markdown("### 🔍 Perbandingan Input vs Minutiae")
    left, right = st.columns(2)
    with left:
        st.image(img_rgb, caption="Input Asli", width=320)
    with right:
        st.image(minutiae_img, caption=f"Minutiae", width=320)

    # Animasi CSI
    st.markdown("#### 🔗 Visualisasi Forensik")
    all_points = endings + bifs
    if len(all_points) > 50:
        all_points = random.sample(all_points, 50)

    col1, col2 = st.columns([4, 1])
    with col2:
        play = st.button("▶️ Putar Animasi CSI")
    with col1:
        placeholder = st.empty()

    base = create_forensic_frame(img_rgb, minutiae_img, all_points, 0)
    placeholder.image(base, caption="Siap menganalisa", use_container_width=True)

    if play:
        for i in range(1, len(all_points) + 1):
            frame = create_forensic_frame(img_rgb, minutiae_img, all_points, i)
            placeholder.image(
                frame,
                caption=f"Menganalisa titik {i}/{len(all_points)}",
                use_container_width=True,
            )
            time.sleep(0.07)

    # Pipeline langsung tampil
    st.markdown("### 📊 Tahapan Pipeline")
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        st.image(gray, caption="1. Grayscale", width=210)
    with r1c2:
        st.image(enh, caption="2. CLAHE", width=210)
    with r1c3:
        st.image(bin_img, caption="3. Binary", width=210)
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        st.image(clean, caption="4. Morfologi", width=210)
    with r2c2:
        st.image(skel, caption="5. Thinning", width=210)
    with r2c3:
        st.image(minutiae_img, caption="6. Minutiae", width=210)

    # PDF
    st.divider()
    if st.button("Generate PDF", type="primary"):
        if not REPORTLAB_OK:
            st.error("pip install reportlab")
            return
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story += [
            Paragraph("LAPORAN FINGERPRINT", styles["Title"]),
            Paragraph(
                f"Ismail Pamudji | 14250035 | {datetime.now():%d %B %Y}",
                styles["Normal"],
            ),
            Spacer(1, 12),
        ]
        for name, im in zip(
            ["Original", "Gray", "Enhanced", "Binary", "Clean", "Skeleton", "Minutiae"],
            [img_rgb, gray, enh, bin_img, clean, skel, minutiae_img],
        ):
            tmp = save_temp(im)
            story.append(Paragraph(name, styles["Heading3"]))
            story.append(RLImage(tmp, width=280, height=200))
        doc.build(story)
        buf.seek(0)
        st.download_button(
            "⬇ Download PDF", buf, file_name="Laporan_FP.pdf", mime="application/pdf"
        )

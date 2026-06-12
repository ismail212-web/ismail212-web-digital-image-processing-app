# modules/tugas2/__init__.py
import logging

# Import semua modul Tugas 2
from .gamma_correction import run as run_gamma
from .histogram_eq import run as run_histeq
from .contrast_stretching import run as run_contrast
from .logic_operations import run as run_logic
from .arithmetic_subtraction import run as run_subtract
from .image_averaging import run as run_average
from .spatial_filtering import run as run_spatial
from .local_enhancement import run as run_local
from .smoothing_hubble import run as run_hubble
from .median_filter import run as run_median
from .sobel_gradient import run as run_sobel  # <— MODUL 11 BARU

# Daftar eksperimen yang muncul di sidebar
EXPERIMENT_TUGAS2 = {
    "1. Gamma Correction (Power-Law)": run_gamma,
    "2. Histogram Equalization & CLAHE": run_histeq,
    "3. Contrast Stretching": run_contrast,
    "4. Logic Operations (AND/OR/NOT/XOR)": run_logic,
    "5. Arithmetic Operation: Subtraction": run_subtract,
    "6. Image Averaging (Noise Reduction)": run_average,
    "7. Spatial Filtering (Smooth & Sharpen)": run_spatial,
    "8. Local Enhancement (Local HE & Statistic)": run_local,
    "9. Hubble Smoothing + Thresholding (Fig 3.36)": run_hubble,
    "10. Median Filter (Fig 3.37)": run_median,
    "11. Sobel Gradient (First Order Derivative)": run_sobel,  # <— BARU
}

__all__ = ["EXPERIMENT_TUGAS2"]

logging.getLogger("DIP_Lab").info("✅ Modul Tugas 2 terdaftar (11 eksperimen).")

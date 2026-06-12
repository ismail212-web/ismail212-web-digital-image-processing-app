# modules/tugas1/__init__.py
import logging
from .image_viewer import run as run_image_viewer
from .mach_band import run as run_mach_band
from .spatial_resolution import run as run_spatial_res
from .quantization import run as run_quantization

EXPERIMENT_TUGAS1 = {
    "1. Image Viewer & Operasi Dasar Piksel": run_image_viewer,
    "2. Efek Mach Band & Lateral Inhibition": run_mach_band,
    "3. Spatial Resolution & Downsampling": run_spatial_res,
    "4. Quantization & False Contouring": run_quantization,
}

__all__ = ["EXPERIMENT_TUGAS1"]
logging.getLogger("DIP_Lab").info("✅ Modul Tugas 1 terdaftar.")

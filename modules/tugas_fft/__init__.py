# modules/tugas_fft/__init__.py
import logging

from .fft_analysis import run as run_fft_analysis
from .frequency_filters import run as run_freq_filters

EXPERIMENT_FFT = {
    "1. FFT Analysis & DC Component": run_fft_analysis,
    "2. Frequency Domain Filters (Ideal, Butterworth, Gaussian)": run_freq_filters,
}

__all__ = ["EXPERIMENT_FFT"]

logging.getLogger("DIP_Lab").info("✅ Modul Tugas FFT terdaftar (2 eksperimen).")

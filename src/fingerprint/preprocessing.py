"""
Modul preprocessing sidik jari.
Berisi fungsi-fungsi murni untuk enhancement, binarisasi, dan pembersihan noise.
"""
import cv2
import numpy as np


def apply_clahe(img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)) -> np.ndarray:
    """
    Meningkatkan kontras lokal citra menggunakan CLAHE.
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(img)


def apply_otsu_binarization(img: np.ndarray) -> np.ndarray:
    """
    Mengubah citra grayscale menjadi biner menggunakan Otsu's Thresholding.
    Menggunakan THRESH_BINARY_INV agar ridge (garis sidik jari) bernilai 255 (putih) 
    dan background bernilai 0 (hitam), sesuai standar algoritma thinning.
    """
    _, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary_img


def apply_morphological_cleaning(img: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Menghilangkan noise (bintik putih/hitam kecil) menggunakan operasi morfologi.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    # Opening: menghilangkan noise putih kecil di background
    cleaned = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    # Closing: menutup lubang hitam kecil di dalam ridge
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)
    return cleaned


def preprocess_fingerprint(img: np.ndarray) -> dict:
    """
    Pipeline preprocessing lengkap.
    Mengembalikan dictionary berisi semua tahap untuk keperluan visualisasi di UI.
    """
    # Pastikan input adalah grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    enhanced = apply_clahe(img)
    binary = apply_otsu_binarization(enhanced)
    cleaned = apply_morphological_cleaning(binary)
    
    return {
        "original": img,
        "enhanced": enhanced,
        "binary": binary,
        "cleaned": cleaned
    }

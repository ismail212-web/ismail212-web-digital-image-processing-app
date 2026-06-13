"""
Modul thinning (penipisan) sidik jari.
Mengimplementasikan algoritma Zhang-Suen untuk menipiskan ridge menjadi ketebalan 1 piksel.
"""
import cv2
import numpy as np


def apply_thinning(img: np.ndarray) -> np.ndarray:
    """
    Menipiskan citra biner (skeletonization) hingga ketebalan 1 piksel.
    Menggunakan algoritma Zhang-Suen dari OpenCV Contrib (ximgproc).
    
    Args:
        img (np.ndarray): Citra biner input (ridge = 255, background = 0).
        
    Returns:
        np.ndarray: Citra hasil thinning (skeleton).
    """
    # Pastikan input adalah citra biner (0 dan 255)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Normalisasi ke 0 dan 1 untuk keamanan algoritma thinning
    _, binary = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
    
    try:
        # Gunakan cv2.ximgproc.thinning (Zhang-Suen algorithm)
        # THINNING_ZHANGSUEN = 0, THINNING_GUOHALL = 1
        thinned = cv2.ximgproc.thinning(binary, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
        
        # Kembalikan ke format 0 dan 255 agar konsisten dengan OpenCV standar
        return thinned * 255
        
    except AttributeError:
        # Fallback jika opencv-contrib-python tidak terinstal
        raise ImportError(
            "Modul cv2.ximgproc tidak ditemukan. "
            "Silakan instal: pip install opencv-contrib-python"
        )

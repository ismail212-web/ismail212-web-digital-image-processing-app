"""
Modul ekstraksi minutiae sidik jari menggunakan metode Crossing Number (CN).
Ridge Ending: CN = 1
Bifurcation: CN = 3
"""
import cv2
import numpy as np


def compute_crossing_number(skeleton: np.ndarray) -> np.ndarray:
    """
    Menghitung nilai Crossing Number (CN) untuk setiap piksel pada citra skeleton.
    Menggunakan vektorisasi NumPy untuk performa tinggi.
    
    Args:
        skeleton (np.ndarray): Citra skeleton biner (0 dan 255).
        
    Returns:
        np.ndarray: Matriks CN dengan ukuran yang sama dengan input.
    """
    # Normalisasi ke 0 dan 1
    img = (skeleton > 0).astype(np.uint8)
    
    # Padding 1 piksel di semua sisi (agar bisa proses tepi)
    padded = np.pad(img, 1, mode='constant', constant_values=0)
    
    # Ekstrak 8 tetangga (urutan searah jarum jam, mulai dari top-left)
    p1 = padded[0:-2, 0:-2]  # top-left
    p2 = padded[0:-2, 1:-1]  # top
    p3 = padded[0:-2, 2:]    # top-right
    p4 = padded[1:-1, 2:]    # right
    p5 = padded[2:, 2:]      # bottom-right
    p6 = padded[2:, 1:-1]    # bottom
    p7 = padded[2:, 0:-2]    # bottom-left
    p8 = padded[1:-1, 0:-2]  # left
    
    # Rumus CN = 1/2 * sum(|Pi - P_{i+1}|)
    cn = 0.5 * (
        np.abs(p1 - p2) + np.abs(p2 - p3) + np.abs(p3 - p4) + np.abs(p4 - p5) +
        np.abs(p5 - p6) + np.abs(p6 - p7) + np.abs(p7 - p8) + np.abs(p8 - p1)
    )
    
    return cn


def extract_minutiae(skeleton: np.ndarray, border_margin: int = 10) -> dict:
    """
    Mengekstrak titik minutiae (Ridge Ending dan Bifurcation) dari citra skeleton.
    
    Args:
        skeleton (np.ndarray): Citra skeleton biner (0 dan 255).
        border_margin (int): Jarak minimum dari tepi citra untuk mengabaikan 
                             minutiae palsu (artefak tepi).
                             
    Returns:
        dict: {
            'ridge_endings': (y_coords, x_coords),
            'bifurcations': (y_coords, x_coords),
            'total': int
        }
    """
    cn = compute_crossing_number(skeleton)
    center = (skeleton > 0).astype(np.uint8)
    
    # Buat mask untuk mengabaikan area tepi (border)
    h, w = center.shape
    mask = np.ones_like(center, dtype=bool)
    if border_margin > 0:
        mask[:border_margin, :] = False
        mask[-border_margin:, :] = False
        mask[:, :border_margin] = False
        mask[:, -border_margin:] = False
    
    # Deteksi Ridge Ending (CN = 1) dan Bifurcation (CN = 3)
    # Hanya pada piksel yang memang bagian dari ridge (center == 1)
    ridge_endings = np.where((cn == 1) & (center == 1) & mask)
    bifurcations = np.where((cn == 3) & (center == 1) & mask)
    
    return {
        "ridge_endings": ridge_endings,
        "bifurcations": bifurcations,
        "total": len(ridge_endings[0]) + len(bifurcations[0])
    }


def draw_minutiae(img: np.ndarray, minutiae: dict, 
                  ending_color: tuple = (0, 0, 255),
                  bifurcation_color: tuple = (0, 255, 0),
                  radius: int = 3) -> np.ndarray:
    """
    Menggambar titik minutiae pada citra untuk visualisasi.
    Ridge Ending = Merah, Bifurcation = Hijau.
    
    Args:
        img (np.ndarray): Citra latar (bisa grayscale atau BGR).
        minutiae (dict): Output dari fungsi extract_minutiae().
        ending_color (tuple): Warna BGR untuk Ridge Ending.
        bifurcation_color (tuple): Warna BGR untuk Bifurcation.
        radius (int): Radius titik yang digambar.
        
    Returns:
        np.ndarray: Citra BGR dengan titik minutiae tergambarkan.
    """
    # Konversi ke BGR jika grayscale
    if len(img.shape) == 2:
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        vis = img.copy()
    
    # Gambar Ridge Ending (merah)
    for y, x in zip(minutiae["ridge_endings"][0], minutiae["ridge_endings"][1]):
        cv2.circle(vis, (int(x), int(y)), radius, ending_color, -1)
    
    # Gambar Bifurcation (hijau)
    for y, x in zip(minutiae["bifurcations"][0], minutiae["bifurcations"][1]):
        cv2.circle(vis, (int(x), int(y)), radius, bifurcation_color, -1)
    
    return vis

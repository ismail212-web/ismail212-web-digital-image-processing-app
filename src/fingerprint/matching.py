"""
Modul pencocokan sidik jari menggunakan SIFT dan FLANN Matcher.
Menerapkan Lowe's Ratio Test untuk menyaring kecocokan yang kuat.
"""
import cv2
import numpy as np


def extract_sift_features(img: np.ndarray):
    """
    Mengekstrak keypoints dan descriptors menggunakan algoritma SIFT.
    
    Args:
        img (np.ndarray): Citra grayscale input.
        
    Returns:
        tuple: (keypoints, descriptors)
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return keypoints, descriptors


def match_features(des1: np.ndarray, des2: np.ndarray, ratio_threshold: float = 0.75):
    """
    Mencocokkan dua set descriptors menggunakan FLANN dan Lowe's Ratio Test.
    
    Args:
        des1 (np.ndarray): Descriptors dari citra pertama.
        des2 (np.ndarray): Descriptors dari citra kedua.
        ratio_threshold (float): Threshold untuk Lowe's ratio test (default 0.75).
        
    Returns:
        list: Daftar objek DMatch yang lolos seleksi (good matches).
    """
    if des1 is None or des2 is None:
        return []
        
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    # KNN Match (k=2) untuk ratio test
    raw_matches = flann.knnMatch(des1, des2, k=2)
    
    good_matches = []
    for pair in raw_matches:
        if len(pair) == 2:
            m, n = pair
            # Lowe's ratio test
            if m.distance < ratio_threshold * n.distance:
                good_matches.append(m)
                
    return good_matches


def calculate_similarity(good_matches: list, kp1: list, kp2: list) -> float:
    """
    Menghitung skor similarity berdasarkan jumlah good matches.
    
    Args:
        good_matches (list): Hasil dari match_features().
        kp1 (list): Keypoints citra pertama.
        kp2 (list): Keypoints citra kedua.
        
    Returns:
        float: Skor similarity dalam persentase (0 - 100).
    """
    num_matches = len(good_matches)
    max_possible = min(len(kp1), len(kp2))
    
    if max_possible == 0:
        return 0.0
        
    return (num_matches / max_possible) * 100.0


def match_fingerprints(img1: np.ndarray, img2: np.ndarray, ratio_threshold: float = 0.75) -> dict:
    """
    Pipeline lengkap pencocokan dua sidik jari.
    
    Returns:
        dict: {
            'kp1': keypoints img1,
            'kp2': keypoints img2,
            'good_matches': list of DMatch,
            'similarity_score': float (0-100),
            'is_match': bool (True jika score > 20% atau matches >= 15)
        }
    """
    kp1, des1 = extract_sift_features(img1)
    kp2, des2 = extract_sift_features(img2)
    
    good_matches = match_features(des1, des2, ratio_threshold)
    score = calculate_similarity(good_matches, kp1, kp2)
    
    # Threshold logis untuk keputusan pencocokan
    is_match = (len(good_matches) >= 15) or (score > 20.0)
    
    return {
        "kp1": kp1,
        "kp2": kp2,
        "good_matches": good_matches,
        "similarity_score": score,
        "is_match": is_match
    }

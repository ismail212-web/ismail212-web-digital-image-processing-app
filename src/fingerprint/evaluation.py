"""
Modul evaluasi performa sistem pengenalan sidik jari.
Menghitung metrik standar biometrik: FAR, FRR, dan EER.
"""
import numpy as np
from typing import List, Tuple, Dict


def calculate_far_frr_at_threshold(
    genuine_scores: List[float],
    impostor_scores: List[float],
    threshold: float
) -> Tuple[float, float]:
    """
    Menghitung FAR dan FRR pada satu nilai threshold tertentu.
    
    Args:
        genuine_scores (List[float]): Skor pencocokan dari pasangan sidik jari yang SAMA (user yang sama).
        impostor_scores (List[float]): Skor pencocokan dari pasangan sidik jari yang BERBEDA (user berbeda).
        threshold (float): Nilai threshold keputusan.
        
    Returns:
        Tuple[float, float]: (FAR, FRR) dalam rentang 0.0 - 1.0
    """
    if not genuine_scores or not impostor_scores:
        return 0.0, 0.0
    
    # FAR: impostor yang lolos (score >= threshold) / total impostor
    false_accepts = sum(1 for s in impostor_scores if s >= threshold)
    far = false_accepts / len(impostor_scores)
    
    # FRR: genuine yang ditolak (score < threshold) / total genuine
    false_rejects = sum(1 for s in genuine_scores if s < threshold)
    frr = false_rejects / len(genuine_scores)
    
    return far, frr


def calculate_far_frr_curve(
    genuine_scores: List[float],
    impostor_scores: List[float],
    num_thresholds: int = 100
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Menghitung kurva FAR dan FRR untuk berbagai nilai threshold.
    
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: (thresholds, far_values, frr_values)
    """
    # Gabungkan semua skor untuk menentukan rentang threshold
    all_scores = genuine_scores + impostor_scores
    min_score = min(all_scores)
    max_score = max(all_scores)
    
    thresholds = np.linspace(min_score, max_score, num_thresholds)
    far_values = np.zeros(num_thresholds)
    frr_values = np.zeros(num_thresholds)
    
    for i, threshold in enumerate(thresholds):
        far, frr = calculate_far_frr_at_threshold(genuine_scores, impostor_scores, threshold)
        far_values[i] = far
        frr_values[i] = frr
    
    return thresholds, far_values, frr_values


def calculate_eer(
    genuine_scores: List[float],
    impostor_scores: List[float],
    num_thresholds: int = 100
) -> Dict[str, float]:
    """
    Menghitung Equal Error Rate (EER) — titik di mana FAR = FRR.
    EER adalah metrik standar internasional untuk evaluasi sistem biometrik.
    
    Returns:
        Dict[str, float]: {
            'eer': nilai EER (0-1),
            'threshold_at_eer': nilai threshold saat EER tercapai,
            'far_at_eer': FAR saat EER,
            'frr_at_eer': FRR saat EER
        }
    """
    thresholds, far_values, frr_values = calculate_far_frr_curve(
        genuine_scores, impostor_scores, num_thresholds
    )
    
    # Cari titik di mana |FAR - FRR| paling kecil
    diff = np.abs(far_values - frr_values)
    eer_idx = np.argmin(diff)
    
    # Interpolasi linear untuk akurasi lebih tinggi
    if eer_idx > 0 and eer_idx < len(thresholds) - 1:
        # Rata-rata FAR dan FRR di titik terdekat
        eer_value = (far_values[eer_idx] + frr_values[eer_idx]) / 2.0
    else:
        eer_value = far_values[eer_idx]
    
    return {
        "eer": float(eer_value),
        "threshold_at_eer": float(thresholds[eer_idx]),
        "far_at_eer": float(far_values[eer_idx]),
        "frr_at_eer": float(frr_values[eer_idx])
    }


def evaluate_system_performance(
    genuine_scores: List[float],
    impostor_scores: List[float]
) -> Dict:
    """
    Pipeline evaluasi lengkap sistem pengenalan sidik jari.
    
    Args:
        genuine_scores: List skor pencocokan dari sidik jari yang SAMA.
        impostor_scores: List skor pencocokan dari sidik jari yang BERBEDA.
        
    Returns:
        Dict berisi semua metrik evaluasi.
    """
    # Hitung EER
    eer_result = calculate_eer(genuine_scores, impostor_scores)
    
    # Hitung kurva lengkap
    thresholds, far_curve, frr_curve = calculate_far_frr_curve(
        genuine_scores, impostor_scores
    )
    
    # Statistik dasar
    result = {
        "eer": eer_result,
        "mean_genuine_score": float(np.mean(genuine_scores)) if genuine_scores else 0.0,
        "mean_impostor_score": float(np.mean(impostor_scores)) if impostor_scores else 0.0,
        "num_genuine_pairs": len(genuine_scores),
        "num_impostor_pairs": len(impostor_scores),
        "curve_data": {
            "thresholds": thresholds.tolist(),
            "far_values": far_curve.tolist(),
            "frr_values": frr_curve.tolist()
        }
    }
    
    return result

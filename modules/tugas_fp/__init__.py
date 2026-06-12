# modules/tugas_fp/__init__.py
from .fingerprint import run as run_fingerprint
from .fingerprint_fraud import run as run_fraud

EXPERIMENT_FP = {
    "4.1 Fingerprint Processing": run_fingerprint,
    "4.2 Fingerprint Fraud Detection (SIFT)": run_fraud,
    # "4.3 Palm" sudah dipindah ke tugas_palm
}

__all__ = ["EXPERIMENT_FP", "fingerprint", "fingerprint_fraud"]

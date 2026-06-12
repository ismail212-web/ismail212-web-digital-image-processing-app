# modules/__init__.py
from modules.tugas1 import EXPERIMENT_TUGAS1
from modules.tugas2 import EXPERIMENT_TUGAS2
from modules.tugas_fft import EXPERIMENT_FFT

from modules.tugas_fp import fingerprint, fingerprint_fraud
from modules.tugas_palm import palm_ripeness

MASTER_LAB_REGISTRY = {
    "Materi 1: Elemen & Operasi Piksel": EXPERIMENT_TUGAS1,
    "Materi 2: Transformasi": EXPERIMENT_TUGAS2,
    "Materi 3: Filtering": EXPERIMENT_FFT,
    "Materi 4: Sidik Jari": {
        "4.1 Fingerprint Processing": fingerprint.run,
        "4.2 Fingerprint Fraud Detection (SIFT)": fingerprint_fraud.run,
    },
    "Materi 5: Palm Ripeness": {
        "5.1 Palm Oil Ripeness Detection": palm_ripeness.run,
    },
}

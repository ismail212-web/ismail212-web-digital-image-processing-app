# modules/tugas_palm/__init__.py
import logging
from .palm_ripeness import run as run_palm

EXPERIMENT_PALM = {
    "5.1 Palm Oil Ripeness Detection": run_palm,
}

__all__ = ["EXPERIMENT_PALM", "palm_ripeness"]
logging.getLogger("DIP_Lab").info("✅ Modul Tugas Palm terdaftar.")

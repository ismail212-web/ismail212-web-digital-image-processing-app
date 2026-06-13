import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="logs/app.log", level="INFO"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("DIPLabDesktop")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

"""
src/logger.py
Production-Grade Structured Logging Utility Module
Establishes a dual-stream rotating file logger framework to handle automation tracking.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import settings

# 1. Resolve Runtime Log Persistence Boundaries
LOG_DIR: Path = Path(settings.DATABASE_URL.replace("sqlite:///./", "")).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH: Path = LOG_DIR / "app.log"

# 2. Define Enterprise-Grade Structured Log Formatter String Layout
LOG_FORMATTER: logging.Formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 3. Initialize Core Corporate Log Instance Engine
logger: logging.Logger = logging.getLogger("agency_automation_engine")

# Map dynamic level boundaries securely from our validated config configurations
numeric_level: int = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logger.setLevel(numeric_level)

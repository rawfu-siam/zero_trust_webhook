"""
src/logger.py
Production-Grade Structured Logging Utility Module
Establishes a dual-stream rotating file logger framework to handle automation tracking.
"""

import logging
import sys
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
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 3. Initialize Core Corporate Log Instance Engine
logger: logging.Logger = logging.getLogger("agency_automation_engine")

# Map dynamic level boundaries securely from our validated config configurations
numeric_level: int = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logger.setLevel(numeric_level)


# ==============================================================================
# 4. Storage Shield: Configure Rotating File Handlers (50KB Constraints)
# ==============================================================================
# 50KB size cap constraint (50 * 1024 Bytes) with a 3-file back-up rotation buffer
FILE_STREAM_SHIELD: RotatingFileHandler = RotatingFileHandler(
    filename=LOG_FILE_PATH, maxBytes=51200, backupCount=3, encoding="utf-8"
)
FILE_STREAM_SHIELD.setFormatter(LOG_FORMATTER)
logger.addHandler(FILE_STREAM_SHIELD)

# ==============================================================================
# 5. Console Stream Integration: Live Development Execution Views
# ==============================================================================
CONSOLE_STREAM_HANDLER: logging.StreamHandler = logging.StreamHandler(sys.stdout)
CONSOLE_STREAM_HANDLER.setFormatter(LOG_FORMATTER)
logger.addHandler(CONSOLE_STREAM_HANDLER)

# Disallow logs from propagating up to the root log ecosystem to block print duplicates
logger.propagate = False

# ==============================================================================
# 6. Corporate Application Global Interface Export Hooks
# ==============================================================================
__all__ = ["logger"]

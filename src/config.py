"""
src/config.py
System Configuration Management Module
Handles secure runtime parsing, mapping, and verification of environment variables.
"""

import os
import sys
from pathlib import Path
from typing import Final

# 1. Base Directory Tracking Definitions
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# 2. Zero-Trust Local Environment Bootstrap Initialization
ENV_FILE_PATH: Final[Path] = BASE_DIR / ".env"

if ENV_FILE_PATH.exists():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=ENV_FILE_PATH)
else:
    # Explicitly fail-safe to stderr before the app logging system is available
    sys.stderr.write(f"WARNING: Configuration initialization failed to locate .env at: {ENV_FILE_PATH}\n")

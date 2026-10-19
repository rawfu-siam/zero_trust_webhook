"""
src/config.py
System Configuration Management Module
Handles secure runtime parsing, mapping, and verification of environment variables.
"""

import os
import sys
from pathlib import Path
from typing import Final

from pydantic import BaseModel, Field, ValidationError

# 1. Base Directory Tracking Definitions
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# 2. Zero-Trust Local Environment Bootstrap Initialization
ENV_FILE_PATH: Final[Path] = BASE_DIR / ".env"

if ENV_FILE_PATH.exists():
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=ENV_FILE_PATH)
else:
    # Explicitly fail-safe to stderr before the app logging system is available
    sys.stderr.write(
        f"WARNING: Configuration initialization failed to locate .env at: {ENV_FILE_PATH}\n"
    )


# 3. Enterprise Configuration Type Enforcement & Schema Guardrails
class Settings(BaseModel):
    """
    Settings Schema Engine
    Enforces runtime type-safety and structural fallback configurations
    for incoming enterprise automation primitives.
    """

    APP_ENV: str = Field(
        default="development", description="System deployment stage constraint"
    )
    LOG_LEVEL: str = Field(
        default="INFO", description="Granularity boundary limit for native logger"
    )
    WEBHOOK_SECRET_TOKEN: str = Field(
        ..., description="Secure header signature key token for ingestion filtering"
    )
    DATABASE_URL: str = Field(
        default="sqlite:///./src/webhook_data.db",
        description="Target persistence string",
    )


# 4. Zero-Trust Bootstrap Safety Execution Verification
try:
    # Hydrate the immutable data container directly out of system environment maps
    settings: Settings = Settings(
        APP_ENV=os.environ.get("APP_ENV", "development"),
        LOG_LEVEL=os.environ.get("LOG_LEVEL", "INFO"),
        WEBHOOK_SECRET_TOKEN=os.environ.get("WEBHOOK_SECRET_TOKEN"),
        DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///./src/webhook_data.db"),
    )
except ValidationError as e:
    # Intercept missing fields at system boot time to block execution in unsafe zones
    sys.stderr.write("\n" + "=" * 80 + "\n")
    sys.stderr.write(
        "CRITICAL CONFIGURATION ERROR: System bootstrapped into an unverified state.\n"
    )
    sys.stderr.write(
        "Missing or structurally malformed environment variable variables detected:\n"
    )
    sys.stderr.write(str(e))
    sys.stderr.write("\n" + "=" * 80 + "\n\n")
    # Immediate application crash exit to guarantee zero-trust boundary execution
    sys.exit(1)

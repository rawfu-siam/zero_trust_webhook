"""
tests/conftest.py
Global Pytest Shared Testing Infrastructure Framework Configuration File
Establishes environment isolation mocking parameters and provisions test application clients.
"""

import os
import sys
from typing import Generator
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Establish absolute systemic module lookup paths target directions
TEST_ROOT_DIR: Path = Path(__file__).resolve().parent.parent
sys.path.append(str(TEST_ROOT_DIR / "src"))

# 1. Enforce Hard Isolated Environmental Variables Configurations for Safety
os.environ["APP_ENV"] = "testing"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["WEBHOOK_SECRET_TOKEN"] = "test_suite_secret_credential_token_999888"
os.environ["DATABASE_URL"] = "sqlite:///./tests/test_sandbox_vault.db"

# Now safely import application modules after environmental overrides are strictly bound
from main import app
from database import initialize_database_schema, DB_FILE_PATH

@pytest.fixture(scope="session", autouse=True)
def run_database_bootstrap_lifecycle() -> Generator[None, None, None]:
    """
    Automated Lifecycle Hook for Global Testing Persistence Layer.
    Guarantees isolation boundaries by dropping old test database fixtures at runtime startup.
    """
    # Defensive cleanup configuration step to ensure data tracking starts fresh
    if DB_FILE_PATH.exists():
        try:
            DB_FILE_PATH.unlink()
        except OSError:
            pass
            
    # Provision the temporary isolated testing sandbox environment
    initialize_database_schema()
    yield
    
    # Tear down test data artifacts post session completion cycles to clean the local directory
    if DB_FILE_PATH.exists():
        try:
            DB_FILE_PATH.unlink()
        except OSError:
            pass

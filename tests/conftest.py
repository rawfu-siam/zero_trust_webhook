"""
tests/conftest.py
Global Pytest Shared Testing Infrastructure Framework Configuration File
Establishes environment isolation mocking parameters and provisions test application clients.
"""

import os
import sys
from pathlib import Path
from typing import Generator

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
from database import DB_FILE_PATH, initialize_database_schema  # noqa: E402
from main import app  # noqa: E402


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


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """
    Function-scoped testing client fixture runner.
    Yields an isolated FastAPI TestClient block, then aggressively clears out
    relational data records between case runs to maintain pristine testing states.
    """
    with TestClient(app) as test_client:
        yield test_client

    # Boundary Cleanup: Execute dynamic table truncation queries after every test case run
    try:
        from database import get_db_connection

        with get_db_connection() as connection:
            cursor = connection.cursor()
            # Clear target lead record allocations cleanly without killing DDL structures
            cursor.execute("DELETE FROM processed_webhooks;")
            connection.commit()
    except Exception:
        # Gracefully log or pass if database unlinking happened during session teardown
        pass

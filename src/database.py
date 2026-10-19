"""
src/database.py
Database Connection Management & Lifecycle Mapping Module
Coordinates low-level transactional connection wrappers and auto-provisions schema states.
"""

import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Final, Generator, Optional

from config import settings
from logger import logger

# 1. Resolve Immutable Path String Targets from Validated Configuration Layer
DB_CONNECTION_STRING: Final[str] = settings.DATABASE_URL.replace("sqlite:///", "")
DB_FILE_PATH: Final[Path] = Path(DB_CONNECTION_STRING).resolve()


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context Manager Lifecycle Hook for Transaction Isolation Pools.
    Yields an active SQLite connection pointer with atomic autocommit safety configurations,
    catching operational runtime failures defensively.
    """
    connection: Optional[sqlite3.Connection] = None
    try:
        # Guarantee relational row tracking configurations are returned as indexed mapping dict structures
        connection = sqlite3.connect(database=str(DB_FILE_PATH), timeout=10.0)
        connection.row_factory = sqlite3.Row

        # Enforce foreign key constraints inside SQLite core explicitly on every thread session boot
        connection.execute("PRAGMA foreign_keys = ON;")

        yield connection

    except sqlite3.OperationalError as db_fault:
        logger.critical(
            f"Database Boundary Integrity Breached: Transaction connectivity pool failed. Detail: {str(db_fault)}"
        )
        raise db_fault

    finally:
        if connection:
            connection.close()


# ==============================================================================
# 2. Enterprise Relational Schema Definitions (DDL Declarations)
# ==============================================================================
INGESTION_TABLE_DDL: Final[str] = """
CREATE TABLE IF NOT EXISTS processed_webhooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,
    lead_name TEXT NOT NULL,
    lead_email TEXT NOT NULL,
    lead_phone TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status TEXT DEFAULT 'COMPLETED'
);
"""


# ==============================================================================
# 3. Defensive Schema Initialization Bootstrapping
# ==============================================================================
def initialize_database_schema() -> None:
    """
    Defensively executes core DDL statements at engine boot sequence.
    Guarantees target persistence layer storage structures exist before processing events.
    """
    logger.info("Initializing relational database storage schema validation layouts...")

    # Auto-generate target parent container folders to avoid local IO system faults
    DB_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with get_db_connection() as connection:
            cursor: sqlite3.Cursor = connection.cursor()

            # Execute DDL table mapping schema blocks atomically
            cursor.execute(INGESTION_TABLE_DDL)
            connection.commit()

            logger.info(
                "Database schema structure check verified successfully. Tables generated."
            )

    except sqlite3.Error as schema_fault:
        logger.critical(
            f"FATAL: Structural table blueprint injection failed down internal pipeline: {str(schema_fault)}"
        )
        sys.exit(1)


# Ensure database tables map correctly onto current workspace layer during module compile cycles
if __name__ not in ("__main__", "src.database"):
    initialize_database_schema()

if __name__ == "__main__":
    # Allow terminal users to explicitly trigger clean standalone structure generation loops
    initialize_database_schema()

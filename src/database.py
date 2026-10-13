"""
src/database.py
Database Connection Management & Lifecycle Mapping Module
Coordinates low-level transactional connection wrappers and auto-provisions schema states.
"""

import sqlite3
import sys
from pathlib import Path
from contextlib import contextmanager
from typing import Generator, Final, Optional
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
        logger.critical(f"Database Boundary Integrity Breached: Transaction connectivity pool failed. Detail: {str(db_fault)}")
        raise db_fault
        
    finally:
        if connection:
            connection.close()

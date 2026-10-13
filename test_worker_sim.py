"""
test_worker_sim.py
Background Worker Simulation Module
Simulates a high-throughput, flaky data loop pipeline to test log file rotation parameters.
"""

import random
import time
import sys
from pathlib import Path

# Adjust path context to allow seamless local runtime discovery of internal source modules
sys.path.append(str(Path(__file__).resolve().parent / "src"))
from logger import logger

class WorkerPipelineError(Exception):
    """Custom corporate execution exception raised during transient pipeline updates."""
    pass

def execute_automation_iteration(iteration_id: int) -> None:
    """
    Executes a high-velocity simulated webhook processing event.
    Intentionally throws transient exceptions to force error log growth matrices.
    """
    # Large structured descriptive payload block to purposefully bloat log footprint sizes
    payload_fingerprint: str = (
        f"METRIC_RUN_ID={iteration_id} | STATUS=PROCESSING | "
        f"CIPHER_HASH=sha256_8f3c8d1e2b9a4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d | "
        f"TELEMETRY_DATA_INGESTION_STREAM_VAL=ACTIVE_SUCCESS_VERIFIED"
    )
    
    logger.debug(f"Attempting transactional pipeline entry allocation: {payload_fingerprint}")
    
    # Intentionally model a high failure-rate metric (25% transient drop probability)
    if random.random() < 0.25:
        raise WorkerPipelineError(
            f"Transient transmission fault detected during webhook packet ingestion on run #{iteration_id}"
        )
        
    logger.info(f"Pipeline milestone completed successfully for task entity ID: {iteration_id}")

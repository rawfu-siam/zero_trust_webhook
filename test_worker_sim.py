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

def run_high_velocity_worker_loop(target_iterations: int = 400) -> None:
    """
    Drives a high-throughput pipeline runner execution sequence.
    Pipes deep validation tracing into the logger utility to force 50KB boundary splits.
    """
    logger.info(f"System Boot: Launching automated logging storage shield stress test for {target_iterations} iterations.")
    
    for iteration in range(1, target_iterations + 1):
        try:
            execute_automation_iteration(iteration_id=iteration)
        except WorkerPipelineError as error_trace:
            # Catch transient failures safely, logging complete contextual trace metrics
            logger.error(f"Execution Exception Caught on Step #{iteration}: {str(error_trace)}")
        
        # Micro-delay to avoid CPU lockup while maintaining rapid sequential high-throughput volume
        time.sleep(0.002)
        
    logger.info("Stress Testing Suite Complete. Validating local log rotation targets...")

if __name__ == "__main__":
    # Standard fallback deployment size to ensure rotation thresholds are easily breached
    run_high_velocity_worker_loop()

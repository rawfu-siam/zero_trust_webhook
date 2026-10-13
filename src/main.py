"""
src/main.py
Core FastAPI Webhook Ingestion Engine
Orchestrates secure webhook lifecycle endpoints, structural middleware filters, 
and automated transactional persistence pipelines.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, status, HTTPException

# Adjust the system path explicitly to guarantee seamless absolute runtime module discoverability
sys.path.append(str(Path(__file__).resolve().parent))

from config import settings
from logger import logger
from database import initialize_database_schema

# 1. Enterprise App Orchestration Engine Configurations
app: FastAPI = FastAPI(
    title="Zero-Trust Webhook Ingestion Engine",
    description="Production-grade, highly dependable lead ingestion firewall pipeline for USA Boutique AI Automation Agencies.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
def on_app_startup() -> None:
    """Triggered on application boot cycle to ensure relational systems are mapped."""
    logger.info("FastAPI Server Context spinning up. Checking persistence layer baseline bounds...")
    initialize_database_schema()
    logger.info("Application bootstrap sequences fully established. Awaiting client traffic.")

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoring"])
def run_health_checkpoint() -> dict[str, str]:
    """
    Standard low-latency infrastructure system pulse health endpoint.
    Used by uptime checkers, cloud container platforms, and routing fabrics to monitor liveliness.
    """
    return {"status": "healthy", "engine": "active", "environment": settings.APP_ENV}

"""
src/main.py
Core FastAPI Webhook Ingestion Engine
Orchestrates secure webhook lifecycle endpoints, structural middleware filters, 
and automated transactional persistence pipelines.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, status, HTTPException
from typing import Any

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

# ==============================================================================
# 2. Zero-Trust Security Token Verification Layer (Dependency Injection)
# ==============================================================================
from fastapi import Header, Security

def verify_webhook_security_signature(x_agency_token: str = Header(..., alias="X-Agency-Token")) -> str:
    """
    Defensively audits incoming HTTP request header credentials.
    Rejects unauthorized actors at the boundary before script processing cycles run.
    """
    if x_agency_token != settings.WEBHOOK_SECRET_TOKEN:
        logger.warning("SECURITY ALERT: Unauthorized webhook entry attempt intercepted with invalid signature header.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security authentication verification signature mismatch. Access denied."
        )
    return x_agency_token

# ==============================================================================
# 3. Webhook Ingestion Router & Persistence Pipeline Implementation
# ==============================================================================
import json
import sqlite3
from schemas import WebhookPayloadSchema
from database import get_db_connection

@app.post("/webhook/ingest", status_code=status.HTTP_201_CREATED, tags=["Ingestion Framework"])
def ingest_client_webhook_payload(
    payload: WebhookPayloadSchema,
    _security_token: str = Security(verify_webhook_security_signature)
) -> dict[str, str | int]:
    """
    Validates, normalizes, and safely processes incoming lead webhook events.
    Enforces strict signature authorization filters and commits raw data schemas securely.
    """
    logger.info(f"Incoming Ingestion Request Verified. Executing write transaction for event ID: {payload.event_id}")
    
    try:
        with get_db_connection() as connection:
            cursor: sqlite3.Cursor = connection.cursor()
            
            # Execute transactional lookup check to enforce schema uniqueness constraints defensively
            cursor.execute("SELECT id FROM processed_webhooks WHERE event_id = ?;", (payload.event_id,))
            if cursor.fetchone():
                logger.warning(f"Idempotency Guardrail: Event ID '{payload.event_id}' rejected as duplicate tracking entry.")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Transactional conflict: Webhook payload event ID '{payload.event_id}' has already been processed."
                )
            
            # Persist the fully validated and sanitized Pydantic model directly to SQLite
            cursor.execute(
                """
                INSERT INTO processed_webhooks (event_id, lead_name, lead_email, lead_phone, payload_json)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    payload.event_id,
                    payload.lead_name,
                    payload.lead_email,
                    payload.lead_phone,
                    payload.model_dump_json()
                )
            )
            connection.commit()
            
            # Fetch the auto-incremented primary key to return an explicit confirmation audit token
            inserted_id: int = cursor.lastrowid or 0
            
        logger.info(f"Transaction Committed Successfully. Lead database record logged with primary reference index key ID: {inserted_id}")
        return {"status": "success", "message": "Lead ingested successfully", "record_id": inserted_id}
        
    except HTTPException as api_exit:
        # Re-raise explicit HTTP errors like our 409 conflict straight back out to the response layer
        raise api_exit
        
    except Exception as raw_pipeline_fault:
        # Prevent downstream crashes from killing the worker thread; log trace variables and fail cleanly
        logger.error(f"Unchecked Internal Database Pipeline Exception Intercepted: {str(raw_pipeline_fault)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal engineering processing threshold error. Transaction rolled back safely."
        )

# ==============================================================================
# 4. Enterprise Global Exception Overrides & Structural Validation Mapping
# ==============================================================================
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(RequestValidationError)
def global_validation_exception_override_handler(
    _request: Request, 
    exception_packet: RequestValidationError
) -> JSONResponse:
    """
    Globally intercepts incoming schema-malformed payload exception states.
    Suppresses native long structural framework traces, returning a clean diagnostic array
    to client APIs while dumping the precise anomaly straight to our RotatingFileHandler log database.
    """
    error_summary_metrics: list[dict[str, Any]] = []
    for issue in exception_packet.errors():
        error_summary_metrics.append({
            "target_field": " -> ".join(str(path_node) for path_node in issue.get("loc", []) if path_node != "body"),
            "issue_type": issue.get("type"),
            "diagnostic_message": issue.get("msg")
        })
        
    logger.error(
        f"Validation Boundary Intercepted Malformed Incoming Payload: "
        f"Detected structural anomaly matrix: {json.dumps(error_summary_metrics)}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "reason": "Provided request schema structural data parameter configurations failed type coercion guardrails.",
            "anomalies": error_summary_metrics
        }
    )

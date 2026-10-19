"""
tests/test_ingestion_api.py
Integration & Contract Testing Suite
Tests security validation filters, Pydantic guardrails, and database row allocations.
"""

import sys
import os
from pathlib import Path
from fastapi import status
from fastapi.testclient import TestClient

# Establish shared absolute lookup mappings for backend discovery
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from database import get_db_connection

# Define structural, high-fidelity mock metrics for testing streams
VALID_AUTH_HEADERS: dict[str, str] = {"X-Agency-Token": "test_suite_secret_credential_token_999888"}
INVALID_AUTH_HEADERS: dict[str, str] = {"X-Agency-Token": "compromised_token_999"}

def test_health_checkpoint_liveliness(client: TestClient) -> None:
    """Verifies that the infrastructure pulse check responds with structural system telemetry."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"
    assert response.json()["environment"] == "testing"

def test_webhook_ingest_success_path(client: TestClient) -> None:
    """Verifies that clean customer data parses correctly, persists, and returns success logs."""
    mock_payload: dict[str, str] = {
        "event_id": "evt_integration_001",
        "lead_name": "Marcus Aurelius",
        "lead_email": "marcus.aurelius@rome.gov",
        "lead_phone": "+1 (555) 019-2834"
    }

    response = client.post("/webhook/ingest", headers=VALID_AUTH_HEADERS, json=mock_payload)
    
    # 1. Assert correct endpoint routing response parameters
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "success"
    assert "record_id" in response.json()

    # 2. Database State Validation: Verify row allocation matching our parameters
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM processed_webhooks WHERE event_id = ?;", (mock_payload["event_id"],))
        db_row = cursor.fetchone()
        
    assert db_row is not None
    assert db_row["lead_name"] == "Marcus Aurelius"
    assert db_row["lead_email"] == "marcus.aurelius@rome.gov"
    # Ensure phone data was completely cleaned via field validator mappings before saving
    assert db_row["lead_phone"] == "15550192834"

def test_webhook_ingest_unauthorized_header_interception(client: TestClient) -> None:
    """Ensures unauthorized webhook request entries are hard-blocked at the api border."""
    mock_payload: dict[str, str] = {
        "event_id": "evt_unauth_002",
        "lead_name": "Hack Entity",
        "lead_email": "attacker@darknet.org",
        "lead_phone": "1000000000"
    }

    response = client.post("/webhook/ingest", headers=INVALID_AUTH_HEADERS, json=mock_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()

def test_webhook_ingest_idempotency_guardrail(client: TestClient) -> None:
    """Ensures duplicate webhook event submissions throw a transactional conflict."""
    mock_payload: dict[str, str] = {
        "event_id": "evt_duplicate_100",
        "lead_name": "John Connor",
        "lead_email": "john.connor@resistance.net",
        "lead_phone": "15559998888"
    }

    # First entry submission (Should succeed)
    first_response = client.post("/webhook/ingest", headers=VALID_AUTH_HEADERS, json=mock_payload)
    assert first_response.status_code == status.HTTP_201_CREATED

    # Identical sequential entry submission (Should trigger our database duplicate block)
    second_response = client.post("/webhook/ingest", headers=VALID_AUTH_HEADERS, json=mock_payload)
    assert second_response.status_code == status.HTTP_409_CONFLICT
    assert "processed" in second_response.json()["detail"]


def test_webhook_ingest_malformed_payload_interception(client: TestClient) -> None:
    """Verifies that heavily corrupted data schemas trigger our custom diagnostic 422 JSON array."""
    corrupted_payload: dict[str, str] = {
        "event_id": "shrt",
        "lead_name": "A",
        "lead_email": "broken-email-string",
        "lead_phone": "invalid_phone_123"
    }

    response = client.post("/webhook/ingest", headers=VALID_AUTH_HEADERS, json=corrupted_payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data["status"] == "error"
    assert "anomalies" in response_data
    # Ensure our diagnostic override captures specific array fields cleanly
    assert len(response_data["anomalies"]) > 0


def test_webhook_ingest_phone_sanitation_normalization(client: TestClient) -> None:
    """Ensures complex, messy white-space phone layouts clean up perfectly on database write."""
    messy_payload: dict[str, str] = {
        "event_id": "evt_phone_clean_200",
        "lead_name": "Ellen Ripley",
        "lead_email": "ripley@nostromo.org",
        "lead_phone": "  +1 (800)-555-2345  "
    }

    response = client.post("/webhook/ingest", headers=VALID_AUTH_HEADERS, json=messy_payload)
    assert response.status_code == status.HTTP_201_CREATED

    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT lead_phone FROM processed_webhooks WHERE event_id = ?;", (messy_payload["event_id"],))
        row = cursor.fetchone()

    assert row is not None
    # Verify the regex completely normalized typography bounds
    assert row["lead_phone"] == "18005552345"

"""
src/schemas.py
Runtime Data Validation & Payload Schema Module
Leverages Pydantic BaseModel to enforce strict corporate type-coercion and sanitization.
"""

import re
from typing import Final

from pydantic import BaseModel, EmailStr, Field, field_validator

# Strict USA Agency Formatting Regex Pattern for Phone Sanitation Checkpoints
USA_PHONE_REGEX: Final[re.Pattern] = re.compile(r"^\+?1?\d{10,14}$")


class WebhookPayloadSchema(BaseModel):
    """
    Webhook Ingestion Parsing Layer
    Intercepts unstructured third-party JSON payloads, forcing type compliance,
    sanitizing field parameters, and mapping standardized lead records.
    """

    event_id: str = Field(
        ...,
        min_length=5,
        description="Unique source identity tracker tracking token string",
    )
    lead_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full designation name of incoming entity customer",
    )
    lead_email: EmailStr = Field(
        ...,
        description="Strictly validated corporate electronic mailing vector destination",
    )
    lead_phone: str = Field(
        ...,
        description="Target telephonic communication vector numeric sequence string",
    )

    @field_validator("lead_phone", mode="before")
    @classmethod
    def sanitize_and_format_phone(cls, raw_value: str) -> str:
        """
        Defensively sanitizes raw telephone text input matrices.
        Strips arbitrary space blocks, parentheses, or dashes to evaluate string integrity.
        """
        if not isinstance(raw_value, str):
            raise ValueError(
                "Telephonic metadata parameters must arrive as explicit string sequences."
            )

        # Strip common typographic character spacing blocks to force data normalization
        cleaned_digits: str = re.sub(r"[\s\-\(\)\+]", "", raw_value)

        # Enforce international structural capacity limit checks
        if not USA_PHONE_REGEX.match(cleaned_digits) and not (
            len(cleaned_digits) >= 10 and cleaned_digits.isdigit()
        ):
            raise ValueError(
                f"Supplied phone layout configuration sequence failed structure check: {raw_value}"
            )

        return cleaned_digits

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "event_id": "evt_9f8e7d6c5b4a",
                "lead_name": "Alex Mercer",
                "lead_email": "alex.mercer@agencyclient.com",
                "lead_phone": "+1 (555) 019-2834",
            }
        },
    }


# ==============================================================================
# 2. Standalone Verification Driver Pipeline Simulation
# ==============================================================================
if __name__ == "__main__":
    import sys

    from pydantic import ValidationError

    sys.stdout.write("Launching runtime Pydantic schema validation pipeline tests...\n")

    # Scenario A: Clean Success Path with Messy Formatting Input
    raw_messy_payload = {
        "event_id": "evt_1029384756",
        "lead_name": "Sarah Connor",
        "lead_email": "sarah@sky-net.io",
        "lead_phone": " +1 (555)-234-5678  ",
    }

    try:
        validated_record = WebhookPayloadSchema(**raw_messy_payload)
        sys.stdout.write("\n[SUCCESS] Payload passed zero-trust structural boundary!\n")
        sys.stdout.write(f"Original Phone : '{raw_messy_payload['lead_phone']}'\n")
        sys.stdout.write(f"Sanitized Phone: '{validated_record.lead_phone}'\n\n")
    except ValidationError as error_packet:
        sys.stderr.write(
            f"[FAILURE] Valid payload rejected unexpectedly: {str(error_packet)}\n"
        )
        sys.exit(1)

    # Scenario B: Intentional Crash Validation Boundary Check
    raw_corrupted_payload = {
        "event_id": "short",
        "lead_name": "X",
        "lead_email": "invalid-email-address",
        "lead_phone": "broken_string_123",
    }

    try:
        WebhookPayloadSchema(**raw_corrupted_payload)
        sys.stderr.write(
            "[FAILURE] Guardrail failed to intercept a corrupted payload string structure!\n"
        )
        sys.exit(1)
    except ValidationError as validation_faults:
        sys.stdout.write(
            "[SUCCESS] Zero-trust defensive boundary safely blocked a corrupted payload:\n"
        )
        sys.stdout.write(str(validation_faults) + "\n")

"""
src/schemas.py
Runtime Data Validation & Payload Schema Module
Leverages Pydantic BaseModel to enforce strict corporate type-coercion and sanitization.
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
import re
from typing import Final

# Strict USA Agency Formatting Regex Pattern for Phone Sanitation Checkpoints
USA_PHONE_REGEX: Final[re.Pattern] = re.compile(r"^\+?1?\d{10,14}$")

class WebhookPayloadSchema(BaseModel):
    """
    Webhook Ingestion Parsing Layer
    Intercepts unstructured third-party JSON payloads, forcing type compliance,
    sanitizing field parameters, and mapping standardized lead records.
    """
    event_id: str = Field(..., min_length=5, description="Unique source identity tracker tracking token string")
    lead_name: str = Field(..., min_length=2, max_length=100, description="Full designation name of incoming entity customer")
    lead_email: EmailStr = Field(..., description="Strictly validated corporate electronic mailing vector destination")
    lead_phone: str = Field(..., description="Target telephonic communication vector numeric sequence string")

    @field_validator("lead_phone", mode="before")
    @classmethod
    def sanitize_and_format_phone(cls, raw_value: str) -> str:
        """
        Defensively sanitizes raw telephone text input matrices.
        Strips arbitrary space blocks, parentheses, or dashes to evaluate string integrity.
        """
        if not isinstance(raw_value, str):
            raise ValueError("Telephonic metadata parameters must arrive as explicit string sequences.")
        
        # Strip common typographic character spacing blocks to force data normalization
        cleaned_digits: str = re.sub(r"[\s\-\(\)\+]", "", raw_value)
        
        # Enforce international structural capacity limit checks
        if not USA_PHONE_REGEX.match(cleaned_digits) and not (len(cleaned_digits) >= 10 and cleaned_digits.isdigit()):
            raise ValueError(f"Supplied phone layout configuration sequence failed structure check: {raw_value}")
            
        return cleaned_digits

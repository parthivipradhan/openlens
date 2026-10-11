"""
Strict JSON schema validation for AI-extracted evidence outputs.

Rules (AGENTS.md):
- Never fabricate missing dates, coordinates, measurements, or event details.
- Insufficient evidence -> reject extraction, never invent.
- Reject invalid outputs and log validation failures.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


class EvidenceCategory(str, Enum):
    WATERLOGGING = "waterlogging"
    AIR_QUALITY = "air_quality"
    ROAD_CLOSURE = "road_closure"
    PUBLIC_TRANSPORT = "public_transport"
    GREEN_SPACES = "green_spaces"
    HEALTHCARE = "healthcare"
    NOISE = "noise"
    INFRASTRUCTURE = "infrastructure"
    EDUCATION = "education"


class ExtractedClaim(BaseModel):
    claim_text: str = Field(..., min_length=5, max_length=500)
    claim_type: str = Field("observation", max_length=50)
    confidence: float = Field(0.7, ge=0.0, le=1.0)


class ExtractedEvidenceSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    summary: str = Field(..., min_length=10, max_length=1000)
    category: EvidenceCategory
    original_location_text: str = Field(..., min_length=2, max_length=200)
    event_date: Optional[str] = Field(None, description="ISO YYYY-MM-DD format if known")
    severity: Optional[str] = Field("medium", max_length=20)
    confidence: float = Field(0.8, ge=0.0, le=1.0)
    claims: list[ExtractedClaim] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @field_validator("event_date")
    @classmethod
    def validate_event_date(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        # Must be valid ISO date YYYY-MM-DD
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            # If the model tried to fabricate or format wrongly, do not accept it
            return None


def validate_ai_extraction(raw_data: dict[str, Any]) -> tuple[Optional[ExtractedEvidenceSchema], Optional[str]]:
    """
    Validate AI extraction payload against ExtractedEvidenceSchema.
    Returns (schema_instance, None) on success, or (None, error_message) on failure.
    """
    try:
        validated = ExtractedEvidenceSchema.model_validate(raw_data)
        return validated, None
    except ValidationError as err:
        return None, str(err)

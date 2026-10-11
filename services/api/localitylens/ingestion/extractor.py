"""
Structured evidence extraction using open-weight LLMs (Ollama) or Mock provider.

Generates precise extraction prompt requiring JSON output conforming to ExtractedEvidenceSchema.
Enforces the no-fabrication rule and passes untrusted text through isolation fences.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import structlog

from localitylens.ai.provider import get_ai_provider, AIProviderError
from localitylens.ingestion.sanitizer import wrap_untrusted_input
from localitylens.ingestion.validator import validate_ai_extraction, ExtractedEvidenceSchema

log = structlog.get_logger(__name__)

EXTRACTION_SYSTEM_PROMPT = """You are a factual evidence extraction engine for LocalityLens, an open intelligence platform.
Your task is to extract neighbourhood observations and factual civic evidence from the provided document.

CRITICAL RULES:
1. Never fabricate dates, coordinates, metrics, or locations. If not explicitly mentioned in the text, leave event_date as null.
2. Select category only from: waterlogging, air_quality, road_closure, public_transport, green_spaces, healthcare, noise, infrastructure, education.
3. original_location_text MUST be extracted verbatim from the text (e.g. "Sector 17", "Madhya Marg", "Sector 35 near market").
4. Output ONLY valid JSON matching this schema:
{
  "title": "Short descriptive title (max 100 chars)",
  "summary": "Objective 1-3 sentence summary of the reported condition or event",
  "category": "one of the allowed categories",
  "original_location_text": "Exact location mentioned in source",
  "event_date": "YYYY-MM-DD or null if date is not stated",
  "severity": "low | medium | high",
  "confidence": 0.85,
  "claims": [{"claim_text": "Specific factual claim", "claim_type": "observation", "confidence": 0.9}],
  "limitations": ["Any limitation or ambiguity mentioned"]
}
"""


async def extract_evidence_from_text(
    raw_text: str,
    source_name: str = "External Source",
) -> tuple[Optional[ExtractedEvidenceSchema], Optional[str]]:
    """
    Extract structured evidence record from unstructured text.
    Returns (validated_record, None) or (None, error_reason).
    """
    wrapped_text = wrap_untrusted_input(raw_text, source_label=f"DOCUMENT_{source_name}")
    prompt = f"{EXTRACTION_SYSTEM_PROMPT}\n\nDocument to extract:\n{wrapped_text}\n\nOutput JSON:"

    provider = get_ai_provider()

    # For mock provider, return a deterministic structured extraction
    from localitylens.ai.provider import MockAIProvider
    if isinstance(provider, MockAIProvider):
        mock_data = {
            "title": f"Civic observation from {source_name}",
            "summary": raw_text[:200] if len(raw_text) > 20 else f"Extracted civic report from {source_name}",
            "category": "infrastructure",
            "original_location_text": "Sector 17, Chandigarh",
            "event_date": None,
            "severity": "medium",
            "confidence": 0.85,
            "claims": [{"claim_text": "Civic observation recorded in Chandigarh", "claim_type": "observation", "confidence": 0.85}],
            "limitations": ["Mock extraction mode active"],
        }
        return validate_ai_extraction(mock_data)

    # For Ollama / real provider
    try:
        from localitylens.ai.provider import OllamaProvider
        if isinstance(provider, OllamaProvider):
            import httpx
            from localitylens.core.config import settings

            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "format": "json",
                        "stream": False,
                    },
                )
                res.raise_for_status()
                response_text = res.json().get("response", "")
                parsed = json.loads(response_text)
                return validate_ai_extraction(parsed)
    except Exception as exc:
        log.warning("Extraction failed", error=str(exc))
        return None, f"Extraction failed: {exc}"

    return None, "No suitable provider available for extraction"

"""
Ingestion Pipeline — LocalityLens Phase 4 & Phase 7.

Orchestrates:
1. URL validation with SSRF protection (core.security)
2. Safe content fetching with timeout and size caps
3. Prompt-injection sanitisation (ingestion.sanitizer)
4. Structured AI extraction (ingestion.extractor)
5. Strict output schema validation (ingestion.validator)
6. Canonical SHA-256 digest computation (integrity.merkle)
7. Geocoding / sector assignment (geospatial)
"""

from __future__ import annotations

from typing import Any, Optional
import httpx
import structlog

from localitylens.core.security import validate_source_url
from localitylens.ingestion.extractor import extract_evidence_from_text
from localitylens.ingestion.sanitizer import sanitize_source_content
from localitylens.ingestion.validator import ExtractedEvidenceSchema
from localitylens.integrity.merkle import compute_evidence_digest

log = structlog.get_logger(__name__)

MAX_FETCH_BYTES = 5 * 1024 * 1024  # 5 MB max download limit
FETCH_TIMEOUT_SECONDS = 15.0


async def fetch_source_document(url: str) -> str:
    """
    Fetch an external document safely with SSRF protection and download caps.
    """
    safe_url = validate_source_url(url)

    async with httpx.AsyncClient(
        timeout=FETCH_TIMEOUT_SECONDS,
        follow_redirects=True,
        max_redirects=3,
        headers={"User-Agent": "LocalityLens-Ingestion-Bot/1.0 (+https://localitylens.org)"},
    ) as client:
        response = await client.get(safe_url)
        response.raise_for_status()

        # Check content length
        content = response.text
        if len(content.encode("utf-8")) > MAX_FETCH_BYTES:
            raise ValueError(f"Content exceeded {MAX_FETCH_BYTES} bytes limit.")

        return content


async def ingest_source_document(
    url: Optional[str] = None,
    raw_text: Optional[str] = None,
    source_name: str = "External Ingestion",
    source_id: str = "src_manual",
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    """
    Execute full ingestion pipeline for a document:
    Fetch -> Sanitize -> Extract -> Validate -> Compute Digest
    """
    try:
        text_content = raw_text
        if not text_content and url:
            text_content = await fetch_source_document(url)

        if not text_content:
            return None, "No text content provided or retrieved."

        # Sanitize
        clean_text = sanitize_source_content(text_content)

        # Extract & validate
        extracted, error = await extract_evidence_from_text(clean_text, source_name=source_name)
        if error or not extracted:
            return None, f"Extraction rejected: {error}"

        # Construct final record
        record_dict = {
            "source_id": source_id,
            "title": extracted.title,
            "summary": extracted.summary,
            "category": extracted.category.value,
            "original_location_text": extracted.original_location_text,
            "event_date": extracted.event_date,
            "published_at": None,
            "is_synthetic": False,
        }

        # Generate mock id for digest preview if not yet saved to DB
        record_dict["id"] = "ev_preview"
        digest = compute_evidence_digest(record_dict)
        record_dict["digest_sha256"] = digest
        record_dict["claims"] = [c.model_dump() for c in extracted.claims]
        record_dict["limitations"] = extracted.limitations

        return record_dict, None

    except Exception as exc:
        log.error("Ingestion pipeline failed", error=str(exc))
        return None, str(exc)

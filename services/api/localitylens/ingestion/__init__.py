"""Ingestion pipeline and extraction validation package."""

from localitylens.ingestion.extractor import extract_evidence_from_text
from localitylens.ingestion.pipeline import ingest_source_document
from localitylens.ingestion.sanitizer import sanitize_source_content, wrap_untrusted_input
from localitylens.ingestion.validator import validate_ai_extraction, ExtractedEvidenceSchema

__all__ = [
    "extract_evidence_from_text",
    "ingest_source_document",
    "sanitize_source_content",
    "wrap_untrusted_input",
    "validate_ai_extraction",
    "ExtractedEvidenceSchema",
]

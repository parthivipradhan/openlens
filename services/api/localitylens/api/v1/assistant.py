"""POST /api/v1/assistant/ask — Grounded question answering (Phase 4)."""

from __future__ import annotations

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from localitylens.ai.provider import EvidenceContext, get_ai_provider, AIProviderError
from localitylens.ai.rag import retrieve_evidence_for_query
from localitylens.core.security import check_ai_rate_limit
from localitylens.db.session import get_db

log = structlog.get_logger(__name__)
router = APIRouter()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    locality_id: Optional[str] = Field(None, description="Narrow retrieval to a specific locality")


class Citation(BaseModel):
    evidence_id: str


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[str]
    limitations: list[str]
    mock: bool
    model: str
    insufficient_evidence: bool
    retrieved_count: int


@router.post("/ask", summary="Ask the LocalityLens AI assistant", response_model=AskResponse)
async def ask(
    req: AskRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _rate: None = Depends(check_ai_rate_limit),
):
    """
    Grounded Q&A using RAG over the evidence database.

    Rules enforced (per AGENTS.md):
    - AI answers are grounded in retrieved evidence only.
    - Insufficient evidence → explicit abstention, never fabrication.
    - Cited evidence IDs are validated against retrieved records.
    - AI output JSON schema is validated before returning.
    """
    # Step 1: Retrieve relevant evidence
    records = await retrieve_evidence_for_query(
        db, req.question, locality_id=req.locality_id
    )
    context = EvidenceContext(records)

    # Step 2: Ask AI provider (mock or Ollama)
    provider = get_ai_provider()
    try:
        result = await provider.ask(req.question, context)
    except AIProviderError as exc:
        log.error("AI provider error", exc=str(exc))
        raise HTTPException(
            status_code=503,
            detail=f"AI provider unavailable: {exc}. Set AI_MOCK_MODE=true to use mock mode.",
        )

    return AskResponse(
        question=req.question,
        answer=result["answer"],
        citations=result.get("citations", []),
        limitations=result.get("limitations", []),
        mock=result.get("mock", True),
        model=result.get("model", "unknown"),
        insufficient_evidence=result.get("insufficient_evidence", False),
        retrieved_count=len(records),
    )

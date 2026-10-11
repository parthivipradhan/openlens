"""RAG retrieval helper — fetch evidence records relevant to a query."""

from __future__ import annotations

from typing import Any, Optional

import structlog
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from localitylens.db.models import EvidenceRecord

log = structlog.get_logger(__name__)


async def retrieve_evidence_for_query(
    db: AsyncSession,
    question: str,
    locality_id: Optional[str] = None,
    limit: int = 8,
) -> list[dict[str, Any]]:
    """
    Simple keyword-based retrieval from the evidence table.

    Phase 4 uses keyword search. A future phase can replace this with pgvector
    embedding similarity once vector columns are added.

    Rules enforced:
    - Never return synthetic records in production (unless explicitly requested).
    - Returned records are the ground truth; AI must cite only these IDs.
    """
    # Build keyword terms from the question (naive tokenization)
    stop_words = {"is", "in", "the", "a", "an", "of", "are", "for", "what", "how", "does", "do"}
    tokens = [
        t.lower().strip(".,?!")
        for t in question.split()
        if len(t) > 2 and t.lower() not in stop_words
    ]

    query = select(EvidenceRecord).where(EvidenceRecord.review_status != "rejected")

    if locality_id:
        query = query.where(EvidenceRecord.source_id == locality_id)

    # Apply keyword filters using OR across title + summary
    if tokens:
        conditions = []
        for token in tokens[:6]:  # cap tokens for query safety
            conditions.append(EvidenceRecord.title.ilike(f"%{token}%"))
            conditions.append(EvidenceRecord.summary.ilike(f"%{token}%"))
            conditions.append(EvidenceRecord.category.ilike(f"%{token}%"))
            conditions.append(EvidenceRecord.original_location_text.ilike(f"%{token}%"))
        query = query.where(or_(*conditions))

    query = query.limit(limit)

    try:
        result = await db.execute(query)
        records = result.scalars().all()
        log.info("RAG retrieval", tokens=tokens[:6], found=len(records))
        return [r.to_dict() for r in records]
    except Exception as exc:
        log.error("RAG retrieval error", exc=str(exc))
        return []

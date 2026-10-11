"""POST /api/v1/compare — Locality comparison engine (Phase 5)."""

from __future__ import annotations

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from localitylens.comparison.engine import (
    compute_comparison,
    count_evidence_by_category,
)
from localitylens.db.models import Locality
from localitylens.db.session import get_db

log = structlog.get_logger(__name__)
router = APIRouter()


class CompareRequest(BaseModel):
    locality_ids: list[str] = Field(..., min_length=2, max_length=5)
    weights: Optional[dict[str, float]] = Field(
        None,
        description="User-defined dimension weights (e.g. {'public_transport': 0.25}). "
        "Unnormalised — will be normalised to sum to 1.",
    )


@router.post("", summary="Compare localities side-by-side")
async def compare_localities(req: CompareRequest, db: AsyncSession = Depends(get_db)):
    """
    Deterministic locality comparison using evidence record counts.

    All scoring is performed by application code, not an LLM.
    Transparent weights, missing-data warnings, and full dimension breakdown included.
    """
    # Validate localities exist
    localities: dict[str, dict] = {}
    for lid in req.locality_ids:
        result = await db.execute(select(Locality).where(Locality.id == lid))
        loc = result.scalar_one_or_none()
        if not loc:
            raise HTTPException(status_code=404, detail=f"Locality '{lid}' not found.")
        localities[lid] = loc.to_dict()

    # Fetch evidence counts per locality
    counts_per_locality: dict[str, dict[str, int]] = {}
    for lid in req.locality_ids:
        counts_per_locality[lid] = await count_evidence_by_category(db, lid)

    # Run deterministic comparison
    result = compute_comparison(
        locality_ids=req.locality_ids,
        counts_per_locality=counts_per_locality,
        weights=req.weights,
    )

    return {
        "localities": localities,
        "comparison": result,
        "methodology": (
            "Scores are derived from evidence record counts per category for each locality. "
            "Negative-polarity dimensions (e.g. waterlogging) are inverted so fewer incidents = higher score. "
            "All intermediate values are provided for full transparency."
        ),
    }

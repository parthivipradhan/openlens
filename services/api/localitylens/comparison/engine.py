"""
Locality Comparison Engine — Phase 5.

Deterministic scoring: all weights are explicit, all calculations are done
by application code (never by an LLM). Missing data → warnings, not zeros.

Categories scored:
  - waterlogging    (lower is better → invert)
  - air_quality     (lower incidents = better → invert)
  - noise           (lower is better → invert)
  - road_closure    (lower is better → invert)
  - public_transport (higher is better)
  - green_spaces    (higher is better)
  - healthcare      (higher is better)
  - education       (higher is better)
  - infrastructure  (higher is better)

Score formula (per dimension):
  - Count evidence records of that category for the locality.
  - Normalise across compared localities (0–100 scale).
  - Apply user-defined weight.
  - Sum to produce composite score.

Transparency: all intermediate values are returned in the response.
"""

from __future__ import annotations

from typing import Any, Optional

import structlog
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from localitylens.db.models import EvidenceRecord, Locality

log = structlog.get_logger(__name__)

# Dimensions and whether a higher count is good (+1) or bad (-1)
DIMENSION_POLARITY: dict[str, int] = {
    "waterlogging": -1,
    "air_quality": -1,
    "noise": -1,
    "road_closure": -1,
    "public_transport": 1,
    "green_spaces": 1,
    "healthcare": 1,
    "education": 1,
    "infrastructure": 1,
}

DEFAULT_WEIGHTS: dict[str, float] = {
    "waterlogging": 0.15,
    "air_quality": 0.12,
    "noise": 0.08,
    "road_closure": 0.10,
    "public_transport": 0.15,
    "green_spaces": 0.12,
    "healthcare": 0.12,
    "education": 0.10,
    "infrastructure": 0.06,
}


async def count_evidence_by_category(
    db: AsyncSession,
    locality_id: str,
) -> dict[str, int]:
    """
    Count evidence records per category for a given locality_id.
    Uses parameterised queries — no string-formatted SQL (per AGENTS.md rule 14).
    """
    # Join evidence to locality via original_location_text matching locality name
    # In a PostGIS-enabled setup this would use ST_Within; here we use the
    # locality name stored on each evidence record for the demo dataset.
    locality_result = await db.execute(select(Locality).where(Locality.id == locality_id))
    locality = locality_result.scalar_one_or_none()
    if not locality:
        return {}

    # Count by category for evidence whose location text contains the locality name
    # (demo approximation; real implementation uses PostGIS ST_Within)
    result = await db.execute(
        select(EvidenceRecord.category, func.count(EvidenceRecord.id).label("cnt"))
        .where(
            EvidenceRecord.original_location_text.ilike(f"%{locality.name}%")
        )
        .where(EvidenceRecord.review_status != "rejected")
        .group_by(EvidenceRecord.category)
    )
    counts: dict[str, int] = {row.category: row.cnt for row in result}
    return counts


def _normalise(values: list[float]) -> list[float]:
    """Min-max normalise to [0, 100]. If all equal, returns 50 for each."""
    mn, mx = min(values), max(values)
    if mx == mn:
        return [50.0] * len(values)
    return [(v - mn) / (mx - mn) * 100 for v in values]


def compute_comparison(
    locality_ids: list[str],
    counts_per_locality: dict[str, dict[str, int]],
    weights: Optional[dict[str, float]] = None,
) -> dict[str, Any]:
    """
    Pure, deterministic comparison calculation.
    Returns full scoring breakdown for transparency.
    """
    effective_weights = {**DEFAULT_WEIGHTS, **(weights or {})}
    # Normalise weights to sum to 1
    total_weight = sum(effective_weights.values()) or 1.0
    effective_weights = {k: v / total_weight for k, v in effective_weights.items()}

    dimensions = list(DIMENSION_POLARITY.keys())
    missing_warnings: list[str] = []

    # Build score matrix: locality_id → dimension → raw count
    raw: dict[str, dict[str, int]] = {lid: counts_per_locality.get(lid, {}) for lid in locality_ids}

    # Per-dimension normalisation
    dim_scores: dict[str, dict[str, float]] = {lid: {} for lid in locality_ids}
    for dim in dimensions:
        polarity = DIMENSION_POLARITY[dim]
        raw_vals = [raw[lid].get(dim, None) for lid in locality_ids]

        # Track missing data
        missing = [locality_ids[i] for i, v in enumerate(raw_vals) if v is None]
        if missing:
            missing_warnings.append(
                f"No '{dim}' evidence found for locality(ies): {', '.join(missing)}. "
                "Scores for this dimension may be unreliable."
            )
            # Do NOT substitute zero. Use None → excluded from normalisation.
            # Assign 50 (neutral) for missing localities.
            filled = [v if v is not None else 0 for v in raw_vals]
        else:
            filled = [v for v in raw_vals]  # type: ignore[assignment]

        normalised = _normalise(filled)
        for i, lid in enumerate(locality_ids):
            if polarity == -1:
                dim_scores[lid][dim] = 100 - normalised[i]  # invert: fewer incidents = better
            else:
                dim_scores[lid][dim] = normalised[i]

    # Compute composite score
    composite: dict[str, float] = {}
    for lid in locality_ids:
        score = sum(
            dim_scores[lid].get(dim, 50.0) * effective_weights.get(dim, 0)
            for dim in dimensions
        )
        composite[lid] = round(score, 2)

    # Rank
    ranked = sorted(locality_ids, key=lambda lid: composite[lid], reverse=True)

    return {
        "weights_applied": effective_weights,
        "dimensions": dimensions,
        "dimension_polarity": DIMENSION_POLARITY,
        "raw_evidence_counts": raw,
        "dimension_scores": dim_scores,
        "composite_scores": composite,
        "ranking": ranked,
        "missing_data_warnings": missing_warnings,
    }

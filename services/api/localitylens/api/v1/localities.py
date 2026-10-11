"""Locality endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from localitylens.db.session import get_db
from localitylens.db.models import Locality

router = APIRouter()


@router.get("", summary="Search localities")
async def list_localities(
    db: AsyncSession = Depends(get_db),
    q: Optional[str] = Query(None, description="Name search"),
    limit: int = Query(50, le=200),
):
    query = select(Locality).order_by(Locality.name).limit(limit)
    if q:
        query = query.where(Locality.name.ilike(f"%{q}%"))
    result = await db.execute(query)
    localities = result.scalars().all()
    return {"localities": [loc.to_dict() for loc in localities]}


@router.get("/{locality_id}/summary", summary="Locality summary")
async def get_locality_summary(locality_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Locality).where(Locality.id == locality_id))
    locality = result.scalar_one_or_none()
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
    return {
        "locality": locality.to_dict(),
        "summary": "Locality Intelligence Report — Phase 4 feature (AI-generated, grounded in evidence).",
        "evidence_counts": {},
        "data_freshness": {},
    }

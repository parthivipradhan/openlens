"""GET /api/v1/sources — source registry and freshness."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from localitylens.db.session import get_db
from localitylens.db.models import DatasetManifest, EvidenceRecord, Source

router = APIRouter()


@router.get("", summary="List data sources with freshness and counts")
async def list_sources(
    db: AsyncSession = Depends(get_db),
    source_type: Optional[str] = Query(None, description="Filter by type (news, osm, govt, community, demo)"),
    authority_classification: Optional[str] = Query(None, description="Filter by authority tier"),
    status: Optional[str] = Query(None, description="Filter by status (active, stale, degraded, paused)"),
    q: Optional[str] = Query(None, description="Search source name or publisher"),
):
    query = select(Source)
    if source_type:
        query = query.where(Source.source_type == source_type)
    if authority_classification:
        query = query.where(Source.authority_classification == authority_classification)
    if status:
        query = query.where(Source.status == status)
    if q:
        query = query.where(
            (Source.name.ilike(f"%{q}%")) | (Source.publisher.ilike(f"%{q}%"))
        )

    query = query.order_by(Source.name)
    result = await db.execute(query)
    sources = result.scalars().all()

    # Get evidence counts per source
    counts_res = await db.execute(
        select(EvidenceRecord.source_id, func.count(EvidenceRecord.id))
        .group_by(EvidenceRecord.source_id)
    )
    counts = dict(counts_res.all())

    items = []
    for s in sources:
        d = s.to_dict()
        d["evidence_count"] = counts.get(s.id, 0)
        items.append(d)

    return {"sources": items, "total": len(items)}


@router.get("/{source_id}", summary="Get source detail")
async def get_source(source_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Source).where(Source.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    count_res = await db.execute(
        select(func.count(EvidenceRecord.id)).where(EvidenceRecord.source_id == source_id)
    )
    evidence_count = count_res.scalar_one()

    # Match dataset manifest by identifier or publisher
    manifest_res = await db.execute(
        select(DatasetManifest).where(
            (DatasetManifest.dataset_identifier.ilike(f"%{source.name.lower().replace(' ', '-')}%")) |
            (DatasetManifest.publisher.ilike(f"%{source.publisher or source.name}%"))
        ).limit(1)
    )
    manifest = manifest_res.scalar_one_or_none()

    data = source.to_dict()
    data["evidence_count"] = evidence_count
    data["manifest"] = manifest.to_dict() if manifest else None
    return data


@router.get("/{source_id}/manifest", summary="Get source dataset manifest")
async def get_source_manifest(source_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Source).where(Source.id == source_id))
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    manifest_res = await db.execute(
        select(DatasetManifest).where(
            (DatasetManifest.dataset_identifier.ilike(f"%{source.name.lower().replace(' ', '-')}%")) |
            (DatasetManifest.publisher.ilike(f"%{source.publisher or source.name}%"))
        ).limit(1)
    )
    manifest = manifest_res.scalar_one_or_none()
    if not manifest:
        raise HTTPException(status_code=404, detail="Dataset manifest not found for this source")
    return manifest.to_dict()

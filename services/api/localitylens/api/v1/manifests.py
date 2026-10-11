"""Dataset Manifests endpoints — transparency and provenance."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from localitylens.db.session import get_db
from localitylens.db.models import DatasetManifest

router = APIRouter()


@router.get("", summary="List dataset manifests")
async def list_manifests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DatasetManifest).order_by(DatasetManifest.name))
    manifests = result.scalars().all()
    return {"manifests": [m.to_dict() for m in manifests], "total": len(manifests)}


@router.get("/{manifest_id}", summary="Get dataset manifest by ID or identifier")
async def get_manifest(manifest_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DatasetManifest).where(
            (DatasetManifest.id == manifest_id) | (DatasetManifest.dataset_identifier == manifest_id)
        )
    )
    manifest = result.scalar_one_or_none()
    if not manifest:
        raise HTTPException(status_code=404, detail="Dataset manifest not found")
    return manifest.to_dict()

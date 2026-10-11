"""
TrustLayer API endpoints — Phase 6.

GET  /api/v1/anchors             — list anchor batches
GET  /api/v1/anchors/{id}/receipt — receipt for an anchor batch
"""

from __future__ import annotations

import structlog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from localitylens.db.session import get_db
from localitylens.db.models import AnchorBatch, AnchorLeaf

log = structlog.get_logger(__name__)
router = APIRouter()


@router.get("", summary="List evidence anchor batches")
async def list_anchors(db: AsyncSession = Depends(get_db)):
    """List all Merkle anchor batches (TrustLayer)."""
    result = await db.execute(
        select(AnchorBatch).order_by(AnchorBatch.created_at.desc()).limit(50)
    )
    batches = result.scalars().all()
    return {
        "anchors": [
            {
                "id": b.id,
                "batch_identifier": b.batch_identifier,
                "merkle_root": b.merkle_root,
                "leaf_count": b.leaf_count,
                "chain_id": b.chain_id,
                "transaction_hash": b.transaction_hash,
                "block_number": b.block_number,
                "verification_status": b.verification_status,
                "canonicalisation_version": b.canonicalisation_version,
                "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in batches
        ]
    }


@router.get("/{anchor_id}/receipt", summary="Retrieve a verification receipt")
async def get_receipt(anchor_id: str, db: AsyncSession = Depends(get_db)):
    """Return a Merkle anchor batch receipt with leaf digests."""
    result = await db.execute(select(AnchorBatch).where(AnchorBatch.id == anchor_id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise HTTPException(status_code=404, detail="Anchor batch not found.")

    leaves_result = await db.execute(
        select(AnchorLeaf).where(AnchorLeaf.batch_id == anchor_id)
    )
    leaves = leaves_result.scalars().all()

    return {
        "batch_id": batch.id,
        "batch_identifier": batch.batch_identifier,
        "merkle_root": batch.merkle_root,
        "leaf_count": batch.leaf_count,
        "chain_id": batch.chain_id,
        "contract_address": batch.contract_address,
        "transaction_hash": batch.transaction_hash,
        "block_number": batch.block_number,
        "verification_status": batch.verification_status,
        "created_at": batch.created_at.isoformat() if batch.created_at else None,
        "leaves": [
            {
                "evidence_id": leaf.evidence_id,
                "leaf_digest": leaf.leaf_digest,
                "leaf_index": leaf.leaf_index,
                "merkle_proof": leaf.merkle_proof,
            }
            for leaf in leaves
        ],
        "note": (
            "Blockchain verification confirms digest integrity, not truth of underlying claims. "
            "Only Merkle roots are stored on-chain — no personal data or raw evidence."
        ),
    }

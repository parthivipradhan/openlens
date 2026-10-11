"""Evidence endpoints — search, detail, relations, provenance, review history, and verify."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, asc, func, or_, select
from sqlalchemy.orm import selectinload

from localitylens.db.session import get_db
from localitylens.db.models import (
    EvidenceClaim,
    EvidenceRecord,
    EvidenceRelation,
    RELATION_TYPES,
    ReviewEvent,
    Source,
)

router = APIRouter()


class EvidenceRelationCreate(BaseModel):
    target_evidence_id: str = Field(..., description="Target evidence record ID to relate to")
    relation_type: str = Field(..., description="One of: supports, contradicts, duplicate_of, supersedes, derived_from")


class EvidenceReviewCreate(BaseModel):
    action: str = Field(..., description="Review action: e.g. verified, rejected, corrected_category, flagged_duplicate")
    reason: Optional[str] = Field(None, description="Explanation or reasoning for this action")
    reviewer: Optional[str] = Field("community_reviewer", description="Identifier of the reviewer")
    new_review_status: Optional[str] = Field(None, description="Updated review status, e.g. verified, disputed, archived")
    new_category: Optional[str] = Field(None, description="Corrected category if applicable")


@router.get("", summary="Search and filter evidence records")
async def list_evidence(
    db: AsyncSession = Depends(get_db),
    q: Optional[str] = Query(None, description="Search keyword in title, summary, or location"),
    category: Optional[str] = Query(None, description="Category filter"),
    locality_id: Optional[str] = Query(None, description="Locality filter"),
    source_id: Optional[str] = Query(None, description="Source filter"),
    review_status: Optional[str] = Query(None, description="Status filter: verified, pending, demo, rejected"),
    is_synthetic: Optional[bool] = Query(None, description="Filter synthetic demo records"),
    geocoding_precision: Optional[str] = Query(None, description="Precision filter: point, road, sector, area"),
    start_date: Optional[str] = Query(None, description="Earliest published_at or event_date (ISO 8601)"),
    end_date: Optional[str] = Query(None, description="Latest published_at or event_date (ISO 8601)"),
    sort_by: str = Query("published_at", pattern="^(published_at|event_date|created_at|title)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
):
    query = select(EvidenceRecord).options(selectinload(EvidenceRecord.source))

    if q:
        search_filter = or_(
            EvidenceRecord.title.ilike(f"%{q}%"),
            EvidenceRecord.summary.ilike(f"%{q}%"),
            EvidenceRecord.original_location_text.ilike(f"%{q}%"),
        )
        query = query.where(search_filter)

    if category:
        query = query.where(EvidenceRecord.category == category)

    if source_id:
        query = query.where(EvidenceRecord.source_id == source_id)

    if review_status:
        query = query.where(EvidenceRecord.review_status == review_status)

    if is_synthetic is not None:
        query = query.where(EvidenceRecord.is_synthetic == is_synthetic)

    if geocoding_precision:
        query = query.where(EvidenceRecord.geocoding_precision == geocoding_precision)

    if start_date:
        try:
            parsed_start = datetime.fromisoformat(start_date)
            query = query.where(
                or_(
                    EvidenceRecord.published_at >= parsed_start,
                    EvidenceRecord.event_date >= parsed_start,
                )
            )
        except ValueError:
            pass

    if end_date:
        try:
            parsed_end = datetime.fromisoformat(end_date)
            query = query.where(
                or_(
                    EvidenceRecord.published_at <= parsed_end,
                    EvidenceRecord.event_date <= parsed_end,
                )
            )
        except ValueError:
            pass

    # Total count query
    count_subquery = query.with_only_columns(func.count(EvidenceRecord.id)).order_by(None)
    total_result = await db.execute(count_subquery)
    total_count = total_result.scalar_one()

    # Sorting
    sort_column = getattr(EvidenceRecord, sort_by, EvidenceRecord.published_at)
    order_fn = desc if sort_order == "desc" else asc
    query = query.order_by(order_fn(sort_column)).limit(limit).offset(offset)

    result = await db.execute(query)
    records = result.scalars().all()

    # Get distinct categories for filtering UI
    cat_res = await db.execute(
        select(EvidenceRecord.category, func.count(EvidenceRecord.id))
        .group_by(EvidenceRecord.category)
        .order_by(func.count(EvidenceRecord.id).desc())
    )
    categories = [{"name": row[0], "count": row[1]} for row in cat_res.all()]

    items = []
    for r in records:
        d = r.to_dict()
        if r.source:
            d["source_publisher"] = r.source.publisher
            d["source_type"] = r.source.source_type
        items.append(d)

    return {
        "evidence": items,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "categories": categories,
    }


@router.get("/{evidence_id}", summary="Evidence record full detail")
async def get_evidence(evidence_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EvidenceRecord)
        .options(
            selectinload(EvidenceRecord.source),
            selectinload(EvidenceRecord.claims),
        )
        .where(EvidenceRecord.id == evidence_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Evidence record not found")

    data = record.to_dict()

    # Source information
    if record.source:
        data["source"] = record.source.to_dict()
    else:
        data["source"] = None

    # Claims
    data["claims"] = [c.to_dict() for c in record.claims]

    # Relations (both outgoing and incoming)
    outgoing_res = await db.execute(
        select(EvidenceRelation, EvidenceRecord.title, EvidenceRecord.category)
        .join(EvidenceRecord, EvidenceRecord.id == EvidenceRelation.target_evidence_id)
        .where(EvidenceRelation.source_evidence_id == evidence_id)
    )
    outgoing_relations = [
        {
            **rel.to_dict(),
            "related_evidence_id": rel.target_evidence_id,
            "related_title": target_title,
            "related_category": target_category,
            "direction": "outgoing",
        }
        for rel, target_title, target_category in outgoing_res.all()
    ]

    incoming_res = await db.execute(
        select(EvidenceRelation, EvidenceRecord.title, EvidenceRecord.category)
        .join(EvidenceRecord, EvidenceRecord.id == EvidenceRelation.source_evidence_id)
        .where(EvidenceRelation.target_evidence_id == evidence_id)
    )
    incoming_relations = [
        {
            **rel.to_dict(),
            "related_evidence_id": rel.source_evidence_id,
            "related_title": src_title,
            "related_category": src_category,
            "direction": "incoming",
        }
        for rel, src_title, src_category in incoming_res.all()
    ]

    data["relations"] = outgoing_relations + incoming_relations

    # Review events (audit trail)
    review_res = await db.execute(
        select(ReviewEvent)
        .where(ReviewEvent.evidence_id == evidence_id)
        .order_by(ReviewEvent.created_at.desc())
    )
    data["review_history"] = [rev.to_dict() for rev in review_res.scalars().all()]

    return data


@router.get("/{evidence_id}/relations", summary="List evidence relations")
async def get_evidence_relations(evidence_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EvidenceRecord).where(EvidenceRecord.id == evidence_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Evidence record not found")

    outgoing_res = await db.execute(
        select(EvidenceRelation, EvidenceRecord.title, EvidenceRecord.category)
        .join(EvidenceRecord, EvidenceRecord.id == EvidenceRelation.target_evidence_id)
        .where(EvidenceRelation.source_evidence_id == evidence_id)
    )
    outgoing = [
        {
            **rel.to_dict(),
            "related_evidence_id": rel.target_evidence_id,
            "related_title": target_title,
            "related_category": target_category,
            "direction": "outgoing",
        }
        for rel, target_title, target_category in outgoing_res.all()
    ]

    incoming_res = await db.execute(
        select(EvidenceRelation, EvidenceRecord.title, EvidenceRecord.category)
        .join(EvidenceRecord, EvidenceRecord.id == EvidenceRelation.source_evidence_id)
        .where(EvidenceRelation.target_evidence_id == evidence_id)
    )
    incoming = [
        {
            **rel.to_dict(),
            "related_evidence_id": rel.source_evidence_id,
            "related_title": src_title,
            "related_category": src_category,
            "direction": "incoming",
        }
        for rel, src_title, src_category in incoming_res.all()
    ]

    return {"relations": outgoing + incoming, "total": len(outgoing) + len(incoming)}


@router.post("/{evidence_id}/relations", status_code=201, summary="Create evidence relation")
async def create_evidence_relation(
    evidence_id: str,
    payload: EvidenceRelationCreate,
    db: AsyncSession = Depends(get_db),
):
    if payload.relation_type not in RELATION_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid relation_type. Must be one of: {', '.join(RELATION_TYPES)}",
        )

    if evidence_id == payload.target_evidence_id:
        raise HTTPException(status_code=400, detail="Cannot relate evidence record to itself")

    # Verify both records exist
    src_res = await db.execute(select(EvidenceRecord).where(EvidenceRecord.id == evidence_id))
    if not src_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Source evidence record not found")

    tgt_res = await db.execute(select(EvidenceRecord).where(EvidenceRecord.id == payload.target_evidence_id))
    if not tgt_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Target evidence record not found")

    relation = EvidenceRelation(
        id=str(uuid.uuid4()),
        source_evidence_id=evidence_id,
        target_evidence_id=payload.target_evidence_id,
        relation_type=payload.relation_type,
        review_status="active",
        created_at=datetime.now(timezone.utc),
    )
    db.add(relation)
    await db.commit()

    return relation.to_dict()


@router.get("/{evidence_id}/history", summary="Get evidence correction and review history")
async def get_evidence_history(evidence_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EvidenceRecord).where(EvidenceRecord.id == evidence_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Evidence record not found")

    events_res = await db.execute(
        select(ReviewEvent)
        .where(ReviewEvent.evidence_id == evidence_id)
        .order_by(ReviewEvent.created_at.desc())
    )
    events = events_res.scalars().all()
    return {"history": [e.to_dict() for e in events], "total": len(events)}


@router.post("/{evidence_id}/review", summary="Submit review or correction")
async def submit_evidence_review(
    evidence_id: str,
    payload: EvidenceReviewCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(EvidenceRecord).where(EvidenceRecord.id == evidence_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Evidence record not found")

    previous_values = {
        "review_status": record.review_status,
        "category": record.category,
    }

    if payload.new_review_status:
        record.review_status = payload.new_review_status

    if payload.new_category:
        record.category = payload.new_category

    record.updated_at = datetime.now(timezone.utc)

    event = ReviewEvent(
        id=str(uuid.uuid4()),
        evidence_id=evidence_id,
        action=payload.action,
        reason=payload.reason,
        reviewer=payload.reviewer or "community_reviewer",
        previous_values=previous_values,
        created_at=datetime.now(timezone.utc),
    )
    db.add(event)
    await db.commit()

    return {
        "message": "Review event recorded successfully",
        "review_event": event.to_dict(),
        "evidence_id": evidence_id,
        "current_status": record.review_status,
        "current_category": record.category,
    }


@router.get("/{evidence_id}/provenance", summary="Get evidence provenance metadata")
async def get_evidence_provenance(evidence_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EvidenceRecord)
        .options(
            selectinload(EvidenceRecord.source),
            selectinload(EvidenceRecord.claims),
        )
        .where(EvidenceRecord.id == evidence_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Evidence record not found")

    model_info = None
    if record.claims:
        first_claim = record.claims[0]
        model_info = {
            "extraction_model": first_claim.extraction_model,
            "model_revision": first_claim.model_revision,
            "schema_version": first_claim.schema_version,
        }

    return {
        "evidence_id": record.id,
        "title": record.title,
        "source": {
            "id": record.source.id if record.source else record.source_id,
            "name": record.source.name if record.source else None,
            "publisher": record.source.publisher if record.source else None,
            "source_url": record.source.source_url if record.source else None,
            "license": record.source.license if record.source else None,
            "attribution": record.source.attribution if record.source else None,
            "authority_classification": record.source.authority_classification if record.source else None,
        },
        "timestamps": {
            "event_date": record.event_date.isoformat() if record.event_date else None,
            "published_at": record.published_at.isoformat() if record.published_at else None,
            "retrieved_at": record.retrieved_at.isoformat() if record.retrieved_at else None,
            "processed_at": record.processed_at.isoformat() if record.processed_at else None,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        },
        "geocoding": {
            "original_location_text": record.original_location_text,
            "geocoding_precision": record.geocoding_precision,
        },
        "integrity": {
            "canonical_digest": record.canonical_digest,
            "is_synthetic": record.is_synthetic,
            "review_status": record.review_status,
        },
        "ai_extraction": model_info,
        "limitations": record.limitations or [],
    }


@router.post("/{evidence_id}/verify", summary="Verify evidence integrity (TrustLayer)")
async def verify_evidence(evidence_id: str, db: AsyncSession = Depends(get_db)):
    """
    TrustLayer verification receipt — Phase 6.

    Steps:
    1. Fetch evidence record from DB.
    2. Re-compute SHA-256 canonical digest on the fly.
    3. Compare against stored canonical_digest (tamper detection).
    4. Look up Merkle inclusion proof in anchor_leaves table.
    5. Validate the Merkle proof against the batch root.
    6. Return full verification receipt.

    Note: blockchain verification confirms digest integrity, not truth of claims.
    """
    from localitylens.db.models import AnchorBatch, AnchorLeaf
    from localitylens.integrity.merkle import (
        compute_evidence_digest,
        verify_inclusion_proof,
    )

    result = await db.execute(select(EvidenceRecord).where(EvidenceRecord.id == evidence_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Evidence record not found")

    rec_dict = record.to_dict()
    fresh_digest = compute_evidence_digest(rec_dict)

    # Tamper detection: compare fresh digest to stored digest
    stored_digest = record.canonical_digest
    digest_matches = (stored_digest == fresh_digest) if stored_digest else None

    # Look up Merkle inclusion proof
    leaf_result = await db.execute(
        select(AnchorLeaf).where(AnchorLeaf.evidence_id == evidence_id).limit(1)
    )
    leaf = leaf_result.scalar_one_or_none()

    merkle_verified = False
    merkle_proof = None
    batch_info = None

    if leaf and leaf.merkle_proof:
        # Reconstruct proof dict and verify
        proof_dict = {
            "leaf": leaf.leaf_digest,
            "root": "",  # will fill from batch
            "proof": leaf.merkle_proof,
        }
        batch_result = await db.execute(
            select(AnchorBatch).where(AnchorBatch.id == leaf.batch_id)
        )
        batch = batch_result.scalar_one_or_none()
        if batch and batch.merkle_root:
            proof_dict["root"] = batch.merkle_root
            try:
                merkle_verified = verify_inclusion_proof(proof_dict)
            except Exception:
                merkle_verified = False

            batch_info = {
                "batch_id": batch.id,
                "merkle_root": batch.merkle_root,
                "leaf_count": batch.leaf_count,
                "transaction_hash": batch.transaction_hash,
                "block_number": batch.block_number,
                "verification_status": batch.verification_status,
            }
            merkle_proof = {
                "leaf_index": leaf.leaf_index,
                "leaf_digest": leaf.leaf_digest,
                "proof_steps": leaf.merkle_proof,
            }

    # Determine overall verification status
    if digest_matches is None:
        status = "no_digest"
        message = "No canonical digest has been generated for this record yet."
    elif not digest_matches:
        status = "tampered"
        message = "WARNING: Recomputed digest does not match stored digest. Record may have been modified."
    elif leaf and merkle_verified:
        status = "merkle_verified"
        message = "Digest verified and Merkle inclusion proof is valid."
    elif leaf and not merkle_verified:
        status = "merkle_proof_invalid"
        message = "Digest matches but Merkle proof verification failed."
    else:
        status = "digest_valid_not_anchored"
        message = "Digest matches stored value. Record has not been anchored to a Merkle batch yet."

    return {
        "evidence_id": evidence_id,
        "fresh_digest": fresh_digest,
        "stored_digest": stored_digest,
        "digest_matches": digest_matches,
        "verification_status": status,
        "message": message,
        "merkle_verified": merkle_verified,
        "merkle_proof": merkle_proof,
        "anchor_batch": batch_info,
        "chain_enabled": False,
        "note": "Blockchain verification confirms digest integrity, not truth of underlying claims.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

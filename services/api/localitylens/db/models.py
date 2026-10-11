"""
SQLAlchemy ORM models — all tables defined in the README database design.
Uses GeoAlchemy2 for PostGIS geometry columns.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from localitylens.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ─────────────────────────────────────────────────────────────────────────────
# Sources
# ─────────────────────────────────────────────────────────────────────────────

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)  # news, osm, govt, community
    publisher: Mapped[Optional[str]] = mapped_column(String(255))
    license: Mapped[Optional[str]] = mapped_column(String(255))
    attribution: Mapped[Optional[str]] = mapped_column(Text)
    authority_classification: Mapped[Optional[str]] = mapped_column(String(64))
    update_cadence: Mapped[Optional[str]] = mapped_column(String(64))
    last_successful_retrieval: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    evidence_records: Mapped[list["EvidenceRecord"]] = relationship(back_populates="source")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "source_url": self.source_url,
            "source_type": self.source_type,
            "publisher": self.publisher,
            "license": self.license,
            "attribution": self.attribution,
            "authority_classification": self.authority_classification,
            "update_cadence": self.update_cadence,
            "last_successful_retrieval": self.last_successful_retrieval.isoformat() if self.last_successful_retrieval else None,
            "status": self.status,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Evidence Records
# ─────────────────────────────────────────────────────────────────────────────

class EvidenceRecord(Base):
    __tablename__ = "evidence_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), nullable=False)
    source_item_id: Mapped[Optional[str]] = mapped_column(String(255))  # ID in original source system
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    original_location_text: Mapped[Optional[str]] = mapped_column(Text)
    geometry: Mapped[Optional[object]] = mapped_column(Geometry("GEOMETRY", srid=4326))
    geocoding_precision: Mapped[str] = mapped_column(String(32), default="unknown")
    event_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    retrieved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    review_status: Mapped[str] = mapped_column(String(32), default="pending")
    archive_reference: Mapped[Optional[str]] = mapped_column(Text)
    canonical_digest: Mapped[Optional[str]] = mapped_column(String(64))  # SHA-256 hex
    duplicate_cluster_id: Mapped[Optional[str]] = mapped_column(String)
    limitations: Mapped[Optional[list]] = mapped_column(JSONB)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)  # labelled demo records
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    source: Mapped["Source"] = relationship(back_populates="evidence_records")
    claims: Mapped[list["EvidenceClaim"]] = relationship(back_populates="evidence", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "source_item_id": self.source_item_id,
            "title": self.title,
            "summary": self.summary,
            "category": self.category,
            "original_location_text": self.original_location_text,
            "geocoding_precision": self.geocoding_precision,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "retrieved_at": self.retrieved_at.isoformat() if self.retrieved_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "review_status": self.review_status,
            "archive_reference": self.archive_reference,
            "canonical_digest": self.canonical_digest,
            "duplicate_cluster_id": self.duplicate_cluster_id,
            "limitations": self.limitations or [],
            "is_synthetic": self.is_synthetic,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "source_name": self.source.name if (hasattr(self, "source") and self.source) else None,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Evidence Claims
# ─────────────────────────────────────────────────────────────────────────────

class EvidenceClaim(Base):
    __tablename__ = "evidence_claims"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence_records.id"), nullable=False)
    claim_text: Mapped[Text] = mapped_column(Text, nullable=False)
    supporting_excerpt: Mapped[Optional[str]] = mapped_column(Text)
    extraction_model: Mapped[Optional[str]] = mapped_column(String(255))
    model_revision: Mapped[Optional[str]] = mapped_column(String(64))
    schema_version: Mapped[Optional[str]] = mapped_column(String(16))
    review_status: Mapped[str] = mapped_column(String(32), default="pending")

    evidence: Mapped["EvidenceRecord"] = relationship(back_populates="claims")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "evidence_id": self.evidence_id,
            "claim_text": self.claim_text,
            "supporting_excerpt": self.supporting_excerpt,
            "extraction_model": self.extraction_model,
            "model_revision": self.model_revision,
            "schema_version": self.schema_version,
            "review_status": self.review_status,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Evidence Relations
# ─────────────────────────────────────────────────────────────────────────────

RELATION_TYPES = ("supports", "contradicts", "duplicate_of", "supersedes", "derived_from")


class EvidenceRelation(Base):
    __tablename__ = "evidence_relations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    source_evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence_records.id"), nullable=False)
    target_evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence_records.id"), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    review_status: Mapped[str] = mapped_column(String(32), default="pending")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_evidence_id": self.source_evidence_id,
            "target_evidence_id": self.target_evidence_id,
            "relation_type": self.relation_type,
            "review_status": self.review_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Localities
# ─────────────────────────────────────────────────────────────────────────────

class Locality(Base):
    __tablename__ = "localities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    boundary_geometry: Mapped[Optional[object]] = mapped_column(Geometry("MULTIPOLYGON", srid=4326))
    boundary_source: Mapped[Optional[str]] = mapped_column(Text)
    boundary_license: Mapped[Optional[str]] = mapped_column(String(255))
    alternative_names: Mapped[Optional[list]] = mapped_column(JSONB)
    locality_type: Mapped[Optional[str]] = mapped_column(String(64))  # sector, neighbourhood, ward

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "boundary_source": self.boundary_source,
            "boundary_license": self.boundary_license,
            "alternative_names": self.alternative_names or [],
            "locality_type": self.locality_type,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Dataset Manifests
# ─────────────────────────────────────────────────────────────────────────────

class DatasetManifest(Base):
    __tablename__ = "dataset_manifests"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    dataset_identifier: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    publisher: Mapped[Optional[str]] = mapped_column(String(255))
    original_url: Mapped[Optional[str]] = mapped_column(Text)
    license: Mapped[Optional[str]] = mapped_column(String(255))
    attribution: Mapped[Optional[str]] = mapped_column(Text)
    retrieval_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    geographic_coverage: Mapped[Optional[str]] = mapped_column(Text)
    temporal_coverage: Mapped[Optional[str]] = mapped_column(Text)
    imported_fields: Mapped[Optional[list]] = mapped_column(JSONB)
    transformations: Mapped[Optional[list]] = mapped_column(JSONB)
    update_cadence: Mapped[Optional[str]] = mapped_column(String(64))
    redistribution_permitted: Mapped[Optional[bool]] = mapped_column(Boolean)
    known_limitations: Mapped[Optional[list]] = mapped_column(JSONB)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "dataset_identifier": self.dataset_identifier,
            "name": self.name,
            "publisher": self.publisher,
            "original_url": self.original_url,
            "license": self.license,
            "attribution": self.attribution,
            "retrieval_timestamp": self.retrieval_timestamp.isoformat() if self.retrieval_timestamp else None,
            "geographic_coverage": self.geographic_coverage,
            "temporal_coverage": self.temporal_coverage,
            "imported_fields": self.imported_fields or [],
            "transformations": self.transformations or [],
            "update_cadence": self.update_cadence,
            "redistribution_permitted": self.redistribution_permitted,
            "known_limitations": self.known_limitations or [],
        }


# ─────────────────────────────────────────────────────────────────────────────
# Ingestion Jobs
# ─────────────────────────────────────────────────────────────────────────────

class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    source_id: Mapped[Optional[str]] = mapped_column(ForeignKey("sources.id"))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    records_created: Mapped[int] = mapped_column(Integer, default=0)
    records_skipped: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


# ─────────────────────────────────────────────────────────────────────────────
# Anchor Batches (TrustLayer)
# ─────────────────────────────────────────────────────────────────────────────

class AnchorBatch(Base):
    __tablename__ = "anchor_batches"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    batch_identifier: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    merkle_root: Mapped[Optional[str]] = mapped_column(String(64))
    chain_id: Mapped[Optional[str]] = mapped_column(String(32))
    contract_address: Mapped[Optional[str]] = mapped_column(String(64))
    leaf_count: Mapped[int] = mapped_column(Integer, default=0)
    transaction_hash: Mapped[Optional[str]] = mapped_column(String(66))
    block_number: Mapped[Optional[int]] = mapped_column(Integer)
    canonicalisation_version: Mapped[Optional[str]] = mapped_column(String(16))
    verification_status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    leaves: Mapped[list["AnchorLeaf"]] = relationship(back_populates="batch")


class AnchorLeaf(Base):
    __tablename__ = "anchor_leaves"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    batch_id: Mapped[str] = mapped_column(ForeignKey("anchor_batches.id"), nullable=False)
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence_records.id"), nullable=False)
    leaf_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    merkle_proof: Mapped[Optional[list]] = mapped_column(JSONB)
    leaf_index: Mapped[Optional[int]] = mapped_column(Integer)

    batch: Mapped["AnchorBatch"] = relationship(back_populates="leaves")


# ─────────────────────────────────────────────────────────────────────────────
# Review Events (audit trail)
# ─────────────────────────────────────────────────────────────────────────────

class ReviewEvent(Base):
    __tablename__ = "review_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    evidence_id: Mapped[str] = mapped_column(ForeignKey("evidence_records.id"), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    reviewer: Mapped[Optional[str]] = mapped_column(String(255))
    previous_values: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "evidence_id": self.evidence_id,
            "action": self.action,
            "reason": self.reason,
            "reviewer": self.reviewer,
            "previous_values": self.previous_values,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

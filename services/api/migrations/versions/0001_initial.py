"""
Initial migration — creates all LocalityLens tables with PostGIS extension.

Revision: 0001
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")  # pgvector, optional

    # sources
    op.create_table(
        "sources",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(64), nullable=False),
        sa.Column("publisher", sa.String(255)),
        sa.Column("license", sa.String(255)),
        sa.Column("attribution", sa.Text()),
        sa.Column("authority_classification", sa.String(64)),
        sa.Column("update_cadence", sa.String(64)),
        sa.Column("last_successful_retrieval", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(32), server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    # evidence_records
    op.create_table(
        "evidence_records",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("source_id", sa.String(), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("source_item_id", sa.String(255)),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("summary", sa.Text()),
        sa.Column("category", sa.String(64), nullable=False),
        sa.Column("original_location_text", sa.Text()),
        sa.Column("geometry", Geometry("GEOMETRY", srid=4326)),
        sa.Column("geocoding_precision", sa.String(32), server_default="unknown"),
        sa.Column("event_date", sa.DateTime(timezone=True)),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("retrieved_at", sa.DateTime(timezone=True)),
        sa.Column("processed_at", sa.DateTime(timezone=True)),
        sa.Column("review_status", sa.String(32), server_default="pending"),
        sa.Column("archive_reference", sa.Text()),
        sa.Column("canonical_digest", sa.String(64)),
        sa.Column("duplicate_cluster_id", sa.String()),
        sa.Column("limitations", JSONB()),
        sa.Column("is_synthetic", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_category", "evidence_records", ["category"])
    op.create_index("ix_evidence_published_at", "evidence_records", ["published_at"])
    op.create_index("ix_evidence_review_status", "evidence_records", ["review_status"])

    # evidence_claims
    op.create_table(
        "evidence_claims",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("evidence_id", sa.String(), sa.ForeignKey("evidence_records.id"), nullable=False),
        sa.Column("claim_text", sa.Text(), nullable=False),
        sa.Column("supporting_excerpt", sa.Text()),
        sa.Column("extraction_model", sa.String(255)),
        sa.Column("model_revision", sa.String(64)),
        sa.Column("schema_version", sa.String(16)),
        sa.Column("review_status", sa.String(32), server_default="pending"),
        sa.PrimaryKeyConstraint("id"),
    )

    # evidence_relations
    op.create_table(
        "evidence_relations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("source_evidence_id", sa.String(), sa.ForeignKey("evidence_records.id"), nullable=False),
        sa.Column("target_evidence_id", sa.String(), sa.ForeignKey("evidence_records.id"), nullable=False),
        sa.Column("relation_type", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("review_status", sa.String(32), server_default="pending"),
        sa.PrimaryKeyConstraint("id"),
    )

    # localities
    op.create_table(
        "localities",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("boundary_geometry", Geometry("MULTIPOLYGON", srid=4326)),
        sa.Column("boundary_source", sa.Text()),
        sa.Column("boundary_license", sa.String(255)),
        sa.Column("alternative_names", JSONB()),
        sa.Column("locality_type", sa.String(64)),
        sa.PrimaryKeyConstraint("id"),
    )

    # dataset_manifests
    op.create_table(
        "dataset_manifests",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("dataset_identifier", sa.String(255), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("publisher", sa.String(255)),
        sa.Column("original_url", sa.Text()),
        sa.Column("license", sa.String(255)),
        sa.Column("attribution", sa.Text()),
        sa.Column("retrieval_timestamp", sa.DateTime(timezone=True)),
        sa.Column("geographic_coverage", sa.Text()),
        sa.Column("temporal_coverage", sa.Text()),
        sa.Column("imported_fields", JSONB()),
        sa.Column("transformations", JSONB()),
        sa.Column("update_cadence", sa.String(64)),
        sa.Column("redistribution_permitted", sa.Boolean()),
        sa.Column("known_limitations", JSONB()),
        sa.PrimaryKeyConstraint("id"),
    )

    # ingestion_jobs
    op.create_table(
        "ingestion_jobs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("idempotency_key", sa.String(255), unique=True),
        sa.Column("source_id", sa.String(), sa.ForeignKey("sources.id")),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("records_processed", sa.Integer(), server_default="0"),
        sa.Column("records_created", sa.Integer(), server_default="0"),
        sa.Column("records_skipped", sa.Integer(), server_default="0"),
        sa.Column("error", sa.Text()),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    # anchor_batches
    op.create_table(
        "anchor_batches",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("batch_identifier", sa.String(255), nullable=False, unique=True),
        sa.Column("merkle_root", sa.String(64)),
        sa.Column("chain_id", sa.String(32)),
        sa.Column("contract_address", sa.String(64)),
        sa.Column("leaf_count", sa.Integer(), server_default="0"),
        sa.Column("transaction_hash", sa.String(66)),
        sa.Column("block_number", sa.Integer()),
        sa.Column("canonicalisation_version", sa.String(16)),
        sa.Column("verification_status", sa.String(32), server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    # anchor_leaves
    op.create_table(
        "anchor_leaves",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("batch_id", sa.String(), sa.ForeignKey("anchor_batches.id"), nullable=False),
        sa.Column("evidence_id", sa.String(), sa.ForeignKey("evidence_records.id"), nullable=False),
        sa.Column("leaf_digest", sa.String(64), nullable=False),
        sa.Column("merkle_proof", JSONB()),
        sa.Column("leaf_index", sa.Integer()),
        sa.PrimaryKeyConstraint("id"),
    )

    # review_events
    op.create_table(
        "review_events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("evidence_id", sa.String(), sa.ForeignKey("evidence_records.id"), nullable=False),
        sa.Column("action", sa.String(64), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("reviewer", sa.String(255)),
        sa.Column("previous_values", JSONB()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("review_events")
    op.drop_table("anchor_leaves")
    op.drop_table("anchor_batches")
    op.drop_table("ingestion_jobs")
    op.drop_table("dataset_manifests")
    op.drop_table("localities")
    op.drop_table("evidence_relations")
    op.drop_table("evidence_claims")
    op.drop_table("evidence_records")
    op.drop_table("sources")

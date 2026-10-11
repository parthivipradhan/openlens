#!/usr/bin/env python3
"""
scripts/build_merkle_batch.py — Phase 6 TrustLayer

Fetches all evidence records, computes SHA-256 canonical digests,
builds a Merkle tree, and stores the batch in the database.

Usage:
  python scripts/build_merkle_batch.py [--dry-run]

Rules (AGENTS.md):
  - Only Merkle roots are stored on-chain (when chain is enabled).
  - No personal data or raw evidence goes on-chain.
  - Private keys stay server-side only.
  - Blockchain confirmation confirms digest integrity, not truth of claims.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import os

# Allow running from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "services", "api"))

import structlog
from sqlalchemy import select

from localitylens.core.config import settings
from localitylens.core.logging import setup_logging
from localitylens.db.session import AsyncSessionLocal, init_db
from localitylens.db.models import AnchorBatch, AnchorLeaf, EvidenceRecord
from localitylens.integrity.merkle import (
    build_merkle_tree,
    compute_evidence_digest,
    generate_inclusion_proof,
)

setup_logging()
log = structlog.get_logger(__name__)


async def build_batch(dry_run: bool = False) -> None:
    await init_db()

    async with AsyncSessionLocal() as db:
        # Fetch all non-rejected evidence records
        result = await db.execute(
            select(EvidenceRecord).where(EvidenceRecord.review_status != "rejected")
        )
        records = result.scalars().all()

        if not records:
            log.warning("No evidence records found. Batch not created.")
            return

        log.info("Building Merkle batch", record_count=len(records))

        # Compute digests and update canonical_digest on each record
        digests: list[str] = []
        id_to_digest: dict[str, str] = {}

        for record in records:
            digest = compute_evidence_digest(record.to_dict())
            id_to_digest[record.id] = digest
            digests.append(digest)

            if not dry_run and record.canonical_digest != digest:
                record.canonical_digest = digest

        # Build Merkle tree
        tree = build_merkle_tree(digests)
        log.info("Merkle tree built", root=tree["root"], leaves=tree["leaf_count"])

        if dry_run:
            print(f"\n[DRY RUN] Merkle root: {tree['root']}")
            print(f"[DRY RUN] Leaf count:  {tree['leaf_count']}")
            print("[DRY RUN] No changes written to database.")
            return

        # Create batch record
        import uuid
        from datetime import datetime, timezone
        batch_identifier = f"batch-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        batch = AnchorBatch(
            id=str(uuid.uuid4()),
            batch_identifier=batch_identifier,
            merkle_root=tree["root"],
            leaf_count=tree["leaf_count"],
            canonicalisation_version="v1",
            verification_status="pending",
        )
        db.add(batch)
        await db.flush()  # get batch.id

        # Create leaf records with inclusion proofs
        leaves_hex = tree["levels"][0]
        for i, record in enumerate(records):
            digest = id_to_digest[record.id]
            proof = generate_inclusion_proof(digest, tree)
            leaf = AnchorLeaf(
                id=str(uuid.uuid4()),
                batch_id=batch.id,
                evidence_id=record.id,
                leaf_digest=digest,
                leaf_index=i,
                merkle_proof=proof["proof"] if proof else [],
            )
            db.add(leaf)

        await db.commit()
        log.info(
            "Merkle batch committed",
            batch_id=batch.id,
            batch_identifier=batch_identifier,
            root=tree["root"],
            leaves=tree["leaf_count"],
        )
        print(f"\n✅ Merkle batch created: {batch_identifier}")
        print(f"   Root: {tree['root']}")
        print(f"   Leaves: {tree['leaf_count']}")
        print("\nTo anchor on-chain, configure CHAIN_ENABLED=true and CHAIN_RPC_URL.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Merkle anchor batch for all evidence records.")
    parser.add_argument("--dry-run", action="store_true", help="Compute without writing to database")
    args = parser.parse_args()
    asyncio.run(build_batch(dry_run=args.dry_run))


if __name__ == "__main__":
    main()

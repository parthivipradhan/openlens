#!/usr/bin/env python3
"""
scripts/verify_receipt.py — Phase 6 TrustLayer

Verify a LocalityLens evidence record's integrity using its stored Merkle proof.

Usage:
  python scripts/verify_receipt.py <evidence_id>

Returns:
  0 — digest valid and Merkle proof passes
  1 — tampered or proof failed
  2 — not anchored (digest valid, no Merkle batch)
  3 — no digest stored
"""

from __future__ import annotations

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "services", "api"))


async def verify(evidence_id: str) -> int:
    from sqlalchemy import select
    from localitylens.core.logging import setup_logging
    from localitylens.db.session import AsyncSessionLocal, init_db
    from localitylens.db.models import AnchorBatch, AnchorLeaf, EvidenceRecord
    from localitylens.integrity.merkle import (
        compute_evidence_digest,
        verify_inclusion_proof,
    )

    setup_logging()
    await init_db()

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(EvidenceRecord).where(EvidenceRecord.id == evidence_id)
        )
        record = result.scalar_one_or_none()
        if not record:
            print(f"❌ Evidence record '{evidence_id}' not found.")
            return 1

        fresh_digest = compute_evidence_digest(record.to_dict())
        stored_digest = record.canonical_digest

        print(f"\nEvidence ID:    {evidence_id}")
        print(f"Title:          {record.title[:80]}")
        print(f"Fresh digest:   {fresh_digest}")
        print(f"Stored digest:  {stored_digest or 'None'}")

        if not stored_digest:
            print("\n⚠️  No canonical digest stored for this record.")
            return 3

        if fresh_digest != stored_digest:
            print("\n🚨 TAMPER DETECTED: Recomputed digest does not match stored digest!")
            return 1

        print("\n✅ Digest matches stored value.")

        # Check Merkle proof
        leaf_result = await db.execute(
            select(AnchorLeaf).where(AnchorLeaf.evidence_id == evidence_id).limit(1)
        )
        leaf = leaf_result.scalar_one_or_none()

        if not leaf or not leaf.merkle_proof:
            print("⚠️  Not yet anchored to a Merkle batch.")
            return 2

        batch_result = await db.execute(
            select(AnchorBatch).where(AnchorBatch.id == leaf.batch_id)
        )
        batch = batch_result.scalar_one_or_none()

        if not batch or not batch.merkle_root:
            print("⚠️  Anchor batch has no Merkle root.")
            return 2

        proof_dict = {
            "leaf": leaf.leaf_digest,
            "root": batch.merkle_root,
            "proof": leaf.merkle_proof,
        }

        print(f"\nAnchor batch:   {batch.batch_identifier}")
        print(f"Merkle root:    {batch.merkle_root}")
        print(f"Leaf index:     {leaf.leaf_index}")

        try:
            valid = verify_inclusion_proof(proof_dict)
        except Exception as e:
            print(f"\n❌ Proof verification error: {e}")
            return 1

        if valid:
            print("\n✅ Merkle inclusion proof is VALID.")
            print("   Blockchain verification confirms digest integrity, not truth of claims.")
            return 0
        else:
            print("\n❌ Merkle inclusion proof FAILED verification.")
            return 1


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <evidence_id>")
        sys.exit(1)
    evidence_id = sys.argv[1]
    rc = asyncio.run(verify(evidence_id))
    sys.exit(rc)


if __name__ == "__main__":
    main()

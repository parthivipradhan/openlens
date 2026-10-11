#!/usr/bin/env python3
"""
scripts/demo_tamper.py — Phase 6 TrustLayer Tamper Detection Demo.

Demonstrates how LocalityLens cryptographically rejects any tampered evidence record:
1. Takes a genuine evidence record and computes its canonical SHA-256 digest.
2. Builds a Merkle root and proof.
3. Verifies that genuine record verifies 100% against the root.
4. Simulates a malicious edit (e.g., modifying 'category', 'event_date', or 'title').
5. Recomputes digest and shows proof verification failure (REJECTED).
"""

import os
import sys
from pathlib import Path

# Ensure services/api is in sys.path
API_DIR = Path(__file__).resolve().parent.parent / "services" / "api"
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from localitylens.integrity.merkle import (
    compute_evidence_digest,
    build_merkle_tree,
    generate_inclusion_proof,
    verify_inclusion_proof,
)


def run_tamper_demo():
    print("=" * 70)
    print(" LocalityLens TrustLayer — Cryptographic Tamper-Detection Demo")
    print("=" * 70)

    # 1. Genuine record
    genuine_record = {
        "id": "ev_demo_waterlogging_sec17",
        "source_id": "src_chandigarh_smartcity",
        "title": "Severe Waterlogging along Jan Marg Sector 17",
        "summary": "Water accumulation up to 1.5 ft observed during July torrential rainfall.",
        "category": "waterlogging",
        "original_location_text": "Jan Marg, Sector 17, Chandigarh",
        "event_date": "2024-07-15",
        "published_at": "2024-07-16T10:00:00Z",
        "is_synthetic": True,
    }

    other_record = {
        "id": "ev_demo_park_sec10",
        "source_id": "src_osm",
        "title": "Rose Garden Sector 16 Open Grounds",
        "summary": "Public botanical garden with 1600 rose varieties.",
        "category": "green_spaces",
        "original_location_text": "Sector 16, Chandigarh",
        "event_date": "2024-01-01",
        "published_at": "2024-01-01T00:00:00Z",
        "is_synthetic": True,
    }

    genuine_digest = compute_evidence_digest(genuine_record)
    other_digest = compute_evidence_digest(other_record)

    print(f"\n[1] Genuine record ID: {genuine_record['id']}")
    print(f"    Canonical SHA-256:  {genuine_digest}")

    # 2. Build Merkle tree and anchor root
    tree = build_merkle_tree([genuine_digest, other_digest])
    root = tree["root"]
    print(f"[2] Merkle Tree constructed with {tree['leaf_count']} leaves.")
    print(f"    Batch Merkle Root: {root}")

    # 3. Generate inclusion proof for genuine record
    proof = generate_inclusion_proof(genuine_digest, tree)
    assert proof is not None, "Failed to generate proof"
    print(f"[3] Inclusion proof generated ({len(proof['proof'])} sibling hashes).")

    # 4. Verify genuine record
    valid = verify_inclusion_proof(genuine_digest, proof["proof"], root)
    print(f"\n[4] Genuine record verification: {'PASSED (VERIFIED)' if valid else 'FAILED'}")
    assert valid, "Genuine record failed verification!"

    # 5. Tamper scenario: an adversary alters the severity or changes waterlogging to green_spaces
    tampered_record = dict(genuine_record)
    tampered_record["category"] = "green_spaces"  # Fraudulent change
    tampered_record["summary"] = "No waterlogging here, beautiful green lawn."

    tampered_digest = compute_evidence_digest(tampered_record)
    print(f"\n[5] Adversary modifies record: category='green_spaces'")
    print(f"    New tampered digest: {tampered_digest}")
    print(f"    Original digest:     {genuine_digest}")

    # 6. Verify tampered record against original anchor root
    tamper_result = verify_inclusion_proof(tampered_digest, proof["proof"], root)
    print(f"\n[6] Tampered record verification against anchor root:")
    if not tamper_result:
        print("    [!] TAMPER DETECTED: Verification REJECTED with cryptographic certainty.")
        print("    [!] The hash chain does not resolve to the anchored Merkle root.")
    else:
        print("    [X] Unexpected pass — tamper was not caught!")
        sys.exit(1)

    print("\n" + "=" * 70)
    print(" Conclusion: TrustLayer cryptographic proof guarantees data immutability.")
    print("=" * 70)
    return True


if __name__ == "__main__":
    run_tamper_demo()

"""
TrustLayer — SHA-256 digest generation and Merkle tree builder.

Rules (AGENTS.md):
- Store only Merkle roots on-chain. Never put personal data or raw evidence on-chain.
- Blockchain verification confirms digest integrity, not truth of underlying claims.
- Private keys stay server-side only.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


# ---------------------------------------------------------------------------
# Canonical digest helpers
# ---------------------------------------------------------------------------

def _canonical_json(data: dict[str, Any]) -> bytes:
    """
    Produce deterministic, domain-separated JSON bytes for hashing.
    Uses sorted keys and no whitespace for reproducibility across environments.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def compute_evidence_digest(record: dict[str, Any]) -> str:
    """
    Compute SHA-256 digest of the canonical evidence record representation.

    Only stable, non-mutable fields are included in the canonical form.
    Mutable operational fields (processed_at, review_status) are excluded
    so that routine updates do not invalidate existing digests.
    """
    canonical = {
        "id": record["id"],
        "source_id": record["source_id"],
        "title": record["title"],
        "summary": record.get("summary", ""),
        "category": record["category"],
        "original_location_text": record.get("original_location_text", ""),
        "event_date": record.get("event_date", ""),
        "published_at": record.get("published_at", ""),
        "is_synthetic": record.get("is_synthetic", False),
    }
    raw = _canonical_json(canonical)
    # Domain separator prevents cross-context hash collision
    domain = b"localitylens:evidence:v1:"
    return hashlib.sha256(domain + raw).hexdigest()


# ---------------------------------------------------------------------------
# Merkle tree
# ---------------------------------------------------------------------------

def _hash_pair(left: bytes, right: bytes) -> bytes:
    """Hash two sibling nodes together, sorted to ensure determinism."""
    a, b = sorted([left, right])
    return hashlib.sha256(b"localitylens:merkle:" + a + b":" + b).digest()


def _hex_to_bytes(h: str) -> bytes:
    return bytes.fromhex(h)


def build_merkle_tree(leaf_digests: list[str]) -> dict[str, Any]:
    """
    Build a deterministic, binary Merkle tree from a list of leaf hex-digests.
    Returns the root digest and the full tree structure for proof generation.

    Rules:
    - If odd number of leaves, duplicate the last leaf (standard Bitcoin-style).
    - Domain-separated at each level.
    """
    if not leaf_digests:
        raise ValueError("Cannot build Merkle tree from empty leaf list.")

    leaves = [_hex_to_bytes(d) for d in leaf_digests]
    levels: list[list[bytes]] = [leaves]

    current = leaves
    while len(current) > 1:
        if len(current) % 2 == 1:
            current = current + [current[-1]]  # duplicate last leaf
        next_level = [_hash_pair(current[i], current[i + 1]) for i in range(0, len(current), 2)]
        levels.append(next_level)
        current = next_level

    root = current[0].hex()
    return {
        "root": root,
        "leaf_count": len(leaf_digests),
        "levels": [[node.hex() for node in level] for level in levels],
    }


def generate_inclusion_proof(leaf_digest: str, tree: dict[str, Any]) -> dict[str, Any] | None:
    """
    Generate a Merkle inclusion proof for a given leaf digest.
    Returns None if the leaf is not found in the tree.
    """
    levels_hex: list[list[str]] = tree["levels"]
    if not levels_hex:
        return None

    leaves = levels_hex[0]
    try:
        idx = leaves.index(leaf_digest)
    except ValueError:
        # May need to check duplicate last leaf
        return None

    proof_steps: list[dict[str, str]] = []
    current_idx = idx
    level_nodes = [_hex_to_bytes(h) for h in leaves]

    for level in levels_hex[:-1]:  # exclude root level
        nodes = [_hex_to_bytes(h) for h in level]
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])

        if current_idx % 2 == 0:
            sibling_idx = current_idx + 1
            side = "right"
        else:
            sibling_idx = current_idx - 1
            side = "left"

        proof_steps.append({
            "sibling": nodes[sibling_idx].hex(),
            "side": side,
        })
        current_idx //= 2

    return {
        "leaf": leaf_digest,
        "root": tree["root"],
        "proof": proof_steps,
    }


def verify_inclusion_proof(
    proof_or_leaf: dict[str, Any] | str,
    proof_steps: list[dict[str, str]] | None = None,
    expected_root: str | None = None,
) -> bool:
    """
    Recompute the Merkle root from a proof and verify it matches the stored root.
    Supports either:
      verify_inclusion_proof(proof_dict)
    OR
      verify_inclusion_proof(leaf_hex, proof_steps, expected_root)
    """
    if isinstance(proof_or_leaf, dict):
        leaf_hex = proof_or_leaf["leaf"]
        steps = proof_or_leaf["proof"]
        target_root = proof_or_leaf["root"]
    else:
        leaf_hex = proof_or_leaf
        steps = proof_steps or []
        target_root = expected_root or ""

    try:
        current = _hex_to_bytes(leaf_hex)
        for step in steps:
            sibling = _hex_to_bytes(step["sibling"])
            if step["side"] == "right":
                current = _hash_pair(current, sibling)
            else:
                current = _hash_pair(sibling, current)
        return current.hex() == target_root
    except Exception:
        return False

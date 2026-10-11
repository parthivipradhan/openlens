# TrustLayer — Trust Model

## Overview

LocalityLens uses a **TrustLayer** to provide cryptographic integrity guarantees for evidence records.
TrustLayer **does not** claim that evidence records are true — it guarantees that records have not been
silently modified after being ingested.

## Canonical Digest

Each evidence record is reduced to a **canonical JSON representation** using a deterministic,
domain-separated encoding:

```
domain = "localitylens:evidence:v1:"
digest = SHA-256(domain + canonical_json(record))
```

**Fields included in canonical form** (stable, non-mutable):
- `id`, `source_id`, `title`, `summary`, `category`
- `original_location_text`, `event_date`, `published_at`
- `is_synthetic`

**Fields excluded** (operational/mutable, would invalidate digests on routine updates):
- `processed_at`, `review_status`, `duplicate_cluster_id`

## Merkle Tree

Digests are aggregated into a **binary Merkle tree**:

- Leaves are SHA-256 digests of individual evidence records.
- Each internal node is `SHA-256("localitylens:merkle:" + sorted(left, right))`.
- Odd leaf counts: last leaf is duplicated (Bitcoin-style).
- Root is stored in the `anchor_batches` table.

The Merkle root is what is anchored to a blockchain (Phase 6+).

## What Blockchain Verification Proves

> **Blockchain verification confirms digest integrity, not truth of underlying claims.**

A valid Merkle proof means:
1. The evidence record's canonical digest was part of the Merkle batch.
2. The Merkle root was anchored on-chain at a known block.
3. The on-chain root matches the locally recomputed root.

It does **not** mean:
- The evidence is accurate or factually correct.
- The original source was reliable.
- The event described actually occurred.

## On-Chain Storage Policy

> Only Merkle roots are stored on-chain. **Never** personal data, raw evidence text, or user information.

## Tamper Detection

When `POST /api/v1/evidence/{id}/verify` is called:
1. The canonical digest is recomputed from the current DB state.
2. It is compared against the stored `canonical_digest`.
3. If they differ, the record is flagged as `"tampered"`.

## Limitations

- The current implementation does not perform live on-chain verification (`CHAIN_ENABLED=false` in demo mode).
- On-chain anchoring requires a funded wallet and a deployed `EvidenceRegistry` contract (Phase 6+).
- Private keys are kept server-side only — never exposed via API.
- Records ingested before the first Merkle batch was built will not have a stored digest.

## Versioning

Canonical form version: **v1** (tracked in `anchor_batches.canonicalisation_version`)

Any change to the canonical form schema must increment the version and re-anchor all records.

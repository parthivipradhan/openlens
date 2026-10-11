# LocalityLens — Hackathon Demo Script

> **Duration:** 4–5 minutes  
> **Audience:** Hackathon judges, municipal officials, civic researchers  
> **Topic:** Open-source AI neighbourhood intelligence with blockchain-verified integrity.

---

## Act 1: The Problem (0:00 – 0:45)

**Spoken:**
> "Finding out what a neighbourhood is actually like—before you move there, open a shop, or plan infrastructure—is broken.  
> Online reviews are biased, municipal reports are buried in PDFs, and generic AI chatbots hallucinate fake facts and imaginary park ratings.  
> Meet **LocalityLens**: an open-source neighbourhood intelligence platform that combines **deterministic geospatial queries**, **open-weight AI models**, and **cryptographic blockchain verification**."

**Visual:**
- Open `http://localhost:3000` — Show the **Evidence Explorer** tab.
- Point out the clean stat counters: Verified Records, Canonical Sources, Anchored Batches.

---

## Act 2: Evidence Explorer & Provenance (0:45 – 1:30)

**Spoken:**
> "Every claim in LocalityLens starts as an immutable evidence record.  
> Here in the Evidence Explorer, we see 20+ curated records across Chandigarh—from Central Pollution Control Board air monitors to municipal waterlogging reports and OpenStreetMap amenities.  
> Let's filter for **Waterlogging**."

**Actions:**
1. Click the **Waterlogging** category pill.
2. Click on the record: *"Severe Monsoon Waterlogging at Sector 17 Jan Marg Underpass"*.
3. Show the **Evidence Detail Modal**:
   - Highlight the separate date fields: `event_date`, `published_at`, `retrieved_at` (never conflated).
   - Show the **Original Location Text** preserved verbatim alongside geocoded coordinates.
   - Point to the **SHA-256 Digest**: `e3b0c44...`

---

## Act 3: Interactive Geospatial Map (1:30 – 2:15)

**Spoken:**
> "Civic data isn't just rows in a database; it has spatial context and spatial uncertainty."

**Actions:**
1. Switch to the **Interactive Map** tab.
2. Show the MapLibre GL dark-matter canvas centered on Chandigarh (Sectors 1 to 40).
3. Toggle category layers (e.g., toggle Public Transport on/off).
4. Hover over an evidence marker to display the rich hover card.
5. Highlight the **Uncertainty Circle**:
   > *"Notice the translucent circle around each pin? In LocalityLens, we explicitly render geographic uncertainty radius (e.g. 500m for sector-level mentions vs 50m for exact street addresses), so users are never misled by false precision."*

---

## Act 4: Grounded AI Assistant (2:15 – 3:00)

**Spoken:**
> "Next, let's look at the AI Assistant. Most LLMs hallucinate neighbourhood details. LocalityLens enforces a zero-fabrication contract."

**Actions:**
1. Switch to the **AI Assistant** tab.
2. Click the suggested prompt: *"Which sectors experience regular monsoon waterlogging and road closures?"*
3. Show the response:
   - Highlight the **Citations badge** (`[EV-1]`, `[EV-2]`) linking back to real evidence IDs.
   - Show the **Limitations disclosure**.
4. Test insufficient evidence: Ask *"What are the secret military missile bunkers in Sector 99?"*
5. Highlight the **Honest Abstention**:
   > *"Because no verified evidence exists, the model refuses to guess, returning an explicit insufficient-evidence warning rather than inventing answers."*

---

## Act 5: Locality Comparison Engine (3:00 – 3:45)

**Spoken:**
> "When comparing two neighbourhoods—say Sector 17 vs Sector 22—we don't use black-box AI rankings. We use deterministic scoring with transparent user weights."

**Actions:**
1. Switch to the **Locality Compare** tab.
2. Select **Sector 17** (City Center / Commercial) and **Sector 22** (Residential & Transit Hub).
3. Adjust the **Public Transport** slider to high and **Waterlogging** penalty to high.
4. Point out the live recalculated scores:
   > *"Scores are calculated by application code using real event counts and distances—not by an LLM prompt. Notice the missing-data warnings: if a sector lacks noise monitoring, the system transparently warns you instead of assuming zero."*

---

## Act 6: TrustLayer Cryptographic Verification (3:45 – 4:30)

**Spoken:**
> "Finally, how do you know no one altered this civic evidence for political or commercial reasons? That's our **TrustLayer**."

**Actions:**
1. Go back to an evidence record modal and click **Verify On-Chain Integrity**.
2. Run the live tamper demo in terminal:
   ```bash
   python scripts/demo_tamper.py
   ```
3. Show the terminal output:
   - Genuine record: canonical SHA-256 computed -> Merkle inclusion proof verified against batch root -> **PASSED**.
   - Malicious record with edited category: new digest computed -> Merkle verification fails -> **TAMPER DETECTED / REJECTED**.
4. Explain the architecture:
   > *"We never put private or raw data on-chain. Only the Merkle root is committed to our Solidity EvidenceRegistry contract. The math guarantees that even a 1-character alteration breaks verification instantly."*

---

## Closing (4:30 – 5:00)

**Spoken:**
> "LocalityLens proves that local intelligence can be **open**, **verifiable**, and **grounded in truth**.  
> Thank you! All code is open-source under the MIT license on GitHub."

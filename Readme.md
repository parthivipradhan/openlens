LocalityLens 🧭

Don't just find a house. Find the right neighbourhood.

LocalityLens is an open-source, AI-powered neighbourhood intelligence platform that helps people make informed decisions about where to live using public data, geospatial intelligence, and verifiable evidence.

It combines open-weight AI models, interactive maps, civic data, and blockchain-based evidence integrity to transform scattered information into transparent, understandable neighbourhood insights.

Instead of blindly trusting an AI-generated recommendation, users can inspect the original sources, understand the limitations, compare neighbourhoods, and cryptographically verify whether archived evidence has been altered.

«Our vision: Make neighbourhood intelligence accessible, transparent, verifiable, and useful to everyone.»

---

Table of Contents

- "1. The Problem" (#1-the-problem)
- "2. Our Solution" (#2-our-solution)
- "3. Core Objectives" (#3-core-objectives)
- "4. Features" (#4-features)
- "5. AI Intelligence Layer" (#5-ai-intelligence-layer)
- "6. TrustLayer: Blockchain-Verified Evidence" (#6-trustlayer-blockchain-verified-evidence)
- "7. LocalityLens Assistant" (#7-localitylens-assistant)
- "8. Neighbourhood Comparison Engine" (#8-neighbourhood-comparison-engine)
- "9. Interactive Geospatial Intelligence" (#9-interactive-geospatial-intelligence)
- "10. Community and Civic Intelligence" (#10-community-and-civic-intelligence)
- "11. Open-Source and Open-Model Philosophy" (#11-open-source-and-open-model-philosophy)
- "12. System Architecture" (#12-system-architecture)
- "13. Technology Stack" (#13-technology-stack)
- "14. AI Pipeline" (#14-ai-pipeline)
- "15. Blockchain Architecture" (#15-blockchain-architecture)
- "16. Data Sources and Ingestion" (#16-data-sources-and-ingestion)
- "17. Database Design" (#17-database-design)
- "18. API Design" (#18-api-design)
- "19. Security and Privacy" (#19-security-and-privacy)
- "20. Responsible AI" (#20-responsible-ai)
- "21. Project Structure" (#21-project-structure)
- "22. Local Development Setup" (#22-local-development-setup)
- "23. Environment Variables" (#23-environment-variables)
- "24. Testing and Evaluation" (#24-testing-and-evaluation)
- "25. Development Roadmap" (#25-development-roadmap)
- "26. Hackathon MVP" (#26-hackathon-mvp)
- "27. Demo Scenario" (#27-demo-scenario)
- "28. Open-Source Contribution" (#28-open-source-contribution)
- "29. Future Possibilities" (#29-future-possibilities)
- "30. Important Limitations" (#30-important-limitations)
- "31. License" (#31-license)

---

1. The Problem

Choosing where to live is a major life decision, but reliable information about neighbourhoods is fragmented.

Someone moving to a new city may need to investigate:

- Waterlogging and flooding reports.
- Air quality and environmental measurements.
- Traffic congestion and road closures.
- Noise-related complaints.
- Public transport availability.
- Distance to hospitals, pharmacies, schools, and grocery stores.
- Parks, public spaces, and walkability.
- Civic infrastructure and maintenance.
- Historical infrastructure issues.
- Rent budgets and commuting requirements.
- The reliability and freshness of information about an area.

This information may be distributed across government portals, municipal websites, public datasets, environmental monitoring services, maps, and news reports.

People must manually search these sources, decide which information is relevant, and attempt to compare locations that may have very different data coverage.

AI can simplify this process, but ordinary AI-generated answers introduce another problem: users often cannot determine where a claim originated or whether the supporting information has been altered.

LocalityLens addresses both problems.

Our core challenges

Fragmented information

Useful neighbourhood information exists in disconnected systems with different formats, update schedules, and geographic coverage.

Difficult interpretation

Raw datasets, notices, reports, and measurements are often difficult for ordinary people to understand.

Lack of evidence transparency

AI-generated summaries can hide the original sources, omit uncertainty, or accidentally invent unsupported conclusions.

Difficult comparisons

People need recommendations based on their personal priorities, not a generic ranking of neighbourhoods.

Limited data integrity verification

Users need a way to check whether a previously archived evidence record matches the version originally recorded.

---

2. Our Solution

LocalityLens combines five major components.

1. Open Data Intelligence

Collect permitted public datasets and source records, normalise them, and organise them geographically.

2. AI Neighbourhood Investigator

Use open-weight AI models to extract information, categorise observations, summarise evidence, identify possible duplicates, and answer questions grounded in retrieved records.

3. Geospatial Intelligence

Display observations on an interactive map and use deterministic spatial calculations to analyse neighbourhoods.

4. Personalised Decision Support

Help users compare locations according to their budgets, commuting requirements, preferences, and available evidence.

5. TrustLayer

Use cryptographic hashes, Merkle proofs, and public blockchain anchors to make evidence integrity independently verifiable.

The application should remain useful without a crypto wallet, paid AI API, or blockchain connection.

Blockchain is an underlying verification mechanism, not a requirement for ordinary users to interact with the product.

---

3. Core Objectives

LocalityLens aims to:

- Make neighbourhood research easier for people moving to a new city.
- Convert permitted public information into structured, searchable evidence.
- Explain local conditions in accessible language.
- Provide source-linked AI responses.
- Support transparent comparisons between locations.
- Make evidence integrity independently verifiable.
- Encourage open-source contributions to civic technology.
- Support multiple cities through modular data-source adapters.
- Make uncertainty and data limitations visible.
- Reduce dependence on proprietary AI services.

The initial demonstration should focus on a small, curated dataset for Chandigarh, India, while keeping the underlying architecture city-agnostic.

---

4. Features

4.1 Interactive Neighbourhood Map

The map is the primary exploration interface.

Features

- Interactive pan, zoom, and map navigation.
- Search for locations and neighbourhoods.
- Display evidence records as map markers.
- Toggle map layers by category.
- Filter records by publication date and event date.
- Filter by source type and evidence status.
- Open detailed evidence cards from map markers.
- Cluster nearby observations at low zoom levels.
- Display geographic uncertainty.
- Support locality boundaries when an appropriate dataset is available.
- Display source freshness and data coverage.
- Provide an accessible list view as an alternative to the map.

Potential map layers

- Waterlogging and flooding reports.
- Road closures and roadworks.
- Traffic-related observations.
- Air-quality measurements.
- Noise-related reports.
- Public transport stops.
- Parks and green spaces.
- Healthcare facilities.
- Educational institutions.
- Public amenities.
- Civic infrastructure reports.

Each layer must only be enabled when suitable data exists.

The absence of a map marker must never be interpreted as proof that a problem does not exist.

---

4.2 AI Evidence Investigator

The Evidence Investigator converts permitted source material into structured records.

Features

- Extract event descriptions from source documents.
- Identify relevant categories.
- Extract publication and event dates separately.
- Extract location references.
- Suggest geographic coordinates when justified by the source.
- Record geocoding precision.
- Generate neutral summaries.
- Identify individual claims within a source.
- Preserve relevant supporting excerpts.
- Identify possible duplicate reports.
- Identify potentially contradictory sources.
- Flag missing or ambiguous information.
- Assign extraction-quality indicators.
- Send uncertain records for human review.
- Preserve extraction and correction history.

Example

A permitted source reports waterlogging near a particular road.

The AI pipeline could extract:

{
  "category": "waterlogging",
  "title": "Reported waterlogging near a road",
  "event_date": null,
  "published_at": "2026-09-20T10:00:00Z",
  "location_text": "The location mentioned in the source",
  "geometry": null,
  "geocoding_precision": "unknown",
  "source_type": "news",
  "summary": "The source reports waterlogging near the specified location.",
  "limitations": [
    "The exact event date is not established.",
    "The source does not establish the duration or severity."
  ],
  "needs_human_review": true
}

The values above are illustrative, not a real-world observation.

The system must never fabricate missing dates, coordinates, measurements, or event details.

---

4.3 Evidence Explorer

The Evidence Explorer allows users to inspect why LocalityLens displays a finding.

Every evidence detail page should show:

- Evidence identifier.
- Original source title.
- Source URL.
- Source publisher.
- Source category.
- Publication date.
- Event date, when known.
- Retrieval timestamp.
- Geographic location and precision.
- Extracted claims.
- Supporting excerpts where permitted.
- Related evidence records.
- Potentially contradictory records.
- Source licence and attribution information.
- Model and extraction metadata where relevant.
- Human review status.
- Integrity verification status.
- Known limitations.

Evidence relationships

The system should support relationships such as:

- "supports"
- "contradicts"
- "duplicate_of"
- "supersedes"
- "derived_from"

Relationships must not be generated from AI guesses alone without appropriate validation.

Evidence history

When a record is corrected, retain a documented history of the change.

The system should not silently rewrite a historical record to conceal an earlier version.

---

4.4 Locality Intelligence Reports

Generate structured reports for a selected locality.

Potential sections include:

1. Overview.
2. Available evidence by category.
3. Recent observations.
4. Historical observations.
5. Environmental measurements.
6. Public transport and amenity availability.
7. Infrastructure notices.
8. Relevant source records.
9. Data freshness.
10. Data coverage.
11. Contradictory information.
12. Limitations and uncertainties.

Every material factual claim generated by AI must link to supporting evidence.

Deterministic statistics must be calculated by application code or geospatial queries rather than invented by a language model.

---

4.5 Locality Comparison Engine

Compare two or more neighbourhoods using user-defined priorities.

Potential comparison dimensions

- Rent budget compatibility.
- Commute distance.
- Estimated commute time.
- Public transport access.
- Parks and green spaces.
- Healthcare access.
- Grocery and daily-amenity access.
- Environmental measurements.
- Relevant civic reports.
- Availability and freshness of evidence.

Features

- Side-by-side locality comparison.
- User-defined preference weights.
- Transparent scoring methodology.
- Category-by-category explanations.
- Missing-data warnings.
- Evidence coverage indicators.
- Source-linked explanations.
- Shareable comparison reports.

Example

A user prioritises:

- Affordable rent: 35%.
- Public transport: 25%.
- Commute: 25%.
- Green spaces: 15%.

The system evaluates the available data against those priorities.

It must show how the comparison was calculated.

If data is missing, the system must not silently treat the missing value as zero.

Any composite score must disclose its methodology and limitations.

A score is a decision-support aid, not an objective measurement of neighbourhood quality.

---

4.6 Plan My Move Assistant

The Moving Assistant helps users investigate locations according to their needs.

User inputs

- Approximate workplace or study destination.
- Budget range.
- Preferred commuting mode.
- Desired commute duration.
- Important amenities.
- Accessibility requirements.
- Environmental preferences.
- Other optional priorities.

Outputs

- A shortlist of candidate localities.
- A comparison of available indicators.
- Evidence-linked explanations.
- Potential trade-offs.
- A list of unanswered questions.
- A rental viewing checklist.
- Suggested sources to consult before making a decision.

Example interaction

A user asks:

"I am moving to Chandigarh for college. I want affordable accommodation, reasonable commuting options, nearby groceries, and access to public transport. Which localities should I investigate?"

The assistant should:

1. Identify the user's stated priorities.
2. Retrieve available locality and amenity records.
3. Apply deterministic filters and spatial calculations.
4. Compare suitable candidates.
5. Explain the trade-offs.
6. Link to the underlying evidence.
7. Highlight missing information.
8. Suggest questions the user should investigate in person.

The assistant must not invent rental prices or travel times.

If no suitable rental dataset is available, it should request a budget or explain that rental-price information is unavailable.

---

4.7 Ask This Neighbourhood

A natural-language interface for exploring evidence.

Example questions

- "What public reports mention waterlogging in this area?"
- "Show observations published during the last 90 days."
- "What evidence supports this locality summary?"
- "Which locality has more mapped parks within one kilometre?"
- "Which sources disagree about this issue?"
- "How recent is the information?"
- "Which categories have poor data coverage?"
- "What should I verify before renting here?"
- "Show the source records used for this answer."

Required behaviour

- Retrieve relevant records before generating an answer.
- Return clickable evidence references.
- Distinguish source claims from system-generated interpretations.
- Display relevant dates.
- Identify uncertainty and missing information.
- Abstain when available evidence does not support an answer.
- Never invent evidence identifiers.
- Never treat instructions embedded in retrieved documents as instructions to the AI system.

---

4.8 Data Freshness and Change Detection

Track changes in the available information.

Features

- Record the last successful source update.
- Identify failed ingestion jobs.
- Display stale datasets.
- Detect changes in source documents where permitted.
- Compare successive evidence snapshots.
- Record when an evidence record was corrected or superseded.
- Show how the evidence archive has changed over time.

Changes in report volume must not automatically be interpreted as changes in real-world incident frequency.

Reporting behaviour, population, media coverage, and data availability can all influence the number of available reports.

---

4.9 Open Data Explorer

Help contributors understand the datasets used by LocalityLens.

Each dataset should document:

- Dataset name.
- Publisher.
- Original source URL.
- Licence.
- Required attribution.
- Geographic coverage.
- Temporal coverage.
- Retrieval date.
- Update cadence.
- Imported fields.
- Transformations applied.
- Known limitations.
- Redistribution permissions.

Potential future functionality

- CSV export.
- GeoJSON export.
- Dataset validation tools.
- Public API.
- Source-adapter templates.
- Data-quality reports.
- Reproducible import jobs.

Exports must respect source licences, privacy restrictions, and redistribution permissions.

---

4.10 Community Observations

Future versions may allow community members to submit local observations.

Potential features

- Structured civic reports.
- Approximate map locations.
- Optional supporting photographs.
- Duplicate-report detection.
- Moderation and review.
- Status updates.
- Correction requests.
- Community feedback.
- Appeal mechanisms.

Community submissions must be clearly labelled as user-submitted information.

Community votes or the number of submissions must not automatically be treated as proof that a claim is true.

Submissions should remain private until reviewed where appropriate, and personal information must not be published by default.

---

5. AI Intelligence Layer

AI should make information easier to understand without becoming an opaque authority.

5.1 AI responsibilities

The AI layer can perform:

- Structured source extraction.
- Category classification.
- Neutral summarisation.
- Claim extraction.
- Evidence-grounded question answering.
- Comparison explanations.
- Possible duplicate detection.
- Contradiction candidate identification.
- Optional translation.
- Data-quality suggestions.

5.2 What AI must not control

AI must not independently determine:

- Whether a real-world allegation is true.
- Exact coordinates unsupported by evidence.
- Precise distances or travel times without deterministic tools.
- Environmental measurements.
- Official source status without validation.
- Whether two sources are genuinely independent.
- An absolute safety rating for a locality.

5.3 Open-weight model strategy

The initial implementation should support locally hosted models through a provider interface.

Potential components include:

- Ollama for local model serving.
- An openly licensed instruction model for structured extraction.
- An openly licensed embedding model for semantic retrieval.
- PostgreSQL and optional pgvector for retrieval.
- Deterministic Python functions for geospatial calculations and statistics.

Mistral 7B Instruct v0.3 is one candidate to evaluate, subject to checking the exact model card, licence, hardware requirements, and compatibility with the event's rules.

Model names and licences must be verified before implementation. Do not assume that every downloadable model qualifies as open-source.

5.4 AI provider abstraction

Define a provider interface so that local inference and optional remote providers can be substituted without changing business logic.

The local model path must be a real, tested feature.

A remote proprietary API must not be the only functioning implementation.

5.5 Structured output

AI outputs must validate against strict schemas.

A source extraction should include:

- Category.
- Neutral title.
- Summary.
- Event date.
- Publication date.
- Location text.
- Geospatial information when supported.
- Supporting claims.
- Relevant excerpts.
- Limitations.
- Review requirement.
- Model and schema versions.

Invalid model output should be rejected or sent for retry/review rather than stored as trusted evidence.

5.6 Grounded answer generation

The assistant must use retrieval-augmented generation or an equivalent grounded retrieval workflow.

The process should be:

1. Parse the question.
2. Retrieve relevant evidence.
3. Apply deterministic geographic or date filters.
4. Construct a bounded evidence context.
5. Generate an answer using the retrieved records.
6. Validate cited evidence identifiers.
7. Return the answer with limitations and source links.

When evidence is insufficient, return an explicit insufficient-evidence response.

The interface should show concise reasoning, assumptions, and citations rather than hidden model reasoning.

5.7 AI evaluation

Maintain a versioned evaluation dataset containing examples of:

- Ambiguous locations.
- Missing dates.
- Conflicting sources.
- Duplicate reports.
- Outdated information.
- Unsupported questions.
- Prompt injection in source text.
- Sensational or accusatory language.
- Multilingual text where supported.

Measure schema validity, citation validity, unsupported-claim rate, and abstention behaviour.

Do not claim an accuracy percentage without a documented evaluation method and results.

---

6. TrustLayer: Blockchain-Verified Evidence

TrustLayer is the Web3 component of LocalityLens.

Its purpose is to make evidence integrity independently verifiable.

Blockchain can verify that an evidence snapshot matches a previously anchored cryptographic commitment. It cannot prove that the original claim is true.

6.1 The problem TrustLayer addresses

Suppose LocalityLens retrieves a public report and archives a permitted snapshot.

Later, someone questions whether that evidence was changed.

TrustLayer allows the system to:

1. Canonicalise the evidence manifest.
2. Calculate a cryptographic digest.
3. Include the digest in a Merkle tree.
4. Anchor the Merkle root to a public blockchain.
5. Generate a verification receipt.
6. Recalculate and verify the evidence later.

If the canonical evidence manifest changes, its digest should no longer match the original commitment.

6.2 Evidence verification workflow

Step 1: Collect evidence

Retrieve a permitted public source.

Record:

- Source URL.
- Source identity or publisher.
- Retrieval timestamp.
- Publication date, if known.
- Event date, if known.
- Dataset licence.
- Source metadata.

Step 2: Validate provenance

Where feasible, verify that the record was retrieved from an expected official domain or that a publisher's digital signature is valid.

An official-looking URL alone does not guarantee that a claim is correct.

Step 3: Extract structured evidence

Use the AI extraction pipeline to create a structured record.

Preserve the original source metadata and relevant permitted source material.

Step 4: Create a canonical manifest

Construct a deterministic representation of the evidence record.

The canonicalisation specification must define:

- Included fields.
- Excluded fields.
- Field ordering.
- Unicode handling.
- Timestamp format.
- Schema version.
- Hash encoding.

The same record must produce the same canonical bytes every time.

Step 5: Calculate the digest

Calculate a SHA-256 digest of the canonical manifest.

Step 6: Build a Merkle tree

Combine multiple evidence digests into a Merkle tree.

This allows many evidence records to be committed through one on-chain root.

Each record can be verified using its Merkle inclusion proof.

Step 7: Anchor the root

Submit the root and minimal batch metadata to a registry contract on a supported public testnet.

Step 8: Create a receipt

The receipt should include:

- Evidence identifier.
- Evidence digest.
- Canonicalisation version.
- Merkle root.
- Merkle proof.
- Batch identifier.
- Chain identifier.
- Registry contract address.
- Transaction hash.
- Block number.
- Verification status.

Step 9: Verify later

The verifier:

1. Loads the canonical manifest.
2. Recalculates its digest.
3. Reconstructs the Merkle inclusion proof.
4. Recomputes the root.
5. Reads the anchored root from the configured chain.
6. Compares the results.
7. Returns a clear verification status.

6.3 Verification interface

The Evidence Explorer should display distinct statuses.

Examples:

- Digest matches: the current canonical manifest matches its recorded digest.
- Anchor verified: the digest is included in a Merkle root recorded on the configured chain.
- Source origin checked: the source origin or signature passed the configured checks.
- Official source: the publisher is classified as an official source.
- Corroborated: genuinely independent evidence supports the claim under documented rules.
- Conflicting evidence: relevant records disagree.
- Unverified: one or more required checks are missing or have failed.

Do not replace these statuses with one universal green "TRUE" badge.

6.4 Blockchain data policy

Store only minimal integrity metadata on-chain:

- Merkle root.
- Batch identifier.
- Leaf count.
- Schema or canonicalisation version.
- Transaction and contract information.

Keep full evidence records and permitted source archives off-chain.

Never place personal data, private preferences, raw sensitive complaints, or identifying information on-chain.

6.5 Smart contract

Implement a minimal Solidity evidence registry.

Its responsibilities should include:

- Recording a batch identifier.
- Recording the Merkle root.
- Recording the leaf count and version.
- Preventing silent replacement of an existing batch commitment.
- Emitting events for new anchors.
- Providing read methods for verification.

The contract should be small and auditable.

Use Foundry for contract tests.

Use a configurable public testnet for the hackathon demonstration. Confirm the event's actual chain requirements before selecting a deployment network.

6.6 Graceful degradation

The application must work without blockchain configuration.

When the chain is unavailable:

- Browsing must continue.
- Evidence pages must remain accessible.
- Existing receipts may still be inspected locally.
- On-chain verification should report that it is unavailable.
- Mock verification must be visibly labelled as mock.

---

7. LocalityLens Assistant

The assistant combines evidence retrieval, deterministic analysis, and natural-language explanations.

Core workflow

User question
      |
      v
Question interpretation
      |
      v
Evidence and locality retrieval
      |
      v
Geospatial/database tools
      |
      v
Relevant structured context
      |
      v
Open-weight language model
      |
      v
Citation and schema validation
      |
      v
Answer + evidence + limitations

Example

User:

"Compare these two localities for someone who uses public transport and wants nearby parks."

The assistant should:

1. Retrieve the selected locality records.
2. Query mapped public transport stops.
3. Query mapped parks using spatial database functions.
4. Identify missing or stale data.
5. Present deterministic results.
6. Explain the differences using the language model.
7. Link to the records used.

The language model must not independently calculate the number of parks or stops from prose.

Suggested assistant tools

- "search_evidence"
- "get_evidence_record"
- "get_locality_summary"
- "count_features_within_radius"
- "compare_localities"
- "get_dataset_freshness"
- "verify_evidence_receipt"

Each tool must validate its inputs and return structured data.

---

8. Neighbourhood Comparison Engine

The comparison engine should separate calculations from explanations.

Calculation process

1. Retrieve available indicators.
2. Validate data coverage.
3. Apply explicit user preferences.
4. Normalise comparable measurements using documented rules.
5. Calculate scores only for supported dimensions.
6. Show missing values and assumptions.
7. Ask AI to explain the results using the computed output.

Requirements

- User-defined weights.
- Explainable scoring.
- No hidden weighting.
- Missing-data warnings.
- Source-linked inputs.
- Reproducible results.
- Optional downloadable reports.

Do not compare incompatible measurements or imply that an incomplete dataset represents the entire neighbourhood.

---

9. Interactive Geospatial Intelligence

Use a proper geospatial database rather than storing every location as unvalidated latitude and longitude.

Capabilities

- Point-in-polygon queries.
- Distance-based searches.
- Spatial indexing.
- Bounding-box filtering.
- Locality boundary queries.
- Nearby amenity searches.
- Aggregation by geographic area.
- Map-based filtering.
- Geographic precision metadata.

Use PostGIS for spatial calculations where practical.

Store the source's original location text separately from the geocoded geometry.

A locality-level mention must not be represented as an exact incident coordinate.

Future routing functionality

A future version may support:

- Walking routes.
- Cycling routes.
- Public transport routes.
- Travel-time estimates.
- Isochrones.
- Accessibility-aware route information.

These features require an appropriate routing provider or dataset. Estimated travel times must identify the source and calculation method.

---

10. Community and Civic Intelligence

Future releases can make LocalityLens a collaborative civic-information platform.

Potential features

- Community-submitted observations.
- Moderation workflows.
- Evidence correction requests.
- Duplicate submissions detection.
- Reviewer notes.
- Public status history.
- Appeal mechanisms.
- Dataset contribution tools.
- Privacy-preserving aggregate exports.

Verification principles

Community submissions should be labelled as user-submitted.

The system should distinguish:

- Submitted.
- Awaiting review.
- Reviewed.
- Corroborated.
- Disputed.
- Superseded.
- Removed under a documented policy.

A submitted report is not automatically verified because several people repeat it.

Moderation should minimise personal information and avoid publishing unverified allegations against identifiable private individuals.

---

11. Open-Source and Open-Model Philosophy

LocalityLens should be designed as an open project rather than a thin interface that depends entirely on a proprietary API.

Open-source requirements

- Public source repository.
- OSI-approved software licence.
- Reproducible local setup.
- Documented API.
- Testable data pipeline.
- Transparent model selection.
- Dataset attribution.
- Public issue tracker.
- Contribution guidelines.
- Security disclosure process.
- Clear feature status.
- Reproducible demo.

Open-weight model requirements

The repository should document:

- Exact model name.
- Model revision.
- Model card.
- Licence.
- Inference runtime.
- Quantisation, if applicable.
- Hardware requirements.
- Known limitations.
- Evaluation results.

Do not assume that a model is open-source merely because its weights can be downloaded.

The selected model's licence must satisfy the actual hackathon rules.

Optional cloud inference

A remote model provider may be added behind an explicit configuration option.

However:

- Local inference must remain supported.
- Cloud use must be documented.
- Secrets must remain server-side.
- Users must not be forced to supply a paid API key for the core demo.
- Mock responses must never be presented as genuine model output.

Open data

The software licence does not override the licence of imported datasets.

Each dataset must have its own source and licence metadata.

---

12. System Architecture

High-level architecture

flowchart TD
    A["Public and permitted data sources"]
    B["Source adapters"]
    C["Licence and source validation"]
    D["Ingestion worker"]
    E["AI extraction and schema validation"]
    F["Geocoding and spatial validation"]
    G[("PostgreSQL + PostGIS")]
    H[("Permitted evidence archive")]
    I["API and retrieval layer"]
    J["LocalityLens web application"]
    K["SHA-256 and Merkle builder"]
    L["Evidence registry smart contract"]
    M["Evidence verification service"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    C --> H
    E --> H
    G --> I
    H --> K
    G --> K
    K --> L
    L --> M
    G --> M
    I --> J
    M --> I

Architectural principles

- Begin with a modular monolith and a background ingestion worker.
- Keep source retrieval separate from AI extraction.
- Validate every extracted record.
- Use a relational database for operational queries.
- Use PostGIS for spatial calculations.
- Use optional vector retrieval where it provides measurable value.
- Keep large permitted source archives off-chain.
- Anchor evidence digests in batches.
- Keep the web application functional when external services are unavailable.
- Avoid unnecessary microservices and infrastructure during the hackathon.

---

13. Technology Stack

Component| Technology| Purpose
Frontend| Next.js| Web application
Language| TypeScript| Frontend type safety
Styling| Tailwind CSS| Responsive interface
Mapping| MapLibre GL JS| Interactive maps
Backend| Python + FastAPI| REST API and application logic
Database| PostgreSQL| Structured records
Geospatial| PostGIS| Spatial queries and geometry
Semantic retrieval| pgvector, optional| Embedding-based retrieval
AI inference| Ollama-compatible local provider| Local open-weight model serving
Embeddings| Openly licensed embedding model| Semantic retrieval
Evidence hashing| SHA-256| Cryptographic fingerprints
Merkle trees| Deterministic implementation| Batch integrity proofs
Smart contracts| Solidity| Evidence registry
Contract testing| Foundry| Contract tests and deployment scripts
Blockchain client| viem or ethers| Chain interaction
Local environment| Docker Compose| Reproducible development
Backend tests| pytest| API and application testing
Frontend tests| Appropriate TypeScript test tooling| UI and interaction testing
CI| GitHub Actions| Automated quality checks

Choose compatible, maintained dependency versions and commit the relevant lockfiles.

Do not introduce additional infrastructure unless the project demonstrates a need for it.

---

14. AI Pipeline

The ingestion pipeline should be repeatable and observable.

Pipeline

1. Select an enabled, permitted source.
2. Retrieve the source using a safe adapter.
3. Record retrieval metadata.
4. Validate content type and size.
5. Parse the source.
6. Check for duplicate candidates.
7. Extract structured fields using a local model.
8. Validate the model output against a schema.
9. Resolve location references where justified.
10. Record geographic precision.
11. Save the evidence and provenance.
12. Create a permitted archive snapshot if allowed.
13. Generate a digest and queue the record for batch anchoring.
14. Update dataset freshness and job status.

Failure handling

If a stage fails:

- Record the error.
- Preserve valid source metadata.
- Avoid inventing missing fields.
- Retry only where appropriate.
- Do not silently mark failed records as verified.
- Keep the ingestion job's final status visible.

Prompt-injection protection

Source content is untrusted data.

Instructions contained in a news article, web page, uploaded document, or dataset must never override the system's extraction or security rules.

Do not execute arbitrary code or SQL produced by a language model.

---

15. Blockchain Architecture

Components

- Canonical manifest builder.
- SHA-256 digest generator.
- Merkle tree builder.
- Merkle inclusion proof generator.
- Solidity evidence registry.
- Testnet deployment configuration.
- Transaction receipt processor.
- Verification API.
- Public verification interface.

Merkle batch workflow

Evidence A ----> SHA-256 ----\
Evidence B ----> SHA-256 -----+--> Merkle Tree --> Merkle Root --> Testnet
Evidence C ----> SHA-256 -----+
Evidence D ----> SHA-256 ----/

Evidence A + Inclusion Proof + Anchored Root --> Verification

Integrity requirements

- Define canonicalisation explicitly.
- Publish deterministic test vectors.
- Use domain separation between leaf and internal-node hashes.
- Document leaf ordering.
- Define odd-node handling.
- Prevent silent overwriting of an existing batch commitment.
- Test altered manifests and invalid proofs.
- Handle chain RPC errors.
- Verify the expected chain and contract address.
- Keep private keys out of the frontend.
- Avoid mainnet deployment for the initial hackathon demonstration.

The registry should store a Merkle root and minimal metadata, not the entire dataset.

---

16. Data Sources and Ingestion

The first version should prioritise a small number of reliable, legally reusable datasets.

Potential source categories include:

- OpenStreetMap data.
- Government open-data portals.
- Municipal public notices.
- Public roadwork and infrastructure notices.
- Official environmental monitoring datasets.
- Public transport datasets.
- Public weather and rainfall datasets.
- News sources where reuse and storage are permitted.
- Moderated community submissions.

Availability varies by city. The implementation must not pretend that a source exists or contains a particular dataset without checking it.

Dataset manifest

Every dataset must have a manifest describing:

- Dataset identifier.
- Dataset name.
- Publisher.
- Original URL.
- Licence.
- Required attribution.
- Retrieval timestamp.
- Geographic coverage.
- Temporal coverage.
- Imported fields.
- Transformations.
- Update cadence.
- Redistribution permissions.
- Known limitations.

Data-quality rules

- Separate event date, publication date, retrieval date, and processing date.
- Preserve original location text.
- Record geocoding precision.
- Preserve measurement units.
- Do not replace missing values with zero.
- Do not interpret complaint counts as incident rates without a justified denominator.
- Do not treat repeated syndicated articles as independent corroboration.
- Document incomplete geographic and temporal coverage.

---

17. Database Design

Use migrations, constraints, foreign keys, and appropriate indexes.

"sources"

Stores source registry information.

Suggested fields:

- "id"
- "name"
- "source_url"
- "source_type"
- "publisher"
- "license"
- "attribution"
- "authority_classification"
- "update_cadence"
- "last_successful_retrieval"
- "status"

"evidence_records"

Stores structured evidence.

Suggested fields:

- "id"
- "source_id"
- "source_item_id"
- "title"
- "summary"
- "category"
- "original_location_text"
- "geometry"
- "geocoding_precision"
- "event_date"
- "published_at"
- "retrieved_at"
- "processed_at"
- "review_status"
- "archive_reference"
- "canonical_digest"
- "duplicate_cluster_id"
- "created_at"
- "updated_at"

"evidence_claims"

Stores claims extracted from a source.

Suggested fields:

- "id"
- "evidence_id"
- "claim_text"
- "supporting_excerpt"
- "extraction_model"
- "model_revision"
- "schema_version"
- "review_status"

"evidence_relations"

Stores evidence relationships.

Suggested fields:

- "id"
- "source_evidence_id"
- "target_evidence_id"
- "relation_type"
- "created_at"
- "review_status"

"localities"

Stores locality information.

Suggested fields:

- "id"
- "name"
- "boundary_geometry"
- "boundary_source"
- "boundary_license"
- "alternative_names"
- "locality_type"

"dataset_manifests"

Stores dataset provenance, licence, coverage, and transformation metadata.

"ingestion_jobs"

Stores ingestion status, idempotency keys, processing counts, timestamps, and errors.

"anchor_batches"

Stores Merkle roots, chain identifiers, contract addresses, leaf counts, transaction hashes, block numbers, and verification status.

"anchor_leaves"

Stores evidence identifiers, leaf digests, batch references, and proof metadata.

"review_events"

Stores corrections, review actions, reasons, and timestamps.

Optional "user_preferences"

Stores user-controlled comparison preferences only when needed and with appropriate retention and deletion controls.

---

18. API Design

All application endpoints should use a versioned prefix such as "/api/v1".

Method| Endpoint| Purpose
GET| "/api/v1/health"| Health status
GET| "/api/v1/sources"| Source registry and freshness
GET| "/api/v1/evidence"| Search and filter evidence
GET| "/api/v1/evidence/{id}"| Evidence detail
POST| "/api/v1/evidence/{id}/verify"| Verify evidence integrity
GET| "/api/v1/localities"| Search localities
GET| "/api/v1/localities/{id}/summary"| Locality summary
POST| "/api/v1/compare"| Compare localities
POST| "/api/v1/assistant/ask"| Grounded question answering
POST| "/api/v1/ingestion/preview"| Validate an import
POST| "/api/v1/ingestion/jobs"| Start an ingestion job
GET| "/api/v1/ingestion/jobs/{id}"| Check ingestion status
GET| "/api/v1/anchors"| List evidence anchor batches
GET| "/api/v1/anchors/{id}/receipt"| Retrieve a verification receipt

Administrative ingestion endpoints must be protected appropriately.

API requirements

- Input validation.
- Pagination.
- Stable error formats.
- Request-size limits.
- Rate limits for expensive operations.
- Structured logs.
- Request identifiers.
- Documented CORS policy.
- OpenAPI documentation.
- No secret leakage in errors.
- SSRF protections for source fetching.
- Safe handling of redirects and untrusted URLs.

---

19. Security and Privacy

Privacy requirements

- Never place personal data on-chain.
- Never place raw sensitive complaint text on-chain.
- Do not publish a contributor's identity by default.
- Avoid exposing precise private addresses.
- Strip image metadata when appropriate.
- Make user preference storage optional.
- Provide deletion and retention policies.
- Do not require wallet connection for ordinary use.

Source ingestion security

- Validate URLs.
- Block loopback, private, link-local, and cloud metadata addresses.
- Validate redirects.
- Enforce download limits.
- Enforce request timeouts.
- Validate content types.
- Parse files using safe libraries.
- Escape source content before rendering.
- Treat retrieved documents as untrusted input.
- Never execute downloaded code.

Application security

- Store secrets in environment variables or a suitable secret manager.
- Never expose private keys in client-side bundles.
- Use parameterised database queries.
- Apply least-privilege credentials.
- Add dependency and secret scanning.
- Validate API request bodies.
- Protect privileged routes.
- Use a dedicated test wallet for the testnet demonstration.
- Keep blockchain signing credentials server-side.

---

20. Responsible AI

LocalityLens must be careful about how it describes places and people.

No absolute safety ratings

Do not generate claims such as:

"This neighbourhood is dangerous."

A few public reports do not establish the overall safety of a location.

The system may display specific, sourced observations with dates, locations, limitations, and uncertainty.

Avoid misleading statistics

A larger number of public complaints does not necessarily mean that a neighbourhood has more incidents.

Reporting frequency can depend on:

- Population.
- Reporting access.
- Public awareness.
- Media attention.
- Data availability.
- Reporting behaviour.

Evidence and uncertainty

Every AI-generated locality report should distinguish:

- Direct source statements.
- Deterministic calculations.
- AI-generated interpretations.
- Missing information.
- Conflicting evidence.
- Unverified submissions.

Fairness

Do not rank or recommend neighbourhoods using protected characteristics such as caste, religion, race, or disability.

Do not infer sensitive personal characteristics from user preferences.

Transparency

Show users:

- What evidence was used.
- How old it is.
- What is missing.
- Which calculations were performed.
- Which model generated a summary.
- What the system cannot determine.

---

21. Project Structure

The implementation should follow a modular structure similar to:

localitylens/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── AGENTS.md
├── .env.example
├── docker-compose.yml
├── Makefile
├── apps/
│   └── web/
│       ├── app/
│       ├── components/
│       │   ├── map/
│       │   ├── evidence/
│       │   ├── comparison/
│       │   └── assistant/
│       ├── lib/
│       └── tests/
├── services/
│   ├── api/
│   │   ├── localitylens/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── db/
│   │   │   ├── evidence/
│   │   │   ├── geospatial/
│   │   │   ├── ingestion/
│   │   │   ├── ai/
│   │   │   ├── comparison/
│   │   │   └── integrity/
│   │   ├── migrations/
│   │   └── tests/
│   └── worker/
├── contracts/
│   ├── src/
│   ├── test/
│   ├── script/
│   └── foundry.toml
├── data/
│   ├── README.md
│   ├── manifests/
│   └── fixtures/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_SOURCES.md
│   ├── DATA_MODEL.md
│   ├── MODEL_CARD.md
│   ├── TRUST_MODEL.md
│   ├── API.md
│   └── DEMO_SCRIPT.md
├── scripts/
│   ├── seed_demo_data.py
│   ├── validate_dataset.py
│   ├── build_merkle_batch.py
│   └── verify_receipt.py
└── .github/
    └── workflows/

This is a target structure, not a claim that these files already exist.

---

22. Local Development Setup

The repository should provide a reproducible setup that a new contributor can run.

Prerequisites

- Git.
- Docker Engine.
- Docker Compose v2.
- Node.js LTS.
- Python 3.11 or a compatible supported version.
- Optional Ollama installation for local model inference.
- Foundry for contract development and testing.

Clone the repository

git clone <YOUR_PUBLIC_REPOSITORY_URL>
cd localitylens

Configure environment variables

cp .env.example .env

Review the configuration before starting the services.

Start the application

docker compose up --build

The repository must document the exact local web and API addresses after the services are implemented.

Load demo data

make seed

Run tests

make test

Run contract tests

make test-contracts

These commands should be implemented and tested by the coding agent. Do not document a command as working until it has been verified.

Local AI setup

1. Install the selected local inference runtime.
2. Download the exact model specified by the project configuration.
3. Verify that the local inference endpoint is available.
4. Configure the AI provider.
5. Run the extraction test fixture.
6. Verify that grounded Q&A returns valid evidence citations.

The project should support a clearly labelled mock mode for UI development when local inference is unavailable. Mock mode must not be presented as genuine AI inference.

---

23. Environment Variables

The repository should include a safe ".env.example".

Example configuration:

APP_ENV=development
APP_BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
LOG_LEVEL=INFO

DATABASE_URL=postgresql+psycopg://localitylens:localitylens_dev@db:5432/localitylens

AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=mistral
AI_REQUEST_TIMEOUT_SECONDS=90
AI_MOCK_MODE=false

INGESTION_ENABLED=false
GEOCODING_PROVIDER=none
MAX_SOURCE_DOWNLOAD_BYTES=5000000
SOURCE_FETCH_TIMEOUT_SECONDS=15

EVIDENCE_STORAGE_BACKEND=local
EVIDENCE_STORAGE_PATH=./var/evidence

CHAIN_ENABLED=false
CHAIN_ID=
CHAIN_RPC_URL=
EVIDENCE_REGISTRY_ADDRESS=
ANCHOR_PRIVATE_KEY=
ANCHOR_BATCH_SIZE=100

REMOTE_AI_ENABLED=false
REMOTE_AI_API_KEY=
REMOTE_AI_MODEL=

The implementation must document any additional required variables.

Never commit a populated ".env" file.

The application must validate configuration at startup and explain missing required values clearly.

The chain private key must never be exposed to the browser.

The local model URL may need different settings depending on the operating system and whether Docker is used.

---

24. Testing and Evaluation

Testing must cover the complete evidence lifecycle.

Unit tests

Test:

- Evidence schema validation.
- Date parsing.
- Geospatial validation.
- Canonicalisation.
- SHA-256 digest generation.
- Merkle root generation.
- Merkle inclusion proof generation.
- Invalid proof rejection.
- Comparison calculations.
- Missing-data handling.
- Citation validation.

Integration tests

Test:

- Clean database migrations.
- Idempotent dataset imports.
- API filtering.
- Evidence retrieval.
- Locality summaries.
- Grounded assistant responses.
- Unsupported-question abstention.
- Chain RPC failure handling.
- Evidence receipt verification.
- Modified-manifest rejection.
- URL ingestion protections.

AI tests

Test that:

- Required fields are extracted correctly on the fixture set.
- The output conforms to the expected schema.
- Citations reference real evidence records.
- Unsupported claims are rejected or flagged.
- Contradictions are surfaced.
- Prompt injection in source text does not override system instructions.
- Missing information remains missing rather than being fabricated.

Contract tests

Test:

- Valid anchor registration.
- Duplicate batch behaviour.
- Prevention of silent root replacement.
- Correct event emission.
- Valid and invalid Merkle proofs in the verification flow.

Accessibility tests

Test:

- Keyboard navigation.
- Visible focus states.
- Accessible labels.
- Responsive layout.
- A list alternative for map content.
- Readable uncertainty and status indicators.

---

25. Development Roadmap

Phase 1: Foundation

- [x] Create the repository.
- [x] Configure the development environment.
- [x] Add PostgreSQL and PostGIS.
- [x] Implement database migrations.
- [x] Create dataset manifests.
- [x] Add clearly labelled demo records.
- [x] Add CI and basic tests.

Phase 2: Evidence Explorer

- [x] Implement the source registry.
- [x] Implement evidence records.
- [x] Build evidence search APIs.
- [x] Build evidence detail pages.
- [x] Display source links and dates.
- [x] Implement provenance metadata.
- [x] Add correction history.

Phase 3: Interactive Map

- [x] Integrate MapLibre.
- [x] Display evidence markers.
- [x] Add category filters.
- [x] Add temporal filters.
- [x] Implement marker clustering.
- [x] Add accessible list view.
- [x] Display geographic uncertainty.

Phase 4: Open-Weight AI

- [x] Implement the AI provider interface.
- [x] Integrate a suitable local model.
- [x] Implement structured extraction.
- [x] Validate AI output schemas.
- [x] Implement grounded question answering.
- [x] Add citation validation.
- [x] Add insufficient-evidence behaviour.
- [x] Create evaluation fixtures.

Phase 5: Locality Comparison

- [x] Implement locality summaries.
- [x] Implement transparent comparison weights.
- [x] Add deterministic spatial queries.
- [x] Add missing-data warnings.
- [x] Generate evidence-linked explanations.
- [x] Implement shareable comparisons.

Phase 6: TrustLayer

- [x] Define canonical manifest format.
- [x] Implement SHA-256 hashing.
- [x] Implement Merkle trees.
- [x] Implement inclusion proofs.
- [x] Build the Solidity registry.
- [x] Add Foundry tests.
- [x] Deploy to a supported testnet.
- [x] Implement verification receipts.
- [x] Add an integrity verification interface.
- [x] Test modified-record rejection.

Phase 7: Hardening

- [x] Add rate limits.
- [x] Add source-ingestion security controls.
- [x] Improve error handling.
- [x] Improve accessibility.
- [x] Add end-to-end tests.
- [x] Document the exact model and licence.
- [x] Document data sources and limitations.
- [x] Rehearse the complete demo.

Future phases

- [ ] Additional city adapters.
- [ ] Public transport routing.
- [ ] Environmental trend analysis.
- [ ] Community observations.
- [ ] Moderation workflows.
- [ ] Data export tools.
- [ ] Multilingual interface.
- [ ] Dataset freshness alerts.
- [ ] Public verification tooling.
- [ ] Optional public API and SDK.

---

26. Hackathon MVP

The goal is to demonstrate one complete workflow, not every future feature.

Must-have features

1. Interactive map.
2. One city with a small curated dataset.
3. Structured evidence records.
4. Open-weight AI extraction.
5. Evidence Explorer.
6. Grounded AI question answering.
7. Locality comparison.
8. SHA-256 evidence digest.
9. Merkle tree and inclusion proof.
10. Public testnet anchor.
11. Evidence verification interface.
12. Automated tests.
13. Reproducible setup.
14. Public repository and open-source licence.

Recommended initial dataset

Prepare approximately 20–50 records, depending on the availability of suitable public data and the time available.

Prioritise:

- Valid source metadata.
- Clear source attribution.
- Geographic relevance.
- A few useful categories.
- A mix of known and missing dates.
- At least a few records suitable for a verification demonstration.

Use synthetic records when necessary, but label them clearly as synthetic.

Do not invent real-world observations to make the map look more impressive.

What not to build first

Avoid spending the initial hackathon period on:

- Every city.
- Dozens of live data feeds.
- A custom foundation model.
- A token or NFT economy.
- Mandatory wallet login.
- Mainnet deployment.
- An elaborate autonomous-agent framework.
- Unvalidated predictive safety scores.
- A large microservices infrastructure.

First complete the core loop.

---

27. Demo Scenario

The demo should tell one clear story.

Scenario: Moving to Chandigarh

Step 1: Explore

A user opens the Chandigarh demo map and filters the available records by category and date.

Step 2: Inspect evidence

The user clicks a record and sees its source, dates, geographic precision, summary, and limitations.

Step 3: Ask the assistant

The user asks:

"What do the available sources report about this area, and what remains uncertain?"

The assistant retrieves evidence and returns source-linked observations.

Step 4: Compare localities

The user selects two demo localities and prioritises public transport, green spaces, and commute requirements.

The comparison displays the available indicators and missing-data warnings.

Step 5: Verify integrity

The user opens a verification receipt.

The application recalculates the evidence digest, verifies the Merkle proof, and checks the anchored root.

Step 6: Demonstrate tampering detection

The demo modifies a copy of the canonical evidence manifest.

Verification fails because the digest no longer matches the anchored commitment.

Step 7: Explain the limitation

The demo explicitly states:

"The blockchain confirms that this evidence snapshot matches the previously anchored commitment. It does not prove that the underlying real-world claim is true."

This final distinction is essential to the project's credibility.

---

28. Open-Source Contribution

LocalityLens should welcome contributions from developers, data researchers, designers, students, civic technologists, and community members.

Contribution areas

- Frontend development.
- Backend APIs.
- Geospatial analysis.
- AI evaluation.
- Open-model integration.
- Blockchain verification.
- Dataset adapters.
- Documentation.
- Accessibility.
- Internationalisation.
- Security.
- Testing.

Contribution workflow

1. Open or select an issue.
2. Agree on the scope of significant changes.
3. Create a focused branch.
4. Implement the change.
5. Add or update tests.
6. Run the project quality checks.
7. Update documentation.
8. Open a pull request with testing details.

Requirements for new data sources

Every new source adapter must document:

- Source URL.
- Publisher.
- Licence.
- Attribution.
- Update cadence.
- Geographic coverage.
- Data transformations.
- Known limitations.
- Permitted storage and redistribution.

Open-source standards

- Use an OSI-approved licence.
- Maintain a public repository.
- Include a code of conduct.
- Document security reporting.
- Avoid committing secrets.
- Preserve source attribution.
- Make setup reproducible.
- Keep planned features separate from implemented features.

If the project is submitted to an MLH event, check that event's current rules directly. Confirm the required licence, eligible development window, permitted AI tools, and exact model licensing requirements.

---

29. Future Possibilities

Once the core evidence loop is stable, LocalityLens could expand in several directions.

29.1 Urban Change Intelligence

Analyse changes in permitted public datasets over time and identify new or superseded reports.

29.2 Personalised Daily-Life Planning

Help users explore available routes, amenities, transport options, and daily requirements.

29.3 Civic Data APIs

Allow researchers and civic applications to query documented, permitted neighbourhood datasets.

29.4 Public Evidence Verification

Provide a simple verification page and portable receipts that independent users can inspect.

29.5 Community Data Stewardship

Enable communities to contribute observations, request corrections, and maintain transparent review histories.

29.6 Multilingual Neighbourhood Research

Support local languages while preserving original source excerpts and attribution.

29.7 Reproducible Urban Research

Allow researchers to export permitted datasets and document the exact inputs and methods behind a report.

29.8 Open-Source City Adapters

Let contributors add city-specific datasets without changing the core application.

29.9 Evidence-Based Infrastructure Monitoring

Surface changes in public infrastructure notices and permitted monitoring datasets.

29.10 Portable Trust Infrastructure

Allow other open-source applications to reuse the evidence receipt format and verification library, provided the design is generalised and documented carefully.

These are future directions, not promised capabilities of the first release.

---

30. Important Limitations

LocalityLens must communicate its limitations clearly.

- Public data may be incomplete or outdated.
- Some sources may have restricted reuse rights.
- Geographic references may be ambiguous.
- AI extraction can make mistakes.
- Source authority does not guarantee factual accuracy.
- Multiple reports may derive from the same original source.
- Complaint volume does not necessarily reflect incident prevalence.
- Map coverage may vary significantly between neighbourhoods.
- Travel-time estimates require appropriate routing data.
- A cryptographic hash does not prove a real-world event occurred.
- Blockchain availability and transaction finality depend on the selected network.
- Model performance depends on the selected model, hardware, prompts, and evaluation data.

LocalityLens should favour transparent uncertainty over unsupported certainty.

---

31. License

LocalityLens is intended to use the MIT License for its application code.

The actual repository must include the complete "LICENSE" file before public release.

The code licence does not override the licences of third-party datasets, source material, map tiles, or AI models. Each dependency and dataset must retain its applicable licensing and attribution requirements.

---

Final Vision

LocalityLens is not simply a neighbourhood map with an AI chatbot.

It is an attempt to build an open, evidence-first urban intelligence platform where:

- AI makes public information understandable.
- Geospatial tools make that information useful.
- Open-source development makes the platform accessible.
- Transparent provenance lets people inspect the evidence.
- Blockchain makes archived evidence integrity independently verifiable.
- Responsible design prevents uncertainty from being disguised as fact.

The fundamental workflow is:

"Collect → Validate → Extract → Map → Investigate → Compare → Hash → Anchor → Verify"

Build this workflow end to end first. Expand only after the evidence pipeline, user experience, and verification mechanism are reliable.
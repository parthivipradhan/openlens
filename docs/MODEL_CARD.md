# Model Card — LocalityLens AI

## Overview

LocalityLens uses open-weight language models via **Ollama** for:
1. Structured evidence extraction (Phase 4 ingestion pipeline)
2. Grounded Q&A assistant (`POST /api/v1/assistant/ask`)

> **Default configuration: `AI_MOCK_MODE=true`**
> The system is fully operational without any AI model. Mock mode returns clearly labelled placeholder responses.

---

## Supported Models

| Model Name | Provider | Size | Recommended For |
|---|---|---|---|
| `mistral` | Mistral AI | 7B | Default — balanced quality/speed |
| `llama3` | Meta | 8B | Higher quality extraction |
| `phi3` | Microsoft | 3.8B | Low-resource environments |
| `gemma2` | Google | 9B | Multilingual support |

Configure via `OLLAMA_MODEL` environment variable.

## Hardware Requirements

| Model | Minimum RAM | GPU (recommended) |
|---|---|---|
| mistral (7B) | 8 GB | 8 GB VRAM |
| llama3 (8B) | 8 GB | 10 GB VRAM |
| phi3 (3.8B) | 6 GB | 6 GB VRAM |

CPU inference is supported but significantly slower (~30–90s per query).

---

## Intended Uses

- Summarising neighbourhood evidence records for a specific locality
- Answering questions about Chandigarh infrastructure, transport, environment
- Extracting structured claims from unstructured text articles

## Out-of-Scope Uses

- Generating information about individuals (privacy violation)
- Providing medical, legal, or financial advice
- Predicting future events
- Verifying the truth of evidence claims (this is a data-quality problem, not an AI problem)

---

## Risk Mitigations

| Risk | Mitigation |
|---|---|
| Hallucination / fabrication | RAG limits context to retrieved records; citation IDs validated against retrieval |
| Prompt injection | System prompt treats all retrieved content as untrusted; output schema validated |
| Insufficient evidence | Explicit abstention behaviour — returns `insufficient_evidence: true`, never guesses |
| Model output schema violation | JSON schema validated; invalid outputs rejected with HTTP 503 |
| Data freshness | AI sees `published_at` / `event_date` metadata; context window limited to 8 records |

---

## Evaluation

Evaluation fixtures are located in `data/fixtures/`.

Run evaluation:
```bash
# Not yet automated — see data/fixtures/ for test cases
python scripts/eval_assistant.py
```

---

## Licences

- **Mistral 7B**: Apache 2.0
- **Llama 3**: Meta Llama 3 Community License
- **Phi-3**: MIT
- **Gemma 2**: Gemma Terms of Use

Model weights are served locally via Ollama and are not redistributed.

---

## Contact

For concerns about model behaviour or data quality, file an issue at the project repository
or see `SECURITY.md` for responsible disclosure.

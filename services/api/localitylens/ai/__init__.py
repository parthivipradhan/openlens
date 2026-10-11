"""LocalityLens AI provider package."""
from localitylens.ai.provider import get_ai_provider, MockAIProvider, OllamaProvider, EvidenceContext
from localitylens.ai.rag import retrieve_evidence_for_query

__all__ = [
    "get_ai_provider",
    "MockAIProvider",
    "OllamaProvider",
    "EvidenceContext",
    "retrieve_evidence_for_query",
]

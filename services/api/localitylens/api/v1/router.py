"""API v1 router — mounts all sub-routers."""

from fastapi import APIRouter

from localitylens.api.v1 import (
    anchors,
    assistant,
    compare,
    evidence,
    health,
    ingestion,
    localities,
    manifests,
    sources,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sources.router, prefix="/sources", tags=["Sources"])
api_router.include_router(manifests.router, prefix="/manifests", tags=["Manifests"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["Evidence"])
api_router.include_router(localities.router, prefix="/localities", tags=["Localities"])
api_router.include_router(compare.router, prefix="/compare", tags=["Comparison"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])
api_router.include_router(anchors.router, prefix="/anchors", tags=["TrustLayer"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])

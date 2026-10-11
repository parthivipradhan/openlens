"""GET /api/v1/health — service health check."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

from localitylens.db.session import get_db
from localitylens.core.config import settings

router = APIRouter()
log = structlog.get_logger(__name__)


@router.get("/health", summary="Health status")
async def health(db: AsyncSession = Depends(get_db)):
    """Returns service health, DB status, and configuration flags."""
    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as exc:
        log.error("Health check DB failure", error=str(exc))

    return {
        "status": "ok" if db_ok else "degraded",
        "env": settings.APP_ENV,
        "db": "connected" if db_ok else "unavailable",
        "ai_provider": settings.AI_PROVIDER,
        "ai_mock_mode": settings.AI_MOCK_MODE,
        "chain_enabled": settings.CHAIN_ENABLED,
        "ingestion_enabled": settings.INGESTION_ENABLED,
    }

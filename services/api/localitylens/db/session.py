"""SQLAlchemy async session and database initialisation."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

import structlog

from localitylens.core.config import settings

log = structlog.get_logger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    """Verify DB connection is reachable at startup."""
    try:
        async with engine.connect() as conn:
            await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        log.info("Database connection verified")
    except Exception as exc:
        log.error("Database connection failed", error=str(exc))
        raise


async def get_db():
    """FastAPI dependency — yields an async session."""
    async with AsyncSessionLocal() as session:
        yield session

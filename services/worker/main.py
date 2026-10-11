"""
LocalityLens Background Worker (Phase 4 & Phase 7).

Monitors ingestion jobs, runs safe fetching, AI extraction, validation,
and commits verified evidence records to the database.
"""

from __future__ import annotations

import asyncio
import structlog

from localitylens.core.config import settings
from localitylens.core.logging import setup_logging
from localitylens.ingestion.pipeline import ingest_source_document

setup_logging()
log = structlog.get_logger(__name__)


async def process_pending_jobs():
    """Poll database for pending ingestion jobs and process them."""
    log.debug("Worker checking for pending ingestion jobs...")
    # In full deployment, pulls pending jobs from PostgreSQL ingestion_jobs table


async def main():
    log.info("LocalityLens worker initialized", ingestion_enabled=settings.INGESTION_ENABLED)

    if not settings.INGESTION_ENABLED:
        log.info("Ingestion is disabled (INGESTION_ENABLED=false). Worker in standby mode.")

    while True:
        try:
            if settings.INGESTION_ENABLED:
                await process_pending_jobs()
            await asyncio.sleep(30)
        except Exception as exc:
            log.error("Worker loop encountered an error", error=str(exc))
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())

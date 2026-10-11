"""
LocalityLens — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from localitylens.core.config import settings
from localitylens.core.logging import setup_logging
from localitylens.db.session import init_db
from localitylens.api.v1.router import api_router

setup_logging()
log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("LocalityLens API starting", env=settings.APP_ENV)
    await init_db()
    yield
    log.info("LocalityLens API shutting down")


app = FastAPI(
    title="LocalityLens API",
    description=(
        "Open-source neighbourhood intelligence platform. "
        "AI-powered evidence extraction, geospatial analysis, "
        "and blockchain-verified evidence integrity."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

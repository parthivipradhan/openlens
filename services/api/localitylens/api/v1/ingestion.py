"""Ingestion job endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class IngestionPreviewRequest(BaseModel):
    source_url: str


@router.post("/preview", summary="Preview a source import")
async def preview_ingestion(req: IngestionPreviewRequest):
    return {"status": "not_implemented", "message": "Ingestion pipeline is a Phase 4 feature."}


@router.post("/jobs", summary="Start an ingestion job")
async def start_ingestion_job(req: IngestionPreviewRequest):
    return {"status": "not_implemented", "message": "Ingestion pipeline is a Phase 4 feature."}


@router.get("/jobs/{job_id}", summary="Check ingestion job status")
async def get_ingestion_job(job_id: str):
    raise HTTPException(status_code=404, detail="Job not found. Ingestion is a Phase 4 feature.")

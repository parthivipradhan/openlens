"""Phase 1 — Basic API tests."""

import pytest
from httpx import AsyncClient, ASGITransport

from localitylens.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "env" in data


@pytest.mark.asyncio
async def test_evidence_list_empty():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/evidence")
    assert response.status_code == 200
    assert "evidence" in response.json()


@pytest.mark.asyncio
async def test_evidence_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/evidence/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sources_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sources")
    assert response.status_code == 200
    assert "sources" in response.json()


@pytest.mark.asyncio
async def test_localities_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/localities")
    assert response.status_code == 200
    assert "localities" in response.json()


@pytest.mark.asyncio
async def test_assistant_mock():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/assistant/ask", json={"question": "What is the waterlogging situation?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["mock"] is True

"""Phase 2 — Evidence Explorer API tests."""

import pytest
from httpx import AsyncClient, ASGITransport

from localitylens.main import app


@pytest.mark.asyncio
async def test_sources_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # List sources
        res = await ac.get("/api/v1/sources")
        assert res.status_code == 200
        data = res.json()
        assert "sources" in data
        assert isinstance(data["sources"], list)

        # Filter sources by type
        res_filter = await ac.get("/api/v1/sources?source_type=govt")
        assert res_filter.status_code == 200
        assert "sources" in res_filter.json()


@pytest.mark.asyncio
async def test_manifests_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/manifests")
        assert res.status_code == 200
        data = res.json()
        assert "manifests" in data
        assert isinstance(data["manifests"], list)


@pytest.mark.asyncio
async def test_evidence_list_and_search():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Basic list
        res = await ac.get("/api/v1/evidence?limit=10")
        assert res.status_code == 200
        data = res.json()
        assert "evidence" in data
        assert "total" in data
        assert "categories" in data
        assert data["limit"] == 10

        # Category filter
        res_cat = await ac.get("/api/v1/evidence?category=waterlogging")
        assert res_cat.status_code == 200

        # Search query
        res_search = await ac.get("/api/v1/evidence?q=Chandigarh")
        assert res_search.status_code == 200


@pytest.mark.asyncio
async def test_evidence_detail_and_provenance():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First get an evidence record if available
        list_res = await ac.get("/api/v1/evidence?limit=1")
        assert list_res.status_code == 200
        records = list_res.json()["evidence"]

        if records:
            ev_id = records[0]["id"]

            # Detail
            detail_res = await ac.get(f"/api/v1/evidence/{ev_id}")
            assert detail_res.status_code == 200
            detail = detail_res.json()
            assert detail["id"] == ev_id
            assert "claims" in detail
            assert "relations" in detail
            assert "review_history" in detail

            # Provenance
            prov_res = await ac.get(f"/api/v1/evidence/{ev_id}/provenance")
            assert prov_res.status_code == 200
            prov = prov_res.json()
            assert "timestamps" in prov
            assert "source" in prov
            assert "integrity" in prov

            # Verify
            ver_res = await ac.post(f"/api/v1/evidence/{ev_id}/verify")
            assert ver_res.status_code == 200
            assert "verification_status" in ver_res.json()

            # Review submission
            review_payload = {
                "action": "verified",
                "reason": "Automated Phase 2 integration test verification",
                "reviewer": "test_suite",
                "new_review_status": "verified",
            }
            rev_post = await ac.post(f"/api/v1/evidence/{ev_id}/review", json=review_payload)
            assert rev_post.status_code == 200
            assert rev_post.json()["current_status"] == "verified"

            # Review history
            hist_res = await ac.get(f"/api/v1/evidence/{ev_id}/history")
            assert hist_res.status_code == 200
            assert hist_res.json()["total"] >= 1

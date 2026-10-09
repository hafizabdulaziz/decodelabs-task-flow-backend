"""
Unit tests for standardized global exception handler and error schema verification.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.anyio
async def test_global_exception_handler_schema():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/non-existent-route")
        assert response.status_code == 404
        data = response.json()
        assert "error_code" in data
        assert "message" in data
        assert "timestamp" in data
        assert data["error_code"] == "NOT_FOUND"


@pytest.mark.anyio
async def test_validation_error_schema():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json={"password": "123"})
        assert response.status_code == 422
        data = response.json()
        assert "error_code" in data
        assert "message" in data
        assert "timestamp" in data
        assert data["error_code"] == "VALIDATION_ERROR"

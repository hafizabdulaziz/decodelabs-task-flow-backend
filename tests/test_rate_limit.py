"""
Integration tests for rate limiting middleware.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.anyio
async def test_rate_limiting_auth_routes():
    """
    Test that auth routes enforce strict rate limiting (5 req/min) and return 429 upon exhaustion,
    including correct X-RateLimit headers and standardized error response.
    """
    payload = {
        "email": "ratelimit@decodelabs.com",
        "password": "SecurePassword123!",
        "full_name": "Rate Limit Test",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for _ in range(5):
            response = await ac.post("/api/v1/auth/register", json=payload)
            assert "X-RateLimit-Limit" in response.headers
            assert "X-RateLimit-Remaining" in response.headers

        # 6th request should trigger 429 Too Many Requests
        response_6 = await ac.post("/api/v1/auth/register", json=payload)
        assert response_6.status_code == 429
        data = response_6.json()
        assert data["error_code"] == "RATE_LIMIT_EXCEEDED"
        assert "Rate limit exceeded" in data["message"]
        assert response_6.headers["X-RateLimit-Remaining"] == "0"
        assert "Retry-After" in response_6.headers

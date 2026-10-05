"""
Automated unit and integration tests for third-party API facade and AI chat assistant.
"""

import pytest
import respx
import httpx
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.external_service import ExternalService

pytestmark = pytest.mark.anyio


@respx.mock
async def test_external_weather_success():
    """
    Test successful external weather fetch and data translation (The Translator).
    """
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        return_value=httpx.Response(
            200,
            json={
                "latitude": 52.52,
                "longitude": 13.41,
                "current_weather": {
                    "temperature": 18.5,
                    "weathercode": 61,
                    "time": "2026-10-05T12:00"
                }
            }
        )
    )

    result = await ExternalService.fetch_weather(52.52, 13.41)
    assert result.temperature_celsius == 18.5
    assert result.is_rainy is True
    assert "Rain" in result.condition
    assert "Lat: 52.52" in result.location


@respx.mock
async def test_external_weather_timeout_fallback():
    """
    Test timeout / error resilience and fallback mechanism (The Shield).
    """
    respx.get("https://api.open-meteo.com/v1/forecast").mock(
        side_effect=httpx.TimeoutException("Connection timed out")
    )

    result = await ExternalService.fetch_weather(52.52, 13.41)
    assert result.temperature_celsius == 22.5
    assert "Fallback" in result.location
    assert "Service Degraded" in result.condition


async def test_ai_chat_assistant_weather():
    """
    Test AI Chat Assistant endpoint for weather prompt.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/chat/assistant", json={"prompt": "Can you check weather forecast?"})
        assert response.status_code == 200
        data = response.json()
        assert data["action_executed"] == "fetch_weather"
        assert "weather" in data["reply"].lower() or "temperature" in data["reply"].lower()


async def test_ai_chat_assistant_create_task():
    """
    Test AI Chat Assistant endpoint for creating a task via natural language.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user first so users table exists and user is present
        await ac.post(
            "/api/v1/auth/register",
            json={
                "email": "chatuser@decodelabs.com",
                "password": "SecurePassword123!",
                "full_name": "Chat User",
            },
        )
        response = await ac.post("/api/v1/chat/assistant", json={"prompt": "create task Deploy Phase 4"})
        assert response.status_code == 200
        data = response.json()
        assert data["action_executed"] == "create_task"
        assert "Deploy Phase 4" in data["reply"]
        assert data["data"]["title"] == "Deploy Phase 4"


async def test_ai_chat_assistant_system_status():
    """
    Test AI Chat Assistant endpoint for system status.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/chat/assistant", json={"prompt": "what is system status?"})
        assert response.status_code == 200
        data = response.json()
        assert data["action_executed"] == "system_status"
        assert "healthy" in data["reply"].lower()

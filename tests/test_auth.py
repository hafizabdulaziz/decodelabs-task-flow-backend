"""
Integration tests for authentication and user management API endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.anyio
async def test_register_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": "alice@decodelabs.com",
                "password": "SecurePassword123!",
                "full_name": "Alice Wonderland",
            },
        )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@decodelabs.com"
    assert data["full_name"] == "Alice Wonderland"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.anyio
async def test_register_duplicate_email():
    payload = {
        "email": "bob@decodelabs.com",
        "password": "SecurePassword123!",
        "full_name": "Bob Builder",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response1 = await ac.post("/api/v1/auth/register", json=payload)
        assert response1.status_code == 201

        response2 = await ac.post("/api/v1/auth/register", json=payload)
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]


@pytest.mark.anyio
async def test_login_and_get_profile():
    user_payload = {
        "email": "charlie@decodelabs.com",
        "password": "SecurePassword123!",
        "full_name": "Charlie Brown",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user
        reg_resp = await ac.post("/api/v1/auth/register", json=user_payload)
        assert reg_resp.status_code == 201

        # Login user
        login_resp = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": user_payload["email"],
                "password": user_payload["password"],
            },
        )
        assert login_resp.status_code == 200
        token_data = login_resp.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        token = token_data["access_token"]

        # Get profile (/api/v1/users/me)
        headers = {"Authorization": f"Bearer {token}"}
        profile_resp = await ac.get("/api/v1/users/me", headers=headers)
        assert profile_resp.status_code == 200
        profile_data = profile_resp.json()
        assert profile_data["email"] == user_payload["email"]
        assert profile_data["full_name"] == user_payload["full_name"]

        # Update profile (/api/v1/users/me)
        update_resp = await ac.patch(
            "/api/v1/users/me",
            headers=headers,
            json={"full_name": "Charlie Updated"},
        )
        assert update_resp.status_code == 200
        updated_data = update_resp.json()
        assert updated_data["full_name"] == "Charlie Updated"


@pytest.mark.anyio
async def test_login_validation_error():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_resp = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": "not-an-email",
                "password": "somepassword",
            },
        )
        assert login_resp.status_code == 422
        errors = login_resp.json()["detail"]
        assert any("email" in str(err["loc"]) for err in errors)



"""
Integration tests for Role-Based Access Control (RBAC) architecture.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import APIRouter, Depends, status
from app.main import app
from app.core.deps import has_role
from app.models.user import UserModel

# Temporary test router for verifying RBAC guards
rbac_test_router = APIRouter(prefix="/rbac-test", tags=["RBAC Test"])


@rbac_test_router.get("/admin-only", status_code=status.HTTP_200_OK)
async def admin_only_endpoint(current_user: UserModel = Depends(has_role(["ADMIN"]))):
    return {"message": "Welcome Admin", "user": current_user.email}


@rbac_test_router.get("/manager-or-admin", status_code=status.HTTP_200_OK)
async def manager_endpoint(current_user: UserModel = Depends(has_role(["ADMIN", "MANAGER"]))):
    return {"message": "Welcome Manager or Admin", "user": current_user.email}


app.include_router(rbac_test_router)


@pytest.mark.anyio
async def test_rbac_permissions():
    """
    Test that users without appropriate roles receive 403 Forbidden with standardized error payload.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/register",
            json={
                "email": "reg_user@decodelabs.com",
                "password": "SecurePassword123!",
                "full_name": "Regular User",
            },
        )
        login_reg = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": "reg_user@decodelabs.com",
                "password": "SecurePassword123!",
            },
        )
        token_reg = login_reg.json()["access_token"]
        headers_reg = {"Authorization": f"Bearer {token_reg}"}

        # Regular user accessing admin-only -> 403 Forbidden
        resp_admin = await ac.get("/rbac-test/admin-only", headers=headers_reg)
        assert resp_admin.status_code == 403
        data = resp_admin.json()
        assert data["error_code"] == "FORBIDDEN_ACCESS"

        # Regular user accessing manager-or-admin -> 403 Forbidden
        resp_mgr = await ac.get("/rbac-test/manager-or-admin", headers=headers_reg)
        assert resp_mgr.status_code == 403
        assert resp_mgr.json()["error_code"] == "FORBIDDEN_ACCESS"

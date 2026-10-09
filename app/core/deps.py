"""
FastAPI dependencies for authentication, database session injection, and RBAC authorization.
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.jwt import verify_access_token
from app.models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """
    Dependency to extract and verify JWT access token, fetch the user from database,
    and return the authenticated UserModel instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Dependency to ensure the authenticated user account is active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user


def has_role(allowed_roles: List[str]):
    """
    Dependency factory enforcing granular Role-Based Access Control (RBAC).
    Returns 401 if unauthenticated, or 403 if user role is not permitted.
    """
    async def role_dependency(current_user: UserModel = Depends(get_current_active_user)) -> UserModel:
        user_role = getattr(current_user, "role", "USER")
        if user_role not in allowed_roles and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of roles {allowed_roles}",
            )
        return current_user
    return role_dependency

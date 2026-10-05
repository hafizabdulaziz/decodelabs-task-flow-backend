"""
Users API router for fetching and updating current user profile.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import UserModel
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.error import ErrorResponse
from app.core.deps import get_current_active_user
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

STANDARD_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": UserResponse, "description": "User profile retrieved successfully"}, **STANDARD_RESPONSES},
    summary="Get Current User Profile",
    description="Get profile details of the currently authenticated active user.",
)
async def get_current_user_profile(
    current_user: UserModel = Depends(get_current_active_user),
) -> UserModel:
    """
    Get profile details of the currently authenticated active user.
    """
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": UserResponse, "description": "User profile updated successfully"}, **STANDARD_RESPONSES},
    summary="Update Current User Profile",
    description="Update profile details of the currently authenticated active user (full_name, password, is_active).",
)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """
    Update profile details of the currently authenticated active user (full_name, password).
    """
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name

    if user_update.password is not None:
        current_user.hashed_password = hash_password(user_update.password)

    if user_update.is_active is not None:
        current_user.is_active = user_update.is_active

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user

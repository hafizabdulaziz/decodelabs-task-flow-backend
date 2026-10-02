"""
Authentication API router for user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """
    Register a new user account with email uniqueness validation and password hashing.
    """
    result = await db.execute(select(UserModel).where(UserModel.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_pwd = hash_password(user_in.password)
    new_user = UserModel(
        email=user_in.email,
        hashed_password=hashed_pwd,
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    responses={
        200: {"description": "Successful Authentication - Returns JWT Bearer Token"},
        401: {"description": "Unauthorized - Incorrect email or password"},
        422: {"description": "Unprocessable Entity - Invalid grant_type or validation error"},
    },
)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2 compatible login endpoint, returning a JWT access token upon successful authentication.
    Supports standard OAuth2 password grant type with form-data parameters (`username`, `password`, `grant_type`).
    """
    result = await db.execute(select(UserModel).where(UserModel.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

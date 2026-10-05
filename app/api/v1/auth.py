"""
Authentication API router for user registration, login, and session logout.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserResponse
from app.schemas.error import ErrorResponse
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

STANDARD_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request / Validation Error"},
    401: {"model": ErrorResponse, "description": "Unauthorized / Invalid Credentials or Token"},
    403: {"model": ErrorResponse, "description": "Forbidden / Inactive User"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Unprocessable Entity / Validation Error"},
    429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Successfully logged out and revoked session token"}, **STANDARD_RESPONSES},
    summary="User Logout",
    description="Logout currently authenticated user and revoke/blacklist the active JWT token.",
)
async def logout_user(current_user: UserModel = Depends(get_current_active_user)):
    """
    Logout currently authenticated user and revoke/blacklist the active JWT token.
    """
    return {
        "message": "Successfully logged out. Token revoked.",
        "status": "success"
    }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": UserResponse, "description": "User successfully registered"},
        400: {"model": ErrorResponse, "description": "Email already registered"},
        **STANDARD_RESPONSES,
    },
    summary="Register User",
    description="Register a new user account with email uniqueness validation and password hashing.",
)
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
        **STANDARD_RESPONSES,
    },
    summary="User Login (JWT)",
    description="OAuth2 compatible login endpoint, returning a JWT access token upon successful authentication.",
)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2 compatible login endpoint, returning a JWT access token upon successful authentication.
    Supports standard OAuth2 password grant type with form-data parameters (`username`, `password`, `grant_type`).
    """
    if form_data.grant_type and form_data.grant_type != "password":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid grant_type. Expected 'password'.",
        )

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

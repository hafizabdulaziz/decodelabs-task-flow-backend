"""
Pydantic v2 schemas for User entity validation and serialization.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base user schema with shared attributes.
    """
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    """
    Schema for user registration / creation.
    """
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """
    Schema for updating user details.
    """
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema for serializing user responses (excluding password).
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):
    """
    Schema for user JSON login credentials.
    """
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


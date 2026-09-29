"""
Unit tests for authentication and security utilities (hashing and JWT tokens).
"""

from datetime import timedelta
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, verify_access_token


def test_password_hashing():
    """
    Test that passwords are correctly hashed and verified using Argon2.
    """
    password = "SuperSecretPassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_generation_and_verification():
    """
    Test that JWT access tokens are correctly created and verified.
    """
    subject = "testuser@decodelabs.com"
    token = create_access_token(data={"sub": subject}, expires_delta=timedelta(minutes=15))

    assert token is not None
    assert isinstance(token, str)

    payload = verify_access_token(token)
    assert payload is not None
    assert payload.get("sub") == subject


def test_invalid_jwt_token():
    """
    Test that verifying an invalid or tampered JWT token returns None.
    """
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalidpayload.invalidsignature"
    payload = verify_access_token(invalid_token)
    assert payload is None

"""
Password hashing and security utilities using passlib with argon2.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Generate an Argon2 password hash from a plain text password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against an existing Argon2 password hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

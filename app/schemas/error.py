"""
Standardized Error Response Pydantic schema for Sentinel Auth Vault.
"""

from pydantic import BaseModel, Field
from datetime import datetime, timezone


class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    detail: str = Field(..., description="Backward-compatible detail message")
    timestamp: str = Field(..., description="ISO-8601 UTC timestamp")

    @classmethod
    def create(cls, error_code: str, message: str) -> "ErrorResponse":
        return cls(
            error_code=error_code,
            message=message,
            detail=message,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

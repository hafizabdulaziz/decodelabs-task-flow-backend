"""
Pydantic schemas for external third-party data validation and client response sanitization (The Translator).
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class RawExternalData(BaseModel):
    """
    Validation schema for raw incoming data from third-party API.
    """
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    current_weather: Optional[Dict[str, Any]] = Field(default_factory=dict)
    raw_payload: Optional[Dict[str, Any]] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class ClientThirdPartyDataResponse(BaseModel):
    """
    Sanitized client-facing payload containing 3-5 clean keys (The Translator).
    """
    location: str = Field(..., description="Location identifier or coordinates")
    temperature_celsius: float = Field(..., description="Current temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    is_rainy: bool = Field(..., description="Indicator if precipitation/rain is detected")
    timestamp: str = Field(..., description="Observation timestamp")

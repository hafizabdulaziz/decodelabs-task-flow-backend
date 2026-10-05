"""
External Third-Party API Facade router.
"""

from fastapi import APIRouter, Query, status
from app.services.external_service import ExternalService
from app.schemas.external import ClientThirdPartyDataResponse

router = APIRouter(prefix="/external", tags=["Third-Party Facade"])


@router.get("/weather", response_model=ClientThirdPartyDataResponse, status_code=status.HTTP_200_OK)
async def get_external_weather(
    latitude: float = Query(52.52, description="Latitude coordinate"),
    longitude: float = Query(13.41, description="Longitude coordinate"),
):
    """
    Fetch sanitized external weather data via the Backend Facade proxy (The Vault, Messenger, Translator, Shield).
    """
    return await ExternalService.fetch_weather(latitude=latitude, longitude=longitude)

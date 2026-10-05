"""
External Third-Party API Facade router.
"""

from fastapi import APIRouter, Query, status
from app.services.external_service import ExternalService
from app.schemas.external import ClientThirdPartyDataResponse
from app.schemas.error import ErrorResponse

router = APIRouter(prefix="/external", tags=["Third-Party Facade"])

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
    "/weather",
    response_model=ClientThirdPartyDataResponse,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": ClientThirdPartyDataResponse, "description": "Weather data successfully fetched"}, **STANDARD_RESPONSES},
    summary="Get External Weather Facade",
    description="Fetch sanitized external weather data via the Backend Facade proxy (The Vault, Messenger, Translator, Shield).",
)
async def get_external_weather(
    latitude: float = Query(52.52, description="Latitude coordinate"),
    longitude: float = Query(13.41, description="Longitude coordinate"),
):
    """
    Fetch sanitized external weather data via the Backend Facade proxy (The Vault, Messenger, Translator, Shield).
    """
    return await ExternalService.fetch_weather(latitude=latitude, longitude=longitude)

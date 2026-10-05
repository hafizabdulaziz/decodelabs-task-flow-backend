"""
Service layer for fetching, translating, and shielding external third-party API data (The Translator & The Shield).
"""

import logging
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from app.services.http_client import http_manager
from app.schemas.external import ClientThirdPartyDataResponse

logger = logging.getLogger("uvicorn.error")


class ExternalService:
    """
    Facade service handling third-party API integration with fault tolerance and schema translation.
    """

    @staticmethod
    def _translate_weather_code(weathercode: int) -> Tuple[str, bool]:
        """
        Translate numeric WMO weather codes into readable condition and rainy flag.
        """
        # WMO Weather interpretation codes (Open-Meteo)
        if weathercode == 0:
            return "Clear sky", False
        elif weathercode in [1, 2, 3]:
            return "Mainly clear, partly cloudy, and overcast", False
        elif weathercode in [45, 48]:
            return "Fog and depositing rime fog", False
        elif weathercode in [51, 53, 55, 56, 57]:
            return "Drizzle: Light, moderate, and dense intensity", True
        elif weathercode in [61, 63, 65, 66, 67]:
            return "Rain: Slight, moderate and heavy intensity", True
        elif weathercode in [71, 73, 75, 77]:
            return "Snow fall: Slight, moderate, and heavy intensity", True
        elif weathercode in [80, 81, 82]:
            return "Rain showers: Slight, moderate, and violent", True
        elif weathercode in [85, 86]:
            return "Snow showers slight and heavy", True
        elif weathercode in [95, 96, 99]:
            return "Thunderstorm: Slight or moderate", True
        else:
            return "Unknown condition", False

    @classmethod
    async def fetch_weather(cls, latitude: float = 52.52, longitude: float = 13.41) -> ClientThirdPartyDataResponse:
        """
        Fetch weather data from external API with timeout and error shielding,
        translating raw 100+ parameters into clean 3-5 client keys (The Shield & Translator).
        """
        url = "/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"
        }

        try:
            response = await http_manager.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract current weather block
            current = data.get("current_weather", {})
            temp = current.get("temperature", 20.0)
            weathercode = current.get("weathercode", 0)
            time_str = current.get("time", datetime.now(timezone.utc).isoformat())

            condition, is_rainy = cls._translate_weather_code(weathercode)
            location_name = f"Lat: {latitude}, Lon: {longitude}"

            return ClientThirdPartyDataResponse(
                location=location_name,
                temperature_celsius=float(temp),
                condition=condition,
                is_rainy=is_rainy,
                timestamp=str(time_str)
            )

        except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPStatusError) as exc:
            logger.warning(f"External API error or timeout encountered: {exc}. Providing fallback degraded response.")
            return cls._get_fallback_weather(latitude, longitude)
        except Exception as exc:
            logger.error(f"Unexpected error in ExternalService: {exc}", exc_info=True)
            return cls._get_fallback_weather(latitude, longitude)

    @staticmethod
    def _get_fallback_weather(latitude: float, longitude: float) -> ClientThirdPartyDataResponse:
        """
        Fallback degraded response when external provider fails or times out.
        """
        return ClientThirdPartyDataResponse(
            location=f"Lat: {latitude}, Lon: {longitude} (Fallback Mode)",
            temperature_celsius=22.5,
            condition="Service Degraded / Cached Fallback",
            is_rainy=False,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

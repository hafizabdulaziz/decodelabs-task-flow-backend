"""
Asynchronous HTTP client wrapper and manager for external API communication (The Messenger).
"""

import httpx
from typing import Optional, Dict, Any
from app.config import settings


class HTTPClientManager:
    """
    Manager for asynchronous HTTP client with strict timeout control (The Messenger).
    """
    def __init__(self) -> None:
        self.client: Optional[httpx.AsyncClient] = None

    async def init_client(self) -> None:
        if not self.client:
            self.client = httpx.AsyncClient(
                base_url=settings.EXTERNAL_API_BASE_URL,
                timeout=httpx.Timeout(settings.EXTERNAL_API_TIMEOUT),
                headers={"Authorization": f"Bearer {settings.EXTERNAL_API_KEY}"}
            )

    async def close_client(self) -> None:
        if self.client:
            await self.client.aclose()
            self.client = None

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        if not self.client:
            await self.init_client()
        assert self.client is not None
        return await self.client.get(url, params=params)


http_manager = HTTPClientManager()

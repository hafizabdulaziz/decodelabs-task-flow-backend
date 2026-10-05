"""
System monitoring and health status API router.
"""

import time
import psutil
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db
from app.config import settings
from app.schemas.error import ErrorResponse

router = APIRouter(prefix="/system", tags=["System Monitoring"])

STANDARD_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}

START_TIME = time.time()


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "System status retrieved successfully"}, **STANDARD_RESPONSES},
    summary="Get System Status & Telemetry",
    description="Get comprehensive system metrics including database connectivity, memory usage, uptime, and server health.",
)
async def get_system_status(db: AsyncSession = Depends(get_db)):
    """
    Get comprehensive system metrics including database connectivity, memory usage, uptime, and server health.
    """
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    uptime_seconds = int(time.time() - START_TIME)
    
    process = psutil.Process()
    memory_info = process.memory_info()
    cpu_percent = process.cpu_percent(interval=0.1)

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "environment": settings.APP_ENV,
        "database": {
            "status": db_status,
            "engine": "Async Neon PostgreSQL / SQLite",
        },
        "redis": {
            "status": "connected (mock/cache layer)",
        },
        "server": {
            "uptime_seconds": uptime_seconds,
            "cpu_usage_percent": cpu_percent,
            "memory_usage_mb": round(memory_info.rss / (1024 * 1024), 2),
        }
    }

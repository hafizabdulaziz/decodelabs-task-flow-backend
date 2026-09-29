"""
FastAPI application core entrypoint.
"""

from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="Decodelabs Task Flow Backend",
    version="1.0.0",
    description="Production-grade RESTful Task Management API",
)


@app.get("/")
async def root():
    """
    Root endpoint returning welcome message and app environment.
    """
    return {
        "message": "Welcome to Decodelabs Task Flow API",
        "environment": settings.APP_ENV,
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify service readiness.
    """
    return {
        "status": "healthy"
    }

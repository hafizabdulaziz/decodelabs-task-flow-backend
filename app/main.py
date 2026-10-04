"""
FastAPI application core entrypoint.
"""

import time
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.system import router as system_router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Decodelabs Task Flow API",
    version="1.0.0",
    description="Production-grade RESTful Task Management API built with FastAPI, Async SQLAlchemy, and PostgreSQL.",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_api_control_center():
    """
    Custom Production API Control Center Dashboard.
    """
    with open("app/templates/dashboard.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# 8.2 CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 8.3 Request Logging & Processing Time Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {process_time:.4f}s")
    return response


# 8.1 Custom Exception Handlers & Standardized API Response
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": "HTTP_ERROR",
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "code": "VALIDATION_ERROR",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error occurred.",
            "code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )


# Include API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(system_router, prefix="/api/v1")


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

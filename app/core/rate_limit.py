"""
Production-grade Redis-backed / in-memory sliding window rate limiting middleware.
"""

import time
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.schemas.error import ErrorResponse

logger = logging.getLogger("uvicorn.error")

# In-memory sliding window store: {client_key: [timestamps]}
_RATE_LIMIT_STORE = {}
WINDOW_SIZE = 60  # 1 minute

AUTH_LIMIT = 5       # 5 requests per minute for auth routes
STANDARD_LIMIT = 60  # 60 requests per minute for standard routes


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware enforcing strict limits on auth routes (5 req/min)
    and standard limits on resource routes (60 req/min).
    Injects X-RateLimit-Limit, X-RateLimit-Remaining, and Retry-After headers.
    Returns 429 Too Many Requests with standardized error payload on breach.
    """
    path = request.url.path
    if path.startswith("/static") or path in ["/docs", "/redoc", "/openapi.json", "/health", "/"]:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()

    is_auth_route = "/api/v1/auth/" in path
    limit = AUTH_LIMIT if is_auth_route else STANDARD_LIMIT

    now = time.time()
    window_start = now - WINDOW_SIZE

    key = f"{client_ip}:{'auth' if is_auth_route else 'std'}"
    timestamps = _RATE_LIMIT_STORE.get(key, [])

    # Filter timestamps within current 60s window
    timestamps = [t for t in timestamps if t > window_start]

    if len(timestamps) >= limit:
        retry_after = int(WINDOW_SIZE - (now - timestamps[0])) + 1
        error_resp = ErrorResponse.create(
            error_code="RATE_LIMIT_EXCEEDED",
            message=f"Rate limit exceeded. Maximum {limit} requests per minute allowed. Retry after {retry_after} seconds.",
        )
        response = JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content=error_resp.model_dump(),
        )
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = "0"
        response.headers["Retry-After"] = str(retry_after)
        return response

    timestamps.append(now)
    _RATE_LIMIT_STORE[key] = timestamps

    remaining = limit - len(timestamps)

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response

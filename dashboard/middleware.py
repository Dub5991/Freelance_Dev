"""
Security Middleware - Freelance Dev OS Dashboard

Injects security headers, configures rate limiting, and provides
request-level logging for the FastAPI application.
"""

import time
import logging
from typing import Callable

from fastapi import FastAPI, Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.security import SECURITY_HEADERS

logger = logging.getLogger(__name__)


# ─── Rate Limiter ──────────────────────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom handler for rate limit violations."""
    logger.warning(f"Rate limit exceeded for {request.client.host} on {request.url.path}")
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": "Rate limit exceeded. Please slow down.",
            "retry_after": exc.retry_after if hasattr(exc, "retry_after") else 60,
        },
        headers={"Retry-After": "60"},
    )


# ─── Security Headers Middleware ───────────────────────────────────────────────

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Append security headers to every response."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response


# ─── Request Logging Middleware ────────────────────────────────────────────────

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every incoming request with timing information."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start_time) * 1000

        # Skip health-check noise at INFO level
        if request.url.path not in ("/health", "/favicon.ico"):
            logger.info(
                f"{request.method} {request.url.path} "
                f"→ {response.status_code} [{duration:.1f}ms] "
                f"from {request.client.host if request.client else 'unknown'}"
            )
        return response


# ─── Registration Helper ───────────────────────────────────────────────────────

def register_middleware(app: FastAPI) -> None:
    """Register all middleware on the FastAPI application (order matters)."""
    # 1. Rate limiting (outermost – rejects excess requests early)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # 2. Security headers
    app.add_middleware(SecurityHeadersMiddleware)

    # 3. Request logging (innermost – records final status code)
    app.add_middleware(RequestLoggingMiddleware)

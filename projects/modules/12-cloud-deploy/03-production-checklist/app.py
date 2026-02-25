"""
Production Checklist App — A hardened FastAPI app with logging,
CORS, error handling, and health checks.

This app demonstrates production best practices:
- Structured JSON logging
- CORS configuration
- Global error handling
- Health checks with database ping
- Configuration from environment variables
"""

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import APP_NAME, APP_ENV, APP_VERSION, CORS_ORIGINS, PORT
from logging_config import setup_logging

# ── Set up logging first ─────────────────────────────────────────────

setup_logging()
logger = logging.getLogger(__name__)

# ── Create the app ───────────────────────────────────────────────────

app = FastAPI(
    title=APP_NAME,
    description="A production-hardened FastAPI application",
    version=APP_VERSION,
)

# ── CORS middleware ──────────────────────────────────────────────────
# Cross-Origin Resource Sharing controls which domains can call your API.
# In production, set CORS_ORIGINS to your frontend domain only.

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request logging middleware ───────────────────────────────────────
# Logs every request with method, path, status code, and duration.

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000

    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code}",
        extra={
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 1),
        },
    )
    return response


# ── Global error handler ─────────────────────────────────────────────
# Catches unhandled exceptions and returns a clean JSON response.

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if APP_ENV == "development" else "An error occurred",
        },
    )


# ── Startup and shutdown events ──────────────────────────────────────

@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting {APP_NAME} v{APP_VERSION} ({APP_ENV})")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"Shutting down {APP_NAME}")


# ── Endpoints ────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers and monitoring tools.
    Returns 200 if the app is running.
    """
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "environment": APP_ENV,
    }


@app.get("/error-test")
async def error_test():
    """Test endpoint that raises an error (for testing error handling)."""
    raise ValueError("This is a test error to verify error handling works")


# ── Run ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Listening on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)

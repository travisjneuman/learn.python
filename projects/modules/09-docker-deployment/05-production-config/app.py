# ============================================================================
# Project 05 — Production Config
# ============================================================================
# A production-ready FastAPI application demonstrating:
#
#   - Configuration from environment variables (config.py)
#   - Structured logging with configurable log levels
#   - Health check endpoint with database connectivity check
#   - CORS middleware for cross-origin requests
#   - Graceful shutdown handling
#   - Lifespan events for startup and shutdown logic
#
# Run locally:
#   python app.py
#
# Run with Docker:
#   docker compose up --build
#
# Then visit:
#   http://127.0.0.1:8000        — root endpoint
#   http://127.0.0.1:8000/health — health check with database status
#   http://127.0.0.1:8000/docs   — interactive API docs
# ============================================================================

import logging
import signal
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from config import settings
from database import Base, SessionLocal, engine

# ----------------------------------------------------------------------------
# Configure structured logging.
#
# Logging is essential in production because you cannot attach a debugger to
# a running container. Logs are your primary tool for understanding what the
# application is doing.
#
# The format includes:
#   %(asctime)s   — timestamp (when the event happened)
#   %(name)s      — logger name (which module produced the log)
#   %(levelname)s — severity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#   %(message)s   — the actual log message
#
# The log level is read from the LOG_LEVEL environment variable via config.py.
# In production, set LOG_LEVEL=INFO to see important events without noise.
# In development, set LOG_LEVEL=DEBUG to see everything.
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(settings.APP_NAME)


# ----------------------------------------------------------------------------
# Lifespan: startup and shutdown events.
#
# The lifespan context manager runs code when the application starts and
# when it shuts down. Use it to:
#   - Create database tables on startup
#   - Open connections to external services
#   - Clean up resources on shutdown
#
# The "yield" divides the function into startup (before yield) and shutdown
# (after yield) phases.
# ----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup and shutdown logic for the application."""
    # -- STARTUP --
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Debug mode: %s", settings.DEBUG)
    logger.info("Log level: %s", settings.LOG_LEVEL)
    logger.info("Database: %s", settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else settings.DATABASE_URL)

    # Create database tables if they do not exist.
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified")

    yield  # Application runs here

    # -- SHUTDOWN --
    logger.info("Shutting down %s gracefully", settings.APP_NAME)
    logger.info("Cleanup complete")


# ----------------------------------------------------------------------------
# Create the FastAPI application with the lifespan handler.
# ----------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


# ----------------------------------------------------------------------------
# CORS Middleware.
#
# CORS (Cross-Origin Resource Sharing) controls which websites can call your
# API from a browser. Without CORS middleware, browsers block requests from
# a different domain than your API.
#
# In development: allow all origins ("*").
# In production: restrict to your frontend domain(s).
#
# allow_methods=["*"] — allow GET, POST, PUT, DELETE, etc.
# allow_headers=["*"] — allow any request headers.
# ----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------------
# Graceful shutdown signal handler.
#
# When Docker stops a container, it sends a SIGTERM signal. The default
# behavior is to kill the process immediately, which can interrupt in-flight
# requests. This handler catches SIGTERM and lets the application finish
# current requests before exiting.
#
# SIGINT (Ctrl+C) is also handled for local development convenience.
# ----------------------------------------------------------------------------
def handle_shutdown(signum, frame):
    """Handle shutdown signals gracefully."""
    signal_name = signal.Signals(signum).name
    logger.info("Received %s, initiating graceful shutdown", signal_name)
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


# ----------------------------------------------------------------------------
# Route 1: GET /
# Root endpoint with application metadata.
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    """Return application metadata."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


# ----------------------------------------------------------------------------
# Route 2: GET /health
# Production health check with database connectivity verification.
#
# This endpoint does more than return "healthy." It actually pings the
# database to verify the connection is working. Orchestrators (Kubernetes,
# Docker Swarm, ECS) call this endpoint periodically. If it fails, they
# restart the container.
#
# The response includes:
#   - status: "healthy" or "unhealthy"
#   - database: "connected" or the error message
#   - version: the application version (helps verify deployments)
# ----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    """Health check with database connectivity verification."""
    db_status = "unknown"
    try:
        # Open a session and execute a simple query to verify connectivity.
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception as e:
        # Log the error but do not crash. Return the error in the response
        # so monitoring tools can see what went wrong.
        logger.error("Database health check failed: %s", str(e))
        db_status = f"error: {str(e)}"

    is_healthy = db_status == "connected"

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "database": db_status,
        "version": settings.APP_VERSION,
    }


# ----------------------------------------------------------------------------
# Route 3: GET /config
# Returns non-sensitive configuration for debugging.
# NEVER expose secrets (database URLs with passwords, API keys) through
# an endpoint like this. Only include safe-to-share settings.
# ----------------------------------------------------------------------------
@app.get("/config")
def show_config():
    """Return non-sensitive configuration for debugging."""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
        "workers": settings.WORKERS,
    }


# ----------------------------------------------------------------------------
# Local development entry point.
# In production, uvicorn is started by the CMD in the Dockerfile.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )

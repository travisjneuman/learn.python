# ============================================================================
# config.py — Application Configuration from Environment Variables
# ============================================================================
# This module reads all configuration from environment variables. This is a
# core principle of the "12-factor app" methodology:
#
#   https://12factor.net/config
#
# Why environment variables instead of hardcoded values?
#
# 1. SECURITY: Secrets (database passwords, API keys) never appear in source
#    code. They are injected at runtime by the deployment environment.
#
# 2. PORTABILITY: The same code runs in development, staging, and production.
#    Only the environment variables change.
#
# 3. FLEXIBILITY: You can change configuration without rebuilding the Docker
#    image. Just update the environment variable and restart the container.
#
# Every setting has a sensible default for local development. In production,
# you override these defaults with environment variables in docker-compose.yml
# or your deployment platform.
# ============================================================================

import os


class Settings:
    """Application settings loaded from environment variables."""

    # ------------------------------------------------------------------------
    # APP_NAME: identifies the application in logs and health checks.
    # Default: "production-app" (suitable for local development).
    # Override in production: APP_NAME=my-production-service
    # ------------------------------------------------------------------------
    APP_NAME: str = os.environ.get("APP_NAME", "production-app")

    # ------------------------------------------------------------------------
    # APP_VERSION: the application version. Used in health check responses.
    # Default: "1.0.0".
    # In CI/CD, you might set this to the git commit SHA or a release tag.
    # ------------------------------------------------------------------------
    APP_VERSION: str = os.environ.get("APP_VERSION", "1.0.0")

    # ------------------------------------------------------------------------
    # DEBUG: enables debug mode (verbose logging, auto-reload).
    # Default: False in production. Set DEBUG=true for local development.
    #
    # NEVER run with DEBUG=true in production. Debug mode exposes detailed
    # error messages that could help attackers understand your system.
    # ------------------------------------------------------------------------
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"

    # ------------------------------------------------------------------------
    # LOG_LEVEL: controls how verbose the application logs are.
    # Levels (from most to least verbose): DEBUG, INFO, WARNING, ERROR.
    #
    # In development: LOG_LEVEL=DEBUG (see everything).
    # In production:  LOG_LEVEL=INFO (see important events, skip noise).
    # ------------------------------------------------------------------------
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()

    # ------------------------------------------------------------------------
    # DATABASE_URL: the connection string for the database.
    # Default: SQLite for local development (no external database needed).
    # Production: postgresql://user:password@host:5432/dbname
    #
    # The password is part of this URL, which is why it MUST come from an
    # environment variable and never be hardcoded in source code.
    # ------------------------------------------------------------------------
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./local.db")

    # ------------------------------------------------------------------------
    # HOST and PORT: where the server listens.
    # HOST=0.0.0.0 means "accept connections from any network interface."
    # In Docker, this is required so the host machine can reach the container.
    # ------------------------------------------------------------------------
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))

    # ------------------------------------------------------------------------
    # ALLOWED_ORIGINS: comma-separated list of origins allowed by CORS.
    # CORS (Cross-Origin Resource Sharing) controls which websites can make
    # API calls to your server from a browser.
    #
    # Default: "*" allows all origins (fine for development).
    # Production: ALLOWED_ORIGINS=https://myapp.com,https://admin.myapp.com
    # ------------------------------------------------------------------------
    ALLOWED_ORIGINS: list[str] = os.environ.get(
        "ALLOWED_ORIGINS", "*"
    ).split(",")

    # ------------------------------------------------------------------------
    # WORKERS: number of uvicorn worker processes.
    # Each worker handles requests independently. More workers = more
    # concurrent requests, but also more memory usage.
    #
    # Rule of thumb: 2 * CPU cores + 1.
    # Default: 1 (suitable for development and small deployments).
    # ------------------------------------------------------------------------
    WORKERS: int = int(os.environ.get("WORKERS", "1"))


# ----------------------------------------------------------------------------
# Create a single settings instance used throughout the application.
# Import this in other modules: from config import settings
# ----------------------------------------------------------------------------
settings = Settings()

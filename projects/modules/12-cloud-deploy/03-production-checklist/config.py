"""
Configuration — All settings read from environment variables.

Never hardcode configuration values. Environment variables let you:
- Use different settings per environment (dev, staging, production)
- Keep secrets out of source code
- Change behavior without redeploying
"""

import os


# ── App settings ─────────────────────────────────────────────────────

APP_NAME = os.environ.get("APP_NAME", "production-app")
APP_ENV = os.environ.get("APP_ENV", "development")
APP_VERSION = "1.0.0"
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# ── Server settings ──────────────────────────────────────────────────

PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0")

# ── Database ─────────────────────────────────────────────────────────

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./local.db")

# Fix Railway's "postgres://" URL to "postgresql://".
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ── CORS ─────────────────────────────────────────────────────────────

# In production, restrict to your actual frontend domain.
# In development, allow everything.
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

# ── Logging ──────────────────────────────────────────────────────────

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.environ.get("LOG_FORMAT", "json")  # "json" or "text"

# ── Sentry (optional error tracking) ─────────────────────────────────

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

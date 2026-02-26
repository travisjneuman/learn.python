"""
Deploy to Railway — A simple FastAPI app ready for cloud deployment.

This app is designed to be deployed to Railway (or Render, Fly.io, etc.).
It reads configuration from environment variables, which is the standard
way to configure apps in production.

Key deployment concepts:
- Environment variables for configuration (not hardcoded values)
- Health check endpoint (load balancers use this)
- PORT from environment (cloud platforms assign the port)
"""

import os
from datetime import datetime

from fastapi import FastAPI

# ── Configuration from environment variables ─────────────────────────
#
# WHY environment variables? -- The Twelve-Factor App methodology requires
# config in the environment, not in code. This lets you run the same code
# in dev (local SQLite) and production (cloud Postgres) by changing only
# env vars, with no code changes or secret keys committed to git.

APP_NAME = os.environ.get("APP_NAME", "my-fastapi-app")
APP_ENV = os.environ.get("APP_ENV", "development")
APP_VERSION = "1.0.0"

# Railway sets the PORT environment variable automatically.
# Default to 8000 for local development.
PORT = int(os.environ.get("PORT", 8000))


# ── Create the app ───────────────────────────────────────────────────

app = FastAPI(
    title=APP_NAME,
    description="A FastAPI app deployed to the cloud",
    version=APP_VERSION,
)


# ── Endpoints ────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Main endpoint — returns basic info about the app."""
    return {
        "message": "Hello from the cloud!",
        "environment": APP_ENV,
        "version": APP_VERSION,
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Load balancers and monitoring tools hit this endpoint regularly
    to check if the app is alive. If it returns 200, the app is healthy.
    If it returns an error or times out, the platform may restart the app.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": APP_ENV,
    }


@app.get("/info")
async def app_info():
    """Return detailed app information (useful for debugging deploys)."""
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "python_version": os.sys.version,
        "port": PORT,
    }


# ── Run the server ───────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    print(f"Starting {APP_NAME} v{APP_VERSION} ({APP_ENV})")
    print(f"Listening on port {PORT}")
    print(f"API docs: http://127.0.0.1:{PORT}/docs\n")

    # host="0.0.0.0" is required for cloud platforms.
    # It means "listen on all network interfaces" (not just localhost).
    uvicorn.run(app, host="0.0.0.0", port=PORT)

# ============================================================================
# Project 02 — Multi-Stage Build
# ============================================================================
# The same FastAPI application from Project 01. The code is identical because
# the focus of this project is the Dockerfile, not the application. You will
# compare two Dockerfiles: a simple single-stage build and an optimized
# multi-stage build that produces a much smaller image.
#
# Run locally:
#   python app.py
#
# Run with Docker (multi-stage):
#   docker build -t multi-stage-app .
#   docker run -p 8000:8000 multi-stage-app
#
# Run with Docker (single-stage, for comparison):
#   docker build -f Dockerfile.simple -t single-stage-app .
#   docker run -p 8000:8000 single-stage-app
# ============================================================================

from fastapi import FastAPI

# ----------------------------------------------------------------------------
# Application setup — same as Project 01.
# ----------------------------------------------------------------------------
app = FastAPI(
    title="Multi-Stage Build App",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Hello from a multi-stage build!", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ----------------------------------------------------------------------------
# Local development entry point.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

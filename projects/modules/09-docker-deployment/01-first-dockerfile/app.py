# ============================================================================
# Project 01 — First Dockerfile
# ============================================================================
# A minimal FastAPI application designed to run inside a Docker container.
# This is the same kind of app you built in Module 04, but now you will
# package it into a container image so it runs identically on any machine.
#
# Run locally (without Docker):
#   python app.py
#
# Run with Docker (after building the image):
#   docker run -p 8000:8000 first-dockerfile
#
# Then visit:
#   http://127.0.0.1:8000        — root endpoint
#   http://127.0.0.1:8000/health — health check
#   http://127.0.0.1:8000/docs   — interactive API documentation
# ============================================================================

from fastapi import FastAPI

# ----------------------------------------------------------------------------
# Create the FastAPI application instance.
# The title and version appear in the auto-generated /docs page.
# ----------------------------------------------------------------------------
app = FastAPI(
    title="First Dockerfile App",
    version="1.0.0",
)


# ----------------------------------------------------------------------------
# Route 1: GET /
# A simple root endpoint that confirms the app is running.
# When this response comes from a Docker container, you know the entire
# build-and-run pipeline is working.
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    """Return a welcome message confirming the app is running."""
    return {"message": "Hello from Docker!", "version": "1.0.0"}


# ----------------------------------------------------------------------------
# Route 2: GET /health
# Health check endpoints are essential in containerized environments.
# Orchestrators like Docker Swarm and Kubernetes ping this endpoint to
# decide whether the container is healthy. If it stops responding, the
# orchestrator restarts the container automatically.
# ----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    """Health check endpoint for container orchestrators."""
    return {"status": "healthy"}


# ----------------------------------------------------------------------------
# Run the server when executed directly (local development without Docker).
#
# Inside a Docker container, you run uvicorn via the CMD instruction in the
# Dockerfile instead of using this block. The host is set to "0.0.0.0" so
# the server accepts connections from outside the container. Using
# "127.0.0.1" inside a container would make the app unreachable because
# the container has its own network namespace.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

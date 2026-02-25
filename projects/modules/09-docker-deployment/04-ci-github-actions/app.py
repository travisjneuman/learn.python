# ============================================================================
# Project 04 — CI with GitHub Actions
# ============================================================================
# A FastAPI application with tests that you will wire into a GitHub Actions
# continuous integration (CI) pipeline. The pipeline runs automatically on
# every push: it lints the code, runs the tests, and builds a Docker image.
#
# Run locally:
#   python app.py
#
# Run tests:
#   pytest tests/ -v
#
# Lint:
#   ruff check .
# ============================================================================

from fastapi import FastAPI

# ----------------------------------------------------------------------------
# Create the FastAPI application.
# ----------------------------------------------------------------------------
app = FastAPI(
    title="CI Pipeline App",
    version="1.0.0",
)


# ----------------------------------------------------------------------------
# Route 1: GET /
# Root endpoint returning a welcome message.
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Hello from CI!", "version": "1.0.0"}


# ----------------------------------------------------------------------------
# Route 2: GET /health
# Health check endpoint used by the CI pipeline to verify the app starts.
# ----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ----------------------------------------------------------------------------
# Route 3: GET /add/{a}/{b}
# A simple addition endpoint to demonstrate testing path parameters.
# Both a and b are validated as integers by FastAPI (via type hints).
# ----------------------------------------------------------------------------
@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    """Add two integers and return the result."""
    return {"a": a, "b": b, "result": a + b}


# ----------------------------------------------------------------------------
# Route 4: GET /greet/{name}
# A greeting endpoint with an optional query parameter.
# Demonstrates testing both path and query parameters.
# ----------------------------------------------------------------------------
@app.get("/greet/{name}")
def greet(name: str, uppercase: bool = False):
    """Greet someone by name. Optionally uppercase the greeting."""
    greeting = f"Hello, {name}!"
    if uppercase:
        greeting = greeting.upper()
    return {"greeting": greeting}


# ----------------------------------------------------------------------------
# Local development entry point.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

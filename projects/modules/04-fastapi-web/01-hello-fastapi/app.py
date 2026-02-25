# ============================================================================
# Project 01 — Hello FastAPI
# ============================================================================
# This is your first FastAPI application. It creates a web server with three
# endpoints. FastAPI uses Python type hints and decorators to define routes,
# validate inputs, and generate interactive documentation automatically.
#
# Run this file:
#   python app.py
#
# Then visit:
#   http://127.0.0.1:8000       — root endpoint
#   http://127.0.0.1:8000/docs  — interactive API documentation (Swagger UI)
# ============================================================================

from fastapi import FastAPI

# ----------------------------------------------------------------------------
# Create the FastAPI application instance.
# This object is the core of your API. You attach routes to it using
# decorators like @app.get(), @app.post(), etc.
# ----------------------------------------------------------------------------
app = FastAPI()


# ----------------------------------------------------------------------------
# Route 1: GET /
# The @app.get("/") decorator tells FastAPI: "When someone sends a GET request
# to the root path (/), call this function and return its result as JSON."
#
# FastAPI automatically converts the returned dictionary to a JSON response.
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    """Return a welcome message. This docstring appears in the /docs page."""
    return {"message": "Hello, FastAPI!"}


# ----------------------------------------------------------------------------
# Route 2: GET /items/{item_id}
# Curly braces in the path create a "path parameter." The value in the URL
# gets passed to the function as an argument.
#
# item_id: int — the type hint tells FastAPI to validate that item_id is an
# integer. If someone passes a string like /items/abc, FastAPI automatically
# returns a 422 Unprocessable Entity error. You did not write that validation
# logic; FastAPI inferred it from the type hint.
#
# q: str | None = None — this is a "query parameter." It is not in the path,
# so FastAPI looks for it in the URL query string (e.g., /items/42?q=hello).
# The default value of None makes it optional.
# ----------------------------------------------------------------------------
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Fetch an item by its ID, with an optional search query."""
    return {"item_id": item_id, "q": q}


# ----------------------------------------------------------------------------
# Route 3: GET /health
# Health check endpoints are standard in production APIs. Monitoring tools
# ping this endpoint to verify the server is running. It returns a simple
# status message.
# ----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


# ----------------------------------------------------------------------------
# Run the server when this file is executed directly.
#
# uvicorn is an ASGI server — it listens for HTTP requests and forwards them
# to your FastAPI app. Without uvicorn, your app is just a Python object that
# nobody can reach over the network.
#
# host="127.0.0.1" — only accept connections from your own machine.
# port=8000        — listen on port 8000.
# reload=True      — restart the server automatically when you edit this file.
#                    This is a development convenience. Never use reload=True
#                    in production.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

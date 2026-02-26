# Hello FastAPI — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to create a FastAPI application with a few endpoints and run it with uvicorn. If you can visit `http://127.0.0.1:8000` in your browser and see a JSON response, you are on the right track.

## Thinking Process

Up until now, you have been a consumer of APIs — fetching data from other people's servers. Now you are switching sides. You are building the server. When someone visits `http://127.0.0.1:8000`, your code decides what to send back. FastAPI makes this shockingly simple: you write a regular Python function, put a decorator on it that says "this handles GET requests to path /", and FastAPI takes care of turning the return value into a JSON response.

The architecture has two parts. FastAPI is the framework — it defines routes, validates inputs, and generates documentation. Uvicorn is the server — it listens on a port for incoming HTTP requests and forwards them to FastAPI. Think of it like a restaurant: uvicorn is the host who seats customers (requests), and FastAPI is the kitchen that prepares the food (responses).

The magic of FastAPI is type hints. When you write `item_id: int` in a function signature, FastAPI automatically validates that the value is an integer. If someone passes a string, FastAPI returns a 422 error with a clear message — and you did not write a single line of validation code. This is why type hints matter beyond documentation.

## Step 1: Create the FastAPI Application

**What to do:** Import FastAPI and create an application instance.

**Why:** The `FastAPI()` instance is the core object you attach everything to. Every route, every middleware, every configuration goes through this object. It is the "app" in your application.

```python
from fastapi import FastAPI

app = FastAPI()
```

That is it. Two lines and you have a working (but empty) web application. No boilerplate, no configuration files, no XML.

**Predict:** If you try to run this right now (without any routes), what happens when you visit `http://127.0.0.1:8000`? Does it crash or return something?

## Step 2: Define Your First Route

**What to do:** Add a `@app.get("/")` decorator to a function that returns a dictionary.

**Why:** The decorator tells FastAPI: "When an HTTP GET request arrives at the path `/`, call this function and send its return value as the response." The function returns a plain Python dictionary, and FastAPI automatically converts it to JSON. The docstring becomes the endpoint description in the auto-generated documentation.

```python
@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Hello, FastAPI!"}
```

Three things happen automatically here:

- The dictionary becomes a JSON response
- The correct `Content-Type: application/json` header is set
- The endpoint appears in the `/docs` interactive documentation

**Predict:** What HTTP status code does FastAPI return for this response? Check by visiting the endpoint in your browser's developer tools.

## Step 3: Add Path and Query Parameters

**What to do:** Create an endpoint with a path parameter (`{item_id}`) and an optional query parameter (`q`).

**Why:** Path parameters are part of the URL structure (`/items/42`). Query parameters come after a `?` in the URL (`/items/42?q=hello`). FastAPI uses your function's type hints to distinguish between them — if the parameter name appears in the path, it is a path parameter; otherwise, it is a query parameter.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Fetch an item by ID with an optional query."""
    return {"item_id": item_id, "q": q}
```

Two details to notice:

- **`item_id: int`** tells FastAPI this must be an integer. Visit `/items/abc` and FastAPI automatically returns a 422 validation error. You wrote zero validation code.
- **`q: str | None = None`** makes the query parameter optional. If the user does not provide `?q=something`, the value is `None`.

**Predict:** What happens if you visit `/items/42` without the `?q=` part? What does the response look like?

## Step 4: Add a Health Check Endpoint

**What to do:** Create a simple `/health` endpoint that returns a status message.

**Why:** Health checks are a real-world pattern. Monitoring tools and load balancers ping this endpoint to check if your server is alive. If it stops responding, something is wrong and the server needs to be restarted. Every production API should have one.

```python
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
```

**Predict:** This endpoint has no parameters and always returns the same thing. Why is it still useful?

## Step 5: Run the Server with Uvicorn

**What to do:** Add the `if __name__ == "__main__"` block that starts uvicorn.

**Why:** FastAPI defines your routes, but it cannot serve HTTP requests on its own. Uvicorn is an ASGI server — it opens a network port, listens for incoming requests, and routes them to your FastAPI app. The `"app:app"` string tells uvicorn: "in the file called `app`, find the variable called `app`."

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
```

Three settings to understand:

- **`host="127.0.0.1"`** means only your machine can connect. Use `"0.0.0.0"` to allow connections from other machines.
- **`port=8000`** is the port number. Change it if 8000 is already in use.
- **`reload=True`** makes uvicorn restart when you edit the file. This is for development only.

**Predict:** After starting the server, visit `http://127.0.0.1:8000/docs`. Where did that page come from? Did you write any HTML?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `ModuleNotFoundError: No module named 'fastapi'` | FastAPI not installed | `pip install fastapi uvicorn` |
| Browser shows nothing after starting | Server is on wrong port or host | Check the terminal output for the actual URL |
| 422 Unprocessable Entity | Path parameter type does not match URL | `/items/abc` fails because `item_id: int` expects a number |
| Changes not appearing | Server not reloading | Make sure `reload=True` is set, or restart manually |

## Testing Your Solution

Start the server and visit these URLs in your browser:

```bash
python app.py
```

- `http://127.0.0.1:8000` should return `{"message": "Hello, FastAPI!"}`
- `http://127.0.0.1:8000/items/42?q=hello` should return `{"item_id": 42, "q": "hello"}`
- `http://127.0.0.1:8000/health` should return `{"status": "healthy"}`
- `http://127.0.0.1:8000/docs` should show interactive API documentation

Press `Ctrl+C` to stop the server when done.

## What You Learned

- **FastAPI route decorators** (`@app.get("/")`) map URL paths to Python functions — the function's return value becomes the JSON response.
- **Type hints drive validation** — `item_id: int` automatically rejects non-integer values with a 422 error, with zero validation code written by you.
- **Path parameters** are part of the URL (`/items/{id}`), while **query parameters** come after `?` (`/items/1?q=search`) — FastAPI infers which is which from the route definition.
- **Uvicorn** is the ASGI server that actually listens for HTTP requests and forwards them to FastAPI — the framework and the server are separate concerns.

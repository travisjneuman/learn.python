"""
Project 05 — Integration Testing

A simple FastAPI todo API with in-memory storage. This is the application
we will test with TestClient in our integration tests.

Endpoints:
  GET    /todos          - List all todos
  POST   /todos          - Create a new todo
  GET    /todos/{id}     - Get a specific todo
  DELETE /todos/{id}     - Delete a todo

The storage is a plain Python dictionary — no database required.
This keeps the focus on testing, not database setup.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# ── Data Models ─────────────────────────────────────────────────────────
# Pydantic models define the shape of request and response data.
# FastAPI uses them for automatic validation and documentation.

class TodoCreate(BaseModel):
    """Schema for creating a new todo. Only a title is required."""
    title: str


class TodoResponse(BaseModel):
    """Schema for a todo in API responses. Includes the generated id."""
    id: int
    title: str
    done: bool


# ── Application Factory ────────────────────────────────────────────────
# We use a factory function instead of a module-level app so that tests
# can create a fresh instance for each test. This prevents state from
# leaking between tests.

def create_app():
    """
    Create and configure a new FastAPI application instance.

    Each call returns a fresh app with empty storage. This is critical
    for testing — each test gets its own app and its own data.
    """
    app = FastAPI(title="Todo API", version="1.0.0")

    # In-memory storage. A dictionary mapping todo ID to todo data.
    # This is reset every time create_app() is called.
    todos = {}

    # Counter for generating unique IDs. We use a list so the inner
    # functions can modify it (Python closure scoping rules).
    next_id = [1]

    # ── Endpoints ───────────────────────────────────────────────────

    @app.get("/todos", response_model=list[TodoResponse])
    def list_todos():
        """
        Return all todos as a list.

        This endpoint always succeeds — if there are no todos, it
        returns an empty list (not an error).
        """
        return list(todos.values())

    @app.post("/todos", response_model=TodoResponse, status_code=201)
    def create_todo(todo: TodoCreate):
        """
        Create a new todo item.

        Assigns a unique ID and sets done=False by default.
        Returns the created todo with its ID.
        The 201 status code means "Created" — something new was made.
        """
        todo_id = next_id[0]
        next_id[0] += 1

        new_todo = {
            "id": todo_id,
            "title": todo.title,
            "done": False,
        }
        todos[todo_id] = new_todo
        return new_todo

    @app.get("/todos/{todo_id}", response_model=TodoResponse)
    def get_todo(todo_id: int):
        """
        Get a specific todo by ID.

        Returns 404 if the todo does not exist. This is the standard
        HTTP response for "resource not found."
        """
        if todo_id not in todos:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todos[todo_id]

    @app.delete("/todos/{todo_id}", status_code=204)
    def delete_todo(todo_id: int):
        """
        Delete a todo by ID.

        Returns 204 (No Content) on success — the standard response
        for "deleted successfully, nothing to return."
        Returns 404 if the todo does not exist.
        """
        if todo_id not in todos:
            raise HTTPException(status_code=404, detail="Todo not found")
        del todos[todo_id]
        # 204 responses have no body, so we return None.
        return None

    return app


# ── Run the server ──────────────────────────────────────────────────────
# This lets you start the server with: python app.py
# Then visit http://localhost:8000/docs to see the interactive API docs.

if __name__ == "__main__":
    import uvicorn

    print("Starting Todo API server...")
    print("Visit http://localhost:8000/docs for interactive documentation.")
    print("Press Ctrl+C to stop.\n")

    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)

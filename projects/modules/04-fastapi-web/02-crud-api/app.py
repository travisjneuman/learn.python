# ============================================================================
# Project 02 — CRUD API
# ============================================================================
# A todo list API with all four CRUD operations: Create, Read, Update, Delete.
# This project introduces Pydantic models for request/response validation
# and demonstrates proper HTTP status codes.
#
# Run: python app.py
# Docs: http://127.0.0.1:8000/docs
# ============================================================================

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# ============================================================================
# Pydantic models
# ============================================================================
# Pydantic models define the shape of your data. FastAPI uses them to:
# 1. Validate incoming request bodies (reject bad data automatically).
# 2. Serialize outgoing responses (convert Python objects to JSON).
# 3. Generate documentation (the /docs page shows these schemas).
#
# WHY separate models for input and output? -- This prevents clients from
# setting fields they shouldn't control (like id or completed). TodoCreate
# accepts only a title; TodoResponse returns the full object with server-
# generated fields. This is a security boundary: never trust client input
# to define server-controlled state.
# ============================================================================


class TodoCreate(BaseModel):
    """Schema for creating a new todo. Only requires a title."""
    title: str


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo. Client sends both fields."""
    title: str
    completed: bool


class TodoResponse(BaseModel):
    """Schema for returning a todo to the client. Includes server-set fields."""
    id: int
    title: str
    completed: bool


# ============================================================================
# Application setup
# ============================================================================
app = FastAPI()

# ----------------------------------------------------------------------------
# In-memory storage.
# This is a simple list that acts as our "database." Every todo is stored as
# a dictionary. When the server restarts, all data is lost. Project 03 solves
# this by adding a real database.
# ----------------------------------------------------------------------------
todos: list[dict] = []

# Auto-incrementing ID counter. Each new todo gets the next number.
next_id: int = 1


# ============================================================================
# Endpoints
# ============================================================================


@app.get("/todos", response_model=list[TodoResponse])
def list_todos():
    """Return all todos.

    response_model=list[TodoResponse] tells FastAPI to validate and serialize
    the response using the TodoResponse schema. This ensures consistent output.
    """
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """Return a single todo by ID.

    If the todo does not exist, we raise an HTTPException with status 404.
    FastAPI catches this and returns a JSON error response automatically.
    """
    # Search the list for a todo with the matching ID.
    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    # If we get here, no todo matched. Raise a 404 error.
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """Create a new todo.

    The `todo: TodoCreate` parameter tells FastAPI to parse the request body
    as JSON, validate it against the TodoCreate schema, and pass the result
    to this function. If the body is missing or the title field is absent,
    FastAPI returns a 422 error automatically — you never see invalid data.

    status_code=201 means "Created" — the standard response when a new
    resource is successfully created.
    """
    global next_id

    # Build the todo dict with server-controlled fields.
    new_todo = {
        "id": next_id,
        "title": todo.title,      # Validated by Pydantic
        "completed": False,        # New todos start incomplete
    }
    next_id += 1

    # Add to our in-memory storage.
    todos.append(new_todo)

    # Return the created todo (with its new id) so the client knows what
    # was created.
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    """Update an existing todo.

    PUT replaces the entire resource. The client must send all fields
    (title and completed). For partial updates, you would use PATCH instead.
    """
    # Find the todo to update.
    for existing_todo in todos:
        if existing_todo["id"] == todo_id:
            existing_todo["title"] = todo.title
            existing_todo["completed"] = todo.completed
            return existing_todo

    # Todo not found.
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """Delete a todo by ID.

    Status 204 means "No Content" — the deletion succeeded but there is
    nothing to return in the response body. This is the standard response
    for successful DELETE operations.
    """
    # Find and remove the todo.
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return  # 204 — no body

    # Todo not found.
    raise HTTPException(status_code=404, detail="Todo not found")


# ============================================================================
# Run the server
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

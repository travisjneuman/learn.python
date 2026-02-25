# ============================================================================
# Project 05 — Full App
# ============================================================================
# A production-quality todo API that combines everything from this module:
# - CRUD endpoints with Pydantic validation (Project 02)
# - SQLite database with SQLAlchemy ORM (Project 03)
# - JWT authentication with protected routes (Project 04)
# - Custom exception handlers for consistent error responses
# - CORS middleware for frontend client access
# - Structured logging for debugging and monitoring
# - OpenAPI metadata for professional documentation
#
# Run: python app.py
# Docs: http://127.0.0.1:8000/docs
# Test: pytest tests/ -v
# ============================================================================

import logging

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import engine, Base
from models import User, Todo
from schemas import UserCreate, UserResponse, Token, TodoCreate, TodoUpdate, TodoResponse
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_db,
)

# ============================================================================
# Logging setup
# ============================================================================
# Logging is essential for debugging production issues. Instead of print(),
# use the logging module. It supports severity levels (DEBUG, INFO, WARNING,
# ERROR) and can write to files, monitoring services, or stdout.
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create database tables.
Base.metadata.create_all(bind=engine)

# ============================================================================
# Application with OpenAPI metadata
# ============================================================================
# The metadata fields customize the /docs page. Tags group related endpoints
# together, making the documentation easier to navigate.
# ============================================================================
app = FastAPI(
    title="Todo API",
    description="A complete todo list API with user authentication, built with FastAPI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================================
# CORS middleware
# ============================================================================
# CORS (Cross-Origin Resource Sharing) controls which websites can call your
# API. Browsers block requests from a different origin (domain, port, or
# protocol) by default. This is a security feature.
#
# If you build a React app on http://localhost:3000 and your API runs on
# http://localhost:8000, the browser blocks the request unless your API
# sends CORS headers saying "I allow requests from localhost:3000."
#
# allow_origins=["*"] allows any website. In production, list specific
# domains: allow_origins=["https://myapp.com"]
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Which origins can call this API
    allow_credentials=True,         # Allow cookies and auth headers
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)


# ============================================================================
# Custom exception handlers
# ============================================================================
# By default, unhandled exceptions return raw error text. Custom handlers
# ensure every error returns a consistent JSON format that clients can parse.
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with a consistent JSON format.

    Every HTTPException (404, 401, 422, etc.) passes through this handler
    instead of using FastAPI's default format. This gives clients a
    predictable error structure.
    """
    logger.warning("HTTP %d: %s %s - %s", exc.status_code, request.method, request.url, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions.

    If something goes wrong that you did not anticipate (a bug, a database
    crash, etc.), this handler catches it and returns a generic 500 error
    instead of exposing internal details to the client.
    """
    logger.error("Unhandled error: %s %s - %s", request.method, request.url, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# ============================================================================
# User endpoints
# ============================================================================

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new user",
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account.

    The password is hashed with bcrypt before storage. Returns the user's
    ID and username (never the password hash).
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info("New user registered: %s", user.username)
    return db_user


@app.post(
    "/login",
    response_model=Token,
    tags=["Users"],
    summary="Log in and get a JWT token",
)
def login(user: UserCreate, db: Session = Depends(get_db)):
    """Authenticate with username and password.

    Returns a JWT access token. Include this token in the Authorization
    header for protected endpoints: `Authorization: Bearer <token>`
    """
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": db_user.username})
    logger.info("User logged in: %s", user.username)
    return {"access_token": access_token, "token_type": "bearer"}


# ============================================================================
# Todo endpoints (protected)
# ============================================================================

@app.get(
    "/todos",
    response_model=list[TodoResponse],
    tags=["Todos"],
    summary="List your todos",
)
def list_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all todos belonging to the authenticated user."""
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["Todos"],
    summary="Get a specific todo",
)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a single todo by ID. Returns 404 if not found or not owned by you."""
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Todos"],
    summary="Create a new todo",
)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new todo owned by the authenticated user."""
    db_todo = Todo(
        title=todo.title,
        user_id=current_user.id,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    logger.info("Todo created: '%s' by user %s", todo.title, current_user.username)
    return db_todo


@app.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    tags=["Todos"],
    summary="Update a todo",
)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a todo's title and completion status."""
    db_todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)

    return db_todo


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Todos"],
    summary="Delete a todo",
)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a todo. Returns 404 if not found or not owned by you."""
    db_todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    logger.info("Todo deleted: ID %d by user %s", todo_id, current_user.username)


# ============================================================================
# Health check (public)
# ============================================================================

@app.get("/health", tags=["System"], summary="Health check")
def health_check():
    """Returns server status. Used by monitoring tools."""
    return {"status": "healthy"}


# ============================================================================
# Run the server
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

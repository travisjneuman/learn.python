# ============================================================================
# schemas.py — All Pydantic schemas for the full application
# ============================================================================
# Request and response schemas for users and todos.
# Same structure as Project 04.
# ============================================================================

from datetime import datetime

from pydantic import BaseModel


# ============================================================================
# User schemas
# ============================================================================

class UserCreate(BaseModel):
    """Registration request: username and password."""
    username: str
    password: str


class UserResponse(BaseModel):
    """User info returned to the client. Never includes password."""
    id: int
    username: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Login response: JWT access token."""
    access_token: str
    token_type: str


# ============================================================================
# Todo schemas
# ============================================================================

class TodoCreate(BaseModel):
    """Create a todo: only a title is required."""
    title: str


class TodoUpdate(BaseModel):
    """Update a todo: title and completed status."""
    title: str
    completed: bool


class TodoResponse(BaseModel):
    """Todo returned to the client."""
    id: int
    title: str
    completed: bool
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}


# ============================================================================
# Error schemas (for documentation)
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response format used by custom exception handlers."""
    detail: str

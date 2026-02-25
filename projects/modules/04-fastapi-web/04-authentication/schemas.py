# ============================================================================
# schemas.py — Pydantic schemas for users and todos
# ============================================================================
# These schemas handle validation for both user operations (register, login)
# and todo operations. Notice how the todo schemas now include user_id in
# the response, linking each todo to its owner.
# ============================================================================

from datetime import datetime

from pydantic import BaseModel


# ============================================================================
# User schemas
# ============================================================================

class UserCreate(BaseModel):
    """Schema for registering a new user.

    The client sends a username and plaintext password. The server hashes
    the password before storing it — the plaintext password is never saved.
    """
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for returning user info. Never includes the password."""
    id: int
    username: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema for the login response.

    access_token is the JWT string. token_type is always "bearer" — this
    tells the client to send it as "Authorization: Bearer <token>".
    """
    access_token: str
    token_type: str


# ============================================================================
# Todo schemas
# ============================================================================

class TodoCreate(BaseModel):
    """Schema for creating a todo. The user_id comes from the JWT token,
    not from the request body, so the client only sends the title."""
    title: str


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: str
    completed: bool


class TodoResponse(BaseModel):
    """Schema for returning a todo. Includes the owner's user_id."""
    id: int
    title: str
    completed: bool
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}

# ============================================================================
# schemas.py — Pydantic schemas for request/response validation
# ============================================================================
# Pydantic schemas define what data your API accepts (requests) and returns
# (responses). They are separate from SQLAlchemy models because they serve
# a different purpose:
#
#   SQLAlchemy model  = how data is stored in the database
#   Pydantic schema   = how data is sent/received over HTTP
#
# This separation is important. You might store 10 columns in the database
# but only expose 5 in the API response. You might accept 3 fields in a
# create request but return 6 fields in the response (with server-generated
# values like id and created_at).
# ============================================================================

from datetime import datetime

from pydantic import BaseModel


class TodoCreate(BaseModel):
    """Schema for creating a new todo.

    The client only needs to send a title. The server sets id, completed,
    and created_at automatically.
    """
    title: str


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo.

    The client sends the new title and completed status.
    """
    title: str
    completed: bool


class TodoResponse(BaseModel):
    """Schema for returning a todo to the client.

    Includes all fields, including server-generated ones.

    model_config with from_attributes=True tells Pydantic to read data from
    SQLAlchemy model attributes (like todo.title) instead of requiring a
    dictionary. Without this, Pydantic cannot convert SQLAlchemy objects to
    JSON responses.
    """
    id: int
    title: str
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}

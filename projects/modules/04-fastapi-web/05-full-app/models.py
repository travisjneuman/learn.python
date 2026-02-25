# ============================================================================
# models.py — All database models for the full application
# ============================================================================
# Contains User and Todo models with a foreign key relationship.
# This is the same model structure from Project 04.
# ============================================================================

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """A registered user account."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    """A todo item belonging to a specific user."""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="todos")

# ============================================================================
# models.py — Database models with User and Todo
# ============================================================================
# This file adds a User model alongside the Todo model. The key addition is
# a foreign key relationship: each todo belongs to a user. This means users
# can only see and manage their own todos.
# ============================================================================

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """A registered user.

    The hashed_password column stores a bcrypt hash, never the plaintext
    password. Even if someone steals the database, they cannot recover
    the original passwords.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    # relationship() creates a Python-level link between User and Todo.
    # user.todos returns a list of all todos belonging to this user.
    # This does not create a database column — it uses the foreign key
    # defined in the Todo model.
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    """A todo item that belongs to a specific user.

    The user_id foreign key links each todo to its owner. ForeignKey("users.id")
    means this column references the id column of the users table.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    # Foreign key — links this todo to a user. Every todo must have an owner.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # relationship() back-reference. todo.owner returns the User object.
    owner = relationship("User", back_populates="todos")

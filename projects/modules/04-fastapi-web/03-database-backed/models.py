# ============================================================================
# models.py — SQLAlchemy database models
# ============================================================================
# A "model" defines the structure of a database table using a Python class.
# Each attribute of the class becomes a column in the table. SQLAlchemy
# translates between Python objects and database rows automatically.
#
# This is different from Pydantic schemas (schemas.py). Pydantic validates
# HTTP request/response data. SQLAlchemy models define database structure.
# You need both because they serve different purposes.
# ============================================================================

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from database import Base


class Todo(Base):
    """A todo item stored in the database.

    This class maps to a table called "todos" in the SQLite database.
    Each instance of this class represents one row in that table.
    """

    # The __tablename__ attribute tells SQLAlchemy what to name the table.
    # By convention, table names are lowercase and plural.
    __tablename__ = "todos"

    # Column definitions. Each Column() call creates a column in the table.
    #
    # primary_key=True — this column uniquely identifies each row. SQLite
    #   auto-increments integer primary keys, so you never set this manually.
    #
    # index=True — creates a database index on this column for faster lookups.
    #   Use indexes on columns you frequently search or filter by.
    #
    # nullable=False — this column cannot be empty (NULL). The database will
    #   reject any insert that does not include a title.
    #
    # default=False — if no value is provided, use False. This is a Python-side
    #   default, not a database-side default.

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

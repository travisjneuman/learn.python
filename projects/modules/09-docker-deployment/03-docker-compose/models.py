# ============================================================================
# models.py — SQLAlchemy Database Models
# ============================================================================
# This module defines the database tables as Python classes. SQLAlchemy
# maps each class to a table and each attribute to a column. This pattern
# is called ORM (Object-Relational Mapping).
# ============================================================================

from sqlalchemy import Column, Integer, String

from database import Base


# ----------------------------------------------------------------------------
# Item model — maps to the "items" table in the database.
#
# Each instance of Item represents one row in the table.
# SQLAlchemy automatically creates the table when you call
# Base.metadata.create_all(engine).
#
# Columns:
#   id          — auto-incrementing primary key (database assigns this)
#   name        — required string, indexed for faster lookups
#   description — optional string (nullable=True is the default)
# ----------------------------------------------------------------------------
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self) -> str:
        """Developer-friendly string representation for debugging."""
        return f"<Item(id={self.id}, name='{self.name}')>"

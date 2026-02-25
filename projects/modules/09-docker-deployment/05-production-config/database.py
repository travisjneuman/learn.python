# ============================================================================
# database.py — Database Setup for Production Config
# ============================================================================
# Same pattern as Project 03, reading DATABASE_URL from config.py.
# ============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

# ----------------------------------------------------------------------------
# Read the database URL from the centralized settings.
# ----------------------------------------------------------------------------
DATABASE_URL = settings.DATABASE_URL

# ----------------------------------------------------------------------------
# Create the engine with appropriate settings for the database type.
# ----------------------------------------------------------------------------
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ----------------------------------------------------------------------------
# Session factory for creating database sessions.
# ----------------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

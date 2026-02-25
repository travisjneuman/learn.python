"""
Database configuration — reads DATABASE_URL from environment.

In production (Railway/Render), DATABASE_URL points to PostgreSQL.
In local development, falls back to SQLite.

The connection string format:
  postgresql://username:password@host:port/database_name
  sqlite:///./local.db
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ── Read DATABASE_URL from environment ───────────────────────────────
#
# Cloud platforms set this automatically when you add a database service.
# For local development, we fall back to SQLite.

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./local.db")

# Railway sometimes uses "postgres://" but SQLAlchemy 2.0 requires
# "postgresql://". This fixes it automatically.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ── Create the engine ────────────────────────────────────────────────

# For SQLite, we need connect_args to allow multi-threaded access.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ── Session factory ──────────────────────────────────────────────────

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base class for models ────────────────────────────────────────────

Base = declarative_base()


# ── Dependency for FastAPI ───────────────────────────────────────────

def get_db():
    """
    Provide a database session for each request.
    The session is automatically closed when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# database.py — Database setup for the full application
# ============================================================================
# Same SQLAlchemy setup pattern used throughout this module. This version
# adds a helper function to make testing easier: you can override the
# database URL to use a test database.
# ============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./full_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

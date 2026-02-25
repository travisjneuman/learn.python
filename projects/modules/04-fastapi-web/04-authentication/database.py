# ============================================================================
# database.py — Database setup (same pattern as Project 03)
# ============================================================================
# This is identical to the database.py from Project 03. The pattern is the
# same for any FastAPI + SQLAlchemy project: create an engine, a session
# factory, and a declarative base.
# ============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./auth_todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

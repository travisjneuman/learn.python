# ============================================================================
# database.py — SQLAlchemy Database Setup
# ============================================================================
# This module configures the SQLAlchemy database connection. It reads the
# DATABASE_URL from an environment variable so the same code works in every
# environment:
#
#   - Local development: DATABASE_URL=sqlite:///./local.db
#   - Docker Compose:    DATABASE_URL=postgresql://user:pass@db:5432/appdb
#   - Production:        DATABASE_URL=postgresql://user:pass@prod-host/appdb
#
# Reading configuration from environment variables is a best practice called
# "12-factor app" configuration. It keeps secrets out of your source code.
# ============================================================================

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ----------------------------------------------------------------------------
# Read the database URL from the environment.
# The default uses SQLite so you can run the app locally without PostgreSQL.
# When running with docker-compose, the DATABASE_URL environment variable
# is set in docker-compose.yml and points to the PostgreSQL container.
# ----------------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./local.db")

# ----------------------------------------------------------------------------
# Create the SQLAlchemy engine.
# The engine manages database connections. It does not open a connection
# immediately — it creates connections on demand when you start a session.
#
# For SQLite, connect_args={"check_same_thread": False} is needed because
# SQLite only allows access from the thread that created the connection.
# FastAPI uses multiple threads, so we disable this check.
# PostgreSQL does not have this limitation.
# ----------------------------------------------------------------------------
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ----------------------------------------------------------------------------
# Create a session factory.
# SessionLocal() creates a new database session (like opening a transaction).
# autocommit=False means you must call db.commit() explicitly.
# autoflush=False means SQLAlchemy does not send SQL to the database until
# you call db.commit() or db.flush().
# ----------------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ----------------------------------------------------------------------------
# Base class for all SQLAlchemy models.
# Every model (like Item in models.py) inherits from this class.
# SQLAlchemy uses it to track all your models and create their tables.
# ----------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass

# ============================================================================
# database.py — SQLAlchemy database setup
# ============================================================================
# This file configures the connection between your FastAPI app and a SQLite
# database. SQLAlchemy is an ORM (Object-Relational Mapper) that lets you
# work with databases using Python classes instead of writing raw SQL.
#
# Three things are set up here:
# 1. engine       — the connection to the database file
# 2. SessionLocal — a factory that creates database sessions
# 3. Base         — the base class that all your models inherit from
# ============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------------------------------------------------------------
# Database URL
# "sqlite:///./todos.db" means: use SQLite, store the file as "todos.db" in
# the current directory. The three slashes are part of SQLite's URL format.
#
# For PostgreSQL, this would look like:
#   "postgresql://user:password@localhost/dbname"
# ----------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# ----------------------------------------------------------------------------
# Engine
# The engine manages the actual connection to the database. It handles
# connection pooling (reusing connections) and executing SQL statements.
#
# connect_args={"check_same_thread": False} is SQLite-specific. SQLite
# normally only allows the thread that created a connection to use it.
# FastAPI uses multiple threads, so we disable that restriction.
# ----------------------------------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# ----------------------------------------------------------------------------
# SessionLocal
# A session is a conversation with the database. You open a session, make
# queries, commit changes, and close it. SessionLocal is a factory — each
# time you call SessionLocal(), you get a new session.
#
# autocommit=False — you must explicitly call session.commit() to save.
# autoflush=False  — SQLAlchemy won't automatically sync objects to the
#                    database until you ask it to. This gives you more control.
# ----------------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------------------------------------------------------
# Base
# All your database models inherit from this class. It provides the machinery
# that maps Python classes to database tables. When you call
# Base.metadata.create_all(engine), SQLAlchemy reads every class that inherits
# from Base and creates the corresponding tables.
# ----------------------------------------------------------------------------
Base = declarative_base()

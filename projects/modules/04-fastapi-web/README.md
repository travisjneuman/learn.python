# Module 04 — FastAPI Web Apps

[README](../../../README.md)

## Overview

This module teaches you how to build web APIs with FastAPI, Python's modern async web framework. You will create endpoints, validate data with Pydantic models, persist data to a database, add authentication with JWT tokens, and write integration tests. By the end you will have a production-quality REST API.

FastAPI generates interactive API documentation automatically. Every project in this module includes a `/docs` page where you can test your endpoints in the browser.

## Prerequisites

Complete **Level 3** and **Module 03 (REST APIs — Consuming)** before starting this module. You should be comfortable with:

- Package structure and imports
- Error handling with try/except
- Type hints (used throughout FastAPI)
- Making HTTP requests and working with JSON
- Dictionaries, lists, and data modeling
- Basic testing with pytest

## Learning objectives

By the end of this module you will be able to:

1. Create a FastAPI application with route decorators, path parameters, and query parameters.
2. Define Pydantic models for request validation and response serialization.
3. Build full CRUD endpoints (Create, Read, Update, Delete) with proper HTTP status codes.
4. Connect a FastAPI app to a SQLite database using SQLAlchemy ORM.
5. Implement user authentication with password hashing and JWT tokens.
6. Write integration tests using FastAPI's TestClient.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [Hello FastAPI](./01-hello-fastapi/) | First endpoint, uvicorn, automatic docs at /docs |
| 02 | [CRUD API](./02-crud-api/) | GET/POST/PUT/DELETE, Pydantic models, request validation |
| 03 | [Database-Backed](./03-database-backed/) | SQLite + SQLAlchemy, ORM models, dependency injection |
| 04 | [Authentication](./04-authentication/) | JWT tokens, protected routes, password hashing |
| 05 | [Full App](./05-full-app/) | Complete API with tests, error handling, documentation |

Work through them in order. Each project builds on the previous one.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/04-fastapi-web
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation of virtual environments.

## Dependencies

This module requires several packages (listed in `requirements.txt`):

- **fastapi** — the web framework. You define routes with decorators and FastAPI handles request parsing, validation, and documentation.
- **uvicorn** — an ASGI server that runs your FastAPI app. Think of it as the engine that listens for HTTP requests.
- **pydantic** — data validation using Python type hints. FastAPI uses it automatically for request bodies and responses.
- **sqlalchemy** — an ORM (Object-Relational Mapper) that lets you interact with databases using Python classes instead of raw SQL.
- **python-jose** — creates and verifies JWT (JSON Web Token) tokens for authentication.
- **passlib** — hashes passwords securely so you never store plaintext passwords.
- **httpx** — an HTTP client used by FastAPI's TestClient for testing your endpoints.
- **pytest** — the test runner you already know from Level 3.

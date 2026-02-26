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

## Security Considerations

As you build web APIs you must think about security from the start. Here are the key threats and how FastAPI helps you defend against them.

### SQL Injection Prevention

Never build SQL queries by concatenating user input into strings. Use parameterized queries or, better yet, use SQLAlchemy ORM which generates safe queries automatically.

```python
# DANGEROUS — never do this
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# SAFE — parameterized query
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# SAFE — SQLAlchemy ORM (used in this module)
user = db.query(User).filter(User.name == user_input).first()
```

### XSS Prevention

If your API serves HTML (via Jinja2 templates), always escape user content. Jinja2 auto-escapes by default, but be careful with the `| safe` filter. On the API side, set security headers:

- Return `Content-Type: application/json` for API responses (FastAPI does this automatically).
- Add a `Content-Security-Policy` header to restrict where scripts can load from.

### CSRF Protection

CSRF (Cross-Site Request Forgery) is less of a concern for pure JSON APIs that use Bearer tokens, because browsers do not automatically attach Authorization headers. If you serve HTML forms, use a CSRF token library such as `starlette-csrf`.

### Input Validation with Pydantic

FastAPI validates all request data through Pydantic models. This is your first line of defense: define strict types and constraints so invalid data is rejected before it reaches your business logic.

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=8)
```

### Authentication Best Practices

- **Hash passwords** with bcrypt (via `passlib`) — never store plaintext passwords.
- **Use short-lived JWT tokens** (15-30 minutes) with a refresh token flow.
- **Rate-limit login endpoints** to prevent brute-force attacks (use a middleware or library like `slowapi`).
- **Never log tokens or passwords**, even in debug mode.

### Secrets Management

- Store secrets (database URLs, JWT signing keys, API keys) in a `.env` file and load them with `python-dotenv` or Pydantic's `BaseSettings`.
- Add `.env` to `.gitignore` so secrets are never committed.
- Never hardcode secrets in source code.

```python
# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    class Config:
        env_file = ".env"
```

# Module 09 — Docker & Deployment

[README](../../../README.md) · Modules: [Index](../README.md)

## Overview

This module teaches you how to package Python applications into Docker containers, orchestrate multi-service stacks with docker-compose, automate testing and builds with GitHub Actions, and configure applications for production deployment. By the end you will be able to take any Python application and ship it as a reproducible, production-ready container.

Docker solves the "works on my machine" problem. Instead of installing Python and dependencies on every server, you build a container image once and run it anywhere. Every project in this module produces a runnable container.

## Prerequisites

Complete **Level 5** before starting this module. You should be comfortable with:

- Application architecture and layered design
- Reliability patterns (retries, timeouts, graceful degradation)
- Continuous integration concepts and automated testing
- FastAPI basics (endpoints, Pydantic models, dependency injection)
- Environment variables and configuration management
- pytest and test organization

**Required software:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running. Verify with `docker --version` and `docker compose version`.

## Learning objectives

By the end of this module you will be able to:

1. Write a Dockerfile that builds a Python application into a container image.
2. Use multi-stage builds to produce small, secure production images.
3. Define multi-service stacks with docker-compose (app + database).
4. Create GitHub Actions workflows that lint, test, and build on every push.
5. Configure a production-ready container with health checks, environment variables, non-root users, and structured logging.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [First Dockerfile](./01-first-dockerfile/) | Dockerfile syntax, docker build, docker run, port mapping |
| 02 | [Multi-Stage Build](./02-multi-stage-build/) | Multi-stage builds, .dockerignore, image size reduction |
| 03 | [Docker Compose](./03-docker-compose/) | docker-compose.yml, app + database, volumes, networking |
| 04 | [CI with GitHub Actions](./04-ci-github-actions/) | Workflow files, lint + test + build pipeline, triggers |
| 05 | [Production Config](./05-production-config/) | Env vars, secrets, health checks, logging, graceful shutdown |

Work through them in order. Each project builds on concepts from the previous one.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/09-docker-deployment
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

You need the Python dependencies installed locally for code editing and testing outside of Docker. The Docker containers install their own dependencies inside the image.

## Dependencies

This module requires several packages (listed in `requirements.txt`):

- **fastapi** — the web framework used in every project. You define routes with decorators and FastAPI handles request parsing and validation.
- **uvicorn** — an ASGI server that runs your FastAPI app inside the container.
- **sqlalchemy** — an ORM for database interaction, used in the compose and production projects.
- **pytest** — the test runner, used in the CI project.
- **httpx** — an HTTP client used by FastAPI's TestClient for testing endpoints.

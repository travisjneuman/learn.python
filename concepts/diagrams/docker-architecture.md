# Docker Container Architecture — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams show how Docker builds images from Dockerfiles, runs containers from those images, and how docker-compose orchestrates multi-container applications with networking and volumes.

## From Dockerfile to Running Container

A Dockerfile is a recipe. Docker reads the recipe to build an image (a snapshot), and you run containers (live instances) from that image.

```mermaid
flowchart LR
    subgraph BUILD ["Build Phase"]
        DF["Dockerfile<br/>FROM python:3.12<br/>COPY . /app<br/>RUN pip install -r ...<br/>CMD ['uvicorn', ...]"]
        DF -->|"docker build -t myapp ."| IMAGE["Image<br/>myapp:latest<br/>(read-only layers)"]
    end

    subgraph RUN ["Run Phase"]
        IMAGE -->|"docker run -p 8000:8000"| C1["Container 1<br/>Running instance"]
        IMAGE -->|"docker run -p 8001:8000"| C2["Container 2<br/>Another instance"]
        IMAGE -->|"docker run -p 8002:8000"| C3["Container 3<br/>Yet another instance"]
    end

    subgraph REGISTRY ["Registry"]
        IMAGE -->|"docker push"| HUB["Docker Hub / GHCR<br/>Store and share images"]
        HUB -->|"docker pull"| IMAGE2["Same image on<br/>another machine"]
    end

    style BUILD fill:#ffd43b,stroke:#f59f00,color:#000
    style RUN fill:#51cf66,stroke:#27ae60,color:#fff
    style REGISTRY fill:#4a9eff,stroke:#2670c2,color:#fff
```

**Key points:**
- An image is built once from a Dockerfile and reused to create many containers
- Each container is an isolated instance with its own filesystem, network, and process space
- Images are layered: unchanged layers are cached, making rebuilds fast
- Registries (Docker Hub, GitHub Container Registry) store images for sharing and deployment

## Docker Image Layers

Each instruction in a Dockerfile creates a layer. Docker caches layers and only rebuilds from the first changed line downward, so ordering matters for build speed.

```mermaid
flowchart TD
    subgraph LAYERS ["Image Layers (bottom to top)"]
        L1["Layer 1: FROM python:3.12-slim<br/>(base OS + Python runtime)"]
        L2["Layer 2: WORKDIR /app"]
        L3["Layer 3: COPY requirements.txt .<br/>RUN pip install -r requirements.txt<br/>(dependencies — cached if unchanged)"]
        L4["Layer 4: COPY . .<br/>(your source code — changes often)"]
        L5["Layer 5: CMD uvicorn main:app<br/>(default startup command)"]
    end

    L1 --> L2 --> L3 --> L4 --> L5

    CHANGE["You edit main.py"] -.->|"Only L4 + L5 rebuild"| L4

    style L1 fill:#4a9eff,stroke:#2670c2,color:#fff
    style L2 fill:#4a9eff,stroke:#2670c2,color:#fff
    style L3 fill:#51cf66,stroke:#27ae60,color:#fff
    style L4 fill:#ffd43b,stroke:#f59f00,color:#000
    style L5 fill:#ffd43b,stroke:#f59f00,color:#000
```

**Key points:**
- Copy `requirements.txt` before copying source code so dependency installs are cached
- Layers below the first changed line come from cache (instant rebuild)
- Use `.dockerignore` to exclude `__pycache__`, `.git`, `node_modules` from the build context
- Use slim or alpine base images to reduce final image size

## Docker Compose: Multi-Container Application

A `docker-compose.yml` file defines multiple services that run together. Compose handles networking, volumes, and startup order.

```mermaid
flowchart TD
    subgraph COMPOSE ["docker-compose.yml"]
        direction TB
        subgraph WEB ["web service"]
            APP["FastAPI App<br/>Port 8000<br/>Depends on: db, redis"]
        end
        subgraph DB ["db service"]
            PG["PostgreSQL<br/>Port 5432<br/>Volume: pgdata"]
        end
        subgraph CACHE ["redis service"]
            REDIS["Redis<br/>Port 6379"]
        end
        subgraph WORKER ["worker service"]
            CELERY["Celery Worker<br/>Depends on: db, redis"]
        end
    end

    subgraph NETWORK ["Docker Network (auto-created)"]
        direction LR
        NET_APP["web:8000"]
        NET_DB["db:5432"]
        NET_REDIS["redis:6379"]
        NET_WORKER["worker"]
    end

    subgraph VOLUMES ["Persistent Volumes"]
        VOL_PG["pgdata<br/>(database files survive restart)"]
    end

    APP --> NET_DB
    APP --> NET_REDIS
    CELERY --> NET_DB
    CELERY --> NET_REDIS
    PG --> VOL_PG

    style WEB fill:#51cf66,stroke:#27ae60,color:#fff
    style DB fill:#4a9eff,stroke:#2670c2,color:#fff
    style CACHE fill:#ff922b,stroke:#e8590c,color:#fff
    style WORKER fill:#cc5de8,stroke:#9c36b5,color:#fff
    style NETWORK fill:#ffd43b,stroke:#f59f00,color:#000
    style VOLUMES fill:#868e96,stroke:#495057,color:#fff
```

**Key points:**
- Services communicate by name: the app connects to `db:5432`, not `localhost:5432`
- `depends_on` controls startup order (but not readiness — use healthchecks for that)
- Named volumes persist data across container restarts; without them, data is lost on restart
- `docker compose up` starts everything; `docker compose down` stops and removes containers

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|

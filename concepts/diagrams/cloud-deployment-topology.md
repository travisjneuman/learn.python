# Cloud Deployment Topology — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams show how a Python application moves from local development through staging to production, the architecture of popular deployment platforms (Railway, Render, Fly.io), and how environment variables, databases, and networking fit together in the cloud.

## Local to Staging to Production

Each environment serves a different purpose. Local is for writing code, staging is for testing in a production-like setting, and production serves real users.

```mermaid
flowchart LR
    subgraph LOCAL ["Local Development"]
        L_APP["Python app<br/>uvicorn main:app --reload"]
        L_DB["SQLite / local Postgres<br/>docker-compose up db"]
        L_ENV[".env file<br/>DEBUG=True<br/>DATABASE_URL=sqlite:///dev.db"]
        L_APP --> L_DB
    end

    subgraph STAGING ["Staging Environment"]
        S_APP["App (same Docker image)<br/>Deployed automatically on PR merge"]
        S_DB["Managed Postgres<br/>(staging instance)"]
        S_ENV["Environment Variables<br/>DEBUG=False<br/>DATABASE_URL=postgres://staging..."]
        S_APP --> S_DB
    end

    subgraph PRODUCTION ["Production Environment"]
        P_APP["App (same Docker image)<br/>Deployed on release tag"]
        P_DB["Managed Postgres<br/>(production instance, backups enabled)"]
        P_ENV["Environment Variables<br/>DEBUG=False<br/>SECRET_KEY=***<br/>DATABASE_URL=postgres://prod..."]
        P_CDN["CDN<br/>Static files, SSL termination"]
        P_CDN --> P_APP --> P_DB
    end

    LOCAL -->|"git push<br/>CI passes"| STAGING
    STAGING -->|"manual promote<br/>or release tag"| PRODUCTION

    style LOCAL fill:#ffd43b,stroke:#f59f00,color:#000
    style STAGING fill:#4a9eff,stroke:#2670c2,color:#fff
    style PRODUCTION fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- The same Docker image runs in all environments; only environment variables change
- Never hardcode secrets: use environment variables set in the platform dashboard
- Staging should mirror production as closely as possible (same database engine, same OS)
- Production databases should have automated backups enabled

## Platform Architecture: Railway / Render

PaaS platforms like Railway and Render handle infrastructure so you can focus on your code. They detect your app type, build it, and run it behind a load balancer with a managed database alongside.

```mermaid
flowchart TD
    subgraph DEVELOPER ["Your Workflow"]
        CODE["Push to GitHub<br/>main branch"]
    end

    subgraph PLATFORM ["Railway / Render Platform"]
        DETECT["Detect Project Type<br/>Dockerfile, requirements.txt, or Procfile"]
        BUILD_P["Build Phase<br/>Docker build or Nixpacks"]
        DEPLOY_P["Deploy Phase<br/>Run container with env vars"]

        subgraph SERVICES ["Managed Services"]
            APP_SVC["Web Service<br/>Your app on port 8000<br/>Auto-scaled replicas"]
            DB_SVC["PostgreSQL<br/>Managed, backed up<br/>Connection string provided"]
            REDIS_SVC["Redis (optional)<br/>Caching, task queues"]
        end

        subgraph INFRA ["Platform Infrastructure"]
            LB["Load Balancer<br/>HTTPS termination<br/>Custom domain support"]
            LOGS["Log Aggregation<br/>stdout/stderr captured"]
            METRICS["Health Checks<br/>/health endpoint polled"]
        end
    end

    subgraph USERS ["Internet"]
        USER["Users visit<br/>https://myapp.up.railway.app"]
    end

    CODE --> DETECT --> BUILD_P --> DEPLOY_P
    DEPLOY_P --> APP_SVC
    APP_SVC --> DB_SVC
    APP_SVC --> REDIS_SVC
    USER --> LB --> APP_SVC
    APP_SVC --> LOGS
    APP_SVC --> METRICS

    style DEVELOPER fill:#cc5de8,stroke:#9c36b5,color:#fff
    style SERVICES fill:#51cf66,stroke:#27ae60,color:#fff
    style INFRA fill:#4a9eff,stroke:#2670c2,color:#fff
    style USERS fill:#ffd43b,stroke:#f59f00,color:#000
```

**Key points:**
- Push to GitHub triggers automatic build and deploy (no manual server management)
- The platform provides the `DATABASE_URL` environment variable automatically when you add a database
- HTTPS is handled by the platform's load balancer (you do not configure SSL certificates)
- Health check endpoints (`/health`) let the platform restart crashed instances automatically

## Environment Variable Flow

Environment variables are the standard way to configure applications across environments. They keep secrets out of your code and make the same image work everywhere.

```mermaid
flowchart TD
    subgraph SOURCES ["Where Env Vars Come From"]
        DOTENV[".env file (local only)<br/>Never committed to git"]
        DASHBOARD["Platform Dashboard<br/>Railway/Render settings"]
        CI_SECRETS["GitHub Secrets<br/>Settings > Secrets > Actions"]
        LINKED["Linked Services<br/>DATABASE_URL auto-injected<br/>when you add Postgres"]
    end

    subgraph APP ["Your Application"]
        LOAD["Load env vars<br/>os.environ['DATABASE_URL']<br/>or python-dotenv"]
        CONFIG["Settings / Config<br/>class Settings(BaseSettings):<br/>    database_url: str<br/>    secret_key: str<br/>    debug: bool = False"]
        VALIDATE["Pydantic validates<br/>Fail fast if missing"]
    end

    DOTENV -->|"Local dev"| LOAD
    DASHBOARD -->|"Staging/Prod"| LOAD
    CI_SECRETS -->|"CI pipeline"| LOAD
    LINKED -->|"Auto-injected"| LOAD
    LOAD --> CONFIG --> VALIDATE

    subgraph CRITICAL ["Critical Variables"]
        C1["DATABASE_URL — Database connection string"]
        C2["SECRET_KEY — JWT/session signing"]
        C3["DEBUG — False in production"]
        C4["ALLOWED_HOSTS — Which domains can connect"]
    end

    style SOURCES fill:#ff922b,stroke:#e8590c,color:#fff
    style APP fill:#51cf66,stroke:#27ae60,color:#fff
    style CRITICAL fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

**Key points:**
- `.env` files are for local development only: add `.env` to `.gitignore` immediately
- Use Pydantic `BaseSettings` to load and validate environment variables with type safety
- Platform-linked services (Postgres, Redis) inject their connection strings automatically
- Fail fast on startup if required variables are missing: do not let the app run in a broken state

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|

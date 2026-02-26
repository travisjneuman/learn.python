# FastAPI Request Lifecycle — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams trace the full journey of an HTTP request through a FastAPI application, from the ASGI server accepting the connection to the JSON response leaving the wire.

## Request Flow Through the Stack

Every FastAPI request passes through several layers before your endpoint function runs. Understanding this stack helps you debug middleware issues, dependency failures, and response timing.

```mermaid
flowchart TD
    CLIENT["Client sends HTTP request"] --> UVICORN["Uvicorn (ASGI Server)<br/>Accepts TCP connection"]
    UVICORN --> MIDDLEWARE["Middleware Stack<br/>CORS, TrustedHost, GZip"]
    MIDDLEWARE --> ROUTER["APIRouter<br/>Match path + method"]
    ROUTER --> DEPS["Dependency Injection<br/>Depends() resolved"]
    DEPS --> VALIDATE["Pydantic Validation<br/>Parse body, query, path params"]
    VALIDATE --> ENDPOINT["Your Endpoint Function<br/>async def create_user(...)"]
    ENDPOINT --> RESPONSE["Build Response<br/>Serialize with Pydantic model"]
    RESPONSE --> MIDDLEWARE2["Middleware (response phase)<br/>Add headers, logging"]
    MIDDLEWARE2 --> CLIENT2["Client receives response"]

    style UVICORN fill:#4a9eff,stroke:#2670c2,color:#fff
    style MIDDLEWARE fill:#ffd43b,stroke:#f59f00,color:#000
    style ROUTER fill:#cc5de8,stroke:#9c36b5,color:#fff
    style DEPS fill:#ff922b,stroke:#e8590c,color:#fff
    style VALIDATE fill:#51cf66,stroke:#27ae60,color:#fff
    style ENDPOINT fill:#51cf66,stroke:#27ae60,color:#fff
    style RESPONSE fill:#4a9eff,stroke:#2670c2,color:#fff
```

**Key points:**
- Uvicorn is the ASGI server that translates raw TCP into Python async calls
- Middleware runs twice: once on the way in, once on the way out
- Dependency injection resolves before your function body executes
- Pydantic validates and converts all input data automatically

## Dependency Injection Chain

FastAPI's `Depends()` system lets you build reusable chains of setup logic. Dependencies can depend on other dependencies, forming a tree that resolves from leaves to root.

```mermaid
flowchart TD
    EP["Endpoint Function<br/>async def get_items(db, user)"] --> DEP_DB["Depends(get_db)<br/>Open database session"]
    EP --> DEP_USER["Depends(get_current_user)<br/>Validate JWT, return User"]

    DEP_USER --> DEP_TOKEN["Depends(oauth2_scheme)<br/>Extract Bearer token from header"]

    DEP_DB --> YIELD_DB["yield db<br/>--- endpoint runs ---<br/>db.close()"]
    DEP_TOKEN --> DECODE["Decode JWT<br/>Query user from DB"]

    subgraph LIFECYCLE ["Dependency Lifecycle"]
        direction LR
        RESOLVE["1. Resolve tree<br/>leaf-first"] --> INJECT["2. Inject into<br/>endpoint params"] --> CLEANUP["3. Run yield<br/>cleanup code"]
    end

    style EP fill:#cc5de8,stroke:#9c36b5,color:#fff
    style DEP_DB fill:#ff922b,stroke:#e8590c,color:#fff
    style DEP_USER fill:#ff922b,stroke:#e8590c,color:#fff
    style DEP_TOKEN fill:#ffd43b,stroke:#f59f00,color:#000
    style LIFECYCLE fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- Dependencies form a tree resolved bottom-up (leaves first)
- `yield` dependencies run setup code, then cleanup after the endpoint finishes
- The same dependency used twice in one request is resolved only once (cached)
- Dependency injection replaces global variables with testable, swappable components

## Sequence: Authentication + Database Request

A realistic sequence showing how a protected endpoint handles a request from token validation through database access to JSON response.

```mermaid
sequenceDiagram
    participant C as Client
    participant U as Uvicorn
    participant M as Middleware
    participant R as Router
    participant D as Dependencies
    participant E as Endpoint
    participant DB as Database

    C->>U: POST /items<br/>Authorization: Bearer <token><br/>Body: {"name": "Widget"}
    U->>M: ASGI scope + receive
    M->>R: Route lookup
    R->>D: Resolve Depends(get_db)
    D->>DB: Open session
    DB-->>D: Session ready
    R->>D: Resolve Depends(get_current_user)
    Note over D: Decode JWT, validate
    D-->>R: user=User(id=7)

    R->>E: create_item(db=session, user=user, item=Item(name="Widget"))
    Note over E: Pydantic already validated body
    E->>DB: INSERT INTO items ...
    DB-->>E: New row (id=42)
    E-->>R: ItemResponse(id=42, name="Widget")
    R-->>M: JSONResponse(status=201)
    M-->>U: Add CORS headers
    U-->>C: HTTP/1.1 201 Created<br/>{"id": 42, "name": "Widget"}

    Note over D: Cleanup: db.close()
```

**Key points:**
- Authentication happens in the dependency layer, not in your endpoint code
- Pydantic validates the request body before the endpoint function is called
- Database session cleanup runs after the response is built (yield dependency)
- The endpoint only contains business logic, everything else is handled by the framework

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|

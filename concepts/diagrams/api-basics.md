# Diagrams: API Basics

[Back to concept](../api-basics.md)

---

## REST API Architecture

A REST API sits between the client and the database. It receives HTTP requests, processes them, and returns JSON responses.

```mermaid
flowchart LR
    subgraph CLIENTS ["Clients"]
        PY["Python script<br/>requests.get()"]
        WEB["Web browser<br/>fetch()"]
        MOB["Mobile app<br/>HTTP client"]
    end

    subgraph API ["REST API Server"]
        ROUTER["Router<br/>Match URL to handler"]
        AUTH["Auth middleware<br/>Verify token/key"]
        HANDLER["Route handler<br/>Business logic"]
        SERIAL["Serializer<br/>Dict to JSON"]
    end

    subgraph DATA ["Data Layer"]
        DB[("Database<br/>PostgreSQL")]
        CACHE[("Cache<br/>Redis")]
    end

    PY -->|"HTTP request"| ROUTER
    WEB -->|"HTTP request"| ROUTER
    MOB -->|"HTTP request"| ROUTER

    ROUTER --> AUTH
    AUTH --> HANDLER
    HANDLER --> DB
    HANDLER --> CACHE
    DB --> SERIAL
    SERIAL -->|"JSON response"| PY
    SERIAL -->|"JSON response"| WEB
    SERIAL -->|"JSON response"| MOB

    style CLIENTS fill:#4a9eff,stroke:#2670c2,color:#fff
    style API fill:#cc5de8,stroke:#9c36b5,color:#fff
    style DATA fill:#51cf66,stroke:#27ae60,color:#fff
```

## CRUD to HTTP Method Mapping

REST maps the four database operations (Create, Read, Update, Delete) to HTTP methods and URL patterns.

```mermaid
flowchart TD
    subgraph CRUD ["Database Operation"]
        CREATE["CREATE<br/>Insert new row"]
        READ["READ<br/>Select rows"]
        UPDATE["UPDATE<br/>Modify row"]
        DELOP["DELETE<br/>Remove row"]
    end

    subgraph HTTP ["HTTP Method + URL"]
        POST["POST /users<br/>Body: {name, email}"]
        GET1["GET /users<br/>List all"]
        GET2["GET /users/42<br/>Get one"]
        PUT["PUT /users/42<br/>Body: {name, email}"]
        DEL["DELETE /users/42<br/>No body"]
    end

    subgraph RESPONSE ["Response"]
        R201["201 Created<br/>{id: 43, name: ...}"]
        R200L["200 OK<br/>[{id: 1}, {id: 2}, ...]"]
        R200O["200 OK<br/>{id: 42, name: ...}"]
        R200U["200 OK<br/>{id: 42, name: ...}"]
        R204["204 No Content"]
    end

    CREATE --> POST --> R201
    READ --> GET1 --> R200L
    READ --> GET2 --> R200O
    UPDATE --> PUT --> R200U
    DELOP --> DEL --> R204

    style CRUD fill:#ff922b,stroke:#e8590c,color:#fff
    style HTTP fill:#4a9eff,stroke:#2670c2,color:#fff
    style RESPONSE fill:#51cf66,stroke:#27ae60,color:#fff
```

## API Request/Response Flow

Step-by-step sequence of a typical API call from Python using the `requests` library.

```mermaid
sequenceDiagram
    participant Script as Python Script
    participant Lib as requests library
    participant API as API Server
    participant Logic as Route Handler

    Script->>Lib: requests.post(url, json=data, headers=headers)
    Note over Lib: Serialize dict to JSON<br/>Add Content-Type header

    Lib->>API: POST /users HTTP/1.1<br/>Authorization: Bearer eyJ...<br/>Content-Type: application/json<br/>{"name": "Alice", "email": "..."}

    API->>API: Validate auth token
    API->>Logic: Call create_user handler

    Note over Logic: Validate input<br/>Insert into database<br/>Build response

    Logic-->>API: {"id": 43, "name": "Alice"}
    API-->>Lib: HTTP/1.1 201 Created<br/>Content-Type: application/json

    Lib-->>Script: Response object

    Note over Script: response.status_code → 201<br/>response.json() → {"id": 43, ...}
```

## Authentication Token Flow

How bearer token authentication works: login once, then include the token with every request.

```mermaid
sequenceDiagram
    participant Client as Python Client
    participant API as API Server
    participant DB as User Database

    Note over Client: Step 1: Login to get a token

    Client->>API: POST /auth/login<br/>{"username": "alice", "password": "s3cret"}
    API->>DB: Verify credentials
    DB-->>API: User found, password matches

    Note over API: Generate JWT token<br/>Encode user ID + expiry

    API-->>Client: 200 OK<br/>{"token": "eyJhbGci...", "expires_in": 3600}

    Note over Client: Save the token

    Note over Client: Step 2: Use token for API calls

    Client->>API: GET /users/me<br/>Authorization: Bearer eyJhbGci...

    Note over API: Decode token<br/>Verify signature<br/>Check expiry

    API-->>Client: 200 OK<br/>{"id": 1, "name": "Alice", "role": "admin"}

    Note over Client: Step 3: Token expires

    Client->>API: GET /users/me<br/>Authorization: Bearer eyJhbGci...

    Note over API: Token expired!

    API-->>Client: 401 Unauthorized<br/>{"detail": "Token expired"}

    Note over Client: Must login again<br/>to get a new token
```

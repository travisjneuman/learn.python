# Diagrams: HTTP Explained

[Back to concept](../http-explained.md)

---

## HTTP Request/Response Cycle

Every HTTP interaction follows the same pattern: the client builds a request, sends it over the network, the server processes it and returns a response.

```mermaid
sequenceDiagram
    participant Client as Python Client
    participant DNS as DNS Server
    participant Server as Web Server
    participant DB as Database

    Client->>DNS: Resolve api.example.com
    DNS-->>Client: 93.184.216.34

    Client->>Server: GET /users/42 HTTP/1.1<br/>Host: api.example.com<br/>Accept: application/json
    Note over Server: Parse request<br/>Route to handler

    Server->>DB: SELECT * FROM users WHERE id=42
    DB-->>Server: Row data

    Note over Server: Serialize to JSON
    Server-->>Client: HTTP/1.1 200 OK<br/>Content-Type: application/json<br/>{"id": 42, "name": "Alice"}

    Note over Client: response.json()<br/>Parse JSON to dict
```

## HTTP Methods Comparison

Each HTTP method has a specific purpose. The combination of method + URL tells the server exactly what you want to do.

```mermaid
flowchart LR
    subgraph SAFE ["Safe Methods (read-only)"]
        GET["GET<br/>Read data<br/>No body sent"]
    end

    subgraph UNSAFE ["Unsafe Methods (modify data)"]
        POST["POST<br/>Create new<br/>Body: new data"]
        PUT["PUT<br/>Replace entire<br/>Body: full object"]
        PATCH["PATCH<br/>Update part<br/>Body: partial data"]
        DELETE["DELETE<br/>Remove<br/>No body needed"]
    end

    subgraph IDEM ["Idempotent?"]
        YES["Same result if<br/>called 1x or 100x:<br/>GET, PUT, DELETE"]
        NO["May create duplicates<br/>if called twice:<br/>POST"]
    end

    SAFE --> IDEM
    UNSAFE --> IDEM

    style SAFE fill:#51cf66,stroke:#27ae60,color:#fff
    style UNSAFE fill:#ff922b,stroke:#e8590c,color:#fff
    style YES fill:#4a9eff,stroke:#2670c2,color:#fff
    style NO fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

## Status Code Categories

The first digit of the status code tells you the category of response.

```mermaid
flowchart TD
    REQ["Server receives request"] --> CODE{"Status code?"}

    CODE -->|"2xx"| SUCCESS["SUCCESS"]
    CODE -->|"3xx"| REDIRECT["REDIRECT"]
    CODE -->|"4xx"| CLIENT_ERR["CLIENT ERROR"]
    CODE -->|"5xx"| SERVER_ERR["SERVER ERROR"]

    SUCCESS --> S200["200 OK — Request worked"]
    SUCCESS --> S201["201 Created — New resource made"]
    SUCCESS --> S204["204 No Content — Done, nothing to return"]

    REDIRECT --> R301["301 Moved — Use new URL forever"]
    REDIRECT --> R304["304 Not Modified — Use your cache"]

    CLIENT_ERR --> C400["400 Bad Request — Malformed request"]
    CLIENT_ERR --> C401["401 Unauthorized — Login required"]
    CLIENT_ERR --> C403["403 Forbidden — No permission"]
    CLIENT_ERR --> C404["404 Not Found — Resource missing"]
    CLIENT_ERR --> C429["429 Too Many Requests — Rate limited"]

    SERVER_ERR --> E500["500 Internal Error — Server broke"]
    SERVER_ERR --> E503["503 Unavailable — Server overloaded"]

    style SUCCESS fill:#51cf66,stroke:#27ae60,color:#fff
    style REDIRECT fill:#4a9eff,stroke:#2670c2,color:#fff
    style CLIENT_ERR fill:#ffd43b,stroke:#f59f00,color:#000
    style SERVER_ERR fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

## Full Request Lifecycle in Python

What happens step by step when you call `requests.get()`.

```mermaid
flowchart TD
    A["response = requests.get(url, timeout=10)"] --> B["Build HTTP request<br/>Method + URL + Headers"]
    B --> C["Open TCP connection<br/>to server"]
    C --> D["Send request bytes<br/>over the network"]
    D --> E{"Server responds<br/>within timeout?"}
    E -->|"Yes"| F["Read response bytes"]
    E -->|"No"| TIMEOUT["Raise Timeout error"]
    F --> G["Parse status code<br/>and headers"]
    G --> H{"Check status"}
    H -->|"2xx"| SUCCESS["response.json()<br/>Parse body as JSON"]
    H -->|"4xx"| CLIENT["Client error<br/>raise_for_status() raises HTTPError"]
    H -->|"5xx"| SERVER["Server error<br/>raise_for_status() raises HTTPError"]

    SUCCESS --> DONE["Use the data"]
    CLIENT --> RETRY{"Retry?"}
    SERVER --> RETRY
    TIMEOUT --> RETRY
    RETRY -->|"Yes"| A
    RETRY -->|"No"| FAIL["Handle error gracefully"]

    style A fill:#cc5de8,stroke:#9c36b5,color:#fff
    style SUCCESS fill:#51cf66,stroke:#27ae60,color:#fff
    style DONE fill:#51cf66,stroke:#27ae60,color:#fff
    style TIMEOUT fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style CLIENT fill:#ffd43b,stroke:#f59f00,color:#000
    style SERVER fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

# Diagrams: Security Basics

[Back to concept](../security-basics.md)

---

## OWASP Top Risks for Python Developers

The most common web security vulnerabilities, ranked by how often they appear in Python projects.

```mermaid
flowchart TD
    subgraph INJECTION ["Injection Attacks"]
        SQL["SQL Injection<br/>User input in queries<br/>Fix: parameterized queries"]
        CMD["Command Injection<br/>User input in shell calls<br/>Fix: subprocess with list args"]
    end

    subgraph XSS_CSRF ["Cross-Site Attacks"]
        XSS["XSS<br/>Script in user content<br/>Fix: auto-escaping templates"]
        CSRF["CSRF<br/>Forged form submission<br/>Fix: CSRF tokens"]
    end

    subgraph AUTH_ISSUES ["Authentication Flaws"]
        WEAK["Weak Passwords<br/>No complexity rules<br/>Fix: bcrypt/argon2 hashing"]
        SESSION["Session Hijacking<br/>Stolen cookies<br/>Fix: HttpOnly, Secure flags"]
    end

    subgraph DATA_EXPOSURE ["Data Exposure"]
        SECRETS["Hardcoded Secrets<br/>API keys in source code<br/>Fix: environment variables"]
        PATH["Path Traversal<br/>../../etc/passwd<br/>Fix: resolve() + is_relative_to()"]
        LOGGING["Sensitive Data in Logs<br/>Passwords in log output<br/>Fix: never log secrets"]
    end

    subgraph SUPPLY ["Supply Chain"]
        DEPS["Vulnerable Dependencies<br/>Outdated packages<br/>Fix: pip audit regularly"]
    end

    style INJECTION fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style XSS_CSRF fill:#ff922b,stroke:#e8590c,color:#fff
    style AUTH_ISSUES fill:#ffd43b,stroke:#f59f00,color:#000
    style DATA_EXPOSURE fill:#4a9eff,stroke:#2670c2,color:#fff
    style SUPPLY fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## Input Sanitization Flow

Every piece of user input must be validated before it touches your application logic, database, or output.

```mermaid
flowchart TD
    INPUT["Raw User Input<br/>(form, URL, API body, file)"] --> VALIDATE{"Step 1: Validate<br/>Correct type and format?"}

    VALIDATE -->|"Invalid"| REJECT["Reject with clear error<br/>400 Bad Request"]
    VALIDATE -->|"Valid"| SANITIZE["Step 2: Sanitize<br/>Strip dangerous characters"]

    SANITIZE --> CONTEXT{"Where is this<br/>data going?"}

    CONTEXT -->|"Database"| DB_SAFE["Use parameterized queries<br/>cursor.execute(sql, (value,))"]
    CONTEXT -->|"HTML output"| HTML_SAFE["Auto-escape template<br/>Jinja2 escapes by default"]
    CONTEXT -->|"File path"| PATH_SAFE["Resolve and check<br/>path.is_relative_to(base)"]
    CONTEXT -->|"Shell command"| CMD_SAFE["Use subprocess with list<br/>Never pass raw strings"]
    CONTEXT -->|"JSON response"| JSON_SAFE["Serialize with json.dumps<br/>Auto-escapes special chars"]

    DB_SAFE --> SAFE["Data is safe"]
    HTML_SAFE --> SAFE
    PATH_SAFE --> SAFE
    CMD_SAFE --> SAFE
    JSON_SAFE --> SAFE

    style INPUT fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style REJECT fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style VALIDATE fill:#ffd43b,stroke:#f59f00,color:#000
    style SANITIZE fill:#ff922b,stroke:#e8590c,color:#fff
    style SAFE fill:#51cf66,stroke:#27ae60,color:#fff
```

## Authentication vs Authorization

Authentication proves WHO you are. Authorization determines WHAT you can do. They are separate steps.

```mermaid
sequenceDiagram
    participant User as User
    participant App as Application
    participant AuthN as Authentication<br/>(Who are you?)
    participant AuthZ as Authorization<br/>(What can you do?)
    participant Resource as Protected Resource

    User->>App: POST /login<br/>username + password

    App->>AuthN: Verify credentials
    Note over AuthN: Check password hash<br/>with bcrypt.checkpw()
    AuthN-->>App: Identity confirmed: alice (role: editor)

    Note over App: Create session/JWT token<br/>Include user ID and role

    App-->>User: 200 OK + token

    User->>App: GET /admin/users<br/>Authorization: Bearer token

    App->>AuthN: Verify token is valid
    AuthN-->>App: Token valid, user = alice

    App->>AuthZ: Can alice access /admin/users?
    Note over AuthZ: Check role: editor<br/>Required: admin

    AuthZ-->>App: DENIED

    App-->>User: 403 Forbidden<br/>You are logged in (authenticated)<br/>but not allowed (not authorized)

    User->>App: GET /articles<br/>Authorization: Bearer token

    App->>AuthN: Verify token
    AuthN-->>App: Token valid, user = alice

    App->>AuthZ: Can alice access /articles?
    Note over AuthZ: Check role: editor<br/>Required: editor or admin

    AuthZ-->>App: ALLOWED

    App->>Resource: Fetch articles
    Resource-->>App: Article data
    App-->>User: 200 OK + articles
```

## Secrets Management Decision Tree

Where and how to store secrets depends on your environment.

```mermaid
flowchart TD
    START["Where to store secrets?"] --> ENV{"What environment?"}

    ENV -->|"Local development"| DOTENV[".env file<br/>+ python-dotenv<br/>+ add to .gitignore"]
    ENV -->|"CI/CD pipeline"| CI_SECRETS["Pipeline secrets<br/>GitHub Secrets<br/>GitLab CI Variables"]
    ENV -->|"Production server"| PROD{"Scale?"}

    PROD -->|"Small/simple"| ENV_VARS["Environment variables<br/>Set in hosting platform<br/>(Railway, Heroku, etc.)"]
    PROD -->|"Large/enterprise"| VAULT["Secrets manager<br/>AWS Secrets Manager<br/>HashiCorp Vault"]

    subgraph NEVER ["NEVER DO THIS"]
        N1["Hardcode in source code"]
        N2["Commit .env to git"]
        N3["Log secrets to console"]
        N4["Send secrets in URL params"]
    end

    subgraph ALWAYS ["ALWAYS DO THIS"]
        A1["Add .env to .gitignore FIRST"]
        A2["Rotate exposed credentials"]
        A3["Use read-only tokens when possible"]
        A4["Audit access regularly"]
    end

    style DOTENV fill:#51cf66,stroke:#27ae60,color:#fff
    style CI_SECRETS fill:#4a9eff,stroke:#2670c2,color:#fff
    style ENV_VARS fill:#ff922b,stroke:#e8590c,color:#fff
    style VAULT fill:#cc5de8,stroke:#9c36b5,color:#fff
    style NEVER fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style ALWAYS fill:#51cf66,stroke:#27ae60,color:#fff
```

# SQLAlchemy ORM Mapping — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams show how SQLAlchemy connects Python classes to database tables, how the Engine/Session/Model stack works, and how relationships and queries translate to SQL.

## Engine, Session, and Model Stack

SQLAlchemy has three main layers. The Engine manages database connections, the Session tracks changes, and Models define your table structure in Python.

```mermaid
flowchart TD
    subgraph APP ["Your Application Code"]
        CODE["user = User(name='Alice')<br/>session.add(user)<br/>session.commit()"]
    end

    subgraph SESSION_LAYER ["Session Layer"]
        SESSION["Session<br/>Tracks new, modified, deleted objects<br/>Unit of Work pattern"]
        IDENTITY["Identity Map<br/>Cache: one Python object per DB row<br/>session.get(User, 42) returns same object"]
    end

    subgraph ENGINE_LAYER ["Engine Layer"]
        ENGINE["Engine<br/>create_engine('postgresql://...')"]
        POOL["Connection Pool<br/>Reuses DB connections<br/>(pool_size=5 default)"]
    end

    subgraph DB ["Database"]
        PG["PostgreSQL / SQLite<br/>Tables, indexes, constraints"]
    end

    CODE --> SESSION
    SESSION --> IDENTITY
    SESSION -->|"flush: generate SQL"| ENGINE
    ENGINE --> POOL
    POOL -->|"SQL over wire"| PG

    style APP fill:#cc5de8,stroke:#9c36b5,color:#fff
    style SESSION_LAYER fill:#ff922b,stroke:#e8590c,color:#fff
    style ENGINE_LAYER fill:#4a9eff,stroke:#2670c2,color:#fff
    style DB fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- The Engine is created once at app startup and shared across the application
- The Session is short-lived: create one per request or unit of work, then close it
- The Identity Map ensures you get the same Python object for the same database row within a session
- `commit()` triggers `flush()` which converts tracked changes into SQL statements

## Model to Table Mapping

SQLAlchemy's declarative system maps Python classes to database tables. Fields become columns, and relationships define how tables connect.

```mermaid
flowchart LR
    subgraph MODELS ["Python Models (declarative)"]
        USER["class User(Base):<br/>    __tablename__ = 'users'<br/>    id = Column(Integer, primary_key=True)<br/>    name = Column(String(100))<br/>    posts = relationship('Post', back_populates='author')"]
        POST["class Post(Base):<br/>    __tablename__ = 'posts'<br/>    id = Column(Integer, primary_key=True)<br/>    title = Column(String(200))<br/>    author_id = Column(ForeignKey('users.id'))<br/>    author = relationship('User', back_populates='posts')"]
    end

    subgraph TABLES ["Database Tables"]
        T_USER["users<br/>id INTEGER PRIMARY KEY<br/>name VARCHAR(100)"]
        T_POST["posts<br/>id INTEGER PRIMARY KEY<br/>title VARCHAR(200)<br/>author_id INTEGER REFERENCES users(id)"]
    end

    USER -->|"Base.metadata.create_all()"| T_USER
    POST --> T_POST
    T_POST ---|"FOREIGN KEY"| T_USER

    style MODELS fill:#51cf66,stroke:#27ae60,color:#fff
    style TABLES fill:#4a9eff,stroke:#2670c2,color:#fff
```

**Key points:**
- `relationship()` creates a Python-level link; `ForeignKey` creates the database-level constraint
- `back_populates` makes the relationship bidirectional: `user.posts` and `post.author`
- `Base.metadata.create_all(engine)` generates all tables (use Alembic for migrations in real projects)
- Column types like `String(100)` map to `VARCHAR(100)` in the database

## Query Execution: Python to SQL

When you query with SQLAlchemy, it builds a SQL expression tree, compiles it to the database dialect, executes it, and maps the results back to Python objects.

```mermaid
flowchart TD
    QUERY["Python Query<br/>session.query(User).filter(User.name == 'Alice').first()"]
    QUERY --> BUILD["Build Expression Tree<br/>SELECT ... FROM users WHERE name = :name_1"]
    BUILD --> COMPILE["Compile to Dialect<br/>PostgreSQL: uses $1 params<br/>SQLite: uses ? params"]
    COMPILE --> EXECUTE["Execute via Engine<br/>Send SQL + bound parameters"]
    EXECUTE --> FETCH["Fetch Rows<br/>Raw tuples from database"]
    FETCH --> MAP["Map to Objects<br/>Row -> User(id=1, name='Alice')"]
    MAP --> CACHE["Store in Identity Map<br/>Subsequent queries return same object"]
    CACHE --> RESULT["Return to Your Code<br/>user.name  # 'Alice'"]

    style QUERY fill:#cc5de8,stroke:#9c36b5,color:#fff
    style BUILD fill:#ffd43b,stroke:#f59f00,color:#000
    style COMPILE fill:#ff922b,stroke:#e8590c,color:#fff
    style EXECUTE fill:#4a9eff,stroke:#2670c2,color:#fff
    style MAP fill:#51cf66,stroke:#27ae60,color:#fff
    style RESULT fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- SQLAlchemy uses bound parameters (`:name_1`) to prevent SQL injection automatically
- The dialect compiler adapts SQL syntax to your specific database engine
- Results are mapped back to Python objects with full attribute access
- The Identity Map means `session.query(User).get(1)` returns the exact same object if already loaded

## Alembic Migration Workflow

Alembic manages database schema changes over time. It generates migration scripts from model changes and applies them in order.

```mermaid
flowchart LR
    subgraph DEV ["Development"]
        CHANGE["Change Model<br/>Add Column, new Table"]
        CHANGE -->|"alembic revision --autogenerate"| SCRIPT["Migration Script<br/>def upgrade():<br/>    op.add_column(...)<br/>def downgrade():<br/>    op.drop_column(...)"]
    end

    subgraph APPLY ["Apply Migrations"]
        SCRIPT -->|"alembic upgrade head"| DB_NEW["Database Updated<br/>Schema matches models"]
        DB_NEW -->|"alembic downgrade -1"| DB_OLD["Previous Schema<br/>Rolled back one step"]
    end

    subgraph TRACK ["Version Tracking"]
        VER["alembic_version table<br/>Stores current revision ID"]
        CHAIN["Revision chain<br/>abc123 -> def456 -> ghi789"]
    end

    DB_NEW --> VER
    SCRIPT --> CHAIN

    style DEV fill:#ffd43b,stroke:#f59f00,color:#000
    style APPLY fill:#51cf66,stroke:#27ae60,color:#fff
    style TRACK fill:#4a9eff,stroke:#2670c2,color:#fff
```

**Key points:**
- `--autogenerate` compares your models to the database and generates the migration diff
- Every migration has `upgrade()` and `downgrade()` so you can roll back safely
- Migrations are chained: each knows its parent revision, ensuring correct ordering
- Always review auto-generated migrations before applying them (they can miss renames or data changes)

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|

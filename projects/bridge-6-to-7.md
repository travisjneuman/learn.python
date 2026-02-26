# Bridge Exercise: Level 6 to Level 7

You have completed Level 6. You can work with SQL databases (SQLite), use decorators, and make basic API calls. Level 7 introduces **API client design**, **caching**, **data transformation between formats**, and **more sophisticated error handling**. This bridge exercise connects database queries with API integration.

---

## What Changes in Level 7

In Level 6, you stored data in SQLite and fetched data from simple APIs. In Level 7, you will:
- Build **reusable API clients** with proper error handling and retries
- Implement **caching** so you do not hit the same API endpoint repeatedly
- **Transform data** between API responses (JSON) and database tables
- Handle **rate limiting** and **pagination** from real-world APIs

---

## Part 1: A Cached API-to-Database Pipeline

### Exercise

Build a system that fetches data from an API, caches it locally, and stores it in a database.

Create `bridge_6_to_7.py`:

```python
import json
import sqlite3
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class SimpleCache:
    """File-based cache with expiration.

    Stores API responses as JSON files so repeated calls
    do not hit the network.
    """

    def __init__(self, cache_dir, ttl_seconds=300):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl_seconds

    def _key_path(self, key):
        safe_key = key.replace("/", "_").replace(":", "_")
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key):
        """Return cached value if it exists and is not expired."""
        path = self._key_path(key)
        if not path.exists():
            return None

        data = json.loads(path.read_text())
        cached_at = data.get("_cached_at", 0)
        if time.time() - cached_at > self.ttl:
            logger.info("Cache expired for %s", key)
            path.unlink()
            return None

        logger.info("Cache hit for %s", key)
        return data["value"]

    def set(self, key, value):
        """Store a value in the cache."""
        path = self._key_path(key)
        data = {"value": value, "_cached_at": time.time()}
        path.write_text(json.dumps(data, indent=2))
        logger.info("Cached %s", key)
```

**New concepts introduced:**
- **Caching**: save expensive results (API calls) so you do not repeat them.
- **TTL (Time To Live)**: cached data expires after a set time.
- File-based cache — simple, no external dependencies.

---

## Part 2: Database Storage Layer

### Exercise

Add functions that store and query API data in SQLite.

Add to `bridge_6_to_7.py`:

```python
def create_database(db_path):
    """Create the database and tables."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # access columns by name
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            fetched_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def store_users(conn, users):
    """Insert or update users in the database.

    Uses INSERT OR REPLACE to handle duplicates.
    """
    now = datetime.now().isoformat()
    for user in users:
        conn.execute(
            "INSERT OR REPLACE INTO users (id, name, email, fetched_at) VALUES (?, ?, ?, ?)",
            (user["id"], user["name"], user.get("email"), now),
        )
    conn.commit()
    logger.info("Stored %d users", len(users))


def query_users(conn, name_contains=None):
    """Query users from the database.

    Args:
        name_contains: filter by name (case-insensitive LIKE match)
    """
    if name_contains:
        cursor = conn.execute(
            "SELECT * FROM users WHERE name LIKE ?",
            (f"%{name_contains}%",),
        )
    else:
        cursor = conn.execute("SELECT * FROM users")

    return [dict(row) for row in cursor.fetchall()]
```

**New concepts introduced:**
- `conn.row_factory = sqlite3.Row` — access columns by name instead of index.
- `INSERT OR REPLACE` — upsert pattern (insert or update if exists).
- Parameterized queries with `?` — prevents SQL injection.
- Converting database rows to dicts for easy use.

---

## Part 3: Putting It Together

### Exercise

Add a function that ties the cache and database together.

Add to `bridge_6_to_7.py`:

```python
def sync_users(api_data, cache, conn):
    """Sync user data: check cache, store in database.

    This simulates fetching from an API (using api_data as the response)
    with caching and database storage.

    In real code, api_data would come from requests.get().json().
    """
    cache_key = "users_list"

    # Check cache first
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info("Using cached data (%d users)", len(cached))
        return query_users(conn)

    # "Fetch" from API (in real code: requests.get(url).json())
    logger.info("Fetching fresh data (%d users)", len(api_data))

    # Cache the response
    cache.set(cache_key, api_data)

    # Store in database
    store_users(conn, api_data)

    return query_users(conn)
```

---

## Part 4: Tests

Create `test_bridge_6_to_7.py`:

```python
import pytest
from bridge_6_to_7 import SimpleCache, create_database, store_users, query_users, sync_users


@pytest.fixture
def cache(tmp_path):
    return SimpleCache(tmp_path / "cache", ttl_seconds=60)


@pytest.fixture
def db(tmp_path):
    return create_database(str(tmp_path / "test.db"))


@pytest.fixture
def sample_users():
    return [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie Brown"},
    ]


def test_cache_miss(cache):
    assert cache.get("nonexistent") is None


def test_cache_hit(cache):
    cache.set("key", {"data": 42})
    assert cache.get("key") == {"data": 42}


def test_cache_expiry(cache, tmp_path):
    expired_cache = SimpleCache(tmp_path / "expired", ttl_seconds=0)
    expired_cache.set("key", "value")
    assert expired_cache.get("key") is None  # already expired


def test_store_and_query(db, sample_users):
    store_users(db, sample_users)
    result = query_users(db)
    assert len(result) == 3


def test_query_filter(db, sample_users):
    store_users(db, sample_users)
    result = query_users(db, name_contains="alice")
    assert len(result) == 1
    assert result[0]["name"] == "Alice Johnson"


def test_sync_caches(db, cache, sample_users):
    # First sync — stores in cache and db
    result1 = sync_users(sample_users, cache, db)
    assert len(result1) == 3

    # Second sync — should use cache
    result2 = sync_users([], cache, db)  # empty data, but cache has data
    assert len(result2) == 3
```

Run: `pytest test_bridge_6_to_7.py -v`

---

## You Are Ready

If you can build a file-based cache, store and query data in SQLite, and combine API responses with database storage, you are ready for Level 7.

---

| [Level 6 Projects](level-6/README.md) | [Home](../README.md) | [Level 7 Projects](level-7/README.md) |
|:---|:---:|---:|

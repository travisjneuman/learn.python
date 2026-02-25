# HTTP Explained

HTTP (HyperText Transfer Protocol) is how browsers and apps talk to servers. Every time you visit a website or call an API, you're using HTTP.

## The request-response cycle

1. Your code sends a **request** to a server.
2. The server processes it and sends back a **response**.

```
Client                          Server
  |                               |
  |--- GET /posts/1 ------------>|
  |                               | (looks up post #1)
  |<-- 200 OK + JSON data -------|
  |                               |
```

## HTTP methods

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Read data | Get a list of users |
| `POST` | Create new data | Create a new user |
| `PUT` | Replace data entirely | Update all user fields |
| `PATCH` | Update part of data | Change just the email |
| `DELETE` | Remove data | Delete a user |

## Status codes

The server tells you what happened with a number:

| Range | Meaning | Common codes |
|-------|---------|-------------|
| **2xx** | Success | 200 OK, 201 Created, 204 No Content |
| **3xx** | Redirect | 301 Moved Permanently, 304 Not Modified |
| **4xx** | Client error (your fault) | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| **5xx** | Server error (their fault) | 500 Internal Server Error, 503 Service Unavailable |

## Headers

Extra information attached to requests and responses:

```python
import requests

# Request headers — tell the server about your request.
response = requests.get(
    "https://api.example.com/data",
    headers={
        "Authorization": "Bearer your-token-here",
        "Accept": "application/json",
        "User-Agent": "my-python-app/1.0",
    }
)

# Response headers — the server tells you about the response.
print(response.headers["Content-Type"])    # "application/json"
print(response.headers["Content-Length"])   # "1234"
```

## Request body

POST and PUT requests often send data in the body:

```python
import requests

# Sending JSON data.
response = requests.post(
    "https://api.example.com/users",
    json={"name": "Alice", "email": "alice@example.com"},
)
```

## Query parameters

Extra data in the URL after `?`:

```
https://api.example.com/users?page=2&limit=10&sort=name
```

```python
response = requests.get(
    "https://api.example.com/users",
    params={"page": 2, "limit": 10, "sort": "name"},
)
```

## JSON — the language of APIs

Most APIs send and receive JSON (JavaScript Object Notation):

```json
{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": true,
    "tags": ["admin", "user"]
}
```

Python dictionaries map directly to JSON:

```python
response = requests.get("https://api.example.com/users/1")
data = response.json()    # Parse JSON → Python dict
print(data["name"])        # "Alice"
```

## Common mistakes

**Not checking status codes:**
```python
# Bad — assumes success.
data = requests.get(url).json()

# Good — check first.
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error: {response.status_code}")
```

**Not setting timeouts:**
```python
# Bad — waits forever if the server is down.
requests.get(url)

# Good — give up after 10 seconds.
requests.get(url, timeout=10)
```

## Related exercises

- [Module 03 — REST APIs](../projects/modules/03-rest-apis/) (consuming APIs)
- [Module 04 — FastAPI](../projects/modules/04-fastapi-web/) (building APIs)

---

## Practice This

- [Level 3 / 14 Service Simulator](../projects/level-3/14-service-simulator/README.md)
- [Level 4 / 13 Reconciliation Reporter](../projects/level-4/13-reconciliation-reporter/README.md)
- [Level 5 / 10 Api Polling Simulator](../projects/level-5/10-api-polling-simulator/README.md)
- [Level 6 / 12 Etl Health Dashboard Feed](../projects/level-6/12-etl-health-dashboard-feed/README.md)
- [Level 7 / 04 Source Field Mapper](../projects/level-7/04-source-field-mapper/README.md)
- [Level 8 / 02 Query Cache Layer](../projects/level-8/02-query-cache-layer/README.md)
- [Level 8 / 03 Pagination Stress Lab](../projects/level-8/03-pagination-stress-lab/README.md)
- [Level 8 / 04 Filter State Manager](../projects/level-8/04-filter-state-manager/README.md)
- [Level 8 / 05 Export Governance Check](../projects/level-8/05-export-governance-check/README.md)
- [Level 8 / 06 Response Time Profiler](../projects/level-8/06-response-time-profiler/README.md)

**Quick check:** [Take the quiz](quizzes/http-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

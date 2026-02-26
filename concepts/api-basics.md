# API Basics

An **API** (Application Programming Interface) is a way for programs to talk to each other. When people say "API" in web development, they usually mean a web API — a server that accepts HTTP requests and returns data (usually JSON).

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/api-basics.md) | [Quiz](quizzes/api-basics-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/api-basics.md) |

<!-- modality-hub-end -->

## Visualize It

See how Python works with JSON data, the format APIs use to communicate:
[Open in Python Tutor](https://pythontutor.com/render.html#code=import%20json%0A%0Apost%20%3D%20%7B%0A%20%20%20%20%22title%22%3A%20%22My%20Post%22%2C%0A%20%20%20%20%22tags%22%3A%20%5B%22python%22%2C%20%22api%22%5D%0A%7D%0Ajson_str%20%3D%20json.dumps%28post%29%0Aprint%28json_str%29%0Aparsed%20%3D%20json.loads%28json_str%29%0Aprint%28parsed%5B%22tags%22%5D%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## How APIs work

```
Your Python script          The API server
       |                          |
       |-- GET /posts ----------->|
       |                          | (looks up posts in database)
       |<-- 200 OK + JSON --------|
       |                          |
```

Your script is the **client**. The API is the **server**. The conversation happens over HTTP.

## REST — the most common API style

REST (Representational State Transfer) is a set of conventions for designing APIs:

| Action | HTTP Method | URL | Example |
|--------|------------|-----|---------|
| List all | GET | `/users` | Get all users |
| Get one | GET | `/users/42` | Get user #42 |
| Create | POST | `/users` | Create a new user |
| Update | PUT | `/users/42` | Replace user #42 |
| Delete | DELETE | `/users/42` | Delete user #42 |

The URL identifies the **resource** (what you're working with). The HTTP method identifies the **action** (what you're doing to it).

## Making API calls with Python

```python
import requests

# GET — read data.
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
post = response.json()
print(post["title"])

# POST — create data.
new_post = {"title": "My Post", "body": "Content here", "userId": 1}
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post,
)
print(response.status_code)    # 201 Created
```

## Building APIs with Python

FastAPI lets you create APIs:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}
```

Run with `uvicorn app:app` and visit `http://localhost:8000/hello/Alice`.

## Authentication

Most APIs require you to prove who you are:

**API Key** — a secret string you include in the request:
```python
response = requests.get(url, headers={"X-API-Key": "your-key-here"})
```

**Bearer Token (JWT)** — a token you get by logging in:
```python
response = requests.get(url, headers={"Authorization": "Bearer eyJ..."})
```

## Common public APIs for practice

| API | URL | What it provides |
|-----|-----|-----------------|
| JSONPlaceholder | jsonplaceholder.typicode.com | Fake posts, users, comments |
| Open Meteo | open-meteo.com | Weather data |
| PokéAPI | pokeapi.co | Pokémon data |
| REST Countries | restcountries.com | Country information |

These are free, require no API key, and are safe to practice with.

## Common mistakes

**Not handling errors:**
```python
# Bad — crashes if the API is down.
data = requests.get(url).json()

# Good — check the response first.
response = requests.get(url, timeout=10)
response.raise_for_status()    # Raises an exception for 4xx/5xx
data = response.json()
```

**Hardcoding API URLs:**
```python
# Bad
requests.get("https://api.example.com/v2/users")

# Good — use a variable or config.
BASE_URL = "https://api.example.com/v2"
requests.get(f"{BASE_URL}/users")
```

## Practice

- [Module 03 REST APIs](../projects/modules/03-rest-apis/)
- [Module 04 FastAPI Web Apps](../projects/modules/04-fastapi-web/)
- [HTTP Explained](./http-explained.md)
- [Module: Elite Track / 04 Secure Auth Gateway](../projects/elite-track/04-secure-auth-gateway/README.md)
- [Level 1 / 09 Json Settings Loader](../projects/level-1/09-json-settings-loader/README.md)
- [Level 10 / 01 Enterprise Python Blueprint](../projects/level-10/01-enterprise-python-blueprint/README.md)
- [Level 10 / 02 Autonomous Run Orchestrator](../projects/level-10/02-autonomous-run-orchestrator/README.md)
- [Level 10 / 03 Policy As Code Validator](../projects/level-10/03-policy-as-code-validator/README.md)
- [Level 10 / 04 Multi Tenant Data Guard](../projects/level-10/04-multi-tenant-data-guard/README.md)
- [Level 10 / 05 Compliance Evidence Builder](../projects/level-10/05-compliance-evidence-builder/README.md)
- [Level 10 / 06 Resilience Chaos Workbench](../projects/level-10/06-resilience-chaos-workbench/README.md)
- [Level 10 / 07 High Risk Change Gate](../projects/level-10/07-high-risk-change-gate/README.md)
- [Level 10 / 08 Zero Downtime Migration Lab](../projects/level-10/08-zero-downtime-migration-lab/README.md)

**Quick check:** [Take the quiz](quizzes/api-basics-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](http-explained.md) | [Home](../README.md) | [Next →](async-explained.md) |
|:---|:---:|---:|

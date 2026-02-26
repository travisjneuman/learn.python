# Security Basics

Security is about protecting your application and its users from attacks. Even a small Python script can be vulnerable if it handles user input, connects to a database, or stores passwords. This page covers the most common attacks and how to prevent them.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/security-basics-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Why This Matters

A single security vulnerability can expose every user's data, destroy trust, and create legal liability. The good news: most attacks exploit a small set of well-known mistakes. Learn these patterns and you will avoid the vast majority of real-world vulnerabilities.

## The OWASP Top 10 (Python edition)

OWASP (Open Worldwide Application Security Project) maintains a list of the most critical web security risks. Here are the ones most relevant to Python developers:

### 1. SQL Injection

An attacker puts SQL code into user input to manipulate your database.

```python
# VULNERABLE — NEVER do this:
username = input("Username: ")
query = "SELECT * FROM users WHERE name = '" + username + "'"
cursor.execute(query)
# If user types: ' OR '1'='1
# The query becomes: SELECT * FROM users WHERE name = '' OR '1'='1'
# This returns ALL users!

# SAFE — use parameterized queries:
cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
```

The `?` placeholder (or `%s` in some libraries) tells the database to treat the value as data, not as SQL code. This is the single most important security rule for database code.

**With SQLAlchemy:**
```python
# SAFE — ORM handles parameterization:
user = session.query(User).filter(User.name == username).first()

# SAFE — text() with bound parameters:
from sqlalchemy import text
result = session.execute(text("SELECT * FROM users WHERE name = :name"), {"name": username})
```

### 2. Cross-Site Scripting (XSS)

An attacker injects JavaScript into your web page through user input. If user input is rendered as raw HTML, the browser will execute any script tags the attacker includes.

**Protection:**
- Use auto-escaping templates (Jinja2, used by Flask/FastAPI, auto-escapes by default)
- Never render raw user content in HTML without escaping
- Validate and sanitize input on the server side

### 3. Cross-Site Request Forgery (CSRF)

An attacker tricks a logged-in user into making a request they did not intend. The attacker hosts a form that submits to your site — the browser automatically includes the user's cookies.

**Protection:** Use CSRF tokens in every form. Django includes CSRF protection by default. FastAPI with forms should use a CSRF middleware or token pattern.

### 4. Broken Authentication

Weak passwords, missing rate limiting, and improper session handling.

```python
# NEVER store passwords in plain text:
# BAD:
db.save(username=user, password=password)

# GOOD — hash with bcrypt:
import bcrypt

# When creating a user:
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
db.save(username=user, password_hash=hashed)

# When checking a password:
if bcrypt.checkpw(password.encode(), stored_hash):
    print("Login successful")
```

## Secrets management

Never put secrets (API keys, passwords, database URLs) directly in your code.

```python
# BAD — hardcoded secrets in source code (never do this)

# GOOD — use environment variables:
import os

API_KEY = os.environ["API_KEY"]
DB_URL = os.environ["DATABASE_URL"]
```

Use a `.env` file for local development (never commit it):

```bash
# .env file (add to .gitignore!):
API_KEY=your-key-here
DATABASE_URL=postgresql://user:pass@localhost/mydb
```

```python
# Load .env with python-dotenv:
from dotenv import load_dotenv
import os

load_dotenv()    # Reads .env into environment variables
api_key = os.environ["API_KEY"]
```

Your `.gitignore` must include:
```gitignore
.env
*.pem
*.key
credentials.json
```

## Input validation

Never trust user input. Validate everything at the boundary.

```python
# BAD — trusting user input:
age = int(input("Age: "))    # Crashes if user types "abc"

# GOOD — validate:
age_str = input("Age: ")
if not age_str.isdigit() or not (0 <= int(age_str) <= 150):
    print("Please enter a valid age")
else:
    age = int(age_str)
```

**With Pydantic (used by FastAPI):**
```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

# Pydantic validates automatically:
user = UserCreate(name="Alice", email="alice@example.com", age=30)    # OK
user = UserCreate(name="", email="not-an-email", age=-5)               # ValidationError
```

## Dependency auditing

Third-party packages can have vulnerabilities. Check them regularly.

```bash
# Check for known vulnerabilities in your dependencies:
pip audit

# With uv:
uv pip audit

# Keep dependencies updated:
pip install --upgrade requests

# Pin exact versions in production:
# requirements.txt:
requests==2.31.0
flask==3.0.2
```

## Path traversal

An attacker manipulates file paths to access files outside the intended directory.

```python
# VULNERABLE:
filename = input("Which file? ")
# Opening user-controlled paths without validation is dangerous!
# If filename = "../../etc/passwd" — reads system files!

# SAFE — validate the path:
from pathlib import Path

base_dir = Path("/app/uploads").resolve()
requested = (base_dir / filename).resolve()

if not requested.is_relative_to(base_dir):
    raise ValueError("Access denied: path traversal detected")

with open(requested) as f:
    print(f.read())
```

## Dangerous built-in functions

Python has built-in functions that can execute arbitrary code. Never use them with untrusted input:

- **`ast.literal_eval()`** is the safe alternative when you need to parse simple Python literals (strings, numbers, lists, dicts) from text input
- Always use `ast.literal_eval()` instead of alternatives that execute arbitrary code
- For math expressions, use a dedicated library like `simpleeval`

## Security checklist for Python projects

- [ ] Use parameterized queries for ALL database operations
- [ ] Hash passwords with bcrypt or argon2 (never store plain text)
- [ ] Store secrets in environment variables, not in code
- [ ] Add `.env`, `*.key`, `*.pem` to `.gitignore`
- [ ] Validate all user input at the boundary
- [ ] Use auto-escaping templates for HTML output
- [ ] Run `pip audit` regularly
- [ ] Keep dependencies updated
- [ ] Use HTTPS in production
- [ ] Set secure cookie flags (`HttpOnly`, `Secure`, `SameSite`)

## Common Mistakes

**Logging sensitive data:**
```python
# BAD — passwords in logs:
logger.info("Login attempt: user=%s, password=%s", username, password)

# GOOD — never log secrets:
logger.info("Login attempt: user=%s", username)
```

**Assuming client-side validation is enough:**
Client-side validation (JavaScript in the browser) improves user experience but provides zero security. An attacker can bypass it completely. Always validate on the server.

**Committing secrets to git:**
If you accidentally commit an API key or password, it lives in the git history forever — even if you delete the file later. You must rotate (change) any exposed credentials immediately. Prevention is key: set up `.gitignore` before your first commit.

## Practice

- [Module 04 FastAPI Web](../projects/modules/04-fastapi-web/) — authentication and input validation
- [Module 06 Databases & ORM](../projects/modules/06-databases-orm/) — parameterized queries
- [Elite Track / 04 Secure Auth Gateway](../projects/elite-track/04-secure-auth-gateway/README.md)
- [Elite Track / 08 Policy Compliance Engine](../projects/elite-track/08-policy-compliance-engine/README.md)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices (docs.python.org)](https://docs.python.org/3/library/security_warnings.html)
- [Bandit — Python security linter](https://bandit.readthedocs.io/)
- [pip-audit documentation](https://pypi.org/project/pip-audit/)

---

| [← Prev](git-basics.md) | [Home](../README.md) | [Next →](enums-explained.md) |
|:---|:---:|---:|

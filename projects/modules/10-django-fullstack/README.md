# Module 10 — Django Full-Stack

[README](../../../README.md) · Modules: [Index](../README.md)

## Overview

This module teaches you how to build full-stack web applications with Django, Python's most popular web framework. Django follows a "batteries included" philosophy: it ships with an ORM, an admin interface, a template engine, form handling, authentication, and much more. You will start by creating a project from scratch, then add views, templates, forms, user authentication, and finally a REST API with Django REST Framework.

By the end of this module you will have built a complete bookstore application with a web interface, user accounts, and a REST API.

## Prerequisites

Complete **Module 04 (FastAPI Web Apps)** and **Module 06 (Databases & ORM)** before starting this module. You should be comfortable with:

- Building web APIs with path parameters, query parameters, and request bodies
- HTTP methods (GET, POST, PUT, DELETE) and status codes
- ORM concepts: models, migrations, queries, relationships
- SQL fundamentals (SELECT, INSERT, UPDATE, DELETE, JOIN)
- Python classes, decorators, and type hints
- Virtual environments and pip

## Learning objectives

By the end of this module you will be able to:

1. Create a Django project and app using `startproject` and `startapp`.
2. Define models, run migrations, and use the Django admin interface.
3. Build views and templates using Django's MTV (Model-Template-View) pattern.
4. Create forms with validation using Django's ModelForm system.
5. Implement user registration, login, logout, and access control with `@login_required`.
6. Build a REST API using Django REST Framework with serializers, viewsets, and routers.
7. Write tests for models, views, and API endpoints using Django's test framework.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [Django Setup](./01-django-setup/) | startproject, startapp, models, admin, migrations, runserver |
| 02 | [Views & Templates](./02-views-templates/) | Function-based views, URL routing, templates, template tags |
| 03 | [Forms & Auth](./03-forms-auth/) | ModelForm, form validation, registration, login/logout, @login_required |
| 04 | [REST Framework](./04-rest-framework/) | DRF serializers, viewsets, routers, browsable API |
| 05 | [Complete App](./05-complete-app/) | Full CRUD combining models, views, templates, DRF, auth, and tests |

Work through them in order. Each project builds on concepts from the previous one.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/10-django-fullstack
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation of virtual environments.

## Dependencies

This module requires two packages (listed in `requirements.txt`):

- **django** — the web framework. It includes an ORM, template engine, form handling, authentication, admin interface, and development server. Django follows the MTV (Model-Template-View) pattern, which is similar to MVC but with different naming conventions.
- **djangorestframework** — a toolkit for building REST APIs on top of Django. It adds serializers (like Pydantic models in FastAPI), viewsets, routers, and a browsable API interface. If you used FastAPI in Module 04, DRF is Django's equivalent approach to API building.

## Django vs FastAPI

You already know FastAPI from Module 04. Here is how Django compares:

| Aspect | FastAPI | Django |
|--------|---------|--------|
| Philosophy | Minimal, bring your own tools | Batteries included |
| ORM | SQLAlchemy (separate library) | Built-in Django ORM |
| Admin | None (build your own) | Built-in admin interface |
| Templates | Jinja2 (optional) | Built-in template engine |
| Auth | Manual (JWT, etc.) | Built-in user model and auth views |
| API docs | Automatic Swagger/OpenAPI | Via DRF browsable API |
| Async | Native async | Supported since Django 4.1 |
| Best for | APIs, microservices | Full-stack apps, admin-heavy apps |

Both are excellent frameworks. Django excels when you need a full web application with a database, admin panel, and user authentication out of the box.

## Security Considerations

Django is famous for its built-in security features, but you still need to understand what they protect against and how to use them correctly.

### CSRF Protection

Django includes CSRF (Cross-Site Request Forgery) protection out of the box. Every HTML form that uses `POST` must include the token:

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

The `CsrfViewMiddleware` is enabled by default. Never disable it. For AJAX requests, include the CSRF token in the `X-CSRFToken` header.

### SQL Injection Prevention

The Django ORM generates parameterized queries, so standard queryset methods are safe:

```python
# SAFE — ORM handles parameterization
Book.objects.filter(title=user_input)

# DANGEROUS — raw SQL with string formatting
Book.objects.raw(f"SELECT * FROM books WHERE title = '{user_input}'")

# SAFE — raw SQL with parameters
Book.objects.raw("SELECT * FROM books WHERE title = %s", [user_input])
```

If you must use `raw()` or `cursor.execute()`, always pass parameters as a list — never use f-strings or `.format()`.

### XSS Prevention

Django's template engine auto-escapes all variables by default. The string `<script>alert('xss')</script>` renders as harmless text, not executable HTML.

Be careful with these patterns that bypass auto-escaping:

```python
# DANGEROUS — marks string as safe, skips escaping
from django.utils.safestring import mark_safe
mark_safe(user_input)  # Never do this with user input

# DANGEROUS — |safe filter in templates
{{ user_input|safe }}  # Only use with content YOU control
```

Only use `mark_safe()` or the `|safe` filter on content you have generated yourself, never on user-provided data.

### Django Security Middleware

Enable these middleware classes in `settings.py` (most are on by default):

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security headers
    "django.middleware.csrf.CsrfViewMiddleware",      # CSRF protection
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking prevention
    # ...
]
```

Key security settings to enable in production:

```python
# Force HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent XSS and content sniffing
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

### Authentication Best Practices

Django's built-in auth system handles password hashing (PBKDF2 by default) and session management. Follow these practices:

- Use `@login_required` or `LoginRequiredMixin` to protect views.
- Use Django's `User.objects.create_user()` which hashes passwords automatically.
- Never store passwords in plaintext or use `User.objects.create()` for user creation (it does not hash).
- Consider `django-allauth` for social login (Google, GitHub).

### Secrets Management with django-environ

Never hardcode secrets in `settings.py`. Use `django-environ` to load them from a `.env` file:

```python
# settings.py
import environ

env = environ.Env()
environ.Env.read_env()  # reads .env file

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3"),
}
```

Add `.env` to `.gitignore` so secrets are never committed to version control. Provide a `.env.example` file with placeholder values so other developers know which variables are needed.

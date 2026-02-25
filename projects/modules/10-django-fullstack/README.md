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

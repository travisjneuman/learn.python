# Django Setup — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently. The goal is to understand the files that Django generates when you create a new project and app. If you can run `setup_guide.py` and then start the development server with `python manage.py runserver`, you are on the right track.

## Thinking Process

Django is a "batteries included" framework — it gives you an admin panel, a database layer, user authentication, and URL routing out of the box. The tradeoff is that it creates a lot of files upfront, and if you do not understand what each file does, the project structure feels overwhelming.

This project takes a different approach from most Django tutorials. Instead of running `django-admin startproject` and accepting the magic, you run a guided script that creates each file manually and explains its purpose. The files are identical to what Django generates, but now you understand every one.

The core distinction in Django is between a "project" and an "app." A project is the overall website — it has settings, URL routing, and deployment configuration. An app is a self-contained feature module — it has models, views, and templates. A project can contain many apps. For example, an e-commerce project might have apps for catalog, cart, checkout, and accounts. This separation is what makes Django code reusable and organized.

## Step 1: Understand the Project Structure

**What to do:** Run `setup_guide.py` and read the explanation for each generated file.

**Why:** Before writing any Django code, you need a mental map of where things go. Every Django project has the same structure. Learning it now saves you hours of confusion later.

```bash
python setup_guide.py
```

The script creates this structure:

```
demo_project/
├── manage.py                 # CLI entry point (runserver, migrate, etc.)
├── demo_project/
│   ├── __init__.py           # Python package marker
│   ├── settings.py           # Central configuration
│   ├── urls.py               # URL routing table
│   └── wsgi.py               # Production server entry point
└── catalog/
    ├── __init__.py
    ├── apps.py               # App configuration
    ├── models.py             # Database models
    ├── admin.py              # Admin interface registration
    ├── views.py              # View functions (empty for now)
    └── migrations/
        └── __init__.py
```

**Predict:** Why is there a `demo_project/` directory inside `demo_project/`? What does each level represent?

## Step 2: Understand manage.py and settings.py

**What to do:** Read the generated `manage.py` and `settings.py` files. Focus on what each setting controls.

**Why:** `manage.py` is the command-line entry point for everything — starting the server, applying database changes, creating admin users. It does one critical thing: it sets `DJANGO_SETTINGS_MODULE` so Django knows which configuration to load. `settings.py` is the central configuration file that controls everything about your project.

```python
# manage.py sets this environment variable:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_project.settings")
```

Key settings to understand in `settings.py`:

- **`INSTALLED_APPS`** — every Django app must be listed here to be active
- **`DATABASES`** — where your data is stored (SQLite by default)
- **`ROOT_URLCONF`** — which file contains the top-level URL patterns
- **`DEBUG`** — shows detailed error pages in development (must be False in production)
- **`SECRET_KEY`** — used for sessions and CSRF tokens (never commit a real one)

**Predict:** What happens if you remove `'django.contrib.admin'` from `INSTALLED_APPS` and try to visit `/admin`?

## Step 3: Define a Model

**What to do:** Examine the `Item` model in `catalog/models.py`.

**Why:** A model is a Python class that maps to a database table. Each attribute becomes a column. Django's ORM (Object-Relational Mapper) translates between Python objects and SQL — you work with Python classes, and Django handles the database queries behind the scenes.

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

Four field types to understand:

- **`CharField(max_length=200)`** — short text, requires max_length (maps to VARCHAR in SQL)
- **`DecimalField`** — precise numbers for money (unlike FloatField, which has rounding issues)
- **`BooleanField(default=True)`** — True/False, with a default value
- **`DateTimeField(auto_now_add=True)`** — set automatically when the object is created

**Predict:** Why use `DecimalField` for price instead of `FloatField`? Try `0.1 + 0.2` in a Python shell to understand.

## Step 4: Register the App and Run Migrations

**What to do:** Add the app to `INSTALLED_APPS`, generate migrations, and apply them.

**Why:** Django does not create database tables directly from your models. Instead, it generates "migration" files — Python scripts that describe what changes to make to the database. This two-step process lets you review changes before applying them and provides a history of every schema change.

```bash
cd demo_project

# Step 1: Add the app to settings.py INSTALLED_APPS
# Add: "catalog.apps.CatalogConfig"

# Step 2: Generate migration files from your models
python manage.py makemigrations

# Step 3: Apply migrations to the database
python manage.py migrate
```

The first `migrate` applies Django's built-in tables (auth, sessions, admin) plus your catalog app's tables. You will see output like "Applying auth.0001_initial... OK" for each migration.

**Predict:** What happens if you change a model field and forget to run `makemigrations`? Does the database update automatically?

## Step 5: Create a Superuser and Start the Server

**What to do:** Create an admin account and run the development server.

**Why:** Django comes with a full admin interface at `/admin` that gives you CRUD operations (create, read, update, delete) for any registered model. You need a superuser account to log in. The development server lets you test everything locally.

```bash
# Create an admin account
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Then visit:
- **http://127.0.0.1:8000** — Django welcome page
- **http://127.0.0.1:8000/admin** — log in with your superuser credentials

Once logged in, you can add, edit, and delete Items through the admin interface — Django generated this entire UI from your model definition.

**Predict:** The admin interface shows "Catalog > Items." Where do the display columns come from? Look at `admin.py` for the `list_display` setting.

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `No installed app with label 'catalog'` | App not in `INSTALLED_APPS` | Add `"catalog.apps.CatalogConfig"` to the list |
| `CharField` missing `max_length` | Django requires it for CharFields | Add `max_length=200` (or use `TextField` for unlimited text) |
| Model changes not in database | Forgot `makemigrations` + `migrate` | Always run both commands after changing models |
| Admin shows object ID instead of name | Missing `__str__` method | Define `__str__(self)` on your model to return a readable name |

## Testing Your Solution

Run the setup script and then start the Django project:

```bash
python setup_guide.py
cd demo_project
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Verify:
- `http://127.0.0.1:8000` shows the Django welcome page
- `http://127.0.0.1:8000/admin` shows the login page
- After logging in, you can see and manage Items in the admin interface

Press `Ctrl+C` to stop the server.

## What You Learned

- **Django separates projects and apps** — a project is the overall configuration (settings, URLs), while an app is a self-contained feature module (models, views, templates) that can be reused across projects.
- **`manage.py`** is the entry point for all Django commands: `runserver` starts development, `migrate` applies database changes, `createsuperuser` creates admin accounts.
- **Models are Python classes that map to database tables** — Django's ORM translates between Python objects and SQL, so you rarely write raw SQL.
- **Migrations are a version control system for your database schema** — `makemigrations` generates the change scripts, `migrate` applies them, and the history is preserved.

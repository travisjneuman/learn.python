# ============================================================================
# Project 01 — Django Setup Guide
# ============================================================================
# This script programmatically creates a Django project structure and explains
# every file it generates. It is NOT a Django app itself — it is a learning
# tool that shows you what `django-admin startproject` and `manage.py startapp`
# would create, with detailed commentary on each file's purpose.
#
# Run this file:
#   python setup_guide.py
#
# After running, explore the generated `demo_project/` directory.
# ============================================================================

import os
import textwrap


# ----------------------------------------------------------------------------
# Helper: create a file with content and print an explanation.
#
# This function handles three things:
# 1. Creates any missing parent directories (like mkdir -p)
# 2. Writes the file content
# 3. Prints a human-readable explanation of what the file does
# ----------------------------------------------------------------------------
def create_file(filepath: str, content: str, explanation: str) -> None:
    """Create a file, write content to it, and print an explanation."""
    # os.makedirs creates all intermediate directories if they don't exist.
    # exist_ok=True prevents an error if the directory already exists.
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Created: {filepath}")
    # textwrap.indent adds padding to make the explanation visually distinct.
    print(textwrap.indent(explanation, "    -> "))
    print()


# ----------------------------------------------------------------------------
# Step 1: Create the project directory.
#
# In a real Django workflow, you would run:
#   django-admin startproject demo_project
#
# That command creates a directory with manage.py and a settings package.
# We are doing the same thing manually so you can see exactly what gets created.
# ----------------------------------------------------------------------------
def create_project_structure() -> str:
    """Create the Django project structure and return the base directory path."""
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_project")

    print("=" * 60)
    print("=== Django Project Setup Guide ===")
    print("=" * 60)
    print()

    # ------------------------------------------------------------------
    # Check if the project already exists. If so, warn the user.
    # ------------------------------------------------------------------
    if os.path.exists(base_dir):
        print(f"  Directory '{base_dir}' already exists.")
        print("  Delete it first if you want a fresh start:")
        print(f"    rm -rf {base_dir}")
        print()
        return base_dir

    print(f"[1/6] Creating project directory: demo_project/")
    print()

    # ------------------------------------------------------------------
    # manage.py — The command-line entry point for your Django project.
    #
    # Every Django command goes through manage.py:
    #   python manage.py runserver      — start the dev server
    #   python manage.py migrate        — apply database changes
    #   python manage.py makemigrations — generate migration files
    #   python manage.py createsuperuser — create an admin user
    #   python manage.py shell          — open a Python shell with Django loaded
    #   python manage.py startapp <name> — create a new app
    #
    # manage.py is nearly identical across all Django projects. It sets the
    # DJANGO_SETTINGS_MODULE environment variable and calls Django's CLI.
    # ------------------------------------------------------------------
    create_file(
        os.path.join(base_dir, "manage.py"),
        textwrap.dedent('''\
            #!/usr/bin/env python
            """Django's command-line utility for administrative tasks."""
            import os
            import sys


            def main():
                """Run administrative tasks."""
                # This tells Django which settings file to use. The string
                # "demo_project.settings" means: import demo_project/settings.py.
                os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_project.settings")
                try:
                    from django.core.management import execute_from_command_line
                except ImportError as exc:
                    raise ImportError(
                        "Couldn't import Django. Are you sure it's installed and "
                        "available on your PYTHONPATH environment variable? Did you "
                        "forget to activate a virtual environment?"
                    ) from exc
                execute_from_command_line(sys.argv)


            if __name__ == "__main__":
                main()
        '''),
        "The command-line entry point for your Django project.\n"
        "Run migrations, start the server, create apps — all through manage.py.\n"
        "It sets DJANGO_SETTINGS_MODULE so Django knows which config to load."
    )

    # ------------------------------------------------------------------
    # __init__.py files — Make directories into Python packages.
    #
    # Python requires an __init__.py file in a directory for it to be
    # importable as a package. These are usually empty in Django projects.
    # ------------------------------------------------------------------
    project_pkg = os.path.join(base_dir, "demo_project")

    create_file(
        os.path.join(project_pkg, "__init__.py"),
        "",
        "Makes the demo_project/ directory a Python package.\n"
        "Usually empty. Required for Python imports to work."
    )

    # ------------------------------------------------------------------
    # settings.py — The central configuration file.
    #
    # This is the single most important file in a Django project. It controls:
    # - INSTALLED_APPS: which Django apps are active
    # - DATABASES: where your data is stored
    # - MIDDLEWARE: request/response processing pipeline
    # - TEMPLATES: how Django finds and renders HTML templates
    # - AUTH_PASSWORD_VALIDATORS: password security rules
    # - STATIC_URL: where static files (CSS, JS, images) are served from
    # - SECRET_KEY: cryptographic key for sessions, CSRF tokens, etc.
    # ------------------------------------------------------------------
    print("[2/6] Creating settings.py")
    print()
    create_file(
        os.path.join(project_pkg, "settings.py"),
        textwrap.dedent('''\
            """
            Django settings for demo_project.

            Generated by the setup_guide.py learning script.
            For the full settings reference, see:
            https://docs.djangoproject.com/en/5.0/ref/settings/
            """

            from pathlib import Path

            # Build paths inside the project like this: BASE_DIR / "subdir".
            # BASE_DIR points to the directory containing manage.py.
            # Path(__file__).resolve() gets the absolute path of this settings file,
            # then .parent.parent goes up two directories to the project root.
            BASE_DIR = Path(__file__).resolve().parent.parent

            # SECURITY WARNING: keep the secret key used in production secret!
            # This key is used for cryptographic signing (sessions, CSRF tokens, etc.).
            # In production, load this from an environment variable — never commit it.
            SECRET_KEY = "django-insecure-learning-key-do-not-use-in-production"

            # SECURITY WARNING: don't run with debug turned on in production!
            # DEBUG=True shows detailed error pages with stack traces and variable values.
            # In production, set this to False so users see a generic error page instead.
            DEBUG = True

            # A list of hostnames/domains this Django site can serve.
            # With DEBUG=True, Django allows localhost automatically.
            # In production, add your domain: ["mysite.com", "www.mysite.com"]
            ALLOWED_HOSTS = []

            # ----------------------------------------------------------------
            # INSTALLED_APPS: Every Django app must be listed here to be active.
            #
            # Django comes with several built-in apps:
            # - admin: the /admin interface for managing database objects
            # - auth: user accounts, passwords, permissions, groups
            # - contenttypes: tracks which models exist (used internally)
            # - sessions: server-side session storage for logged-in users
            # - messages: one-time notification messages (e.g., "Item saved!")
            # - staticfiles: serves CSS, JS, and images during development
            #
            # Your own apps go at the end of this list.
            # ----------------------------------------------------------------
            INSTALLED_APPS = [
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
                # Add your apps here, e.g.:
                # "catalog.apps.CatalogConfig",
            ]

            # ----------------------------------------------------------------
            # MIDDLEWARE: A pipeline that processes every request and response.
            #
            # Each middleware is a layer. Requests pass through them top to bottom,
            # and responses pass back bottom to top. Order matters.
            # ----------------------------------------------------------------
            MIDDLEWARE = [
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
            ]

            # ROOT_URLCONF tells Django which file contains the top-level URL patterns.
            # Django starts here and follows includes to find the right view for each URL.
            ROOT_URLCONF = "demo_project.urls"

            # ----------------------------------------------------------------
            # TEMPLATES: How Django finds and renders HTML templates.
            #
            # DIRS: extra directories to search for templates (besides app directories).
            # APP_DIRS: if True, Django looks in each app's templates/ subdirectory.
            # ----------------------------------------------------------------
            TEMPLATES = [
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.template.context_processors.debug",
                            "django.template.context_processors.request",
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                        ],
                    },
                },
            ]

            # WSGI_APPLICATION points to the WSGI callable for deployment.
            # WSGI (Web Server Gateway Interface) is the standard for Python web apps.
            WSGI_APPLICATION = "demo_project.wsgi.application"

            # ----------------------------------------------------------------
            # DATABASES: Where your data lives.
            #
            # By default, Django uses SQLite — a file-based database that
            # requires zero setup. The database file (db.sqlite3) appears in
            # your project root after running migrate.
            #
            # For production, you would switch to PostgreSQL or MySQL.
            # ----------------------------------------------------------------
            DATABASES = {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                }
            }

            # Password validation rules. These prevent weak passwords.
            AUTH_PASSWORD_VALIDATORS = [
                {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
                {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
                {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
                {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
            ]

            # Internationalization settings.
            LANGUAGE_CODE = "en-us"
            TIME_ZONE = "UTC"
            USE_I18N = True    # Enable Django's translation system
            USE_TZ = True      # Store datetimes in UTC in the database

            # Static files (CSS, JavaScript, Images).
            # STATIC_URL is the URL prefix for static files.
            # In development, Django serves them automatically.
            STATIC_URL = "static/"

            # Default primary key field type for models.
            # BigAutoField creates an auto-incrementing 64-bit integer.
            DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
        '''),
        "The central configuration file for your Django project.\n"
        "Controls installed apps, database, middleware, templates, and more.\n"
        "Every setting has a comment explaining its purpose."
    )

    # ------------------------------------------------------------------
    # urls.py — The top-level URL configuration.
    #
    # This file maps URL patterns to views. It is the "table of contents"
    # for your web application. When a request comes in, Django starts here
    # and follows the patterns to find the right view function.
    # ------------------------------------------------------------------
    print("[3/6] Creating urls.py")
    print()
    create_file(
        os.path.join(project_pkg, "urls.py"),
        textwrap.dedent('''\
            """
            URL configuration for demo_project.

            The `urlpatterns` list routes URLs to views. For more information:
            https://docs.djangoproject.com/en/5.0/topics/http/urls/
            """
            from django.contrib import admin
            from django.urls import path

            # Each path() call maps a URL pattern to a view.
            # "admin/" maps to Django's built-in admin interface.
            # You will add more patterns here as you create views.
            urlpatterns = [
                path("admin/", admin.site.urls),
            ]
        '''),
        "The top-level URL configuration (like a routing table).\n"
        "Django reads this file to decide which view handles each URL.\n"
        "You add entries here for each app and endpoint."
    )

    # ------------------------------------------------------------------
    # wsgi.py — The WSGI entry point for deployment.
    #
    # WSGI (Web Server Gateway Interface) is the standard protocol between
    # Python web apps and web servers (like Gunicorn or Apache). In production,
    # the web server imports this file to get the application callable.
    #
    # You rarely edit this file. It exists so deployment tools can find your app.
    # ------------------------------------------------------------------
    print("[4/6] Creating wsgi.py")
    print()
    create_file(
        os.path.join(project_pkg, "wsgi.py"),
        textwrap.dedent('''\
            """
            WSGI config for demo_project.

            It exposes the WSGI callable as a module-level variable named ``application``.
            For more information:
            https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
            """

            import os
            from django.core.wsgi import get_wsgi_application

            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_project.settings")

            # This is the WSGI application object that web servers use.
            # Gunicorn, uWSGI, or Apache mod_wsgi will import this.
            application = get_wsgi_application()
        '''),
        "The WSGI entry point for production deployment.\n"
        "Web servers (Gunicorn, Apache) import this to serve your app.\n"
        "You rarely need to edit this file."
    )

    # ------------------------------------------------------------------
    # Step 2: Create a sample app called "catalog".
    #
    # In a real workflow, you would run:
    #   python manage.py startapp catalog
    #
    # A Django "app" is a self-contained module with models, views, templates,
    # and tests. A project can contain many apps. For example, an e-commerce
    # site might have apps for: catalog, cart, checkout, accounts.
    # ------------------------------------------------------------------
    print("[5/6] Creating the 'catalog' app")
    print()
    app_dir = os.path.join(base_dir, "catalog")

    create_file(
        os.path.join(app_dir, "__init__.py"),
        "",
        "Makes the catalog/ directory a Python package."
    )

    create_file(
        os.path.join(app_dir, "apps.py"),
        textwrap.dedent('''\
            from django.apps import AppConfig


            class CatalogConfig(AppConfig):
                """Configuration class for the catalog app.

                Django uses this to identify your app. The `name` attribute must
                match the directory name. You can set a human-readable `verbose_name`
                for the admin interface.
                """
                default_auto_field = "django.db.models.BigAutoField"
                name = "catalog"
        '''),
        "App configuration class. Django reads this to register your app.\n"
        "The `name` must match the directory name exactly."
    )

    # ------------------------------------------------------------------
    # models.py — Where you define your database tables as Python classes.
    #
    # Each model class becomes a database table. Each attribute becomes a column.
    # Django's ORM handles the translation between Python objects and SQL.
    #
    # After defining or changing models, you must run:
    #   python manage.py makemigrations  (generate the migration file)
    #   python manage.py migrate         (apply it to the database)
    # ------------------------------------------------------------------
    create_file(
        os.path.join(app_dir, "models.py"),
        textwrap.dedent('''\
            from django.db import models


            class Item(models.Model):
                """A simple item in our catalog.

                Each attribute becomes a database column:
                - name: a short text field (VARCHAR in SQL), max 200 characters
                - price: a decimal number with up to 8 digits and 2 decimal places
                - in_stock: a boolean (True/False), defaults to True
                - created_at: a datetime that is set automatically when created

                The __str__ method controls how this object appears in the admin
                interface and in print() statements.
                """
                # CharField requires max_length. It maps to VARCHAR(200) in SQL.
                name = models.CharField(max_length=200)

                # DecimalField is precise (unlike FloatField). Use it for money.
                # max_digits=8 means up to 99999999. decimal_places=2 means two decimals.
                price = models.DecimalField(max_digits=8, decimal_places=2)

                # BooleanField stores True or False. default=True means new items
                # are in stock unless you say otherwise.
                in_stock = models.BooleanField(default=True)

                # DateTimeField with auto_now_add=True records the creation timestamp.
                # Django sets this automatically; you never assign it manually.
                created_at = models.DateTimeField(auto_now_add=True)

                def __str__(self):
                    """Return the item name when this object is printed or displayed."""
                    return self.name
        '''),
        "Model definitions — your database tables as Python classes.\n"
        "Each attribute becomes a column. Django's ORM handles the SQL.\n"
        "After changing models, run: makemigrations then migrate."
    )

    # ------------------------------------------------------------------
    # admin.py — Register your models with the Django admin interface.
    #
    # The admin interface is one of Django's killer features. By registering
    # a model, you get a full CRUD interface (create, read, update, delete)
    # with search, filtering, and pagination — for free.
    # ------------------------------------------------------------------
    create_file(
        os.path.join(app_dir, "admin.py"),
        textwrap.dedent('''\
            from django.contrib import admin
            from .models import Item


            # Register the Item model with the admin interface.
            # After registering, you can manage Items at /admin/catalog/item/.
            # Django automatically generates list views, detail forms, and
            # search/filter capabilities.
            @admin.register(Item)
            class ItemAdmin(admin.ModelAdmin):
                """Customize how Items appear in the admin interface."""

                # list_display controls which columns appear in the item list.
                list_display = ["name", "price", "in_stock", "created_at"]

                # list_filter adds filter sidebar options.
                list_filter = ["in_stock"]

                # search_fields enables a search box that searches these fields.
                search_fields = ["name"]
        '''),
        "Registers models with the Django admin interface.\n"
        "You get a full CRUD UI for free: list, create, edit, delete.\n"
        "Customize with list_display, list_filter, and search_fields."
    )

    # ------------------------------------------------------------------
    # views.py — Placeholder for view functions.
    # We will build views properly in Project 02.
    # ------------------------------------------------------------------
    create_file(
        os.path.join(app_dir, "views.py"),
        textwrap.dedent('''\
            # Views will be created in Project 02 (views-templates).
            # A view is a Python function that receives a web request and returns
            # a web response. The response can be HTML, JSON, a redirect, etc.
            #
            # Example:
            #   from django.http import HttpResponse
            #
            #   def index(request):
            #       return HttpResponse("Hello from the catalog app!")
        '''),
        "Placeholder for view functions (covered in Project 02).\n"
        "Views receive HTTP requests and return HTTP responses."
    )

    # ------------------------------------------------------------------
    # Initial migration — Django needs this directory to track schema changes.
    # ------------------------------------------------------------------
    migrations_dir = os.path.join(app_dir, "migrations")
    create_file(
        os.path.join(migrations_dir, "__init__.py"),
        "",
        "Makes migrations/ a Python package.\n"
        "Django stores migration files here (one per schema change).\n"
        "Never delete this directory — migrations are your schema history."
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("[6/6] Setup complete!")
    print()
    print("=" * 60)
    print("Generated project structure:")
    print("=" * 60)
    print()
    print("  demo_project/")
    print("  ├── manage.py               <- CLI entry point")
    print("  ├── demo_project/")
    print("  │   ├── __init__.py          <- Python package marker")
    print("  │   ├── settings.py          <- Central configuration")
    print("  │   ├── urls.py              <- URL routing table")
    print("  │   └── wsgi.py              <- Production server entry point")
    print("  └── catalog/")
    print("      ├── __init__.py          <- Python package marker")
    print("      ├── apps.py              <- App configuration")
    print("      ├── models.py            <- Database models (tables)")
    print("      ├── admin.py             <- Admin interface registration")
    print("      ├── views.py             <- View functions (empty for now)")
    print("      └── migrations/")
    print("          └── __init__.py      <- Migration package marker")
    print()
    print("=" * 60)
    print("Next steps:")
    print("=" * 60)
    print()
    print("  1. Add 'catalog.apps.CatalogConfig' to INSTALLED_APPS in settings.py")
    print("  2. cd demo_project")
    print("  3. python manage.py makemigrations    # Generate migration for Item model")
    print("  4. python manage.py migrate           # Apply all migrations")
    print("  5. python manage.py createsuperuser   # Create an admin account")
    print("  6. python manage.py runserver         # Start the dev server")
    print("  7. Open http://127.0.0.1:8000/admin   # Log in and manage Items")
    print()

    return base_dir


# ----------------------------------------------------------------------------
# Main entry point.
# Run this script to create the project structure and see explanations.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    create_project_structure()

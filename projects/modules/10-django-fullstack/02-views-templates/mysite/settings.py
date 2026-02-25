# ============================================================================
# Django Settings — Views & Templates Project
# ============================================================================
# This is the central configuration file for this Django project.
# Every setting that matters is explained with comments below.
# ============================================================================

from pathlib import Path

# BASE_DIR points to the directory containing manage.py.
# All relative paths in this file are resolved from BASE_DIR.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY is used for cryptographic signing (sessions, CSRF protection).
# In production, load this from an environment variable. Never commit real keys.
SECRET_KEY = "django-insecure-learning-key-change-in-production"

# DEBUG=True shows detailed error pages with tracebacks and local variables.
# Always set to False in production to avoid leaking sensitive information.
DEBUG = True

# ALLOWED_HOSTS is a list of domain names this site can serve.
# Empty list means only localhost is allowed (when DEBUG=True).
ALLOWED_HOSTS = []

# ----------------------------------------------------------------
# INSTALLED_APPS: Every active Django app must be listed here.
#
# Django apps are self-contained modules with models, views, templates,
# and tests. The order matters for template resolution: Django searches
# apps top to bottom and uses the first matching template it finds.
# ----------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",          # Admin interface at /admin/
    "django.contrib.auth",           # User authentication system
    "django.contrib.contenttypes",   # Content type framework (internal)
    "django.contrib.sessions",       # Session framework for logged-in users
    "django.contrib.messages",       # One-time notification messages
    "django.contrib.staticfiles",    # Serves CSS/JS/images in development
    "bookstore",                     # Our bookstore app
]

# MIDDLEWARE: A pipeline that processes every HTTP request and response.
# Each middleware wraps the next one. Requests flow top-to-bottom,
# responses flow bottom-to-top. Order matters.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF: The module that contains the top-level URL patterns.
# Django starts URL resolution here.
ROOT_URLCONF = "mysite.urls"

# TEMPLATES: Configuration for Django's template engine.
# APP_DIRS=True means Django looks for a templates/ directory inside each app.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],            # Additional template directories (beyond app dirs)
        "APP_DIRS": True,      # Auto-discover templates/ in each installed app
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

WSGI_APPLICATION = "mysite.wsgi.application"

# DATABASE: SQLite for development. The file db.sqlite3 appears in BASE_DIR
# after running `python manage.py migrate`.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# STATIC_URL: URL prefix for static files (CSS, JavaScript, images).
# In development, Django serves these automatically.
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

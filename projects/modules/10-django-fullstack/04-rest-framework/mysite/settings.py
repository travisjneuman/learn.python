# ============================================================================
# Django Settings — REST Framework Project
# ============================================================================
# Extends settings from previous projects with Django REST Framework.
# New: "rest_framework" in INSTALLED_APPS and REST_FRAMEWORK config.
# ============================================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-learning-key-change-in-production"

DEBUG = True

ALLOWED_HOSTS = []

# ----------------------------------------------------------------
# INSTALLED_APPS: Note "rest_framework" at the end.
#
# Django REST Framework must be in INSTALLED_APPS because it includes:
# - Templates for the browsable API interface
# - Static files (CSS/JS for the browsable API)
# - App configuration for DRF's internals
# ----------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",    # NEW: Django REST Framework
    "bookstore",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

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

WSGI_APPLICATION = "mysite.wsgi.application"

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

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================================
# NEW: Django REST Framework configuration
# ============================================================================
# REST_FRAMEWORK is DRF's global settings dictionary. Common settings:
#
# DEFAULT_PERMISSION_CLASSES: Who can access the API by default.
#   - AllowAny: anyone (no auth required)
#   - IsAuthenticated: only logged-in users
#   - IsAuthenticatedOrReadOnly: anyone can read, only auth users can write
#
# DEFAULT_AUTHENTICATION_CLASSES: How users prove their identity.
#   - SessionAuthentication: uses Django's session cookie (for browsers)
#   - BasicAuthentication: HTTP Basic auth (username:password in headers)
#   - TokenAuthentication: token-based auth (similar to JWT)
# ============================================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ============================================================================
# Django Settings — Complete App Project
# ============================================================================
# This is the final settings file for the complete bookstore application.
# It combines all settings from previous projects: Django core, auth
# configuration, and Django REST Framework.
# ============================================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: In a real app, load this from an environment variable:
#   SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
SECRET_KEY = "django-insecure-learning-key-change-in-production"

# DEBUG: Set to False in production. With True, Django shows detailed errors
# including source code, local variables, and SQL queries to anyone who
# triggers an error — a security risk on public servers.
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",          # Admin interface
    "django.contrib.auth",           # Authentication system
    "django.contrib.contenttypes",   # Content type framework
    "django.contrib.sessions",       # Session framework
    "django.contrib.messages",       # Messaging framework
    "django.contrib.staticfiles",    # Static file serving
    "rest_framework",                # Django REST Framework
    "bookstore",                     # Our bookstore app
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

# Authentication settings
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/books/"
LOGOUT_REDIRECT_URL = "/books/"

# Django REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

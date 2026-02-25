# ============================================================================
# Top-Level URL Configuration — Forms & Auth Project
# ============================================================================
# This project adds authentication URLs alongside the bookstore app URLs.
# ============================================================================

from django.contrib import admin
from django.urls import include, path

from bookstore import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Bookstore app URLs (book list, detail, add).
    path("books/", include("bookstore.urls")),

    # Authentication URLs: register, login, logout.
    # These are defined here (not in bookstore/urls.py) because authentication
    # is a site-wide concern, not specific to the bookstore app.
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

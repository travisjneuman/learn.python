# ============================================================================
# Top-Level URL Configuration — Complete App
# ============================================================================
# This combines all URL patterns: admin, HTML views, API endpoints, and auth.
# ============================================================================

from django.contrib import admin
from django.urls import include, path

from bookstore import views

urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),

    # HTML views (book list, detail, add)
    path("books/", include("bookstore.urls_html")),

    # REST API endpoints (DRF router-generated)
    path("api/", include("bookstore.urls_api")),

    # Authentication views
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

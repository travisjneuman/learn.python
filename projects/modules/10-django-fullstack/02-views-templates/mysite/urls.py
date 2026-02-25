# ============================================================================
# Top-Level URL Configuration
# ============================================================================
# This is the root URL configuration for the project. Django starts here
# when resolving URLs. We include the bookstore app's URLs and the admin.
#
# The include() function delegates URL resolution to another module.
# This keeps URL patterns organized: each app manages its own URLs.
# ============================================================================

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django's built-in admin interface.
    path("admin/", admin.site.urls),

    # Include all URL patterns from the bookstore app.
    # Any URL starting with "books/" is handed off to bookstore/urls.py.
    path("books/", include("bookstore.urls")),
]

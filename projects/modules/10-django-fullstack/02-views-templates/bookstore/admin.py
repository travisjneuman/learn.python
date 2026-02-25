# ============================================================================
# Bookstore Admin Configuration
# ============================================================================
# Register models here to make them manageable through Django's admin
# interface at /admin/. The admin gives you a complete CRUD interface
# (create, read, update, delete) for free.
# ============================================================================

from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Customize how Book objects appear in the admin interface."""

    # list_display: which columns to show in the list view.
    list_display = ["title", "author", "price", "published_date"]

    # list_filter: adds a filter sidebar. Users can filter by these fields.
    list_filter = ["author"]

    # search_fields: enables a search box. Searches these fields.
    search_fields = ["title", "author"]

    # ordering: default sort order in the admin list view.
    ordering = ["-published_date"]

# ============================================================================
# Bookstore URL Patterns — REST Framework Project
# ============================================================================
# DRF routers automatically generate URL patterns from ViewSets.
#
# router.register("books", BookViewSet) generates:
#   /books/       -> list and create
#   /books/{pk}/  -> retrieve, update, and destroy
#
# This is similar to FastAPI's APIRouter, but DRF routers generate all
# CRUD URLs from a single registration call.
#
# The DefaultRouter also creates an API root view at the base URL that
# lists all registered endpoints — useful for API discovery.
# ============================================================================

from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet

# DefaultRouter generates URL patterns and an API root view.
# SimpleRouter is an alternative that skips the API root view.
router = DefaultRouter()

# Register each ViewSet with a URL prefix and an optional base_name.
# The prefix becomes the URL path: "books" -> /api/books/
# The base_name is used for URL naming: "book-list", "book-detail"
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)

# router.urls contains all generated URL patterns.
# We assign it to urlpatterns so Django includes them.
urlpatterns = router.urls

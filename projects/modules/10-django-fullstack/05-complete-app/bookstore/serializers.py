# ============================================================================
# Bookstore Serializers — Complete App
# ============================================================================
# DRF serializers for the REST API. Same as Project 04.
# ============================================================================

from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author objects."""

    class Meta:
        model = Author
        fields = ["id", "name", "bio"]


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book objects with author name included."""

    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_name", "price", "published_date"]

    def get_author_name(self, obj):
        """Return the author's name."""
        return obj.author.name

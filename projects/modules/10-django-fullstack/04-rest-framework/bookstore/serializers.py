# ============================================================================
# Bookstore Serializers — REST Framework Project
# ============================================================================
# Serializers convert Django model instances to JSON (serialization) and
# convert JSON data back to model instances (deserialization). They also
# handle validation, similar to Pydantic models in FastAPI.
#
# Comparison to FastAPI:
#   FastAPI Pydantic model  ->  DRF Serializer
#   model_validate()        ->  serializer.is_valid()
#   model_dump()            ->  serializer.data
#   Field(...)              ->  serializer field options
#
# ModelSerializer is like ModelForm: it auto-generates fields from a model.
# ============================================================================

from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model.

    ModelSerializer automatically creates serializer fields that correspond
    to the model fields listed in Meta.fields. It also generates:
    - create() method: creates a new Author from validated data
    - update() method: updates an existing Author from validated data

    The 'id' field is included as read-only by default (you cannot set it).
    """

    class Meta:
        # model: which Django model to serialize
        model = Author

        # fields: which model fields to include in the JSON output.
        # Use "__all__" for all fields, or list specific field names.
        # Explicit field lists are safer (prevent accidental data exposure).
        fields = ["id", "name", "bio"]


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model.

    This serializer demonstrates:
    1. Including a ForeignKey field (author) as an ID
    2. Adding a computed field (author_name) using SerializerMethodField
    3. Automatic validation based on model field constraints

    In the JSON output, the author field contains the author's ID (integer),
    and author_name contains the author's name (string, read-only).
    """

    # SerializerMethodField creates a read-only field whose value comes from
    # a method on the serializer. The method name must be get_<field_name>.
    # This is useful for computed or denormalized data in API responses.
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_name", "price", "published_date"]

    def get_author_name(self, obj):
        """Return the author's name for the author_name field.

        Args:
            obj: The Book instance being serialized.

        Returns:
            The name of the book's author as a string.

        This method is called automatically by DRF when serializing each Book.
        The `obj` parameter is the Book instance, so obj.author accesses the
        related Author object through the ForeignKey.
        """
        return obj.author.name

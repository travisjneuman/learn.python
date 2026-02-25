# ============================================================================
# Bookstore Models — Views & Templates Project
# ============================================================================
# Models define your database schema as Python classes. Each model becomes a
# database table, and each attribute becomes a column.
#
# After defining or changing models, run:
#   python manage.py makemigrations    (generate migration file)
#   python manage.py migrate           (apply to database)
# ============================================================================

from django.db import models


class Book(models.Model):
    """A book in the bookstore.

    This model has four fields that map to database columns:
    - title: the book's title (up to 300 characters)
    - author: the author's name (up to 200 characters)
    - price: the book's price as a precise decimal
    - published_date: when the book was published

    The __str__ method controls how this object appears in the admin
    interface, in print() statements, and in template output like {{ book }}.
    """

    # CharField: short text. max_length is required and maps to VARCHAR in SQL.
    title = models.CharField(max_length=300)

    # Another CharField for the author name.
    author = models.CharField(max_length=200)

    # DecimalField: precise decimal numbers. Use this for money instead of
    # FloatField, which can have rounding errors (e.g., 0.1 + 0.2 != 0.3).
    # max_digits=6 allows values up to 9999.99 with decimal_places=2.
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # DateField: stores a date (year, month, day) without a time component.
    # null=True allows the database column to be NULL.
    # blank=True allows the field to be left empty in forms and the admin.
    # These two settings usually go together for optional fields.
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """Return a readable string for this book."""
        return f"{self.title} by {self.author}"

    class Meta:
        """Model metadata. Controls database-level behavior."""
        # ordering: default sort order for querysets.
        # "-published_date" means newest first (descending).
        ordering = ["-published_date"]

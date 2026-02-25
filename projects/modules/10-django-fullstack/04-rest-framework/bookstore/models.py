# ============================================================================
# Bookstore Models — REST Framework Project
# ============================================================================
# This project introduces a relationship between two models: Author and Book.
# An Author can have many Books (one-to-many relationship via ForeignKey).
#
# This is the same pattern you learned in Module 06 (Databases & ORM) with
# SQLAlchemy. Django's ORM uses ForeignKey instead of sqlalchemy.relationship.
# ============================================================================

from django.db import models


class Author(models.Model):
    """An author who writes books.

    This model demonstrates:
    - CharField: short text fields
    - TextField: long text with no max_length requirement
    - The reverse relationship: author.books.all() returns all their books
    """

    # The author's name. max_length is required for CharField.
    name = models.CharField(max_length=200)

    # A short biography. TextField has no max_length limit.
    # blank=True means this field is optional in forms.
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Book(models.Model):
    """A book in the bookstore, linked to an Author.

    The ForeignKey field creates a many-to-one relationship:
    - Each Book belongs to exactly one Author
    - Each Author can have many Books

    In the database, this creates a column `author_id` in the book table
    that references the author table's primary key.
    """

    title = models.CharField(max_length=300)

    # ForeignKey creates the relationship. Arguments:
    # - Author: the related model
    # - on_delete=models.CASCADE: if the author is deleted, delete their books too
    #   Other options: PROTECT (prevent deletion), SET_NULL, SET_DEFAULT
    # - related_name="books": the name for the reverse relationship
    #   This lets you do: author.books.all() to get all books by an author
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )

    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ["-published_date"]

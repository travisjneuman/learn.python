# ============================================================================
# Bookstore Models — Complete App
# ============================================================================
# This combines the Author/Book relationship from Project 04 with all
# the features from previous projects. Both the HTML views and the REST API
# share these same models.
# ============================================================================

from django.db import models


class Author(models.Model):
    """An author who writes books."""

    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Book(models.Model):
    """A book in the bookstore, linked to an Author."""

    title = models.CharField(max_length=300)
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

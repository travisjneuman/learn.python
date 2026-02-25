# ============================================================================
# Bookstore Models — Forms & Auth Project
# ============================================================================
# Same Book model from Project 02. Repeated here so this project is
# self-contained and runnable on its own.
# ============================================================================

from django.db import models


class Book(models.Model):
    """A book in the bookstore."""

    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ["-published_date"]

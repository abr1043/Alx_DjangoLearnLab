from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True, help_text="Enter the title of the book")
    author = models.CharField(max_length=200, help_text="Enter the author of the book")
    published_date = models.DateField(null=True, blank=True, help_text="Date when the book was published")
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when created
    updated_at = models.DateTimeField(auto_now=True)      # Updated on each save

    class Meta:
        ordering = ["title"]  # Books will be ordered alphabetically by title
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} by {self.author}"

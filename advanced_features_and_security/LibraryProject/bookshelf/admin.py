from django.contrib import admin
from .models import Book

# Custom admin configuration
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # show these in the list
    search_fields = ('title', 'author')                      # search bar for title/author
    list_filter = ('publication_year',)                      # filter by year

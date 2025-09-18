
- **retrieve.md**
```markdown
```python
retrieved = Book.objects.get(id=book.id)
retrieved.title, retrieved.author, retrieved.publication_year
# ('1984', 'George Orwell', 1949)

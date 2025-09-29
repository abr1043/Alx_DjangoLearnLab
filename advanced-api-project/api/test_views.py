from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.book = Book.objects.create(title="Test Book", author="Author Name", publication_year=2023)

    def test_get_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response contains the book title
        self.assertIn("Test Book", str(response.data))

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "New Book", "author": "Another Author", "publication_year": 2024}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check response returns the same title
        self.assertEqual(response.data["title"], "New Book")

    def test_update_book(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "Updated Title", "author": "Author Name", "publication_year": 2023}
        response = self.client.put(f"/api/books/{self.book.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify update applied
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_book(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Confirm book is deleted
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_permissions_for_unauthenticated_users(self):
        data = {"title": "No Auth Book", "author": "Unknown", "publication_year": 2022}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure no book was created
        self.assertFalse(Book.objects.filter(title="No Auth Book").exists())

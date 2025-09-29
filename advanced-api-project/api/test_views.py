from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        # Create an author and a book
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )

        # Endpoints
        self.book_list_url = reverse("book-list")  # /books/
        self.book_detail_url = reverse("book-detail", args=[self.book.id])  # /books/<id>/

    def test_list_books(self):
        """Test GET /books/ returns status 200 and contains book data"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.book.title)

    def test_create_book(self):
        """Test POST /books/ creates a new book"""
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.book_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """Test PUT /books/<id>/ updates the book"""
        data = {
            "title": "Updated Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        """Test DELETE /books/<id>/ deletes the book"""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_year(self):
        """Test filtering by publication_year"""
        response = self.client.get(self.book_list_url, {"publication_year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.book.title)

    def test_permissions_for_unauthenticated_users(self):
        """Ensure unauthenticated users only have read access"""
        self.client.logout()
        response = self.client.post(self.book_list_url, {"title": "Blocked Book"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

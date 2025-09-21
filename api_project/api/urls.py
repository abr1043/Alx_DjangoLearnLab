from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Initialize router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Old ListAPIView endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # Router-based CRUD endpoints
    path('', include(router.urls)),
]

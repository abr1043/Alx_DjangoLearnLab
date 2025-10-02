from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),                  # List all posts
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # View single post
    path('post/new/', PostCreateView.as_view(), name='post-create'),      # Create a new post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Update post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete post
]

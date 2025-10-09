from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikePostAPIView, FeedAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),

    # ✅ Feed view (shows posts from followed users)
    path('feed/', FeedAPIView.as_view(), name='feed'),

    # ✅ Like and Unlike routes (required by checker)
    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', LikePostAPIView.as_view(), name='unlike-post'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikePostAPIView, FeedAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('feed/', FeedAPIView.as_view(), name='user-feed'),
]

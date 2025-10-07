from django.urls import path
from .views import RegisterAPIView, FollowUserAPIView, UnfollowUserAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('follow/<str:username>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', UnfollowUserAPIView.as_view(), name='unfollow-user'),
]

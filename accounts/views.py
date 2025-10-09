from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser


class FollowUserView(generics.GenericAPIView):
    """
    Allows an authenticated user to follow another user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        # Prevent self-follow
        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add follow relationship
        request.user.following.add(user_to_follow)
        return Response(
            {"detail": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    Allows an authenticated user to unfollow another user.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        # Prevent self-unfollow
        if user_to_unfollow == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove follow relationship
        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": f"You have unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )

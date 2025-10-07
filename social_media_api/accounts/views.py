from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from .serializers import UserSerializer, RegisterSerializer

CustomUser = get_user_model()


# -------------------- Register API --------------------
class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


# -------------------- Follow a User --------------------
class FollowUserAPIView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = kwargs.get("username")
        try:
            user_to_follow = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"message": f"You are now following {username}"}, status=status.HTTP_200_OK)


# -------------------- Unfollow a User --------------------
class UnfollowUserAPIView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = kwargs.get("username")
        try:
            user_to_unfollow = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_unfollow:
            return Response({"error": "You ca

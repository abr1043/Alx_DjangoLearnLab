from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikePostAPIView(APIView):
    """
    Handles liking and unliking posts.
    Uses Like model and creates notifications.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ Required check line:
        post = generics.get_object_or_404(Post, pk=pk)

        # ✅ Required Like creation:
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            # User already liked → unlike
            like.delete()
            return Response({'message': 'Post unliked.'}, status=status.HTTP_200_OK)

        # ✅ Create notification only when liked
        if post.author != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                message=f"{request.user.username} liked your post."
            )

        return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)


class FeedAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

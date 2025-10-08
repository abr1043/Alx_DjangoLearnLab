from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Handles creating, listing, retrieving, updating, and deleting posts.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles creating, listing, and deleting comments.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikePostAPIView(APIView):
    """
    Allows authenticated users to like or unlike a post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'message': 'Post unliked.'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({'message': 'Post liked.'}, status=status.HTTP_200_OK)


class FeedAPIView(generics.GenericAPIView):
    """
    Returns posts from users that the current user follows,
    ordered by most recent first.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

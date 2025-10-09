# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments', 'likes_count']


class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'user_username', 'created_at']
        read_only_fields = ['id', 'user', 'user_username', 'created_at']

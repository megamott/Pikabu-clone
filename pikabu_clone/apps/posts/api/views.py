from rest_framework import generics, viewsets
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    CommentChildSerializer,
)
from ..models import (
    Post,
    Comment
)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer


class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CommentDetailView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentChildSerializer


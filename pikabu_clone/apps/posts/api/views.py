from rest_framework import generics
from .serializers import (
    PostDetailSerializer,
    PostListSerializer
)
from ..models import Post


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer


class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

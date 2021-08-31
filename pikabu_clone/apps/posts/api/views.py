from rest_framework import generics
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    CommentDetailsSerializer,
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
    serializer_class = CommentDetailsSerializer

    def get_queryset(self):
        return Comment.objects.find_parent_comments()

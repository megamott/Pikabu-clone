from rest_framework import generics, viewsets
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostCommentsSerializer,
    CommentDetailSerializer,
    CommentChildSerializer
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


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentDetailSerializer


class CommentListView(generics.ListAPIView):
    serializer_class = PostCommentsSerializer

    def get_queryset(self):
        return Post.objects.find_by_id(pk=self.kwargs['pk'])


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer

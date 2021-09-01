from rest_framework import generics, viewsets
from .serializers import (
    PostUpdateSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)
from ..models import (
    Post,
    Comment
)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostUpdateSerializer


class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentUpdateSerializer


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = Post.objects.find_by_id(pk=self.kwargs['pk'])
        return Comment.objects.find_by_post(post)


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer

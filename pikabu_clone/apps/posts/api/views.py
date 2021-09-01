from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostSerializerWithoutAuthorField,
    CommentSerializer,
    CommentCreateSerializer,
    CommentSerializerWithOnlyBodyField
)
from ..models import (
    Post,
    Comment
)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializerWithoutAuthorField

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def get_serializer_class(self):
        """ Update only body field """
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = PostSerializerWithoutAuthorField

        return serializer_class


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        post_comments_ids = Post.objects.get_comments_pks(pk=self.kwargs['pk'])
        parent_id = request.data['parent']

        if int(parent_id) not in post_comments_ids:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={'message': 'this parent comment is not a comment on this post'}
            )

        return super(CommentCreateView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.find_by_id(pk=self.kwargs['pk'])
        )


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """ Get comments belongs to post with pk1 """
        post = Post.objects.find_by_id(pk=self.kwargs['pk'])
        return Comment.objects.find_by_post(post)


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        """ Get comments belongs to post with pk1 """
        post = Post.objects.find_by_id(pk=self.kwargs['pk1'])
        return Comment.objects.find_by_post(post)

    def get_serializer_class(self):
        """ Forbid updating author and parent fields """
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = CommentSerializerWithOnlyBodyField

        return serializer_class

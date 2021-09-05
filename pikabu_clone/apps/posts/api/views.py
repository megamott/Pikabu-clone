from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from pikabu_clone.apps.authentication.permissions import IsAuthorOrReadOnly

from .serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostSerializerWithoutUserField,
    CommentSerializer,
    CommentCreateSerializer,
    CommentSerializerWithOnlyTextField
)
from ..models import (
    Post,
    Comment
)
from ...core.class_utils import BaseView


class PostCreateView(BaseView, generics.CreateAPIView):
    serializer_class = PostSerializerWithoutUserField
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        """ Set user field from query parameters """
        serializer.save(user=self.request.user)


class PostsListView(BaseView, generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated,)


class PostDetailView(BaseView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        """ Update only body field """
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = PostSerializerWithoutUserField

        return serializer_class


class CommentCreateView(BaseView, generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        post_comments_ids = Post.objects.get_comments_pks(pk=self.kwargs['pk'])

        try:
            parent_id = request.data['parent']
            if int(parent_id) not in post_comments_ids:
                return Response(
                    status=HTTP_405_METHOD_NOT_ALLOWED,
                    data={
                        'message': 'this parent comment is not a comment on this post'
                    }
                )
        except MultiValueDictKeyError:  # when we create comment without parent
            pass

        return super(CommentCreateView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """ Set user and post fields from query parameters """
        serializer.save(
            user=self.request.user,
            post=Post.objects.find_by_id(pk=self.kwargs['pk'])
        )


class PostCommentListView(BaseView, generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Get comments belongs to post with pk1 """
        post = Post.objects.find_by_id(pk=self.kwargs['pk'])
        return Comment.objects.find_by_post(post)


class CommentDetailView(BaseView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        """ Get comments belongs to post with pk1 """
        post = Post.objects.find_by_id(pk=self.kwargs['pk1'])
        return Comment.objects.find_by_post(post).filter(deleted=False)

    def get_serializer_class(self):
        """ Forbid updating user and parent fields """
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = CommentSerializerWithOnlyTextField

        return serializer_class

    def perform_destroy(self, instance):
        """ Doesn't remove comment from database """
        instance.deleted = True
        instance.save()

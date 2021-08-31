from rest_framework import serializers
from ..models import (
    Post,
    Comment
)


class PostDetailSerializer(serializers.ModelSerializer):
    """ Serializer for POST, PUT, DELETE requests """
    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    """ Serializer for GET requests """
    author = serializers.CharField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'comments')

    @staticmethod
    def get_comments(obj):
        """ List of replies to these comment """
        return CommentDetailsSerializer(Comment.objects.find_by_post(obj), many=True).data


class CommentChildSerializer(serializers.ModelSerializer):
    """ Serializer to display parent comments """
    class Meta:
        model = Comment
        fields = ['body', 'author']


class CommentDetailsSerializer(serializers.ModelSerializer):
    """ Comment serializer for GET requests with nested comments"""
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['body', 'author', 'parent_comment', 'post', 'replies']

    @staticmethod
    def get_replies(obj):
        """ List of replies to these comment """
        if obj.is_parent:
            return CommentChildSerializer(
                Comment.objects.find_by_parent_comment(obj),
                many=True
            ).data
        return []

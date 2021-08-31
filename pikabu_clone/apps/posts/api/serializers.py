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
    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'comments')

    @staticmethod
    def get_author(obj):
        """ Get author username """
        return str(obj.author.username)

    @staticmethod
    def get_comments(obj):
        """ List of replies to these comment """
        return CommentDetailsSerializer(
            Comment.objects.find_by_post_with_nested_comments(obj),
            many=True
        ).data


class CommentDetailsSerializer(serializers.ModelSerializer):
    """ Comment serializer for GET requests with nested comments """

    class Meta:
        model = Comment
        fields = ['body', 'author', 'replies']


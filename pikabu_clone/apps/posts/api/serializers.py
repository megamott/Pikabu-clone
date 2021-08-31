from rest_framework import serializers
from ..models import (
    Post,
    Comment
)
from ...service.CommentUtils import find_ids_of_comments


class PostDetailSerializer(serializers.ModelSerializer):
    """ Serializer for POST, PUT, DELETE requests """

    class Meta:
        model = Post
        fields = '__all__'


class CommentDetailSerializer(serializers.ModelSerializer):
    """ Serializer for POST, PUT, DELETE requests """
    class Meta:
        model = Comment
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
        """ Get author username """
        ids = find_ids_of_comments([], obj.comments.all())
        return CommentChildSerializer(Comment.objects.find_by_ids(ids), many=True).data


class CommentChildSerializer(serializers.ModelSerializer):
    """ Comment serializer post GET request """

    class Meta:
        model = Comment
        fields = ('id', 'body', 'author', 'parent_comment')


class PostCommentsSerializer(serializers.ModelSerializer):
    """ Comments belonging to Post serializer """

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('comments',)

    @staticmethod
    def get_comments(obj):
        """ Get author username """
        ids = find_ids_of_comments([], obj.comments.all())
        return CommentChildSerializer(Comment.objects.find_by_ids(ids), many=True).data

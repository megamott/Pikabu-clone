from rest_framework import serializers
from ..models import (
    Post,
    Comment
)


class PostUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for POST, PUT, DELETE requests """

    class Meta:
        model = Post
        fields = '__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for POST requests """

    class Meta:
        model = Comment
        fields = '__all__'


class RecursiveSerializer(serializers.Serializer):
    """ Output children recursively """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCommentListSerializer(serializers.ListSerializer):
    """ Output only parent comments """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    """ Comments belongs to Post serializer """

    comment_children = RecursiveSerializer(many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ('id', 'author', 'body', 'post', 'parent', 'created_date', 'comment_children')

    @staticmethod
    def get_author(obj):
        """ Get author username """
        return str(obj.author.username)


class PostDetailSerializer(serializers.ModelSerializer):
    """ Serializer for GET requests """
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'comments')

    @staticmethod
    def get_author(obj):
        """ Get author username """
        return str(obj.author.username)

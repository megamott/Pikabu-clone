from rest_framework import serializers
from ..models import (
    Post,
    Comment
)


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'comments')


class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'author']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentDetailsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['body', 'author', 'parent_comment', 'post', 'replies']

    @staticmethod
    def get_replies(obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return []

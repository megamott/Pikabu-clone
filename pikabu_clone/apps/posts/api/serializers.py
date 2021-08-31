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


class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'







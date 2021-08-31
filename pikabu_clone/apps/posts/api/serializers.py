from rest_framework import serializers
from ..models import Post


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author')






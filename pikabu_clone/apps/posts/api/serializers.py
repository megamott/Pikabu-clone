from rest_framework import serializers
from ..models import (
    Post,
    Comment
)


class PostCreateSerializer(serializers.ModelSerializer):
    """ Serializer for POST, PUT, DELETE requests """

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializerWithoutUserField(serializers.ModelSerializer):
    """ Serializer for PUT requests """

    class Meta:
        model = Post
        exclude = ('user',)


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Serializer for POST requests """

    class Meta:
        model = Comment
        exclude = ('user', 'post')


class CommentSerializerWithOnlyTextField(serializers.ModelSerializer):
    """ Serializer for PUT requests """

    class Meta:
        model = Comment
        fields = ('text',)


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
    user = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = (
            'id',
            'user',
            'text',
            'post',
            'parent',
            'created_date',
            'deleted',
            'comment_children'
        )

    @staticmethod
    def get_user(obj):
        """ Get user username """
        return str(obj.user.username)

    @staticmethod
    def get_text(obj):
        if obj.deleted:
            return None
        return obj.text


class PostDetailSerializer(serializers.ModelSerializer):
    """ Serializer for GET requests """
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'user', 'comments')

    @staticmethod
    def get_user(obj):
        """ Get user username """
        return str(obj.user.username)

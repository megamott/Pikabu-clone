from django.contrib import admin
from .models import (
    Post,
    Comment
)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'body', 'author', 'timestamp')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'author', 'content_type', 'object_id', 'timestamp')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

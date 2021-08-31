from django.contrib import admin
from .models import (
    Post,
    Comment
)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'body', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'author', 'post', 'parent_comment')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

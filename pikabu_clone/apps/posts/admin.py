from django.contrib import admin
from .models import (
    Post,
    Comment
)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'body', 'user', 'created_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'parent', 'created_date', 'deleted')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

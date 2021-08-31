from django.contrib import admin
from .models import (
    Post,
)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'body', 'author')


admin.site.register(Post, PostAdmin)

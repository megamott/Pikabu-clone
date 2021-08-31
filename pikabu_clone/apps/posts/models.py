from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """ Post in Pikabu-clone app """

    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    body = models.TextField(verbose_name='main post text')
    title = models.CharField(
        max_length=50,
        verbose_name='title describing the essence of the post'
    )
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='which user the post belongs to'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'Posts'

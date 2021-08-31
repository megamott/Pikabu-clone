from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

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
    timestamp = models.DateTimeField(auto_now=True, verbose_name='date of post creation')
    comments = GenericRelation('comment')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    """ Comment under the post """

    body = models.TextField(verbose_name='main comment text')
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='which user the post belongs to'
    )
    parent_comment = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE,
        verbose_name='parent comment which the comment belongs to'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now=True, verbose_name='date of comment creation')
    is_child = models.BooleanField(default=True, verbose_name='is it child comment?')

    def __str__(self):
        return f'{self.body}: {self.author}'

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'


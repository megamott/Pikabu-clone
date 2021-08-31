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
    comments = GenericRelation('comment')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'Posts'


class CommentManager(models.Manager):
    """ Manager for Comment model """

    def get_queryset(self):
        """ Override get_queryset method from BaseManager """
        return super().get_queryset()

    def find_by_post(self, post):
        """ Retrieve comments by post """
        return self.get_queryset().filter(post=post)

    def find_by_post_with_nested_comments(self, post):
        """
        Retrieve comments by post
        If the comment is nested, then it will be displayed at the nested level
        """
        return self.find_by_post(post).filter(post=post, parent_comment=None)

    def find_parent_comments(self):
        return self.get_queryset().filter(parent_comment=None)

    def find_by_parent_comment(self, parent_comment):
        """ Get children of comment """
        return self.get_queryset().filter(parent_comment=parent_comment)


class Comment(models.Model):
    """ Comment under the post """

    body = models.TextField(verbose_name='main comment text')
    author = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='which user the post belongs to'
    )
    post = models.ForeignKey(
        Post,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='which post the comment belongs to'
    )
    parent_comment = models.ForeignKey(
        'self',
        related_name='comment_children',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='parent comment, to achieve tree comments behavior'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    objects = CommentManager()

    def __str__(self):
        return f'{self.body}: {self.post} by {self.author}'

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'

    @property
    def is_parent(self):
        """ Determines if a comment is a parent """
        if self.parent_comment is None:
            return True
        return False

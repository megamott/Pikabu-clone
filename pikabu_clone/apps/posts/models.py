from django.contrib.auth import get_user_model
from mptt.models import TreeForeignKey, MPTTModel
from django.db import models

User = get_user_model()


class PostManager(models.Manager):
    """ Manager for Comment model """

    def get_queryset(self):
        """ Override get_queryset method from BaseManager """
        return super().get_queryset()

    def find_by_id(self, pk):
        """ Retrieve comments by id """
        return self.get_queryset().filter(pk=pk).first()

    def get_comments(self):
        """ Get parent comments related to this post """
        return self.comments.filter(parent=None)

    def get_comments_pks(self, pk):
        """ Get ids of nested comments """
        return list(
            map(
                lambda a: a.pk,
                list(self.find_by_id(pk=pk).comments.all())
            )
        )


class Post(models.Model):
    """ Post in Pikabu-clone app """

    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    body = models.TextField(verbose_name='main post text')
    title = models.CharField(
        max_length=50,
        verbose_name='title describing the essence of the post'
    )
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='which user the post belongs to'
    )
    created_date = models.DateTimeField(
        auto_now=True,
        verbose_name='date of post creation'
    )

    objects = PostManager()

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
        """ Find comments related to post"""
        return self.get_queryset().filter(post=post)


class Comment(MPTTModel):
    """ Comment under the post """

    text = models.TextField(verbose_name='main comment text')
    user = models.ForeignKey(
        User,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='which user the post belongs to'
    )
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="post the comment belongs to",
    )
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.SET_NULL,
        verbose_name='parent comment which the comment belongs to'
    )
    created_date = models.DateTimeField(
        auto_now=True,
        verbose_name='date of comment creation'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name='has this comment been deleted?'
    )

    objects = CommentManager()

    def __str__(self):
        return f'{self.text}: {self.user}'

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'

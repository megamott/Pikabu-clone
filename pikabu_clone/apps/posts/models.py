from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

User = get_user_model()


class PostManager(models.Manager):
    """ Manager for Comment model """

    def get_queryset(self):
        """ Override get_queryset method from BaseManager """
        return super().get_queryset()

    def find_by_id(self, pk):
        """ Retrieve comments by id """
        return self.get_queryset().filter(pk=pk)


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

    def find_by_instance(self, instance):
        """ Retrieve comments by instance """
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(CommentManager, self).filter(
            content_type=content_type,
            object_id=object_id
        )


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
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='type of parent object'
    )
    object_id = models.PositiveIntegerField(verbose_name='parent object id')
    timestamp = models.DateTimeField(auto_now=True, verbose_name='date of comment creation')

    objects = CommentManager()

    def __str__(self):
        return f'{self.body}: {self.author}'

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'

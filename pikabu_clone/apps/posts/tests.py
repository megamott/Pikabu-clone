from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from pikabu_clone.apps.posts.models import (
    Post,
    Comment
)

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        # Create user and token
        user = User.objects.create_user({
            'email': 'mail@mail.ru',
            'username': 'username',
            'password': 'password'
        })
        user2 = User.objects.create_user({
            'email': 'gmail@gmail.com',
            'username': 'username2',
            'password': 'password2'
        })
        self.token = Token.objects.create(user=user)
        self.token_user2 = Token.objects.create(user=user2)

        # Create Posts and Comments models
        self.post = Post.objects.create(slug='slug', body='body', title='title', user=user)
        self.post2 = Post.objects.create(slug='slug1', body='body1', title='title1', user=user)
        self.comment = Comment.objects.create(text='text', user=user, post=self.post)
        Comment.objects.create(
            text='text',
            user=user,
            post=self.post,
            parent=Comment.objects.first()
        )
        self.comment2 = Comment.objects.create(
            text='text',
            user=user,
            post=self.post2,
        )
        self.deleted_comment = Comment.objects.create(
            text='text',
            user=user,
            post=self.post,
            parent=Comment.objects.first(),
            deleted=True
        )

        # Data for Post creation
        self.post_data = {
            'slug': 'some_slug',
            'body': 'some_body',
            'title': 'some_title'
        }

        # Data for Post update
        self.post_update_data = {
            'slug': 'some_up_slug',
            'body': 'some_up_body',
            'title': 'some_up_title'
        }

        # Data for parent Comment creation
        self.comment_data = {
            'text': 'some_text',
        }

        # Data for Comment with parent creation
        self.comment_with_parent_data = {
            'text': 'some_text',
            'parent': self.comment.pk
        }

        # Data for Comment update
        self.comment_update_data = {
            'text': 'updated_text',
        }

    def test_post_list(self):
        """ Test post list GET query """
        url = reverse('post:list-posts')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(response.data[0]['comments']), 1)

    def test_fail_post_list_without_auth(self):
        """ Test post comments list GET query without Token authorisation """
        url = reverse('post:post-comments', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_post_detail(self):
        """ Test for retrieving non existing post """
        url = reverse('post:post-detail', kwargs={'pk': 100})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_detail(self):
        """ Test for retrieving existing post """
        url = reverse('post:post-detail', kwargs={'pk': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), 'title')

    def test_create_invalid_post(self):
        """ Test for create post without authentication """
        url = reverse('post:create-post')
        response = self.client.post(url, data=self.post_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post(self):
        """ Test for create post """
        url = reverse('post:create-post')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data=self.post_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_update_post(self):
        """ Test update fields in post from not author user """
        url = reverse('post:post-detail', kwargs={'pk': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)
        response = self.client.put(url, data=self.post_update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post(self):
        """ Test update fields in post """
        url = reverse('post:post-detail', kwargs={'pk': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, data=self.post_update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('body'), self.post_update_data['body'])

    def test_fail_comment_detail(self):
        """ Test for retrieving comment belonging to the other post """
        url = reverse('post:comment-detail', kwargs={'pk': self.post.id, 'pk1': self.comment2.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_invalid_comment(self):
        """ Test for create comment without authentication """
        url = reverse('post:create-comment', kwargs={'pk': self.post.id})
        response = self.client.post(url, data=self.comment_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_without_parent_comment(self):
        """ Test for create parent comment """
        url = reverse('post:create-comment', kwargs={'pk': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data=self.comment_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_parent_comment(self):
        """ Test for create comment with parent """
        url = reverse('post:create-comment', kwargs={'pk': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data=self.comment_with_parent_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_comment_from_other_post(self):
        """ Test for create comment with parent """
        url = reverse('post:create-comment', kwargs={'pk': self.post2.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data=self.comment_with_parent_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invalid_update_comment(self):
        """ Test update fields in comment from not author user """
        url = reverse('post:comment-detail', kwargs={'pk1': self.post.id, 'pk': self.comment.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)
        response = self.client.put(url, data=self.comment_update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment(self):
        """ Test update 'text' field in comment """
        url = reverse('post:comment-detail', kwargs={'pk1': self.post.id, 'pk': self.comment.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, data=self.comment_update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('text'), self.comment_update_data['text'])

    def test_update_invalid_comment(self):
        """ Test for update comment without authentication """
        url = reverse('post:comment-detail', kwargs={'pk1': self.post.id, 'pk': self.comment.id})
        response = self.client.put(url, data=self.comment_update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_deleted_comment(self):
        """ Test for view of deleted comment """
        url = reverse('post:post-comments', kwargs={'pk': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['comment_children'][1]['deleted'])
        self.assertIsNone(response.data[0]['comment_children'][1]['text'])

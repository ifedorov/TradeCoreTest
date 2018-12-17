from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from tradetestapp.models import Post, Like


class SimpleTest(TestCase):
    fixtures = ['test-data.json']

    def setUp(self):
        self.api_client = APIClient()

    def test_post_create(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.post('/v1/post/',
                                        data={'content': "text"})
        self.assertEqual(response.status_code, 201)

    def test_post_create_unauth_error(self):
        response = self.api_client.post('/v1/post/',
                                        data={'content': "text"})
        self.assertEqual(response.status_code, 401)

    def test_post_like(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.get('/v1/post/1/like/')
        self.assertEqual(response.status_code, 201)

    def test_post_like_db(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        self.assertFalse(
            Like.objects.all().exists()
        )
        response = self.api_client.get('/v1/post/1/like/')
        like = Like.objects.get(post=1, user=user)
        self.assertEqual(response.status_code, 201)
        like.refresh_from_db()
        self.assertTrue(like.is_like)

    def test_post_unlike_to_like(self):
        user = User.objects.get(username='testuser')
        post = Post.objects.get(pk=1)
        self.api_client.force_authenticate(user=user)
        self.assertFalse(
            Like.objects.all().exists()
        )
        like, _ = Like.objects.update_or_create(
            post=post,
            user=user,
            defaults={
                'is_like': False
            }
        )
        self.assertFalse(like.is_like)
        response = self.api_client.get('/v1/post/1/like/')
        self.assertEqual(response.status_code, 201)
        like.refresh_from_db()
        self.assertTrue(like.is_like)

    def test_post_like_wrong_method(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.post('/v1/post/1/like/')
        self.assertEqual(response.status_code, 400)

    def test_post_like_unauth_error(self):
        response = self.api_client.get('/v1/post/1/like/')
        self.assertEqual(response.status_code, 401)

    def test_post_unlike(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.get(
            '/v1/post/1/unlike/')
        self.assertEqual(response.status_code, 201)

    def test_post_like_to_unlike(self):
        user = User.objects.get(username='testuser')
        post = Post.objects.get(pk=1)
        self.api_client.force_authenticate(user=user)
        self.assertFalse(
            Like.objects.all().exists()
        )
        like, _ = Like.objects.update_or_create(
            post=post,
            user=user,
            defaults={
                'is_like': True
            }
        )
        self.assertTrue(like.is_like)
        response = self.api_client.get('/v1/post/1/unlike/')
        self.assertEqual(response.status_code, 201)
        like.refresh_from_db()
        self.assertFalse(like.is_like)

    def test_post_unlike_db(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.get('/v1/post/1/unlike/')
        self.assertEqual(response.status_code, 201)
        like = Like.objects.get(post__pk=1, user=user)
        self.assertFalse(like.is_like)

    def test_post_unlike_wrong_method(self):
        user = User.objects.get(username='testuser')
        self.api_client.force_authenticate(user=user)
        response = self.api_client.post(
            '/v1/post/1/unlike/')
        self.assertEqual(response.status_code, 400)

    def test_post_unlike_unauth_error(self):
        response = self.api_client.get(
            '/v1/post/1/unlike/')
        self.assertEqual(response.status_code, 401)

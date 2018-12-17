from django.test import TestCase, override_settings
from rest_framework.test import APIClient


class SimpleTest(TestCase):
    fixtures = ['test-data.json']

    def setUp(self):
        self.api_client = APIClient()

    def test_login_success(self):
        response = self.api_client.post(
            '/v1/user/login/',
            data={'username': 'testuser',
                  'password': 'aNe9Q!ih#*'}
        )
        self.assertIn('token', response.data)

    def test_login_incorrect_password(self):
        response = self.api_client.post(
            '/v1/user/login/',
            data={'username': 'testuser',
                  'password': 'wrong_password'}
        )
        self.assertEqual(
            response.data,
            {
                'non_field_errors': [
                    'Unable to log in with provided credentials.'
                ]
            }
        )

    def test_login_incorrect_username(self):
        response = self.api_client.post(
            '/v1/user/login/',
            data={'username': 'not exists',
                  'password': 'wrong_password'}
        )
        self.assertEqual(
            response.data,
            {
                'non_field_errors':
                    [
                        'Unable to log in with provided credentials.'
                    ]
            }
        )

    def test_login_no_password(self):
        response = self.api_client.post(
            '/v1/user/login/',
            data={'username': 'testuser'}
        )
        self.assertEqual(
            response.data,
            {'password': ['This field is required.']}
        )

    def test_login_no_username(self):

        response = self.api_client.post(
            '/v1/user/login/',
            data={'password': 'aNe9Q!ih#*'}
        )
        self.assertEqual(
            response.data,
            {'username': ['This field is required.']}
        )

    def test_signup_success(self):
        response = self.api_client.post(
            '/v1/user/signup/',
            data={'username': 'test_signup',
                  'email': 'dont@mail.me',
                  'password': '1'}
        )
        self.assertIn('username', response.data)
        self.assertEqual(response.status_code, 201)

    @override_settings(HUNTER_ENABLE=True)
    def test_signup_wrong_email(self):
        response = self.api_client.post(
            '/v1/user/signup/',
            data={'username': 'test_signup',
                  'email': '1',
                  'password': '1'}
        )
        self.assertEqual({'email': ['The verified email is invalid.']},
                         response.data)
        self.assertEqual(response.status_code, 400)

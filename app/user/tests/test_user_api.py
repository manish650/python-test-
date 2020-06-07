from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user api public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test create user with valid payload is successfull"""
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """User creation fail to test user alredy exits"""
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short(self):
        """Password must be greater than 5 charector"""
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': 'te'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """create a token for user"""
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Token is not created if credential is invalid"""
        create_user(email='manishmishra650@gmail.com', password='testpass')
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': 'test123'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('tpokem', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_notexist_user(self):
        """create should note created for not exist user"""
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': 'testpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_feild(self):
        """test case if feild is missed so ticket should not create"""
        create_user(email='manishmishra650@gmail.com', password='testpass')
        payload = {
            'email': 'manishmishra650@gmail.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthrize(self):
        """authentication is required for manage the user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTets(TestCase):
    """Test api that required authentication"""

    def setUp(self):
        self.user = create_user(
            email='manishmishra650@gmail.com',
            password='testpass',
            name='manish'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test for retriving the profile for login user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_not_allow(self):
        """Post method not allowed for retreving the profile"""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """we are going to test the update profile authenticated user"""
        payload = {
            'name': 'new name',
            'password': 'test123'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

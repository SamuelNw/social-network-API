"""
Tests for the user API.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    """Create a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tests for the public endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_user_creation_success(self):
        """Test create new user success."""
        payload = {
            "email": "user@example.com",
            "password": "changeme",
            "name": "Test User"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_already_exists(self):
        """Test users are unique."""
        payload = {
            "email": "user@example.com",
            "password": "changeme",
            "name": "Test User"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test passwords are longer than 5 chars."""
        payload = {
            "email": "user@example.com",
            "password": "pw",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()

        self.assertFalse(user_exists)

    def test_token_creation_for_valid_entries(self):
        """Test creating tokens for valid entries is successful."""
        user_details = {
            "email": "user@example.com",
            "password": "testpass123",
            "name": "Test Name"
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"]
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_no_token_created_for_invalid_entries(self):
        """Test no token created if details are wrong."""
        user_details = {
            "email": "user@example.com",
            "password": "testpass123",
            "name": "Test Name"
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": "wrongpassword"
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_no_token_created_for_blank_password(self):
        """Test that no creation of tokens for blank password."""
        user_details = {
            "email": "user@example.com",
            "password": "testpass123",
            "name": "Test Name"
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": ""
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_user_data_fetch_requires_authentication(self):
        """Test unauthorized requests to get user data fails."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Tests for endpoints that require authentication."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com",
            password="testpassword123",
            name="Test User"
        )
        self.client.force_authenticate(user=self.user)

    def test_authorized_requests_success(self):
        """Test authorized fetch requests are a success."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "email": self.user.email,
            "name": self.user.name
        })

    def test_updating_user_details_success(self):
        """Test that updating user data is a success."""
        payload = {
            "name": "Updated Name",
            "password": "Changed_Password"
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_unallowed_methods(self):
        """Test POST methods are denied."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

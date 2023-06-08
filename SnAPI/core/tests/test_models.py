from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests for the Models."""

    def test_create_user_with_email_successful(self):
        """Test user account creation with email works."""

        email = "test@example.com"
        password = "changeme"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_emails_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for sample, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=sample,
                password="changeme"
            )
            self.assertEqual(user.email, expected)

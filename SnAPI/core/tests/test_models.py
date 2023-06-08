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
        """Test that user emails are stored as needed."""
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

    def test_user_email_required(self):
        """Test that a value error is thrown when an email is not provided."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpassword123")

    def test_create_superusers(self):
        """Test the creation of superusers."""
        super_user = get_user_model().objects.create_superuser(
            email="test@example.com", password="testpass123")

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)

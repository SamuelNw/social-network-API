"""
User API Views.
"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)


class CreateUserAPIView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class GenerateTokenAPIView(ObtainAuthToken):
    """Generate auth tokens for users."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

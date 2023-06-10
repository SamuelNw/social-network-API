"""
User API urls.
"""

from django.urls import path

from .views import (
    CreateUserAPIView,
    GenerateTokenAPIView
)


app_name = "user"

urlpatterns = [
    path("create/", CreateUserAPIView.as_view(), name="create"),
    path("token/", GenerateTokenAPIView.as_view(), name="token"),
]

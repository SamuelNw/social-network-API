"""
User API urls.
"""

from django.urls import path

from .views import (
    CreateUserAPIView,
    GenerateTokenAPIView,
    ManageUserAPIView
)


app_name = "user"

urlpatterns = [
    path("create/", CreateUserAPIView.as_view(), name="create"),
    path("token/", GenerateTokenAPIView.as_view(), name="token"),
    path("me/", ManageUserAPIView.as_view(), name="me"),
]

"""
User API urls.
"""

from django.urls import path

from .views import (
    CreateUserAPIView,
    AuthTokenAPIView
)


app_name = "user"

urlpatterns = [
    path("create/", CreateUserAPIView.as_view(), name="create"),
    path("token/", AuthTokenAPIView.as_view(), name="token"),
]

"""
User API urls.
"""

from django.urls import path

from views import CreateUserAPIView


app_name = "user"

urlpatterns = [
    path("create/", CreateUserAPIView.as_view(), name="create")
]

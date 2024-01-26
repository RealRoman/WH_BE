from django.urls import path, include
from .views import (
    UserList
)

urlpatterns = [
    path('users/', UserList.as_view()),
]

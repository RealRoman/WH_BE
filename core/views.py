from rest_framework.views import APIView
from .serializers import (
    TokenSerializer,
    UserSerializer,
)
from .models import (
    User
)
from rest_framework import mixins
from rest_framework import generics


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

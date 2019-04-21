import logging

from rest_framework import generics, filters, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer, CreateUserSerializer
from api.utils.permissions import IsUser, IsAuthenticated

logger = logging.getLogger(__name__)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CreateUserView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.create(serializer.validated_data)

            return Response({'username': user.username},
                            status=status.HTTP_201_CREATED)


class UserViewSet(generics.GenericAPIView):

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permission() for permission in [IsAuthenticated, IsUser]]
        else:
            return []

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('Username not found')

        self.check_object_permissions(self.request, user)
        return user

    def get(self, request, username=None, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Username not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response({'user': serializer.data},
                        status=status.HTTP_200_OK)

    def delete(self, request, username=None, *args, **kwargs):
        user = self.get_user(username=username)

        password = request.POST.get('password')
        if not password:
            return Response({'error': 'Password is not specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        check = User.delete_user(user, password)
        if not check:
            return Response({'error': 'Password is not correct'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'username': username}, status=status.HTTP_200_OK)

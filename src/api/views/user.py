import logging

from rest_framework import generics, filters, status
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer, NewUserSerializer, FollowSerializer

logger = logging.getLogger(__name__)


class UserViews(generics.GenericAPIView):

    @staticmethod
    def delete(request, username):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Username not found'},
                            status=status.HTTP_404_NOT_FOUND)

        password = request.POST.get('password')
        if not password:
            return Response({'error': 'Password is not specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        check = User.delete_user(user, password)
        if not check:
            return Response({'error': 'Password is not correct'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'username': username}, status=status.HTTP_200_OK)

    @staticmethod
    def get(request, username=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Username not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response({'user': serializer.data},
                        status=status.HTTP_200_OK)


class UserCreateView(generics.GenericAPIView):

    @staticmethod
    def post(request):
        serializer = NewUserSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.create(serializer.validated_data)

            return Response({'username': user.username},
                            status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class FollowViews(generics.GenericAPIView):
    @staticmethod
    def post(request, username=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': f'Username {username} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        target = request.POST.get('target')
        if not target:
            return Response({'error': 'Target parameter is not specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(username=target)
        except User.DoesNotExist:
            return Response({'error': f'Target {target} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        if user.is_following(target_user):
            return Response({'error': f'User {username} is already following {target}'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.follow(target_user)

        return Response({'username': username, 'target': target},
                        status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': f'Username {username} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        target = request.POST.get('target')
        if not target:
            return Response({'error': 'Target parameter is not specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(username=target)
        except User.DoesNotExist:
            return Response({'error': f'Target {target} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        if not user.is_following(target_user):
            return Response({'error': f'User {username} is not following {target} yew'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.unfollow(target_user)
        return Response({'username': username, 'target': target},
                        status=status.HTTP_200_OK)

    @staticmethod
    def get(request, username):
        user = User.objects.get(username=username)
        serializer = FollowSerializer(user.followers, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

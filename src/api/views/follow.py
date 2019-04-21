import logging

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.models import User
from api.serializers import FollowerSerializer
from api.utils.permissions import IsUser, IsAuthenticated

logger = logging.getLogger(__name__)


class FollowViews(generics.GenericAPIView):
    serializer_class = FollowerSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
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

    def post(self, request, username=None, *args, **kwargs):
        user = self.get_user(username=username)

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

    def delete(self, request, username, *args, **kwargs):
        user = self.get_user(username=username)

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

    def get(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)

        queryset = user.followers.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

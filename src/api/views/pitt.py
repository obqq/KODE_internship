import logging

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.models import User, Pitt
from api.serializers import PittSerializer
from api.utils.permissions import IsUser, IsAuthenticated

logger = logging.getLogger(__name__)


class PittListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = PittSerializer

    def get(self, request, username, *args, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('Username not found')

        self.check_object_permissions(self.request, user)

        targets = [target.target for target in user.targets.all()]
        queryset = Pitt.objects.filter(user__in=targets).order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class PittViewSet(generics.GenericAPIView):
    serializer_class = PittSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'POST']:
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

        request.data.update({'user': user.user_id})

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        pitt = user.create_pitt(**serializer.validated_data)

        return Response({'pitt_id': pitt.pitt_id},
                        status=status.HTTP_201_CREATED)

    def delete(self, request, username=None, pitt_id=None, *args, **kwargs):
        user = self.get_user(username=username)

        try:
            user.delete_pitt(pitt_id)
        except Pitt.DoesNotExist:
            return Response({'error': f'Pitt {pitt_id} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'username': username, 'pitt_id': pitt_id},
                        status=status.HTTP_200_OK)

    def get(self, request, username, *args, **kwargs):

        user = User.objects.get(username=username)

        queryset = user.pitts.order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

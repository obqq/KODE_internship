import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import UserSerializer
from api.models import User

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.create(serializer.validated_data)

            return Response({'username': user.username}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):

        try:
            user = User.objects.get(username=pk)
        except Exception as e:
            print(e)
            return Response({'error': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)

        password = request.POST.get('password')
        if not password:
            return Response({'error': 'Password is not specified'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            check = User.objects.delete_user(user, password)
        except Exception as e:
            logger.error(e)
            return Response(
                {'error': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not check:
            return Response({'error': 'Password is not correct'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'username': pk}, status=status.HTTP_200_OK)

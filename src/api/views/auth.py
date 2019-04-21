import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.utils.access_token import generate_token, decode_token

logger = logging.getLogger(__name__)


class PublicKeyView(APIView):

    def get(self, request):
        with open(settings.API_PUBLIC_KEY_PATH) as f:
            public_key = f.read()

        return Response({'public_key': public_key}, status=status.HTTP_200_OK)


class AccessTokenView(APIView):

    def get(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({'error': 'Username is not specified'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'error': 'Password is not specified'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Password is not correct'}, status=status.HTTP_400_BAD_REQUEST)

        token = generate_token(username)

        return Response(token, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Refresh token is not specified'}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = auth_header[7:]

        try:
            token = decode_token(refresh_token)
            token['refresh_token']
        except KeyError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        token = generate_token(token.get('username'))

        return Response(token, status=status.HTTP_200_OK)

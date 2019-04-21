import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api.utils.access_token import decode_token


class IsAuthenticated(BaseAuthentication):
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise AuthenticationFailed('Invalid token type specified')

        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Access token is not specified')

        access_token = auth_header[7:]

        try:
            request.token = decode_token(access_token)
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid access token')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired')

        return True

    def has_object_permission(self, request, view, user):
        return True


class IsUser(BaseAuthentication):
    def has_permission(self, request, view):
        if not request.token:
            raise AuthenticationFailed('Access token is not specified')
        return True

    def has_object_permission(self, request, view, user):
        if user.username != request.token.get('username'):
            raise AuthenticationFailed('You don\'t have permission to perform this action.')
        else:
            return True

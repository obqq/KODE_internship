from datetime import datetime, timedelta

import jwt
from django.conf import settings


def decode_token(token):
    data = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
    return data


def generate_token(username):
    expire_seconds = settings.JWT_REFRESH_EXPIRATION_DELTA

    expires = datetime.now() + timedelta(seconds=expire_seconds)
    payload = {'username': username, 'exp': expires.timestamp()}
    access_token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)
    payload.update({'refresh_token': True})
    refresh_token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)

    token = {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': expire_seconds,
        'refresh_token': refresh_token
    }

    return token

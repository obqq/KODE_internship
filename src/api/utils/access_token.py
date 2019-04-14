import jwt
from datetime import datetime, timedelta

from django.conf import settings


def decode_token(token):
    with open(settings.API_PUBLIC_KEY_PATH) as f:
        public_key = f.read()
    data = jwt.decode(token, public_key, algorithms=['RS256'])

    return data


def generate_token(username):
    expire_seconds = settings.ACCESS_TOKEN_EXPIRE_SECONDS

    with open(settings.API_PRIVATE_KEY_PATH) as f:
        private_key = f.read()

    expires = datetime.now() + timedelta(seconds=expire_seconds)
    payload = {'username': username, 'expires': expires.timestamp()}
    access_token = jwt.encode(payload, private_key, algorithm='RS256')
    payload.update({'refresh_token': True})
    refresh_token = jwt.encode(payload, private_key, algorithm='RS256')

    token = {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': expire_seconds,
        'refresh_token': refresh_token
    }

    return token

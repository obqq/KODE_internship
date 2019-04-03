import json
from datetime import datetime

from django import http
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rmr.types import JsonDict


class RequestDecoder:
    content_type = 'application/json'

    allowed_methods = {
        'POST', 'PUT', 'PATCH',
    }

    def process_request(self, request):
        date = request.META.get('HTTP_DATE')
        if date:
            request.client_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        else:
            request.client_date = None

        if request.method not in self.allowed_methods:
            return
        content_type = request.META.get('CONTENT_TYPE', '')

        if not content_type.startswith(self.content_type):
            return
        encoding = request.encoding or settings.DEFAULT_CHARSET
        try:
            body = request.body.decode(encoding=encoding)
        except UnicodeDecodeError:
            return http.HttpResponseBadRequest('bad unicode')
        try:
            request.POST = self.json_decode(body)
        except ValueError:
            pass

    @staticmethod
    def json_decode(body):
        data = json.loads(body)
        if not isinstance(data, dict):
            # all data of type other then dict will be returned as is
            return data
        return JsonDict(data)


class BaseAppRequestDecoder(MiddlewareMixin, RequestDecoder):
    pass

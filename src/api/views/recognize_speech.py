import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.integrations.speech_to_text import GoogleSpeechToTextAPI
from api.serializers import SpeechSerializer

logger = logging.getLogger(__name__)

FILE_MAX_SIZE = 1024 * 1024 * 10


class RecognizeSpeech(APIView):

    def post(self, request):
        serializer = SpeechSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        request_data = request.POST
        audiofile = request.FILES.get('file')

        encoding = request_data.get('encoding')
        sample_rate_hertz = request_data.get('sampleRateHertz')
        language_code = request_data.get('languageCode')

        if not audiofile:
            return Response(
                {'error': 'Audio file was not specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not audiofile.size > FILE_MAX_SIZE:
            return Response(
                {'error': "Audio file size exceeds the maximum size limit of 10 MB."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if audiofile:
            try:
                API = GoogleSpeechToTextAPI()
                response = API.recognize(audiofile, encoding, sample_rate_hertz, language_code)
            except Exception as e:
                logger.error(e)
                return Response(
                    {'error': 'Something went wrong. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            error = response.get('error')
            if error:
                return Response(
                    {'error': error.get('message')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            results = response.get('results')

            return dict(
                transcript='\n'.join([result['alternatives'][0]['transcript'] for result in results])
            )

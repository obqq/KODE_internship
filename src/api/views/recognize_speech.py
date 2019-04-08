import logging
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import SpeechSerializer
from api.integrations.speech_to_text import GoogleSpeechToTextAPI

logger = logging.getLogger(__name__)


FILE_MAX_SIZE = 1024 * 1024 * 10


class RecognizeSpeech(APIView):

	def post(self, request):
		serializer = SpeechSerializer(data=request.POST)
		if not serializer.is_valid():
			return Response(
				{'error': serializer.errors},
				status=400
			)

		request_data = request.POST
		audiofile = request.FILES.get('file')

		encoding = request_data.get('encoding')
		sample_rate_hertz = request_data.get('sampleRateHertz')
		language_code = request_data.get('languageCode')

		if not audiofile:
			return Response(
				{'error': 'Audio file was not specified.'},
				status=400
			)

		if not audiofile.size > FILE_MAX_SIZE:
			return Response(
				{'error': "Audio file size exceeds the maximum size limit of 10 MB."},
				status=400
			)

		if audiofile:
			try:
				API = GoogleSpeechToTextAPI()
				response = API.recognize(audiofile, encoding, sample_rate_hertz, language_code)
			except Exception as e:
				logger.error(e)
				return Response(
					{'error': 'Something went wrong. Please try again later.'},
					status=500
				)

			error = response.get('error')
			if error:
				return Response(
					{'error': error.get('message')},
					status=400
				)

			results = response.get('results')

			return dict(
				transcript='\n'.join([result['alternatives'][0]['transcript'] for result in results])
			)


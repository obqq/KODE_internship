import logging
from django.http import JsonResponse

from base_app.utils.json import Json
from base_app.serializers import SpeechSerializer
from base_app.integrations.speech_to_text import GoogleSpeechToTextAPI

logger = logging.getLogger(__name__)


class RecognizeSpeech(Json):

	def post(self, request):
		serializer = SpeechSerializer(data=request.POST)
		if not serializer.is_valid():
			return JsonResponse(
				{'error': serializer.errors},
				status=400
			)

		request_data = request.POST
		audiofile = request.FILES.get('file')

		encoding = request_data.get('encoding')
		sampleRateHertz = request_data.get('sampleRateHertz')
		languageCode = request_data.get('languageCode')


		if audiofile is not None:
			try:
				API = GoogleSpeechToTextAPI()
				response = API.recognize(audiofile, encoding, sampleRateHertz, languageCode)
			except Exception as e:
				logger.error(e)
				return JsonResponse(
					{'error': 'Something went wrong. Please try again later.'},
					status=500
				)

			error = response.get('error')
			if error is not None:
				return JsonResponse(
					{'error': error.get('message')},
					status=400
				)

			results = response.get('results')

			return dict(
				transcript='\n'.join([result['alternatives'][0]['transcript'] for result in results])
			)

		return JsonResponse(
				{'error': 'Audio file was not specified.'},
				status=400
			)

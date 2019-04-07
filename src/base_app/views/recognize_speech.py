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
				{'message': serializer.errors},
				status=400
			)

		request_data = request.POST
		audiofile = request.FILES.get('file')

		encoding = request_data.get('encoding')
		sampleRateHertz = request_data.get('sampleRateHertz')
		languageCode = request_data.get('languageCode')


		if audiofile is not None:
			API = GoogleSpeechToTextAPI()
			response = API.recognize(audiofile, encoding, sampleRateHertz, languageCode)

			error = response.get('error')
			if error is not None:
				return JsonResponse(
					{'message': error.get('message')},
					status=400
				)

			results = response.get('results')

			return dict(
				transcript='\n'.join([result['alternatives'][0]['transcript'] for result in results])
			)

		return JsonResponse(
				{'message': 'Audio file was not specified.'},
				status=400
			)

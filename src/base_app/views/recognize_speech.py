import logging
from django.http import JsonResponse

from base_app.utils.json import Json

logger = logging.getLogger(__name__)


class RecognizeSpeech(Json):

	def post(self, request):


		request_data = request.POST
		audiofile = request.FILES.get('file')

		encoding = request_data.get('encoding')
		sampleRateHertz = request_data.get('sampleRateHertz')
		languageCode = request_data.get('languageCode')


		if audiofile is not None:
			pass

		return JsonResponse(
				{'message': 'Audio file was not specified.'},
				status=400
			)

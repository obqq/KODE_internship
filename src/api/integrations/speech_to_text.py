import json
import base64
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)


class GoogleSpeechToTextAPI:
	def __init__(self):
		self.API_KEY = settings.GOOGLE_SPEECH_API_KEY

	def send_request(self, data):
		try:
			URL = f'https://speech.googleapis.com/v1/speech:recognize?alt=json&key={self.API_KEY}'

			response = requests.post(URL, json=data)
			return response.json()

		except requests.exceptions.RequestException as e:
			logger.error(e)

	def encode_audio(self, audiofile):
		audio_content = audiofile.read()
		return base64.b64encode(audio_content)

	def recognize(self, audiofile, encoding, sample_rate_hertz, language_code):
		speech_content = self.encode_audio(audiofile)

		data = {
			'audio': {
				'content': speech_content.decode('UTF-8')
			},
			'config': {
				'encoding': encoding,
				'sampleRateHertz': sample_rate_hertz,
				'languageCode': language_code
			}
		}

		return self.send_request(data)
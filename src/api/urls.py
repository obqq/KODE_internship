from django.urls import path

from api import views


urlpatterns = [
	path('speech', views.RecognizeSpeech.as_view(), name='speech_recognition'),
]

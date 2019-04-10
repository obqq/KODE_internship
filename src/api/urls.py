from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, RecognizeSpeech

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('speech/', RecognizeSpeech.as_view(), name='speech')
]

urlpatterns += router.urls
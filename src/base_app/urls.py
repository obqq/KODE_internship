from django.urls import path, include

from base_app import views


urlpatterns = [
    path('health', views.HeartBeatHealthCheck.as_view(), name='common_healthcheck'),
]

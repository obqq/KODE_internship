from django.urls import path

from base_app import views


urlpatterns = [
    path('health/', views.HeartBeatHealthCheck.as_view(), name='common_healthcheck'),
]

from django.conf.urls import url

from base_project.common import views

urlpatterns = [
    url('health', views.HeartBeatHealthCheck.as_view(), name='common_healthcheck'),
]

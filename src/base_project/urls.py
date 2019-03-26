from django.conf.urls import include, url

urlpatterns = [
    url('common/', include('base_project.common.urls')),
]

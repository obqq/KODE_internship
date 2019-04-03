from django.conf.urls import include, url

urlpatterns = [
    url('base/', include('base_app.urls')),
]

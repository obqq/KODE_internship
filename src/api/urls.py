from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path(r'access_token', AccessToken.as_view()),
    path(r'refresh_token', RefreshToken.as_view()),
    path(r'public_key', PublicKey.as_view())
]

urlpatterns += router.urls

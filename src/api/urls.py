from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path(r'auth/access_token', AccessTokenView.as_view()),
    path(r'auth/refresh_token', RefreshTokenView.as_view()),
    path(r'auth/public_key', PublicKeyView.as_view())
]

urlpatterns += router.urls

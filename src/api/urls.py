
from django.urls import path

from api.views import (UserListView, CreateUserView, UserViewSet,
                       FollowViews, PittListView, PittViewSet,
                       AccessTokenView, RefreshTokenView, PublicKeyView)

urlpatterns = [
    path(r'users', UserListView.as_view()),
    path(r'users/create', CreateUserView.as_view()),
    path(r'users/<str:username>/', UserViewSet.as_view()),
    path(r'users/<str:username>/follows', FollowViews.as_view()),
    path(r'users/<str:username>/feed', PittListView.as_view()),
    path(r'users/<str:username>/pitts', PittViewSet.as_view()),
    path(r'auth/access_token', AccessTokenView.as_view()),
    path(r'auth/refresh_token', RefreshTokenView.as_view()),
    path(r'auth/public_key', PublicKeyView.as_view())
]

from django.urls import path

from api.views import (UserListView, UserCreateView, UserViews, FollowViews,
                       AccessTokenView, RefreshTokenView, PublicKeyView)

urlpatterns = [
    path(r'users', UserListView.as_view()),
    path(r'users/create', UserCreateView.as_view()),
    path(r'users/<str:username>/', UserViews.as_view()),
    path(r'users/<str:username>/follow', FollowViews.as_view()),
    path(r'auth/access_token', AccessTokenView.as_view()),
    path(r'auth/refresh_token', RefreshTokenView.as_view()),
    path(r'auth/public_key', PublicKeyView.as_view())
]


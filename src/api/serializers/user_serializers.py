import django.contrib.auth.password_validation as validators
from rest_framework import serializers

from api.models import User
from .follow_serializers import FollowerSerializer, TargetSerializer
from .pitt_serializers import PittSerializer


class UserSerializer(serializers.ModelSerializer):
    followers = FollowerSerializer(many=True)
    targets = TargetSerializer(many=True)
    pitts = PittSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'followers', 'targets', 'pitts')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.create_user(**validated_data)
        user.save()
        return user

    def validate_password(self, password):
        validators.validate_password(password=password, user=User)

        return password
